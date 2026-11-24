"""Render portable rule and query files from the reviewed local definitions."""

import argparse
import json
import xml.etree.ElementTree as et
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import yaml
from app.catalog import ROOT, Catalog
from app.models import Event, Predicate, Scenario

SIGMA_SOURCE = {
    "identity": {"product": "azure", "service": "signinlogs"},
    "mail": {"category": "email"},
    "windows": {"product": "windows"},
    "linux": {"product": "linux", "service": "auditd"},
    "network": {"category": "network_connection"},
    "cloud": {"product": "aws", "service": "cloudtrail"},
    "github": {"product": "github", "service": "audit"},
    "kubernetes": {"product": "kubernetes", "service": "audit"},
    "saas": {"category": "application"},
    "scanner": {"category": "application"},
}
SIGMA_MODIFIER = {
    "contains": "|contains",
    "starts_with": "|startswith",
    "ends_with": "|endswith",
    "gte": "|gte",
}


def field_name(field: str) -> str:
    return "THX" + "".join(part.title() for part in field.removeprefix("observables.").split("_"))


def sigma_documents(scenario: Scenario) -> list[dict]:
    rule = scenario.rule
    key = f"threathuntx_{scenario.id}"
    tags = [f"attack.{scenario.attack.id.lower()}"]
    selection = {"THXSource": rule.source}
    selection.update(
        {field_name(p.field) + SIGMA_MODIFIER.get(p.op, ""): p.value for p in rule.match}
    )
    detection = {"selection": selection, "condition": "selection"}
    if rule.suppress_when:
        detection.update(
            {
                f"filter_{i}": {field_name(p.field) + SIGMA_MODIFIER.get(p.op, ""): p.value}
                for i, p in enumerate(rule.suppress_when)
            }
        )
        detection["condition"] = "selection and not 1 of filter_*"
    logsource = SIGMA_SOURCE[rule.source]
    if rule.source == "windows":
        if scenario.id == "06":
            logsource = {"product": "windows", "service": "powershell"}
        elif scenario.id in {"09", "10", "12", "17", "38"}:
            logsource = {"product": "windows", "service": "sysmon"}
        elif scenario.id in {"13", "14"}:
            logsource = {"product": "windows", "service": "security"}
    base = {
        "title": f"{scenario.title} observation",
        "name": key,
        "id": str(uuid5(NAMESPACE_URL, f"https://threathuntx.invalid/rule/{key}")),
        "status": "test",
        "description": scenario.hypothesis,
        "references": [scenario.reference],
        "author": "ThreatHuntX contributors",
        "license": "MIT",
        "tags": tags,
        "logsource": {
            **logsource,
            "definition": f"{scenario.telemetry}; ThreatHuntX normalized field mapping required",
        },
        "detection": detection,
        "falsepositives": [scenario.false_positive],
        "level": rule.severity,
    }
    if rule.threshold == 1:
        return [base]
    condition = {"gte": rule.threshold}
    if rule.distinct:
        condition["field"] = field_name(rule.distinct)
    return [
        base,
        {
            "title": f"{scenario.title} correlation",
            "id": str(uuid5(NAMESPACE_URL, f"https://threathuntx.invalid/rule/{key}/correlation")),
            "status": "test",
            "description": scenario.evidence,
            "references": [scenario.reference],
            "tags": tags,
            "correlation": {
                "type": "value_count" if rule.distinct else "event_count",
                "rules": [key],
                "group-by": [field_name(rule.group_by)],
                "timespan": f"{rule.window_seconds // 60}m"
                if rule.window_seconds % 60 == 0
                else f"{rule.window_seconds}s",
                "condition": condition,
            },
            "level": rule.severity,
        },
    ]


def regex_escape(text: str) -> str:
    return "".join("\\" + char if char in r"\.^$|?*+()[]{}" else char for char in text)


def regex_value(value) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return regex_escape(str(value))


def wazuh_regex(predicate: Predicate) -> str:
    text = regex_value(predicate.value)
    match predicate.op:
        case "eq":
            return f"(?i)^{text}$"
        case "in":
            alternatives = "|".join(regex_value(item) for item in predicate.value)
            return f"(?i)^(?:{alternatives})$"
        case "contains":
            return f"(?i){text}"
        case "starts_with":
            return f"(?i)^{text}"
        case "ends_with":
            return f"(?i){text}$"
    raise ValueError(f"Wazuh event examples do not support {predicate.op}")


def wazuh_documents(scenarios: list[Scenario]) -> tuple[str, str]:
    decoder = et.Element("decoder", {"name": "threathuntx_json"})
    et.SubElement(decoder, "type").text = "syslog"
    et.SubElement(decoder, "prematch", {"type": "pcre2"}).text = r"^THX_JSON\s+"
    et.SubElement(decoder, "plugin_decoder", {"offset": "after_prematch"}).text = "JSON_Decoder"
    rules = et.Element("group", {"name": "threathuntx,synthetic,"})
    base = et.SubElement(rules, "rule", {"id": "100100", "level": "0"})
    et.SubElement(base, "decoded_as").text = "threathuntx_json"
    et.SubElement(
        base, "field", {"name": "lab_format", "type": "pcre2"}
    ).text = r"^threathuntx\.normalized\.v1$"
    et.SubElement(base, "description").text = "ThreatHuntX synthetic envelope"
    for scenario in scenarios:
        rule = scenario.rule
        child = et.SubElement(
            rules,
            "rule",
            {
                "id": str(100100 + int(scenario.id)),
                "level": {"low": "4", "medium": "7", "high": "10"}[rule.severity],
            },
        )
        et.SubElement(child, "if_sid").text = "100100"
        et.SubElement(
            child, "field", {"name": "THXSource", "type": "pcre2"}
        ).text = f"^{rule.source}$"
        for predicate in rule.match:
            et.SubElement(
                child, "field", {"name": field_name(predicate.field), "type": "pcre2"}
            ).text = wazuh_regex(predicate)
        for predicate in rule.suppress_when:
            et.SubElement(
                child,
                "field",
                {"name": field_name(predicate.field), "type": "pcre2", "negate": "yes"},
            ).text = wazuh_regex(predicate)
        et.SubElement(
            child, "description"
        ).text = f"THX {scenario.id} {scenario.title} event candidate"
        mitre = et.SubElement(child, "mitre")
        et.SubElement(mitre, "id").text = scenario.attack.id
    et.indent(decoder, space="  ")
    et.indent(rules, space="  ")
    return et.tostring(decoder, encoding="unicode") + "\n", et.tostring(
        rules, encoding="unicode"
    ) + "\n"


def projection(event: Event, fields: set[str]) -> dict:
    projected = {
        "lab_format": "threathuntx.normalized.v1",
        "TimeGenerated": event.event_timestamp.isoformat(),
        "THXSource": event.source,
        "THXRecordId": event.record_id,
    }
    return projected | {field_name(field): event.detection_field(field) for field in sorted(fields)}


def rule_fields(scenario: Scenario) -> set[str]:
    rule = scenario.rule
    return {
        rule.group_by,
        *(item.field for item in rule.match + rule.suppress_when),
        *([rule.distinct] if rule.distinct else []),
    }


def kql_predicate(p: Predicate) -> str:
    key = field_name(p.field)
    value = json.dumps(p.value, ensure_ascii=False)
    if p.op == "in":
        op = "in~" if isinstance(p.value[0], str) else "in"
        return f"{key} {op} ({', '.join(json.dumps(v, ensure_ascii=False) for v in p.value)})"
    operator = {
        "eq": "=~" if isinstance(p.value, str) else "==",
        "contains": "contains",
        "starts_with": "startswith",
        "ends_with": "endswith",
        "gte": ">=",
    }[p.op]
    return f"{key} {operator} {value}"


def spl_predicate(p: Predicate) -> str:
    key = field_name(p.field)
    if p.op == "gte":
        return f"tonumber({key}) >= {p.value}"
    if p.op == "in":
        values = ", ".join(json.dumps(str(v).lower(), ensure_ascii=False) for v in p.value)
        return f"in(lower(tostring({key})), {values})"
    value = str(p.value).lower()
    field = f"lower(tostring({key}))"
    if p.op == "eq":
        return f"{field} = {json.dumps(value, ensure_ascii=False)}"
    pattern = regex_value(value)
    if p.op == "starts_with":
        pattern = "^" + pattern
    if p.op == "ends_with":
        pattern += "$"
    return f"match({field}, {json.dumps(pattern, ensure_ascii=False)})"


def queries(scenario: Scenario) -> tuple[str, str]:
    rule = scenario.rule
    kql = [
        f"// {rule.id} {scenario.title} | Review-only. Custom normalized schema.",
        "THXNormalized_CL",
        f'| where THXSource == "{rule.source}"',
    ]
    spl = [
        f'index=threathuntx sourcetype="thx:normalized:json" THXSource="{rule.source}"',
        "| where " + " AND ".join(f"({spl_predicate(p)})" for p in rule.match),
    ]
    kql.extend(f"| where {kql_predicate(p)}" for p in rule.match)
    kql.extend(f"| where not(coalesce(({kql_predicate(p)}), false))" for p in rule.suppress_when)
    spl.extend(f"| where NOT coalesce(({spl_predicate(p)}), false())" for p in rule.suppress_when)
    if rule.threshold > 1:
        group = field_name(rule.group_by)
        distinct = field_name(rule.distinct) if rule.distinct else None
        kql_count = f"dcount({distinct})" if distinct else "count()"
        spl_count = f"dc({distinct})" if distinct else "count"
        kql.extend(
            [
                f"| summarize Observations={kql_count}, Evidence=make_set(THXRecordId, 100) by {group}, bin(TimeGenerated, {rule.window_seconds}s)",
                f"| where Observations >= {rule.threshold}",
            ]
        )
        spl.extend(
            [
                f"| bin _time span={rule.window_seconds}s",
                f"| stats {spl_count} AS observations values(THXRecordId) AS evidence BY _time {group}",
                f"| where observations >= {rule.threshold}",
            ]
        )
    else:
        kql.append(
            "| project TimeGenerated, THXSource, THXRecordId, "
            + ", ".join(field_name(field) for field in sorted(rule_fields(scenario)))
        )
        spl.append(
            "| table _time THXSource THXRecordId "
            + " ".join(field_name(field) for field in sorted(rule_fields(scenario)))
        )
    return "\n".join(kql) + "\n", "\n".join(spl) + "\n"


def render(catalog: Catalog) -> dict[Path, str]:
    results = {}
    scenarios = list(catalog.scenarios.values())
    for scenario in scenarios:
        results[Path(f"detections/sigma/{scenario.id}.yml")] = yaml.safe_dump_all(
            sigma_documents(scenario), sort_keys=False, allow_unicode=True
        )
    for scenario in scenarios[:15]:
        kql, spl = queries(scenario)
        results[Path(f"detections/kql/{scenario.id}.kql")] = kql
        results[Path(f"detections/spl/{scenario.id}.spl")] = spl
    wazuh_scenarios = scenarios[:20]
    decoder, rules = wazuh_documents(wazuh_scenarios)
    results[Path("detections/wazuh/decoders.xml")] = decoder
    results[Path("detections/wazuh/rules.xml")] = rules
    fields = set().union(*(rule_fields(scenario) for scenario in wazuh_scenarios))
    fixtures = []
    for scenario in wazuh_scenarios:
        for mode in ("baseline", "positive", "negative"):
            for event in catalog.fixtures[scenario.id, mode]:
                row = projection(event, fields)
                row = {key: "__missing__" if value is None else value for key, value in row.items()}
                fixtures.append(
                    "THX_JSON " + json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                )
    results[Path("detections/wazuh/synthetic.log")] = "\n".join(fixtures) + "\n"
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for relative, expected in render(Catalog()).items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_text() != expected:
                stale.append(str(relative))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    if stale:
        parser.exit(1, "Stale detection artifacts: " + ", ".join(stale) + "\n")
    print("Detection artifacts checked" if args.check else "Detection artifacts written")


if __name__ == "__main__":
    main()
