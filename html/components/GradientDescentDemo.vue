<template>
  <div class="gd-demo">
    <svg :width="width" :height="height" class="gd-plot" role="img" aria-label="Gradient descent iterates on a scalar quadratic">
      <polyline :points="curvePoints" fill="none" stroke="#999" stroke-width="2" />
      <line :x1="0" :y1="toY(0)" :x2="width" :y2="toY(0)" stroke="#ccc" />
      <line :x1="toX(0)" :y1="0" :x2="toX(0)" :y2="height" stroke="#ccc" />
      <polyline :points="pathPoints" fill="none" stroke="#8c0000" stroke-width="3" stroke-dasharray="4 3" />
      <circle
        v-for="(point, index) in visibleHistory"
        :key="index"
        :cx="toX(point)"
        :cy="toY(point * point)"
        r="4"
        :fill="index === visibleHistory.length - 1 ? '#d79b00' : '#8c0000'"
      />
    </svg>

    <div class="gd-controls">
      <div class="gd-recurrence">
        <div class="gd-equation">
          <i>x</i><sub>t+1</sub>
          <span>=</span>
          <span class="gd-factor">(1 − 2<i>η</i>)</span>
          <i>x</i><sub>t</sub>
        </div>
        <div class="gd-multiplier">
          <span>multiplier</span>
          <strong>1 − 2<i>η</i> = {{ multiplier.toFixed(2) }}</strong>
        </div>
      </div>

      <label class="gd-slider">
        Learning rate <b>{{ lr.toFixed(2) }}</b>
        <input type="range" min="0.01" max="1.10" step="0.01" v-model.number="lr" @input="reset" />
      </label>

      <div class="gd-presets">
        <button @click="setLearningRate(0.10)">slow</button>
        <button @click="setLearningRate(0.75)">oscillatory</button>
        <button @click="setLearningRate(1.05)">unstable</button>
      </div>

      <div :class="['gd-regime', regimeClass]">{{ regimeLabel }}</div>

      <div class="gd-buttons">
        <button @click="step">Step</button>
        <button @click="runAll">Run 15 steps</button>
        <button @click="reset">Reset</button>
      </div>

      <div class="gd-status">
        step {{ history.length - 1 }}:
        x = {{ currentX.toFixed(3) }},
        f(x) = {{ (currentX ** 2).toFixed(3) }}
        <span v-if="Math.abs(currentX) > xRange" class="gd-diverging">— outside the plot</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const width = 520
const height = 320
const xRange = 3.2

const lr = ref(0.1)
const x0 = 2.6
const history = ref([x0])

const multiplier = computed(() => 1 - 2 * lr.value)
const currentX = computed(() => history.value[history.value.length - 1])
const visibleHistory = computed(() => history.value.filter(value => Math.abs(value) <= xRange))
const regimeLabel = computed(() => {
  if (lr.value < 0.5) return 'monotone convergence'
  if (Math.abs(lr.value - 0.5) < 1e-9) return 'minimum in one step'
  if (lr.value < 1) return 'oscillatory convergence'
  if (Math.abs(lr.value - 1) < 1e-9) return 'persistent oscillation'
  return 'divergence'
})
const regimeClass = computed(() => {
  if (lr.value < 1) return 'convergent'
  if (Math.abs(lr.value - 1) < 1e-9) return 'boundary'
  return 'divergent'
})

function toX(x) { return (x + xRange) / (2 * xRange) * width }
function toY(y) { return height - (y / (xRange * xRange)) * height }

const curvePoints = Array.from({ length: 60 }, (_, index) => {
  const x = -xRange + (2 * xRange) * (index / 59)
  return `${toX(x)},${toY(x * x)}`
}).join(' ')

const pathPoints = computed(() =>
  visibleHistory.value.map(value => `${toX(value)},${toY(value * value)}`).join(' '),
)

function gradStep(x) {
  return x - lr.value * 2 * x
}

function step() {
  history.value = [...history.value, gradStep(currentX.value)]
}

function runAll() {
  for (let index = 0; index < 15; index += 1) step()
}

function reset() {
  history.value = [x0]
}

function setLearningRate(value) {
  lr.value = value
  reset()
}
</script>

<style scoped>
.gd-demo {
  display: flex;
  gap: 2em;
  align-items: center;
  justify-content: center;
  margin: 8px auto 2px;
}
.gd-plot {
  border: 1px solid #9ba8aa;
  background: #fff;
}
.gd-controls {
  display: flex;
  width: 390px;
  flex-direction: column;
  gap: 0.6em;
  font-size: 0.78em;
}
.gd-recurrence {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.15em;
  align-items: center;
  padding-bottom: 0.35em;
  border-bottom: 1px solid #9ba8aa;
}
.gd-equation {
  display: flex;
  align-items: baseline;
  gap: 0.18em;
  white-space: nowrap;
  font-family: KaTeX_Main, 'Times New Roman', serif;
  font-size: 1.35em;
}
.gd-equation sub {
  font-size: 0.62em;
}
.gd-factor {
  color: #8c0000;
}
.gd-multiplier {
  display: flex;
  flex-direction: column;
  gap: 0.05em;
  padding-left: 0.8em;
  border-left: 2px solid #d7b2b2;
  color: #667678;
  font-size: 0.72em;
  line-height: 1.2;
}
.gd-multiplier strong {
  color: #8c0000;
  font-weight: 600;
  white-space: nowrap;
}
.gd-slider {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.2em 0.7em;
  align-items: center;
}
.gd-slider input {
  grid-column: 1 / -1;
  width: 100%;
  accent-color: #8c0000;
}
.gd-presets,
.gd-buttons {
  display: flex;
  gap: 0.45em;
}
.gd-presets button,
.gd-buttons button {
  padding: 0.24em 0.65em;
  border: 1px solid #8c0000;
  background: #fff;
  color: #8c0000;
  cursor: pointer;
}
.gd-presets button:hover,
.gd-buttons button:hover {
  background: #f7eeee;
}
.gd-regime {
  padding-left: 0.55em;
  border-left: 4px solid #617b67;
  font-weight: 600;
}
.gd-regime.boundary {
  border-color: #d79b00;
  color: #8a6200;
}
.gd-regime.divergent {
  border-color: #8c0000;
  color: #8c0000;
}
.gd-status {
  min-height: 1.4em;
  font-family: 'Fira Mono', monospace;
}
.gd-diverging {
  color: #8c0000;
  font-weight: 600;
}
</style>
