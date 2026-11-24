# Community v2 engineering notes

Community v2 builds on the `community-alpha` baseline at commit `8e510c47fdba37e61154bee59e42e579c9bb9bbc`. That baseline contained the first Compose deployment and guided replay. [Community alpha PR](https://github.com/Aventador-LP700/ThreatHuntX/pull/1) · [Community v2 PR](https://github.com/Aventador-LP700/ThreatHuntX/pull/2)

| Area | Community alpha | Community v2 |
| --- | --- | --- |
| Framework and diagrams | The README linked to a screenshot of the ATT&CK view. | The README links a lossless framework preview to the full-size PNG. The gallery includes SVG and PDF downloads. |
| Catalog | Forty manifests, clean and noisy controls, positive samples, and pinned ATT&CK 20.1 metadata. | Eight domains with a generated coverage matrix and fixture results for each lesson. |
| Learning | Vue lessons, five worked cases, ten hunts, browser progress, replays, and evidence timelines. | An interactive Technique Map, fifteen hunt hypotheses, and learning checkpoints. |
| Analyst tools | Read-only rule views, recent-run filtering, and JSON and CSV evidence exports. | Temporary rule trials, evidence pivots, browser-local case notes, and printable reports. |
| Deployment | Docker Compose and a static build with recorded Linux and CI results. | Rehearsed Compose and static builds, a Pages workflow, and deployment instructions. Hosted Pages requires repository configuration. |
| Analyst integrations | Wazuh rule projections passed static checks. | The Wazuh 4.14.10 engine evaluated bundled synthetic records. Live collection and full manager deployment require separate verification. |

The catalog maps each scenario to the pinned ATT&CK release. The Technique Map links the forty scenario and countermeasure pairs, and the CLI reports the underlying fixture evidence and detection results. [Evidence matrix](evidence-matrix.md) · [Diagram downloads](diagrams/README.md) · [Validation summary](../reports/validation-summary.md) · [Integration status](INTEGRATION_ACCEPTANCE.md)
