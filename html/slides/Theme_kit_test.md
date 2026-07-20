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
