# PT01 and PT02: shared course notebooks

> [!note] Written by Codex (2026-09-14)

PT01 and PT02 are maintained here as one shared set for all courses, including
NN and NNDS (Simone's decision, October 1, 2026). Lectures can select different
sections from the same notebooks; additions do not require course-specific copies.
The directory retains its original draft name for stable links. The original Colab
notebooks and Notion page were not modified. This choice does not establish a
course-wide policy on agent use.

## Files

- `PT01_Introduction_to_PyTorch.ipynb`: required preparation, with complete
  examples, including a walkthrough of a tensor's autograd attributes.
  Optional tensor-semantics and autograd exercises, array operations and layout
  material follow the main path. Exercise answers are in the instructor notebook.
- `PT01_Introduction_to_PyTorch_solutions.ipynb`: instructor source with readiness
  answers, tensor-semantics solutions and autograd diagnoses as executable cells.
- `PT02_Logistic_regression.ipynb`: student lab with four activities: forward
  computation, loss, training, and investigation, followed by learning-rate
  and mini-batch experiments. An optional per-example-gradient demonstration and
  a coordinate-to-RGB reader exercise follow the core. It contains no exercise
  reference implementations.
- `PT02_Logistic_regression_solutions.ipynb`: instructor copy with the four
  core references and runnable fallbacks, discussion notes for the gradient
  diagnostic, and a complete coordinate-MLP reference experiment.
- Matching `.html` files: reading previews; use the notebooks to edit or run
  code.
- `make_student_notebook.py`: reproducibly rebuilds both student notebooks from
  the instructor sources, removing reference cells, fallbacks and saved outputs.
  Use `--check` to verify that the generated sources are current. Edit instructor
  notebooks first; shared code and prose belong there, with instructor-only
  cells tagged `reference`.
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
gradient accumulation and shapes. Answers and runnable exercise repairs live
in its instructor notebook. The explanatory worked examples stay in both versions.

The optional tensor-semantics section implements item 25 of the shared additions
menu: students predict, diagnose and repair a broadcasted regression error, a
transposed batch and centering over the wrong axis. Each uses hand-checkable
values and asks for assertions that reject the original computation. The section
can also be used after Section 2; it needs no autograd or PT02 material.

Item 26 extends Sections 3 and 4 with a tensor-level view of autograd:
`requires_grad`, `is_leaf`, `grad_fn`, `grad`, and `retains_grad`, followed by
`retain_grad()`, graph lifetime, `detach()` and `no_grad()`. Worked examples show
the attributes before and after backward. Four optional detective cases ask
students to explain missing intermediate gradients, a detached new leaf,
intentional accumulation over unequal microbatches, and an in-place mutation
before backward. Instructor diagnoses and executable repairs follow the exercises.
The verifier executes those answers and checks the failures, accumulation weights,
shared storage after detaching, and the distinction between retaining gradients
and retaining the graph. The prose follows the linked PyTorch documentation and
received the same humanizer pass as the other student-facing material.

PT02 compares three learning rates from identical initial parameters over
200 full-batch updates, selecting the final model by validation loss. A separate
30-epoch mini-batch extension uses batches of 32, including a final batch of 13,
and compares equal epoch counts while explaining the unequal update counts.
Both notebooks use jaxtyping annotations with torch.Tensor at function boundaries;
annotations document shapes without enabling runtime checking.

Item 34 is an optional worked diagnostic using the fixed 200-update, learning-rate
0.1 snapshot and training data only. It compares a transparent `autograd.grad`
loop with `functional_call`, `grad` and `vmap`, verifies that their mean equals the
batch gradient, and plots gradient norm and alignment for original and deliberately
changed labels. No model is retrained or selected using this diagnostic.

Item 36 is a reader exercise for after the MLP lecture. Students receive a small
generated image, a fixed observed/held-out pixel split and a comparison brief.
Only the instructor notebook implements the four prescribed raw/Fourier and
width-16/32 runs, with checkpoints, curves, parameter counts, float32 payload sizes
including frequency buffers, and dense coordinate queries. The reference runs on
CPU without a download. It is a teaching comparison, not an image-codec benchmark.

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
reviewed with the humanizer skill in embedded mode. The optional coordinate-MLP
exercise is separate from the logistic-regression core. No slide content changed.

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
`--write-outputs` to refresh instructor outputs, regenerate the unfilled student
sources and refresh all four HTML previews. The script starts
temporary local Jupyter kernels using the Python executable that invoked it.

The updated pass was checked on CPU with Python 3.9, PyTorch 2.3.0, jaxtyping 0.2.36, NumPy 1.26.4,
pandas 2.3.3, scikit-learn 1.6.1 and Matplotlib 3.8.3. Notebook checks use
nbformat 5.10.4, nbclient 0.10.2 and nbconvert 7.17.1. The notebooks have not
been run in Colab or on a GPU.

The validation covers clean execution of both notebooks, filled student
implementations, split isolation, train-only scaling, agreement with PyTorch,
and rejection of incorrect forwards, uncleared gradients and partially
completed updates. It executes the displayed PT01 exercise solutions and checks
that they reject all three original mistakes, including cases where shapes match.
It also checks the loss exercise, mini-batch counts, validation-based
selection and full-size-batch update equivalence. Plot inspection covers data, training/validation curves and
the diagnostic comparison. The seeded reference run reports validation
accuracy 68/68 for the selected learning rate (10.0), and test accuracy 67/69, compared with a test majority baseline
of 31/69. These are example results, not thresholds students must reproduce to
receive credit.

The October 1 tensor-semantics addition passed the full verifier on CPU with
Python 3.12.4, PyTorch 2.14.1, jaxtyping 0.3.11, NumPy 2.5.3, pandas 3.0.6,
scikit-learn 1.9.1 and Matplotlib 3.11.2 (nbformat 5.11.1, nbclient 0.11.0,
nbconvert 7.17.1, ipykernel 7.4.0). All notebook and exercise checks passed;
the sandbox reported process-inspection warnings during kernel shutdown.
The PT01 HTML preview was regenerated and its collapsed solution blocks checked.
Saved example outputs from the earlier pass were retained; the new exercise
cells have no saved outputs so students can predict them before execution.
The subsequent item 26 pass uses the same environment and saves outputs for the
new guided autograd examples while leaving the detective cells unexecuted in the
distributed notebook. The full verifier also runs those cells in fresh kernels.

The item 34/36 pass moves PT01 exercise answers into a separate executable
instructor notebook and generates both student sources without saved outputs.
The full verifier checks both instructor notebooks, PT01's student path and
completed PT02 student implementations. It checks loop/transform agreement,
mean-gradient equivalence, label-change isolation, zero-vector alignment handling,
fixed Fourier buffers, held-out image metrics and storage accounting. All four
image configurations improve their training MSE; no particular held-out ranking
is required to pass. Plot review covers the gradient diagnostic, sparse image
samples, reconstruction checkpoints, learning curves and dense queries.

The October 1 readability pass rewrote the markdown of both instructor notebooks
and the generated student introductions for shorter, plainer prose; code cells
are unchanged. Required and optional parts of PT01 are now signposted, including
the two optional autograd subsections inside Sections 3 and 4. PT02 gains one
discussion cell after the learning-rate comparison: the training set is linearly
separable or nearly so, so the largest rate (10.0) wins and students are pointed to
larger rates to see the unstable first updates. Corrected the PT01 reason for
updating under `no_grad`: in-place updates of leaves that require gradients are
refused outside it. The full verifier passed with the October 1 environment, and
the cited reference results did not change.

Follow-up (Simone, October 1): PT01's tensor-level autograd material (attribute
table, `x -> h -> o` walkthrough, graph lifetime, cutting a connection) moved out
of Sections 3 and 4 into an optional "closer look at autograd" section just
before the autograd detective, so the required path runs straight through
Sections 1 to 5. Detective case 3 stays. In PT02 both closing sections are
optional, with the image exercise last and framed as reusing the lab's training
loop with an MLP; its storage and extrapolation questions are now an extension.
A learning-rate instability demonstration belongs to the MLP material, since the
penguin data cannot show one.

PT02 Section 9 (Simone, October 1) trains a one-hidden-layer MLP on the penguins
with the unchanged `fit`/`training_step` code, for use after the MLP lecture.
Two questions, with instructor answers and asserted reference runs, show what
the linear model hid: `lr=10` makes the MLP's loss explode (about 2e5 in the
recorded run, NaN at 30), and zero initialization leaves every weight at zero,
so only the output bias learns. The image exercise now builds on this section.
