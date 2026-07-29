<template>
  <div class="opt-lab">
    <div v-if="mode === 'batch'" class="batch-demo">
      <div class="controls">
        <label>
          Batch size <strong>{{ batch }}</strong>
          <input v-model.number="batch" type="range" min="1" max="128" step="1" />
        </label>
        <div class="batch-presets" aria-label="Batch-size presets">
          <button @click="batch = 4">4</button>
          <button @click="batch = 32">32</button>
          <button @click="batch = 128">128</button>
        </div>
        <button @click="seed += 1">Resample mini-batches</button>
      </div>

      <div class="batch-readout">
        <span>gradient-noise scale ∝ 1/√B: <strong>{{ noiseScale.toFixed(3) }}</strong></span>
        <span>examples used in 60 updates: <strong>{{ samplesProcessed }}</strong></span>
        <span>final-run spread: <strong>{{ finalSpread.toFixed(2) }}</strong> log units</span>
      </div>

      <svg class="loss-chart" viewBox="0 0 900 350" role="img" aria-label="Loss curves for stochastic gradient descent">
        <g class="grid">
          <line v-for="tick in yTicks" :key="`y-${tick}`" x1="72" :y1="yScale(tick)" x2="875" :y2="yScale(tick)" />
          <line v-for="tick in xTicks" :key="`x-${tick}`" :x1="xScale(tick)" y1="20" :x2="xScale(tick)" y2="302" />
        </g>
        <line class="axis" x1="72" y1="302" x2="875" y2="302" />
        <line class="axis" x1="72" y1="20" x2="72" y2="302" />
        <text class="axis-label" x="452" y="340">iteration</text>
        <text class="axis-label vertical" x="-162" y="22">log loss</text>
        <text v-for="tick in xTicks" :key="`xl-${tick}`" class="tick-label" :x="xScale(tick)" y="324">{{ tick }}</text>
        <text v-for="tick in yTicks" :key="`yl-${tick}`" class="tick-label y-label" x="62" :y="yScale(tick) + 5">{{ tick }}</text>

        <polyline
          :points="toPoints(fullBatchLoss)"
          class="full-batch"
          fill="none"
        />
        <polyline
          v-for="(run, index) in batchRuns"
          :key="`run-${seed}-${index}`"
          :points="toPoints(run)"
          class="sample-run"
          fill="none"
        />
        <polyline :points="toPoints(meanBatchLoss)" class="mean-run" fill="none" />
      </svg>

      <div class="legend">
        <span><i class="legend-line sample"></i>individual mini-batch runs</span>
        <span><i class="legend-line mean"></i>mean loss</span>
        <span><i class="legend-line full"></i>full gradient</span>
      </div>
    </div>

    <div v-else class="schedule-demo">
      <div class="controls schedule-controls">
        <label>
          Highlight
          <select v-model="schedule">
            <option value="constant">constant</option>
            <option value="step">step decay</option>
            <option value="cosine">warm-up + cosine</option>
          </select>
        </label>
        <label>
          Peak learning rate <strong>{{ peakLearningRate.toFixed(3) }}</strong>
          <input v-model.number="peakLearningRate" type="range" min="0.04" max="0.22" step="0.005" />
        </label>
        <label>
          Conditioning <strong>{{ conditioning }}</strong>
          <input v-model.number="conditioning" type="range" min="4" max="20" step="1" />
        </label>
      </div>

      <div class="schedule-readout">
        <span>fixed-step stability boundary η &lt; 2/κ ≈ <strong>{{ stabilityLimit.toFixed(3) }}</strong></span>
        <span>selected final loss: <strong>{{ selectedFinalLoss.toExponential(1) }}</strong></span>
        <span>best at this setting: <strong>{{ scheduleLabels[bestSchedule] }}</strong></span>
      </div>

      <div class="schedule-plots">
        <svg class="comparison-chart" viewBox="0 0 590 330" role="img" aria-label="Loss curves under three learning-rate schedules">
          <g class="grid">
            <line v-for="tick in scheduleYTicks" :key="`sy-${tick}`" x1="66" :y1="scheduleYScale(tick)" x2="575" :y2="scheduleYScale(tick)" />
            <line v-for="tick in scheduleXTicks" :key="`sx-${tick}`" :x1="scheduleXScale(tick)" y1="24" :x2="scheduleXScale(tick)" y2="282" />
          </g>
          <line class="axis" x1="66" y1="282" x2="575" y2="282" />
          <line class="axis" x1="66" y1="24" x2="66" y2="282" />
          <text class="plot-title" x="72" y="18">log loss</text>
          <text class="axis-label" x="318" y="320">iteration</text>
          <text v-for="tick in scheduleXTicks" :key="`sxl-${tick}`" class="tick-label" :x="scheduleXScale(tick)" y="304">{{ tick }}</text>
          <text v-for="tick in scheduleYTicks" :key="`syl-${tick}`" class="tick-label y-label" x="56" :y="scheduleYScale(tick) + 5">{{ tick }}</text>
          <polyline
            v-for="name in scheduleNames"
            :key="name"
            :points="toSchedulePoints(scheduleLosses[name])"
            :class="['schedule-loss', { active: schedule === name }]"
            fill="none"
          />
        </svg>

        <svg class="learning-rate-chart" viewBox="0 0 310 330" role="img" aria-label="Selected learning-rate schedule">
          <g class="grid">
            <line v-for="tick in learningRateYTicks" :key="`ly-${tick}`" x1="48" :y1="learningRateYScale(tick)" x2="296" :y2="learningRateYScale(tick)" />
          </g>
          <line class="axis" x1="48" y1="282" x2="296" y2="282" />
          <line class="axis" x1="48" y1="24" x2="48" y2="282" />
          <text class="plot-title" x="54" y="18">learning rate</text>
          <text class="axis-label" x="171" y="320">iteration</text>
          <text v-for="tick in learningRateYTicks" :key="`lyl-${tick}`" class="tick-label y-label" x="40" :y="learningRateYScale(tick) + 5">{{ tick.toFixed(2) }}</text>
          <polyline :points="learningRatePoints" class="selected-schedule" fill="none" />
        </svg>
      </div>

      <div class="legend schedule-legend">
        <span v-for="name in scheduleNames" :key="`legend-${name}`" :class="{ emphasized: schedule === name }">
          <i :class="['legend-line', `schedule-${name}`]"></i>{{ scheduleLabels[name] }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  mode: { type: String, required: true },
})

const iterations = 60
const batch = ref(16)
const seed = ref(1)
const schedule = ref('cosine')
const peakLearningRate = ref(0.16)
const conditioning = ref(12)
const scheduleNames = ['constant', 'step', 'cosine']
const scheduleLabels = {
  constant: 'constant',
  step: 'step decay',
  cosine: 'warm-up + cosine',
}

function mulberry32(initialSeed) {
  let state = initialSeed >>> 0
  return () => {
    state += 0x6D2B79F5
    let value = state
    value = Math.imul(value ^ (value >>> 15), value | 1)
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61)
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296
  }
}

function gaussian(random) {
  const u = Math.max(random(), 1e-9)
  const v = random()
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v)
}

function stochasticLosses(batchSize, runSeed) {
  const random = mulberry32(runSeed)
  let theta = 3.2
  const losses = []
  for (let t = 0; t <= iterations; t += 1) {
    losses.push(0.5 * theta * theta)
    const noise = (2.4 / Math.sqrt(batchSize)) * gaussian(random)
    theta -= 0.085 * (theta + noise)
  }
  return losses
}

function deterministicLosses() {
  let theta = 3.2
  const losses = []
  for (let t = 0; t <= iterations; t += 1) {
    losses.push(0.5 * theta * theta)
    theta -= 0.085 * theta
  }
  return losses
}

const batchRuns = computed(() =>
  Array.from({ length: 6 }, (_, index) =>
    stochasticLosses(batch.value, seed.value * 97 + index * 7919),
  ),
)

const meanBatchLoss = computed(() =>
  Array.from({ length: iterations + 1 }, (_, index) =>
    batchRuns.value.reduce((sum, run) => sum + run[index], 0) / batchRuns.value.length,
  ),
)

const fullBatchLoss = deterministicLosses()
const noiseScale = computed(() => 1 / Math.sqrt(batch.value))
const samplesProcessed = computed(() => iterations * batch.value)
const finalSpread = computed(() => {
  const values = batchRuns.value.map(run => logLoss(run[run.length - 1]))
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length
  return Math.sqrt(values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length)
})
const xTicks = [0, 15, 30, 45, 60]
const yTicks = [1, 0, -1, -2, -3]
const xScale = value => 72 + (value / iterations) * 803
const yScale = value => 20 + ((1.1 - value) / 4.3) * 282
const logLoss = value => Math.log10(Math.max(value, 1e-3))
const toPoints = values =>
  values.map((value, index) => `${xScale(index)},${yScale(logLoss(value))}`).join(' ')

function learningRateAt(name, step) {
  const progress = step / iterations
  const peak = peakLearningRate.value
  if (name === 'constant') return peak
  if (name === 'step') return progress < 0.4 ? peak : progress < 0.72 ? peak * 0.35 : peak * 0.1
  if (progress < 0.12) return peak * (0.12 + 0.88 * progress / 0.12)
  return peak * 0.5 * (1 + Math.cos(Math.PI * (progress - 0.12) / 0.88))
}

function scheduledLosses(name) {
  let x = 4
  let y = 1.3
  const losses = []
  for (let t = 0; t <= iterations; t += 1) {
    const loss = 0.5 * (x * x + conditioning.value * y * y)
    losses.push(Math.min(loss, 160))
    const eta = learningRateAt(name, t)
    x -= eta * x
    y -= eta * conditioning.value * y
  }
  return losses
}

const scheduleLosses = computed(() =>
  Object.fromEntries(scheduleNames.map(name => [name, scheduledLosses(name)])),
)
const stabilityLimit = computed(() => 2 / conditioning.value)
const selectedFinalLoss = computed(() => {
  const values = scheduleLosses.value[schedule.value]
  return values[values.length - 1]
})
const bestSchedule = computed(() =>
  scheduleNames.reduce((best, name) => {
    const bestLoss = scheduleLosses.value[best].at(-1)
    const candidateLoss = scheduleLosses.value[name].at(-1)
    return candidateLoss < bestLoss ? name : best
  }, scheduleNames[0]),
)

const scheduleXTicks = [0, 20, 40, 60]
const scheduleYTicks = [2, 1, 0, -1, -2, -3]
const scheduleXScale = value => 66 + (value / iterations) * 509
const scheduleYScale = value => 24 + ((2.2 - value) / 5.4) * 258
const toSchedulePoints = values =>
  values
    .map((value, index) => `${scheduleXScale(index)},${scheduleYScale(Math.log10(Math.max(value, 1e-3)))}`)
    .join(' ')

const learningRateYTicks = computed(() => [0, peakLearningRate.value / 2, peakLearningRate.value])
const learningRateYScale = value => 282 - (value / Math.max(peakLearningRate.value, 1e-6)) * 242
const learningRatePoints = computed(() =>
  Array.from({ length: iterations + 1 }, (_, index) =>
    `${48 + (index / iterations) * 248},${learningRateYScale(learningRateAt(schedule.value, index))}`,
  ).join(' '),
)
</script>

<style scoped>
.opt-lab {
  width: 100%;
  margin: 0 auto;
  color: #24383c;
}
.controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 34px;
  min-height: 42px;
  margin-bottom: 4px;
  font-size: .82em;
}
.controls label {
  display: flex;
  align-items: center;
  gap: 10px;
}
.controls strong {
  min-width: 48px;
  color: #8c0000;
  font-weight: 600;
}
.controls input {
  width: 245px;
  accent-color: #8c0000;
}
.controls select,
.controls button,
.controls + button,
button {
  border: 1px solid #8c0000;
  background: #fff;
  color: #8c0000;
  font: inherit;
}
.controls select { padding: 5px 9px; }
.controls button { padding: 7px 14px; cursor: pointer; }
.batch-presets {
  display: flex;
  gap: 5px;
}
.batch-presets button {
  min-width: 40px;
  padding: 6px 8px;
  cursor: pointer;
}
.batch-readout,
.schedule-readout {
  display: flex;
  justify-content: center;
  gap: 28px;
  color: #667678;
  font-size: .66em;
  line-height: 1.3;
}
.batch-readout strong,
.schedule-readout strong {
  color: #8c0000;
  font-weight: 600;
}
.loss-chart {
  display: block;
  width: 100%;
  height: 285px;
}
.schedule-controls {
  gap: 20px;
  font-size: .72em;
}
.schedule-controls input { width: 170px; }
.schedule-plots {
  display: grid;
  grid-template-columns: 1.8fr 1fr;
  gap: 12px;
  margin-top: 3px;
}
.comparison-chart,
.learning-rate-chart {
  display: block;
  width: 100%;
  height: 330px;
}
.grid line {
  stroke: #dfe4e5;
  stroke-width: 1;
}
.axis {
  stroke: #758487;
  stroke-width: 1.5;
}
.axis-label,
.plot-title {
  fill: #42575a;
  font-family: 'Fira Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  text-anchor: middle;
}
.plot-title {
  fill: #24383c;
  text-anchor: start;
}
.axis-label.vertical { transform: rotate(-90deg); }
.tick-label {
  fill: #7b898b;
  font-family: 'Fira Sans', sans-serif;
  font-size: 13px;
  text-anchor: middle;
}
.tick-label.y-label { text-anchor: end; }
.sample-run {
  stroke: #7fa7d5;
  stroke-width: 2;
  opacity: .42;
}
.mean-run {
  stroke: #8c0000;
  stroke-width: 4;
}
.full-batch {
  stroke: #42575a;
  stroke-width: 3;
  stroke-dasharray: 9 7;
}
.schedule-loss {
  stroke: #aab4b6;
  stroke-width: 2.5;
  opacity: .72;
}
.schedule-loss.active {
  stroke: #8c0000;
  stroke-width: 4;
  opacity: 1;
}
.selected-schedule {
  stroke: #8c0000;
  stroke-width: 4;
}
.legend {
  display: flex;
  justify-content: center;
  gap: 34px;
  margin-top: -4px;
  color: #667678;
  font-size: .7em;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.legend-line {
  display: inline-block;
  width: 34px;
  height: 0;
  border-top: 3px solid #7fa7d5;
}
.legend-line.mean,
.legend-line.schedule-cosine { border-color: #8c0000; }
.legend-line.full { border-color: #42575a; border-top-style: dashed; }
.legend-line.schedule-constant,
.legend-line.schedule-step,
.legend-line.schedule-cosine { border-color: #aab4b6; }
.schedule-legend .emphasized {
  color: #8c0000;
  font-weight: 600;
}
.schedule-legend .emphasized .legend-line { border-color: #8c0000; }
</style>
