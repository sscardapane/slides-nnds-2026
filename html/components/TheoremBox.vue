<!-- Equivalent of the Beamer `theo` environment: a mdframed-style box with a
     red-top title tab, used for definitions/theorems. -->
<template>
  <div class="nnds-theorem">
    <div class="nnds-theorem-title">{{ title }}</div>
    <div class="nnds-theorem-body"><slot /></div>
  </div>
</template>

<script setup>
defineProps({ title: { type: String, required: true } })
</script>

<style scoped>
.nnds-theorem {
  border-top: 2px solid #ffcccc;
  background: #fff5f5;
  padding: 0.75em 1em 0.5em;
  margin: 0.75em 0;
  position: relative;
}
.nnds-theorem-title {
  position: absolute;
  top: -0.85em;
  right: 1em;
  background: #ffcccc;
  padding: 0.1em 0.6em;
  font-weight: bold;
  font-size: 0.85em;
}
.nnds-theorem-body {
  margin-top: 0.4em;
}
</style>
