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
      <h1 id="hero-title">Learn threat hunting.<br /><span>Follow the evidence.</span></h1>
      <p v-if="showcase">Explore a real lesson through read-only examples from the Community Lab. All events and alerts shown here use synthetic sample data.</p>
      <p v-else>Investigate realistic security signals, test detection rules, and build analyst skills in a local lab that runs on synthetic data.</p>
      <div class="actions">
        <RouterLink class="button primary" to="/lesson/02"><BookOpen :size="17" aria-hidden="true" /> Start Learning <ArrowRight :size="17" aria-hidden="true" /></RouterLink>
        <RouterLink class="button secondary" to="/techniques">Explore techniques</RouterLink>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <img src="../assets/radar.webp" alt="" width="420" height="300" />
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
