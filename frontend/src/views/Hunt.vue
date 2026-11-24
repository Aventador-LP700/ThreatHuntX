<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import PageHeading from '../components/PageHeading.vue'
import EvidenceFilters from '../components/EvidenceFilters.vue'
import Timeline from '../components/Timeline.vue'
import { runs, scenarios, showcase } from '../api'
import { blankFilter, filterEvidence } from '../cases'
import type { PivotField } from '../cases'
import { titleCase } from '../learning'
import hunts from '../content/hunts.json'

const filter = ref(blankFilter())
const chosen = ref('')
const subset = computed(() => chosen.value ? runs.value.filter(run => run.id === chosen.value) : runs.value)
const events = computed(() => subset.value.flatMap(run => run.events))
const grouped = computed(() => subset.value.flatMap(run => {
  const visible = filterEvidence(run.events, filter.value)
  return visible.length ? [{ id: run.id, name: scenarios.value.find(s => s.id === run.scenario_id)?.title ?? run.scenario_id, mode: run.mode, events: visible }] : []
}))
const hypotheses = computed(() => hunts.flatMap(hunt => {
  const lesson = scenarios.value.find(item => item.id === hunt.id)
  return lesson ? [{ ...hunt, lesson }] : []
}))
watch(chosen, () => { filter.value = blankFilter() })
function pivot(field: PivotField, value: string) {
  filter.value = { ...blankFilter(), [field]: value }
}
</script>

<template>
  <PageHeading title="Investigation Workspace" :description="showcase ? 'Search the synthetic samples you opened.' : 'Filter normalized evidence across the most recent 50 fixture replays.'" />
  <section class="panel search-panel">
    <label class="field">Case<select v-model="chosen"><option value="">All recent cases</option><option v-for="run in runs" :key="run.id" :value="run.id">{{ scenarios.find(s => s.id === run.scenario_id)?.title }} · {{ titleCase(run.mode) }} · {{ run.id.slice(-6) }}</option></select></label>
    <EvidenceFilters v-model="filter" :events="events" />
    <div class="actions evidence-summary"><p role="status">{{ grouped.reduce((count, group) => count + group.events.length, 0) }} matching events</p><button class="button secondary" type="button" @click="filter = blankFilter()">Clear filters</button></div>
    <p v-if="!runs.length">Replay a fixture in <RouterLink to="/simulate">Guided Hunt</RouterLink> to populate the workspace.</p>
  </section>
  <section v-for="group in grouped" :key="group.id" class="panel matrix-panel"><h2><RouterLink :to="`/investigations/${group.id}`">{{ group.name }}</RouterLink> · {{ titleCase(group.mode) }}</h2><Timeline :events="group.events" pivots @pivot="pivot" /></section>
  <section class="panel matrix-panel">
    <h2>Hunt hypotheses</h2><p>Start with a hypothesis, find supporting records, and compare them with benign explanations.</p>
    <div class="list-stack hunt-list"><details v-for="entry in hypotheses" :key="entry.id" class="list-row"><summary>{{ entry.lesson.title }}</summary><p>{{ entry.lesson.hypothesis }}</p><dl class="reading-list small"><div><dt>Pivot</dt><dd>{{ entry.pivot }}</dd></div><div><dt>Check the alternative</dt><dd>{{ entry.check }}</dd></div></dl><RouterLink class="button secondary" :to="`/lesson/${entry.id}`">Open guided lesson</RouterLink></details></div>
  </section>
</template>
