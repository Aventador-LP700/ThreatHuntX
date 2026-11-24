import argparse
import json
import os
from pathlib import Path

from .assessment import assess, markdown
from .catalog import Catalog
from .store import Store


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="Run, verify or reset the local synthetic lab.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("seed", help="Seed the SQLite database with clean baselines.")
    commands.add_parser("reset", help="Reset the SQLite database to clean baselines.")
    commands.add_parser("verify", help="Report default fixture check results as JSON.")
    lab = commands.add_parser("lab", help="Run scenario exercises and write a report to stdout.")
    lab.add_argument("scenario", nargs="?", default="all", help="Scenario ID such as 02, or all.")
    lab.add_argument("--format", choices=["markdown", "json"], default="markdown")
    lab.add_argument(
        "--threshold", type=int, help="Compare a temporary threshold for one scenario."
    )
    args = parser.parse_args(argv)
    catalog = Catalog()
    if args.command == "lab":
        if args.scenario != "all" and args.scenario not in catalog.scenarios:
            lab.error("Select a scenario ID from the catalog, such as 02, or use all.")
        if args.threshold is not None and (args.scenario == "all" or not 1 <= args.threshold <= 30):
            lab.error("--threshold requires one scenario ID and a value from 1 to 30.")
        selected = list(catalog.scenarios) if args.scenario == "all" else [args.scenario]
        report = assess(catalog, selected, args.threshold)
        print(json.dumps(report, indent=2) if args.format == "json" else markdown(report))
        return int(not report["passed"])
    if args.command == "verify":
        print(json.dumps(catalog.validation, indent=2))
        return int(
            catalog.validation["metrics"]["passed"] != catalog.validation["metrics"]["total"]
        )
    store = Store(Path(os.getenv("THREATHUNTX_DB", "var/lab.sqlite")))
    store.initialize(catalog)
    if args.command == "reset":
        store.reset(catalog)
    print(f"{len(catalog.scenarios)} synthetic baselines available in {store.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
