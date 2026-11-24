# Investigations and reports

Open **Investigation Workspace** to filter the last 50 replays by case, host, actor, source and outcome. Open a case to search record IDs and normalized fields. Expanded timeline events provide pivots for their host, actor and source, plus the original evidence reference and linked alert ID.

In **Case analysis**, record a hypothesis, a triage decision, notes and a response. Saving writes to the current browser’s storage under `threathuntx.case.v1.<case-id>`. Use **Case JSON** for a structured snapshot and **Case CSV** for one row per evidence record with case metadata. **Printable report** renders the case, evidence, decision, mitigation and limitations for the browser's print or Save as PDF action.

A report includes the full replay evidence even when a timeline filter is active. The replay timestamp records the batch. Individual event timestamps come from the fixture. Unsaved input can be included in an export. Save a case to retain notes through a page reload. Keep personal or operational data out of training cases and exports.

CSV exports neutralize values that spreadsheet software could treat as formulas. Notes render as text on the case and printable report pages. The application serves the same browser-only case editor in the read-only showcase.

[Case report JSON Schema](../scenarios/schema/case-report-v1.json) · [Normalized event schema](../scenarios/schema/event-v1.json) · [Privacy](PRIVACY.md)
