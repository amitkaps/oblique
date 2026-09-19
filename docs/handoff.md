# Project state and how to continue

Written for whoever picks this up next, after a long working session. It says where the
project stands, how the pieces fit, how to run each step, what was learned (including what
was retracted), and what is open. Narrative detail lives in
[`investigation-log.md`](investigation-log.md); the short public version is
[`summary.md`](summary.md); the live page is <https://oblique.amitkaps.com>.

## What this project is

An interop test suite for CSS Fonts 4 oblique/italic matching (`font-style`, the `slnt` and
`ital` variable axes) across Chrome, Firefox and Safari, aimed at a possible WPT/interop
proposal. **Nothing has been upstreamed and no WPT PR is open.** Sibling project
`vizchitra-fonts` (`/code/vizchitra-fonts`, page `fonts.vizchitra.com/compat`) measured the
real-world bugs this repo generalises.

## The pipeline, in one picture

```
reference/cases/matrix.json        rows (use-site requests) x columns (@font-face descriptors)
        |
reference/  (JS, Node 24)          independent CSS Fonts 4 matching: expected() -> allowed outcomes
        |  node src/cli.mjs generate
tests/oblique-style-matching/      matrix-{row}-{column}.html (+ refs) and matrix.manifest.json
        |
   +----+-----------------------------+---------------------------+
   |                                  |                           |
wpt run (Chrome, Firefox)     scripts/safari-replay.py     scripts/survey.py (lean, all 3)
   |                                  |                           |
   +---- results/browser-matrix.md ---+                    results/survey.json
                     |                                          |
              reference compare  <-------------------------------+
                     |
scripts/generate-site-data.py + site/  ->  docs/  (GitHub Pages, oblique.amitkaps.com)
```

Key rule: **the browser is the system under test.** The reference decides what each cell
should do; it never asks a browser. The generated files are never edited by hand.

## Where things are

| Path | What |
|---|---|
| `reference/` | the JS reference implementation, its tests, `cases/matrix.json`, the saved spec text. See `reference/README.md` |
| `tests/oblique-style-matching/` | the single candidate folder for a WPT PR: 21 generated tests (`matrix-*`) plus 14 hand-written regression tests, fonts in `resources/` |
| `tests/oblique-style-matching/resources/Cairo.var.subset.ttf` | real Cairo (OFL, no Reserved Font Name) subset to `OBLIQUE`, both axes kept; rebuilt by `build-cairo-subset.sh`. The tests render the capital `I` |
| `results/browser-matrix.md` | this repo's own results (the only writer is `scripts/record-results.py` or `safari-replay.py --record`) |
| `results/upstream.json` | wpt.fyi results, synced daily by CI. **Never merged with the file above** (provenance) |
| `results/survey.json` | measured lean per cell per engine (`scripts/survey.py`) |
| `docs/coverage.json` | audit of upstream WPT coverage and this repo's gaps; `coverage.md` is rendered from it |
| `site/`, `docs/index.html` | zero-JS static page (Python renders HTML, Vite bundles CSS); `docs/` is the deploy directory |

## How to run each step

```
# reference
cd reference && node --test                     # 33 tests
node src/cli.mjs generate                       # write tests + manifest (--check: fail if stale)
node src/cli.mjs classes                        # which branch/outcome each cell exercises
node src/cli.mjs compare                        # expected vs recorded results

# run the tests
./scripts/setup-wpt.sh                          # once: sparse WPT checkout in .wpt/ (gitignored)
./scripts/sync-tests-to-wpt.sh                  # after ANY change under tests/ (rsync --delete)
echo "cryptography<=48.0.1" > /tmp/wpt-constraints.txt     # wpt's venv build needs this cap
cd .wpt && PIP_CONSTRAINT=/tmp/wpt-constraints.txt ./wpt run chrome css/css-fonts/variable-oblique-interop/ \
  --binary="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --webdriver-binary=_venv3/bin/chrome/chromedriver --log-wptreport=../results/latest-chrome.json
# firefox: same with `run --yes firefox`, --binary=/Applications/Firefox.app/Contents/MacOS/firefox, geckodriver
uv run scripts/record-results.py results/latest-chrome.json     # never hand-edit browser-matrix.md
uv run --with pillow scripts/safari-replay.py --record          # Safari (see below)
uv run --with pillow scripts/survey.py                          # lean measurements, all three
cd .wpt && ./wpt lint css/css-fonts/variable-oblique-interop/oblique-style-matching/

# publish the site
uv run scripts/render-coverage-docs.py && uv run scripts/generate-site-data.py
cd site && pnpm run build && cd .. && rm -rf docs/assets && cp -r site/dist/* docs/
```

`results/latest-*` are ignored scratch reports; only the curated `browser-matrix.md` is tracked.
`git pull` first: a daily bot commit rewrites `docs/index.html` and `results/upstream.*`.

## Safari: use the replay, not `wpt run`

`wpt run safari` is unreliable here (about 20 of 44 tests reported FAIL although test and
reference are pixel-identical, one really failing test passed, five flipped between identical
runs), so it is not used. `scripts/safari-replay.py` does what a reftest runner does through
`safaridriver` and compares pixels exactly; every result must agree across repeats. Rows are
recorded as "no (safaridriver automation)" with a note pointing at investigation-log section 11.

If a session times out ("session not created ... timed out"): tick Safari > Develop > Allow Remote
Automation, quit Safari fully, and check System Settings > Privacy & Security > Automation for the
terminal app (this was the fix here). Safari 27.0 on macOS 15.8. A real-device manual reading,
as vizchitra-fonts keeps, was never done.

## What the reference decides

Expectations are **sets of allowed outcomes** (`upright`, `axis slnt=n`, `synth`) in three statuses:

- **specified**: one testable outcome. A reftest with one `match` reference.
- **constrained**: several outcomes, or synthesis, are allowed but something is forbidden.
  Several `match` references (any one passes), or `mismatch` references for what is forbidden.
- **unspecified**: the spec excludes nothing testable. No test; only observed.

Grid today (5 columns A-E x 6 rows 1-6 = 30 cells): 17 specified, 4 constrained, 9 unspecified.
References are plain faces with the axis pinned via `font-variation-settings`, so they never
depend on the descriptor under test. **No generated test sets `font-synthesis`**: the spec
synthesizes only when a face is missing, so forcing it off would hide an engine that synthesizes
on top of a matched face.

Spec rules that decide cells (all quoted in `reference/spec/css-fonts-4-excerpts.txt`):
bare `oblique` is a one-point range at 14deg; `normal` is `oblique 0deg`; a descriptor "is used in
place of the style implied by the underlying font data" (so a `normal`-declared face never reaches
the axis); CSS angle and OpenType `slnt` have opposite signs (`oblique 11deg` = `slnt -11`);
`auto` is "selected as if normal" with "clamping does not occur"; italic "angle and direction of
slant is unspecified"; synthesis is "will be generated" (2.3) but "may create" (5.2).

## Findings (Chrome 153, Firefox 156, Safari 27.0)

**Confirmed, spec-decided failures** (cells E2, E3, E5: `italic`, bare `oblique`, `<em>` against a
face declared `oblique -11deg 11deg`, default synthesis): the axis must clamp to -11 and nothing may
be synthesized on top. Firefox passes. Chrome stacks a synthetic skew on the axis (36px lean vs the
expected 16px). Safari stacks for bare `oblique` and, for `italic`/`<em>`, gives a pure synthetic skew
with no axis at all (21px). Independently measured in `vizchitra-fonts`.

**Retracted** (kept in `coverage.json`, marked withdrawn): (1) "Chrome fails an italic-declared face on
a `slnt`-only font": the spec permits both upright and slanted; (2) "Chrome and Safari fail `oblique
11deg` against a normal face": synthesis is permitted, not required. Earlier tables had also lumped the
bare-`oblique` column with the italic one; bare `oblique` leans for a `normal` request because it is a
14deg point range.

**Cross-check:** the reftests and the independent lean measurement agree in every cell (27 agree, 3
diverge, none `reference-suspect`). Older hand-written results (e.g. `italic-no-extra-synthesis`,
`ital-slnt-independence-dual-axis`, which use an `ital`-axis font) were **not** re-judged by the reference.

**Validation of the reference:** unit tests from the spec's own step order, and upstream WPT tests
checked by what they *intend* (several fail on some engine). `oblique-last-resort-weight-selection` is a
recorded **known disagreement** (the test assumes italic is a 14deg slope; the text says 11deg).
`italic-oblique-fallback` matches only with the published resolution csswg-drafts#9389, which the
Editor's Draft text has not caught up with (`RESOLUTIONS` in `match.mjs`, off by default).

## Decisions worth remembering

- Fonts: real Cairo subset, not a synthetic one; WPT itself ships `Inter.var.subset.ttf` the same way.
  Ask before adding any other font, and prefer an OFL subset that shows a real-life use.
- Ambiguity is three-valued, not resolved by picking the majority browser behaviour.
- Spreadsheet addresses (`A1`, `B2`) are **permanent labels**: append new rows/columns, never
  renumber. File names use slugs: `matrix-{row}-{column}` (hyphen-free slugs, e.g. `obl11`, `oblrange`).
- Provenance is never mixed: this repo's `wpt run` results vs wpt.fyi results stay in separate files.
- Claims are measured first. Several earlier claims were wrong and are documented, not deleted.

## Open items

1. **Grow the grid.** Proposed, not built: rows `oblique 10deg`, `12deg`, `-8deg`, `-11deg`, `45deg`
   (past the font's range) and synthesis rows (`font-synthesis-style: none`, `font-synthesis: none`,
   `oblique-only`); columns `oblique 0deg 11deg`, `oblique 5deg 20deg`, `oblique -11deg 0deg`
   (about 14 x 8). Review as a table before generating.
2. **Multi-face families** (the real 11deg ordering among several faces) are implemented and unit-tested
   but not browser-tested: telling faces apart on screen needs more fonts. **Ask before adding one.**
3. **Re-judge the hand-written `ital`-axis tests** with the reference; their "Chrome fails" claims may need
   the same reclassification as the two withdrawn ones. Also `normal-plus-bare-oblique-same-family` (the
   one unbuilt gap in `coverage.json`).
4. **Cause of `wpt run safari` failing** was not isolated (a loading race was suspected and ruled out).
5. **Real-device Safari** (iPhone, older versions) has never been tested; vizchitra-fonts saw version-dependent
   behaviour (18.7 vs 27.0).
6. **Upstreaming:** no PR is open; the site says so. Filing the spec question (synthesis "will"/"may"; italic
   on a `slnt`-only font; `auto` semantics; the 14deg-vs-11deg italic slope) with CSSWG is a natural step.
7. Site and repo are consistent as of the last commit; `reference compare` is not yet shown on the site
   (the page shows reftest results plus "observed" markers).

## Gotchas

- `node --test` (no directory argument) on Node 24; `node --test test/` fails.
- zsh: `echo "=====..."` is parsed as a command; the macOS shell has no `timeout`.
- `wpt run` needs `PIP_CONSTRAINT` (cryptography cap) here; Firefox needs `--yes`; never pass
  `--install-fonts`.
- Headless Chrome narrower than ~500px screenshots badly (a viewport artifact, not a layout bug).
- Safari screenshots carry a dark line in the top few pixels; the scripts crop 8px.
- After changing anything under `tests/`, re-run `sync-tests-to-wpt.sh`, or `.wpt/` keeps stale files.
