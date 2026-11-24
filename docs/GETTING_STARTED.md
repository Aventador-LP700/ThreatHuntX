# Getting started

The Community Lab needs Docker Engine on Linux or Docker Desktop with Compose v2. Docker Desktop must be running before you build. On Windows use Linux containers and the WSL2 backend. See [tested environments and measurements](../reports/validation-summary.md).

```bash
git clone --branch community-v2-workspace https://github.com/Aventador-LP700/ThreatHuntX.git
cd ThreatHuntX
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1:8080/api/health
```

On Windows PowerShell use `Invoke-RestMethod http://127.0.0.1:8080/api/health` in place of `curl -fsS`. On Bash, `./scripts/setup.sh doctor` shows Docker availability, memory, disk space and the local port check. `./scripts/setup.sh` builds and waits for both services. On a fresh build, Docker downloads the pinned base images and packages. The running application uses the bundled dataset and lessons offline.

Open <http://127.0.0.1:8080/> and select **Start Learning** to open MFA fatigue. Then follow [First 10 minutes](FIRST_10_MINUTES.md) or [choose a role-based pathway](curricula/README.md).

When finished, `docker compose down` stops the lab and keeps the SQLite volume. `./scripts/setup.sh reset` resets lab replay while it is running. Browser progress can be reset through site settings. See [Troubleshooting](TROUBLESHOOTING.md) for upgrades, port conflicts and certificates.

For presentation platform setup and the reviewer smoke steps, see [Windows and macOS](WINDOWS_AND_MACOS.md).
