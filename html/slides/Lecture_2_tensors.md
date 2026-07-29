---
theme: default
layout: full
title: "NNDS 2026 — Lecture 2a: Tensors and linear maps"
css: unocss
fonts:
  sans: 'Fira Sans'
  mono: 'Fira Mono'
colorSchema: light
routerMode: hash
---

<style>@import '../styles/index.css';</style>

<script setup>
import BeamerTitle from '../components/BeamerTitle.vue'
</script>

<BeamerTitle />

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Definition of a tensor">

<div class="definition-box">
For the purpose of this course, an <strong>ndarray</strong> (informally, a <em>tensor</em>) is an array of elements of the <em>same type</em>, organized along one or more axes.
</div>

Each axis has a <em>meaning</em> that we encode in the letters we use, for example:

$$
\begin{aligned}
\mathbf{x} \sim (D) &\quad \text{a vector of {\color{darkred}features}}\qquad \\[3pt]
\mathbf{X} \sim ({\color{green}B}, D) &\quad \text{a {\color{darkred}batch} (set) of vectors}\qquad \\[3pt]
\mathbf{X} \sim (T, D) &\quad \text{a sequence of vectors ({\color{darkred}tokens})}\qquad \\[3pt]
X \sim ({\color{green}B}, T, D) &\quad \text{a batch of sequences}\qquad \\[3pt]
X \sim (C, H, W) &\quad \text{a color image ({\color{darkred}channels}, height, width)}\qquad \\[3pt]
X \sim ({\color{green}B}, C, H, W) &\quad \text{a batch of color images}\qquad \\[3pt]
X \sim ({\color{green}B}, T, C, H, W) & \quad \text{a batch of sequences of images (videos)}\qquad
\end{aligned}
$$

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Shape and dtype">

A tensor is described both by its <span class="accent">shape</span> and by the type of its entries (<span class="accent">dtype</span>). We will mostly use three families:

<div class="legacy-code">
  <div class="code-line"><span class="ln">1</span><span class="code-text">X = torch.randn(32, 20, 128)          <span class="comment"># floating point</span></span></div>
  <div class="code-line"><span class="ln">2</span><span class="code-text">token_ids = torch.randint(5000, (32, 20)) <span class="comment"># integers</span></span></div>
  <div class="code-line"><span class="ln">3</span><span class="code-text">mask = token_ids != 0                  <span class="comment"># booleans</span></span></div>
</div>

- <strong>floating point</strong>: features, images, embeddings, activations, and parameters;
- <strong>integers</strong>: token IDs, class labels, and indices;
- <strong>booleans</strong>: masks.

For text, tokenization produces integer IDs with shape $(B,T)$; an embedding layer maps them to floating-point vectors with shape $(B,T,D)$.

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Tensors in practice">
  <p>Tensors are the default data structure in any deep learning framework:</p>
  <div class="legacy-code">
    <div class="code-line"><span class="ln">1</span><span class="code-text"><span class="kw">import</span> torch</span></div>
    <div class="code-line"><span class="ln">2</span><span class="code-text">X = torch.randn((3, 64, 64)) <span class="comment"># shape (C, H, W)</span></span></div>
  </div>
  <p>NumPy-like indexing is pervasive (with 0-based indexing):</p>
  <div class="legacy-code">
    <div class="code-line"><span class="ln">1</span><span class="code-text">X[0, 0, 0]  <span class="comment"># full indexing (a scalar)</span></span></div>
    <div class="code-line"><span class="ln">2</span><span class="code-text">X[0]        <span class="comment"># shape (H, W)</span></span></div>
    <div class="code-line"><span class="ln">3</span><span class="code-text">X[:, 0]     <span class="comment"># shape (C, W)</span></span></div>
  </div>
  <p>In math, we use subscripts for scalar entries and brackets for slices:</p>
  <div class="math-row">
    <div class="formula"><span class="bracket">[</span><i>X</i><span class="bracket">]</span><sub>0,:,: </sub></div>
    <div>2-axis tensor of shape (<i>H</i>, <i>W</i>)</div>
  </div>
</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import PyRunner from '../components/PyRunner.vue'

const indexingCode = [
  'import numpy as np',
  'X = np.empty((32, 20, 128))  # (B, T, D)',
  'print("X[0, 3, :]  ->", X[0, 3, :].shape)',
  'print("X[0, :, :]  ->", X[0, :, :].shape)',
  'print("X[:, 3, :]  ->", X[:, 3, :].shape)',
].join('\n')

const indexingOutput = [
  'X[0, 3, :]  -> (128,)',
  'X[0, :, :]  -> (20, 128)',
  'X[:, 3, :]  -> (32, 128)',
].join('\n')
</script>

<BeamerFrame title="Indexing tensors">

For $X\sim(B,T,D)$, consider a concrete tensor with $B=32$, $T=20$, and $D=128$:

<PyRunner :code-rows="5" :initial-code="indexingCode" :initial-output="indexingOutput" />

<div class="rule-line small">

An integer index removes an axis; <code>:</code> retains it. In math, use $X_{b,t,d}$ for a scalar entry and $[X]_{b,t,:}$ for a slice.

</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Scalars and vectors">

$0$-axis tensors are called <span class="accent">scalars</span> (a physics terminology). Most scalars in this course are real-valued.

$1$-axis tensors are the classical <span class="accent">vectors</span> from linear algebra; they are written in boldface and treated as column vectors (when we care about the distinction):

$$
\mathbf{x}=
\begin{pmatrix}
x_1\\x_2\\\vdots\\x_D
\end{pmatrix},
\qquad
\mathbf{x}^{\top}=
\begin{pmatrix}
x_1 & x_2 & \cdots & x_D
\end{pmatrix}.
$$

The Euclidean norm and the standard inner product are:

$$
\lVert\mathbf{x}\rVert_2=\sqrt{\sum_d x_d^2},
\qquad
\langle\mathbf{x},\mathbf{y}\rangle=\sum_d x_dy_d=\mathbf{x}^{\top}\mathbf{y}.
$$

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Matrices and batches">

$2$-axis tensors are <span class="accent">matrices</span>. A matrix can represent a grid, a sequence of elements, or a stack (a <span class="accent">batch</span>) of vectors:

$$
\mathbf{X}=
\begin{bmatrix}
\mathbf{x}_1^{\top}\\
\vdots\\
\mathbf{x}_B^{\top}
\end{bmatrix}
\sim(B,D).
$$


<div class="definition-box">

For $\mathbf{X}\sim(B,D)$ and $\mathbf{W}\sim(D,H)$, matrix multiplication is defined by:

$$
[\mathbf{X}\mathbf{W}]_{b,h}
=\langle[\mathbf{X}]_{b,:},[\mathbf{W}]_{:,h}\rangle
=\sum_{d=1}^{D}X_{b,d}W_{d,h}.
$$

</div>



</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Matrix multiplication">

Geometrically, a matrix represents a <em>linear map</em> between two vector spaces:

$$
\mathbf{W}^{\top}(\alpha\mathbf{x} + \beta\mathbf{y})
= \alpha\mathbf{W}^{\top}\mathbf{x} + \beta\mathbf{W}^{\top}\mathbf{y},
\qquad \mathbf{W}\sim(D,H).
$$

 When applied to a batch of elements $\mathbf{X} \sim (B, D)$, matrix multiplication yields a transformed batch $\mathbf{H} = \mathbf{X}\mathbf{W} \sim (B, H)$:

$$
[\mathbf{H}]_{b,:}=\mathbf{x}_b^{\top}\mathbf{W}.
$$

Therefore $\mathbf{X}\mathbf{W}\sim(B,H)$ transforms a batch of vectors in $\mathbb{R}^D$ into a batch of vectors in $\mathbb{R}^H$. Importantly, any operation applied to a batch should not introduce any dependency between the elements of the batch.

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Low-rank factorization">

For $\mathbf{W}\sim(D,H)$, a <span class="accent">rank-$r$ approximation</span> can be factorized as:

$$
\mathbf{W}\approx\mathbf{U}\mathbf{V}^{\top},
\qquad
\mathbf{U}\sim(D,r),\quad
\mathbf{V}\sim(H,r),\quad
r\ll\min(D,H).
$$

For a row vector $\mathbf{x}^{\top}$:

$$
\mathbf{x}^{\top}\mathbf{W}\approx
\sum_{k=1}^{r}
(\mathbf{U}_k^{\top}\mathbf{x})\mathbf{V}_k^{\top}.
$$

Each rank-1 component uses $\mathbf{U}_k$ to <em>read</em> one scalar from the input and $\mathbf{V}_k$ to <em>write</em> one output direction.

<div class="definition-box small">

**Why we care:** $\mathbf{U}\mathbf{V}^{\top}$ has rank at most $r$ and uses $r(D+H)$ parameters instead of $DH$. This idea underlies parameter-efficient methods such as **low-rank adaptation** (LoRA).

</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Tensor contractions">

Matrix multiplication sums over one shared axis. The same idea applies to tensors with more axes, e.g., a <strong>batched matrix multiplication</strong>:

$$
X\sim(B,T,D),\qquad
\mathbf{W}\sim(D,H),\qquad
Y\sim(B,T,H),
$$

$$
Y_{b,t,h}=\sum_{d=1}^{D}X_{b,t,d}W_{d,h}.
$$

<div class="definition-box">
Mathematically, this is a <em>contraction</em>: sum over matched indices and retain all the other axes.
</div>

In NumPy and PyTorch, a very common way to express tensor contractions is through ``einsum'' (Einstein summation):

<div class="legacy-code">
  <div class="code-line"><span class="ln">1</span><span class="code-text">Y = torch.einsum(<span class="comment">"btd,dh-&gt;bth"</span>, X, W)</span></div>
</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Element-wise operations">

Some scalar operations extend to tensors by applying them independently to every element:

$$
[\exp(X)]_{i,j}=\exp(X_{i,j}),
\qquad
[X\odot Y]_{i,j}=X_{i,j}Y_{i,j}.
$$

<div class="legacy-code">
  <div class="code-line"><span class="ln">1</span><span class="code-text">X * Y          <span class="comment"># element-wise product</span></span></div>
  <div class="code-line"><span class="ln">2</span><span class="code-text">X @ W          <span class="comment"># matrix multiplication</span></span></div>
  <div class="code-line"><span class="ln">3</span><span class="code-text">torch.exp(X)   <span class="comment"># element-wise exponential</span></span></div>
</div>

The element-wise product of two matrices is also called their <a href="https://en.wikipedia.org/wiki/Hadamard_product_(matrices)">Hadamard product</a>. In neural networks, element-wise non-linear functions are called <span class="accent">activation functions</span>.

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Broadcasting rules">

Before an element-wise operation, align the two shapes from the right:

<div class="broadcast-rules">
  <div><b>1</b><span><strong>Right-align</strong> the axes. Missing leading axes are treated as having size <strong>1</strong>.</span></div>
  <div><b>2</b><span>Aligned sizes <i>p</i> and <i>q</i> are compatible if <i>p</i> = <i>q</i>, <i>p</i> = 1, or <i>q</i> = 1.</span></div>
  <div><b>3</b><span>The output size is max(<i>p</i>, <i>q</i>). Any incompatible pair raises an error.</span></div>
</div>

<div class="broadcast-examples">
  <div class="head"><span>left</span><span>right</span><span>result</span></div>
  <div><code>(B,T,D)</code><code>(D)</code><b>(B,T,D)</b></div>
  <div><code>(B,T,D)</code><code>(T,1)</code><b>(B,T,D)</b></div>
  <div><code>(32,20,128)</code><code>(32,128)</code><b class="error">error</b></div>
  <div><code>(3,1)</code><code>(1,3)</code><b>(3,3)</b></div>
</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import PyRunner from '../components/PyRunner.vue'

const broadcastingCode = [
  'import numpy as np',
  'X = (2, 3, 4)  # (B, T, D)',
  'for Y in [(4,), (3, 1), (2, 4)]:',
  '    try: print(Y, "->", np.broadcast_shapes(X, Y))',
  '    except ValueError: print(Y, "-> error")',
].join('\n')

const broadcastingOutput = [
  '(4,) -> (2, 3, 4)',
  '(3, 1) -> (2, 3, 4)',
  '(2, 4) -> error',
].join('\n')
</script>

<BeamerFrame title="Broadcasting in Python">

Check compatible shapes directly:

<PyRunner :code-rows="5" :initial-code="broadcastingCode" :initial-output="broadcastingOutput" />

<div class="rule-line small">

For a neural-network bias, $(B,H)+(H)\rightarrow(B,H)$: the same bias is added to every row of the batch.

</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
</script>

<BeamerFrame title="Our first neural network layer">

The operations introduced so far already define a fully connected layer:

$$
\mathbf{H}=\psi(\mathbf{X}\mathbf{W}+\mathbf{b}),
\qquad
\mathbf{X}\sim(B,D),\quad
\mathbf{H}\sim(B,H),\quad
\mathbf{b}\sim(H).
$$

<div class="operation-key">
  <div><b>XW</b><span>mix features (linearly)</span></div>
  <div><b>+ b</b><span>broadcast over the batch</span></div>
  <div><b>ψ</b><span>apply element-wise a non-linear transformation</span></div>
</div>

<div class="definition-box">

The parameters are $\boldsymbol{\theta}=\{\mathbf{W},\mathbf{b}\}$. How do we choose them?

</div>

</BeamerFrame>
