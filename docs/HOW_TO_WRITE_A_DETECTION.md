# Write and tune a detection

State a testable hypothesis, a required source, the fields from that source, and a concrete expected analyst decision. Start with an observation that can be falsified using a clean example. Add a noisy example that resembles the target behavior, then define the narrowest defensible selection or suppression.

The lab supports exact matching, alternatives, case-insensitive string substring or prefix/suffix matching, and integer `gte`. Rules select candidate events, skip explicit exclusions and count evidence in a sliding window by group. An optional `distinct` field controls counting. Choose a stable grouping field and test missing values, retries, separate actors and boundary times. Replay both fixtures in the app and verify timestamps and evidence IDs in the investigation.

For the MFA rule, two retries for one challenge should count once. An enrollment test carries a reviewed change-context field. The positive fixture raises an alert after three distinct denied push challenges in five minutes. Check how the same selection maps into Sigma and how the vendor templates handle fixed bins.

[Rule tests](../backend/tests/test_catalog.py) · [Portability](PORTABLE_DETECTIONS.md) · [Contributor workflow](../CONTRIBUTING.md)
