# Docker Desktop on Windows and macOS

Docker Desktop smoke tests on Windows and macOS are manual pending. The Linux verification record includes the current container versions and measurements. [Validation report](../reports/validation-summary.md)

## Windows with WSL 2

1. Install WSL 2, Git and Docker Desktop. In Docker Desktop settings, select the WSL 2 engine and Linux containers. To run Docker commands inside a WSL distribution, enable its WSL integration setting.
2. Open PowerShell in a writable code directory. Use `docker compose version` and `docker info` to confirm connectivity before the build.

```powershell
git clone https://github.com/Aventador-LP700/ThreatHuntX.git
Set-Location ThreatHuntX
docker compose up -d --build --wait
docker compose ps
Invoke-RestMethod http://127.0.0.1:8080/api/health
```

3. Open <http://127.0.0.1:8080/>. Follow the [first MFA investigation](FIRST_10_MINUTES.md). In **Detection Studio**, compare the three fixtures and try threshold `4` for a missed positive. Open an investigation and export a case report.
4. Use `docker compose logs api web` for startup diagnostics. Run `docker compose down` to stop services. `docker compose exec -T api python -m app.cli reset` clears replay runs and reseeds baselines while the lab is running.

## macOS

Install Docker Desktop for your CPU architecture and wait for the engine to start. From Terminal, use the [Bash or Compose quickstart](GETTING_STARTED.md). Run the same MFA smoke check as on Windows. Record the OS version, CPU architecture and Docker Desktop version with the result.

Use `THREATHUNTX_PORT` in a `.env` file if another local app owns port 8080. Name the test checkout separately so its Docker data and browser origin can be identified before resetting. [Troubleshooting](TROUBLESHOOTING.md)
