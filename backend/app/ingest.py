"""Parse declared, synthetic source envelopes into schema v1."""

from typing import Any, Literal

from pydantic import Field

from .models import Event, Model, Scenario, Source

# Envelope shapes are representative lab projections, with source-specific field names.
SOURCE_FIELDS: dict[Source, tuple[str, str, str, str, str, str]] = {
    "identity": (
        "createdDateTime",
        "appDisplayName",
        "userPrincipalName",
        "activityDisplayName",
        "result",
        "id",
    ),
    "windows": ("TimeCreated", "Computer", "User", "Activity", "Status", "EventID"),
    "linux": ("timestamp", "node", "acct", "type", "res", "serial"),
    "mail": (
        "Timestamp",
        "Relay",
        "RecipientEmailAddress",
        "Activity",
        "DeliveryAction",
        "EventType",
    ),
    "network": ("ts", "sensor", "principal", "event_type", "verdict", "signature_id"),
    "cloud": (
        "eventTime",
        "recipientAccountId",
        "userIdentity",
        "eventName",
        "result",
        "eventSource",
    ),
    "github": ("created_at", "repo", "actor", "action", "result", "operation_type"),
    "kubernetes": ("stageTimestamp", "cluster", "username", "verb", "responseStatus", "auditType"),
    "saas": ("CreationTime", "OrganizationId", "UserId", "Operation", "ResultStatus", "RecordType"),
    "scanner": ("timestamp", "repository", "author", "detector", "result", "finding_type"),
}
OPTIONAL_FIELDS = frozenset(
    {"process", "command_line", "parent_process", "source_ip", "destination_ip", "url", "domain"}
)


class Raw(Model):
    format: Literal["threathuntx.synthetic.v1"]
    source: Source
    record_id: str
    record: dict[str, Any]
    context: dict[str, Any] = Field(default_factory=dict)
    observables: dict[str, str | int | bool] = Field(default_factory=dict)


def parse(raw: dict, scenario: Scenario, fixture: str) -> Event:
    envelope = Raw.model_validate(raw)
    timestamp, host, user, action, outcome, event_id = SOURCE_FIELDS[envelope.source]
    required = {timestamp, host, user, action, outcome, event_id}
    if envelope.record.keys() != required:
        raise ValueError(f"{envelope.source} record needs exactly {sorted(required)}")
    if not envelope.context.keys() <= OPTIONAL_FIELDS:
        raise ValueError("Unknown context field")
    return Event(
        event_timestamp=envelope.record[timestamp],
        source=envelope.source,
        host=envelope.record[host],
        user=envelope.record[user],
        action=envelope.record[action],
        outcome=envelope.record[outcome],
        event_id=str(envelope.record[event_id]),
        record_id=envelope.record_id,
        evidence_reference=f"{fixture}#{envelope.record_id}",
        scenario_id=scenario.id,
        technique_id=scenario.attack.id,
        observables=envelope.observables,
        **envelope.context,
    )
