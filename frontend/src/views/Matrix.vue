<script setup lang="ts">
import { computed } from 'vue'
import { Download, ExternalLink } from 'lucide-vue-next'
import PageHeading from '../components/PageHeading.vue'
import { catalog, coverage, scenarios, validationStatus, showcase } from '../api'
import { download } from '../learning'

const groups = computed(() => (catalog.value?.attack.tactics ?? []).map(tactic => ({
  ...tactic, lessons: scenarios.value.filter(scenario => scenario.attack.tactics.includes(tactic.id)),
})))
const metrics = computed(() => coverage.value?.metrics)
const labels = { tp: 'True positives', fp: 'False positives', tn: 'True negatives', fn: 'False negatives' }
const percent = (value: number | null) => value === null ? 'Unavailable' : new Intl.NumberFormat('en', { style: 'percent', maximumFractionDigits: 1 }).format(value)
</script>

<template>
  <PageHeading title="ATT&CK Matrix" :description="`Enterprise ${catalog?.attack.version ?? 'ATT&CK'} mappings and fixture validation.`">
    <button v-if="coverage" class="button secondary" @click="download('threathuntx-fixture-results.json', coverage)"><Download :size="16" aria-hidden="true" /> Export fixture results</button>
  </PageHeading>
  <section v-if="metrics" class="panel matrix-metrics">
    <div class="section-title"><div><h2>Synthetic fixture checks</h2><p>{{ metrics.passed }} of {{ metrics.total }} batches matched expectations. These measurements describe the bundled fixture set.</p></div></div>
    <dl class="matrix-stats"><div v-for="(label, key) in labels" :key="key"><dt>{{ label }}</dt><dd>{{ metrics[key] }}</dd></div><div><dt>Precision</dt><dd>{{ percent(metrics.precision) }}</dd></div><div><dt>Recall</dt><dd>{{ percent(metrics.recall) }}</dd></div><div><dt>Batch pass rate</dt><dd>{{ percent(metrics.pass_rate) }}</dd></div></dl>
  </section>
  <section v-if="groups.length" class="panel matrix-panel">
    <div class="section-title"><div><h2>Tactic coverage</h2><p>Each cell links to a lesson. A mapping may be direct or contextual.</p></div><a v-if="catalog" :href="catalog.attack.source" aria-label="Open pinned MITRE data" target="_blank" rel="noopener noreferrer"><ExternalLink :size="17" aria-hidden="true" /></a></div>
    <div class="matrix-grid"><div v-for="group in groups" :key="group.id" class="matrix-column"><h3>{{ group.name }} <span>{{ group.lessons.length }}</span></h3><p v-if="!group.lessons.length" class="muted">No mapped lesson</p><RouterLink v-for="lesson in group.lessons" :key="lesson.id" :class="['matrix-cell', { verified: validationStatus(lesson.id) === 'Synthetic-verified' }]" :to="`/lesson/${lesson.id}`"><strong>{{ lesson.attack.id }}</strong><span>{{ lesson.title }}</span><small>{{ validationStatus(lesson.id) }}</small></RouterLink></div></div>
  </section>
  <section class="panel matrix-panel"><h2>Coverage gaps</h2><p>Live detector and sensor verification is outside the scope of this {{ showcase ? 'read-only showcase' : 'synthetic lab' }}. Tactics without a mapped lesson and related mappings are visible above. A fixture result applies to the behavior described in its lesson.</p></section>
</template>
