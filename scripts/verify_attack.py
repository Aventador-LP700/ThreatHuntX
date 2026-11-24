"""Validate bundled mappings. Supply a pinned offline STIX file for an upstream comparison."""

import argparse
import json
from pathlib import Path

from app.catalog import Catalog


def check(catalog: Catalog, stix: Path | None = None):
    expected = json.loads((catalog.root / "scenarios/attack/techniques.json").read_text())
    tactics = {tactic["id"] for tactic in catalog.attack["tactics"]}
    assert set(expected) == {scenario.attack.id for scenario in catalog.scenarios.values()}
    for scenario in catalog.scenarios.values():
        mapping = scenario.attack
        assert mapping.model_dump(exclude={"confidence", "rationale"}) == expected[mapping.id]
        assert set(mapping.tactics).issubset(tactics)
        suffix = mapping.id.replace(".", "/")
        assert mapping.url == f"https://attack.mitre.org/techniques/{suffix}"
    if stix:
        objects = json.loads(stix.read_text())["objects"]
        release = next(obj for obj in objects if obj["type"] == "x-mitre-collection")
        assert release["x_mitre_version"] == catalog.attack["version"]
        active = {}
        for obj in objects:
            if (
                obj["type"] != "attack-pattern"
                or obj.get("revoked")
                or obj.get("x_mitre_deprecated")
            ):
                continue
            ref = next(
                item for item in obj["external_references"] if item["source_name"] == "mitre-attack"
            )
            key = ref["external_id"]
            if key in expected:
                active[key] = {
                    "id": key,
                    "name": obj["name"],
                    "url": ref["url"],
                    "tactics": sorted(
                        {
                            phase["phase_name"].replace("-", "_")
                            for phase in obj["kill_chain_phases"]
                        }
                    ),
                }
        assert active == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stix", type=Path)
    options = parser.parse_args()
    catalog = Catalog()
    check(catalog, options.stix)
    print(
        f"{len(catalog.scenarios)} mappings checked against "
        + ("upstream STIX" if options.stix else "bundled MITRE subset")
    )


if __name__ == "__main__":
    main()
