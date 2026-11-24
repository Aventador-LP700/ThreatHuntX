export type Scalar = string | number | boolean
export type Mode = 'baseline' | 'positive' | 'negative'
export type ReplayMode = Exclude<Mode, 'baseline'>
export type Difficulty = 'Beginner' | 'Intermediate' | 'Advanced'

export interface EventRecord {
  event_timestamp: string
  source: string
  host: string
  user: string | null
  process: string | null
  command_line: string | null
  parent_process: string | null
  event_id: string
  record_id: string
  source_ip: string | null
  destination_ip: string | null
  url: string | null
  domain: string | null
  action: string
  outcome: string
  evidence_reference: string
  scenario_id: string
  technique_id: string
  alert_id: string | null
  observables: Record<string, Scalar>
}
export interface Alert {
  id: string
  rule_id: string
  scenario_id: string
  title: string
  severity: string
  group: string
  first_seen: string
  last_seen: string
  event_count: number
  evidence: string[]
}
export interface Run {
  id: string
  scenario_id: string
  mode: Mode
  created_at: string
  events: EventRecord[]
  alerts: Alert[]
}
export interface Predicate {
  field: string
  op: 'eq' | 'in' | 'contains' | 'starts_with' | 'ends_with' | 'gte'
  value: Scalar | Scalar[]
}
export interface Rule {
  id: string
  severity: string
  source: string
  group_by: string
  threshold: number
  window_seconds: number
  distinct: string | null
  match: Predicate[]
  suppress_when: Predicate[]
}
export interface Scenario {
  id: string
  title: string
  category: string
  overview: string
  objective: string
  platform: string
  difficulty: Difficulty
  minutes: number
  prerequisites: string
  attack: { id: string; name: string; url: string; tactics: string[]; confidence: 'direct' | 'related'; rationale: string }
  telemetry: string
  data_sources: string[]
  hypothesis: string
  evidence: string
  false_positive: string
  tuning: string
  response: string
  prevention: string
  validation: string
  limitations: string
  questions: { prompt: string; options: string[]; answer: number; explanation: string }[]
  rule: Rule
  core_lesson: boolean
  reference: string
}
export interface AttackVersion { version: string; domain: string; source: string; terms: string; commit: string }
export interface Catalog { attack: AttackVersion; scenarios: Scenario[] }
export interface FixtureCheck { scenario_id: string; mode: Mode; expected: boolean; actual: boolean; alerts: number; passed: boolean }
export interface Metrics { tp: number; fp: number; tn: number; fn: number; precision: number | null; recall: number | null; passed: number; total: number; pass_rate: number }
export interface Coverage { dataset: string; cases: FixtureCheck[]; metrics: Metrics }
export interface LessonData { scenario: Scenario; baseline: Run }
