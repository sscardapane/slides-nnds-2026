"""Execute the drafts and check solution, student, and incorrect paths.

Usage: python verify_notebooks.py [--write-outputs]
Requires nbformat, nbclient, nbconvert, ipykernel and the notebook dependencies.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parent


def execute(nb):
    return NotebookClient(nb, timeout=180, kernel_name="nnds-validation",
                          resources={"metadata": {"path": str(ROOT)}}).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-outputs", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="nnds-validation-") as temp:
        root = Path(temp)
        kernel = root / "kernels" / "nnds-validation"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "NNDS validation", "language": "python"}))
        os.environ.update(JUPYTER_PATH=str(root), JUPYTER_RUNTIME_DIR=str(root / "runtime"),
                          IPYTHONDIR=str(root / "ipython"), MPLCONFIGDIR=str(root / "mpl"),
                          OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
        completed = {}
        clean_paths = [
            ROOT / "PT01_Introduction_to_PyTorch.ipynb",
            ROOT / "PT02_Logistic_regression_solutions.ipynb",
        ]
        for path in clean_paths:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            executed = execute(nb)
            assert not any(o.output_type == "error" for c in executed.cells
                           for o in c.get("outputs", []))
            completed[path.stem] = executed
            if args.write_outputs:
                # Keep a generic kernel name in the distributed notebooks.
                executed.metadata.kernelspec = {"name": "python3", "display_name": "Python 3", "language": "python"}
                nbformat.write(executed, path)
                html, _ = HTMLExporter().from_notebook_node(executed)
                path.with_suffix(".html").write_text(html)
            print("PASS clean execution:", path.name, flush=True)

        student_path = ROOT / "PT02_Logistic_regression.ipynb"
        student = nbformat.read(student_path, as_version=4)
        nbformat.validate(student)
        assert not any("reference" in c.metadata.get("tags", []) for c in student.cells)
        assert not any("def reference_" in c.source for c in student.cells if c.cell_type == "code")
        forward_checks = next(c.source for c in student.cells
                              if c.cell_type == "code" and c.source.startswith("small_X ="))
        step_checks = next(c.source for c in student.cells
                           if c.cell_type == "code" and c.source.startswith("# Compare two consecutive"))
        for cell in student.cells:
            if cell.cell_type != "code":
                continue
            cell.outputs = []
            cell.execution_count = None
            if cell.source.startswith("def linear_logits("):
                cell.source = cell.source.replace(
                    "    # Replace None with your batched computation.\n    return None",
                    "    return torch.addmm(b, X, W.T)", 1)
            if cell.source.startswith("def student_cross_entropy("):
                cell.source = cell.source.replace(
                    "    # Replace None with the batched loss.\n    return None",
                    "    selected = logits.gather(1, targets[:, None]).squeeze(1)\n"
                    "    return (torch.logsumexp(logits, dim=1) - selected).mean()", 1)
            if cell.source.startswith("def training_step("):
                cell.source = cell.source.replace(
                    "    # Replace None with your training step.\n    return None",
                    '''    model.zero_grad(set_to_none=True)
    loss = cross_entropy(model(X), y)
    loss.backward()
    with torch.no_grad():
        for p in model.parameters():
            p.add_(p.grad, alpha=-lr)
    return loss.item()''', 1)
        student.cells.append(nbformat.v4.new_code_cell('''
# Split isolation and train-only preprocessing.
assert not (set(train_idx) & set(val_idx) or set(train_idx) & set(test_idx) or set(val_idx) & set(test_idx))
assert set(train_idx) | set(val_idx) | set(test_idx) == set(range(len(y)))
torch.testing.assert_close(mean, X[train_idx].mean(dim=0))
torch.testing.assert_close(scale, X[train_idx].std(dim=0, correction=0))
assert history['train_loss'][-1] < history['train_loss'][0]
assert all(np.isfinite(history[k]).all() for k in history)
assert test_accuracy > baseline_accuracy
assert batch_sizes == [32] * 6 + [13]
assert mini_updates == 210
assert mini_history['train_loss'][-1] < mini_history['train_loss'][0]
assert selected_lr == min(learning_rates, key=lambda r: lr_histories[r]['val_loss'][-1])
assert model is lr_models[selected_lr]
# Full-size DataLoader batch must give the same parameter update.
a, b = copy.deepcopy(initial_model), copy.deepcopy(initial_model)
for bx, by in DataLoader(TensorDataset(Xtrain, ytrain), batch_size=len(ytrain)):
    run_step(a, bx, by, 0.1)
run_step(b, Xtrain, ytrain, 0.1)
for pa, pb in zip(a.parameters(), b.parameters()):
    torch.testing.assert_close(pa, pb)

# Exercise checks must reject plausible errors, not just accept the reference.
def must_fail(check):
    try:
        check()
    except (AssertionError, RuntimeError, TypeError):
        return
    raise AssertionError('The checks accepted an incorrect implementation')

saved_loss = student_cross_entropy
student_cross_entropy = lambda logits, targets: F.cross_entropy(logits, targets, reduction="sum")
def check_loss():
    z = torch.tensor([[2., -1., 0.], [0., 1., -2.]], requires_grad=True)
    t = torch.tensor([0, 2])
    torch.testing.assert_close(cross_entropy(z, t), F.cross_entropy(z, t))
must_fail(check_loss)
student_cross_entropy = saved_loss
saved_forward = linear_logits
linear_logits = lambda X, W, b: torch.zeros(X.shape[0], W.shape[0])
must_fail(lambda: exec(FORWARD_CHECKS, globals()))
linear_logits = saved_forward
saved_step = training_step
training_step = suspect_step
must_fail(lambda: exec(STEP_CHECKS, globals()))

def incomplete_step(model, X, y, lr):
    return None
training_step = incomplete_step
must_fail(lambda: run_step(LogisticRegression(4, 3), Xtrain, ytrain, 0.1))
training_step = saved_step
print('PASS student implementations, split isolation, and incorrect-code rejection')
'''.replace("FORWARD_CHECKS", repr(forward_checks)).replace("STEP_CHECKS", repr(step_checks))))
        execute(student)
        print("PASS student notebook has no references and accepts correct implementations", flush=True)
        if args.write_outputs:
            # Export the unfilled student source, never the injected verification copy.
            student_source = nbformat.read(student_path, as_version=4)
            html, _ = HTMLExporter().from_notebook_node(student_source)
            student_path.with_suffix(".html").write_text(html)


if __name__ == "__main__":
    main()
