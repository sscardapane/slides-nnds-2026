# PT01 and PT02: first revision

> [!note] Written by Codex (2026-09-14)

Separate local drafts for Simone's review. The original Colab notebooks and
Notion page were not modified. These copies propose a teaching format; the
instructor has not yet accepted the detailed content or policy on agent use.

## Files

- `PT01_Introduction_to_PyTorch.ipynb`: required preparation, with complete
  examples. Optional array operations and layout material follow the main path.
- `PT02_Logistic_regression.ipynb`: student lab with four activities: forward
  computation, loss, training, and investigation, followed by learning-rate
  and mini-batch experiments. It contains no reference implementations.
- `PT02_Logistic_regression_solutions.ipynb`: instructor copy with the four
  reference cells and runnable fallbacks.
- Matching `.html` files: reading previews; use the notebooks to edit or run
  code.
- `make_student_notebook.py`: reproducibly rebuilds the student notebook from
  the solutions notebook while removing the reference cells and fallbacks.
- `data/penguins.csv`: unscaled Palmer Penguins data, supplied for offline use.
- `verify_notebooks.py`: reproducible execution and exercise-path checks.

Open the folder in Jupyter and select the notebook, so `data/penguins.csv` is
available relative to it. The notebook and data folder travel together. When
PT02 is opened alone in Colab, it downloads the dataset from the source and
checks its SHA-256. If the remote file changes, use the bundled file instead.
PT01 requires PyTorch. PT02 also uses NumPy, pandas, scikit-learn and Matplotlib.
An environment without these packages can install `requirements.txt`.

## Proposed teaching format

PT01 can be read and run from top to bottom without filling gaps. The core
ends after the classification example. The optional examples preserve the
original diagonal, normalization and cosine-similarity exercises as worked
examples, with explicit edge cases.

PT02 supplies data handling, plotting, the model class and accuracy.
Students write the batched forward pass, a stable cross-entropy loss and the training step, then investigate
a step that unintentionally accumulates gradients. The student notebook stops
with a clear error when an activity is unfinished. Reference implementations
and automatic fallbacks exist only in the solutions notebook; they are not
present in the student `.ipynb` or its HTML preview.
PT01 closes its required portion with a readiness check on broadcasting,
gradient accumulation and shapes, with expandable answers.

PT02 compares three learning rates from identical initial parameters over
200 full-batch updates, selecting the final model by validation loss. A separate
30-epoch mini-batch extension uses batches of 32, including a final batch of 13,
and compares equal epoch counts while explaining the unequal update counts.
Both notebooks use jaxtyping annotations with torch.Tensor at function boundaries;
annotations document shapes without enabling runtime checking.

The agent-use paragraph is a proposal: students document a hypothesis and test
suggestions against observed behavior. It does not establish a course-wide
assessment or tool policy. Reference availability, the amount of provided
code, timing, and this paragraph should be discussed in the next review.

## Changes relative to the sources

| Source material | Treatment in these copies |
| --- | --- |
| PT01 tensor introduction and indexing | Condensed around batch and feature axes and a batched linear model. |
| Storage pointers and strides | Optional, using visible mutation to explain views/copies and a short stride example; deprecated typed-storage calls removed. |
| Diagonal, normalization and cosine exercises | Optional worked examples with known-answer checks; constant and zero-vector conventions stated. |
| Profiler and compilation interlude | Deferred to performance material; no claim that compilation guarantees a speedup. |
| Autodiff | Retained with explicit leaf behavior, gradient accumulation, fresh forward passes, updates under `no_grad`, and detached logging. |
| Backward-node traversal/counting cosines | Deferred to the later autodiff unit; no private graph attributes in the required path. |
| PT02 penguin classification | Retained. Uses four unscaled numeric measurements with a fixed stratified split. |
| Pre-normalized CSV | Replaced by the dataset maintainers' unscaled CSV; normalization uses the training split only. No claim that leakage in the old CSV was established. |
| Model, loss, accuracy, training TODOs | Regrouped into four activities, with continuous runnable sections and reference fallbacks. |
| Probability-based cross-entropy | Logits-based implementation, checked against built-in loss values and gradients. |
| Training curves only | Adds validation curves, a diagnostic comparison, final test evaluation, a majority-class baseline, and a confusion matrix. |
| Framework syntax and shape annotations | Restored jaxtyping at function boundaries after instructor review, using torch.Tensor rather than the JAX-specific Array alias. Shapes remain in prose/comments too. |

The original informal, direct style informed the prose. Student-facing text was
reviewed with the humanizer skill in embedded mode. No MLP extension or new
slide content was implemented.

## Sources and data

- [PT01 original](https://colab.research.google.com/drive/1c1i33VUSYFb-4uGbOjBiC2XL4DnEFtxc)
- [PT02 original](https://colab.research.google.com/drive/1SKrfuCplKsDqQYgLalCPlCiYLCgJ-4Ht)
- [Notion index](https://app.notion.com/p/18c25bd12a8c8068b972f7612fcde8d5)
- [Palmer Penguins source](https://allisonhorst.github.io/palmerpenguins/)

The notebook sources were read earlier in this conversation and their Drive
metadata rechecked before revision; both modification times remain 2025-03-10.
The dataset was downloaded on 2026-09-14 from
`https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv`.
SHA-256: `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`.
Data are CC0. Attribution: Horst, Hill and Gorman (2020), palmerpenguins;
original collection by Kristen Gorman and Palmer Station LTER. The notebook
removes only the two rows missing the selected measurements; it keeps 342
examples split into 205 training, 68 validation and 69 test examples. This is a
random within-dataset evaluation, not an island/year generalization study.

## Verification

Run `python verify_notebooks.py` from an environment containing the notebook
packages plus `nbformat`, `nbclient`, `nbconvert` and `ipykernel`. Add
`--write-outputs` to refresh saved outputs and HTML previews. The script starts
temporary local Jupyter kernels using the Python executable that invoked it.

The updated pass was checked on CPU with Python 3.9, PyTorch 2.3.0, jaxtyping 0.2.36, NumPy 1.26.4,
pandas 2.3.3, scikit-learn 1.6.1 and Matplotlib 3.8.3. Notebook checks use
nbformat 5.10.4, nbclient 0.10.2 and nbconvert 7.17.1. The notebooks have not
been run in Colab or on a GPU.

The validation covers clean execution of both notebooks, filled student
implementations, split isolation, train-only scaling, agreement with PyTorch,
and rejection of incorrect forwards, uncleared gradients and partially
completed updates. It also checks the loss exercise, mini-batch counts, validation-based
selection and full-size-batch update equivalence. Plot inspection covers data, training/validation curves and
the diagnostic comparison. The seeded reference run reports validation
accuracy 68/68 for the selected learning rate (10.0), and test accuracy 67/69, compared with a test majority baseline
of 31/69. These are example results, not thresholds students must reproduce to
receive credit.
