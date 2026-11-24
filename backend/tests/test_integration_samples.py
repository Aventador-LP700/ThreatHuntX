import json
import shutil
from pathlib import Path

import pytest
from app.models import CaseReport
from app.portability import wazuh_engine_verified
from jsonschema import Draft202012Validator, FormatChecker

from scripts.vendor_samples import SAMPLES, normalize_sample

EXPECTED = {
    "zeek-dns": ("network", "dns_query", "observed", "CFixtureDNS01-4097"),
    "suricata-dns": ("network", "dns_query", "observed", "108001-4097"),
    "aws-cloudtrail": ("cloud", "role_grant", "success", "00000000-0000-4000-8000-000000000020"),
    "entra-signin": ("identity", "mfa_challenge", "denied", "training-signin-02"),
    "kubernetes-audit": (
        "kubernetes",
        "create_binding",
        "success",
        "00000000-0000-4000-8000-000000000035",
    ),
    "github-audit": ("github", "workflow_job_prepared", "observed", "training-github-33"),
    "sysmon-registry": ("windows", "registry_value_set", "observed", "1009"),
    "linux-audit": ("linux", "audit_syscall", "success", "1008"),
}


@pytest.mark.parametrize("sample", SAMPLES)
def test_native_shaped_example_projects_to_event(catalog, sample):
    event = normalize_sample(catalog, sample)
    assert (event.source, event.action, event.outcome, event.record_id) == EXPECTED[sample]
    assert event.evidence_reference.startswith("integrations/samples/")
    assert event.synthetic and event.event_timestamp.tzinfo
    assert event.technique_id == catalog.scenarios[event.scenario_id].attack.id
    if sample in {"zeek-dns", "suricata-dns"}:
        assert str(event.source_ip) == "192.0.2.20"
        assert event.domain == "docs.training.example"
    if sample == "entra-signin":
        assert event.observables["sign_in_id"] == event.record_id
        assert "challenge_id" not in event.observables


def test_wazuh_proof_requires_exact_rule_and_fixture_bytes(catalog, tmp_path):
    source = Path(catalog.root / "detections/wazuh")
    target = tmp_path / "detections/wazuh"
    shutil.copytree(source, target)
    assert wazuh_engine_verified(tmp_path)
    evidence = json.loads((target / "engine-validation.json").read_text())
    assert len(evidence["records"]) == 138
    assert {int(record["rule_id"]) for record in evidence["records"]} == set(range(100100, 100121))
    changed = target / "rules.xml"
    changed.write_text(changed.read_text() + "\n")
    assert not wazuh_engine_verified(tmp_path)


def test_case_schema_validates_real_replay_evidence(client, catalog):
    scenario = catalog.scenarios["02"]
    run = client.get("/api/scenarios/02/fixtures/positive/export").json()
    report = CaseReport.model_validate(
        {
            "schema_version": 1,
            "synthetic_only": True,
            "case_id": run["id"],
            "scenario": {
                "id": scenario.id,
                "title": scenario.title,
                "attack": scenario.attack.model_dump(),
            },
            "rule_id": scenario.rule.id,
            "fixture_mode": run["mode"],
            "recorded_at": run["created_at"],
            "generated_at": run["created_at"],
            "analysis": {
                "hypothesis": scenario.hypothesis,
                "notes": "<strong>literal markup</strong>",
                "disposition": "investigate",
                "response": scenario.response,
                "updated_at": None,
            },
            "limitations": scenario.limitations,
            "mitigations": [scenario.prevention],
            "alerts": run["alerts"],
            "evidence": run["events"],
        }
    )
    schema = json.loads((catalog.root / "scenarios/schema/case-report-v1.json").read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(
        report.model_dump(mode="json")
    )
