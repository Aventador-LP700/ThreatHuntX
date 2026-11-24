import type { EventRecord, Run, Scenario } from './types'

export const dispositions = {
  unreviewed: 'Unreviewed',
  benign: 'Explained by benign activity',
  investigate: 'Needs more evidence',
  escalate: 'Escalate for response',
} as const
export type Disposition = keyof typeof dispositions
export interface CaseAnalysis {
  hypothesis: string
  notes: string
  disposition: Disposition
  response: string
  updated_at: string | null
}
export interface EventFilter { host: string; user: string; source: string; outcome: string; text: string }
export type PivotField = 'host' | 'user' | 'source'
export const blankFilter = (): EventFilter => ({ host: '', user: '', source: '', outcome: '', text: '' })
const sessionAnalysis = new Map<string, CaseAnalysis>()
const analysisKey = (id: string) => `threathuntx.case.v1.${id}`

export function readAnalysis(id: string): CaseAnalysis {
  const blank: CaseAnalysis = { hypothesis: '', notes: '', disposition: 'unreviewed', response: '', updated_at: null }
  const cached = sessionAnalysis.get(id)
  if (cached) return { ...cached }
  try {
    const value = JSON.parse(localStorage.getItem(analysisKey(id)) ?? 'null')
    if (value && typeof value === 'object') {
      return {
        hypothesis: typeof value.hypothesis === 'string' ? value.hypothesis.slice(0, 700) : '',
        notes: typeof value.notes === 'string' ? value.notes.slice(0, 4000) : '',
        response: typeof value.response === 'string' ? value.response.slice(0, 1500) : '',
        disposition: Object.hasOwn(dispositions, value.disposition) ? value.disposition : 'unreviewed',
        updated_at: typeof value.updated_at === 'string' && Number.isFinite(Date.parse(value.updated_at)) ? value.updated_at : null,
      }
    }
  } catch { /* a clean case remains usable with restricted browser storage */ }
  return blank
}

export function saveAnalysis(id: string, analysis: CaseAnalysis): boolean {
  sessionAnalysis.set(id, { ...analysis })
  try { localStorage.setItem(analysisKey(id), JSON.stringify(analysis)); return true }
  catch { return false }
}

export function filterEvidence(events: EventRecord[], filter: EventFilter) {
  const text = filter.text.trim().toLowerCase()
  return events.filter(event =>
    (!filter.host || event.host === filter.host) &&
    (!filter.user || event.user === filter.user) &&
    (!filter.source || event.source === filter.source) &&
    (!filter.outcome || event.outcome === filter.outcome) &&
    (!text || [event.host, event.user, event.source, event.process, event.action, event.record_id,
      event.source_ip, event.domain, event.evidence_reference, ...Object.values(event.observables)].join(' ').toLowerCase().includes(text)),
  )
}

export function caseReport(run: Run, scenario: Scenario, analysis: CaseAnalysis) {
  return {
    schema_version: 1,
    synthetic_only: true,
    case_id: run.id,
    scenario: { id: scenario.id, title: scenario.title, attack: scenario.attack },
    rule_id: scenario.rule.id,
    fixture_mode: run.mode,
    recorded_at: run.created_at,
    generated_at: new Date().toISOString(),
    analysis: { ...analysis, hypothesis: analysis.hypothesis || scenario.hypothesis },
    limitations: scenario.limitations,
    mitigations: [scenario.response, scenario.prevention],
    alerts: run.alerts,
    evidence: run.events,
  } as const
}
export type CaseReport = ReturnType<typeof caseReport>

function csvCell(value: string | number | null) {
  let text = value === null ? '' : String(value)
  if (/^[\t\r\n]/.test(text) || /^[\s\uFEFF]*[=+\-@＝＋－＠]/.test(text)) text = "'" + text
  return `"${text.replaceAll('"', '""')}"`
}
export function caseCsv(report: CaseReport) {
  const headers = ['case_id', 'scenario_id', 'rule_id', 'fixture_mode', 'recorded_at', 'event_timestamp', 'record_id', 'evidence_reference', 'host', 'user', 'source', 'outcome', 'matched_alert', 'hypothesis', 'disposition', 'notes', 'response', 'limitations', 'mitigations']
  const rows = report.evidence.map(event => [
    report.case_id, report.scenario.id, report.rule_id, report.fixture_mode, report.recorded_at,
    event.event_timestamp, event.record_id, event.evidence_reference, event.host, event.user, event.source, event.outcome, event.alert_id,
    report.analysis.hypothesis, report.analysis.disposition, report.analysis.notes, report.analysis.response, report.limitations, report.mitigations.join(' '),
  ])
  return [headers, ...rows].map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n'
}
