# ThreatHuntX implementation plan

| Milestone | Work | Exit evidence |
| --- | --- | --- |
| M0 | Inspect the supplied map, CSV, master brief, and GitHub target. Establish release and runtime boundaries. | Repository starts empty. Docker, Compose, Chromium, and GitHub access identified. |
| M1 | Build a loopback-only Compose app, single Bash setup, event parser, SQLite storage, MFA correlation, and a first guided hunt. | Fresh build, service health, baseline, positive alert with an evidence timeline, and negative fixture demonstrated. |
| M2 | Validate ATT&CK mappings against a pinned MITRE release. Expand the catalog, safe fixtures, and correlation tests. | Forty catalog entries and at least ten distinct replay investigations verified. |
| M3 | Add portable rules, Wazuh examples, hunting queries, analyst evidence and exports. | Rule validation and offline test results describe the coverage of each tool. |
| M4 | Complete accessibility, curriculum, static showcase, and contributor documentation. | Local learning flow, downloadable report, and community review paths verified. |
| M5 | Rehearse clean installation, collect screenshots and measurements, run CI checks, and prepare release materials. | Validation report, reproducible artifacts, and release or documented publication blocker. |

The default lab requires Docker Engine or Docker Desktop with Compose v2. Resource use and supported platforms will be recorded from the clean installation. Wazuh and real sensors are independent of the default stack.

Scope is deterministic defensive replay. Fixture records represent observations from a fictional environment. The lab never issues the actions represented in the records. SQLite and learning progress are local. The app binds to loopback and has no outbound telemetry.
