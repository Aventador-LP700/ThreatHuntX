import json
import os
from pathlib import Path

from .detect import correlate
from .evaluation import fixture_result, summarize
from .ingest import parse
from .models import Event, Mode, Scenario

ROOT = Path(os.getenv("THREATHUNTX_ROOT", Path(__file__).resolve().parents[2]))


class Catalog:
    def __init__(self, root: Path = ROOT):
        self.root = root
        directory = root / "scenarios"
        self.attack = json.loads((directory / "attack" / "version.json").read_text())
        self.scenarios = {}
        self.fixtures: dict[tuple[str, Mode], list[Event]] = {}
        for path in sorted((directory / "manifests").glob("*.json")):
            scenario = Scenario.model_validate_json(path.read_text())
            if scenario.id in self.scenarios or scenario.rule.id != f"THX-{scenario.id}":
                raise ValueError(f"Invalid or duplicate scenario ID: {path}")
            self.scenarios[scenario.id] = scenario
            for mode in ["baseline", "positive", "negative"]:
                fixture = f"scenarios/fixtures/{scenario.id}.{mode}.json"
                rows = json.loads((root / fixture).read_text())
                events = [parse(raw, scenario, fixture) for raw in rows]
                if not events or len(events) != len({event.record_id for event in events}):
                    raise ValueError(f"Empty fixture or duplicate record IDs: {fixture}")
                self.fixtures[scenario.id, mode] = events
        if not self.scenarios:
            raise ValueError("No scenario manifests found")
        self.validation = self.evaluate()

    def evaluate(self) -> dict:
        cases = []
        for scenario in self.scenarios.values():
            for mode in ["positive", "negative", "baseline"]:
                alerts = correlate(scenario, self.fixtures[scenario.id, mode], "check")
                result = fixture_result(scenario, mode, self.fixtures[scenario.id, mode], alerts)
                cases.append(
                    {
                        key: value
                        for key, value in result.items()
                        if key not in {"event_count", "matched_records"}
                    }
                )
        return {
            "dataset": "Bundled synthetic fixture batches",
            "cases": cases,
            "metrics": summarize(cases),
        }
