# Registry autoruns investigation

A Run or RunOnce value written by a process of user-writable origin requires checking the executable and autorun target.

The Community Lab engine evaluated the packaged evidence and linked 1 record(s) to one alert. A noisy replay yielded zero alerts. All event timestamps below come from the bundled fixture.

## Evidence timeline (UTC)

| Timestamp | Event and outcome | Evidence |
| --- | --- | --- |
| 2025-08-14T11:36:00Z | registry_value_set · success | [09-positive-01](../../scenarios/fixtures/09.positive.json) · Background |
| 2025-08-14T11:36:32Z | registry_value_set · success | [09-positive-02](../../scenarios/fixtures/09.positive.json) · Matched |

Read Target Object and writer process provenance. Confirm the configured path and trace the associated logon or process events.

[Local rule](../../scenarios/manifests/09.json) · [Sigma](../../detections/sigma/09.yml) · [JSON example](../../examples/09-registry-autorun.json)

## Assessment and response

A change to a Run key written by a user-origin process warrants validating the writer and configured target before remediation.

Preserve registry and process evidence. Remove an unauthorized value with endpoint team approval, and look for related sign-ins.

## Root-cause hypothesis and mitigation

The modeled root cause is an unexpected per-user startup change. Investigate the software installer or writer provenance before classifying the endpoint.

Keep a software and autorun baseline, restrict execution from user-writable paths and monitor registry change events.

## Tuning and limitations

The noisy case has a related path and a documented approved change. Keep the approval specific to a workflow, publisher and target.

The source is a Sysmon event 13 projection with added provenance supplied by the fixture.

[Lesson](../learn/09.md) · [T1547.001](https://attack.mitre.org/techniques/T1547/001)
