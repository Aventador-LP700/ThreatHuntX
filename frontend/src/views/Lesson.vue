<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight, BookOpen, Check, ChevronRight, Clock3, ExternalLink, FlaskConical, ListChecks, Play, ShieldCheck } from 'lucide-vue-next'
import { catalog, lesson, replay, showcase, validationStatus } from '../api'
import { complete, progress } from '../learning'
import Timeline from '../components/Timeline.vue'
import type { LessonData, ReplayMode, Run } from '../types'

const props = defineProps<{ id: string }>()
const data = ref<LessonData>()
const scenario = computed(() => data.value?.scenario)
const step = ref(0)
const steps = ['Overview', 'Clean baseline', 'Replay & evidence', 'Response', 'Knowledge check']
const positive = ref<Run>()
const negative = ref<Run>()
const error = ref('')
const replayError = ref('')
const busy = ref<ReplayMode>()
const answers = ref<Record<number, number>>({})
const scored = ref(false)
const stepTitle = ref<HTMLElement>()
const score = computed(() => scenario.value?.questions.filter((question, index) => answers.value[index] === question.answer).length ?? 0)

watch(() => props.id, async (id, _, onCleanup) => {
  let current = true
  onCleanup(() => { current = false })
  data.value = undefined
  step.value = 0
  error.value = ''
  replayError.value = ''
  positive.value = undefined
  negative.value = undefined
  answers.value = {}
  scored.value = false
  busy.value = undefined
  try {
    const loaded = await lesson(id)
    if (current) data.value = loaded
  } catch (err) {
    if (current) error.value = err instanceof Error ? err.message : 'Unable to load this lesson.'
  }
}, { immediate: true })

async function go(index: number) {
  step.value = index
  await nextTick()
  stepTitle.value?.focus()
}
async function run(mode: ReplayMode) {
  const id = props.id
  busy.value = mode
  replayError.value = ''
  try {
    const result = await replay(id, mode)
    if (props.id !== id) return
    if (mode === 'positive') positive.value = result
    else negative.value = result
  } catch (err) {
    if (props.id === id) replayError.value = err instanceof Error ? err.message : 'Replay failed.'
  } finally {
    if (props.id === id) busy.value = undefined
  }
}
</script>

<template>
  <RouterLink class="back-link" to="/learn"><ArrowLeft :size="16" aria-hidden="true" /> All learning tracks</RouterLink>
  <p v-if="error" class="error-box" role="alert">{{ error }}</p>
  <p v-else-if="!scenario" class="muted" role="status">Loading lesson…</p>
  <template v-else>
    <header class="lesson-heading">
      <div class="inline-meta"><span>{{ scenario.difficulty }}</span><span><Clock3 :size="14" aria-hidden="true" /> {{ scenario.minutes }} min</span><span>{{ scenario.platform }}</span></div>
      <h1>{{ scenario.title }}</h1><p>{{ scenario.overview }}</p>
      <a class="attack-link" :href="scenario.reference" target="_blank" rel="noopener noreferrer">{{ scenario.attack.id }} · {{ scenario.attack.name }} <ExternalLink :size="14" aria-hidden="true" /></a>
    </header>
    <nav class="lesson-steps" aria-label="Lesson steps">
      <button v-for="(label, index) in steps" :key="label" :aria-current="step === index ? 'step' : undefined" @click="go(index)"><span aria-hidden="true">{{ index + 1 }}</span>{{ label }}<ChevronRight v-if="index < steps.length - 1" :size="14" aria-hidden="true" /></button>
    </nav>
    <div class="lesson-grid">
      <section class="panel lesson-panel" :aria-label="steps[step]">
        <template v-if="step === 0">
          <h2 ref="stepTitle" tabindex="-1">What you’ll investigate</h2>
          <dl class="reading-list"><div><dt>Attacker objective</dt><dd>{{ scenario.objective }}</dd></div><div><dt>What you’ll learn</dt><dd>{{ scenario.evidence }}</dd></div><div><dt>Prerequisites</dt><dd>{{ scenario.prerequisites }}</dd></div></dl>
          <div class="notice"><ShieldCheck :size="21" aria-hidden="true" /><div><strong>{{ showcase ? 'Read-only sample data' : 'Safe by design' }}</strong><p>{{ showcase ? 'This showcase displays prerecorded synthetic examples.' : 'Replay inserts bundled synthetic log records into your local database. It sends no real sign-in requests, opens no target systems, and uses no actual account data.' }}</p></div></div>
        </template>
        <template v-else-if="step === 1">
          <h2 ref="stepTitle" tabindex="-1">Inspect the clean baseline</h2>
          <p>Expand an event to see the fields the analyst receives. Times are shown in UTC.</p>
          <Timeline v-if="data" :events="data.baseline.events" />
          <div class="notice"><FlaskConical :size="20" aria-hidden="true" /><div><strong>Detection hypothesis</strong><p>{{ scenario.hypothesis }}</p></div></div>
        </template>
        <template v-else-if="step === 2">
          <h2 ref="stepTitle" tabindex="-1">Replay &amp; evidence</h2>
          <p>{{ showcase ? 'Open the positive sample and inspect the evidence the local fixture generated.' : 'Replay the positive fixture, inspect the resulting evidence, then compare it with the noisy fixture.' }}</p>
          <button class="button primary" :disabled="!!busy" @click="run('positive')"><Play :size="16" aria-hidden="true" /> {{ busy === 'positive' ? 'Loading…' : showcase ? 'View positive sample' : 'Replay safe events' }}</button>
          <p v-if="replayError" role="alert" class="error-box">{{ replayError }}</p>
          <div v-if="positive" class="result-panel">
            <p class="result-label" role="status"><span class="dot" /> {{ positive.alerts.length }} {{ positive.alerts.length === 1 ? 'alert' : 'alerts' }} {{ showcase ? 'in sample' : 'generated' }}</p>
            <p>{{ scenario.evidence }}</p>
            <RouterLink class="button secondary" :to="`/investigations/${positive.id}`">Open evidence timeline <ArrowRight :size="16" aria-hidden="true" /></RouterLink>
            <Timeline :events="positive.events" />
          </div>
          <div class="lesson-divider">
            <h3>Compare a noisy fixture</h3><p>{{ scenario.false_positive }}</p>
            <button class="button secondary" :disabled="!!busy" @click="run('negative')"><Play :size="15" aria-hidden="true" /> {{ busy === 'negative' ? 'Loading…' : showcase ? 'View noisy sample' : 'Replay noisy events' }}</button>
            <div v-if="negative" class="result-panel"><p class="result-label" role="status">{{ negative.alerts.length }} {{ negative.alerts.length === 1 ? 'alert' : 'alerts' }} in noisy fixture</p><Timeline :events="negative.events" /></div>
          </div>
        </template>
        <template v-else-if="step === 3">
          <h2 ref="stepTitle" tabindex="-1">Contain, prevent, and validate</h2>
          <dl class="reading-list"><div><dt>Containment</dt><dd>{{ scenario.response }}</dd></div><div><dt>Prevention</dt><dd>{{ scenario.prevention }}</dd></div><div><dt>Rule tuning</dt><dd>{{ scenario.tuning }}</dd></div><div><dt>Validation</dt><dd>{{ scenario.validation }}</dd></div><div><dt>Limitations</dt><dd>{{ scenario.limitations }}</dd></div></dl>
          <RouterLink class="button secondary" :to="`/rules/${scenario.id}`">View rule and queries <ArrowRight :size="16" aria-hidden="true" /></RouterLink>
        </template>
        <template v-else>
          <h2 ref="stepTitle" tabindex="-1">Check your understanding</h2>
          <form @submit.prevent="scored = true">
            <fieldset class="quiz" v-for="(question, index) in scenario.questions" :key="question.prompt">
              <legend>{{ question.prompt }}</legend>
              <label v-for="(option, optionIndex) in question.options" :key="option"><input type="radio" v-model="answers[index]" :name="`question-${index}`" :value="optionIndex" @change="scored = false" required />{{ option }}</label>
              <p v-if="scored" class="feedback" :class="{ incorrect: answers[index] !== question.answer }">{{ answers[index] === question.answer ? 'Correct.' : 'Review this answer.' }} {{ question.explanation }}</p>
            </fieldset>
            <button class="button primary" type="submit"><ListChecks :size="17" aria-hidden="true" /> Check answers</button>
          </form>
          <div v-if="scored" class="result-panel" role="status">{{ score }} of {{ scenario.questions.length }} correct.</div>
          <div v-if="scored && score === scenario.questions.length" class="actions">
            <button class="button secondary" :disabled="!!progress[scenario.id]" @click="complete(scenario.id)"><Check :size="17" aria-hidden="true" /> {{ progress[scenario.id] ? 'Completed' : 'Mark as completed' }}</button>
            <RouterLink class="button text-button" to="/progress">View learning report <ArrowRight :size="16" aria-hidden="true" /></RouterLink>
          </div>
        </template>
        <div v-if="step < steps.length - 1" class="lesson-next actions"><button class="button secondary" @click="go(step + 1)">{{ ['Inspect baseline', 'Continue to replay', 'Continue to response', 'Take the knowledge check'][step] }} <ArrowRight :size="16" aria-hidden="true" /></button></div>
      </section>
      <aside class="panel lesson-aside">
        <div class="section-title"><h2>Lesson details</h2><BookOpen :size="18" aria-hidden="true" /></div>
        <dl class="reading-list small"><div><dt>Telemetry</dt><dd>{{ scenario.telemetry }}</dd></div><div><dt>Detection</dt><dd><code>{{ scenario.rule.id }}</code> · {{ validationStatus(scenario.id) }}</dd></div><div><dt>ATT&amp;CK release</dt><dd>Enterprise {{ catalog?.attack.version ?? 'loading' }} · {{ scenario.attack.confidence }} mapping</dd></div><div><dt>Mapping scope</dt><dd>{{ scenario.attack.rationale }}</dd></div></dl>
      </aside>
    </div>
  </template>
</template>
