# ThreatHuntX v0.2.0 review candidate

The v2 candidate builds on the Community alpha. It adds the grouped technique map and learning checkpoints, Detection Studio, an investigation workspace with saved analysis, and a downloadable case report format. The README documents setup from `main` and presents the original framework infographic. [Community alpha PR](https://github.com/Aventador-LP700/ThreatHuntX/pull/1) · [Framework downloads](diagrams/README.md#scenario-map-and-application-images)

The bundled Wazuh evidence covers the official 4.14.10 engine, its decoder and 20 event candidates on synthetic inputs. The optional YARA engine classifies inert text. Live collection, full Wazuh deployment, and vendor queries require separate verification. See the recorded Windows and macOS status before following desktop setup. [Acceptance matrix](INTEGRATION_ACCEPTANCE.md) · [Validation summary](../reports/validation-summary.md)

The release packaging script derives the version from `pyproject.toml`, builds a deterministic static snapshot, and includes source and showcase ZIP and TAR archives, the Bash launcher, fixture results, SBOMs and SHA-256 checksums. Standalone bootstrap selects the release tag once published. Docker Compose still initializes database schema version 1. Existing replay evidence remains available in the project volume, and optional analysis uses browser storage.

Complete the independent beginner walkthrough before publishing. GitHub Pages requires repository configuration. [Implementation audit](implementation-audit.md) · [Pages setup](../public-demo/README.md)
