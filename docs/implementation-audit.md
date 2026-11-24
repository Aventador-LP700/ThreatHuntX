# Community v2 implementation audit

Baseline `8e510c47fdba37e61154bee59e42e579c9bb9bbc` from `community-alpha`. At the time of inspection, `main` contained the starter lab, PR #1 was open, and the v0.1.0 release was a draft. [PR #1](https://github.com/Aventador-LP700/ThreatHuntX/pull/1)

| Priority | Inspected baseline | Upgrade target |
| --- | --- | --- |
| Infographic | The README linked to a screenshot of the running site's ATT&CK view. The initial attachment contained the specification. | Feature the supplied infographic as a lossless preview linked to the original PNG. Provide SVG and PDF downloads. |
| Catalog | Forty manifests, curated baselines, positive and noisy samples, and pinned ATT&CK 20.1 metadata. | Align display names and the eight sections with the specification, and export a generated matrix and per-lesson fixture results. |
| Learning | Vue lessons, five worked cases, ten hunts, browser progress, replays and evidence timelines. | Add an interactive technique map, fifteen evidence-backed hunts, and clearer checkpoints. |
| Analyst tools | Read-only rule views, recent-run filtering and JSON/CSV evidence exports. | Add isolated rule trials, exact evidence pivots, browser-local case notes and safe printable reports. |
| Deployment | Docker Compose and a static build with recorded Linux and CI evidence. GitHub's Pages endpoint returned 404. | Rehearse both surfaces, add the Pages workflow and settings instructions, and verify documentation and artifact boundaries. |
| Analyst integrations | Wazuh projections passed static checks. The prior manager image extraction exceeded local disk. The vendor and sensor integrations remain pending. | Add safe fixture-shaped adapters and try a bounded manager log test. Distinguish engine validation from deployment and live collector evidence. |

The product catalog uses the specification for scenario names and pinned MITRE data for technique and tactic claims. Links to prior release evidence stay traceable from the [validation report](../reports/validation-summary.md).

## Review candidate status

The v2 implementation adds the grouped catalog, portable case reports, fixture-backed tuning, vendor samples, and an isolated Wazuh engine check. The lab map shows all 40 scenario and countermeasure pairs, and the CLI reports the underlying evidence and detection results. The README features the exact framework infographic from the supplied PNG and labels the application screenshot in the Scenario lab section. [Diagram downloads](diagrams/README.md) · [Validation summary](../reports/validation-summary.md)
