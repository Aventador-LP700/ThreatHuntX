import csv
import io
import json

import pytest
from app.exports import safe_cell

from scripts.build_showcase import snapshot


@pytest.mark.parametrize("lesson", [f"{index:02d}" for index in range(1, 41)])
def test_studio_default_matches_ground_truth(client, lesson):
    trial = client.get(f"/api/scenarios/{lesson}/trial").json()
    assert trial["synthetic_only"]
    assert trial["settings"] == trial["defaults"]
    assert trial["group_options"][0] == trial["settings"]["group_by"]
    assert (trial["metrics"]["tp"], trial["metrics"]["tn"]) == (1, 2)
    assert trial["cases"][0]["matched_records"]
    assert all(not result["matched_records"] for result in trial["cases"][1:])


def test_trial_false_positives_and_misses_leave_rule_and_history_intact(client):
    path = "/api/scenarios/02/trial"
    original = client.get(path).json()
    settings = original["settings"]
    near = client.post(path, json=settings | {"threshold": 4}).json()
    assert near["metrics"]["fn"] == 1 and near["metrics"]["precision"] is None
    narrow = client.post(path, json=settings | {"window_seconds": 1}).json()
    assert narrow["metrics"]["fn"] == 1
    noisy = client.post(path, json=settings | {"threshold": 1, "group_by": "host"}).json()
    assert noisy["metrics"]["fp"] == 1
    assert noisy["settings"]["group_by"] == "host"
    assert client.get(path).json() == original
    assert client.get("/api/runs").json() == []


@pytest.mark.parametrize(
    "overrides",
    [
        {"threshold": True},
        {"threshold": 31},
        {"window_seconds": 0},
        {"group_by": "observables.nonexistent"},
        {"group_by": "record_id"},
        {"match": []},
    ],
)
def test_trial_input_is_bounded(client, overrides):
    path = "/api/scenarios/02/trial"
    settings = client.get(path).json()["settings"]
    assert client.post(path, json=settings | overrides).status_code == 422
    assert (
        client.post(path, json=settings, headers={"Origin": "https://example.invalid"}).status_code
        == 403
    )


def test_static_snapshot_equals_default_fixture_comparison_and_download(client, catalog):
    static = snapshot(catalog)
    assert len(static["trials"]) == 40
    assert len(static["runs"]) == 120
    assert client.get("/api/scenarios/02/trial").json() == static["trials"]["02"]
    fixture = client.get("/api/scenarios/02/fixtures/positive/export")
    assert fixture.json() == {"synthetic_only": True, **static["runs"]["sample-02-positive"]}
    csv_result = client.get("/api/scenarios/02/fixtures/positive/export?format=csv")
    assert len(list(csv.DictReader(io.StringIO(csv_result.text)))) == len(fixture.json()["events"])
    assert "sample-02-positive" in csv_result.headers["Content-Disposition"]
    assert client.get("/api/runs").json() == []


@pytest.mark.parametrize("text", ["=1+1", " +2", "\ufeff\u00a0-2", "\nplain", "\ttext", "＠value"])
def test_spreadsheet_formulas_export_as_text(text):
    assert safe_cell(text) == "'" + text
    assert safe_cell('identity,"interactive"') == 'identity,"interactive"'


def test_taxonomy_matches_all_ids_and_names(catalog):
    taxonomy = json.loads((catalog.root / "scenarios/taxonomy.json").read_text())
    assert len(taxonomy) == 8 and all(len(section["lessons"]) == 5 for section in taxonomy)
    assert [(item.category, item.title) for item in catalog.scenarios.values()] == [
        (section["category"], title) for section in taxonomy for title in section["lessons"]
    ]
