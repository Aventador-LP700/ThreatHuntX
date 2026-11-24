<script setup lang="ts">
import { Printer } from 'lucide-vue-next'
import { dispositions } from '../cases'
import type { CaseReport } from '../cases'

const props = defineProps<{ report: CaseReport }>()
const print = () => window.print()
</script>

<template>
  <article class="panel printable-case">
    <div class="section-title"><div><h1>Case report</h1><p>Synthetic evidence · {{ props.report.scenario.title }}</p></div><button class="button primary print-action" @click="print"><Printer :size="17" aria-hidden="true" /> Print report</button></div>
    <dl class="reading-list">
      <div><dt>Case ID</dt><dd><code>{{ report.case_id }}</code></dd></div>
      <div><dt>Fixture, rule and ATT&amp;CK</dt><dd>{{ report.fixture_mode }} · {{ report.rule_id }} · {{ report.scenario.attack.id }}</dd></div>
      <div><dt>Replay recorded at (UTC)</dt><dd>{{ report.recorded_at }}</dd></div>
      <div><dt>Report generated at (UTC)</dt><dd>{{ report.generated_at }}</dd></div>
      <div><dt>Hypothesis</dt><dd>{{ report.analysis.hypothesis }}</dd></div>
      <div><dt>Triage decision</dt><dd>{{ dispositions[report.analysis.disposition] }}</dd></div>
      <div><dt>Analyst notes</dt><dd class="multiline-text">{{ report.analysis.notes || 'No notes recorded.' }}</dd></div>
      <div><dt>Response decision</dt><dd class="multiline-text">{{ report.analysis.response || 'No response recorded.' }}</dd></div>
      <div><dt>Limitations</dt><dd>{{ report.limitations }}</dd></div>
      <div><dt>Suggested mitigation</dt><dd><ul><li v-for="step in report.mitigations" :key="step">{{ step }}</li></ul></dd></div>
    </dl>
    <h2>Evidence</h2>
    <div class="table-scroll"><table><caption>Evidence records in UTC</caption><thead><tr><th scope="col">Timestamp</th><th scope="col">Record</th><th scope="col">Source and outcome</th><th scope="col">Matched alert</th></tr></thead><tbody><tr v-for="event in report.evidence" :key="event.record_id"><td>{{ event.event_timestamp }}</td><td><code>{{ event.evidence_reference }}</code></td><td>{{ event.source }} / {{ event.outcome }}</td><td>{{ event.alert_id ?? '—' }}</td></tr></tbody></table></div>
  </article>
</template>
