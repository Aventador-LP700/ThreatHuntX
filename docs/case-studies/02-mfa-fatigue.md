# MFA fatigue investigation

Three distinct denied push prompts for one user within five minutes warrant investigation.

The Community Lab engine evaluated the packaged evidence and linked 3 record(s) to one alert. A noisy replay yielded zero alerts. All event timestamps below come from the bundled fixture.

## Evidence timeline (UTC)

| Timestamp | Event and outcome | Evidence |
| --- | --- | --- |
| 2025-08-14T09:58:00Z | mfa_challenge · success | [02-positive-01](../../scenarios/fixtures/02.positive.json) · Background |
| 2025-08-14T09:58:32Z | mfa_challenge · denied | [02-positive-02](../../scenarios/fixtures/02.positive.json) · Matched |
| 2025-08-14T09:59:04Z | mfa_challenge · denied | [02-positive-03](../../scenarios/fixtures/02.positive.json) · Matched |
| 2025-08-14T09:59:36Z | mfa_challenge · denied | [02-positive-04](../../scenarios/fixtures/02.positive.json) · Matched |

Confirm the user, method and outcome. Three distinct challenge IDs within five minutes link the alert to individual requests.

[Local rule](../../scenarios/manifests/02.json) · [Sigma](../../detections/sigma/02.yml) · [JSON example](../../examples/02-mfa-fatigue.json)

## Assessment and response

A series of push denials on one fictional user merits account-pressure triage. The positive batch contains no approval or successful push.

Contact the user through a trusted channel. If a prompt was unexpectedly approved, revoke sessions and review subsequent sign-ins.

## Root-cause hypothesis and mitigation

The fixture models unsolicited repeated prompts. The audit evidence establishes three distinct denials. Establishing the origin or scope of any real account access would require sign-in and session context.

Require phishing-resistant MFA where possible. Enable number matching and authentication throttling for remaining push users.

## Tuning and limitations

The noisy control repeats one challenge and includes an approved enrollment event. It illustrates deduplication and explicit change context.

The sample records prompt denials. Confirming account compromise requires independent sign-in and session evidence.

[Lesson](../learn/02.md) · [T1621](https://attack.mitre.org/techniques/T1621)
