# Threat model

The default deployment is a single-machine teaching environment. Trusted inputs include the checked-out code, the build dependency sources, and reviewed fixture manifests. Local users who control Docker can inspect or change the runtime and its volume.

| Exposure | Controls | Residual risk |
| --- | --- | --- |
| Untrusted network client or malicious website | Loopback bind, loopback host checks, JSON and same-origin replay, CSP, no API port exposure | Local services can access the loopback endpoint. Keep the lab on a trusted device. |
| Offensive or sensitive input | Reviewed synthetic records, strict bundled replay selector and parser, read-only lesson examples | Maintainers have responsibility for reviewing contributions and generated exports. |
| Build supply chain | Dependency lockfiles, image digests, least-privilege CI and security scans | Review upstream updates, base images and binaries as part of every release. |
| Replay or storage exhaustion | Fixed packaged batches, bounded recent-history views, project-local volume reset | Long-running use can grow the SQLite file. Replay records are retained until reset. |
| Learner privacy | Browser-local progress and theme, synthetic database, no additional network calls from the app | Shared browsers can reveal prior completion. Local web logs show request paths and timestamps. |
| Optional integration isolation | Independent deployment and a disposable validation lab | Live collector policy, account handling, resource access and transport security depend on the operator. |

[Safety and scope](SAFETY_AND_SCOPE.md) · [Privacy](PRIVACY.md) · [Security reporting](../SECURITY.md)
