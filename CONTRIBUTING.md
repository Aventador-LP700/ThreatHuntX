# Contributing to ThreatHuntX

Open an issue describing the learning or defensive outcome and how to reproduce it using synthetic data. Check the [roadmap](ROADMAP.md) and the [safety policy](docs/SAFETY_AND_SCOPE.md). See [SECURITY.md](SECURITY.md) for vulnerabilities.

## Developer setup

Use Python 3.12, `uv`, Node 24 and Docker with Compose v2. Install the locked dependencies.

```bash
uv sync --locked
npm --prefix frontend ci
uv run --locked pytest
npm --prefix frontend run typecheck
./scripts/setup.sh
```

Run the browser suite with `npm --prefix frontend exec -- playwright install chromium` and `npm --prefix frontend run test:e2e` from the repository root. If a system Chromium is installed, set `THX_CHROMIUM` to its path. Use `PYTHONPATH=backend` for commands that invoke `app` or `scripts` outside pytest.

## Detection review

Add a reviewed [scenario manifest](docs/HOW_TO_ADD_A_SCENARIO.md) or propose one focused [rule change](docs/HOW_TO_WRITE_A_DETECTION.md). Include the observation, input schema, legitimate alternatives, and positive plus noisy and clean fixtures. Reference official ATT&CK, describe data assumptions, and supply assertions about the exact evidence in a result. Use related mapping status when a fixture shows a proxy signal. Include a learning question when a detector changes the analyst decision.

Run the corresponding generators after changing a manifest or artifact mapping.

```bash
export PYTHONPATH=backend
uv run --locked python -m scripts.build_schemas
uv run --locked python -m scripts.build_detection_artifacts
uv run --locked python -m scripts.build_learning_docs
```

A reviewer checks source fidelity, fixture attribution, suppression impact, limits and test evidence. Status labels should distinguish fixture exercises, static checks and live integration. Keep pull requests focused, explain observable changes, and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
