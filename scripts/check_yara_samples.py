"""Run the optional YARA engine on the two packaged text notes."""

import json
from pathlib import Path

import yara

ROOT = Path(__file__).resolve().parents[1]


def main():
    rule = yara.compile(filepath=str(ROOT / "detections/yara/training-note.yar"))
    results = {
        case: [
            match.rule
            for match in rule.match(str(ROOT / f"integrations/samples/forensics/{case}.txt"))
        ]
        for case in ("positive", "baseline")
    }
    print(
        json.dumps(
            {"engine": yara.__version__, "synthetic_only": True, "samples": results}, indent=2
        )
    )
    return 0 if results == {"positive": ["ThreatHuntX_Training_Note"], "baseline": []} else 1


if __name__ == "__main__":
    raise SystemExit(main())
