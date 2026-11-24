<script setup lang="ts">
import { computed, ref } from 'vue'
import { Search } from 'lucide-vue-next'
import PageHeading from '../components/PageHeading.vue'
import Timeline from '../components/Timeline.vue'
import { runs, scenarios, showcase } from '../api'
import { titleCase } from '../learning'

const source = ref('')
const result = ref('')
const text = ref('')
const chosen = ref('')
const fixtures = computed(() => runs.value.flatMap(run => run.events.map(event => ({ event, runId: run.id }))))
const sources = computed(() => [...new Set(fixtures.value.map(entry => entry.event.source))].sort())
const outcomes = computed(() => [...new Set(fixtures.value.map(entry => entry.event.outcome))].sort())
const found = computed(() => {
  const query = text.value.trim().toLowerCase()
  return fixtures.value.filter(({ event, runId }) => (!chosen.value || runId === chosen.value) && (!source.value || source.value === event.source) && (!result.value || result.value === event.outcome) && (!query || [event.user, event.host, event.action, event.domain, ...Object.values(event.observables)].join(' ').toLowerCase().includes(query)))
})
const grouped = computed(() => runs.value.flatMap(run => {
  const events = found.value.filter(item => item.runId === run.id).map(item => item.event)
  return events.length ? [{ id: run.id, name: scenarios.value.find(s => s.id === run.scenario_id)?.title ?? run.scenario_id, mode: run.mode, events }] : []
}))
const hypotheses = computed(() => scenarios.value.filter(scenario => scenario.core_lesson))
</script>

<template>
  <PageHeading title="Hunt Workspace" :description="showcase ? 'Search the synthetic samples you opened.' : 'Filter normalized evidence across the most recent 50 fixture replays.'" />
  <section class="panel search-panel"><label class="search-field"><Search :size="18" aria-hidden="true" /><span class="sr-only">Search event fields</span><input v-model="text" type="search" placeholder="Search by actor, action, host, domain, or observable" /></label><div class="filters-grid"><label class="field">Source<select v-model="source"><option value="">All sources</option><option v-for="item in sources" :key="item" :value="item">{{ titleCase(item) }}</option></select></label><label class="field">Outcome<select v-model="result"><option value="">All outcomes</option><option v-for="item in outcomes" :key="item" :value="item">{{ titleCase(item) }}</option></select></label><label class="field">Replay batch<select v-model="chosen"><option value="">All batches</option><option v-for="run in runs" :key="run.id" :value="run.id">{{ scenarios.find(s => s.id === run.scenario_id)?.title }} · {{ titleCase(run.mode) }} · {{ run.id.slice(-6) }}</option></select></label></div><p role="status">{{ found.length }} matching events</p></section>
  <section v-for="group in grouped" :key="group.id" class="panel matrix-panel"><h2><RouterLink :to="`/investigations/${group.id}`">{{ group.name }}</RouterLink> · {{ titleCase(group.mode) }}</h2><Timeline :events="group.events" /></section>
  <section class="panel matrix-panel"><h2>Starter hypotheses</h2><p>Pick a hypothesis, replay the source fixture, and compare the behavior with the noisy control.</p><div class="list-stack"><RouterLink v-for="entry in hypotheses" :key="entry.id" class="list-row" :to="`/lesson/${entry.id}`"><span>{{ entry.title }}<small>{{ entry.hypothesis }}</small></span></RouterLink></div></section>
</template>
