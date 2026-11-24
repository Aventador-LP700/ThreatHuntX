"""Deterministic detection using only normalized evidence fields."""

from collections import defaultdict
from datetime import timedelta

from .models import Alert, Event, Predicate, Scenario


def folded(value):
    return value.casefold() if isinstance(value, str) else value


def matches(event: Event, predicate: Predicate) -> bool:
    value = event.detection_field(predicate.field)
    expected = predicate.value
    if value is None:
        return False
    if predicate.op == "in":
        return any(type(value) is type(item) and folded(value) == folded(item) for item in expected)
    if type(value) is not type(expected):
        return False
    value, expected = folded(value), folded(expected)
    match predicate.op:
        case "eq":
            return value == expected
        case "gte":
            return value >= expected
        case "contains":
            return expected in value
        case "starts_with":
            return value.startswith(expected)
        case "ends_with":
            return value.endswith(expected)
    raise ValueError(f"Unknown operator {predicate.op}")


def correlate(scenario: Scenario, events: list[Event], run_id: str) -> list[Alert]:
    rule = scenario.rule
    groups = defaultdict(list)
    seen = set()
    for event in sorted(events, key=lambda item: (item.event_timestamp, item.record_id)):
        key = (event.source, event.record_id)
        if key in seen:
            continue
        seen.add(key)
        if event.source != rule.source or not all(matches(event, part) for part in rule.match):
            continue
        if any(matches(event, part) for part in rule.suppress_when):
            continue
        group = event.detection_field(rule.group_by)
        if group is not None:
            groups[str(folded(group))].append(event)

    alerts = []
    window = timedelta(seconds=rule.window_seconds)
    for group, candidates in groups.items():
        start = 0
        for end, event in enumerate(candidates):
            while event.event_timestamp - candidates[start].event_timestamp > window:
                start += 1
            evidence = candidates[start : end + 1]
            if rule.distinct:
                unique = {}
                for item in evidence:
                    value = item.detection_field(rule.distinct)
                    if value is not None:
                        unique.setdefault(folded(value), item)
                evidence = list(unique.values())
            if len(evidence) < rule.threshold:
                continue
            alerts.append(
                Alert(
                    id=f"{run_id}-{len(alerts) + 1}",
                    rule_id=rule.id,
                    scenario_id=scenario.id,
                    title=scenario.title,
                    severity=rule.severity,
                    group=group,
                    first_seen=evidence[0].event_timestamp,
                    last_seen=evidence[-1].event_timestamp,
                    event_count=len(evidence),
                    evidence=[item.record_id for item in evidence],
                )
            )
            break
    return alerts
