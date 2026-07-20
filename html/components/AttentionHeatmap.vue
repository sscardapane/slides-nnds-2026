<!-- Toy self-attention pattern viewer: fixed random Q/K per token, weights
     recomputed live as temperature changes or the causal mask is toggled.
     Directly matches the "attention patterns, masking" experiment type
     already listed in the course recipe -- capability demo, not real
     course content (weights are synthetic, not from a trained model). -->
<template>
  <div class="attn-demo">
    <div class="attn-grid" :style="gridStyle">
      <div></div>
      <div v-for="(t, j) in tokens" :key="'colhead' + j" class="attn-tok">{{ t }}</div>
      <template v-for="(t, i) in tokens" :key="'row' + i">
        <div class="attn-tok">{{ t }}</div>
        <div
          v-for="(t2, j) in tokens"
          :key="'cell' + i + '-' + j"
          class="attn-cell"
          :style="{ background: cellColor(weights[i][j]) }"
        >{{ weights[i][j].toFixed(2) }}</div>
      </template>
    </div>

    <div class="attn-controls">
      <label>
        Temperature: <b>{{ temperature.toFixed(2) }}</b>
        <input type="range" min="0.2" max="3" step="0.1" v-model.number="temperature" />
      </label>
      <label>
        <input type="checkbox" v-model="causal" /> Causal mask (decoder-style)
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const tokens = ['The', 'cat', 'sat', 'on', 'mat']
const n = tokens.length

// fixed synthetic Q/K vectors (seeded, not learned) so the pattern is stable
// across re-renders and only reacts to temperature/masking.
const seed = [
  [0.8, -0.2, 0.1], [0.1, 0.9, -0.3], [-0.4, 0.2, 0.7],
  [0.6, 0.6, -0.1], [-0.2, -0.5, 0.8],
]
const Q = seed
const K = [
  [0.7, -0.1, 0.2], [0.2, 0.8, -0.2], [-0.3, 0.3, 0.6],
  [0.5, 0.5, 0.0], [-0.1, -0.4, 0.9],
]

const temperature = ref(1)
const causal = ref(false)

function dot(a, b) { return a.reduce((s, v, i) => s + v * b[i], 0) }

const weights = computed(() => {
  const scores = Q.map((q, i) => K.map((k, j) => dot(q, k) / Math.sqrt(3) / temperature.value))
  return scores.map((row, i) => {
    const masked = row.map((s, j) => (causal.value && j > i ? -Infinity : s))
    const m = Math.max(...masked.filter(Number.isFinite))
    const exps = masked.map(s => Number.isFinite(s) ? Math.exp(s - m) : 0)
    const sum = exps.reduce((a, b) => a + b, 0)
    return exps.map(e => e / sum)
  })
})

function cellColor(w) {
  const alpha = Math.min(1, w * 1.8)
  return `rgba(41, 128, 185, ${alpha})`
}

const gridStyle = computed(() => ({
  gridTemplateColumns: `3.5em repeat(${n}, 3.5em)`,
}))
</script>

<style scoped>
.attn-grid {
  display: grid;
  gap: 2px;
  font-size: 0.75em;
}
.attn-tok {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}
.attn-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2.4em;
  border-radius: 2px;
}
.attn-controls {
  display: flex;
  gap: 2em;
  margin-top: 1em;
  font-size: 0.85em;
}
</style>
