<!-- Interactive teaching demo: gradient descent on f(x) = x^2 with an
     adjustable learning rate, showing convergence/divergence live. This is
     the kind of thing that cannot exist in a static Beamer PDF — it is meant
     as a capability demo, not course content. -->
<template>
  <div class="gd-demo">
    <svg :width="width" :height="height" class="border border-gray-200">
      <!-- loss curve f(x) = x^2 -->
      <polyline :points="curvePoints" fill="none" stroke="#999" stroke-width="2" />
      <!-- axes -->
      <line :x1="0" :y1="toY(0)" :x2="width" :y2="toY(0)" stroke="#ccc" />
      <line :x1="toX(0)" :y1="0" :x2="toX(0)" :y2="height" stroke="#ccc" />
      <!-- descent path -->
      <polyline :points="pathPoints" fill="none" stroke="#2980b9" stroke-width="2" stroke-dasharray="4 3" />
      <circle
        v-for="(p, i) in history"
        :key="i"
        :cx="toX(p)"
        :cy="toY(p * p)"
        r="4"
        :fill="i === history.length - 1 ? '#c0392b' : '#2980b9'"
      />
    </svg>

    <div class="gd-controls">
      <label>
        Learning rate: <b>{{ lr.toFixed(2) }}</b>
        <input type="range" min="0.01" max="1.05" step="0.01" v-model.number="lr" @input="reset" />
      </label>
      <div class="gd-buttons">
        <button @click="step">Step</button>
        <button @click="runAll">Run 15 steps</button>
        <button @click="reset">Reset</button>
      </div>
      <div class="gd-status">
        x = {{ history[history.length - 1].toFixed(3) }},
        f(x) = {{ (history[history.length - 1] ** 2).toFixed(3) }}
        <span v-if="Math.abs(history[history.length - 1]) > 3" class="gd-diverging">— diverging</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const width = 420
const height = 260
const xRange = 3.2

const lr = ref(0.1)
const x0 = 2.6
const history = ref([x0])

function toX(x) { return (x + xRange) / (2 * xRange) * width }
function toY(y) { return height - (y / (xRange * xRange)) * height }

const curvePoints = Array.from({ length: 60 }, (_, i) => {
  const x = -xRange + (2 * xRange) * (i / 59)
  return `${toX(x)},${toY(x * x)}`
}).join(' ')

const pathPoints = ref(`${toX(x0)},${toY(x0 * x0)}`)

function gradStep(x) {
  // f(x) = x^2, f'(x) = 2x
  return x - lr.value * 2 * x
}

function step() {
  const last = history.value[history.value.length - 1]
  const next = gradStep(last)
  history.value = [...history.value, next]
  pathPoints.value = history.value.map(x => `${toX(x)},${toY(x * x)}`).join(' ')
}

function runAll() {
  for (let i = 0; i < 15; i++) step()
}

function reset() {
  history.value = [x0]
  pathPoints.value = `${toX(x0)},${toY(x0 * x0)}`
}
</script>

<style scoped>
.gd-demo {
  display: flex;
  gap: 2em;
  align-items: center;
}
.gd-controls {
  display: flex;
  flex-direction: column;
  gap: 0.75em;
  font-size: 0.85em;
}
.gd-buttons button {
  margin-right: 0.5em;
  padding: 0.25em 0.75em;
  border: 1px solid #ccc;
  background: #f7f7f7;
  cursor: pointer;
}
.gd-buttons button:hover {
  background: #eee;
}
.gd-diverging {
  color: #c0392b;
  font-weight: bold;
}
</style>
