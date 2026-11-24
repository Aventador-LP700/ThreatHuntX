<script setup lang="ts">
import { computed } from 'vue'
import { Activity, ArrowRight, BookOpen, Clock3, Fingerprint, FlaskConical, Layers3, Radar, Target } from 'lucide-vue-next'
import { coverage, runs, scenarios, showcase } from '../api'
import { titleCase } from '../learning'

const first = computed(() => scenarios.value.find(item => item.id === '02') ?? scenarios.value[0])
const guided = computed(() => scenarios.value.filter(item => item.core_lesson).length)
const latest = computed(() => runs.value.flatMap(run => run.alerts.map(alert => ({ alert, id: run.id }))))
const domains = computed(() => [...new Set(scenarios.value.map(item => item.category))])
</script>

<template>
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy">
      <div class="hero-kicker"><Radar :size="16" aria-hidden="true" /> THREAT HUNTING WORKSPACE</div>
      <h1 id="hero-title">Learn threat hunting.<br /><span>Follow the evidence.</span></h1>
      <p v-if="showcase">Explore a real lesson through read-only examples from the Community Lab. All events and alerts shown here use synthetic sample data.</p>
      <p v-else>Investigate realistic security signals, test detection rules, and build analyst skills in a local lab that runs on synthetic data.</p>
      <div class="actions">
        <RouterLink class="button primary" :to="first ? `/lesson/${first.id}` : '/learn'"><BookOpen :size="17" aria-hidden="true" /> Start Learning <ArrowRight :size="17" aria-hidden="true" /></RouterLink>
        <RouterLink class="button secondary" to="/techniques">Explore techniques</RouterLink>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <svg viewBox="0 0 420 300" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="spoke" x1="211" y1="156" x2="351" y2="45" gradientUnits="userSpaceOnUse"><stop stop-color="#76f2d1"/><stop offset="1" stop-color="#61d2bc" stop-opacity="0.1"/></linearGradient>
          <linearGradient id="sweep" x1="208" y1="157" x2="362" y2="115" gradientUnits="userSpaceOnUse"><stop stop-color="#52e7bc" stop-opacity="0.31"/><stop offset="1" stop-color="#4cbbab" stop-opacity="0.03"/></linearGradient>
          <radialGradient id="halo"><stop stop-color="#53dbb2" stop-opacity=".16"/><stop offset="1" stop-color="#389595" stop-opacity="0"/></radialGradient>
          <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#497079" opacity=".32"/></pattern>
        </defs>
        <path fill="url(#dots)" d="M8 2h405v294H8z"/>
        <circle cx="211" cy="150" r="144" fill="url(#halo)"/>
        <g stroke="currentColor" stroke-opacity=".55">
          <circle cx="211" cy="150" r="130" stroke-dasharray="1 5" stroke-width="2"/><circle cx="211" cy="150" r="111"/><circle cx="211" cy="150" r="84"/><circle cx="211" cy="150" r="56"/><circle cx="211" cy="150" r="27"/>
          <path d="M55 150h312M211 5v290M120 59l182 182M120 241 302 59" stroke-dasharray="3 6"/>
          <path d="M54 53V33h20m276 0h20v20m0 194v20h-20M74 267H54v-20"/>
        </g>
        <path d="m211 150 89-92c16 17 25 36 32 61L211 150Z" fill="url(#sweep)"/>
        <path d="m211 150 94-97" stroke="url(#spoke)" stroke-width="1.5"/>
        <path d="M194 150h34m-17-17v34" stroke="#4fd7b3" stroke-width="1.35"/>
        <circle cx="211" cy="150" r="6" stroke="#78f0cf"/><circle cx="211" cy="150" r="2" fill="#b0f8e6"/>
        <circle cx="282" cy="92" r="12" stroke="#4de5bd" opacity=".45"/><circle cx="282" cy="92" r="6" fill="#4dd1a9"/><circle cx="282" cy="92" r="2.5" fill="#ddfff4"/>
        <circle cx="160" cy="109" r="3" fill="#72acfb"/><circle cx="259" cy="196" r="4" fill="#85e7d2"/><circle cx="147" cy="203" r="3" fill="#b3a5ff"/><circle cx="295" cy="175" r="3" fill="#72acfb"/><circle cx="181" cy="234" r="2" fill="#7aafac"/>
        <path d="M294 92h44l12-13h31m-234 124h-41l-14 14H61m202-17 19 22h33" stroke="currentColor" stroke-width=".8"/>
        <path d="M381 76v6m-320 132v6m254-1v6" stroke="currentColor"/>
      </svg>
    </div>
  </section>

  <div class="stats-grid" aria-label="Lab overview">
    <div class="stat-card"><div class="stat-icon"><Layers3 :size="19" aria-hidden="true" /></div><span>Techniques</span><strong>{{ scenarios.length || '—' }}</strong></div>
    <div class="stat-card"><div class="stat-icon"><BookOpen :size="19" aria-hidden="true" /></div><span>Core guided hunts</span><strong>{{ scenarios.length ? guided : '—' }}</strong></div>
    <div class="stat-card"><div class="stat-icon"><FlaskConical :size="19" aria-hidden="true" /></div><span>Fixture checks</span><strong>{{ coverage ? `${coverage.metrics.passed}/${coverage.metrics.total}` : '—' }}</strong></div>
    <div class="stat-card"><div class="stat-icon"><Activity :size="19" aria-hidden="true" /></div><span>{{ showcase ? 'Sample alerts viewed' : 'Alerts in recent replays' }}</span><strong>{{ latest.length }}</strong></div>
  </div>

  <div class="overview-grid">
    <section class="panel">
      <div class="section-title"><div><h2>Your first guided hunt</h2><p>Learn to read a detection from start to finish.</p></div><Target :size="20" aria-hidden="true" /></div>
      <div v-if="first" class="featured-lesson">
        <div class="lesson-icon"><Fingerprint :size="23" aria-hidden="true" /></div>
        <div><div class="inline-meta"><span>{{ first.difficulty }}</span><span><Clock3 :size="13" aria-hidden="true" /> {{ first.minutes }} min</span></div>
          <h3>{{ first.title }}</h3><p>{{ first.hypothesis }}</p>
        </div>
        <RouterLink class="button text-button" :to="`/lesson/${first.id}`">Open lesson <ArrowRight :size="16" aria-hidden="true" /></RouterLink>
      </div>
      <p v-else class="muted">Loading the lesson catalog…</p>
    </section>
    <section class="panel">
      <div class="section-title"><div><h2>Recent activity</h2><p>{{ showcase ? 'Alerts you’ve opened in the showcase.' : 'Alerts from your local fixture replays.' }}</p></div><Activity :size="20" aria-hidden="true" /></div>
      <div v-if="!latest.length" class="empty compact"><div class="empty-icon"><Radar :size="24" aria-hidden="true" /></div><strong>No alerts yet</strong><p>{{ showcase ? 'Open an example in a guided lesson.' : 'Replay a fixture in a guided lesson to create your first alert.' }}</p></div>
      <div v-else class="list-stack">
        <RouterLink class="list-row" v-for="entry in latest.slice(0, 4)" :key="entry.alert.id" :to="`/investigations/${entry.id}`"><span>{{ entry.alert.title }}<small>{{ titleCase(entry.alert.severity) }} · {{ entry.alert.event_count }} evidence events</small></span><ArrowRight :size="16" aria-hidden="true" /></RouterLink>
      </div>
    </section>
  </div>

  <section v-if="domains.length" class="panel domains-panel">
    <div class="section-title"><div><h2>Explore by domain</h2><p>Find lessons by the type of activity you want to investigate.</p></div></div>
    <div class="domain-grid"><RouterLink v-for="domain in domains" :key="domain" class="domain-link" :to="{ path: '/techniques', query: { domain } }"><span>{{ domain }}</span><ArrowRight :size="15" aria-hidden="true" /></RouterLink></div>
  </section>
</template>
