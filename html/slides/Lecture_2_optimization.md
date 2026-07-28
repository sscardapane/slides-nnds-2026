---
theme: default
title: "NNDS 2026 — Lecture 2: Optimization in practice"
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

<BeamerTitle subtitle="2c. Optimization in practice" />

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import GradientDescentDemo from '../components/GradientDescentDemo.vue'
</script>

<BeamerFrame title="Gradient descent" page="39">

For $f(x)=x^2$, change the learning rate and inspect the iterations:

<GradientDescentDemo />

<div class="research-note">

Small values move slowly; sufficiently large values make the iteration unstable.

</div>

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import OptimizationLab from '../components/OptimizationLab.vue'
</script>

<BeamerFrame title="Choosing the batch size" page="40">

Keep the objective and learning rate fixed. Change $B$ or resample the mini-batches:

<OptimizationLab mode="batch" />

</BeamerFrame>

---
layout: full
---

<script setup>
import BeamerFrame from '../components/BeamerFrame.vue'
import OptimizationLab from '../components/OptimizationLab.vue'
</script>

<BeamerFrame title="Learning-rate schedules" page="41">

Instead of choosing a small (fixed) learning rate, we can also implement adaptive <strong>learning rate schedules</strong>:

<OptimizationLab mode="schedule" />

</BeamerFrame>
