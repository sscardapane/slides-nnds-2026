# NNDS Slide Refresh

Migrated from the vault's NNDS procedure on 2026-09-19. The repository owns
this guidance; the vault keeps project context and links. Preserve the already
approved unit scope, format, review mode and instructor decisions.

## When To Use

Use when the task is to revise, narrate, audit, or format a specific NNDS
2026 unit ("avviare la revisione del primo argomento NNDS 2026", "narrative
pass su Lecture N").

## Open decisions

- **Labs:** decide the concrete format only when revising the first lab. The
  direction is PyTorch as the main framework, with one purposeful JAX lab.

## Course-wide editorial commitments

- **Readable and accessible by default:** use generously sized type, clear
  hierarchy, legible fonts, and reliable foreground/background contrast. Do
  not accept clipped, crowded, low-contrast, or color-only explanations;
  render and inspect the final deck rather than treating compilation as enough.
- **Beautiful by design:** a refresh should improve the composition, not merely
  make every element fit. Use deliberate margins, balanced text blocks,
  meaningful whitespace, strong alignment, and restrained but informative
  color. Equations should retain or improve the source deck's visual
  structure—for example, coloring corresponding terms or annotating the part
  currently being discussed. Do not flatten a carefully designed LaTeX slide
  into undifferentiated black text simply because the HTML version compiles.
- **Reuse the Lecture 3 visual grammar:** blue marks definitions and quantities
  we can compute; green marks goals, conditions, or stable formulations; orange
  marks warnings and trade-offs; red is reserved for training-specific or
  genuinely problematic elements. Parallel cards must have equal height. A
  colored box contains a complete definition, condition, or takeaway—never an
  isolated equation used as decoration. Keep prose justified, figures
  transparent against the slide canvas, and enough unboxed whitespace that the
  deck does not become a wall of panels. Leave strong visual anchor slides
  visually distinct rather than forcing the card system everywhere.
- **Make room for material that earns its place:** trim unnecessary slides,
  duplicated exposition, and incidental detail before adding new content.
  Increase the material where a clearer intuition, a useful modern connection,
  or an experiment materially improves the course story.
- **Keep the instructor's voice:** write direct, course-specific prose that
  sounds natural when spoken aloud. Avoid generic pedagogical scaffolding and
  other recognisable LLM artefacts.
- **Connect teaching to live research:** when it fits the unit, make the
  relevant SNAIL topics, papers, projects, and thesis/PhD paths visible to
  students. This should be a real connection, not a generic promotional slide.

## For each unit: two broad passes first

First identify the authoritative source deck. Then complete and approve two
separate broad passes before changing individual slides.

### Broad pass 1 — content and narrative

Decide:

1. The central topic and where it belongs in the course story.
2. What it follows, what it unlocks, and whether it should move as a whole.
3. Which intuitions benefit from explicit explanation, a figure or a demonstration. Do not propose live board derivations: this course uses autodiff rather than hand derivation.
4. The one or two intuitions students should carry away, especially when the
   material is otherwise empirical.
5. Where a dynamic demo (a slider-driven plot, a live-trained toy model, a
   runnable code cell, an explorable pattern) would teach a point better than
   a static figure or the board — sketch each candidate in one line (what
   varies, what the viewer should notice). Most units have zero or one or
   two of these; treat it as a brainstorm alongside the content moves, not a
   default to reach for on every slide. See the
   `vault: Workflows/State/NNDS Slide Refresh Log#2026-07-20 — HTML pilot — Lecture 1` (HTML pilot)
   for what these concretely look like (optimization dynamics, attention
   patterns, vanishing gradients, decision boundaries, ...).

Do not create formal learning-outcome lists. The aim is a coherent story from
MLPs and differentiable models, through data structure and architecture, to the
final transition from a pre-trained LLM to an actual agent.

### Broad pass 2 — form and delivery

Decide the unit-wide presentation choices before discussing individual slide
layouts:

1. LaTeX/HTML split, using the format rules below.
2. Target duration, slide count, and overall density.
3. Typography, prose alignment, margins, and the visual grammar for boxes,
   columns, equations, and color.
4. Which figures remain, which need native-source edits, and which slides
   should stay visually distinct as anchors.
5. The role of code, static figures and interactive demonstrations.

Approve both broad passes explicitly. Do not let the slide-by-slide review
quietly reopen the unit's scope or visual system; if either broad decision must
change, pause and re-approve that change before propagating it.

## Lock the refresh contract before implementation

A refresh is not a rewrite. After the two broad passes, choose one review mode:

1. **Ledger-first mode** — use for autonomous work, broad rewrites, or whenever
   the instructor asks to approve the complete plan before implementation.
   Finish the numbered brainstorming list, map every approved edit to the
   affected source slides, and account for every original slide before editing.
2. **Rolling-review mode** — use for a live instructor session when the
   instructor prefers to inspect the deck continuously. Discuss one edit using
   the slide title and visible content rather than requiring slide-number
   recall; implement and render it immediately; record whether it was accepted,
   revised, or reverted; then proceed to the next edit. Keep the decision trail
   in Git and reconstruct the complete preservation audit at the end.
3. **Final coverage approval** — in either mode, compare the final source and
   render with the authoritative deck. In rolling mode, present only the
   reconstructed moves, removals, additions, and unresolved anomalies unless
   the instructor asks for the full slide-by-slide ledger. Every removal still
   requires explicit consent, and later feedback must not silently undo an
   accepted decision.

Classify every visual edit before implementation:

- **system-level** — a reusable change to a slide type or shared component
  (typography, margins, equation treatment, panels, headers, controls); record
  its full blast radius and approve propagation separately;
- **slide-specific** — a local change to one named slide or an explicitly
  listed finite set of slides.

After an edit is accepted, commit that narrow change before beginning the next
materially different content block. Several micro-edits to the same slide may
share one checkpoint after the instructor accepts the result. Use Git to
compare and revert candidates; do not maintain parallel staged copies of the
deck. Preserve unrelated working-tree changes and stage only the approved edit.

The final coverage record uses exactly one preservation status per original
slide. In ledger-first mode this is the approved ledger; in rolling mode it is
reconstructed during the final audit:

1. **leave** — preserve the slide essentially verbatim;
2. **light edit** — apply only the explicitly agreed correction;
3. **substantial edit** — the user has approved changing the slide's structure
   or explanation;
4. **move** — preserve the material but relocate it;
5. **remove** — requires explicit consent;
6. **add** — a new, explicitly accepted slide or demo.

Record every accepted brainstorming decision in the decision trail. In
ledger-first mode, map it before implementation; in rolling mode, map it as the
corresponding visible edit is accepted and verify the complete mapping in the
final audit. Each decision must resolve to concrete source slides, a new slide
or demo, an explanatory moment, or an explicit deferral. Do not silently drop an
accepted addition later, and do not remove an original definition, example,
figure, or derivation merely because another slide appears to cover the same
topic.

Order planned or recorded edits by pedagogical dependency, not by whichever
source file is easiest to edit. An accepted edit is immutable unless the user
explicitly reopens it; later feedback on another edit must not undo or dilute
it.

Build a short dependency and notation table before drafting:

- concepts used by each new or substantially edited slide, with the slide where
  each prerequisite is introduced;
- course-wide symbols and conventions used in the unit;
- terminology that must stay consistent across the LaTeX and HTML sections.

Do not introduce a concept before its prerequisite, even in an example intended
as motivation. Re-run this check after slides are moved.

For additions, first write one representative slide in the instructor's voice
and obtain approval before propagating the style. Compare it directly with
nearby source slides for sentence length, density, emphasis, notation, and
visual hierarchy. After two rejections on the same dimension (voice, fidelity,
layout, or scope), stop editing and re-baseline from the authoritative source
instead of becoming progressively more conservative.

Before porting a subtopic to HTML, render at least two representative frames:
one prose/equation slide and one visually structured slide. Compare them
side-by-side with the source at presentation resolution. The HTML version must
have intentional text blocks and margins, preserve meaningful equation colors
and annotations, and use whitespace to establish hierarchy rather than leaving
large accidental empty regions. If the port is less beautiful or less readable,
improve the shared visual system first or keep the subtopic in LaTeX.

Visual QA always covers the complete slide at presentation resolution, not a
cropped component. Check all four margins, optical balance, implied symmetry,
alignment, spacing around borders and leaders, arrow junctions, and accidental
tangencies, as well as clipping and overlap. Confirm that title, body, caption,
legend, and footer are all visible. For an interactive component, inspect its
default state and every materially different state (selected, expanded,
unstable, high/low parameter values). Compilation or a component screenshot is
never sufficient evidence.

## Then: decide the unit's format

Once the demo brainstorm (step 5 above) is done for the unit, decide the
LaTeX/HTML split **once, top-down, before the slide audit** — the scope of
the decision should match the scope of the interactivity found, not default
to per-slide.

**Default policy:** keep narrative and mathematical exposition in LaTeX and
use standalone HTML only for demonstrations that provide unique interactive
value. An embedded HTML sub-deck is exceptional: before approving it, two
representative frames must pass the side-by-side visual-quality gate above and
the interactive material must depend narratively on its surrounding slides.
If either condition fails, keep the slides in LaTeX and open the demo
separately.

1. **No candidate demos, or only marginal ones** → the whole unit stays
   **latex**. This is the default and should be most units.
2. **Just one or two isolated interactive slides**, otherwise unrelated to
   each other → keep the deck in **latex**, but build each demo as its own
   standalone **html-mini** page (`html/demos/<short-topic>.md`), reusing
   the shared `components/`/`styles/` from the pilot. The presenter switches
   to a browser tab for the demo and back — the same context-switch the
   course already makes today for Colab labs. Minimizes refactor cost since
   no narrative text, macros, or styling gets re-authored in HTML, only the
   demo itself.
3. **Significant interactivity, but confined to one or two subtopics**
   (a contiguous run of slides on one theme within the unit) → split just
   those subtopics into an **html-embedded** sub-deck
   (`html/slides/Lecture_N_<subtopic>.md`) covering that subtopic's full
   narrative plus its demos, and leave the rest of the unit in latex. Use
   this over html-mini when a subtopic's slides depend on each other
   narratively, the approved representative frames are at least as beautiful
   and readable as the source, and hopping to a bare demo page and back would
   break the flow more than porting the connecting slides.
4. **Significant interactivity throughout the unit** → refactor the entire
   unit to **html-embedded** as one full Slidev deck
   (`html/slides/Lecture_N.md`), following the normal narrative pass + slide
   audit rather than a mechanical translation of the old Beamer frames. This
   is rare and requires an explicit format decision after the visual-quality
   gate; interactivity alone does not justify a full port.

## Then: slide audit

For every slide or compact slide group, record only the relevant actions:

- **lighten** — reduce detail, duplication, or framework syntax;
- **move from elsewhere** — bring in missing prerequisite/context;
- **move elsewhere** — relocate it to a better unit, an explanation, or
  appendix;
- **add** — new conceptual material, a clearer intuition, or a modern topic;
- **leave** — retain when it already serves the narrative.

The format decided above applies to the whole unit (case 1 or 4) or to the
specific demo slides/subtopics identified in the brainstorm (case 2 or 3) —
the audit does not re-open the format question per slide.

Apply the course-wide editorial commitments during the audit: readability and
accessibility are acceptance criteria for every retained or new slide, while
trimming and research connections are deliberate narrative choices rather
than a reason to add boilerplate.

## Add experiments as teaching material

For each accepted demo from the narrative-pass brainstorm, build it as a
**static artifact** (a small, self-contained Python script generating a plot,
animation, or figure) or a **live HTML widget** (a small Vue/JS component,
per the pilot's component pattern), following the format decided for that
unit above. Treat both as first-class course artifacts alongside slides,
conceptual explanations, and labs — the live-widget option exists specifically
because it can do things a static figure can't (a learning-rate slider
showing convergence turn into divergence, a live-trained decision boundary,
a scenario picker for training-failure signatures), not because it looks
nicer.

Prefer experiments (static or live) that make an otherwise empirical claim
visible, for example:

- optimization/training curves and debugging failures;
- activation or gradient scale with/without normalization or residual paths;
- receptive field and convolutional inductive bias;
- attention patterns, masking, positional encodings, or KV-cache cost;
- conditional computation in multiplicative layers or MoEs.

Each accepted experiment should have a short source script or component,
deterministic setup where practical, and a clear link from the relevant slide
source. Keep static figures reproducible from the repository rather than
manually edited; keep live widgets small and single-purpose (one concept per
component, matching the pilot's `components/*.vue` pattern) regardless of
whether they end up packaged as html-mini or folded into an html-embedded
deck per the unit's format decision above.

Interactive numerical summaries must name the statistic or comparison
explicitly; avoid labels such as "spread" or "score" without a definition. If
a control crosses a meaningful mathematical boundary, show the live comparison
next to the control (for example, peak learning rate versus the stability
limit) rather than asking the audience to compare distant numbers mentally.
Prefer interactions that expose a coupled relationship or state transition:
several outputs should change together in a way that supports the teaching
claim.

Before implementing a live widget, state all three of the following:

1. the quantity the instructor or student changes;
2. the visible consequence that changes in response;
3. the claim that becomes easier to understand because both can be compared.

If a single static figure can communicate the same claim equally well, use the
static figure. Animation, buttons, or sliders are not sufficient reasons for
HTML. Approve the interaction storyboard before porting its surrounding
subtopic.

When building or restyling the shared theme kit or a new `components/*.vue`
widget (not when writing ordinary slide content), use Claude Code's
[frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)
to ground layout, typography, and color choices instead of reaching for
generic defaults.

## Figures and visual assets

Treat figures as editable teaching artifacts, but preserve them by default.
Before proposing a change, locate the authoritative native source (Python,
notebook, Draw.io, TikZ/LaTeX, SVG, or other vector source) and maintain an
explicit source-to-export mapping. Edit the native source and regenerate the
export; do not paint over a raster.

A figure change must materially improve conceptual correctness, notation
consistency, presentation-scale readability, or reproducibility, or replace a
clearly mismatched external screenshot. Pure restyling is insufficient.
Editable source availability is not itself a reason to redraw. When the
original already communicates the intended mechanism and the instructor
prefers it, preserve it: reconstruction introduces pixel-level risks in arrow
geometry, junctions, spacing, alignment, and symmetry.

Prefer a small reproducible static figure when it communicates the claim as
well as a widget. Prefer direct visible samples to unexplained aggregate bands
or statistical objects; every aggregate shown must already be interpretable
from the lecture.

## HTML build reference

Durable facts from the initial pilot build (Lecture 0 Slidev port +
`Theme_kit_test.md`, 2026-07-20) — needed whenever a unit's format decision
above calls for html-mini or html-embedded. Full pilot history and evaluation:
`vault: Workflows/State/NNDS Slide Refresh Log#2026-07-20 — HTML pilot — Lecture 1` (the log).

- **Theme kit:** shared title/header layout, `\myalert`-equivalent highlight,
  theorem/definition box, Python code block, and header background image live
  in `components/`/`styles/` — reuse rather than rebuilding per unit.
- **Equation annotation** (`annotate-equations` macro): default to compiling
  the annotated equation as a standalone SVG (`pdflatex` + `dvisvgm`/`pdf2svg`)
  and embedding it as a figure — matches Beamer fidelity, no rewrite needed.
  For one or two "hero" equations where the annotation is the actual teaching
  moment, build a live KaTeX + CSS/SVG hover-overlay version instead.
- **Interactive equation inspection:** keep difficult equations monochrome at
  rest. A compact neutral selector may temporarily highlight linked indices or
  terms across separated parts of the expression; hover previews, click pins,
  and a second click clears. Do not impose a persistent course-wide
  five-color ontology or add large description cards. Use this only when the
  selection reveals a non-obvious grouping, and keep the complete equation
  intelligible without interaction and in PDF export.
- **HTML authoring reference:** keep the shared semantic class and inline-math
  catalogue in `html/AUTHORING.md`; ordinary Markdown uses `$...$`/`$$...$$`,
  while raw HTML uses the shared math component rather than duplicated
  hand-written markup.
- **Deployment:** GitHub Actions → GitHub Pages
  (`.github/workflows/deploy-slides.yml`, rebuilds on every push touching
  `html/`); live at https://sscardapane.github.io/slides-nnds-2026/.
- **Known gotchas:**
  - `slidev build --out` resolves relative to the entry file's directory, not
    the shell's cwd — use an absolute `$PWD/dist/$name` path.
  - Default path-based routing 404s on direct links to a slide on GitHub
    Pages (its `404.html` fallback only triggers at the site root) — set
    `routerMode: hash` in each deck's frontmatter instead.
  - The SVG-embed equation path needs `\vspace*` instead of `\vspace` (TeX
    top-of-page glue-discard).

## Current directional choices

- Start with preliminaries, MLPs, and supervised learning reframed around
  debugging neural networks.
- **Tensor notation and indexing:** use the book's shape convention
  `$X \sim (s_1, \ldots, s_n)$`, with early, semantic axis letters such as
  `B` (batch), `T` (tokens/time), `D` (features or embedding), `C`
  (channels), and `H, W` (spatial dimensions). Use ordinary subscripts only
  for simple scalar coordinates (for example, `$X_{i,j,k}$`). For actual
  indexing, slices, or an indexed expression, use the lightly coloured
  bracket notation (`$\idx{X}{b,t,:}$`, `$\idx{X}{b,:,:}$`,
  `$\idx{f(X)}{b}$`); do not collapse multi-axis indexing into `$X_{ijk}$`.
  Code examples follow NumPy's zero-based convention.
- **Derivative notation:** use the new advanced-autodiff chapter as the
  long-term notation authority, but stage its abstraction. In preliminaries,
  write scalar linearization as `$f(x+h)\approx f(x)+\partial f(x)h$`,
  directional derivatives as `$\mathrm D_u f(x)=\langle\nabla f(x),u\rangle$`,
  and vector-function derivatives as a Jacobian `$\partial f(x)$` acting by
  ordinary multiplication (`$\partial f(x)u$`). Introduce the explicit
  linear-map bracket notation `$\partial f(x)[u]$` only in the later autodiff
  unit alongside JVPs/VJPs. Treat `J_f(x)` only as an optional descriptive
  alias, not the course's primary notation.
- Replace the classical autodiff lecture with the newer material and pair it
  with a lab implementing a small autodiff framework.
- After MLPs, introduce 1D/2D/other data structures, tokenization, and the
  alternative architectural responses: convolutions, attention, recurrence, and
  graph models.
- Use PyTorch for the main practical path and JAX for one deliberate comparison.
- Reserve the LLM-to-agent sequence for the end, potentially culminating in a
  constrained coding-agent lab.
- During each relevant unit, assess additions such as RoPE, multiplicative
  layers, and MoEs only when they earn a narrative role.
- **Assessment:** the default is an oral examination on the course material. A
  research project agreed together can replace the oral only for an interested
  student pursuing `30 e lode` or preparing a follow-up thesis; it is normally
  more demanding than the oral. Dates are communicated separately once fixed.

## Close each revision pass

Keep the approved decisions and verification with the repository change. When
a vault project/log update is requested as part of the revision, summarize the unit,
main moves, demonstrations added/deferred and any clarified lab decision there;
do not force the unresolved lab format or duplicate detailed implementation logs.

For LaTeX units in this repository, run `latexmk Lecture_N_*.tex` from
`latex/`. The repository configuration selects LuaLaTeX; do not pass `-pdf`,
which overrides that engine choice with pdfLaTeX.

## Guardrails

- Do not change the published `slides-nnds-2026` repository content beyond
  the unit being revised, and do not publish or deploy without a separate
  explicit decision.
- Do not settle the still-open lab format as a side effect of a slide revision.

## Completion Criteria

The agreed narrative, format and slide changes have recorded decisions and
verification. In addition:

- the broad direction and review mode were approved; ledger-first runs have an
  approved edit-to-slide ledger, while rolling runs have an approved final
  coverage audit reconstructed from the decision trail and source comparison;
- every approved edit was implemented and reviewed according to the selected
  mode before a materially different content block began;
- every original slide is accounted for in the ledger or final coverage audit,
  with every removal explicitly approved;
- every accepted brainstorming decision is present or explicitly deferred;
- no slide uses a concept before it is introduced;
- notation and terminology match across LaTeX and HTML sections;
- changed prose has been compared with neighboring source slides for authorial
  fidelity;
- representative changed slides have passed a side-by-side visual review for
  composition, margins, text grouping, whitespace, equation color, and
  annotation—not only clipping and contrast;
- every live widget passes the change/consequence/claim test above;
- the final render has been compared against the authoritative source for
  accidental omissions as well as clipping, overlap, contrast, and density.
