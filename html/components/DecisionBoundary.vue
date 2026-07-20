<!-- The biggest capability demo: click to place labeled points, a real
     (tiny, hand-rolled) 2-layer MLP trains live via backprop, and the
     decision boundary redraws every step. Pure JS for smooth per-frame
     interactivity -- a Pyodide-backed version is possible (see the earlier
     PyRunner slide) but the async round-trip per animation frame makes
     dragging/live-play noticeably less smooth, so this one stays JS. -->
<template>
  <div class="db-demo">
    <canvas
      ref="canvas"
      :width="size"
      :height="size"
      class="db-canvas"
      @click="onCanvasClick"
    ></canvas>

    <div class="db-controls">
      <div class="db-row">
        <label><input type="radio" value="0" v-model="activeClass" /> class A</label>
        <label><input type="radio" value="1" v-model="activeClass" /> class B</label>
      </div>
      <div class="db-row">
        <button @click="toggleTrain">{{ training ? 'Pause' : 'Train live' }}</button>
        <button @click="stepOnce">Step</button>
        <button @click="resetWeights">Reset weights</button>
        <button @click="clearPoints">Clear points</button>
      </div>
      <label class="db-row">
        Learning rate: <b>{{ lr.toFixed(2) }}</b>
        <input type="range" min="0.05" max="2" step="0.05" v-model.number="lr" />
      </label>
      <div class="db-status">epoch {{ epoch }} — loss {{ loss.toFixed(4) }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const size = 300
const grid = 40 // resolution of the background decision-boundary render
const hidden = 8

const activeClass = ref('0')
const lr = ref(0.6)
const epoch = ref(0)
const loss = ref(0)
const training = ref(false)
const canvas = ref(null)

let points = [
  [-0.5, -0.5, 0], [-0.6, 0.2, 0], [-0.2, -0.7, 0], [0.1, -0.5, 0],
  [0.5, 0.5, 1], [0.6, -0.1, 1], [0.2, 0.7, 1], [-0.1, 0.5, 1],
]

let W1, b1, W2, b2
let rafId = null

function randInit() {
  W1 = Array.from({ length: 2 }, () => Array.from({ length: hidden }, () => (Math.random() - 0.5) * 1.5))
  b1 = Array.from({ length: hidden }, () => 0)
  W2 = Array.from({ length: hidden }, () => (Math.random() - 0.5) * 1.5)
  b2 = 0
}
randInit()

function forward(x0, x1) {
  const h = new Array(hidden)
  for (let j = 0; j < hidden; j++) {
    h[j] = Math.tanh(x0 * W1[0][j] + x1 * W1[1][j] + b1[j])
  }
  let z = b2
  for (let j = 0; j < hidden; j++) z += h[j] * W2[j]
  const out = 1 / (1 + Math.exp(-z))
  return { h, out }
}

function trainStep() {
  if (points.length === 0) return
  const gW1 = [[...W1[0]].fill(0), [...W1[1]].fill(0)]
  const gb1 = b1.map(() => 0)
  const gW2 = W2.map(() => 0)
  let gb2 = 0
  let totalLoss = 0

  for (const [x0, x1, y] of points) {
    const { h, out } = forward(x0, x1)
    const eps = 1e-7
    totalLoss += -(y * Math.log(out + eps) + (1 - y) * Math.log(1 - out + eps))
    const dz = out - y // d(loss)/d(pre-sigmoid)
    for (let j = 0; j < hidden; j++) {
      gW2[j] += dz * h[j]
    }
    gb2 += dz
    for (let j = 0; j < hidden; j++) {
      const dh = dz * W2[j] * (1 - h[j] * h[j])
      gW1[0][j] += dh * x0
      gW1[1][j] += dh * x1
      gb1[j] += dh
    }
  }

  const n = points.length
  for (let j = 0; j < hidden; j++) {
    W1[0][j] -= lr.value * gW1[0][j] / n
    W1[1][j] -= lr.value * gW1[1][j] / n
    b1[j] -= lr.value * gb1[j] / n
    W2[j] -= lr.value * gW2[j] / n
  }
  b2 -= lr.value * gb2 / n

  loss.value = totalLoss / n
  epoch.value++
}

function draw() {
  const ctx = canvas.value.getContext('2d')
  const cell = size / grid
  for (let i = 0; i < grid; i++) {
    for (let j = 0; j < grid; j++) {
      const x0 = (i / grid) * 2 - 1
      const x1 = (j / grid) * 2 - 1
      const { out } = forward(x0, x1)
      const r = Math.round(192 + out * (231 - 192))
      const g = Math.round(57 + out * (76 - 57))
      const b = Math.round(43 + out * (60 - 43))
      // blend blue (class 0) -> red (class 1)
      const cr = Math.round(41 + out * (192 - 41))
      const cg = Math.round(128 + out * (57 - 128))
      const cb = Math.round(185 + out * (43 - 185))
      ctx.fillStyle = `rgba(${cr},${cg},${cb},0.55)`
      ctx.fillRect(i * cell, size - (j + 1) * cell, cell + 1, cell + 1)
    }
  }
  for (const [x0, x1, y] of points) {
    const px = (x0 + 1) / 2 * size
    const py = size - (x1 + 1) / 2 * size
    ctx.beginPath()
    ctx.arc(px, py, 6, 0, Math.PI * 2)
    ctx.fillStyle = y === 0 ? '#2980b9' : '#c0392b'
    ctx.fill()
    ctx.strokeStyle = 'white'
    ctx.lineWidth = 2
    ctx.stroke()
  }
}

function onCanvasClick(e) {
  const rect = canvas.value.getBoundingClientRect()
  const px = e.clientX - rect.left
  const py = e.clientY - rect.top
  const x0 = (px / size) * 2 - 1
  const x1 = ((size - py) / size) * 2 - 1
  points.push([x0, x1, Number(activeClass.value)])
  draw()
}

function loop() {
  trainStep()
  draw()
  if (training.value) rafId = requestAnimationFrame(loop)
}

function toggleTrain() {
  training.value = !training.value
  if (training.value) loop()
  else if (rafId) cancelAnimationFrame(rafId)
}

function stepOnce() {
  trainStep()
  draw()
}

function resetWeights() {
  randInit()
  epoch.value = 0
  draw()
}

function clearPoints() {
  points = []
  draw()
}

onMounted(draw)
onBeforeUnmount(() => { if (rafId) cancelAnimationFrame(rafId) })
</script>

<style scoped>
.db-demo {
  display: flex;
  gap: 1.5em;
  align-items: flex-start;
}
.db-canvas {
  border: 1px solid #ccc;
  cursor: crosshair;
}
.db-controls {
  display: flex;
  flex-direction: column;
  gap: 0.6em;
  font-size: 0.8em;
}
.db-row {
  display: flex;
  gap: 0.8em;
  align-items: center;
}
.db-row button {
  padding: 0.25em 0.7em;
  border: 1px solid #ccc;
  background: #f7f7f7;
  cursor: pointer;
}
.db-status {
  opacity: 0.75;
}
</style>
