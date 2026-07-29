<template>
  <component
    :is="block ? 'div' : 'span'"
    :class="{ 'math-tex-block': block }"
    v-html="rendered"
  />
</template>

<script setup>
import { computed } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const props = defineProps({
  tex: { type: String, required: true },
  block: { type: Boolean, default: false },
})

const rendered = computed(() => katex.renderToString(props.tex, {
  displayMode: props.block,
  throwOnError: false,
  strict: false,
}))
</script>

<style scoped>
.math-tex-block {
  text-align: center;
  margin: 0.55em 0;
}
</style>
