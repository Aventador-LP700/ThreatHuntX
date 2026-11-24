<script setup lang="ts">
import { ArrowRight, ExternalLink } from 'lucide-vue-next'
import PageHeading from '../components/PageHeading.vue'
import { scenarios, showcase } from '../api'
import playbooks from '../content/playbooks.json'
const props = defineProps<{ page: string }>()
const repo = 'https://github.com/Aventador-LP700/ThreatHuntX'
</script>

<template>
  <template v-if="props.page === 'playbooks'">
    <PageHeading title="Response playbooks" description="Practise making and documenting response decisions from the evidence you have." />
    <div class="playbook-grid"><section class="panel" v-for="book in playbooks" :key="book.title"><p class="inline-meta">{{ book.scope }}</p><h2>{{ book.title }}</h2><p>{{ book.trigger }}</p><ol><li v-for="action in book.actions" :key="action">{{ action }}</li></ol><h3>Recovery</h3><p>{{ book.recovery }}</p><div class="actions"><RouterLink class="button text-button" v-for="id in book.cases" :key="id" :to="`/lesson/${id}`">{{ scenarios.find(t => t.id === id)?.title ?? `Lesson ${id}` }} <ArrowRight :size="14" aria-hidden="true" /></RouterLink></div></section></div>
  </template>
  <template v-else-if="props.page === 'deployment'">
    <PageHeading title="Deployment help" description="Run the Community Lab on your own computer with Docker Compose." />
    <div class="playbook-grid"><section class="panel"><h2>Start the lab</h2><p>Install Docker Engine or Docker Desktop with Compose v2 and start Docker.</p><pre><code>git clone https://github.com/Aventador-LP700/ThreatHuntX.git
cd ThreatHuntX
docker compose up -d --build
docker compose ps</code></pre><p>Open <a href="http://127.0.0.1:8080/">http://127.0.0.1:8080/</a> and select <strong>Start Learning</strong>. On Bash, run <code>./scripts/setup.sh</code> to build and wait for both services.</p></section><section class="panel"><h2>Health and teardown</h2><pre><code>curl -fsS http://127.0.0.1:8080/api/health
docker compose logs api web
docker compose down</code></pre><p>Set <code>THREATHUNTX_PORT</code> in <code>.env</code> if 8080 is busy. Use <code>./scripts/setup.sh reset</code> while the lab is healthy to remove this project’s replay runs and reseed its baselines.</p></section></div>
    <div class="actions matrix-panel"><a class="button secondary" :href="`${repo}/blob/main/docs/TROUBLESHOOTING.md`" target="_blank" rel="noopener noreferrer">Troubleshooting <ExternalLink :size="15" aria-hidden="true" /></a><a class="button secondary" :href="`${repo}/blob/main/docs/full-lab-setup.md`" target="_blank" rel="noopener noreferrer">Optional analyst lab <ExternalLink :size="15" aria-hidden="true" /></a></div>
  </template>
  <template v-else>
    <PageHeading title="About ThreatHuntX" description="A free, MIT-licensed learning platform for SOC analysts, defenders, students, and contributors." />
    <div class="playbook-grid"><section class="panel"><h2>How the lab works</h2><ol class="flow-list"><li>Bundled fixture</li><li>Source parser</li><li>Normalized event</li><li>Detection and evidence</li><li>Analyst timeline</li></ol><p>{{ showcase ? 'This showcase serves static files and sample timelines produced by the local runtime.' : 'FastAPI applies the local rule to each packaged replay and stores the evidence and alerts in SQLite.' }}</p><p>Your progress is stored in your browser. ThreatHuntX includes no tracking or account registration.</p></section><section class="panel"><h2>Contribute</h2><p>Suggest a lesson, record a reproducible bug, or propose a defensive rule with positive and negative fixtures.</p><div class="list-stack"><a class="list-row" :href="repo" target="_blank" rel="noopener noreferrer">GitHub repository <ExternalLink :size="16" aria-hidden="true" /></a><a class="list-row" :href="`${repo}/blob/main/CONTRIBUTING.md`" target="_blank" rel="noopener noreferrer">Contribution guide <ExternalLink :size="16" aria-hidden="true" /></a><a class="list-row" :href="`${repo}/blob/main/SECURITY.md`" target="_blank" rel="noopener noreferrer">Private security reporting <ExternalLink :size="16" aria-hidden="true" /></a></div></section></div>
  </template>
</template>
