"""Build the PT02 student notebook from the solutions notebook."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOLUTIONS = ROOT / "PT02_Logistic_regression_solutions.ipynb"
STUDENT = ROOT / "PT02_Logistic_regression.ipynb"


def lines(text):
    return text.splitlines(keepends=True)


def cell_by_id(notebook, cell_id):
    return next(cell for cell in notebook["cells"] if cell.get("id") == cell_id)


def main():
    notebook = json.loads(SOLUTIONS.read_text())

    reference_ids = {
        cell["id"]
        for cell in notebook["cells"]
        if "reference" in cell.get("metadata", {}).get("tags", [])
    }
    expected_reference_ids = {"d4bcbb0d", "f90a471e", "7b7b80ce", "21fe67f8"}
    if reference_ids != expected_reference_ids:
        raise RuntimeError(
            "The set of reference cells changed; review the student export before rebuilding."
        )
    notebook["cells"] = [
        cell for cell in notebook["cells"] if cell.get("id") not in reference_ids
    ]

    cell_by_id(notebook, "b8ce2774")["source"] = lines(
        """# PT02: Logistic regression in PyTorch

Given a few measurements of a penguin, can we predict its species? We will build a linear classifier and follow its training through to evaluation.

Read PT01 before this session. We will use its tensor operations, `backward()`, and parameter updates. The data loading and plotting code are provided. There are four activities: the forward pass, the loss, the training step, and an investigation of a training run. We then compare learning rates and extend training to mini-batches.

This is the student notebook. Complete each activity before continuing; an unfinished activity raises a clear error instead of silently using a reference implementation. Worked solutions are kept in the separate instructor notebook.

> Try to avoid AI coding assistants for these simple exercises."""
    )

    cell_by_id(notebook, "81f5c4d5")["source"] = lines(
        '''def linear_logits(X: Float[torch.Tensor, "batch features"], W: Float[torch.Tensor, "classes features"], b: Float[torch.Tensor, "classes"]) -> Optional[Float[torch.Tensor, "batch classes"]]:
    # Replace None with your batched computation.
    return None

def forward_logits(X: Float[torch.Tensor, "batch features"], W: Float[torch.Tensor, "classes features"], b: Float[torch.Tensor, "classes"]) -> Float[torch.Tensor, "batch classes"]:
    result = linear_logits(X, W, b)
    if result is None:
        raise NotImplementedError("Complete Activity 1 before continuing.")
    return result'''
    )

    cell_by_id(notebook, "c36491ad")["source"] = lines(
        '''small_X = torch.tensor([[1., 2.], [3., 4.]])
small_W = torch.tensor([[1., 0.], [0., 1.], [-1., 1.]])
small_b = torch.tensor([0.5, -0.5, 1.])
expected = torch.tensor([[1.5, 1.5, 2.], [3.5, 3.5, 2.]])
torch.testing.assert_close(forward_logits(small_X, small_W, small_b), expected)
print("Forward-pass check passed.")'''
    )

    cell_by_id(notebook, "97278cda")["source"] = lines(
        '''def student_cross_entropy(logits: Float[torch.Tensor, "batch classes"], targets: Int[torch.Tensor, "batch"]) -> Optional[Float[torch.Tensor, ""]]:
    # Replace None with the batched loss.
    return None

def cross_entropy(logits: Float[torch.Tensor, "batch classes"], targets: Int[torch.Tensor, "batch"]) -> Float[torch.Tensor, ""]:
    result = student_cross_entropy(logits, targets)
    if result is None:
        raise NotImplementedError("Complete Activity 2 before continuing.")
    return result'''
    )

    cell_by_id(notebook, "fefd076e")["source"] = lines(
        '''def accuracy(logits: Float[torch.Tensor, "batch classes"], targets: Int[torch.Tensor, "batch"]) -> Float[torch.Tensor, ""]:
    return (logits.argmax(dim=1) == targets).float().mean()

logits = model(Xtrain)
print("Initial loss:", cross_entropy(logits, ytrain).item())
print("Initial accuracy:", accuracy(logits, ytrain).item())
# Zero logits give uniform probabilities and loss log(C).
torch.testing.assert_close(cross_entropy(logits, ytrain), torch.tensor(float(np.log(3))))
print("Initial-loss check passed.")'''
    )

    cell_by_id(notebook, "05b55ab1")["source"] = lines(
        '''def training_step(model: torch.nn.Module, X: Float[torch.Tensor, "batch features"], y: Int[torch.Tensor, "batch"], lr: float) -> Optional[float]:
    # Replace None with your training step.
    return None

def run_step(model: torch.nn.Module, X: Float[torch.Tensor, "batch features"], y: Int[torch.Tensor, "batch"], lr: float) -> float:
    result = training_step(model, X, y, lr)
    if result is None:
        raise NotImplementedError("Complete Activity 3 before continuing.")
    if not isinstance(result, float):
        raise TypeError("Return loss.item(), not a tensor.")
    return result

@torch.no_grad()
def evaluate(model, X, y):
    model.eval()
    logits = model(X)
    return cross_entropy(logits, y).item(), accuracy(logits, y).item()'''
    )

    cell_by_id(notebook, "e0e04805")["source"] = lines(
        '''# Compare two consecutive updates: the second detects uncleared gradients.
check_model = LogisticRegression(4, 3)
first_loss = run_step(check_model, Xtrain[:16], ytrain[:16], 0.1)
before_second = [parameter.detach().clone() for parameter in check_model.parameters()]
expected_second_loss = cross_entropy(check_model(Xtrain[:16]), ytrain[:16])
expected_second_gradients = torch.autograd.grad(expected_second_loss, tuple(check_model.parameters()))
second_loss = run_step(check_model, Xtrain[:16], ytrain[:16], 0.1)
assert abs(second_loss - expected_second_loss.item()) < 1e-6
for parameter, before, expected_gradient in zip(check_model.parameters(), before_second, expected_second_gradients):
    torch.testing.assert_close(parameter.grad, expected_gradient)
    torch.testing.assert_close(parameter, before - 0.1 * expected_gradient)
print("Both updates passed the checks.")'''
    )

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    STUDENT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    print(f"Wrote {STUDENT.name} without {len(reference_ids)} reference cells.")


if __name__ == "__main__":
    main()
