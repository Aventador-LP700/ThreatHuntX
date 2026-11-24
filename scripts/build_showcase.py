"""Write a deterministic, read-only snapshot using the actual Community Lab runtime."""

import argparse
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from app.catalog import ROOT, Catalog
from app.portability import artifact, artifact_kinds, present_scenario
from app.store import Store


def snapshot(catalog: Catalog, db: Store):
    assets = {}
    runs = {}
    for scenario in catalog.scenarios.values():
        runs[f"baseline-{scenario.id}"] = db.get(f"baseline-{scenario.id}")
        for mode in ("positive", "negative"):
            name = f"sample-{scenario.id}-{mode}"
            with db.connect() as connection:
                run = db.insert(connection, catalog, scenario, mode, name)
            # The sample timestamp is fixture provenance, independent of the build date.
            runs[name] = run | {"created_at": run["events"][0]["event_timestamp"]}
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
        "runs": runs,
        "artifacts": assets,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    catalog = Catalog()
    args.directory.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="threathuntx-showcase-") as directory:
        store = Store(Path(directory) / "showcase.db")
        store.initialize(catalog)
        content = snapshot(catalog, store)
    (args.directory / "snapshot.json").write_text(
        json.dumps(content, ensure_ascii=False, separators=(",", ":")) + "\n"
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
