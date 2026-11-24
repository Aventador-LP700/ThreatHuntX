# Privacy

The application makes requests to its own origin to load lessons and run bundled fixtures. It includes no sign-up, analytics, tracking cookies or background vendor calls. Reference links to MITRE and GitHub are opened by the learner. Dependency downloads occur at build time.

Theme and completion are stored in browser local storage under `threathuntx.theme` and `threathuntx.progress.v1`. Clear site data to reset them. The static showcase also keeps opened sample batches in memory for that page session. Downloads contain learning titles, technique IDs and completion timestamps, or the corresponding synthetic evidence.

The Community Lab records replay batches in Docker volume `threathuntx_lab-data` under the default project name. Run `./scripts/setup.sh reset` to reset the lab database. Nginx and FastAPI write request logs to the local Docker logging driver. Review the Docker driver configuration for retention.
