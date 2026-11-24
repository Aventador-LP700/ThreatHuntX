<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight, Download, ShieldAlert } from 'lucide-vue-next'
import { investigation, scenarios, showcase } from '../api'
import { blankFilter, caseCsv, caseReport, dispositions, filterEvidence, readAnalysis, saveAnalysis } from '../cases'
import type { PivotField } from '../cases'
import { download, downloadText, titleCase } from '../learning'
import PageHeading from '../components/PageHeading.vue'
import PrintableCase from '../components/PrintableCase.vue'
import EvidenceFilters from '../components/EvidenceFilters.vue'
import Timeline from '../components/Timeline.vue'
import type { Run } from '../types'

const props = defineProps<{ id: string; printable?: boolean }>()
const run = ref<Run>()
const error = ref('')
const filters = ref(blankFilter())
const analysis = ref(readAnalysis(props.id))
const saveMessage = ref('')
const scenario = computed(() => scenarios.value.find(item => item.id === run.value?.scenario_id))
const visibleEvents = computed(() => filterEvidence(run.value?.events ?? [], filters.value))
const printReport = computed(() => run.value && scenario.value ? caseReport(run.value, scenario.value, analysis.value) : undefined)

watch(() => props.id, async (id, _, onCleanup) => {
  let current = true
  onCleanup(() => { current = false })
  run.value = undefined
  error.value = ''
  saveMessage.value = ''
  filters.value = blankFilter()
  analysis.value = readAnalysis(id)
  try {
    const entry = await investigation(id)
    if (current) run.value = entry
  } catch (err) { if (current) error.value = err instanceof Error ? err.message : 'Investigation unavailable.' }
}, { immediate: true })

function persist() {
  analysis.value.updated_at = new Date().toISOString()
  saveMessage.value = saveAnalysis(props.id, analysis.value)
    ? 'Case analysis saved in this browser.'
    : 'Case analysis saved for this session.'
}
function pivot(field: PivotField, value: string) {
  filters.value = { ...blankFilter(), [field]: value }
}
function exportCase(format: 'json' | 'csv') {
  if (!run.value || !scenario.value) return
  const report = caseReport(run.value, scenario.value, analysis.value)
  const name = `threathuntx-case-${run.value.id}`
  if (format === 'json') download(`${name}.json`, report)
  else downloadText(`${name}.csv`, caseCsv(report), 'text/csv;charset=utf-8')
}
</script>

<template>
  <RouterLink v-if="printable" class="back-link print-action" :to="`/investigations/${id}`"><ArrowLeft :size="16" aria-hidden="true" /> Back to evidence</RouterLink>
  <RouterLink v-else class="back-link" to="/investigations"><ArrowLeft :size="16" aria-hidden="true" /> Investigations</RouterLink>
  <p v-if="error" class="error-box" role="alert">{{ error }}</p>
  <p v-else-if="!run" class="muted" role="status">Loading evidence…</p>
  <template v-else-if="printable">
    <PrintableCase v-if="printReport" :report="printReport" />
    <p v-else role="status">Loading the scenario details…</p>
  </template>
  <template v-else>
    <PageHeading :title="scenario?.title ?? 'Investigation'" :description="`${titleCase(run.mode)} synthetic ${showcase ? 'sample' : 'fixture'} · ${run.events.length} normalized events · ${run.alerts.length} alerts`">
      <button v-if="showcase" class="button secondary" @click="download(`threathuntx-${run!.id}.json`, { synthetic_only: true, ...run })"><Download :size="17" aria-hidden="true" /> Raw JSON</button>
      <template v-else><a class="button secondary" :href="`/api/runs/${run.id}/export?format=json`"><Download :size="17" aria-hidden="true" /> Raw JSON</a><a class="button secondary" :href="`/api/runs/${run.id}/export?format=csv`"><Download :size="17" aria-hidden="true" /> Raw CSV</a></template>
    </PageHeading>
    <div class="lesson-grid">
      <section class="panel">
        <div class="section-title"><div><h2>Evidence timeline</h2><p>Expand an event to inspect its normalized fields and find related records.</p></div></div>
        <EvidenceFilters v-model="filters" :events="run.events" />
        <div class="actions evidence-summary"><p role="status">{{ visibleEvents.length }} of {{ run.events.length }} events shown</p><button class="button secondary" type="button" @click="filters = blankFilter()">Clear filters</button></div>
        <Timeline v-if="visibleEvents.length" :events="visibleEvents" pivots @pivot="pivot" />
      </section>
      <aside class="panel lesson-aside">
        <div class="section-title"><h2>Alert assessment</h2><ShieldAlert :size="20" aria-hidden="true" /></div>
        <dl class="reading-list small"><div><dt>Case ID</dt><dd><code>{{ run.id }}</code></dd></div><div><dt>Fixture recorded at (UTC)</dt><dd>{{ run.created_at }}</dd></div></dl>
        <div v-if="!run.alerts.length" class="muted">No alert for this fixture.</div>
        <dl v-for="alert in run.alerts" :key="alert.id" class="reading-list small"><div><dt>{{ titleCase(alert.severity) }} severity · {{ alert.rule_id }}</dt><dd>{{ alert.event_count }} evidence events for <code>{{ alert.group }}</code>.</dd></div><div v-if="scenario"><dt>What to verify</dt><dd>{{ scenario.evidence }}</dd></div><div v-if="scenario"><dt>Next action</dt><dd>{{ scenario.response }}</dd></div></dl>
        <RouterLink v-if="scenario" class="button text-button" :to="`/lesson/${scenario.id}`">Return to lesson <ArrowRight :size="16" aria-hidden="true" /></RouterLink>
      </aside>
    </div>
    <section v-if="scenario" class="panel studio-panel" aria-labelledby="analysis-heading">
      <div class="section-title"><div><h2 id="analysis-heading">Case analysis</h2><p>Record your conclusion using synthetic evidence. Saved notes stay in this browser.</p></div></div>
      <form class="case-form" @submit.prevent="persist" @input="saveMessage = ''">
        <label class="field">Working hypothesis<textarea v-model="analysis.hypothesis" :placeholder="scenario.hypothesis" maxlength="700" rows="2" /></label>
        <label class="field">Triage decision<select v-model="analysis.disposition"><option v-for="(label, value) in dispositions" :key="value" :value="value">{{ label }}</option></select></label>
        <label class="field">Analyst notes<textarea v-model="analysis.notes" maxlength="4000" rows="4" /></label>
        <label class="field">Response decision<textarea v-model="analysis.response" maxlength="1500" rows="4" /></label>
        <div class="actions case-actions"><button class="button primary" type="submit">Save case analysis</button><button class="button secondary" type="button" @click="exportCase('json')">Case JSON</button><button class="button secondary" type="button" @click="exportCase('csv')">Case CSV</button><RouterLink class="button secondary" :to="`/investigations/${run.id}/report`">Printable report</RouterLink><span v-if="saveMessage" role="status">{{ saveMessage }}</span></div>
      </form>
    </section>
  </template>
</template>
