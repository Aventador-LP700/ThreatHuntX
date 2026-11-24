"""Render lesson references, the evidence matrix, and the shared playbooks."""

import argparse
import json
from pathlib import Path

from app.catalog import ROOT, Catalog
from app.evaluation import evaluate_trial
from app.portability import artifact_kinds, wazuh_engine_verified


def lessons(catalog):
    rows = []
    generated = {}
    machine_rows = []
    wazuh_status = (
        "Engine verified on synthetic records"
        if wazuh_engine_verified(catalog.root)
        else "Static test"
    )
    for scenario in catalog.scenarios.values():
        rule = scenario.rule
        trial = evaluate_trial(scenario, catalog.fixtures)
        lines = [
            f"# {scenario.id} · {scenario.title}",
            "",
            scenario.overview,
            "",
            f"**Track** {scenario.difficulty} · {scenario.minutes} min · {scenario.platform}",
            "",
            f"**Prerequisites** {scenario.prerequisites}",
            "",
            "## Investigate",
            "",
            f"**Attacker intent** {scenario.objective}",
            "",
            f"**Learning outcome** {scenario.evidence}",
            "",
            f"1. Review the clean baseline. {scenario.telemetry} supplies the exercise evidence.",
            f"2. Consider the hypothesis. {scenario.hypothesis}",
            f"3. Replay the positive fixture and inspect {rule.id}. {scenario.evidence}",
            f"4. Compare the noisy fixture. {scenario.false_positive}",
            "",
            "## Rule and evidence",
            "",
            f"Count at least {rule.threshold} observation(s) per `{rule.group_by}` inside {rule.window_seconds} seconds. "
            + (
                f"Count distinct `{rule.distinct}` values."
                if rule.distinct
                else "Each distinct source record can count once."
            ),
            "",
            "| Field | Comparison | Value |",
            "| --- | --- | --- |",
        ]
        lines.extend(
            f"| `{p.field}` | `{p.op}` | `{json.dumps(p.value, ensure_ascii=False)}` |"
            for p in rule.match
        )
        if rule.suppress_when:
            lines.extend(
                ["", "Review the following event-level exclusions before changing the rule.", ""]
            )
            lines.extend(
                f"- `{p.field}` {p.op} `{json.dumps(p.value)}`" for p in rule.suppress_when
            )
        lines.extend(
            [
                "",
                f"Tuning guidance. {scenario.tuning}",
                "",
                f"[Manifest](../../scenarios/manifests/{scenario.id}.json) · [Clean fixture](../../scenarios/fixtures/{scenario.id}.baseline.json) · [Positive fixture](../../scenarios/fixtures/{scenario.id}.positive.json) · [Noisy fixture](../../scenarios/fixtures/{scenario.id}.negative.json) · [Sigma](../../detections/sigma/{scenario.id}.yml)",
            ]
        )
        if "kql" in artifact_kinds(catalog.root, scenario.id):
            lines.extend(
                [
                    "",
                    f"[KQL](../../detections/kql/{scenario.id}.kql) · [SPL](../../detections/spl/{scenario.id}.spl) · [Field mapping and platform status](../PORTABLE_DETECTIONS.md)",
                ]
            )
        lines.extend(
            [
                "",
                "## Contain and prevent",
                "",
                scenario.response,
                "",
                scenario.prevention,
                "",
                "## Knowledge check",
                "",
            ]
        )
        for item in scenario.questions:
            lines.extend(
                [
                    f"- {item.prompt}",
                    *[f"  - {option}" for option in item.options],
                    "",
                    "<details>",
                    "<summary>Answer and rationale</summary>",
                    "",
                    item.options[item.answer] + ". " + item.explanation,
                    "",
                    "</details>",
                    "",
                ]
            )
        lines.extend(
            [
                "## Validation and mapping",
                "",
                scenario.validation,
                "",
                scenario.limitations,
                "",
                f"Enterprise ATT&CK {catalog.attack['version']} · {scenario.attack.confidence}. {scenario.attack.rationale}",
                "",
                f"[{scenario.attack.id} · {scenario.attack.name}]({scenario.attack.url})",
                "",
                f"[Start the interactive lesson](http://127.0.0.1:8080/#/lesson/{scenario.id}) · [Catalog](../evidence-matrix.md) · [License](../../LICENSE)",
                "",
            ]
        )
        lines.extend(
            [
                "## Observed fixture decisions",
                "",
                "| Batch | Events | Expected alert | Observed alerts | Matched record IDs |",
                "| --- | --- | --- | --- | --- |",
                *[
                    f"| {case['mode']} | {case['event_count']} | {'Yes' if case['expected'] else 'No'} | {case['alerts']} | "
                    + (", ".join(f"`{record}`" for record in case["matched_records"]) or "—")
                    + " |"
                    for case in trial["cases"]
                ],
                "",
                "Reproduce this comparison on the loopback lab.",
                "",
                "```bash",
                f"curl -fsS http://127.0.0.1:8080/api/scenarios/{scenario.id}/trial",
                "```",
                "",
                f"[Normalized field schema](../../scenarios/schema/event-v1.json) · [Detection Studio](http://127.0.0.1:8080/#/rules/{scenario.id})",
                "",
            ]
        )
        generated[Path(f"docs/learn/{scenario.id}.md")] = "\n".join(lines)
        passed = all(
            case["passed"]
            for case in catalog.validation["cases"]
            if case["scenario_id"] == scenario.id
        )
        validation = "Synthetic-verified" if passed else "Fixture check failed"
        kinds = artifact_kinds(catalog.root, scenario.id)
        machine_rows.append(
            {
                "id": scenario.id,
                "title": scenario.title,
                "category": scenario.category,
                "attack": scenario.attack.model_dump(),
                "source": rule.source,
                "detection": rule.id,
                "telemetry": scenario.telemetry,
                "defensive_control": scenario.prevention,
                "status": validation,
                "fixture_results": trial["cases"],
                "artifact_formats": kinds,
                "lesson": f"learn/{scenario.id}.md",
            }
        )
        rows.append(
            f"| {scenario.id} | [{scenario.title}](learn/{scenario.id}.md) | [{scenario.attack.id}]({scenario.attack.url}) {scenario.attack.confidence} | {validation} | "
            + ("Core" if scenario.core_lesson else "Additional")
            + " | "
            + (wazuh_status if "wazuh" in kinds else "—")
            + " | "
            + ("Review" if "kql" in kinds else "—")
            + " |"
        )
    generated[Path("docs/evidence-matrix.md")] = "\n".join(
        [
            "# Evidence and technique coverage",
            "",
            "The local engine runs three labeled batches per scenario. The local validation column covers the bundled fixture set. All 40 scenarios have an original Sigma specification with offline pySigma and fixture-selection checks. The 10 core lessons also have dedicated browser smoke tests.",
            "",
            "[Machine-readable scenario matrix](scenario-matrix.json)",
            "",
            "| ID | Lesson | Enterprise ATT&CK | Local fixture result | Guided coverage | Wazuh | KQL/SPL |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "[Status definitions](TESTING_AND_VALIDATION.md) · [Portable detections](PORTABLE_DETECTIONS.md) · [Observed test results](../reports/validation-summary.md)",
            "",
        ]
    )
    generated[Path("docs/scenario-matrix.json")] = (
        json.dumps(
            {
                "schema_version": 1,
                "attack_release": catalog.attack["version"],
                "synthetic_only": True,
                "scenarios": machine_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    return generated


def playbooks(catalog):
    content = json.loads((ROOT / "frontend/src/content/playbooks.json").read_text())
    result = [
        "# Response playbooks",
        "",
        "Use these steps to practise evidence handling and response decisions. Scenario-specific guidance and limitations are available in the linked lessons.",
        "",
    ]
    for book in content:
        result.extend([f"## {book['title']}", "", book["scope"], "", book["trigger"], ""])
        result.extend(f"{n}. {action}" for n, action in enumerate(book["actions"], start=1))
        result.extend(
            [
                "",
                f"**Recovery** {book['recovery']}",
                "",
                " · ".join(
                    f"[{catalog.scenarios[id].title}](../learn/{id}.md)" for id in book["cases"]
                ),
                "",
            ]
        )
    result.extend(["[Safety and scope](../SAFETY_AND_SCOPE.md)", ""])
    return {Path("docs/analyst-playbooks/README.md"): "\n".join(result)}


def hypotheses(catalog):
    hunts = json.loads((ROOT / "frontend/src/content/hunts.json").read_text())
    result = [
        "# Fifteen fixture-backed hunt hypotheses",
        "",
        "Replay the positive and noisy examples in each lesson. Document support for your conclusion alongside a plausible alternative.",
        "",
    ]
    for hunt in hunts:
        scenario = catalog.scenarios[hunt["id"]]
        positive = evaluate_trial(scenario, catalog.fixtures)["cases"][0]
        ids = ", ".join(f"`{record}`" for record in positive["matched_records"])
        result.extend(
            [
                f"## [{scenario.title}](learn/{scenario.id}.md)",
                "",
                scenario.hypothesis,
                "",
                f"**Pivot** {hunt['pivot']}",
                "",
                f"**Support** {scenario.evidence} Matched records {ids}.",
                "",
                f"**Alternative** {scenario.false_positive} {hunt['check']}",
                "",
                f"[Positive](../scenarios/fixtures/{scenario.id}.positive.json) · [Noisy control](../scenarios/fixtures/{scenario.id}.negative.json)",
                "",
            ]
        )
    return {Path("docs/HUNT_HYPOTHESES.md"): "\n".join(result)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog = Catalog()
    for relative, content in (lessons(catalog) | playbooks(catalog) | hypotheses(catalog)).items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_text() != content:
                parser.exit(1, f"Stale learning document: {relative}\n")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print("Learning documents checked" if args.check else "Learning documents written")


if __name__ == "__main__":
    main()
