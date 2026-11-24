# ThreatHuntX Community alpha validation

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

## Resource measurements

The observed host was Linux x86-64 with 3 Docker-visible CPU cores and 10,452,459,520 bytes of Docker-visible RAM. Docker Engine was 29.9.2, Compose 2.40.3 and Chromium 156.0.8078.79. The images used Python 3.12.14, Node 24.22.3 for the build and Nginx 1.30.5. SQLite reported 3.40.1 inside the API container.

`docker image inspect` reported 141,390,977 bytes for the API and 62,713,232 bytes for the web image. `docker builder du` reported 165.7 MB of build cache after the build. Measurements depend on the storage driver, architecture and retained layers. A repeated build exceeded this environment’s VFS storage budget until its own obsolete build cache was cleared.

After the browser suite and media capture, Linux process status reported 54,792 KiB RSS for Uvicorn and 7,156 KiB and 3,516 KiB for the two Nginx processes. RSS can count shared pages in both processes. The SQLite file measured 172 KiB in that populated lab. The rootless VFS environment reported no Docker cgroup driver. Container-wide peak use and minimum hardware were outside this measurement. The recorded resource values exclude Docker Desktop overhead.

## Artifact and integration scope

- The Community Lab's API and browser checks exercised synthetic events from bundled source projections. The engine evaluates the rule selected for a replay batch. Production-volume evaluation and cross-batch tracking are outside the alpha exercise.
- The 40 Sigma specifications passed pySigma parsing, reference resolution and offline selection checks. Twenty Wazuh event-candidate rules and the decoder passed static XML and regex/fixture checks. Live manager verification is pending.
- The 15 KQL and 15 SPL templates passed offline field and fixture intent checks. Vendor execution is pending. Fixed time bins differ from the local sliding windows.
- Sysmon, Linux audit, Zeek, Suricata, Velociraptor, AWS/Entra and Kubernetes use the [independent setup notes](../docs/full-lab-setup.md) for future live verification. Windows, macOS, and an observed independent beginner usability session are manual pending.
- The [maintainer hand-off](../docs/MAINTAINER_HANDOFF.md) lists the release steps and verifies the applicable gates before a public tag.
