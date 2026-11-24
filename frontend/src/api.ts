import { computed, ref } from 'vue'
import type { Artifact, ArtifactKind, Catalog, Coverage, LessonData, ReplayMode, Run } from './types'

export const showcase = import.meta.env.MODE === 'showcase'
type Snapshot = { catalog: Catalog; coverage: Coverage; artifacts: Record<string, Artifact>; runs: Record<string, Run> }
let snapshotPromise: Promise<Snapshot> | undefined
const showcaseRuns = new Map<string, Run>()

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, options)
  if (!response.ok) throw new Error(`Request failed (${response.status}). Check that the lab is healthy and try again.`)
  return response.json() as Promise<T>
}
function snapshot() {
  if (!snapshotPromise) snapshotPromise = request<Snapshot>(`${import.meta.env.BASE_URL}snapshot.json`).catch(error => {
    snapshotPromise = undefined
    throw error
  })
  return snapshotPromise
}
export const catalog = ref<Catalog>()
export const coverage = ref<Coverage>()
export const runs = ref<Run[]>([])
export const scenarios = computed(() => catalog.value?.scenarios ?? [])
export const loadError = ref('')
export const loading = ref(false)

export async function refreshRuns() {
  runs.value = showcase ? [...showcaseRuns.values()].reverse() : await request<Run[]>('/api/runs')
}
export async function refresh() {
  loadError.value = ''
  loading.value = true
  try {
    const [newCatalog, newCoverage] = await Promise.all([
      showcase ? snapshot().then(data => data.catalog) : request<Catalog>('/api/scenarios'),
      showcase ? snapshot().then(data => data.coverage) : request<Coverage>('/api/coverage'),
      refreshRuns(),
    ])
    catalog.value = newCatalog
    coverage.value = newCoverage
  } catch (error) {
    loadError.value = error instanceof Error ? error.message : 'The catalog could not be loaded.'
  } finally {
    loading.value = false
  }
}
export async function lesson(id: string): Promise<LessonData> {
  if (!showcase) return request(`/api/scenarios/${encodeURIComponent(id)}`)
  const data = await snapshot()
  const scenario = data.catalog.scenarios.find(item => item.id === id)
  const baseline = data.runs[`baseline-${id}`]
  if (!scenario || !baseline) throw new Error('This lesson is unavailable.')
  return { scenario, baseline }
}
export async function replay(id: string, mode: ReplayMode): Promise<Run> {
  if (showcase) {
    const data = await snapshot()
    const run = data.runs[`sample-${id}-${mode}`]
    if (!run) throw new Error('This example is unavailable.')
    showcaseRuns.set(run.id, run)
    await refreshRuns()
    return run
  }
  const run = await request<Run>('/api/replay', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scenario_id: id, mode }),
  })
  runs.value = [run, ...runs.value].slice(0, 50)
  return run
}
export async function investigation(id: string): Promise<Run> {
  if (!showcase) return request(`/api/runs/${encodeURIComponent(id)}`)
  const run = (await snapshot()).runs[id]
  if (!run) throw new Error('This investigation is unavailable.')
  return run
}
export function validationStatus(id: string) {
  const cases = coverage.value?.cases.filter(test => test.scenario_id === id) ?? []
  if (!cases.length) return 'Documented'
  return cases.every(test => test.passed) ? 'Synthetic-verified' : 'Fixture checks failed'
}

export async function ruleArtifact(id: string, kind: ArtifactKind): Promise<Artifact> {
  if (!showcase) return request(`/api/rules/${encodeURIComponent(id)}/artifacts/${kind}`)
  const data = await snapshot()
  const info = data.artifacts[kind === 'wazuh' ? 'wazuh' : `${id}-${kind}`]
  if (!info) throw new Error('This rule format is unavailable.')
  return info
}
