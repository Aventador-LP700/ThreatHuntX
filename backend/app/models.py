from datetime import datetime
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, IPvAnyAddress, model_validator

Source = Literal[
    "identity",
    "windows",
    "linux",
    "mail",
    "network",
    "cloud",
    "github",
    "kubernetes",
    "saas",
    "scanner",
]
Outcome = Literal["success", "failure", "denied", "allowed", "blocked", "observed"]
Mode = Literal["baseline", "positive", "negative"]
Short = Annotated[str, Field(min_length=1, max_length=300)]
Slug = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]{0,79}$")]
Technique = Annotated[str, Field(pattern=r"^T\d{4}(?:\.\d{3})?$")]
ScenarioId = Annotated[str, Field(pattern=r"^\d{2}$")]
Scalar = str | int | bool
FieldName = Annotated[
    str,
    Field(
        pattern=r"^(?:source|host|user|process|command_line|parent_process|event_id|source_ip|destination_ip|url|domain|outcome|action|observables\.[a-z][a-z0-9_]*)$"
    ),
]


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Event(Model):
    schema_version: Literal[1] = 1
    event_timestamp: AwareDatetime
    source: Source
    host: Short
    user: Short | None = None
    process: Short | None = None
    command_line: Short | None = None
    parent_process: Short | None = None
    event_id: Short
    record_id: Short
    source_ip: IPvAnyAddress | None = None
    destination_ip: IPvAnyAddress | None = None
    url: Short | None = None
    domain: Short | None = None
    action: Slug
    outcome: Outcome
    evidence_reference: Short
    scenario_id: ScenarioId
    technique_id: Technique
    alert_id: str | None = None
    synthetic: Literal[True] = True
    observables: dict[Slug, Scalar] = Field(default_factory=dict)

    def detection_field(self, key: str) -> Scalar | None:
        if key.startswith("observables."):
            return self.observables.get(key.split(".", 1)[1])
        value = getattr(self, key)
        return str(value) if key in {"source_ip", "destination_ip"} and value else value


class Predicate(Model):
    field: FieldName
    op: Literal["eq", "in", "contains", "starts_with", "ends_with", "gte"] = "eq"
    value: Scalar | list[Scalar]

    @model_validator(mode="after")
    def check_operand(self):
        if self.op == "in":
            if not isinstance(self.value, list) or not self.value:
                raise ValueError("in requires one or more alternatives")
        elif isinstance(self.value, list):
            raise ValueError("only in accepts a list of values")
        if self.op == "gte" and type(self.value) is not int:
            raise ValueError("gte requires an integer")
        if self.op in {"contains", "starts_with", "ends_with"} and not isinstance(self.value, str):
            raise ValueError("string comparison requires text")
        return self


class Rule(Model):
    id: Annotated[str, Field(pattern=r"^THX-\d{2}$")]
    severity: Literal["low", "medium", "high"]
    source: Source
    match: list[Predicate] = Field(min_length=2)
    suppress_when: list[Predicate] = Field(default_factory=list)
    group_by: FieldName
    threshold: int = Field(ge=1, le=30)
    window_seconds: int = Field(ge=1, le=86400)
    distinct: FieldName | None = None

    @model_validator(mode="after")
    def check_predicates(self):
        for conditions in [self.match, self.suppress_when]:
            fields = [p.field for p in conditions]
            if len(set(fields)) != len(fields):
                raise ValueError("use a single predicate per field within a selection")
        return self


class Mapping(Model):
    id: Technique
    name: Short
    url: Short
    tactics: list[Slug] = Field(min_length=1)
    confidence: Literal["direct", "related"]
    rationale: Short


class Question(Model):
    prompt: Short
    options: list[Short] = Field(min_length=2, max_length=4)
    answer: int = Field(ge=0)
    explanation: Short

    @model_validator(mode="after")
    def check_answer(self):
        if self.answer >= len(self.options) or len(self.options) != len(set(self.options)):
            raise ValueError("answer must select one of the distinct options")
        return self


class Scenario(Model):
    id: ScenarioId
    title: Short
    category: Short
    overview: Short
    objective: Short
    platform: Short
    difficulty: Literal["Beginner", "Intermediate", "Advanced"]
    minutes: int = Field(ge=1, le=45)
    prerequisites: Short
    attack: Mapping
    telemetry: Short
    data_sources: list[Short] = Field(min_length=1)
    hypothesis: Short
    evidence: Short
    false_positive: Short
    tuning: Short
    response: Short
    prevention: Short
    validation: Short
    limitations: Short
    questions: list[Question] = Field(min_length=2, max_length=3)
    rule: Rule
    core_lesson: bool
    reference: Short
    license: Literal["MIT"] = "MIT"


class Alert(Model):
    id: str
    rule_id: str
    scenario_id: ScenarioId
    title: str
    severity: str
    group: str
    first_seen: datetime
    last_seen: datetime
    event_count: int
    evidence: list[str]


class RunRequest(Model):
    scenario_id: ScenarioId
    mode: Literal["positive", "negative"]


class CaseAnalysis(Model):
    hypothesis: Annotated[str, Field(min_length=1, max_length=700)]
    notes: Annotated[str, Field(max_length=4000)]
    disposition: Literal["unreviewed", "benign", "investigate", "escalate"]
    response: Annotated[str, Field(max_length=1500)]
    updated_at: AwareDatetime | None


class CaseScenario(Model):
    id: ScenarioId
    title: Short
    attack: Mapping


class CaseReport(Model):
    schema_version: Literal[1]
    synthetic_only: Literal[True]
    case_id: Short
    scenario: CaseScenario
    rule_id: Annotated[str, Field(pattern=r"^THX-\d{2}$")]
    fixture_mode: Mode
    recorded_at: AwareDatetime
    generated_at: AwareDatetime
    analysis: CaseAnalysis
    limitations: Short
    mitigations: list[Short] = Field(min_length=1)
    alerts: list[Alert]
    evidence: list[Event] = Field(min_length=1)
