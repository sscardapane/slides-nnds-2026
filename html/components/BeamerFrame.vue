<template>
  <section class="beamer-frame">
    <header>{{ title }}</header>
    <main><slot /></main>
    <footer>{{ displayedPage }}</footer>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

const props = defineProps({
  title: { type: String, required: true },
  // Rare escape hatch. Normal slides should rely on Slidev's automatic page.
  page: { type: [String, Number], default: '' },
})

const { $page, $slidev } = useSlideContext()
const pageOffset = computed(() => Number($slidev.configs.themeConfig?.pageOffset || 0))
const displayedPage = computed(() => props.page || $page.value + pageOffset.value)
</script>

<style>
.beamer-frame {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: #fff;
  color: #24383c;
  font-family: 'Fira Sans', sans-serif;
  font-size: 23px;
  font-weight: 300;
  line-height: 1.44;
}
.beamer-frame > header {
  height: 58px;
  box-sizing: border-box;
  padding: 13px 34px 0;
  background: #23393c;
  color: #fff;
  font-size: 27px;
  font-weight: 300;
  line-height: 1;
  text-align: right;
}
.beamer-frame > main {
  padding: 20px 61px 34px;
}
.beamer-frame > footer {
  position: absolute;
  right: 22px;
  bottom: 11px;
  color: #42575a;
  font-size: 13px;
}
.beamer-frame p { margin: 0 0 19px; }
.beamer-frame strong { font-weight: 600; }
.beamer-frame .accent { color: #8c0000; font-weight: 600; }
.beamer-frame .definition-box {
  margin: 0 0 22px;
  padding: 14px 28px;
  border: 3px solid #4b4b4b;
  border-radius: 10px;
  background: #fafafa;
}
.beamer-frame .muted { color: #929292; }
.beamer-frame .small { font-size: .78em; line-height: 1.45; }
.beamer-frame .compact { margin-bottom: 9px; }
.beamer-frame .axis-key {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px 24px;
  margin-top: 15px;
  color: #777;
  font-size: .76em;
}
.beamer-frame .axis-key b { color: #6c9ed6; font-weight: 600; }
.beamer-frame .two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 34px;
  align-items: start;
}
.beamer-frame .operation-key {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  margin: 16px 0 28px;
  padding: 13px 0;
  border-top: 1px solid #24383c;
  border-bottom: 1px solid #24383c;
  text-align: center;
}
.beamer-frame .operation-key b {
  display: block;
  color: #8c0000;
  font-size: 1.12em;
}
.beamer-frame .operation-key span {
  color: #888;
  font-size: .74em;
}
.beamer-frame .rule-line {
  margin: 14px 0;
  padding: 10px 0;
  border-top: 1px solid #24383c;
  border-bottom: 1px solid #24383c;
}
.beamer-frame .research-note {
  margin-top: 16px;
  padding-left: 14px;
  border-left: 4px solid #8c0000;
  color: #666;
  font-size: .76em;
}
.beamer-frame .katex-display { margin: .6em 0 1em; }
.beamer-frame .katex { font-size: 1.08em; }
.beamer-frame ul,
.beamer-frame ol { margin: 9px 0 0 24px; }
.beamer-frame li { margin: 9px 0; }
.beamer-frame .legacy-code {
  margin: 0 0 24px;
  padding: 8px 0 7px;
  border-top: 1px solid #24383c;
  border-bottom: 1px solid #24383c;
  font-family: 'Fira Mono', monospace;
  font-size: 19px;
  font-weight: 400;
  line-height: 1.38;
}
.beamer-frame .code-line {
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr);
  align-items: baseline;
  white-space: pre;
}
.beamer-frame .code-text { min-width: 0; }
.beamer-frame .ln {
  display: inline-block;
  width: 28px;
  color: #aeb4b5;
  font-size: 11px;
  text-align: right;
  margin-right: 11px;
}
.beamer-frame .kw { color: #0000d0; }
.beamer-frame .comment { color: #009900; }
.beamer-frame .math-row {
  display: grid;
  grid-template-columns: 230px 1fr;
  align-items: center;
  margin-top: -7px;
  color: #9a9a9a;
  text-align: left;
}
.beamer-frame .math-row .formula {
  color: #24383c;
  font-size: 25px;
  text-align: right;
  padding-right: 27px;
}
.beamer-frame .math-row .bracket,
.beamer-frame .math-row sub { color: #6c9ed6; }
.beamer-frame .math-row sub { font-size: 0.62em; }
.beamer-frame .broadcast-rules {
  margin: 13px 0 15px;
  border-top: 1px solid #24383c;
  border-bottom: 1px solid #24383c;
  font-size: .88em;
}
.beamer-frame .broadcast-rules > div {
  display: grid;
  grid-template-columns: 50px minmax(0, 1fr);
  gap: 14px;
  align-items: baseline;
  padding: 7px 14px;
}
.beamer-frame .broadcast-rules > div + div { border-top: 1px solid #d7dddd; }
.beamer-frame .broadcast-rules b:first-child {
  color: #8c0000;
  font-size: 1.15em;
}
.beamer-frame .broadcast-examples {
  display: grid;
  gap: 0;
  border-bottom: 1px solid #24383c;
}
.beamer-frame .broadcast-examples > div {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  align-items: baseline;
  padding: 5px 18px;
  border-top: 1px solid #d7dddd;
  text-align: center;
}
.beamer-frame .broadcast-examples .head {
  border-color: #24383c;
  color: #777;
  font-size: .72em;
  text-transform: uppercase;
}
.beamer-frame .broadcast-examples code {
  color: #24383c;
  font-family: 'Fira Mono', monospace;
  font-size: .8em;
}
.beamer-frame .broadcast-examples b { color: #8c0000; }
.beamer-frame .broadcast-examples .error { color: #666; }
.beamer-frame .optimization-overview { padding-top: 18px; }
.beamer-frame .optimization-overview .katex-display {
  margin: 1.05em 0 1.25em;
  font-size: 1.22em;
}
.beamer-frame .optimization-overview .operation-key {
  margin: 28px 0 34px;
  padding: 24px 0;
}
</style>
