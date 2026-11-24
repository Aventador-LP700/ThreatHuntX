<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight, Download, ShieldAlert } from 'lucide-vue-next'
import { investigation, scenarios, showcase } from '../api'
import { download, titleCase } from '../learning'
import PageHeading from '../components/PageHeading.vue'
import Timeline from '../components/Timeline.vue'
import type { Run } from '../types'

const props = defineProps<{ id: string }>()
const run = ref<Run>()
const error = ref('')
const scenario = computed(() => scenarios.value.find(item => item.id === run.value?.scenario_id))
watch(() => props.id, async (id, _, onCleanup) => {
  let current = true
  onCleanup(() => { current = false })
  run.value = undefined
  error.value = ''
  try {
    const entry = await investigation(id)
    if (current) run.value = entry
  } catch (err) { if (current) error.value = err instanceof Error ? err.message : 'Investigation unavailable.' }
}, { immediate: true })
</script>

<template>
  <RouterLink class="back-link" to="/investigations"><ArrowLeft :size="16" aria-hidden="true" /> Investigations</RouterLink>
  <p v-if="error" class="error-box" role="alert">{{ error }}</p>
  <p v-else-if="!run" class="muted" role="status">Loading evidence…</p>
  <template v-else>
    <PageHeading :title="scenario?.title ?? 'Investigation'" :description="`${titleCase(run.mode)} ${showcase ? 'sample' : 'fixture'} · ${run.events.length} normalized events · ${run.alerts.length} alerts`">
      <button v-if="showcase" class="button secondary" @click="download(`threathuntx-${run!.id}.json`, { synthetic_only: true, ...run })"><Download :size="17" aria-hidden="true" /> Export JSON</button>
      <template v-else><a class="button secondary" :href="`/api/runs/${run.id}/export?format=json`"><Download :size="17" aria-hidden="true" /> JSON</a><a class="button secondary" :href="`/api/runs/${run.id}/export?format=csv`"><Download :size="17" aria-hidden="true" /> CSV</a></template>
    </PageHeading>
    <div class="lesson-grid">
      <section class="panel"><div class="section-title"><div><h2>Evidence timeline</h2><p>Expand each event to inspect its normalized fields.</p></div></div><Timeline :events="run.events" /></section>
      <aside class="panel lesson-aside">
        <div class="section-title"><h2>Alert assessment</h2><ShieldAlert :size="20" aria-hidden="true" /></div>
        <div v-if="!run.alerts.length" class="muted">No alert for this fixture.</div>
        <dl v-for="alert in run.alerts" :key="alert.id" class="reading-list small"><div><dt>{{ titleCase(alert.severity) }} severity · {{ alert.rule_id }}</dt><dd>{{ alert.event_count }} evidence events for <code>{{ alert.group }}</code>.</dd></div><div v-if="scenario"><dt>What to verify</dt><dd>{{ scenario.evidence }}</dd></div><div v-if="scenario"><dt>Next action</dt><dd>{{ scenario.response }}</dd></div></dl>
        <RouterLink v-if="scenario" class="button text-button" :to="`/lesson/${scenario.id}`">Return to lesson <ArrowRight :size="16" aria-hidden="true" /></RouterLink>
      </aside>
    </div>
  </template>
</template>
