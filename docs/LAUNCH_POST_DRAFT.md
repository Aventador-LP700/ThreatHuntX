# LinkedIn launch post draft

I built ThreatHuntX to give learners a practical way to go from a security signal to a defensible incident assessment without needing a company SIEM or a cloud account.

The Community Lab starts with `docker compose up -d --build`. A first investigation walks through MFA fatigue. You read a clean baseline, replay generated prompts, open the three records behind the alert, and compare an approved enrollment and retry sequence before deciding what to do next.

The project has 40 fixture-driven exercises across identity, Windows, cloud, CI/CD, Kubernetes and other domains. Docker Compose runs Vue, FastAPI, and SQLite locally. The starter browser suite covers 10 complete investigations, and the repository includes original Sigma specs, Wazuh event-candidate examples and review-only KQL/SPL templates.

If you teach a SOC course, write detections or are learning to investigate alerts, I’d welcome feedback on the first lesson, the evidence views and the contribution workflow. [ThreatHuntX on GitHub](https://github.com/Aventador-LP700/ThreatHuntX)
