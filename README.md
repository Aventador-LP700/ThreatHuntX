# ThreatHuntX

ThreatHuntX is a free, local threat-hunting education lab. Investigate bundled synthetic records, inspect an alert timeline, and practice response decisions.

```bash
docker compose up -d --build
docker compose ps
curl http://127.0.0.1:8080/api/health
```

Open <http://127.0.0.1:8080/> and select **Start Learning**. In **MFA fatigue**, inspect the clean baseline, replay the positive fixture, examine the alert evidence, and compare the noisy fixture. Finish the quiz to record progress in your browser. Replay uses only packaged log records.

`./scripts/setup.sh` builds the same stack and waits for health on Bash. Run `docker compose down` to stop it, or `./scripts/setup.sh reset` while running to reset local fixture runs.
