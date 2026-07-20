<!-- Real Python (not a JS lookalike) running client-side via Pyodide/WASM,
     loaded from a CDN on first use. This is the extreme end of the capability
     test: actual numpy execution inside a slide, no notebook/colab tab
     needed. Heavy (~10MB wasm) and network-dependent -- a real pipeline
     would want to self-host the runtime, evaluated separately. -->
<template>
  <div class="py-runner">
    <textarea v-model="code" class="py-code" spellcheck="false" rows="7" />
    <div class="py-controls">
      <button @click="run" :disabled="status === 'loading' || status === 'running'">
        {{ buttonLabel }}
      </button>
      <span class="py-status">{{ statusText }}</span>
    </div>
    <pre class="py-output" v-if="output !== null">{{ output }}</pre>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  initialCode: { type: String, default: 'print("hello from real Python")' },
})

const code = ref(props.initialCode)
const output = ref(null)
const status = ref('idle') // idle | loading | ready | running | error
let pyodide = null

const buttonLabel = computed(() => {
  if (status.value === 'loading') return 'Loading Python runtime…'
  if (status.value === 'running') return 'Running…'
  return 'Run'
})

const statusText = computed(() => {
  if (status.value === 'loading') return '(first run downloads the WASM runtime, ~10-15s)'
  if (status.value === 'error') return '(failed to load Pyodide -- check network)'
  return ''
})

async function ensurePyodide() {
  if (pyodide) return pyodide
  status.value = 'loading'
  if (!window.loadPyodide) {
    await new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js'
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
  }
  pyodide = await window.loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/',
  })
  await pyodide.loadPackage('numpy')
  return pyodide
}

async function run() {
  try {
    const py = await ensurePyodide()
    status.value = 'running'
    let captured = ''
    py.setStdout({ batched: (s) => { captured += s + '\n' } })
    await py.runPythonAsync(code.value)
    output.value = captured || '(no output)'
    status.value = 'ready'
  } catch (err) {
    output.value = String(err)
    status.value = 'error'
  }
}
</script>

<style scoped>
.py-runner {
  font-family: 'Fira Mono', monospace;
  font-size: 0.8em;
}
.py-code {
  width: 100%;
  box-sizing: border-box;
  background: #1e1e2e;
  color: #cdd6f4;
  border: none;
  padding: 0.75em;
  border-radius: 4px;
}
.py-controls {
  display: flex;
  align-items: center;
  gap: 0.75em;
  margin-top: 0.5em;
}
.py-controls button {
  padding: 0.3em 1em;
  border: 1px solid #ccc;
  background: #f7f7f7;
  cursor: pointer;
}
.py-controls button:disabled {
  opacity: 0.6;
  cursor: wait;
}
.py-status {
  opacity: 0.7;
}
.py-output {
  margin-top: 0.5em;
  background: #f5f5f5;
  padding: 0.6em;
  border-radius: 4px;
  white-space: pre-wrap;
}
</style>
