<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowRight, BookOpen, CheckCircle2, Clock3, Search } from 'lucide-vue-next'
import { scenarios, validationStatus } from '../api'
import { curricula, progress, titleCase, tracks } from '../learning'
import type { ArtifactKind } from '../types'
import PageHeading from '../components/PageHeading.vue'

const props = defineProps<{ learning: boolean }>()
const route = useRoute()
const search = ref('')
const track = ref('')
const platform = ref('')
const domain = ref('')
const tactic = ref('')
const source = ref('')
const status = ref('')
const language = ref('')
const data = ref('')
const curriculum = ref('')
watch(() => [route.path, route.query.domain], () => {
  search.value = track.value = platform.value = tactic.value = source.value = status.value = language.value = data.value = curriculum.value = ''
  domain.value = typeof route.query.domain === 'string' ? route.query.domain : ''
}, { immediate: true })
const all = computed(() => {
  const selected = curricula.find(c => c.name === curriculum.value)
  const words = search.value.trim().toLowerCase()
  return scenarios.value.filter(s =>
    (!selected || selected.ids.includes(s.id)) && (!track.value || track.value === s.difficulty) &&
    (!platform.value || platform.value === s.platform) && (!domain.value || domain.value === s.category) &&
    (!tactic.value || s.attack.tactics.includes(tactic.value)) && (!source.value || source.value === s.rule.source) &&
    (!status.value || status.value === validationStatus(s.id)) &&
    (!language.value || language.value === 'Local rule' || s.artifacts.includes(language.value.toLowerCase() as ArtifactKind)) &&
    (!data.value || data.value === 'Synthetic replay') &&
    (!words || `${s.title} ${s.overview} ${s.attack.id} ${s.category}`.toLowerCase().includes(words)))
})
const facets = computed(() => [
  { label: 'Platform', selected: platform, values: [...new Set(scenarios.value.map(s => s.platform))].sort() },
  { label: 'Domain', selected: domain, values: [...new Set(scenarios.value.map(s => s.category))] },
  { label: 'ATT&CK tactic', selected: tactic, values: [...new Set(scenarios.value.flatMap(s => s.attack.tactics))].sort() },
  { label: 'Telemetry', selected: source, values: [...new Set(scenarios.value.map(s => s.rule.source))].sort() },
  { label: 'Detection language', selected: language, values: ['Local rule', 'Sigma', 'Wazuh', 'KQL', 'SPL'] },
  { label: 'Status', selected: status, values: ['Synthetic-verified', 'Fixture checks failed', 'Documented'] },
  { label: 'Validation scope', selected: data, values: ['Synthetic replay', 'Live validated'] },
])
</script>

<template>
  <PageHeading :title="props.learning ? 'Learning tracks' : 'Technique Explorer'" :description="props.learning ? 'Choose a track and investigate a technique at your own pace.' : 'Browse defensive hypotheses, evidence sources, and ATT&CK mappings.'" />
  <section class="panel search-panel" aria-label="Filter techniques">
    <label class="search-field"><Search :size="18" aria-hidden="true" /><span class="sr-only">Search techniques</span><input v-model="search" type="search" placeholder="Search by technique, keyword, or ATT&CK ID" /></label>
    <div class="actions track-buttons" aria-label="Difficulty track"><button v-for="level in ['', ...tracks]" :key="level" class="button secondary" :aria-pressed="track === level" @click="track = level">{{ level || 'All levels' }}</button></div>
    <label v-if="props.learning" class="field">Role-based curriculum <select v-model="curriculum"><option value="">All curricula</option><option v-for="entry in curricula" :key="entry.name">{{ entry.name }}</option></select></label>
    <p v-if="curriculum" class="muted">{{ curricula.find(entry => entry.name === curriculum)?.description }}</p>
    <details v-if="!props.learning" class="filter-details"><summary>More filters</summary><div class="filters-grid"><label v-for="facet in facets" :key="facet.label" class="field">{{ facet.label }}<select v-model="facet.selected.value"><option value="">All</option><option v-for="value in facet.values" :key="value" :value="value">{{ ['KQL', 'SPL', 'AD', 'CI/CD', 'SaaS'].includes(value) ? value : titleCase(value) }}</option></select></label></div></details>
  </section>
  <p class="results-count" role="status">{{ all.length }} {{ all.length === 1 ? 'technique' : 'techniques' }}</p>
  <div class="cards-grid">
    <RouterLink v-for="scenario in all" :key="scenario.id" class="panel technique-card" :to="`/lesson/${scenario.id}`"><div class="card-top"><span class="lesson-icon"><BookOpen :size="19" aria-hidden="true" /></span><span class="tag">{{ scenario.attack.id }}</span></div><h2>{{ scenario.title }}</h2><p>{{ scenario.overview }}</p><div class="inline-meta"><span>{{ scenario.difficulty }}</span><span><Clock3 :size="13" aria-hidden="true" /> {{ scenario.minutes }} min</span></div><div class="card-footer"><span><CheckCircle2 v-if="progress[scenario.id]" :size="15" aria-hidden="true" /> {{ progress[scenario.id] ? 'Completed' : validationStatus(scenario.id) }}</span><ArrowRight :size="18" aria-hidden="true" /></div></RouterLink>
  </div>
  <p v-if="!all.length && scenarios.length" class="empty">No techniques match these filters.</p>
</template>
