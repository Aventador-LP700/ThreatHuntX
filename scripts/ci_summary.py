"""Summarize the executed checks from machine-readable artifacts."""

import argparse
import json
from pathlib import Path

from defusedxml import ElementTree


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = args.directory / "pytest.xml"
    fixtures = args.directory / "fixture-results.json"
    print("## ThreatHuntX validation\n")
    if report.is_file():
        suites = ElementTree.parse(report).getroot().findall("testsuite")
        for suite in suites:
            print(
                f"- pytest ran {suite.get('tests')} tests with {suite.get('failures')} failures, {suite.get('errors')} errors and {suite.get('skipped')} skips."
            )
    else:
        print("- pytest evidence unavailable for this run.")
    if fixtures.is_file() and fixtures.stat().st_size:
        metrics = json.loads(fixtures.read_text())["metrics"]
        print(f"- Bundled fixture checks passed {metrics['passed']} of {metrics['total']}.")
    else:
        print("- Fixture check evidence unavailable for this run.")
    print(
        "- Live SIEM, agent and provider checks are skipped in community CI. They require independent managed lab environments."
    )


if __name__ == "__main__":
    main()
