"""Render lesson references, the evidence matrix, and the shared playbooks."""

import argparse
import json
from pathlib import Path

from app.catalog import ROOT, Catalog
from app.portability import artifact_kinds


def lessons(catalog):
    rows = []
    generated = {}
    for scenario in catalog.scenarios.values():
        rule = scenario.rule
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
                f"[Manifest](../../scenarios/manifests/{scenario.id}.json) · [Positive fixture](../../scenarios/fixtures/{scenario.id}.positive.json) · [Noisy fixture](../../scenarios/fixtures/{scenario.id}.negative.json) · [Sigma](../../detections/sigma/{scenario.id}.yml)",
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
        generated[Path(f"docs/learn/{scenario.id}.md")] = "\n".join(lines)
        passed = all(
            case["passed"]
            for case in catalog.validation["cases"]
            if case["scenario_id"] == scenario.id
        )
        validation = "Synthetic-verified" if passed else "Fixture check failed"
        kinds = artifact_kinds(catalog.root, scenario.id)
        rows.append(
            f"| {scenario.id} | [{scenario.title}](learn/{scenario.id}.md) | [{scenario.attack.id}]({scenario.attack.url}) {scenario.attack.confidence} | {validation} | "
            + ("Core" if scenario.core_lesson else "Additional")
            + " | "
            + ("Static test" if "wazuh" in kinds else "—")
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
            "| ID | Lesson | Enterprise ATT&CK | Local fixture result | Guided coverage | Wazuh | KQL/SPL |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "[Status definitions](TESTING_AND_VALIDATION.md) · [Portable detections](PORTABLE_DETECTIONS.md) · [Observed test results](../reports/validation-summary.md)",
            "",
        ]
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
    result = [
        "# Ten starter hunt hypotheses",
        "",
        "Replay the positive and noisy examples in each lesson. Read the supporting and contradictory observations before proposing a response.",
        "",
    ]
    for s in catalog.scenarios.values():
        if s.core_lesson:
            result.extend(
                [
                    f"## [{s.title}](learn/{s.id}.md)",
                    "",
                    s.hypothesis,
                    "",
                    f"**Support** {s.evidence}",
                    "",
                    f"**Alternative explanation** {s.false_positive}",
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
