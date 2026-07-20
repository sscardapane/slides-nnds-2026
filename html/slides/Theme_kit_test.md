---
theme: default
title: NNDS 2026 — Theme kit test
info: |
  Capability tests for the NNDS 2026 HTML-format pilot: theme components
  (highlight, theorem box) and the two equation-annotation treatments
  discussed for `annotate-equations`. Synthetic examples only — no lecture
  content, no Lecture 1 material.
css: unocss
fonts:
  sans: 'Fira Sans'
  mono: 'Fira Mono'
colorSchema: light
---

# Theme-kit test: highlight & theorem box

<script setup>
import Alert from '../components/Alert.vue'
import TheoremBox from '../components/TheoremBox.vue'
</script>

A <Alert>highlighted term</Alert> should read the same as Beamer's `\myalert{}` (dark red, bold).

<TheoremBox title="Definition 1.1">

A **loss function** $\mathcal{L}$ measures how well a model's predictions match the observed data.

</TheoremBox>

---

# Equation annotation — SVG-embed path (default)

Compiled with `annotate-equations` + `pdftocairo -svg`, matching the Beamer decks exactly. Synthetic example equation, not course content:

<img src="/cross_entropy_annotated.svg" class="mx-auto mt-8" style="max-height: 220px" />

<div class="text-sm mt-4 opacity-70">
Source: <code>assets/src/cross_entropy_annotated.tex</code> — same package as the LaTeX decks, compiled standalone and embedded as a figure.
</div>

---

# Equation annotation — live hover overlay (hero equations only)

<script setup>
import EqAnnotate from '../components/EqAnnotate.vue'
</script>

<span class="text-2xl mt-8 inline-block">$\mathcal{L} = -\sum_{i=1}^n$ <EqAnnotate label="true label" color="#c0392b">$y_i$</EqAnnotate> $\log$ <EqAnnotate label="predicted probability" color="#2980b9">$\hat{y}_i$</EqAnnotate></span>

<div class="text-sm mt-8 opacity-70">
Hover the underlined terms. Reserved for the one or two equations per unit where the annotation is the actual teaching moment — most equations use the SVG-embed path above.
</div>

---

# Interactive demo — gradient descent

<script setup>
import GradientDescentDemo from '../components/GradientDescentDemo.vue'
</script>

None of this exists in Beamer: drag the learning rate, watch convergence turn into divergence live, during the lecture, on the actual slide.

<GradientDescentDemo />

<span class="text-sm mt-4 opacity-70 inline-block">Toy example: $f(x) = x^2$, gradient step $x \leftarrow x - \eta \cdot f'(x)$. Try $\eta > 1$ to show divergence.</span>

---

# Live, editable code cell

Slides can embed runnable code, not just syntax-highlighted text — students edit and re-run during class:

```js {monaco-run}
function softmax(logits) {
  const m = Math.max(...logits)
  const exps = logits.map(x => Math.exp(x - m))
  const sum = exps.reduce((a, b) => a + b, 0)
  return exps.map(x => x / sum)
}

console.log(softmax([2.0, 1.0, 0.1]))
```

<div class="text-sm mt-4 opacity-70">
This example runs JS in-browser (Monaco + built into Slidev). A real pipeline for JAX/PyTorch snippets would need a Python runtime (e.g. Pyodide) — worth a separate feasibility check, not attempted here.
</div>

---

# Click-to-reveal (native, no extra work)

Beamer's `\pause`/overlays, built into the markdown source with `v-click`:

<v-clicks>

- First point appears immediately
- Second point appears on next click
- Third point appears after that

</v-clicks>
