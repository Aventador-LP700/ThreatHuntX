import csv
import io
from datetime import timedelta

from app.detect import correlate


def test_mfa_journey(client):
    assert client.get("/api/health").json() == {
        "status": "ok",
        "schema_version": 1,
        "synthetic_only": True,
    }
    lesson = client.get("/api/scenarios/02").json()
    assert lesson["baseline"]["alerts"] == []
    assert len(lesson["baseline"]["events"]) == 2
    replay = client.post("/api/replay", json={"scenario_id": "02", "mode": "positive"})
    assert replay.status_code == 201
    run = replay.json()
    assert len(run["alerts"]) == 1
    alert = run["alerts"][0]
    assert alert["rule_id"] == "THX-02"
    matched = [ev for ev in run["events"] if ev["alert_id"] == alert["id"]]
    assert {ev["record_id"] for ev in matched} == set(alert["evidence"])
    assert {ev["outcome"] for ev in matched} == {"denied"}
    assert len({ev["observables"]["challenge_id"] for ev in matched}) == 3
    detail = f"/api/runs/{run['id']}"
    assert client.get(detail).json() == run
    assert client.get(detail + "/export?format=json").json()["synthetic_only"]
    exported = client.get(detail + "/export?format=csv")
    assert len(list(csv.DictReader(io.StringIO(exported.text)))) == len(run["events"])
    noisy = client.post("/api/replay", json={"scenario_id": "02", "mode": "negative"}).json()
    assert noisy["alerts"] == []
    assert len(client.get("/api/runs").json()) == 2


def test_deduplication_grouping_window_and_metadata_independence(catalog):
    scenario = catalog.scenarios["02"]
    first, second, third = catalog.fixtures["02", "positive"][1:]
    assert correlate(scenario, [third, first, second, first], "run")[0].event_count == 3
    assert not correlate(scenario, [first, second, second, second], "run")
    assert not correlate(
        scenario,
        [first, second, third.model_copy(update={"user": "someone@example.invalid"})],
        "run",
    )
    assert not correlate(
        scenario,
        [
            first,
            second,
            third.model_copy(
                update={"event_timestamp": first.event_timestamp + timedelta(minutes=5, seconds=1)}
            ),
        ],
        "run",
    )
    independent = [
        event.model_copy(update={"scenario_id": "99", "technique_id": "T1190"})
        for event in [first, second, third]
    ]
    assert len(correlate(scenario, independent, "run")) == 1


def test_replay_scope(client):
    assert (
        client.post("/api/replay", json={"scenario_id": "00", "mode": "positive"}).status_code
        == 404
    )
    assert (
        client.post("/api/replay", json={"scenario_id": "02", "mode": "baseline"}).status_code
        == 422
    )
    assert (
        client.post(
            "/api/replay", json={"scenario_id": "02", "mode": "positive", "target": "anything"}
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/api/replay",
            json={"scenario_id": "02", "mode": "positive"},
            headers={"Origin": "http://example.invalid"},
        ).status_code
        == 403
    )
    assert (
        client.post("/api/replay", content="{}", headers={"Content-Type": "text/plain"}).status_code
        == 415
    )
    assert client.get("/api/health", headers={"Host": "example.invalid"}).status_code == 400
    assert client.get("/api/runs").json() == []
