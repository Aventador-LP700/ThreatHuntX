import { ref } from 'vue'
import type { Difficulty, Scenario } from './types'

interface Completion { completed_at: string }
const progressKey = 'threathuntx.progress.v1'
function getProgress(): Record<string, Completion> {
  try {
    const value: unknown = JSON.parse(localStorage.getItem(progressKey) ?? '{}')
    if (!value || typeof value !== 'object' || Array.isArray(value)) return {}
    return Object.fromEntries(Object.entries(value).filter(([id, item]) => /^\d{2}$/.test(id) && typeof item?.completed_at === 'string'))
  } catch { return {} }
}
export const progress = ref(getProgress())
export function complete(id: string) {
  if (progress.value[id]) return
  progress.value = { ...progress.value, [id]: { completed_at: new Date().toISOString() } }
  try { localStorage.setItem(progressKey, JSON.stringify(progress.value)) } catch { /* session progress is still available */ }
}
export const tracks: Difficulty[] = ['Beginner', 'Intermediate', 'Advanced']
export const curricula = [
  { name: 'SOC L1', description: 'Triage mail, identity and endpoint alerts.', ids: ['02', '01', '03', '09', '39'] },
  { name: 'SOC L2 / Threat Hunter', description: 'Correlate signals across accounts, hosts and networks.', ids: ['06', '13', '16', '19', '21', '26'] },
  { name: 'Detection Engineer', description: 'Work with thresholds, suppressions and rule portability.', ids: ['03', '06', '09', '18', '23', '34'] },
  { name: 'Penetration Tester to Purple Teamer', description: 'Translate observations into testable defensive hypotheses.', ids: ['04', '15', '17', '23', '37', '38'] },
  { name: 'Cloud / DevSecOps', description: 'Investigate cloud, pipeline and cluster authorization changes.', ids: ['20', '31', '32', '33', '35', '40'] },
]
export function learningReport(scenarios: Scenario[]) {
  return {
    project: 'ThreatHuntX', scope: 'Synthetic learning exercises', schema_version: 1,
    completed: scenarios.filter(s => progress.value[s.id]).map(s => ({
      id: s.id, title: s.title, attack: s.attack.id, difficulty: s.difficulty,
      completed_at: progress.value[s.id].completed_at,
    })),
  }
}
export function download(filename: string, data: any) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2) + '\n'], { type: 'application/json' }))
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.append(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
export function titleCase(value: string) {
  return value.replaceAll('_', ' ').replace(/(?:^|\s)\S/g, char => char.toUpperCase())
}
export function time(value: string) {
  return new Intl.DateTimeFormat('en-GB', { timeZone: 'UTC', hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date(value))
}
