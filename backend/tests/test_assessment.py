import json

import pytest
from app.cli import main


def test_assess_catalog_exports_all_fixture_decisions(capsys, monkeypatch, tmp_path):
    database = tmp_path / "unopened.sqlite"
    monkeypatch.setenv("THREATHUNTX_DB", str(database))
    assert main(["lab", "--format", "json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["synthetic_only"] and report["passed"]
    assert report["trial_summary"] is None
    assert report["published_summary"]["passed"] == report["published_summary"]["total"] == 120
    assert [scenario["id"] for scenario in report["scenarios"]] == [
        f"{i:02d}" for i in range(1, 41)
    ]
    mfa = report["scenarios"][1]
    positive, baseline, noisy = mfa["published_rule"]["checks"]
    assert positive["fixture"] == "scenarios/fixtures/02.positive.json"
    assert len(positive["matched_records"]) == 3
    assert not baseline["actual"] and not noisy["actual"]
    assert not database.exists()


def test_threshold_regression_writes_failed_check_without_changing_published_rule(capsys):
    assert main(["lab", "02", "--threshold", "4", "--format", "json"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert not report["passed"]
    assert report["published_summary"]["passed"] == 3
    assert report["trial_summary"]["fn"] == 1
    mfa = report["scenarios"][0]
    assert mfa["published_rule"]["settings"]["threshold"] == 3
    assert mfa["threshold_trial"]["settings"]["threshold"] == 4

    assert main(["lab", "02", "--threshold", "3"]) == 0
    markdown = capsys.readouterr().out
    assert "Threshold trial passed 3 of 3 fixture checks" in markdown
    assert "## 02 · MFA Fatigue" in markdown
    assert "**Prevention.**" in markdown


@pytest.mark.parametrize("args", [["00"], ["all", "--threshold", "4"], ["02", "--threshold", "31"]])
def test_assessment_rejects_invalid_cli_args(args):
    with pytest.raises(SystemExit) as error:
        main(["lab", *args])
    assert error.value.code == 2
