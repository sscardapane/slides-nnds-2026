<template>
  <div
    class="equation-inspector"
    :class="{ 'has-active': active, inline, compact }"
  >
    <div
      ref="equation"
      class="equation"
      v-html="equationHtml"
      @mousemove="hoverFromEquation"
      @mouseleave="hovered = ''"
      @click="pinFromEquation"
    />

    <div class="inspector-window" :aria-label="label">
      <span class="window-title">{{ label }}</span>
      <button
        v-for="item in normalizedItems"
        :key="item.id"
        type="button"
        class="inspector-chip"
        :class="{ selected: active === item.id }"
        :style="{ color: item.color }"
        @mouseenter="hovered = item.id"
        @mouseleave="hovered = ''"
        @focus="hovered = item.id"
        @blur="hovered = ''"
        @click="togglePin(item.id)"
        v-html="item.html"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import katex from 'katex'

const props = defineProps({
  tex: { type: String, required: true },
  items: { type: Array, required: true },
  label: { type: String, default: 'highlight' },
  inline: { type: Boolean, default: false },
  compact: { type: Boolean, default: false },
})

const palette = ['#3f6f9f', '#b26b00', '#2f7d4a', '#7a5a91', '#8c0000', '#547174']
const equation = ref(null)
const hovered = ref('')
const pinned = ref('')
const active = computed(() => hovered.value || pinned.value)

const normalizedItems = computed(() => props.items.map((item, index) => ({
  id: item.id,
  color: item.color || palette[index % palette.length],
  html: katex.renderToString(item.tex || item.id, {
    displayMode: false,
    throwOnError: false,
    strict: 'ignore',
    trust: true,
  }),
})))

const equationHtml = computed(() => katex.renderToString(props.tex, {
  displayMode: true,
  throwOnError: false,
  strict: 'ignore',
  trust: true,
}))

function idFromTarget(target) {
  if (!(target instanceof Element))
    return ''
  return target.closest('[data-inspect]')?.dataset.inspect || ''
}

function hoverFromEquation(event) {
  hovered.value = idFromTarget(event.target)
}

function pinFromEquation(event) {
  const id = idFromTarget(event.target)
  if (id)
    togglePin(id)
}

function togglePin(id) {
  pinned.value = pinned.value === id ? '' : id
}

function applyHighlight() {
  if (!equation.value)
    return

  const item = normalizedItems.value.find(candidate => candidate.id === active.value)
  equation.value.querySelectorAll('[data-inspect]').forEach((node) => {
    const selected = Boolean(item && node.dataset.inspect === item.id)
    node.classList.toggle('is-active', selected)
    if (selected)
      node.style.setProperty('--inspect-color', item.color)
    else
      node.style.removeProperty('--inspect-color')
  })
}

watch([active, equationHtml], () => nextTick(applyHighlight))
onMounted(applyHighlight)
</script>

<style scoped>
.equation {
  margin: -3px 0 8px;
  min-height: 55px;
  color: var(--nnds-ink, #24383c);
  text-align: center;
}

.equation-inspector.inline {
  display: grid;
  grid-template-columns: max-content max-content;
  gap: 24px;
  align-items: center;
  justify-content: center;
  margin: -6px 0 0;
}

.equation-inspector.inline .equation {
  min-height: 0;
  margin: 0;
}

.equation-inspector.inline .inspector-window {
  margin: 0;
}

.equation :deep(.katex-display) {
  margin: 0;
}

.equation :deep(.katex) {
  font-size: 1.08em;
}

.equation-inspector.compact .equation {
  min-height: 48px;
  margin-bottom: 3px;
}

.equation-inspector.compact .inspector-window {
  min-height: 29px;
  margin-top: 3px;
  padding-top: 2px;
  padding-bottom: 2px;
}

.equation :deep([data-inspect]) {
  box-sizing: border-box;
  border-radius: 3px;
  cursor: pointer;
  transition: color 120ms ease, background 120ms ease, box-shadow 120ms ease, opacity 120ms ease;
}

.has-active .equation :deep([data-inspect]) {
  opacity: .28;
}

.has-active .equation :deep([data-inspect].is-active),
.has-active .equation :deep([data-inspect].is-active [data-inspect]) {
  opacity: 1;
}

.has-active .equation :deep([data-inspect].is-active) {
  color: var(--inspect-color);
  background: color-mix(in srgb, var(--inspect-color) 10%, transparent);
  box-shadow: 0 0 0 4px var(--inspect-color);
}

.inline.has-active .equation :deep([data-inspect].is-active) {
  box-shadow: 0 0 0 3px var(--inspect-color);
}

.inspector-window {
  display: flex;
  gap: 7px;
  align-items: center;
  width: max-content;
  min-height: 32px;
  margin: 8px auto 0;
  padding: 4px 8px 4px 10px;
  border: 1px solid var(--nnds-rule, #cfd8d8);
  border-radius: 6px;
  background: rgba(255, 255, 255, .82);
  box-shadow: 0 1px 2px rgba(35, 57, 60, .08);
}

.window-title {
  margin-right: 3px;
  color: var(--nnds-ink-soft, #5f7073);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: .045em;
  text-transform: uppercase;
}

.inspector-chip {
  display: grid;
  place-items: center;
  min-width: 25px;
  height: 25px;
  padding: 0 6px;
  border: 1px solid currentColor;
  border-radius: 14px;
  background: #fff;
  font: inherit;
  cursor: pointer;
  transition: background 120ms ease, box-shadow 120ms ease, transform 120ms ease;
}

.inspector-chip :deep(.katex) {
  color: inherit;
  font-size: 16px;
}

.inspector-chip:hover,
.inspector-chip:focus-visible,
.inspector-chip.selected {
  outline: none;
  background: color-mix(in srgb, currentColor 10%, white);
  box-shadow: 0 0 0 3px currentColor;
  transform: translateY(-1px);
}
</style>
