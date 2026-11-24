import json
import os
from pathlib import Path

from .detect import correlate
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
                expected = mode == "positive"
                actual = bool(alerts)
                cases.append(
                    {
                        "scenario_id": scenario.id,
                        "mode": mode,
                        "expected": expected,
                        "actual": actual,
                        "alerts": len(alerts),
                        "passed": actual == expected,
                    }
                )
        tp = sum(case["expected"] and case["actual"] for case in cases)
        fp = sum(not case["expected"] and case["actual"] for case in cases)
        tn = sum(not case["expected"] and not case["actual"] for case in cases)
        fn = sum(case["expected"] and not case["actual"] for case in cases)
        return {
            "dataset": "Bundled synthetic fixture batches",
            "cases": cases,
            "metrics": {
                "tp": tp,
                "fp": fp,
                "tn": tn,
                "fn": fn,
                "precision": tp / (tp + fp) if tp + fp else None,
                "recall": tp / (tp + fn) if tp + fn else None,
                "passed": tp + tn,
                "total": len(cases),
                "pass_rate": (tp + tn) / len(cases),
            },
        }
