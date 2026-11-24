# Cloud IAM abuse investigation

A successful interactive administrative role grant warrants checking change approval and later role use.

The Community Lab engine evaluated the packaged evidence and linked 1 record(s) to one alert. A noisy replay yielded zero alerts. All event timestamps below come from the bundled fixture.

## Evidence timeline (UTC)

| Timestamp | Event and outcome | Evidence |
| --- | --- | --- |
| 2025-08-14T14:10:00Z | role_grant · success | [20-positive-01](../../scenarios/fixtures/20.positive.json) · Background |
| 2025-08-14T14:10:32Z | role_grant · success | [20-positive-02](../../scenarios/fixtures/20.positive.json) · Matched |

Identify granting actor, recipient, account, policy and the authorized deployment process.

[Local rule](../../scenarios/manifests/20.json) · [Sigma](../../detections/sigma/20.yml) · [JSON example](../../examples/20-cloud-iam-grant.json)

## Assessment and response

An interactive administrative grant merits immediate approval and downstream role-use review.

Preserve cloud audit evidence, revoke an unauthorized grant and review resource access by the recipient.

## Root-cause hypothesis and mitigation

The fixture models a privileged change outside the expected pipeline identity. Independent change and API activity evidence would determine misuse and blast radius.

Enforce least privilege, short-lived roles and change approval for administrative grants.

## Tuning and limitations

The noisy case uses a recorded break-glass context. Require a time-limited approval and retain the grant for audit.

This is a normalized cloud audit projection. Provider actions and effective permissions require separate verification.

[Lesson](../learn/20.md) · [T1098.003](https://attack.mitre.org/techniques/T1098/003)
