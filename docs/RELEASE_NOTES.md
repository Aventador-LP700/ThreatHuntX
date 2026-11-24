# ThreatHuntX v0.1.0 Community alpha

This release candidate adds the loopback Community Lab and a static public showcase. Learners can replay 40 synthetic scenarios, inspect normalized evidence for alerts, compare noisy controls, answer questions, record local progress, and export JSON or CSV evidence. The code includes original Sigma specifications, Wazuh event-candidate rules, and KQL/SPL templates with explicit portability notes.

## Compatibility and migration

The observed community deployment uses Linux x86-64 with Docker Engine 29 and Compose v2. The build pins Python, Node and Nginx by image digest. Docker Desktop on Windows and macOS needs a separate smoke test. SQLite schema version 1 initializes automatically. This is the initial alpha, so there is no earlier release schema to migrate. Teardown preserves the project volume. See the [upgrade guidance](TROUBLESHOOTING.md).

For the candidate checkout, `./scripts/setup.sh` builds and waits for health. The separately downloadable `setup.sh` supports `bash setup.sh install <directory>` against the release tag. This bootstrap was tested with a temporary Git mirror tagged `v0.1.0`.

## Scope and pending checks

Synthetic verification covers the bundled fixtures, including application integration and the ten core browser lessons. The optional Wazuh manager, endpoint agents, provider data paths and vendor query engines still need live verification. Use the [validation report](../reports/validation-summary.md) to verify how a particular result was obtained.

## Artifact provenance

The source archive is prepared with `git archive` from the release candidate. The static archive comes from `make showcase`, which matches packaged fixtures before building the snapshot. The packaging script records the source commit and SHA-256 checksums. Software bills of materials list locked Python and frontend dependencies. Checksums identify artifacts and the attachments have no signature or formal provenance attestation. [Maintainer hand-off](MAINTAINER_HANDOFF.md)
