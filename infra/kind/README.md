# Optional Kubernetes audit notes

Start with the bundled [Kubernetes RBAC fixture](../../scenarios/fixtures/35.positive.json). For live collection, create a separate named kind cluster using the pinned version in the [analyst lab guide](../../docs/full-lab-setup.md). Review the Kubernetes [audit policy instructions](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/) and mount `audit-policy.yaml` read-only in the control plane. Set the API server `audit-policy-file` to the mounted file and `audit-log-path` to project-owned storage.

Verify the cluster audit log before collecting it. The policy records RBAC request and response data plus metadata for other requests. Restrict access to the audit log and keep the API on loopback. This configuration guide is manual pending. Teardown consists of deleting the named disposable cluster and reviewing the retained log files.
