# Add or update a scenario

Start with an issue that identifies the defensive learning goal and its supporting telemetry. Use the existing numbered scenario that best fits the proposal. Discuss catalog expansion before assigning a new ID. Keep the distinction between the learning domain and the ATT&CK tactics recorded for the technique.

1. Define a short scenario in `scenarios/manifests/NN.json`. Include the title, source, observation, response, preventive controls, honest limitations and two or three knowledge questions. Keep the rule scoped to source fields.
2. Verify an active ATT&CK identifier against the [pinned metadata](../scenarios/attack/version.json). Use related status for proxy signals and write a rationale. If metadata changes, check the subset against the pinned official STIX file.
3. Create `NN.baseline.json`, `NN.positive.json` and `NN.negative.json` in `scenarios/fixtures/`. Use `threathuntx.synthetic.v1`, appropriate source keys, reserved example data and unique record IDs. Keep timestamps stable.
4. Verify the rule triggers from the required observations, and explain why a similar benign batch does not trigger. Link matched events and the downstream decision. Rebuild portable artifacts and lessons.

[Fixture schema](../scenarios/schema/fixture-record-v1.json) · [Scenario schema](../scenarios/schema/scenario-v1.json) · [MFA manifest](../scenarios/manifests/02.json) · [Contributing](../CONTRIBUTING.md)
