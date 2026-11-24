# Ten starter hunt hypotheses

Replay the positive and noisy examples in each lesson. Read the supporting and contradictory observations before proposing a response.

## [Phishing](learn/01.md)

A credential-lure verdict and failed sender alignment on the same inspected link justify reviewing the message.

**Support** Check the recipient, sender alignment, URL verdict and destination domain. Keep the domain as evidence text.

**Alternative explanation** Legitimate forwarded mail can fail alignment. Use independent URL inspection before escalating.

## [MFA fatigue](learn/02.md)

Three distinct denied push prompts for one user within five minutes warrant investigation.

**Support** Confirm the user, method and outcome. Three distinct challenge IDs within five minutes link the alert to individual requests.

**Alternative explanation** Someone re-enrolling a phone can deny repeated prompts. An approved enrollment test is recorded with a change context.

## [Password spraying](learn/03.md)

Four distinct users with bad-password failures from one source within ten minutes warrant a password-spray hunt.

**Support** Group by source IP, count distinct usernames, and pivot to subsequent successful sign-ins.

**Alternative explanation** A shared proxy or SSO outage can make unrelated failures appear to have the same source.

## [PowerShell abuse](learn/06.md)

An obfuscated PowerShell observation under an office parent warrants process-tree and document review.

**Support** Use event 4104, parent process and script classification, then pivot to process identity and document origin.

**Alternative explanation** Internal Office automation can invoke maintenance tooling with similar lineage.

## [Registry autoruns](learn/09.md)

A Run or RunOnce value written by a process of user-writable origin requires checking the executable and autorun target.

**Support** Read Target Object and writer process provenance. Confirm the configured path and trace the associated logon or process events.

**Alternative explanation** Legitimate per-user installers can add logon entries outside centrally managed application paths.

## [RDP / SMB / WinRM abuse](learn/16.md)

Three administrative sessions to distinct targets from a peer source within ten minutes warrant a lateral movement hunt.

**Support** Compare the service, source zone and distinct target IDs. Review authorization and process activity on both sides.

**Alternative explanation** An approved desktop-support activity can touch several systems within minutes.

## [Cloud IAM abuse](learn/20.md)

A successful interactive administrative role grant warrants checking change approval and later role use.

**Support** Identify granting actor, recipient, account, policy and the authorized deployment process.

**Alternative explanation** An approved break-glass grant can be necessary during incident response.

## [Ransomware-like activity](learn/23.md)

Four distinct renames to one unexpected extension pattern on a shared document host in two minutes warrant rapid triage.

**Support** Check distinct file identifiers, extension pattern, process lineage and the affected share. Confirm recoverability with backups.

**Alternative explanation** Controlled migrations and testing can perform bulk renames on a mapped share.

## [GitHub Actions tampering](learn/33.md)

A workflow update that adds write permissions outside approved review warrants examining the diff and executed jobs.

**Support** Use the changed path, permissions delta and review status. Pivot to revision, branch rules and any resulting run.

**Alternative explanation** An emergency policy adjustment can add scoped write rights before normal release workflows run.

## [Kubernetes RBAC abuse](learn/35.md)

An interactive actor granting cluster-admin through a ClusterRoleBinding needs immediate authorization review.

**Support** Check the request actor, role reference, subject and API response. Review later activity by the new subject.

**Alternative explanation** An approved bootstrap or break-glass action can grant high privileges temporarily.
