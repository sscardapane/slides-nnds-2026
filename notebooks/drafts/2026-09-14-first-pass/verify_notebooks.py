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
from make_student_notebook import build_pt01, build_pt02, clear_execution

ROOT = Path(__file__).resolve().parent


def execute(nb):
    return NotebookClient(nb, timeout=180, kernel_name="nnds-validation",
                          resources={"metadata": {"path": str(ROOT)}}).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-outputs", action="store_true")
    args = parser.parse_args()
    for name, generated in [("PT01_Introduction_to_PyTorch", build_pt01()),
                            ("PT02_Logistic_regression", build_pt02())]:
        actual = clear_execution(json.loads((ROOT / f"{name}.ipynb").read_text()))
        assert actual == generated, f"Rebuild {name} from its instructor source"
        assert not any("reference" in c.get("metadata", {}).get("tags", []) for c in actual["cells"])
        print("PASS generated student source:", name, flush=True)
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
            ROOT / "PT01_Introduction_to_PyTorch_solutions.ipynb",
            ROOT / "PT02_Logistic_regression_solutions.ipynb",
        ]
        for path in clean_paths:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            if path.stem == "PT02_Logistic_regression_solutions":
                nb.cells.append(nbformat.v4.new_code_cell('''
# Verify the instructor experiment without distributing this test cell.
assert len(image_runs) == 4
assert not (image_train_mask & image_heldout_mask).any()
assert (image_train_mask | image_heldout_mask).all()
for (encoding, width), (coordinate_model, trace, snapshots) in image_runs.items():
    assert set(snapshots) == {0, 100, 400}
    assert trace['update'][0] == 0 and trace['update'][-1] == 400
    assert trace['train_mse'][-1] < trace['train_mse'][0]
    assert all(np.isfinite(trace[key]).all() for key in ['train_mse', 'heldout_mse'])
    assert not coordinate_model.frequencies.requires_grad
    assert 'frequencies' not in dict(coordinate_model.named_parameters())
    assert 'frequencies' in coordinate_model.state_dict()
    if encoding == 'Fourier':
        expected_frequencies = 1.5 * torch.randn(16, 2, generator=torch.Generator().manual_seed(7))
        torch.testing.assert_close(coordinate_model.frequencies, expected_frequencies)
    output = coordinate_model(coordinate_grid(64))
    assert output.shape == (4096, 3) and torch.isfinite(output).all()
    assert ((output >= 0) & (output <= 1)).all()
    with torch.no_grad():
        heldout_mse = F.mse_loss(coordinate_model(image_coordinates[image_heldout_mask]), image_rgb[image_heldout_mask])
    np.testing.assert_allclose(heldout_mse.item(), trace['heldout_mse'][-1], rtol=1e-5)
assert image_summary['float32 payload bytes'].tolist() == [1484, 5004, 3532, 8972]
assert model is lr_models[selected_lr]
print('PASS image reference: four fits, held-out metrics, fixed buffers, payloads and dense queries')
''', id="instructor-verification"))
            executed = execute(nb)
            assert not any(o.output_type == "error" for c in executed.cells
                           for o in c.get("outputs", []))
            if executed.cells[-1].id == "instructor-verification":
                executed.cells.pop()
                print("PASS image reference experiment and storage accounting", flush=True)
            completed[path.stem] = executed
            if args.write_outputs and path.stem.endswith("_solutions"):
                # Keep a generic kernel name in the distributed notebooks.
                executed.metadata.kernelspec = {"name": "python3", "display_name": "Python 3", "language": "python"}
                nbformat.write(executed, path)
                html, _ = HTMLExporter().from_notebook_node(executed)
                path.with_suffix(".html").write_text(html)
            print("PASS clean execution:", path.name, flush=True)

        # Execute the displayed PT01 answers, then check that their assertions
        # distinguish the intended computations from the runnable mistakes.
        pt01 = completed["PT01_Introduction_to_PyTorch_solutions"]
        snippets = [c.source for c in pt01.cells if c.id.startswith("tensor-challenge-solutions-code-")]
        assert len(snippets) == 3
        setups = [next(c.source for c in pt01.cells
                       if c.id == f"tensor-challenge-{i}-code") for i in range(1, 4)]
        checks = nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_code_cell("import torch"),
            nbformat.v4.new_code_cell("\n\n".join(setups + snippets)),
            nbformat.v4.new_code_cell('''
def must_reject(actual, expected):
    try:
        torch.testing.assert_close(actual, expected)
    except AssertionError:
        return
    raise AssertionError("The check accepted the original tensor-semantics bug")

must_reject(suspect_errors, torch.tensor([1., 0., -1.]))
must_reject(suspect_mse, torch.tensor(2. / 3.))
assert suspect_predictions.shape == row_predictions.shape
must_reject(suspect_predictions, torch.tensor([21., 43.]))
assert suspect_centered.shape == feature_centered.shape
must_reject(suspect_centered, torch.tensor([[-2., -10.], [0., 0.], [2., 10.]]))
must_reject(suspect_centered.mean(dim=0), torch.zeros(2))
try:
    larger_batch.T @ weights
except RuntimeError:
    pass
else:
    raise AssertionError("The transposed three-example batch should fail")
single_error = predictions[:1].squeeze(-1) - targets[:1]
assert single_error.shape == (1,)
torch.testing.assert_close(single_error, torch.tensor([1.]))
''')])
        execute(checks)
        print("PASS PT01 displayed solutions and rejection of all three original bugs", flush=True)

        repairs = [c.source for c in pt01.cells if c.id.startswith("autograd-detective-solutions-code-")]
        assert len(repairs) == 4
        cases = [next(c.source for c in pt01.cells if c.id == f"autograd-case-{i}")
                 for i in range(1, 5)]
        original_checks = '''
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    assert hidden.grad is None
torch.testing.assert_close(leaf.grad, torch.tensor([18., 36.]))
assert restart.is_leaf and restart.grad_fn is None and original.grad is None
torch.testing.assert_close(restart.grad, torch.tensor([6., 12.]))
torch.testing.assert_close(parameter.grad, torch.tensor(28. / 3.))

def must_raise_runtime_error(fn):
    try:
        fn()
    except RuntimeError:
        return
    raise AssertionError("Expected autograd to reject this operation")

must_raise_runtime_error(stale_loss.backward)
alias_source = torch.tensor([1., 2.], requires_grad=True)
alias_loss = alias_source.square().sum()
alias_source.detach().add_(1.)
must_raise_runtime_error(alias_loss.backward)

# None differs from a computed zero gradient.
zero_leaf = torch.tensor(0., requires_grad=True)
assert zero_leaf.grad is None
zero_leaf.square().backward()
torch.testing.assert_close(zero_leaf.grad, torch.tensor(0.))

# Retaining an intermediate gradient does not retain the graph.
graph_leaf = torch.tensor([1., 2.], requires_grad=True)
intermediate = 3 * graph_leaf
intermediate.retain_grad()
graph_loss = intermediate.square().sum()
graph_loss.backward()
assert intermediate.grad is not None and graph_loss.grad_fn is not None
must_raise_runtime_error(graph_loss.backward)

# Conversely, retaining the graph still accumulates leaf gradients.
graph_leaf = torch.tensor([1., 2.], requires_grad=True)
graph_loss = graph_leaf.square().sum()
graph_loss.backward(retain_graph=True)
graph_loss.backward()
torch.testing.assert_close(graph_leaf.grad, torch.tensor([4., 8.]))

unequal_parameter = torch.tensor(1., requires_grad=True)
for values in microbatches:
    ((unequal_parameter * values).square().mean() / len(microbatches)).backward()
torch.testing.assert_close(unequal_parameter.grad, torch.tensor(11.5))
'''
        execute(nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_code_cell("import torch"),
            nbformat.v4.new_code_cell("\n\n".join(cases)),
            nbformat.v4.new_code_cell(original_checks),
            nbformat.v4.new_code_cell("\n\n".join(repairs)),
        ]))
        print("PASS PT01 autograd diagnoses, displayed repairs, and graph lifetime checks", flush=True)

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
# The optional diagnostic preserves the data and trained classifier.
torch.testing.assert_close(analysis_y, ytrain)
for diagnostic_parameter, saved_parameter in zip(analysis_model.parameters(), lr_models[0.1].parameters()):
    torch.testing.assert_close(diagnostic_parameter, saved_parameter.double())
assert all(parameter.grad is None for parameter in analysis_model.parameters())
assert per_example_loop.shape == (len(ytrain), 15)
torch.testing.assert_close(per_example_loop, per_example_transformed)
torch.testing.assert_close(per_example_transformed.mean(dim=0), mean_gradient)
assert torch.isfinite(clean_alignment).all()
assert clean_alignment.abs().max() <= 1 + 1e-10
assert torch.isnan(gradient_alignment(torch.zeros_like(per_example_loop[:1]), mean_gradient)).all()
assert torch.isnan(gradient_alignment(per_example_loop[:1], torch.zeros_like(mean_gradient))).all()
changed_tree = all_gradients(analysis_state, analysis_X[easy_index:easy_index + 1], changed_label)
changed_flat = torch.cat([changed_tree[name].reshape(-1) for name in analysis_parameter_names])
torch.testing.assert_close(changed_flat, changed_gradient)
assert changed_label.item() != analysis_y[easy_index].item()
print('PASS per-example gradients, corrupted-label equivalence and zero-vector handling')
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
        print("PASS student implementations, per-example gradients and diagnostic isolation", flush=True)
        if args.write_outputs:
            # Execution can update instructor kernel metadata. Regenerate the
            # unfilled sources from that final state, never from the test copy.
            for source_path, generated in [(ROOT / "PT01_Introduction_to_PyTorch.ipynb", build_pt01()),
                                           (student_path, build_pt02())]:
                source_path.write_text(json.dumps(generated, indent=1, ensure_ascii=False) + "\n")
                student_source = nbformat.read(source_path, as_version=4)
                html, _ = HTMLExporter().from_notebook_node(student_source)
                source_path.with_suffix(".html").write_text(html)


if __name__ == "__main__":
    main()
