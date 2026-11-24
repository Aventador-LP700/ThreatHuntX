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
make showcase
git archive --format=tar --prefix=ThreatHuntX-0.1.0/ "$commit" | gzip -n > "$destination/threathuntx-0.1.0-source.tar.gz"
tar -C public-demo/dist --sort=name --mtime="@$commit_time" --owner=0 --group=0 --numeric-owner -cf - . | gzip -n > "$destination/threathuntx-0.1.0-showcase.tar.gz"
cp scripts/setup.sh "$destination/setup.sh"
printf '%s\n' "$commit" > "$destination/SOURCE_COMMIT.txt"
cd -- "$destination"
sha256sum threathuntx-0.1.0-source.tar.gz threathuntx-0.1.0-showcase.tar.gz setup.sh SOURCE_COMMIT.txt > SHA256SUMS
printf 'Packaged release candidate %s in %s\n' "$commit" "$destination"
