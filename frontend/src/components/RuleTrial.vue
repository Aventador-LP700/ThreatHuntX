<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { FlaskConical } from 'lucide-vue-next'
import { detectionTrial, showcase } from '../api'
import type { TrialResult, TrialSettings } from '../types'

const props = defineProps<{ id: string }>()
const result = ref<TrialResult>()
const settings = ref<TrialSettings>()
const error = ref('')
const busy = ref(false)
let active = true
const labels = { positive: 'Positive fixture', baseline: 'Clean baseline', negative: 'Noisy control' }
const counts = { tp: 'True positives', fp: 'False positives', fn: 'False negatives', tn: 'True negatives' }
const ratio = (value: number | null) => value === null ? 'Unavailable' : new Intl.NumberFormat('en', { style: 'percent', maximumFractionDigits: 0 }).format(value)
async function compare(trial?: TrialSettings) {
  busy.value = true
  error.value = ''
  try {
    const response = await detectionTrial(props.id, trial)
    if (!active) return
    result.value = response
    settings.value = { ...response.settings }
  } catch (err) {
    if (active) error.value = err instanceof Error ? err.message : 'The comparison could not be evaluated.'
  } finally {
    if (active) busy.value = false
  }
}
onMounted(() => void compare())
onBeforeUnmount(() => { active = false })
</script>

<template>
  <section class="panel studio-panel" aria-labelledby="fixture-trial-title">
    <div class="section-title"><div><h2 id="fixture-trial-title">Fixture comparison</h2><p>{{ showcase ? 'These results were generated from bundled synthetic samples. Use the local lab to try different settings.' : 'Try a temporary version of the rule on the three bundled synthetic batches. The published rule and replay history stay intact.' }}</p></div><FlaskConical :size="21" aria-hidden="true" /></div>
    <form v-if="!showcase && settings" class="filters-grid trial-form" @submit.prevent="compare(settings)">
      <label class="field">Threshold<input v-model.number="settings.threshold" type="number" min="1" max="30" required /></label>
      <label class="field">Window (seconds)<input v-model.number="settings.window_seconds" type="number" min="1" max="86400" required /></label>
      <label class="field">Group by<select v-model="settings.group_by"><option v-for="group in result?.group_options" :key="group" :value="group">{{ group }}</option></select></label>
      <div class="actions"><button class="button primary" :disabled="busy" type="submit">Compare fixtures</button><button class="button secondary" :disabled="busy" type="button" @click="compare()">Reset trial</button></div>
    </form>
    <p v-if="error" class="error-box" role="alert">{{ error }}</p>
    <p v-if="busy" role="status">Evaluating fixture batches…</p>
    <div v-if="result" aria-live="polite">
      <p class="trial-applied">Evaluated {{ result.settings.threshold }} {{ result.settings.threshold === 1 ? 'observation' : 'observations' }} per <code>{{ result.settings.group_by }}</code> within {{ result.settings.window_seconds }} seconds.</p>
      <div class="trial-cases" aria-label="Synthetic fixture decisions">
        <article v-for="entry in result.cases" :key="entry.mode" :class="['trial-card', { mismatch: !entry.passed }]">
          <h3>{{ labels[entry.mode] }}</h3>
          <p>{{ entry.event_count }} events · expected {{ entry.expected ? 'alert' : 'no alert' }}</p>
          <strong>{{ entry.alerts }} {{ entry.alerts === 1 ? 'alert' : 'alerts' }} observed</strong>
          <ul v-if="entry.matched_records.length" aria-label="Matched record IDs"><li v-for="id in entry.matched_records" :key="id"><code>{{ id }}</code></li></ul>
        </article>
      </div>
      <dl class="matrix-stats">
        <div v-for="(label, key) in counts" :key="key"><dt>{{ label }}</dt><dd>{{ result.metrics[key] }}</dd></div>
        <div><dt>Fixture precision</dt><dd>{{ ratio(result.metrics.precision) }}</dd></div><div><dt>Fixture recall</dt><dd>{{ ratio(result.metrics.recall) }}</dd></div>
      </dl>
      <p v-if="result.metrics.fn">The positive batch fell below the trial threshold. Try a larger window, a lower threshold, or a grouping field that keeps related records together.</p>
      <p v-if="result.metrics.fp">A control batch triggered an alert. Check the matched records and try a higher threshold or a grouping field that separates benign activity.</p>
      <p class="muted">These measurements describe the three labeled fixture batches. Validate new settings with representative telemetry before production use.</p>
    </div>
  </section>
</template>
