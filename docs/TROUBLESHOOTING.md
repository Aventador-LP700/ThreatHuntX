# Troubleshooting and maintenance

| Symptom | Action |
| --- | --- |
| `Cannot connect to the Docker daemon` | Start Docker Desktop on Windows or macOS. In WSL2, enable Docker Desktop integration for the selected distro. In Linux, use a working rootless Docker context or consult your administrator about socket access. |
| Compose fails because the host port is taken | Add `THREATHUNTX_PORT=8081` to `.env`, rerun Compose and open the matching loopback address. |
| Web or API remains unhealthy | Run `docker compose ps -a` and `docker compose logs api web`. Verify fixture files are present and the database volume is writable by the container. |
| Build reports low space or memory | Check `./scripts/setup.sh doctor` and `docker system df`. Docker Desktop stores layers inside a managed disk image. Adjust resources or free space according to the Docker setup. |
| Network uses a custom trusted CA | Pass the approved PEM to BuildKit with the example below. Keep TLS verification enabled. |
| A lesson has no alert | Compare the selected fixture, outcome, distinct IDs and context in the timeline. It is expected that a clean or noisy fixture raises zero alerts. |
| Settings persist after teardown | Use `./scripts/setup.sh reset` on the running lab and clear site data in the browser separately. |

## Custom build CA

```bash
THREATHUNTX_CA_FILE=/absolute/path/to/approved-ca.pem \
COMPOSE_FILE=compose.yaml:infra/docker/proxy-ca.compose.yaml \
./scripts/setup.sh
```

The build receives the CA through a BuildKit secret mount. Docker registry trust follows the host daemon configuration. Use a certificate from the operator of your network.

## Use or add sample events

Use **Simulate** for bundled replay. For new lab samples, add a reviewed local fixture, run the schema and detection tests and rebuild. The default API reads packaged fixtures. [Write a scenario](HOW_TO_ADD_A_SCENARIO.md)

## Update, back up, and reset

Export investigation results before updating if you want a portable copy. With the lab stopped, switch your checkout to a reviewed tag and run `docker compose up -d --build`. SQLite schema version 1 is initialized on startup, and unsupported versions stop startup with an error. Existing replay batches remain in the project volume and new baselines are seeded. Release notes document migration requirements.

Run `docker compose down` from the same checkout with its project settings to bring down the stack. The optional reset in the launcher clears only the lab database contents. If you choose to remove the entire project data volume, check the project name and exported evidence first and run `docker compose down --volumes` from that project. [Docker Compose documentation](https://docs.docker.com/compose/)
