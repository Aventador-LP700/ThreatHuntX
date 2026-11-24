# Getting started

The Community Lab needs Docker Engine on Linux or Docker Desktop with Compose v2. Docker Desktop must be running before you build. On Windows use Linux containers and the WSL2 backend. See [tested environments and measurements](../reports/validation-summary.md).

```bash
git clone https://github.com/Aventador-LP700/ThreatHuntX.git
cd ThreatHuntX
docker compose up -d --build --wait
docker compose ps
curl -fsS http://127.0.0.1:8080/api/health
```

On Windows PowerShell use `Invoke-RestMethod http://127.0.0.1:8080/api/health` in place of `curl -fsS`. On Bash, `./scripts/setup.sh doctor` shows Docker availability, memory, disk space and the local port check. `./scripts/setup.sh` builds and waits for both services. On a fresh build, Docker downloads the pinned base images and packages. The running application uses the bundled dataset and lessons offline.

Open <http://127.0.0.1:8080/> and select **Start Learning** to open MFA Fatigue. Select **Browse scenario lab** to see all 40 scenarios and their countermeasures. [First 10 minutes](FIRST_10_MINUTES.md) · [Role-based learning paths](curricula/README.md)

To save an assessment of all documented replays, run the terminal lab from the checkout while Compose is running.

```bash
mkdir -p build
./scripts/setup.sh lab all > build/scenario-assessment.md
```

For a single exercise, use its two-digit ID. Add `--format json` to parse the result or `--threshold N` to compare a temporary threshold with the published rule. A mismatch exits with status 1 and includes the fixture and matched record IDs. See the [terminal exercise example](../README.md#run-and-verify-from-the-terminal).

When finished, `docker compose down` stops the lab and keeps the SQLite volume. `./scripts/setup.sh reset` resets lab replay while it is running. Browser progress can be reset through site settings. See [Troubleshooting](TROUBLESHOOTING.md) for upgrades, port conflicts and certificates.

For presentation platform setup and the reviewer smoke steps, see [Windows and macOS](WINDOWS_AND_MACOS.md).
