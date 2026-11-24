"""Compare detection decisions on the three labeled, bundled fixture batches."""

from pydantic import Field

from .detect import correlate
from .models import Event, FieldName, Mode, Model, Scenario

MODES: tuple[Mode, ...] = ("positive", "baseline", "negative")
GROUP_FIELDS = ("user", "host", "source_ip", "destination_ip", "domain", "process")


class TrialSettings(Model):
    threshold: int = Field(strict=True, ge=1, le=30)
    window_seconds: int = Field(strict=True, ge=1, le=86400)
    group_by: FieldName


def fixture_result(scenario: Scenario, mode: Mode, events: list[Event], alerts: list) -> dict:
    expected = mode == "positive"
    actual = bool(alerts)
    return {
        "scenario_id": scenario.id,
        "mode": mode,
        "expected": expected,
        "actual": actual,
        "alerts": len(alerts),
        "passed": expected == actual,
        "event_count": len(events),
        "matched_records": list(
            dict.fromkeys(record for alert in alerts for record in alert.evidence)
        ),
    }


def summarize(cases: list[dict]) -> dict:
    tp = sum(case["expected"] and case["actual"] for case in cases)
    fp = sum(not case["expected"] and case["actual"] for case in cases)
    tn = sum(not case["expected"] and not case["actual"] for case in cases)
    fn = sum(case["expected"] and not case["actual"] for case in cases)
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "passed": tp + tn,
        "total": len(cases),
        "pass_rate": (tp + tn) / len(cases),
    }


def evaluate_trial(
    scenario: Scenario,
    fixtures: dict[tuple[str, Mode], list[Event]],
    settings: TrialSettings | None = None,
) -> dict:
    defaults = TrialSettings(
        group_by=scenario.rule.group_by,
        threshold=scenario.rule.threshold,
        window_seconds=scenario.rule.window_seconds,
    )
    positive = fixtures[scenario.id, "positive"]
    group_options = [defaults.group_by] + [
        field
        for field in GROUP_FIELDS
        if field != defaults.group_by
        and any(event.detection_field(field) is not None for event in positive)
    ]
    settings = settings or defaults
    if settings.group_by not in group_options:
        raise ValueError("Group by a field present in this lesson's positive fixture.")
    rule = scenario.rule.model_copy(update=settings.model_dump())
    trial = scenario.model_copy(update={"rule": rule})
    cases = []
    for mode in MODES:
        events = fixtures[scenario.id, mode]
        alerts = correlate(trial, events, f"trial-{scenario.id}-{mode}")
        cases.append(fixture_result(trial, mode, events, alerts))
    return {
        "synthetic_only": True,
        "rule_id": rule.id,
        "defaults": defaults.model_dump(),
        "settings": settings.model_dump(),
        "group_options": group_options,
        "cases": cases,
        "metrics": summarize(cases),
    }
