<!-- Illustrative (not real-trained) fault injector: picking a scenario swaps
     in a hand-crafted but representative train/val curve. Directly matches
     the course's own chosen framing -- "supervised learning reframed around
     debugging neural networks" -- rather than a generic capability demo. -->
<template>
  <div class="debug-demo">
    <select v-model="scenario" class="debug-select">
      <option v-for="s in Object.keys(scenarios)" :key="s" :value="s">{{ scenarios[s].label }}</option>
    </select>

    <svg :width="width" :height="height" class="debug-chart">
      <line :x1="pad" :y1="height - pad" :x2="width - pad" :y2="height - pad" stroke="#ccc" />
      <line :x1="pad" :y1="pad" :x2="pad" :y2="height - pad" stroke="#ccc" />
      <polyline :points="toPoints(current.train)" fill="none" stroke="#2980b9" stroke-width="2" />
      <polyline :points="toPoints(current.val)" fill="none" stroke="#c0392b" stroke-width="2" stroke-dasharray="5 3" />
    </svg>
    <div class="debug-legend">
      <span><span class="dot" style="background:#2980b9"></span>train loss</span>
      <span><span class="dot" style="background:#c0392b"></span>val loss</span>
    </div>

    <div class="debug-note">{{ current.note }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const width = 460
const height = 220
const pad = 24
const steps = 30
const maxLoss = 3

function clamp(v) { return Math.max(0, Math.min(maxLoss, v)) }

const scenarios = {
  healthy: {
    label: 'Healthy run',
    train: Array.from({ length: steps }, (_, i) => clamp(2.2 * Math.exp(-i / 10) + 0.08 + Math.random() * 0.03)),
    val: Array.from({ length: steps }, (_, i) => clamp(2.2 * Math.exp(-i / 10) + 0.18 + Math.random() * 0.04)),
    note: 'Train and val decrease together and plateau close to each other — a healthy fit.',
  },
  highLR: {
    label: 'Learning rate too high',
    train: Array.from({ length: steps }, (_, i) => clamp(1.5 + Math.sin(i * 0.9) * (0.6 + i * 0.08) + i * 0.03)),
    val: Array.from({ length: steps }, (_, i) => clamp(1.6 + Math.sin(i * 0.9 + 0.3) * (0.6 + i * 0.08) + i * 0.03)),
    note: 'Loss oscillates and trends upward instead of down — classic overshoot from too large a step size.',
  },
  noNorm: {
    label: 'No normalization (vanishing gradient)',
    train: Array.from({ length: steps }, (_, i) => clamp(2.5 - i * 0.01)),
    val: Array.from({ length: steps }, (_, i) => clamp(2.55 - i * 0.01)),
    note: 'Loss barely moves — gradients are vanishing through the unnormalized deep stack.',
  },
  leakage: {
    label: 'Label leakage',
    train: Array.from({ length: steps }, (_, i) => clamp(2.2 * Math.exp(-i / 2) + 0.01)),
    val: Array.from({ length: steps }, (_, i) => clamp(2.2 - i * 0.01 + Math.random() * 0.05)),
    note: 'Train loss collapses almost instantly while val loss barely improves — too good to be true, check for a leaked feature.',
  },
}

const scenario = ref('healthy')
const current = computed(() => scenarios[scenario.value])

function toPoints(series) {
  return series.map((v, i) => {
    const x = pad + (i / (steps - 1)) * (width - 2 * pad)
    const y = height - pad - (clamp(v) / maxLoss) * (height - 2 * pad)
    return `${x},${y}`
  }).join(' ')
}
</script>

<style scoped>
.debug-demo { font-size: 0.85em; }
.debug-select {
  padding: 0.3em 0.6em;
  margin-bottom: 0.75em;
}
.debug-chart {
  border: 1px solid #eee;
}
.debug-legend {
  display: flex;
  gap: 1.5em;
  margin-top: 0.4em;
}
.dot {
  display: inline-block;
  width: 0.8em;
  height: 0.8em;
  border-radius: 50%;
  margin-right: 0.3em;
}
.debug-note {
  margin-top: 0.6em;
  opacity: 0.8;
  max-width: 34em;
}
</style>
