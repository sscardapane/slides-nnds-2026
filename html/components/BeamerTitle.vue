<template>
  <section class="beamer-title">
    <img class="title-bg" :src="headerUrl" alt="" />
    <div class="title-wash"></div>
    <div class="title-copy">
      <div class="course">Neural Networks for Data Science</div>
      <div class="degree">Master's Degree in Data Science</div>
      <h1>{{ lecture }}</h1>
      <h2>{{ subtitle }}</h2>
      <div class="lecturer"><strong>Lecturer:</strong> S. Scardapane</div>
    </div>
    <img class="title-logo" :src="logoUrl" alt="Sapienza Università di Roma" />
  </section>
</template>

<script setup>
import headerUrl from '../public/nnds-header.jpeg'
import logoUrl from '../public/uniroma1.png'

defineProps({
  lecture: { type: String, default: 'Lecture 2: Mathematical preliminaries' },
  subtitle: { type: String, default: '2a. Tensors and linear maps' },
})
</script>

<style>
.beamer-title { position:absolute; inset:0; overflow:hidden; background:#f8f7f5; font-family:'Fira Sans',sans-serif; color:#23393c; }
.beamer-title .title-bg { position:absolute; z-index:0; inset:0; width:100%; height:100%; object-fit:contain; object-position:center bottom; opacity:.22; }
.beamer-title .title-wash { position:absolute; z-index:1; inset:0; background:linear-gradient(90deg,rgba(255,255,255,.96) 0%,rgba(255,255,255,.90) 52%,rgba(255,255,255,.55) 100%); }
.beamer-title .title-copy { position:absolute; z-index:2; left:72px; top:72px; width:720px; }
.beamer-title .course { font-size:30px; font-weight:400; }
.beamer-title .degree { margin-top:7px; font-size:20px; font-weight:600; }
.beamer-title h1 { margin:70px 0 0; font-size:43px; line-height:1.12; font-weight:600; letter-spacing:0; }
.beamer-title h2 { margin:14px 0 0; color:#8c0000; font-size:30px; font-weight:400; }
.beamer-title .lecturer { margin-top:54px; font-size:18px; }
.beamer-title .title-logo { position:absolute; z-index:3; right:64px; bottom:48px; width:170px; }
</style>
