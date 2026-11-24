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


def artifact(root: Path, scenario_id: str, kind: Kind) -> dict | None:
    path = artifact_path(root, scenario_id, kind)
    if path and path.is_file():
        return {
            "kind": kind,
            "label": LABELS[kind],
            "status": STATUS[kind],
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
