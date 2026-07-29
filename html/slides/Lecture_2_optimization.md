---
theme: default
layout: full
title: "NNDS 2026 — Lecture 2: Optimization in practice"
css: unocss
fonts:
  sans: 'Fira Sans'
  mono: 'Fira Mono'
colorSchema: light
routerMode: hash
themeConfig:
  pageOffset: 38
---

<style>@import '../styles/index.css';</style>

<script setup>
import BeamerTitle from '../components/BeamerTitle.vue'
</script>

<BeamerTitle subtitle="2c. Optimization in practice" />

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import GradientDescentDemo from '../components/GradientDescentDemo.vue'
</script>

<BeamerFrame title="Gradient descent">

For $f(x)=x^2$, compare the slow, oscillatory, and unstable regimes:

<GradientDescentDemo />

<div class="research-note">

The stability boundary follows directly from $x_{t+1}=(1-2\eta)x_t$: convergence requires $|1-2\eta|<1$.

</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import OptimizationLab from '../components/OptimizationLab.vue'
</script>

<BeamerFrame title="Choosing the batch size">

Keep the objective, learning rate, and number of updates fixed. Change $B$ or resample the mini-batches:

<OptimizationLab mode="batch" />

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import OptimizationLab from '../components/OptimizationLab.vue'
</script>

<BeamerFrame title="Learning-rate schedules">

Compare <strong>time-varying learning-rate schedules</strong>. Change the peak rate or the conditioning $\kappa$ and inspect both the schedule and the resulting loss:

<OptimizationLab mode="schedule" />

</BeamerFrame>
