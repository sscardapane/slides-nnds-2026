<!-- Live KaTeX-adjacent hover annotation, for "hero" equations only.
     Wraps a term with a colored underline; hovering shows the annotation.
     Not a general replacement for annotate-equations -- see the SVG-embed
     path (assets/cross_entropy_annotated.svg) for the default treatment. -->
<template>
  <span class="eq-annotate" :style="{ borderBottomColor: color }">
    <slot />
    <span class="eq-annotate-tooltip" :style="{ color }">{{ label }}</span>
  </span>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  color: { type: String, default: '#8c0000' },
})
</script>

<style scoped>
.eq-annotate {
  position: relative;
  border-bottom: 2px dotted;
  cursor: help;
}
.eq-annotate-tooltip {
  position: absolute;
  bottom: 1.6em;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  font-size: 0.5em;
  font-weight: bold;
  background: white;
  border: 1px solid currentColor;
  padding: 0.15em 0.5em;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s ease;
}
.eq-annotate:hover .eq-annotate-tooltip {
  opacity: 1;
}
</style>
