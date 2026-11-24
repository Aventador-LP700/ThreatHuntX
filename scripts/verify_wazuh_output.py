"""Check native Wazuh event selections and keep only sanitized result IDs."""

import argparse
import hashlib
import json
import re
import sys

from app.catalog import ROOT, Catalog
from app.detect import matches

ENGINE_FILES = ("decoders.xml", "rules.xml", "synthetic.log")


def verify(raw: str, catalog: Catalog):
    directory = catalog.root / "detections/wazuh"
    ids = [
        json.loads(line.removeprefix("THX_JSON "))["THXRecordId"]
        for line in (directory / "synthetic.log").read_text().splitlines()
    ]
    records = {
        event.record_id: event
        for (scenario_id, _), events in catalog.fixtures.items()
        if int(scenario_id) <= 20
        for event in events
    }
    results = []
    observed_rules = set()
    for block in raw.split("**Phase 1: Completed pre-decoding.")[1:]:
        decoder = re.search(r"(?m)^\s+decoder: '([^']+)'", block)
        record = re.search(r"(?m)^\s+THXRecordId: '([^']+)'", block)
        rule = re.search(r"(?m)^\s+Rule id: '(\d+)'", block)
        if not decoder or not record or not rule or decoder[1] != "threathuntx_json":
            raise ValueError("Wazuh did not decode and classify a bundled record.")
        event = records[record[1]]
        expected = sorted(
            str(100100 + int(scenario.id))
            for scenario in list(catalog.scenarios.values())[:20]
            if event.source == scenario.rule.source
            and all(matches(event, predicate) for predicate in scenario.rule.match)
            and not any(matches(event, predicate) for predicate in scenario.rule.suppress_when)
        ) or ["100100"]
        if rule[1] not in expected:
            raise ValueError(f"{record[1]} selected rule {rule[1]}; expected {expected}.")
        if rule[1] != "100100":
            observed_rules.add(rule[1])
        results.append(
            {
                "record_id": record[1],
                "decoder": decoder[1],
                "rule_id": rule[1],
                "expected_candidates": expected,
            }
        )
    if [result["record_id"] for result in results] != ids:
        raise ValueError("Wazuh result sequence does not match the bundled input.")
    if observed_rules != {str(value) for value in range(100101, 100121)}:
        raise ValueError(
            f"Expected each candidate rule to trigger; observed {sorted(observed_rules)}."
        )
    if re.search(r"(?m)wazuh-testrule: (?:ERROR|CRITICAL):", raw):
        raise ValueError("Wazuh reported an engine error.")
    return {
        "engine": "Wazuh 4.14.10 wazuh-logtest-legacy",
        "scope": "isolated engine with bundled synthetic records",
        "sha256": {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in ENGINE_FILES
        },
        "record_count": len(results),
        "matched_candidate_count": len(observed_rules),
        "records": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="Wazuh 4.14.10 bundled test")
    parser.parse_args()
    print(json.dumps(verify(sys.stdin.read(), Catalog(ROOT)), indent=2))


if __name__ == "__main__":
    main()
