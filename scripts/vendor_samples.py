"""Read bundled vendor-shaped examples without contacting vendor services."""

import argparse
import json
import re
import shlex
from datetime import UTC, datetime
from pathlib import Path

from app.catalog import ROOT, Catalog
from app.models import Event
from defusedxml import ElementTree

SAMPLES = {
    "zeek-dns": ("zeek-dns.json", "19"),
    "suricata-dns": ("suricata-dns.json", "19"),
    "aws-cloudtrail": ("aws-cloudtrail.json", "20"),
    "entra-signin": ("entra-signin.json", "02"),
    "kubernetes-audit": ("kubernetes-audit.json", "35"),
    "github-audit": ("github-audit.json", "33"),
    "sysmon-registry": ("sysmon-registry.xml", "09"),
    "linux-audit": ("linux-audit.log", "08"),
}


def utc_epoch(value):
    return datetime.fromtimestamp(value, tz=UTC)


def zeek(data):
    return {
        "event_timestamp": utc_epoch(data["ts"]),
        "source": "network",
        "host": "training-zeek",
        "event_id": "dns",
        "record_id": f"{data['uid']}-{data['trans_id']}",
        "action": "dns_query",
        "outcome": "observed",
        "source_ip": data["id.orig_h"],
        "destination_ip": data["id.resp_h"],
        "domain": data["query"],
        "observables": {"query_type": data["qtype_name"], "response_code": data["rcode_name"]},
    }


def suricata(data):
    dns = data["dns"]
    if data["event_type"] != "dns" or dns["version"] != 3 or len(dns["queries"]) != 1:
        raise ValueError("Expected an EVE DNS v3 record with one question.")
    query = dns["queries"][0]
    return {
        "event_timestamp": data["timestamp"],
        "source": "network",
        "host": "training-suricata",
        "event_id": "dns",
        "record_id": f"{data['flow_id']}-{dns['id']}",
        "action": "dns_query",
        "outcome": "observed",
        "source_ip": data["src_ip"],
        "destination_ip": data["dest_ip"],
        "domain": query["rrname"],
        "observables": {"query_type": query["rrtype"], "message_type": dns["type"]},
    }


def aws(data):
    return {
        "event_timestamp": data["eventTime"],
        "source": "cloud",
        "host": data["recipientAccountId"],
        "user": data["userIdentity"]["arn"],
        "event_id": data["eventName"],
        "record_id": data["eventID"],
        "action": "role_grant",
        "outcome": "failure" if data.get("errorCode") else "success",
        "source_ip": data["sourceIPAddress"],
        "observables": {
            "event_source": data["eventSource"],
            "role": data["requestParameters"]["roleName"],
            "policy": data["requestParameters"]["policyArn"],
        },
    }


def entra(data):
    step = next(
        part
        for part in data["authenticationDetails"]
        if part["authenticationMethod"] == "Mobile app notification"
    )
    succeeded = step["succeeded"]
    denied = "denied" in step["authenticationStepResultDetail"].casefold()
    return {
        "event_timestamp": step["authenticationStepDateTime"],
        "source": "identity",
        "host": data["appDisplayName"],
        "user": data["userPrincipalName"],
        "event_id": "mobile-app-notification",
        "record_id": data["id"],
        "action": "mfa_challenge",
        "outcome": "success" if succeeded else "denied" if denied else "failure",
        "source_ip": data["ipAddress"],
        "observables": {
            "auth_method": "push",
            "sign_in_id": data["id"],
            "status_code": data["status"]["errorCode"],
        },
    }


def kubernetes(data):
    if data["kind"] != "Event" or data["stage"] != "ResponseComplete" or data["verb"] != "create":
        raise ValueError("Expected the completed create-binding sample.")
    return {
        "event_timestamp": data["stageTimestamp"],
        "source": "kubernetes",
        "host": "training-cluster",
        "user": data["user"]["username"],
        "event_id": data["verb"],
        "record_id": data["auditID"],
        "action": "create_binding",
        "outcome": "success" if 200 <= data["responseStatus"]["code"] < 300 else "failure",
        "source_ip": data["sourceIPs"][0],
        "observables": {
            "resource": data["objectRef"]["resource"],
            "binding": data["objectRef"]["name"],
            "role_ref": data["requestObject"]["roleRef"]["name"],
        },
    }


def github(data):
    return {
        "event_timestamp": utc_epoch(data["@timestamp"] / 1000),
        "source": "github",
        "host": data["repo"],
        "user": data["actor"],
        "event_id": data["action"],
        "record_id": data["_document_id"],
        "action": "workflow_job_prepared",
        "outcome": "observed",
        "observables": {
            "workflow": data["workflow_name"],
            "job": data["job_name"],
            "branch": data["head_branch"],
        },
    }


def sysmon(text):
    namespace = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}
    root = ElementTree.fromstring(text)
    system = root.find("e:System", namespace)
    if system is None or system.findtext("e:EventID", namespaces=namespace) != "13":
        raise ValueError("Expected a Sysmon registry event ID 13.")
    fields = {
        item.attrib["Name"]: item.text for item in root.findall("e:EventData/e:Data", namespace)
    }
    return {
        "event_timestamp": system.find("e:TimeCreated", namespace).attrib["SystemTime"],
        "source": "windows",
        "host": system.findtext("e:Computer", namespaces=namespace),
        "user": fields["User"],
        "process": fields["Image"],
        "event_id": "13",
        "record_id": system.findtext("e:EventRecordID", namespaces=namespace),
        "action": "registry_value_set",
        "outcome": "observed",
        "observables": {
            "target_object": fields["TargetObject"],
            "registry_event_type": fields["EventType"],
        },
    }


def audit(text):
    match = re.fullmatch(r"type=SYSCALL msg=audit\(([\d.]+):(\d+)\): (.*)", text.strip())
    if match is None:
        raise ValueError("Expected a Linux audit SYSCALL record.")
    epoch, serial, attrs = match.groups()
    fields = dict(entry.split("=", 1) for entry in shlex.split(attrs))
    return {
        "event_timestamp": utc_epoch(float(epoch)),
        "source": "linux",
        "host": "training-linux",
        "user": fields["auid"],
        "process": fields["exe"],
        "event_id": "SYSCALL",
        "record_id": serial,
        "action": "audit_syscall",
        "outcome": "success" if fields["success"] == "yes" else "failure",
        "observables": {"syscall": fields["syscall"], "audit_key": fields["key"]},
    }


PARSERS = {
    "zeek-dns": zeek,
    "suricata-dns": suricata,
    "aws-cloudtrail": aws,
    "entra-signin": entra,
    "kubernetes-audit": kubernetes,
    "github-audit": github,
    "sysmon-registry": sysmon,
    "linux-audit": audit,
}


def normalize_sample(catalog: Catalog, name: str) -> Event:
    filename, scenario_id = SAMPLES[name]
    relative = Path("integrations/samples") / filename
    raw = (catalog.root / relative).read_text()
    record = PARSERS[name](json.loads(raw) if relative.suffix == ".json" else raw)
    return Event.model_validate(
        record
        | {
            "scenario_id": scenario_id,
            "technique_id": catalog.scenarios[scenario_id].attack.id,
            "evidence_reference": relative.as_posix(),
            "synthetic": True,
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample", choices=(*SAMPLES, "all"))
    args = parser.parse_args()
    catalog = Catalog(ROOT)
    names = SAMPLES if args.sample == "all" else [args.sample]
    print(
        json.dumps(
            {name: normalize_sample(catalog, name).model_dump(mode="json") for name in names},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
