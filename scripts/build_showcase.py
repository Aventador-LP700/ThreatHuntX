"""Write a deterministic, read-only snapshot using the actual Community Lab runtime."""

import argparse
import json
import shutil
from pathlib import Path

from app.catalog import ROOT, Catalog
from app.evaluation import MODES, evaluate_trial
from app.exports import sample_run
from app.portability import artifact, artifact_kinds, present_scenario


def snapshot(catalog: Catalog):
    assets = {}
    runs = {}
    trials = {}
    for scenario in catalog.scenarios.values():
        trials[scenario.id] = evaluate_trial(scenario, catalog.fixtures)
        for mode in MODES:
            run = sample_run(scenario, mode, catalog.fixtures[scenario.id, mode])
            runs[run["id"]] = run
        for kind in artifact_kinds(catalog.root, scenario.id):
            key = "wazuh" if kind == "wazuh" else f"{scenario.id}-{kind}"
            if key not in assets:
                assets[key] = artifact(catalog.root, scenario.id, kind)
    return {
        "catalog": {
            "attack": catalog.attack,
            "scenarios": [present_scenario(catalog.root, s) for s in catalog.scenarios.values()],
        },
        "coverage": catalog.validation,
        "trials": trials,
        "runs": runs,
        "artifacts": assets,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    catalog = Catalog()
    args.directory.mkdir(parents=True, exist_ok=True)
    content = snapshot(catalog)
    (args.directory / "snapshot.json").write_text(
        json.dumps(
            content,
            ensure_ascii=False,
            separators=(",", ":"),
            default=lambda model: model.model_dump(mode="json"),
        )
        + "\n"
    )
    (args.directory / ".nojekyll").touch()
    licenses = args.directory / "licenses"
    licenses.mkdir(exist_ok=True)
    for source in [
        ROOT / "LICENSE",
        ROOT / "THIRD_PARTY_NOTICES.md",
        *(ROOT / "docs/licenses").glob("*.txt"),
    ]:
        shutil.copyfile(source, licenses / source.name)


if __name__ == "__main__":
    main()
