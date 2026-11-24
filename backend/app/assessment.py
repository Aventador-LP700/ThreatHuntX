"""Report the evidence and decisions from the bundled scenario exercises."""

from .catalog import Catalog
from .evaluation import TrialSettings, evaluate_trial, summarize

FIXTURE_LABELS = {"positive": "Positive", "baseline": "Clean baseline", "negative": "Noisy control"}


def assess(catalog: Catalog, scenario_ids: list[str], threshold: int | None) -> dict:
    exercises = []
    checks = []
    trial_checks = []
    for scenario_id in scenario_ids:
        scenario = catalog.scenarios[scenario_id]
        published = evaluate_trial(scenario, catalog.fixtures)
        exercise = {
            "id": scenario.id,
            "title": scenario.title,
            "domain": scenario.category,
            "attack_id": scenario.attack.id,
            "hypothesis": scenario.hypothesis,
            "response": scenario.response,
            "prevention": scenario.prevention,
            "rule_id": published["rule_id"],
            "published_rule": report_trial(published),
        }
        checks.extend(published["cases"])
        if threshold is not None:
            settings = TrialSettings(**{**published["defaults"], "threshold": threshold})
            trial = evaluate_trial(scenario, catalog.fixtures, settings)
            exercise["threshold_trial"] = report_trial(trial)
            trial_checks.extend(trial["cases"])
        exercises.append(exercise)

    return {
        "synthetic_only": True,
        "attack_version": catalog.attack["version"],
        "published_summary": summarize(checks),
        "trial_summary": summarize(trial_checks) if trial_checks else None,
        "passed": all(check["passed"] for check in [*checks, *trial_checks]),
        "scenarios": exercises,
    }


def report_trial(result: dict) -> dict:
    return {
        "settings": result["settings"],
        "checks": [
            {
                **case,
                "fixture": f"scenarios/fixtures/{case['scenario_id']}.{case['mode']}.json",
            }
            for case in result["cases"]
        ],
    }


def markdown(report: dict) -> str:
    exercises = report["scenarios"]
    lines = [
        "# ThreatHuntX scenario assessment",
        "",
        "This report evaluates bundled synthetic telemetry using the local detection engine.",
        f"Enterprise ATT&CK version {report['attack_version']}.",
        "",
        f"{len(exercises)} {'scenario' if len(exercises) == 1 else 'scenarios'} assessed.",
        "",
    ]
    for label, summary in (
        ("Published rules", report["published_summary"]),
        ("Threshold trial", report["trial_summary"]),
    ):
        if summary is not None:
            lines.append(
                f"- {label} passed {summary['passed']} of {summary['total']} fixture checks."
            )

    for exercise in exercises:
        lines.extend(
            [
                "",
                f"## {exercise['id']} · {exercise['title']}",
                "",
                f"{exercise['domain']} · `{exercise['attack_id']}` · `{exercise['rule_id']}`",
                "",
                exercise["hypothesis"],
            ]
        )
        for key, label in (
            ("published_rule", "Published rule"),
            ("threshold_trial", "Threshold trial"),
        ):
            if key not in exercise:
                continue
            trial = exercise[key]
            settings = trial["settings"]
            lines.extend(
                [
                    "",
                    f"### {label}",
                    "",
                    f"Threshold {settings['threshold']} in {settings['window_seconds']} seconds, "
                    f"grouped by `{settings['group_by']}`.",
                    "",
                    "| Fixture | Events | Expected alert | Alerts observed | Matched records | Result |",
                    "| --- | ---: | --- | ---: | --- | --- |",
                ]
            )
            for check in trial["checks"]:
                records = ", ".join(f"`{record}`" for record in check["matched_records"]) or "—"
                lines.append(
                    f"| {FIXTURE_LABELS[check['mode']]} `{check['fixture']}` | {check['event_count']} "
                    f"| {'Yes' if check['expected'] else 'No'} | {check['alerts']} | {records} "
                    f"| {'PASS' if check['passed'] else 'FAIL'} |"
                )
        lines.extend(
            [
                "",
                f"**Response.** {exercise['response']}",
                "",
                f"**Prevention.** {exercise['prevention']}",
            ]
        )
    return "\n".join(lines)
