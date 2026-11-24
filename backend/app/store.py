import json
import sqlite3
from contextlib import closing, contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from .catalog import Catalog
from .exports import capture_run
from .models import Mode, Scenario


class Store:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def connect(self):
        with closing(sqlite3.connect(self.path, timeout=10)) as connection, connection:
            connection.row_factory = sqlite3.Row
            yield connection

    def initialize(self, catalog: Catalog):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("BEGIN IMMEDIATE")
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                db.execute("""CREATE TABLE runs (
                    id TEXT PRIMARY KEY,
                    scenario_id TEXT NOT NULL,
                    mode TEXT NOT NULL CHECK (mode IN ('baseline', 'positive', 'negative')),
                    created_at TEXT NOT NULL,
                    events TEXT NOT NULL,
                    alerts TEXT NOT NULL
                )""")
                db.execute("CREATE INDEX runs_recent ON runs (created_at DESC, id)")
                db.execute("PRAGMA user_version=1")
            elif version != 1:
                raise RuntimeError(f"Unsupported database schema version {version}")
            self._seed(db, catalog)

    def _seed(self, db: sqlite3.Connection, catalog: Catalog):
        for scenario in catalog.scenarios.values():
            self.insert(db, catalog, scenario, "baseline", f"baseline-{scenario.id}")

    def reset(self, catalog: Catalog):
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("DELETE FROM runs")
            self._seed(db, catalog)

    def insert(
        self, db: sqlite3.Connection, catalog: Catalog, scenario: Scenario, mode: Mode, run_id: str
    ):
        created_at = (
            datetime.now(UTC).isoformat() if mode != "baseline" else "2025-01-01T00:00:00+00:00"
        )
        run = capture_run(scenario, mode, catalog.fixtures[scenario.id, mode], run_id, created_at)
        db.execute(
            """INSERT INTO runs (id, scenario_id, mode, created_at, events, alerts)
            VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO NOTHING""",
            (
                run_id,
                scenario.id,
                mode,
                run["created_at"],
                json.dumps(run["events"]),
                json.dumps(run["alerts"]),
            ),
        )
        return run

    def replay(self, catalog: Catalog, scenario: Scenario, mode: Mode):
        with self.connect() as db:
            return self.insert(db, catalog, scenario, mode, uuid4().hex)

    def _unpack(self, row: sqlite3.Row) -> dict:
        return dict(row) | {
            "events": json.loads(row["events"]),
            "alerts": json.loads(row["alerts"]),
        }

    def get(self, run_id: str) -> dict | None:
        with self.connect() as db:
            row = db.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return self._unpack(row) if row else None

    def recent(self, limit: int = 50) -> list[dict]:
        with self.connect() as db:
            rows = db.execute(
                "SELECT * FROM runs WHERE mode != 'baseline' ORDER BY created_at DESC, id LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._unpack(row) for row in rows]
