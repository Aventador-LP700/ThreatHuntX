# Testing and validation

| Status | Meaning |
| --- | --- |
| Documented | A lesson or integration is described with source references. |
| Static-validated | An artifact passed a structural, field mapping or offline selection check. |
| Synthetic-verified | The packaged engine or test successfully evaluated labeled synthetic fixtures. |
| CI-verified | A check ran successfully in a recorded CI job for the identified revision. |
| Integration-verified | The feature ran in its stated target environment and produced verified evidence. |
| Manual pending | Work needs a manual check in the stated tool or platform. |

## Run the local checks

```bash
uv sync --locked
uv run --locked pytest
uv run --locked ruff check
uv run --locked ruff format --check
PYTHONPATH=backend uv run --locked python -m app.cli verify
npm --prefix frontend ci
npm --prefix frontend run build
```

After the lab is healthy, install Playwright Chromium with `npm --prefix frontend exec -- playwright install chromium` and run `npm --prefix frontend run test:e2e`. Set `THX_CHROMIUM` when using an installed Chromium. Set `THX_URL` for a custom loopback port. The static showcase has its own browser mode as described in [the showcase README](../public-demo/README.md).

Ground truth is one expected alert outcome per fixture batch. A scenario has one positive batch, one noisy negative batch and one baseline. TP and FN count positive batches. TN and FP count both control variants. Precision is TP divided by TP plus FP. Recall is TP divided by TP plus FN. A zero denominator is reported as unavailable. The pass rate counts TP plus TN over all fixture batches. These measurements describe the published test corpus. The matrix labels contextual ATT&CK mappings and surfaces unmapped tactics.

[Measured results](../reports/validation-summary.md) · [Coverage matrix](evidence-matrix.md) · [Portable artifact status](PORTABLE_DETECTIONS.md)
