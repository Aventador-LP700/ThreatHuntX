"""Format downloads from packaged or persisted synthetic evidence."""

import csv
import io
import re

from fastapi.responses import JSONResponse, Response

from .detect import correlate
from .models import Event, Mode, Scenario

EVENT_FIELDS = (
    "event_timestamp",
    "source",
    "host",
    "user",
    "event_id",
    "action",
    "outcome",
    "record_id",
    "alert_id",
    "evidence_reference",
)


def capture_run(
    scenario: Scenario, mode: Mode, events: list[Event], run_id: str, created_at: str
) -> dict:
    alerts = correlate(scenario, events, run_id)
    alert_by_record = {record: alert.id for alert in alerts for record in alert.evidence}
    return {
        "id": run_id,
        "scenario_id": scenario.id,
        "mode": mode,
        "created_at": created_at,
        "events": [
            event.model_dump(mode="json") | {"alert_id": alert_by_record.get(event.record_id)}
            for event in events
        ],
        "alerts": [alert.model_dump(mode="json") for alert in alerts],
    }


def sample_run(scenario: Scenario, mode: Mode, events: list[Event]) -> dict:
    run_id = f"baseline-{scenario.id}" if mode == "baseline" else f"sample-{scenario.id}-{mode}"
    return capture_run(scenario, mode, events, run_id, events[0].event_timestamp.isoformat())


def safe_cell(value):
    if isinstance(value, str) and (
        value.startswith(("\t", "\r", "\n")) or re.match(r"^[\s\ufeff]*[=+\-@＝＋－＠]", value)
    ):
        return "'" + value
    return value


def export_run(run: dict, format: str) -> Response:
    headers = {"Content-Disposition": f'attachment; filename="threathuntx-{run["id"]}.{format}"'}
    if format == "json":
        return JSONResponse({"synthetic_only": True, **run}, headers=headers)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=EVENT_FIELDS)
    writer.writeheader()
    for event in run["events"]:
        writer.writerow({field: safe_cell(event[field]) for field in EVENT_FIELDS})
    return Response(output.getvalue(), media_type="text/csv", headers=headers)
