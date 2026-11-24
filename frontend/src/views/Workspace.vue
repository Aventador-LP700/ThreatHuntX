<script setup lang="ts">
import { computed, ref } from 'vue'
import { ArrowRight, Download, Play } from 'lucide-vue-next'
import { replay, runs, scenarios, showcase } from '../api'
import { download, learningReport, titleCase } from '../learning'
import PageHeading from '../components/PageHeading.vue'
import Matrix from './Matrix.vue'
import Hunt from './Hunt.vue'
import Rules from './Rules.vue'
import Resources from './Resources.vue'
import type { ReplayMode } from '../types'

const props = defineProps<{ page: string; id?: string }>()
const selected = ref('02')
const mode = ref<ReplayMode>('positive')
const running = ref(false)
const error = ref('')
const replayed = ref('')
const report = computed(() => learningReport(scenarios.value))
const recentAlerts = computed(() => runs.value.flatMap(run => run.alerts.map(alert => ({ run, alert }))))
async function simulate() {
  error.value = ''
  replayed.value = ''
  running.value = true
  try { replayed.value = (await replay(selected.value, mode.value)).id }
  catch (err) { error.value = err instanceof Error ? err.message : 'Replay failed.' }
  finally { running.value = false }
}
</script>

<template>
  <template v-if="page === 'progress'">
    <PageHeading title="Learning progress" description="Your completed lessons are stored in this browser."><button class="button primary" @click="download('threathuntx-learning-report.json', report)"><Download :size="16" aria-hidden="true" /> Export learning report</button></PageHeading>
    <section class="panel"><h2>{{ report.completed.length }} of {{ scenarios.length }} lessons completed</h2><p v-if="!report.completed.length" class="muted">Complete a lesson to build your report.</p><ul v-else><li v-for="entry in report.completed" :key="entry.id"><RouterLink :to="`/lesson/${entry.id}`">{{ entry.title }}</RouterLink> · {{ entry.attack }}</li></ul><RouterLink class="button secondary" to="/learn">Browse learning tracks <ArrowRight :size="16" aria-hidden="true" /></RouterLink></section>
  </template>
  <template v-else-if="page === 'simulate'">
    <PageHeading title="Simulate" :description="showcase ? 'View a prerecorded synthetic sample.' : 'Ingest a bundled synthetic fixture and apply the local detection rule.'" />
    <section class="panel"><form class="filters-grid" @submit.prevent="simulate"><label class="field">Technique<select v-model="selected"><option v-for="entry in scenarios" :key="entry.id" :value="entry.id">{{ entry.title }}</option></select></label><label class="field">Fixture<select v-model="mode"><option value="positive">Positive signal</option><option value="negative">Noisy / negative</option></select></label><button class="button primary" :disabled="running || !scenarios.length"><Play :size="16" aria-hidden="true" /> {{ showcase ? 'View sample' : 'Replay safe events' }}</button></form><p v-if="error" class="error-box" role="alert">{{ error }}</p><p v-if="replayed" role="status"><RouterLink :to="`/investigations/${replayed}`">Open evidence timeline</RouterLink></p></section>
  </template>
  <template v-else-if="page === 'alerts' || page === 'investigations'">
    <PageHeading :title="titleCase(page)" :description="page === 'alerts' ? 'Review evidence linked to recent synthetic alerts.' : 'Explore the event timeline from recent fixture batches.'" />
    <section class="panel list-stack" v-if="page === 'alerts' && recentAlerts.length"><RouterLink v-for="item in recentAlerts" :key="item.alert.id" class="list-row" :to="`/investigations/${item.run.id}`"><span>{{ item.alert.title }}<small>{{ titleCase(item.alert.severity) }} · {{ item.alert.event_count }} evidence events</small></span><ArrowRight :size="17" aria-hidden="true" /></RouterLink></section>
    <section class="panel list-stack" v-else-if="page === 'investigations' && runs.length"><RouterLink v-for="run in runs" :key="run.id" class="list-row" :to="`/investigations/${run.id}`"><span>{{ scenarios.find(s => s.id === run.scenario_id)?.title ?? run.scenario_id }}<small>{{ titleCase(run.mode) }} · {{ run.events.length }} events · {{ run.alerts.length }} alerts</small></span><ArrowRight :size="17" aria-hidden="true" /></RouterLink></section>
    <section v-else class="panel empty"><h2>No {{ page }} yet</h2><p>Run a lesson or a fixture to populate this view.</p><RouterLink class="button primary" to="/simulate">Open Simulate</RouterLink></section>
  </template>
  <Rules v-else-if="page === 'rules'" :id="props.id" />
  <Matrix v-else-if="page === 'matrix'" />
  <Hunt v-else-if="page === 'hunt'" />
  <Resources v-else :page="page" />
</template>
