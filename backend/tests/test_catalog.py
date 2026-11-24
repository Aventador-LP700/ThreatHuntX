from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import pytest
from app.detect import correlate, matches
from app.store import Store

LESSONS = [f"{index:02}" for index in range(1, 41)]


@pytest.mark.parametrize("scenario_id", LESSONS)
def test_full_api_replay_and_investigation(client, catalog, scenario_id):
    scenario = catalog.scenarios[scenario_id]
    baseline = client.get(f"/api/scenarios/{scenario_id}").json()["baseline"]
    assert baseline["events"] and not baseline["alerts"]
    positive = client.post("/api/replay", json={"scenario_id": scenario_id, "mode": "positive"})
    assert positive.status_code == 201
    run = positive.json()
    saved = client.get(f"/api/runs/{run['id']}")
    assert saved.json() == run
    (alert,) = run["alerts"]
    assert alert["rule_id"] == scenario.rule.id
    assert alert["event_count"] == scenario.rule.threshold
    assert {event["record_id"] for event in run["events"] if event["alert_id"]} == set(
        alert["evidence"]
    )
    assert all(
        event["synthetic"] and event["evidence_reference"].startswith("scenarios/fixtures/")
        for event in run["events"]
    )
    negative = client.post(
        "/api/replay", json={"scenario_id": scenario_id, "mode": "negative"}
    ).json()
    assert negative["events"] and not negative["alerts"]
    assert negative["id"] != run["id"]


@pytest.mark.parametrize("scenario_id", LESSONS)
def test_rule_ignores_labels_and_checks_each_observable(catalog, scenario_id):
    scenario = catalog.scenarios[scenario_id]
    events = catalog.fixtures[scenario_id, "positive"]
    independent = [
        event.model_copy(update={"scenario_id": "99", "technique_id": "T1000"}) for event in events
    ]
    assert correlate(scenario, independent, "test")
    mismatched = [
        event.model_copy(update={"source": "scanner" if event.source != "scanner" else "saas"})
        for event in independent
    ]
    assert not correlate(scenario, mismatched, "test")
    for predicate in scenario.rule.match:
        nonempty = [event for event in events if matches(event, predicate)]
        assert nonempty
        if predicate.field.startswith("observables."):
            key = predicate.field.split(".")[1]
            incomplete = [
                event.model_copy(
                    update={"observables": {k: v for k, v in event.observables.items() if k != key}}
                )
                for event in events
            ]
            assert not correlate(scenario, incomplete, "test")
    if scenario.rule.suppress_when:
        without_exception = scenario.model_copy(
            update={"rule": scenario.rule.model_copy(update={"suppress_when": []})}
        )
        assert correlate(without_exception, catalog.fixtures[scenario_id, "negative"], "test")


def test_catalog_and_expected_ground_truth(catalog):
    assert list(catalog.scenarios) == LESSONS
    assert len({scenario.category for scenario in catalog.scenarios.values()}) == 8
    assert sum(scenario.core_lesson for scenario in catalog.scenarios.values()) == 10
    metrics = catalog.validation["metrics"]
    assert (metrics["tp"], metrics["tn"], metrics["fp"], metrics["fn"]) == (40, 80, 0, 0)


def test_window_includes_exact_boundary(catalog):
    scenario = catalog.scenarios["02"]
    first, second, third = catalog.fixtures["02", "positive"][1:]
    third = third.model_copy(
        update={"event_timestamp": first.event_timestamp + timedelta(minutes=5)}
    )
    assert len(correlate(scenario, [first, second, third], "test")) == 1


def test_concurrent_replays_are_atomic_and_survive_restart(catalog, tmp_path):
    store = Store(tmp_path / "runs.db")
    store.initialize(catalog)
    with ThreadPoolExecutor(4) as executor:
        written = list(
            executor.map(
                lambda _: store.replay(catalog, catalog.scenarios["02"], "positive"), range(12)
            )
        )
    assert len({entry["id"] for entry in written}) == 12
    reloaded = Store(store.path)
    reloaded.initialize(catalog)
    assert len(reloaded.recent()) == 12
    assert all(reloaded.get(entry["id"]) == entry for entry in written)
    reloaded.reset(catalog)
    assert not reloaded.recent()
    assert reloaded.get("baseline-02")["alerts"] == []
