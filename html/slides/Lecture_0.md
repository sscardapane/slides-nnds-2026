---
theme: default
title: NNDS 2026 — Lecture 0 (HTML pilot)
info: |
  Slidev port of the existing latex/Lecture_0_about_the_course.tex, used as
  the fidelity test for the NNDS 2026 HTML-format pilot. Content matches the
  current Beamer deck; not a content revision.
css: unocss
fonts:
  sans: 'Fira Sans'
  mono: 'Fira Mono'
colorSchema: light
routerMode: hash
---

<style>
@import '../styles/index.css';
</style>

<div class="absolute inset-0 opacity-40">
  <img src="/header.jpeg" class="w-full h-full object-cover" />
</div>

<div class="relative">

# Neural Networks for Data Science
### Master's Degree in Data Science

## Lecture 0: About the course

<img src="/Uniroma1.png" class="mt-8 h-10" />

<div class="mt-6 text-sm">
  <b>Lecturer</b>: S. Scardapane
</div>

</div>

---

# Timetable and organization

- **Master's Degree in Data Science**, code 10589627, 2nd year, optional group D.
- **Timetable**: TBD
- **Office hours**: by appointment, remotely or in-person (Via Eudossiana 18, DIET Department, 1st floor, room 122).

<div class="border border-red-200 bg-red-50 px-4 py-2 mt-6">
Official course website:<br/>
<a href="https://www.sscardapane.it/teaching/nnds-2026/">https://www.sscardapane.it/teaching/nnds-2026/</a>
</div>

Register to the **Google Classroom** from the website for all updates (<u>mandatory</u>).

---

# Exam dates (TBD)

1. **Sessions 1-2**: TBD
2. **Sessions 3-4**: TBD
3. **Session 5**: TBD
4. **Session E1**: TBD (**reserved**, see regulations).
5. **Session E2**: TBD (**reserved**, see regulations).

---

# Exam

1. One **end-of-term** project (5 points).
2. One **oral examination** on the program (25 points).

The EoT project can be sent before *any* exam date. The mark can be kept during the academic year, irrespective of the oral. *Lode* will be given only to exceptional (top 5%) projects and orals.

---

# Learning objectives

- Broad historical overview of the last 15 years.
- Fundamental tools underlying neural networks: optimization, gradient descent, automatic differentiation.
- Basic blocks to build modern neural networks (convolution, attention, normalization, ...).
- Proficiency in a real-world deep learning library (**JAX**, **PyTorch**).
- Capability of navigating the current literature and ecosystem in autonomy.

---

# Lectures (methodological)

1. **Historical overview**.
2. **Preliminaries** (tensors, linear algebra, optimization).
3. **Supervised learning** as numerical optimization.
4. Linear models and **fully-connected** models.
5. **Convolutional models** (for sequential, spatial, and temporal data).
6. Blocks to train **deeper models** (dropout, batch normalization, ...).
7. **Attention** models for sets.
8. **LLM** building blocks: autoregression, tokenization, pre- and post-training.
9. **Graph** models (e.g., graph convolutional networks).
10. Optional topics depending on time and material.

---

# Lectures (practical)

1. Several practical lectures with **JAX** and **PyTorch** (hands-on coding from scratch).
2. When possible, a showcase of other libraries (e.g., HuggingFace Datasets).
3. Optional topics depending on time and material.

---
layout: two-cols
---

# Textbook

Slides are self-contained, but the material is expanded in a textbook.

The book is available for free as a PDF or via Amazon for a printed copy:

<https://sscardapane.it/alice-book/>

The book was recently published — would be happy for feedback or ideas for completed exercises or additional sections!

::right::

<img src="/Alice.png" class="border-2 border-black w-40 mx-auto mt-12" />

---

# Additional textbooks

Additional useful textbooks:

- **Dive into Deep Learning**, online, much more practical.
- **Understanding Deep Learning**, high-quality illustrations and descriptions.
- **Patterns, Predictions, and Actions**, slightly broader on the machine learning side.
- **Deep Learning - Foundations and Concepts**, for a beginner Bayesian treatment.

From mobile, you can also check out **The Little Book of Deep Learning**.
