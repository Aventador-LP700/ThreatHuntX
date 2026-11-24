import argparse
import json
import os
from pathlib import Path

from .catalog import Catalog
from .store import Store


def main():
    parser = argparse.ArgumentParser(description="Inspect or reset the local synthetic lab.")
    parser.add_argument("command", choices=["seed", "reset", "verify"])
    args = parser.parse_args()
    catalog = Catalog()
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
