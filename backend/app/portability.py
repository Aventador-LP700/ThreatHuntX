import hashlib
import json
from pathlib import Path
from typing import Literal

Kind = Literal["sigma", "wazuh", "kql", "spl"]
LABELS = {"sigma": "Sigma", "wazuh": "Wazuh XML", "kql": "Microsoft KQL", "spl": "Splunk SPL"}
STATUS = {
    "sigma": "Offline pySigma checks · normalized field map required",
    "wazuh": "Static-validated event selection · manager verification pending",
    "kql": "Review-only · custom KQL schema · vendor verification pending",
    "spl": "Review-only · custom Splunk sourcetype · vendor verification pending",
}


def artifact_path(root: Path, scenario_id: str, kind: Kind) -> Path | None:
    directory = root / "detections" / kind
    extensions = {"sigma": "yml", "kql": "kql", "spl": "spl"}
    if kind == "wazuh":
        return directory / "rules.xml" if int(scenario_id) <= 20 else None
    return directory / f"{scenario_id}.{extensions[kind]}"


def wazuh_engine_verified(root: Path) -> bool:
    directory = root / "detections/wazuh"
    try:
        evidence = json.loads((directory / "engine-validation.json").read_text())
        return evidence["matched_candidate_count"] == 20 and all(
            hashlib.sha256((directory / name).read_bytes()).hexdigest() == evidence["sha256"][name]
            for name in ("decoders.xml", "rules.xml", "synthetic.log")
        )
    except (OSError, KeyError, TypeError, ValueError):
        return False


def artifact(root: Path, scenario_id: str, kind: Kind) -> dict | None:
    path = artifact_path(root, scenario_id, kind)
    if path and path.is_file():
        status = STATUS[kind]
        if kind == "wazuh" and wazuh_engine_verified(root):
            status = "Wazuh 4.14.10 engine verified on synthetic records · live collector verification pending"
        return {
            "kind": kind,
            "label": LABELS[kind],
            "status": status,
            "code": path.read_text(),
        }
    return None


def artifact_kinds(root: Path, scenario_id: str) -> list[Kind]:
    return [
        kind
        for kind in LABELS
        if (path := artifact_path(root, scenario_id, kind)) and path.is_file()
    ]


def present_scenario(root: Path, scenario) -> dict:
    return scenario.model_dump(mode="json") | {"artifacts": artifact_kinds(root, scenario.id)}
