# Running the tests

Everything is a `mise run` task (`mise tasks` lists them). Node 24, pnpm, Python 3.12 and uv are pinned
in `.mise.toml`.

```
mise run install                     # once: pnpm install (vite)

# the reference implementation and the generated tests
mise run test                        # unit tests (50)
mise run generate                    # regenerate tests/oblique-style-matching/matrix/ from reference/cases/matrix.json
mise run compare                     # expected vs recorded browser results

# WPT (a sparse checkout in .wpt/, gitignored)
mise run wpt-setup                   # once
mise run wpt-lint                    # sync the tests into .wpt/ and run `wpt lint`
mise run wpt-chrome                  # wpt run in local Chrome, then record the results
mise run wpt-firefox                 # same for Firefox
mise run safari                      # Safari, see below
mise run survey                      # measure the lean of every cell in all three engines

# the site
mise run site-dev                    # serve with hot reload
mise run site                        # build into dist/
```

After any change under `tests/`, `wpt-sync` (or any `wpt-*` task, which sync first) refreshes `.wpt/`.
`generate` rewrites `matrix/` completely; never edit those files by hand.

## Results files

`results/browser-matrix.md` is this repo's own runs: rows are appended by `scripts/record-results.py`
(wpt) and `scripts/safari-replay.py --record` (Safari), never by hand, and the last row for a test and
engine wins. `results/survey.json` holds the measured lean per cell per engine. The site reads both at build
time and fails the build if the manifest, the files on disk and the recorded results disagree.

## Chrome and Firefox

`scripts/wpt-run.sh` uses the locally installed browsers (`/Applications/Google Chrome.app`,
`/Applications/Firefox.app`) rather than downloading copies, and caps `cryptography<=48.0.1` through
`PIP_CONSTRAINT`: wpt's first run builds a venv and cannot build the newest `cryptography` from source on a
machine without a Rust/OpenSSL toolchain. Firefox is run with `--yes` because otherwise the first run waits
forever on an interactive OpenH264 prompt. Never pass `--install-fonts`; on macOS it can stall waiting on a
permission prompt, and these tests use embedded web fonts.
`wpt run` exits nonzero whenever a test fails, so the script records the report regardless and fails only when
no report was written.

## Safari

Do not use `wpt run safari` for results. On Safari 27.0 it reported FAIL for about 20 of 44 tests whose test
and reference screenshots are pixel-identical, passed one test that really fails, and 5 results flipped
between identical runs. The cause inside wptrunner was not isolated; a loading race was ruled out (10 of 10
correct with both loading patterns).

`mise run safari` (`scripts/safari-replay.py`) does what a reftest runner does through `safaridriver`
directly: load the test, wait for `reftest-wait` to clear, screenshot, load each reference, compare pixels
exactly (`match` must be identical, every `mismatch` must differ). It repeats three times and records a
result only if every repetition agrees. Recorded rows say "no (safaridriver automation)" in the `real_device`
column: desktop Safari through `safaridriver`, not a physical device. Its screenshots carry a dark line in the
top few pixels, so the scripts crop 8px.

One-time setup: Safari > Settings > Advanced > Show features for web developers, then Develop >
Allow Remote Automation (or `sudo safaridriver --enable`). If a session fails with "session not created ...
timed out", quit Safari completely (Cmd-Q) and check System Settings > Privacy & Security > Automation for the
terminal app; that was the fix here.

## Gotchas

- `node --test` takes files, not a directory, on Node 24 (`pnpm test` passes the glob).
- Headless Chrome narrower than about 500px screenshots badly: a viewport artifact, not a layout bug.
- zsh parses `echo "====="` as a command; macOS has no `timeout`.
- `pnpm build` prints a warning that `/Cairo.var.subset.ttf` "didn't resolve at build time": the site's
  render plugin emits that file itself, so it is harmless.

## Deploy

CI (`.github/workflows/ci.yml`) runs the tests, checks the generated files are current, lints with
`wpt lint`, builds the site, and on `main` publishes `dist/` to GitHub Pages at
<https://oblique.amitkaps.com> (`site/public/CNAME`). Nothing generated is committed.
