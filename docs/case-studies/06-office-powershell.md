# PowerShell abuse investigation

An obfuscated PowerShell observation under an office parent warrants process-tree and document review.

The Community Lab engine evaluated the packaged evidence and linked 1 record(s) to one alert. A noisy replay yielded zero alerts. All event timestamps below come from the bundled fixture.

## Evidence timeline (UTC)

| Timestamp | Event and outcome | Evidence |
| --- | --- | --- |
| 2025-08-14T10:54:00Z | script_block · observed | [06-positive-01](../../scenarios/fixtures/06.positive.json) · Background |
| 2025-08-14T10:54:32Z | script_block · observed | [06-positive-02](../../scenarios/fixtures/06.positive.json) · Matched |

Use event 4104, parent process and script classification, then pivot to process identity and document origin.

[Local rule](../../scenarios/manifests/06.json) · [Sigma](../../detections/sigma/06.yml) · [JSON example](../../examples/06-office-powershell.json)

## Assessment and response

The synthesized script-block and office parent fields justify escalating for process-tree and document review.

Preserve script-block and process records, scope related executions and isolate if other evidence supports compromise.

## Root-cause hypothesis and mitigation

The fixture models an unexpected interpreter launch after document interaction. Verify why the office application started a script and whether the document was trusted.

Enable script block logging, AMSI integration and application control. Review Office child-process policy.

## Tuning and limitations

The noisy case uses the same observation with an approved automation marker. Scope any exemption to a verified workflow and execution identity.

The fixture uses a preclassified script event with normalized parent context. No script executes.

[Lesson](../learn/06.md) · [T1059.001](https://attack.mitre.org/techniques/T1059/001)
