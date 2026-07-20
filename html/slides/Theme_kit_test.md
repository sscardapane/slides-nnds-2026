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
routerMode: hash
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
This example runs JS in-browser (Monaco + built into Slidev). See the next slide for real Python.
</div>

---

# Extreme: real Python, running in the browser

<script setup>
import PyRunner from '../components/PyRunner.vue'

const pySample = [
  'import numpy as np',
  '',
  'logits = np.array([2.0, 1.0, 0.1])',
  'probs = np.exp(logits) / np.exp(logits).sum()',
  "print('softmax:', probs)",
  "print('sum:', probs.sum())",
].join('\n')
</script>

Not JS pretending to be Python — actual CPython + numpy compiled to WASM (Pyodide), loaded from a CDN on first click. Edit and re-run:

<PyRunner :initial-code="pySample" />

<div class="text-sm mt-4 opacity-70">
First run downloads ~10-15MB of WASM runtime (cached after that). A real deployment would want to self-host the runtime instead of hitting jsdelivr live in a lecture room — flagging, not solving, here.
</div>

---

# Extreme: live attention pattern

<script setup>
import AttentionHeatmap from '../components/AttentionHeatmap.vue'
</script>

Toy self-attention (synthetic Q/K, not a trained model) — drag temperature, toggle the causal mask, watch every row's softmax update live:

<AttentionHeatmap />

<div class="text-sm mt-4 opacity-70">
This is the exact "attention patterns, masking" experiment type already called out in the course recipe — normally a separate generated static figure, here it's explorable during the lecture instead.
</div>

---

# Extreme: live decision-boundary training

<script setup>
import DecisionBoundary from '../components/DecisionBoundary.vue'
</script>

Real backprop (hand-rolled 2-layer MLP, tanh + sigmoid, live in JS — not pre-recorded). Click the canvas to add points, hit "Train live":

<DecisionBoundary />

<div class="text-sm mt-4 opacity-70">
Click to place points for class A or B, then train and watch the boundary fold to fit them. Pyodide could back this instead (real numpy autograd), but the async round-trip per frame makes live dragging/training visibly less smooth than plain JS — noted, not solved, here.
</div>

---

# Extreme: debug-the-run

<script setup>
import DebugRunDemo from '../components/DebugRunDemo.vue'
</script>

Matches the course's own opening frame — "supervised learning reframed around debugging neural networks" — as an interactive scenario picker instead of four separate static plots:

<DebugRunDemo />

<div class="text-sm mt-4 opacity-70">
Curves are hand-crafted to be representative, not from real training runs — the point is the interaction pattern (pick a failure mode, see the diagnostic signature), which a real pipeline would back with actual runs.
</div>

---

# Extreme: KV-cache cost calculator

<script setup>
import KVCacheCalculator from '../components/KVCacheCalculator.vue'
</script>

No training, no visuals to render — just formulas that update live. The "KV-cache cost" experiment type from the course recipe, as a calculator instead of a static number:

<KVCacheCalculator />

---

# Click-to-reveal (native, no extra work)

Beamer's `\pause`/overlays, built into the markdown source with `v-click`:

<v-clicks>

- First point appears immediately
- Second point appears on next click
- Third point appears after that

</v-clicks>
