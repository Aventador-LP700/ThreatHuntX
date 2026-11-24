<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ArrowRight, Copy } from 'lucide-vue-next'
import { ruleArtifact, scenarios, validationStatus } from '../api'
import type { Artifact, ArtifactKind } from '../types'
import PageHeading from '../components/PageHeading.vue'
import RuleTrial from '../components/RuleTrial.vue'

const props = defineProps<{ id?: string }>()
const scenario = computed(() => scenarios.value.find(item => item.id === props.id))
const kinds = { sigma: 'Sigma', wazuh: 'Wazuh XML', kql: 'KQL', spl: 'SPL' }
const selected = ref<ArtifactKind | 'local'>('local')
const artifact = ref<Artifact>()
const status = ref('')
const code = computed(() => selected.value === 'local' ? JSON.stringify(scenario.value?.rule, null, 2) : artifact.value?.code)
watch(() => props.id, () => { selected.value = 'local'; status.value = '' })
watch([() => props.id, selected], async ([id, kind], _, cleanup) => {
  let current = true
  cleanup(() => { current = false })
  artifact.value = undefined
  status.value = ''
  if (!id || kind === 'local') return
  try {
    const value = await ruleArtifact(id, kind)
    if (current) artifact.value = value
  } catch (err) {
    if (current) status.value = err instanceof Error ? err.message : 'The rule could not be opened.'
  }
})
async function copy() {
  if (!code.value) return
  try { await navigator.clipboard.writeText(code.value); status.value = 'Copied to clipboard.' }
  catch { status.value = 'Select the rule text to copy it manually.' }
}
</script>

<template>
  <PageHeading :title="scenario ? `${scenario.rule.id} · ${scenario.title}` : 'Detection Studio'" description="Inspect local detection logic, portable Sigma specifications, and vendor query templates." />
  <template v-if="scenario">
  <div class="lesson-grid">
    <section class="panel">
      <h2>Rule logic</h2><p>{{ scenario.hypothesis }}</p>
      <div class="actions rule-formats" aria-label="Rule format"><button class="button secondary" :aria-pressed="selected === 'local'" @click="selected = 'local'">Local rule</button><button v-for="kind in scenario.artifacts" :key="kind" class="button secondary" :aria-pressed="selected === kind" @click="selected = kind">{{ kinds[kind] }}</button></div>
      <p class="muted">{{ selected === 'local' ? validationStatus(scenario.id) : artifact?.status ?? (status || 'Loading rule…') }}</p>
      <pre v-if="code" tabindex="0" aria-label="Rule code"><code>{{ code }}</code></pre>
      <div class="actions"><button class="button secondary" :disabled="!code" @click="copy"><Copy :size="16" aria-hidden="true" /> Copy rule</button><span v-if="status" role="status">{{ status }}</span></div>
    </section>
    <aside class="panel lesson-aside"><h2>Tuning &amp; verification</h2><dl class="reading-list small"><div><dt>Expected evidence</dt><dd>{{ scenario.evidence }}</dd></div><div><dt>False positives</dt><dd>{{ scenario.false_positive }}</dd></div><div><dt>Rule tuning</dt><dd>{{ scenario.tuning }}</dd></div><div><dt>Validation</dt><dd>{{ scenario.validation }}</dd></div></dl><RouterLink class="button text-button" :to="`/lesson/${scenario.id}`">Open guided lesson <ArrowRight :size="16" aria-hidden="true" /></RouterLink></aside>
  </div>
    <RuleTrial :key="scenario.id" :id="scenario.id" />
  </template>
  <section v-else-if="!props.id" class="panel list-stack"><RouterLink v-for="entry in scenarios" :key="entry.id" class="list-row" :to="`/rules/${entry.id}`"><span>{{ entry.title }}<small>{{ entry.rule.id }} · {{ entry.rule.source }} · {{ validationStatus(entry.id) }}</small></span><ArrowRight :size="17" aria-hidden="true" /></RouterLink></section>
  <p v-else class="muted" role="status">{{ scenarios.length ? 'This rule does not exist.' : 'Loading rule…' }}</p>
</template>
