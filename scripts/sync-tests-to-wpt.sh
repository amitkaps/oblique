#!/usr/bin/env bash
# Mirror tests/oblique-style-matching/ into the vendored .wpt/ checkout so
# `./wpt run` sees the current tests.
#
# The copy is regenerated, never edited: tests/ is the source of truth and
# .wpt/ is gitignored infrastructure. rsync --delete keeps the mirror exact,
# so a renamed or removed test can't linger in .wpt/ and silently keep running
# (a plain `cp -r` never removes anything).
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

./scripts/setup-wpt.sh >/dev/null

dest=.wpt/css/css-fonts/variable-oblique-interop/oblique-style-matching
mkdir -p "$dest"
rsync -a --delete --exclude README.md --exclude '__pycache__' --exclude '*.pyc' \
  tests/oblique-style-matching/ "$dest/"

echo "sync-tests-to-wpt: mirrored to $dest ($(find "$dest" -name '*.html' | wc -l | tr -d ' ') html files)"
