#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$root"
destination=${1:-build/release}
if [[ -n $(git status --porcelain --untracked-files=all) ]]; then
  printf 'Commit the intended source before packaging a release candidate.\n' >&2
  exit 1
fi
mkdir -p "$destination"
destination=$(cd -- "$destination" && pwd)
commit=$(git rev-parse --verify HEAD)
commit_time=$(git show -s --format=%ct "$commit")
release_version=$(python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
base="threathuntx-$release_version"
make showcase
git archive --format=tar --prefix="ThreatHuntX-$release_version/" "$commit" | gzip -n > "$destination/$base-source.tar.gz"
git archive --format=zip --prefix="ThreatHuntX-$release_version/" --output="$destination/$base-source.zip" "$commit"
tar -C public-demo/dist --sort=name --mtime="@$commit_time" --owner=0 --group=0 --numeric-owner -cf - . | gzip -n > "$destination/$base-showcase.tar.gz"
python3 - "$destination/$base-showcase.zip" <<'PYTHON'
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

root = Path("public-demo/dist")
with ZipFile(sys.argv[1], "w") as archive:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            entry = ZipInfo(path.relative_to(root).as_posix())
            archive.writestr(entry, path.read_bytes(), compress_type=ZIP_DEFLATED)
PYTHON
cp scripts/setup.sh "$destination/setup.sh"
PYTHONPATH=backend uv run --locked python -m app.cli verify > "$destination/fixture-results.json"
uv run --locked cyclonedx-py requirements --output-reproducible infra/docker/requirements.txt --output-file "$destination/python.cdx.json"
npm --prefix frontend sbom --omit=dev --sbom-format=cyclonedx > "$destination/web.cdx.json"
printf '%s\n' "$commit" > "$destination/SOURCE_COMMIT.txt"
cd -- "$destination"
sha256sum "$base-source.tar.gz" "$base-source.zip" "$base-showcase.tar.gz" "$base-showcase.zip" setup.sh SOURCE_COMMIT.txt fixture-results.json python.cdx.json web.cdx.json > SHA256SUMS
printf 'Packaged release candidate %s in %s\n' "$commit" "$destination"
