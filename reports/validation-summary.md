# ThreatHuntX validation

## Framework infographic · 2026-11-24

The original PNG from the supplied archive measures 1536 × 1024 pixels and is stored byte for byte at 2,349,700 bytes. Its SHA-256 is `8a7b2d02868b7ff9b80684ed29492f1fa3b5ff3c49b9d6efb3afc6f24896e60b`. The 1,846,188-byte WebP preview has the same decoded pixels and dimensions. The SVG embeds the original PNG, and the one-page PDF preserves those pixels. [Original PNG](../docs/diagrams/png/threathuntx-v2-40-threat-map.png) · [Download gallery](../docs/diagrams/README.md)

All 45 gallery exports opened and matched their expected proportions. The Markdown check confirmed the WebP as the first image in the README and the original PNG as its link target. [README](../README.md)

## Scenario lab update · 2026-11-24

The Linux x86-64 rehearsal built and started both Compose services using `./scripts/setup.sh` with an isolated project and loopback port. `/api/health` returned `synthetic_only: true`. The [scenario map screenshot](../docs/media/v2-technique-map.webp) was captured from this deployment at 2109 × 2244 pixels.

| Check | Observed result |
| --- | --- |
| `uv run --locked pytest -q` | 214 passed. New tests cover all 40 report entries, exact fixture references, read-only assessment, argument validation, and temporary threshold trials. Starlette emitted its existing test-client deprecation warning. |
| `./scripts/setup.sh lab all` and `PYTHONPATH=backend uv run --locked python -m app.cli lab --format json` | Both modes reported 120 checks passed. All 40 positive fixtures alerted and all 80 clean and noisy fixtures stayed quiet. |
| `./scripts/setup.sh lab 02 --threshold 4 --format json` | Exit status 1 with a false negative in the trial. The published rule still passed all three MFA checks. |
| `./scripts/setup.sh lab 02 --threshold 3 --format json` | Exit status 0 with three matched challenge records in the positive fixture and zero alerts in both controls. |
| Chromium on Compose | 15 passed. The suite checked the eight-by-five map, all 40 lesson links and countermeasures, mobile search, rule trials, and case exports. |
| Chromium on the static showcase | Six passed and nine live-app-only checks skipped. The map and all 40 lessons worked from a project subpath. |

The assessment reports decisions for bundled synthetic evidence. [Integration acceptance](../docs/INTEGRATION_ACCEPTANCE.md) records the checks that require external platforms or collectors.

## Community v2 · 2026-11-24

The upgrade starts from the existing `community-alpha` candidate and retains [PR #1](https://github.com/Aventador-LP700/ThreatHuntX/pull/1). Tests exercise the 40 bundled synthetic scenarios. The previous alpha measurements and CI evidence remain below.

| Check | Observed result |
| --- | --- |
| `uv run --locked pytest -q` | 209 passed, including 40 default studio comparisons, threshold and window boundaries, strict trial inputs, exclusion and duplicate handling, report schema, CSV neutralization and vendor adapters. Starlette reported the existing test-client deprecation warning. |
| Via Compose, `npm --prefix frontend run test:e2e` | 15 passed against Chromium. All 40 lesson routes opened, the MFA trial produced the intended miss and noisy control, and case export, reload persistence, printable PDF and selected axe checks passed. |
| `make showcase` and `THX_SHOWCASE=1 THX_URL=http://127.0.0.1:4173/dist/ npm --prefix frontend run test:e2e` | Six passed. Nine local replay-only browser checks skipped in static mode. Both the lesson and case workspace tests observed only static reads. |
| `PYTHONPATH=backend uv run --locked python -m app.cli verify` | 40 positive and 80 control batches matched their expected decision. The synthetic corpus gives 40 TP, 80 TN, 0 FP and 0 FN. |
| `PYTHONPATH=backend uv run --locked python -m scripts.verify_attack --stix enterprise-attack.json` | All 40 mappings matched the pinned upstream Enterprise ATT&CK 20.1 records. |
| `./scripts/check-wazuh-engine.sh /absolute/path/to/wazuh-manager_4.14.10-1_amd64.deb` | Native `wazuh-analysisd -t` succeeded. `wazuh-logtest-legacy` decoded all 138 bundled records and its event selections matched all 20 candidate IDs. [Sanitized engine evidence](../detections/wazuh/engine-validation.json) |
| `PYTHONPATH=backend uv run --locked python -m scripts.vendor_samples all` and `uv run --locked --extra forensics python -m scripts.check_yara_samples` | Eight vendor-shaped examples normalized to the event schema. YARA 4.5.4 matched one inert note and returned no match for its clean control. The two benign DNS query and reply pairs were parsed back from the bundled four-record PCAP. |

A clean checkout cloned from the public candidate branch with credential prompts disabled. The cold workspace build used the documented trusted proxy CA overlay. The direct `docker compose up -d --build --wait` path also passed with those layers available. Both services became healthy, the Wazuh artifact displayed its verified engine state, and the 15 browser checks passed again. The reset left 40 synthetic baselines and zero replay runs. Teardown preserved the original project's volume. A first clean attempt exhausted the workspace's VFS storage. Clearing this task's obsolete images and build cache allowed a successful rehearsal.

`./scripts/package-release.sh` generated source and static ZIP and TAR archives. SHA-256 verification and ZIP integrity checks passed. The static archive contains `index.html`, `snapshot.json`, its assets and license files. The source archive includes the candidate source, documentation and checks. The Linux CI jobs provide an independent fresh build of the reviewed source.

A local x86-64 Linux Compose run used Docker Engine 29.9.2, Compose 2.40.3 and Chromium 156.0.8078.79 in an environment with three Docker-visible CPUs and 10,452,459,520 bytes of RAM. Health returned a synthetic-only schema version 1 service and the published socket was `127.0.0.1:8080`. One tested build reported API and web image sizes of 141,409,719 and 62,738,848 bytes. After the browser tests, the process RSS samples were 52,916 KiB for Uvicorn and 3,200 and 3,184 KiB for the two Nginx processes. The SQLite file was 160 KiB. The environment uses rootless VFS without Docker cgroup accounting. These are observed figures and peak requirements depend on the host and build cache.

GitHub reports the repository as public. The connected credential returned HTTP 403 for Pages creation and repository description/topic changes. The candidate includes the reproducible static build and default-branch Pages workflow. Hosted deployment requires GitHub Pages configuration. [Implementation audit](../docs/implementation-audit.md) · [Pages setup](../public-demo/README.md)

A full Wazuh installation, live agent and network sensor runs, and vendor-specific queries are separate checks. Windows and macOS Docker Desktop tests and an independent beginner walkthrough remain manual pending. [Integration status](../docs/INTEGRATION_ACCEPTANCE.md)

## Community alpha baseline

## Observed results

| Check | Evidence |
| --- | --- |
| `docker compose config --quiet` and `./scripts/setup.sh` | Docker built the API and web images from pinned bases. Both Compose health checks passed. `GET /api/health` through `127.0.0.1:8080` returned `{"status":"ok","schema_version":1,"synthetic_only":true}`. The cold build in this environment used the optional trusted build CA overlay. |
| `uv run --locked pytest --junitxml=build/validation/pytest.xml` | 144 passed. Includes all 40 API investigations, source selection, noisy controls, grouping, suppressions, persistence, JSON and CSV exports, and portable artifact checks. Starlette emitted a test-client deprecation warning. |
| `PYTHONPATH=backend uv run --locked python -m app.cli verify` | All 120 fixture batches matched their labels. 40 TP, 80 TN, 0 FP and 0 FN. The 80 controls include 40 clean baselines and 40 noisy batches. The denominator for precision is 40 predicted positive batches; recall uses 40 labeled positive batches. |
| `PYTHONPATH=backend uv run --locked python -m scripts.verify_attack --stix enterprise-attack.json` | All 40 lesson mappings agreed with the active technique metadata in the pinned official Enterprise ATT&CK 20.1 STIX file. Related mappings carry a rationale. |
| `npm --prefix frontend run test:e2e` | Twelve passed against the Linux Compose app in Chromium. Ten tests cover distinct guided lessons; two cover automated accessibility and mobile/filter/rule workflows. The MFA exercise verifies completion persistence and report export. |
| `make showcase` and `THX_SHOWCASE=1 THX_URL=http://127.0.0.1:4173/dist/ npm --prefix frontend run test:e2e` | Three browser tests passed. Nine Compose-only tests were skipped in showcase mode. The first lesson made only local static GET requests and worked under a project subpath. |
| `uv run --locked ruff check`, `uv run --locked ruff format --check`, frontend typecheck and build | Passed locally. |
| `pip-audit --require-hashes --disable-pip -r infra/docker/requirements.txt`, `npm --prefix frontend audit`, Bandit | No known vulnerabilities in the audited locked Python runtime and npm packages at the time of the run. Bandit passed for backend application source. |
| `actionlint` and SBOM generation | Workflow syntax passed. CycloneDX manifests generated for the locked Python runtime and frontend production dependencies. |
| Runtime media | Five screenshots and a 31.4-second recording captured during a real MFA replay. [Media](../docs/media/README.md) |

## Clean installation and CI evidence

- A fresh local Git checkout with a clean Compose project and a new volume passed `docker compose up -d --build` using cached dependency layers. The Bash launcher repeated startup and readiness checks. The API listed 40 lessons and produced one MFA alert and zero noisy alerts. Reset was run twice, and teardown preserved both the rehearsal and original named volumes.
- The standalone `bash setup.sh install <directory>` path cloned a temporary Git mirror tagged `v0.1.0`, built the project and passed health at a custom loopback port. This measured the installer against a local mirror while the GitHub release tag was pending.
- An authenticated clean clone of the GitHub `community-alpha` branch matched the tested commit. GitHub Actions passed both jobs, including the cold Compose build with default configuration, the Python/browser suites, the static subpath smoke test, and Gitleaks. [GitHub Actions run](https://github.com/Aventador-LP700/ThreatHuntX/actions/runs/45336221731)
- A loopback check confirmed host port `127.0.0.1:8080`, HTTP 421 for a foreign Host header, and HTTP 403 for a cross-origin replay request.

[Machine-readable fixture results](fixture-results.json) · [Review PR](https://github.com/Aventador-LP700/ThreatHuntX/pull/1)

## Resource measurements

The observed host was Linux x86-64 with 3 Docker-visible CPU cores and 10,452,459,520 bytes of Docker-visible RAM. Docker Engine was 29.9.2, Compose 2.40.3 and Chromium 156.0.8078.79. The images used Python 3.12.14, Node 24.22.3 for the build and Nginx 1.30.5. SQLite reported 3.40.1 inside the API container.

`docker image inspect` reported 141,390,977 bytes for the API and 62,713,232 bytes for the web image. `docker builder du` reported 165.7 MB of build cache after the build. Measurements depend on the storage driver, architecture and retained layers. A repeated build exceeded this environment’s VFS storage budget until its own obsolete build cache was cleared.

After the browser suite and media capture, Linux process status reported 54,792 KiB RSS for Uvicorn and 7,156 KiB and 3,516 KiB for the two Nginx processes. RSS can count shared pages in both processes. The SQLite file measured 172 KiB in that populated lab. The rootless VFS environment reported no Docker cgroup driver. Container-wide peak use and minimum hardware were outside this measurement. The recorded resource values exclude Docker Desktop overhead.

## Artifact and integration scope

- The Community Lab's API and browser checks exercised synthetic events from bundled source projections. The engine evaluates the rule selected for a replay batch. Production-volume evaluation and cross-batch tracking are outside the alpha exercise.
- The 40 Sigma specifications passed pySigma parsing, reference resolution and offline selection checks. Twenty Wazuh event-candidate rules and the decoder passed static XML and regex/fixture checks. Live manager verification is pending. Docker could not finish extracting the official Wazuh 4.14.10 manager image because the validation environment ran out of space.
- The 15 KQL and 15 SPL templates passed offline field and fixture intent checks. Vendor execution is pending. Fixed time bins differ from the local sliding windows.
- Sysmon, Linux audit, Zeek, Suricata, Velociraptor, AWS/Entra and Kubernetes use the [independent setup notes](../docs/full-lab-setup.md) for future live verification. Windows, macOS, and an observed independent beginner usability session are manual pending.
- The [maintainer hand-off](../docs/MAINTAINER_HANDOFF.md) lists the release steps and verifies the applicable gates before a public tag.

## Publication status

The candidate is available through the authenticated repository and review PR. The connected GitHub credential returned HTTP 403 for repository settings updates, including the requested metadata operation. Public visibility, description and topics are pending repository administration. The ready tag also awaits a beginner walkthrough with an independent learner. Issue labels for contribution and triage are configured.
