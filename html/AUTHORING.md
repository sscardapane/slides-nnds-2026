# NNDS HTML slide authoring

The HTML lectures use Slidev with the NNDS `BeamerTitle` and `BeamerFrame`
components. Slide numbers are automatic: do not add `page="..."` to ordinary
frames.

## Minimal slide

```md
---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Slide title">

Write the slide in Markdown here.

</BeamerFrame>
```

Adding, deleting, or moving a slide automatically updates every following
number in that HTML deck. For a sub-deck that begins partway through the
lecture, set one offset in the deck headmatter:

```yaml
themeConfig:
  pageOffset: 37
```

With that example, the title remains unnumbered and the first ordinary frame
is page 39 (`2 + 37`). The optional `page` property is retained only as an
escape hatch for exceptional exports.

## Mathematics

Prefer normal Markdown math whenever the formula is outside an HTML element:

```md
Inline math: $X\sim(B,T,D)$.

$$
Y_{b,t,h}=\sum_{d=1}^{D}X_{b,t,d}W_{d,h}.
$$
```

Markdown inside raw HTML is not always parsed. In that case use `MathTex`,
which is auto-imported from `html/slides/components`:

```html
<div class="definition-box">
  A scalar formula: <MathTex tex="\mathbf{x}\in\mathbb{R}^{D}" />.
</div>

<div class="two-columns">
  <MathTex block tex="\mathbf{H}=\mathbf{X}\mathbf{W}" />
  <MathTex block tex="\mathbf{H}\sim(B,H)" />
</div>
```

Use the `tex` property for short formulas. Keep long aligned derivations in
ordinary `$$ ... $$` Markdown blocks, where they remain easier to edit.

## Interactive equation inspection

Keep equations monochrome by default. A persistent multi-color grammar is not
self-explanatory and should not be used merely for decoration. For a difficult
equation, use the reusable `EquationInspector` only when selecting a symbol,
index, or subexpression either:

1. links several separated occurrences; or
2. reveals a non-obvious grouping inside the equation.

The inspector is deliberately small. Hover previews a group, click pins it,
and clicking the selected item again clears it. Do not add explanatory cards
or prose panels when the highlighted correspondence is already visible in the
equation. The unselected equation and its PDF export must remain complete.

Inside the TeX source, mark linked occurrences with KaTeX's `\htmlData`:

```md
<script setup>
import EquationInspector from '../components/EquationInspector.vue'

const equation = String.raw`
  Y_{
    \htmlData{inspect=b}{b},
    \htmlData{inspect=h}{h}
  }
  =
  \sum_{\htmlData{inspect=d}{d}=1}^{D}
  X_{
    \htmlData{inspect=b}{b},
    \htmlData{inspect=d}{d}
  }
  W_{
    \htmlData{inspect=d}{d},
    \htmlData{inspect=h}{h}
  }
`

const items = [
  { id: 'b', tex: 'b' },
  { id: 'd', tex: 'd' },
  { id: 'h', tex: 'h' },
]
</script>

<EquationInspector
  :tex="equation"
  :items="items"
  label="highlight index"
/>
```

The identifiers are local to one equation: they do not imply a course-wide
color legend. The same component can inspect complete terms by wrapping a
subexpression, for example
`\htmlData{inspect=read}{(\mathbf U_k^\top\mathbf x)}` and listing a
corresponding `read` item. Use `inline` when the small selector can sit beside
the equation and the slide is vertically dense.

Do not add an inspector to simple definitions, one-step identities, or
equations where each selectable item occurs only once and its grouping is
already obvious. In those cases, ordinary LaTeX, a static annotation, or no
annotation is clearer.

## Semantic CSS classes

These classes are defined in `html/styles/index.css` and work in every deck.

| Purpose | Class | Typical use |
|---|---|---|
| Main emphasis | `accent` | `<span class="accent">mini-batch</span>` |
| Secondary text | `muted` | sources, qualifications |
| Introductory text | `text-lead` | one opening sentence |
| Smaller text | `text-small` | captions and dense examples |
| Very small text | `text-tiny` | exceptional metadata only |
| Tighter leading | `text-tight` | code-like or unusually dense material |
| Relaxed leading | `text-relaxed` | prose that needs extra separation |
| Monospace | `mono` | shapes, identifiers, short code |
| Prevent wrapping | `nowrap` | a short label or formula |
| Alignment | `center`, `right` | local text alignment |
| Vertical stacks | `stack-sm`, `stack`, `stack-lg` | consistent gaps between children |
| Top spacing | `mt-0`, `mt-sm`, `mt-md`, `mt-lg` | local spacing correction |
| Bottom spacing | `mb-0`, `mb-sm`, `mb-md`, `mb-lg` | local spacing correction |
| Columns | `two-columns`, `three-columns` | equal-width content columns |
| Definition | `definition-box` | definitions and central statements |
| Research aside | `research-note` | optional/out-of-scope connection |
| Ruled statement | `rule-line` | compact rule or convention |
| Code listing | `legacy-code`, `code-line`, `ln` | Beamer-like code blocks |

The default body leading is deliberately relaxed. Apply `text-tight` locally
instead of reducing line spacing for the entire deck.

## Common patterns

```html
<div class="definition-box">
  <strong>Definition.</strong> The central statement goes here.
</div>

<div class="two-columns">
  <div class="stack-sm">
    <span class="accent">Left idea</span>
    <span class="muted">Short explanation.</span>
  </div>
  <div class="stack-sm">
    <span class="accent">Right idea</span>
    <span class="muted">Short explanation.</span>
  </div>
</div>

<div class="research-note">
  Optional connection or material outside the core course.
</div>
```

For one-off positioning, the UnoCSS utilities already enabled by Slidev are
also available (`mt-4`, `grid`, `grid-cols-2`, `gap-6`, `text-center`, and so
on). Prefer the semantic classes above for recurring NNDS patterns.
