# Vendor-shaped sample adapters

Run the adapter exercise from the checkout. It processes the eight bundled examples locally, checks the `Event` schema, and prints normalized JSON.

```bash
uv sync --locked
PYTHONPATH=backend uv run --locked python -m scripts.vendor_samples all
```

| Input | Native fields used | Investigation pivot and missing context |
| --- | --- | --- |
| Sysmon XML Event ID 13 | `System.TimeCreated`, `Computer`, `EventRecordID`, `EventData.Image`, `TargetObject`, `User` | Compare the registry object and originating image. An approved-software baseline or signed-image enrichment is separate evidence. |
| Linux Audit `SYSCALL` | `msg=audit(epoch:serial)`, `auid`, `exe`, `syscall`, `success`, `key` | Pivot by the audit serial and actor. A joined `PATH` record is needed to establish the object accessed. |
| Zeek `dns.log` JSON | `ts`, `uid`, `id.orig_h`, `id.resp_h`, `trans_id`, `query`, `rcode_name` | Combine UID and transaction ID, then inspect the client, resolver and query. THX anomaly labels are separate enrichments. |
| Suricata 8 EVE DNS v3 | `timestamp`, `flow_id`, `src_ip`, `dest_ip`, `dns.id`, `dns.queries[].rrname` | Use the flow and DNS question. The exercise accepts the bundled single-question EVE v3 shape. |
| AWS CloudTrail | `eventTime`, `eventName`, `eventID`, `userIdentity.arn`, `sourceIPAddress`, `requestParameters` | Trace the principal, role and policy. Approval context, policy risk, and later role use require additional audit data. |
| Entra Graph sign-in | `id`, `userPrincipalName`, `ipAddress`, `status.errorCode`, `authenticationDetails` | Review notification outcomes in the sign-in record. Counting distinct requests requires a suitable challenge identifier. The sample keeps the sign-in ID as a separate field. |
| Kubernetes Audit v1 | `auditID`, `stageTimestamp`, `verb`, `user.username`, `objectRef`, `requestObject.roleRef`, `responseStatus.code` | Join the completed action and role scope. Body fields depend on audit policy. The sample grants the ordinary `view` role. |
| GitHub organization audit | `@timestamp`, `_document_id`, `action`, `actor`, `repo`, workflow and job fields | Join the prepared job to a reviewed workflow run and commit diff. Job preparation alone establishes no permissions change. |

The inputs are synthetic examples of native record shapes. The CLI is separate from the Lite replay API. Normalized vendor examples carry fixture provenance and may lack the enrichment required by the scenario rule.

## Offline network baseline

The [training PCAP](../integrations/samples/benign-dns.pcap) contains four Ethernet frames representing two ordinary DNS query and reply pairs. Addresses use reserved documentation ranges. In an optional sensor environment, use this file in offline capture mode and compare the JSON results with the bundled projections. Pivot on `docs.training.example`, query type `A`, and transaction `4097`. The capture was parsed back locally during preparation. Zeek and Suricata outputs from the PCAP remain unverified. [Zeek DNS schema](https://docs.zeek.org/en/current/scripts/base/protocols/dns/main.zeek.html) · [Suricata EVE DNS v3](https://docs.suricata.io/en/suricata-8.0.8/output/eve/eve-json-format.html#event-type-dns)

## Static forensics sample

Run YARA against two bundled text notes. The expected evidence is one training marker match and an empty baseline result.

```bash
uv run --locked --extra forensics python -m scripts.check_yara_samples
```

Velociraptor collection enrollment, retrieval and storage remain vendor deployment checks. The YARA exercise uses its own optional lockfile extra and never executes either sample. [YARA rule](../detections/yara/training-note.yar)

## Live access boundaries

Sentinel connectors and Log Analytics ingestion may incur metered costs. Defender XDR Advanced Hunting depends on licensed tenant access and hunting permission. Typical tables include `DeviceProcessEvents`, `DeviceRegistryEvents` and `IdentityLogonEvents`, with columns such as `Timestamp`, `DeviceName`, `InitiatingProcessFileName`, `RegistryKey`, and `AccountUpn`. Compare these with the actual tenant schema and record required joins before using normalized templates. A Splunk deployment needs approved search access and a configured index or sourcetype. AWS, Entra and organization audit retrieval require owner-approved read permissions and retention settings. Review vendor quotas and pricing before connecting collectors.

[Portable detections](PORTABLE_DETECTIONS.md) · [Integration acceptance matrix](INTEGRATION_ACCEPTANCE.md) · [Analyst lab setup](full-lab-setup.md)
