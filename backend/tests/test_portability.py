import json
import re
from collections import defaultdict

import pytest
import yaml
from app.detect import matches
from defusedxml import ElementTree
from sigma.collection import SigmaCollection

from scripts.build_detection_artifacts import (
    field_name,
    projection,
    render,
    rule_fields,
)
from scripts.verify_attack import check

IDS = [f"{no:02}" for no in range(1, 41)]


def _sigma_select(selection, row):
    for expression, expected in selection.items():
        key, _, modifier = expression.partition("|")
        value = row.get(key)
        if value is None:
            return False
        if isinstance(value, str):
            value = value.lower()
            expected = (
                [item.lower() for item in expected]
                if isinstance(expected, list)
                else expected.lower()
            )
        match modifier:
            case "contains":
                passed = expected in value
            case "startswith":
                passed = value.startswith(expected)
            case "endswith":
                passed = value.endswith(expected)
            case "gte":
                passed = value >= expected
            case "":
                passed = value in expected if isinstance(expected, list) else value == expected
            case _:
                raise AssertionError(modifier)
        if not passed:
            return False
    return True


@pytest.mark.parametrize("scenario_id", IDS)
def test_sigma_schema_references_and_offline_field_mapping(catalog, scenario_id):
    scenario = catalog.scenarios[scenario_id]
    text = (catalog.root / "detections/sigma" / f"{scenario_id}.yml").read_text()
    rules = SigmaCollection.from_yaml(text)
    rules.resolve_rule_references()
    base, *correlations = yaml.safe_load_all(text)
    selection = base["detection"]["selection"]
    assert len(selection) == len(scenario.rule.match) + 1
    filters = [value for key, value in base["detection"].items() if key.startswith("filter_")]
    assert len(filters) == len(scenario.rule.suppress_when)
    assert bool(correlations) == (scenario.rule.threshold > 1)
    if correlations:
        condition = correlations[0]["correlation"]
        assert condition["condition"]["gte"] == scenario.rule.threshold
        assert condition["group-by"] == [field_name(scenario.rule.group_by)]
    for mode in ("positive", "negative", "baseline"):
        for event in catalog.fixtures[scenario_id, mode]:
            row = projection(event, rule_fields(scenario))
            expected = all(matches(event, p) for p in scenario.rule.match) and not any(
                matches(event, p) for p in scenario.rule.suppress_when
            )
            assert (
                _sigma_select(selection, row) and not any(_sigma_select(f, row) for f in filters)
            ) == expected


def test_wazuh_pack_is_well_formed_and_matches_event_candidates(catalog):
    decoder = ElementTree.parse(catalog.root / "detections/wazuh/decoders.xml").getroot()
    doc = ElementTree.parse(catalog.root / "detections/wazuh/rules.xml").getroot()
    rules = doc.findall("rule")
    assert len(rules) == 21
    assert [r.get("id") for r in rules] == [str(value) for value in range(100100, 100121)]
    assert rules[0].findtext("decoded_as") == decoder.get("name")
    events = {}
    for case, values in catalog.fixtures.items():
        events.update({(case[0], e.record_id): e for e in values})
    rows = {}
    for line in (catalog.root / "detections/wazuh/synthetic.log").read_text().splitlines():
        assert re.search(decoder.findtext("prematch"), line)
        row = json.loads(line.removeprefix("THX_JSON "))
        assert re.search(rules[0].findtext("field"), row["lab_format"])
        rows[row["THXRecordId"]] = row
    assert rows
    for scenario, xml_rule in zip(catalog.scenarios.values(), rules[1:]):
        assert xml_rule.findtext("if_sid") == "100100"
        assert xml_rule.findtext("mitre/id") == scenario.attack.id
        positive = []
        for (scenario_id, record_id), event in events.items():
            row = rows.get(record_id)
            if row is None:
                continue
            actual = all(
                bool(re.search(field.text, str(row[field.get("name")]).lower()))
                != (field.get("negate") == "yes")
                for field in xml_rule.findall("field")
            )
            if scenario_id == scenario.id:
                expected = all(matches(event, p) for p in scenario.rule.match) and not any(
                    matches(event, p) for p in scenario.rule.suppress_when
                )
                assert actual == expected
                if "-positive-" in record_id:
                    positive.append(actual)
        assert any(positive)


@pytest.mark.parametrize("scenario_id", IDS[:15])
def test_offline_query_intent_on_fixed_time_bins(catalog, scenario_id):
    scenario = catalog.scenarios[scenario_id]
    rule = scenario.rule
    expressions = (
        (catalog.root / "detections/kql" / f"{scenario_id}.kql").read_text(),
        (catalog.root / "detections/spl" / f"{scenario_id}.spl").read_text(),
    )
    for expression in expressions:
        assert all(
            field_name(predicate.field) in expression
            for predicate in rule.match + rule.suppress_when
        )
        assert "THXRecordId" in expression
    assert expressions[0].splitlines()[1] == "THXNormalized_CL"
    assert expressions[1].startswith('index=threathuntx sourcetype="thx:normalized:json"')
    for mode in ("positive", "negative", "baseline"):
        groups = defaultdict(set)
        for event in catalog.fixtures[scenario_id, mode]:
            if all(matches(event, p) for p in rule.match) and not any(
                matches(event, p) for p in rule.suppress_when
            ):
                bucket = int(event.event_timestamp.timestamp()) // rule.window_seconds
                label = event.detection_field(rule.distinct) if rule.distinct else event.record_id
                if label is not None:
                    groups[(event.detection_field(rule.group_by), bucket)].add(label)
        assert any(len(group) >= rule.threshold for group in groups.values()) == (
            mode == "positive"
        )


def test_artifact_regeneration_and_attack_references(catalog):
    check(catalog)
    for path, contents in render(catalog).items():
        assert (catalog.root / path).read_text() == contents


def test_api_serves_local_artifacts(client):
    assert set(client.get("/api/scenarios/02").json()["scenario"]["artifacts"]) == {
        "sigma",
        "wazuh",
        "kql",
        "spl",
    }
    data = client.get("/api/rules/02/artifacts/sigma").json()
    assert "value_count" in data["code"]
    assert client.get("/api/rules/40/artifacts/spl").status_code == 404
    assert client.get("/api/rules/02/artifacts/nope").status_code == 422
