# FAQ

## What does a replay do?

Replay inserts generated log records and applies a deterministic rule to that batch. This makes it possible to compare expected alerts and false-positive boundaries consistently.

## Do I need a SIEM or account?

The default lab uses Docker, a browser and SQLite. The documented analyst stack is independent. The read-only showcase is an optional static build. [Three tiers](REFERENCE_ARCHITECTURE.md)

## Why is a record omitted from alert evidence?

It may lack a selection field, be suppressed by reviewed context, repeat a distinct observation, or fall outside the earliest qualifying window. Inspect the alert group and candidate fields. [Rule semantics](TESTING_AND_VALIDATION.md)

## Can I keep my results after stopping?

The default Compose volume preserves local replays. Learning completion and theme are stored in your browser. Export a run or learning report to keep a portable copy. [Privacy](PRIVACY.md)
