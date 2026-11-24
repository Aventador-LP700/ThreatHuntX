# Maintainer hand-off

## Triage and review

Use `needs reproduction` for a bug without a fixture-driven reproduction, `detection` for rules or field mappings, and `documentation` for learning and deployment guidance. Mark small, well-scoped issues `good first issue` and use `help wanted` for reviewed work. Route security issues through the [private disclosure policy](../SECURITY.md) and keep evidence redacted.

For each pull request, review its source fidelity, benign alternatives, data provenance and safety. Require fixtures and precise assertions for rule changes. Run the matching checks from [Testing and validation](TESTING_AND_VALIDATION.md). A successful fixture test supports its published synthetic scope.

## Refresh dependencies and references

Use separate changes for Python locks, npm locks, Docker image digest pins and upstream ATT&CK metadata. Regenerate hashed `infra/docker/requirements.txt` with `uv export --locked --no-dev --no-emit-project --no-header`. Rerun the full lab and static showcase on the new base images and inspect security scan and SBOM output. Verify upstream terms when bundling new third-party material.

## Prepare a release

1. Verify local and CI evidence on the exact revision. Run the README from a fresh checkout. Record remaining live integration and platform work.
2. Review the case studies, media, test outputs, disclosure links and third-party notices. Ask a new learner to use the first-hunt instructions and capture any friction.
3. Make sure `scripts/setup.sh` references the release tag and update release notes. Use `./scripts/package-release.sh` on Linux to prepare the candidate and checksums.
4. After approval, merge the reviewed revision and publish the `v0.1.0` release. Use repository settings to set public visibility and configure description and topics with an admin credential. Check the public clone and artifact downloads from a signed-out session.

Keep Pages hosting optional. The static artifacts served by Pages contain educational sample data. Keep the writable Community Lab on localhost. [Release notes](RELEASE_NOTES.md) · [Roadmap](../ROADMAP.md)
