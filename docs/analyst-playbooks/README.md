# Response playbooks

Use these steps to practise evidence handling and response decisions. Scenario-specific guidance and limitations are available in the linked lessons.

## Identity prompt and session abuse

Identity · T1621, T1550.001

Unexpected MFA denials, a risky session or a login burst affecting distinct users.

1. Preserve sign-in and authentication detail with actor, UTC time, source, device and session reference.
2. Verify prompt intent with the user through a trusted channel. Scope successful sign-ins and follow-on application use.
3. Revoke suspicious sessions, assess user and app access and check for repeat signals after containment.

**Recovery** Confirm verified access is restored. Adopt phishing-resistant authentication and review device and prompt policy.

[MFA Fatigue](../learn/02.md) · [Password Spraying](../learn/03.md) · [Token Theft](../learn/11.md) · [Adversary-in-the-Middle Phishing](../learn/26.md) · [Device-Code Phishing](../learn/27.md)

## Suspicious mail and links

Mail · T1566.002, T1027.006

A gateway flags mismatched sender alignment, a risky URL redirect or attachment behavior.

1. Preserve the message and verdict using an approved evidence process. Review message ID, recipients and delivery state.
2. Quarantine related messages. Look for click and identity events for recipients who interacted.
3. Scope credentials and sessions affected by confirmed interactions. Verify later deliveries and update filtering and user guidance.

**Recovery** Confirm users can report follow-up messages and validate the same conditions against known legitimate mail.

[Phishing](../learn/01.md) · [HTML Smuggling](../learn/07.md) · [QR-Code Phishing](../learn/30.md)

## Windows execution and persistence triage

Windows · T1059.001, T1547.001, T1546.003

Unexpected script lineage, autorun modification, permanent WMI subscription or risky driver signal.

1. Preserve process, registry and subscription telemetry and verify signer, parent and effective scope.
2. Compare the observation with software inventory, startup baselines and approved changes. Restrict affected endpoints if corroborated.
3. Coordinate removal through endpoint response, then confirm the relevant artifact and post-remediation events are consistent.

**Recovery** Recheck execution control, startup events and endpoint health after recovery.

[PowerShell Abuse](../learn/06.md) · [Registry Autoruns](../learn/09.md) · [WMI Subscription](../learn/10.md) · [LOLBins/LOLBAS](../learn/17.md) · [BYOVD Driver Abuse](../learn/38.md)

## Lateral movement and directory review

Endpoint and AD · T1021, T1550.002, T1087.002

Administrative sessions fan out from a peer or abnormal account activity appears in directory logs.

1. Scope the user, source, destinations and first observed time. Preserve records on both sides of the session.
2. Validate jump hosts and service ownership. Correlate remote activity with process and account changes.
3. Terminate confirmed unauthorized sessions, restrict access paths, and rotate affected credentials through established policy.

**Recovery** Recheck management network boundaries and confirm expected ticket and session volume after recovery.

[Kerberoasting](../learn/13.md) · [Pass-the-Hash](../learn/14.md) · [RDP/SMB/WinRM Abuse](../learn/16.md) · [Active Directory Enumeration](../learn/21.md) · [RMM Tool Abuse](../learn/39.md)

## Cloud and SaaS access changes

Cloud and SaaS · T1098.003, T1530, T1567

Unexpected administrative grants, restricted object reads or large external shares.

1. Preserve actor, target, policy and API response. Identify which account or tenant contains the affected objects.
2. Verify approval, inventory downstream access and keep affected evidence snapshots.
3. Revoke verified unauthorized grants or links, then review successful access after the change and refine least privilege.

**Recovery** Confirm expected workloads function and monitor later resource access and sharing changes.

[OAuth Consent Phishing](../learn/05.md) · [Cloud IAM Abuse](../learn/20.md) · [Cloud Exfiltration](../learn/22.md) · [Cloud Metadata Credential Theft](../learn/37.md) · [SaaS Exfiltration](../learn/40.md)

## CI/CD and supply chain review

GitHub and CI · T1195.001, T1550.001, T1677

An unexpected package hook, workflow permission change, off-policy runner or shared secret-scanner finding.

1. Preserve revision, reviewed diff, job identity and runner logs. Keep actual credential material out of reports.
2. Suspend an affected workflow through authorized controls. Verify published build outputs and provenance.
3. Revert unauthorized changes, rotate confirmed exposed credentials and rebuild from a reviewed revision.

**Recovery** Require review for workflow paths and apply explicit least-privilege job permissions.

[Malicious Dependencies](../learn/31.md) · [CI/CD Token Compromise](../learn/32.md) · [GitHub Actions Tampering](../learn/33.md) · [Secrets in Git/Artifacts](../learn/34.md)

## Kubernetes authorization and workload review

Kubernetes · T1098.006, T1611

A broad cluster role grant or a workload requests host-level privileges.

1. Preserve audit events with request actor, subject, resource, namespace and API decision.
2. Check change approval, owner and any follow-on activity by the subject. Corroborate host effects with runtime evidence.
3. Remove confirmed unauthorized access under change control and watch for related requests or grants.

**Recovery** Test expected workload behavior and apply reviewed admission and RBAC policy.

[Kubernetes RBAC Abuse](../learn/35.md) · [Container Escape](../learn/36.md)

## Destructive file activity and recovery

Endpoint and storage · T1486, T1485

Clustered renames, sensitive staging or deletion summaries affect protected content.

1. Preserve storage and writer telemetry and document affected resources and time bounds.
2. Restrict confirmed affected writers and follow evidence-handling procedures before cleanup.
3. Check whether approved migration or retention explains the activity. Verify backups and rehearse recovery in isolation.

**Recovery** Restore from a verified recovery point, check integrity and monitor related paths after service resumes.

[Ransomware-Like Activity](../learn/23.md) · [Data Staging](../learn/24.md) · [Wiper-Like Activity](../learn/25.md)

[Safety and scope](../SAFETY_AND_SCOPE.md)
