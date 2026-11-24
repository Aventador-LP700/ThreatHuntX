import csv
import io
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .catalog import Catalog
from .models import RunRequest
from .store import Store


def create_app(db_path: Path | None = None, catalog: Catalog | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        application.state.catalog = catalog or Catalog()
        application.state.store = Store(
            db_path or Path(os.getenv("THREATHUNTX_DB", "var/lab.sqlite"))
        )
        application.state.store.initialize(application.state.catalog)
        yield

    api = FastAPI(
        title="ThreatHuntX Community Lab",
        version="0.1.0",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
    )
    api.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "testserver"]
    )

    def scenario_or_404(request: Request, scenario_id: str):
        value = request.app.state.catalog.scenarios.get(scenario_id)
        if not value:
            raise HTTPException(404, "Unknown scenario")
        return value

    def run_or_404(request: Request, run_id: str):
        value = request.app.state.store.get(run_id)
        if not value:
            raise HTTPException(404, "Unknown investigation")
        return value

    @api.middleware("http")
    async def same_origin_writes(request: Request, call_next):
        if request.method == "POST":
            origin = request.headers.get("origin")
            host = request.headers.get("host")
            if origin and (urlsplit(origin).scheme != "http" or urlsplit(origin).netloc != host):
                return JSONResponse(
                    {"detail": "Replay is available from the local lab origin."}, 403
                )
            content_type = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/json":
                return JSONResponse({"detail": "Send an application/json replay request."}, 415)
        return await call_next(request)

    @api.get("/api/health")
    def health(request: Request):
        with request.app.state.store.connect() as db:
            schema = db.execute("PRAGMA user_version").fetchone()[0]
        return {"status": "ok", "schema_version": schema, "synthetic_only": True}

    @api.get("/api/scenarios")
    def list_scenarios(request: Request):
        lab = request.app.state.catalog
        return {"attack": lab.attack, "scenarios": list(lab.scenarios.values())}

    @api.get("/api/scenarios/{scenario_id}")
    def get_scenario(request: Request, scenario_id: str):
        scenario = scenario_or_404(request, scenario_id)
        return {"scenario": scenario, "baseline": run_or_404(request, f"baseline-{scenario_id}")}

    @api.get("/api/coverage")
    def coverage(request: Request):
        return request.app.state.catalog.validation

    @api.post("/api/replay", status_code=201)
    def replay(request: Request, selection: RunRequest):
        scenario = scenario_or_404(request, selection.scenario_id)
        return request.app.state.store.replay(request.app.state.catalog, scenario, selection.mode)

    @api.get("/api/runs")
    def list_runs(request: Request, limit: Annotated[int, Query(ge=1, le=200)] = 50):
        return request.app.state.store.recent(limit)

    @api.get("/api/runs/{run_id}")
    def get_run(request: Request, run_id: str):
        return run_or_404(request, run_id)

    @api.get("/api/runs/{run_id}/export")
    def export_run(request: Request, run_id: str, format: Literal["json", "csv"] = "json"):
        run = run_or_404(request, run_id)
        headers = {"Content-Disposition": f'attachment; filename="threathuntx-{run_id}.{format}"'}
        if format == "json":
            return JSONResponse({"synthetic_only": True, **run}, headers=headers)
        output = io.StringIO()
        fields = [
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
        ]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for event in run["events"]:
            writer.writerow({field: event[field] for field in fields})
        return Response(output.getvalue(), media_type="text/csv", headers=headers)

    return api


app = create_app()
