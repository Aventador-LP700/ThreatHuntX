"""Export Pydantic validation contracts as JSON Schema."""

import argparse
import json

from app.catalog import ROOT
from app.ingest import Raw
from app.models import CaseReport, Event, Scenario


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name, model in {
        "event-v1": Event,
        "case-report-v1": CaseReport,
        "scenario-v1": Scenario,
        "fixture-record-v1": Raw,
    }.items():
        path = ROOT / "scenarios" / "schema" / f"{name}.json"
        expected = json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n"
        if args.check:
            if path.read_text() != expected:
                parser.exit(1, f"Stale JSON Schema: {path.name}\n")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    print("JSON Schemas checked" if args.check else "JSON Schemas written")


if __name__ == "__main__":
    main()
