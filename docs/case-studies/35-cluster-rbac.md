# Kubernetes RBAC abuse investigation

An interactive actor granting cluster-admin through a ClusterRoleBinding needs immediate authorization review.

The Community Lab engine evaluated the packaged evidence and linked 1 record(s) to one alert. A noisy replay yielded zero alerts. All event timestamps below come from the bundled fixture.

## Evidence timeline (UTC)

| Timestamp | Event and outcome | Evidence |
| --- | --- | --- |
| 2025-08-14T17:40:00Z | create_binding · success | [35-positive-01](../../scenarios/fixtures/35.positive.json) · Background |
| 2025-08-14T17:40:32Z | create_binding · success | [35-positive-02](../../scenarios/fixtures/35.positive.json) · Matched |

Check the request actor, role reference, subject and API response. Review later activity by the new subject.

[Local rule](../../scenarios/manifests/35.json) · [Sigma](../../detections/sigma/35.yml) · [JSON example](../../examples/35-cluster-rbac.json)

## Assessment and response

A successful ClusterRoleBinding to cluster-admin gives the specified subject broad cluster-level access. Escalate the review of who authorized it.

Preserve audit events and revoke the confirmed unauthorized binding. Inventory later access by the subject.

## Root-cause hypothesis and mitigation

The fixture models an interactive elevated grant. Review authorization of the binding and look for subsequent access by its subject.

Use least-privilege RBAC, change review for privileged bindings, and admission controls where appropriate.

## Tuning and limitations

The noisy case uses a recorded bootstrap context. Limit the exception to verified initialization and track expiry of temporary grants.

Fields summarize a Kubernetes audit event. The lab neither connects to a cluster nor mutates roles.

[Lesson](../learn/35.md) · [T1098.006](https://attack.mitre.org/techniques/T1098/006)
