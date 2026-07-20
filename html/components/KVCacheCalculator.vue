<!-- Cheap, no-training capability demo: pure formulas, live as sliders move.
     Matches the "KV-cache cost" experiment type already listed in the
     course recipe. -->
<template>
  <div class="kv-calc">
    <div class="kv-sliders">
      <label>Sequence length: <b>{{ seqLen }}</b>
        <input type="range" min="128" max="32768" step="128" v-model.number="seqLen" />
      </label>
      <label>Layers: <b>{{ layers }}</b>
        <input type="range" min="1" max="80" v-model.number="layers" />
      </label>
      <label>Heads: <b>{{ heads }}</b>
        <input type="range" min="1" max="64" v-model.number="heads" />
      </label>
      <label>Head dim: <b>{{ headDim }}</b>
        <input type="range" min="32" max="256" step="8" v-model.number="headDim" />
      </label>
      <label>dtype:
        <select v-model.number="dtypeBytes">
          <option :value="4">fp32 (4B)</option>
          <option :value="2">fp16/bf16 (2B)</option>
          <option :value="1">int8 (1B)</option>
        </select>
      </label>
    </div>

    <div class="kv-results">
      <div class="kv-metric">
        <div class="kv-label">KV-cache memory (batch=1)</div>
        <div class="kv-value">{{ formatBytes(kvBytes) }}</div>
      </div>
      <div class="kv-metric">
        <div class="kv-label">Attention compute to generate the full sequence</div>
        <div class="kv-bars">
          <div class="kv-bar-row">
            <span>without cache (recompute every step)</span>
            <div class="kv-bar" :style="{ width: '100%', background: '#c0392b' }"></div>
            <span>{{ formatFlops(flopsNoCache) }}</span>
          </div>
          <div class="kv-bar-row">
            <span>with cache</span>
            <div class="kv-bar" :style="{ width: cacheBarWidth + '%', background: '#2980b9' }"></div>
            <span>{{ formatFlops(flopsCache) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const seqLen = ref(4096)
const layers = ref(32)
const heads = ref(32)
const headDim = ref(128)
const dtypeBytes = ref(2)

const kvBytes = computed(() =>
  2 * layers.value * seqLen.value * heads.value * headDim.value * dtypeBytes.value
)

// attention cost per generated token step is O(context length so far);
// without cache: recompute attention over the whole growing context every
// step -> sum_{t=1}^{L} t ~ L^2/2. With cache: O(1) new-token work per step
// (against the stored K/V) -> ~ L.
const flopsNoCache = computed(() => (seqLen.value * (seqLen.value + 1)) / 2)
const flopsCache = computed(() => seqLen.value)
const cacheBarWidth = computed(() => Math.max(1, (flopsCache.value / flopsNoCache.value) * 100))

function formatBytes(b) {
  if (b > 1e9) return (b / 1e9).toFixed(2) + ' GB'
  if (b > 1e6) return (b / 1e6).toFixed(1) + ' MB'
  return (b / 1e3).toFixed(1) + ' KB'
}
function formatFlops(f) {
  if (f > 1e9) return (f / 1e9).toFixed(2) + 'B token-steps'
  if (f > 1e6) return (f / 1e6).toFixed(1) + 'M token-steps'
  return Math.round(f) + ' token-steps'
}
</script>

<style scoped>
.kv-calc { font-size: 0.85em; }
.kv-sliders {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6em 2em;
}
.kv-results { margin-top: 1.2em; }
.kv-metric { margin-bottom: 1em; }
.kv-label { opacity: 0.7; margin-bottom: 0.3em; }
.kv-value { font-size: 1.6em; font-weight: bold; color: #2980b9; }
.kv-bar-row {
  display: grid;
  grid-template-columns: 15em 1fr 8em;
  align-items: center;
  gap: 0.6em;
  margin: 0.3em 0;
}
.kv-bar { height: 1em; border-radius: 2px; }
</style>
