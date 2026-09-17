#!/usr/bin/env bash
# Vendor a minimal, scoped WPT checkout into .wpt/ so `./wpt run` works
# without depending on an external, separately-maintained WPT clone.
#
# .wpt/ is fetched infrastructure, not repo content — it is gitignored and
# never committed. This does not contradict spec.md's "No WPT checkout
# included": that decision scopes to "not committed," not "never present
# locally." Idempotent: if .wpt/ already exists, this is a no-op so
# contributors and CI can call it unconditionally.
#
# Sparse-checkout scope: css/css-fonts (the tests themselves), tools (the
# wpt runner), resources (testharness.js and friends, required by the
# runner regardless of whether a given test is a reftest or testharness
# test), and docs (NOT test docs — `./wpt`'s own CLI entry point reads
# docs/commands.json at startup to register its subcommands, and fails with
# a bare FileNotFoundError without it; confirmed by running `./wpt run
# --help` against the narrower scope). This repo's own tests carry their
# own fonts under tests/*/resources/ rather than referencing WPT's shared
# /fonts/, so that directory is deliberately NOT in scope — extend the
# sparse-checkout set below (with a comment explaining why) if a future
# test needs it.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ -d .wpt ]; then
  echo "setup-wpt: .wpt/ already exists, skipping clone"
  exit 0
fi

git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/web-platform-tests/wpt.git .wpt

cd .wpt
git sparse-checkout set css/css-fonts tools resources docs

echo "setup-wpt: done. See README.md's 'Running the tests' section for next steps."
