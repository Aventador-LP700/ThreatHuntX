# Portable detections

The Community Lab executes the normalized rule in each [scenario manifest](../scenarios/manifests). Original Sigma specifications and Wazuh, KQL, and SPL examples share field mappings. Treat vendor backends, event sources, and required enrichments as independent validation work.

| Artifact | Cases | Inputs and verification |
| --- | --- | --- |
| [Sigma](../detections/sigma) | 01–40 | pySigma parses base specifications and resolves rule references offline. Tests compare normalized positive, noisy and clean event selections against each local rule. Correlations represent counts and distinct counts. Backend execution requires a compatible pipeline and explicit field mapping. |
| [Wazuh](../detections/wazuh) | 01–20 | Decoder and child rules use the `THX_JSON` projection in `synthetic.log`. Static XML and event selection checks run offline. These examples evaluate individual event candidates, including event-level exclusions. See the validation report for Wazuh manager status. |
| [KQL](../detections/kql) | 01–15 | Review-only templates for a Sentinel Log Analytics custom table `THXNormalized_CL`. Offline tests check template fields and intended decisions on fixtures. |
| [SPL](../detections/spl) | 01–15 | Review-only templates for index `threathuntx`, sourcetype `thx:normalized:json`. Offline tests check template fields and intended decisions on fixtures. |

## Normalized projection

Each rule field maps to a `THX`-prefixed PascalCase column. Remove `observables.` and preserve the meaning and scalar type of each field. This is a custom schema. Examples are paired with the local manifest and fixture so you can assess source fidelity before attempting live use.

| Event source | Example projection | Expected real source and additional context |
| --- | --- | --- |
| Identity | `THXUser`, `THXAuthMethod`, `THXChallengeId`, `THXSourceIp` | Entra `SigninLogs` or `AuditLogs`. Normalize `UserPrincipalName`, `IPAddress`, `ResultType`, and authentication step details. Prompt ID may require a provider-specific join. |
| Windows | `THXEventId`, `THXProcess`, `THXParentProcess`, `THXTargetObject` | Sysmon or Security event logs and PowerShell script-block records. Join process and enrichment fields for script and provenance classifications. |
| Linux | `THXAction`, `THXEffectiveUid`, `THXScheduleOwner` | Audit summaries derived from auditd records and reviewed owner context. |
| Mail | `THXSenderAlignment`, `THXUrlCategory`, `THXDomain` | Gateway alignment and sandbox verdicts. Join by message ID or correlate recipient and UTC timestamp. |
| Network | `THXSignatureFamily`, `THXPeerZone`, `THXDomain` | WAF, DNS, or sensor records plus organization-specific classifications. |
| Audit and scanner | `THXActorClass`, `THXRoleRef`, `THXReviewStatus`, `THXFileCount` | Provider audit events with joins to approval, classification and revision records. |

In KQL, use `TimeGenerated` as UTC datetime, `THXRecordId` as a string, and preserve native bool and long fields for predicates. In Splunk, use `_time` derived from `TimeGenerated`, JSON field extraction, and normalized string values or numbers. Wazuh fixtures use the string `__missing__` for absent dynamic fields so exclusions can be tested consistently. Grouping keys such as user and domain should be canonicalized consistently before use.

Template correlation uses fixed time bins, which can split evidence across a boundary. The local engine uses sliding windows and exact distinct values. KQL `dcount()` may approximate at scale. For both vendor templates, review null handling, deduplication, normalization and bin boundaries against live-approved fixture paths before promotion.

The repository includes no automatic Sigma-to-Wazuh conversion. The example artifacts are generated from an explicit supported local predicate set. `wazuh_regex` rejects unsupported operations and the emitted field mapping remains reviewable. [Add a detection](HOW_TO_WRITE_A_DETECTION.md)
