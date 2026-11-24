# Fifteen fixture-backed hunt hypotheses

Replay the positive and noisy examples in each lesson. Document support for your conclusion alongside a plausible alternative.

## [Phishing](learn/01.md)

A credential-lure verdict and failed sender alignment on the same inspected link justify reviewing the message.

**Pivot** Use the mail message ID and sender domain to trace the inspection outcome.

**Support** Check the recipient, sender alignment, URL verdict and destination domain. Keep the domain as evidence text. Matched records `01-positive-02`.

**Alternative** Legitimate forwarded mail can fail alignment. Use independent URL inspection before escalating. Contrast a failing verdict with an approved business sender before proposing a block.

[Positive](../scenarios/fixtures/01.positive.json) · [Noisy control](../scenarios/fixtures/01.negative.json)

## [MFA Fatigue](learn/02.md)

Three distinct denied push prompts for one user within five minutes warrant investigation.

**Pivot** Group denied push requests by user and count distinct challenge IDs over five minutes.

**Support** Confirm the user, method and outcome. Three distinct challenge IDs within five minutes link the alert to individual requests. Matched records `02-positive-02`, `02-positive-03`, `02-positive-04`.

**Alternative** Someone re-enrolling a phone can deny repeated prompts. An approved enrollment test is recorded with a change context. Separate duplicate IDs and approved enrollment from repeated unsolicited prompts.

[Positive](../scenarios/fixtures/02.positive.json) · [Noisy control](../scenarios/fixtures/02.negative.json)

## [Password Spraying](learn/03.md)

Four distinct users with bad-password failures from one source within ten minutes warrant a password-spray hunt.

**Pivot** Sort identity failures by source IP and count the affected accounts.

**Support** Group by source IP, count distinct usernames, and pivot to subsequent successful sign-ins. Matched records `03-positive-02`, `03-positive-03`, `03-positive-04`, `03-positive-05`.

**Alternative** A shared proxy or SSO outage can make unrelated failures appear to have the same source. Check whether the failures concentrate on a shared approved service or recur across unrelated users.

[Positive](../scenarios/fixtures/03.positive.json) · [Noisy control](../scenarios/fixtures/03.negative.json)

## [PowerShell Abuse](learn/06.md)

An obfuscated PowerShell observation under an office parent warrants process-tree and document review.

**Pivot** Use parent process and script logging context to scope the same host and user.

**Support** Use event 4104, parent process and script classification, then pivot to process identity and document origin. Matched records `06-positive-02`.

**Alternative** Internal Office automation can invoke maintenance tooling with similar lineage. Compare an approved administration context with unexpected child process lineage.

[Positive](../scenarios/fixtures/06.positive.json) · [Noisy control](../scenarios/fixtures/06.negative.json)

## [Registry Autoruns](learn/09.md)

A Run or RunOnce value written by a process of user-writable origin requires checking the executable and autorun target.

**Pivot** Compare the registry target, originating image and host across the three batches.

**Support** Read Target Object and writer process provenance. Confirm the configured path and trace the associated logon or process events. Matched records `09-positive-02`.

**Alternative** Legitimate per-user installers can add logon entries outside centrally managed application paths. Check whether the change belongs to a known signed software rollout before escalating.

[Positive](../scenarios/fixtures/09.positive.json) · [Noisy control](../scenarios/fixtures/09.negative.json)

## [WMI Subscription](learn/10.md)

A new permanent WMI binding with unknown ownership warrants a review of the filter, consumer and registration actor.

**Pivot** Group new WMI subscription records by host and connect the filter and consumer contexts.

**Support** Use Sysmon 21 to link filter and consumer. Check related filter and consumer records and authorized endpoint management changes. Matched records `10-positive-02`.

**Alternative** Managed inventory software can register subscriptions during onboarding. Compare the same event family in a scheduled inventory or approved management workflow.

[Positive](../scenarios/fixtures/10.positive.json) · [Noisy control](../scenarios/fixtures/10.negative.json)

## [RDP/SMB/WinRM Abuse](learn/16.md)

Three administrative sessions to distinct targets from a peer source within ten minutes warrant a lateral movement hunt.

**Pivot** Trace remote-service activity by source and destination host, then check account context.

**Support** Compare the service, source zone and distinct target IDs. Review authorization and process activity on both sides. Matched records `16-positive-02`, `16-positive-03`, `16-positive-04`.

**Alternative** An approved desktop-support activity can touch several systems within minutes. Compare the pivot with known maintenance windows and the documented management route.

[Positive](../scenarios/fixtures/16.positive.json) · [Noisy control](../scenarios/fixtures/16.negative.json)

## [Disable Security Tools](learn/18.md)

An unexpected stopped state for an endpoint protection service warrants checking management heartbeat and actor.

**Pivot** Link a security-service state change to the originating process and host.

**Support** Check the service, new state, surrounding activity, managed heartbeat and any maintenance authorization. Matched records `18-positive-02`.

**Alternative** An approved upgrade can temporarily stop an agent. Check whether a signed update explains the stop and whether the service state recovered.

[Positive](../scenarios/fixtures/18.positive.json) · [Noisy control](../scenarios/fixtures/18.negative.json)

## [Cloud IAM Abuse](learn/20.md)

A successful interactive administrative role grant warrants checking change approval and later role use.

**Pivot** Compare the principal and the resulting IAM permission change in the same audit record.

**Support** Identify granting actor, recipient, account, policy and the authorized deployment process. Matched records `20-positive-02`.

**Alternative** An approved break-glass grant can be necessary during incident response. Look for an approved provisioning identity and change ticket before concluding privilege abuse.

[Positive](../scenarios/fixtures/20.positive.json) · [Noisy control](../scenarios/fixtures/20.negative.json)

## [Active Directory Enumeration](learn/21.md)

A workstation actor issuing repeated directory-wide user-listing queries warrants a directory discovery hunt.

**Pivot** Group directory searches by actor and examine the lookup scope and request context.

**Support** Compare actor, LDAP query class, query scope and client role. Check how often that actor normally queries the directory. Matched records `21-positive-02`, `21-positive-03`.

**Alternative** Auditors, administrators and inventory jobs can enumerate users legitimately. Compare with the volume and source of approved inventory or identity maintenance.

[Positive](../scenarios/fixtures/21.positive.json) · [Noisy control](../scenarios/fixtures/21.negative.json)

## [Cloud Exfiltration](learn/22.md)

Repeated high-volume GetObject activity on restricted data by one identity warrants verifying purpose and destination.

**Pivot** Trace the object storage principal, destination, and access-volume indicators.

**Support** Check the principal, data classification, object count and bucket. Compare workload history and transfer logs. Matched records `22-positive-02`, `22-positive-03`.

**Alternative** An approved backup, restore or analytics load can read numerous restricted objects. Compare with an approved backup or export before escalating possible exfiltration.

[Positive](../scenarios/fixtures/22.positive.json) · [Noisy control](../scenarios/fixtures/22.negative.json)

## [Ransomware-Like Activity](learn/23.md)

Four distinct renames to one unexpected extension pattern on a shared document host in two minutes warrant rapid triage.

**Pivot** Find the host and process attached to the unusual synthetic file activity, then compare timing.

**Support** Check distinct file identifiers, extension pattern, process lineage and the affected share. Confirm recoverability with backups. Matched records `23-positive-02`, `23-positive-03`, `23-positive-04`, `23-positive-05`.

**Alternative** Controlled migrations and testing can perform bulk renames on a mapped share. Compare with an authorized backup or build process to rule out benign bulk writes.

[Positive](../scenarios/fixtures/23.positive.json) · [Noisy control](../scenarios/fixtures/23.negative.json)

## [GitHub Actions Tampering](learn/33.md)

A workflow update that adds write permissions outside approved review warrants examining the diff and executed jobs.

**Pivot** Join the audit action to the actor, repository, and reviewed workflow diff metadata.

**Support** Use the changed path, permissions delta and review status. Pivot to revision, branch rules and any resulting run. Matched records `33-positive-02`.

**Alternative** An emergency policy adjustment can add scoped write rights before normal release workflows run. Require confirmation of what changed and whether the change used an approved review path.

[Positive](../scenarios/fixtures/33.positive.json) · [Noisy control](../scenarios/fixtures/33.negative.json)

## [Kubernetes RBAC Abuse](learn/35.md)

An interactive actor granting cluster-admin through a ClusterRoleBinding needs immediate authorization review.

**Pivot** Check the Kubernetes actor, binding name and assigned role in the same audit record.

**Support** Check the request actor, role reference, subject and API response. Review later activity by the new subject. Matched records `35-positive-02`.

**Alternative** An approved bootstrap or break-glass action can grant high privileges temporarily. Review the namespace, provisioning identity and authorization record for expected changes.

[Positive](../scenarios/fixtures/35.positive.json) · [Noisy control](../scenarios/fixtures/35.negative.json)

## [SaaS Exfiltration](learn/40.md)

A large share of restricted SaaS data to external recipients warrants checking access grants and delivery.

**Pivot** Group the SaaS audit records by actor and share scope, then compare file access volume.

**Support** Check actor, volume, data classification and destination. Review subsequent access and whether sharing was approved. Matched records `40-positive-02`.

**Alternative** An approved collaboration or e-discovery export can generate a bulk share event. Compare a known compliance export or approved collaboration with the unusual destination and volume.

[Positive](../scenarios/fixtures/40.positive.json) · [Noisy control](../scenarios/fixtures/40.negative.json)
