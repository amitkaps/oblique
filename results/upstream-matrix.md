# Upstream WPT results (wpt.fyi-sourced)

Generated from `results/upstream.json` by `scripts/render-coverage-docs.py` — do not hand-edit.

**This table is wpt.fyi's own continuous-integration data for pre-existing upstream WPT tests catalogued in [`docs/coverage.md`](../docs/coverage.md), fetched via `scripts/sync-wpt-results.py`.** It is a separate data source from [`results/browser-matrix.md`](browser-matrix.md), which records only tests *this repo* ran locally via the official WPT runner. Never merge the two — one is "we ran this ourselves," the other is "wpt.fyi ran this continuously upstream," and conflating them misrepresents provenance.

**Last synced: 2026-09-18T08:16:34.759289+00:00** (chrome: 153.0.8010.47, firefox: 156.0, safari: 27.0 (22625.1.29.11.27)). If this timestamp looks old, the scheduled sync (see `.github/workflows/sync-wpt-results.yml`) may have stopped — treat stale data as unverified, not as current status.

| Path | Chrome | Firefox | Safari |
|---|---|---|---|
| `css/css-fonts/variations/slnt-variable.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/slnt-backslant-variable.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-slant-1.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-slant-2a.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-slant-2b.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-slant-2c.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-slant-3.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/at-font-face-font-matching.html` | OK | OK | OK |
| `css/css-fonts/variations/font-style-parsing.html` | OK | OK | OK |
| `css/css-fonts/variations/font-style-interpolation.html` | OK | OK | OK |
| `css/css-fonts/animations/font-style-interpolation.html` | OK | OK | OK |
| `css/css-fonts/font-face-style-auto-variable.html` | PASS | PASS | PASS |
| `css/css-fonts/font-face-style-default-variable.html` | PASS | PASS | PASS |
| `css/css-fonts/font-variation-settings-descriptor-01.html` | PASS | PASS | FAIL |
| `css/css-fonts/parsing/font-variation-settings-valid.html` | OK | OK | OK |
| `css/css-fonts/synthetic-oblique-out-of-capabilities-range.html` | PASS | PASS | PASS |
| `css/css-fonts/font-style-angle.html` | OK | OK | OK |
| `css/css-fonts/font-style-sign-function.html` | OK | OK | OK |
| `css/css-fonts/test-synthetic-italic.html` | PASS | PASS | PASS |
| `css/css-fonts/test-synthetic-italic-2.html` | FAIL | PASS | FAIL |
| `css/css-fonts/test-synthetic-italic-3.html` | FAIL | FAIL | FAIL |
| `css/css-fonts/font-synthesis-style.html` | PASS | PASS | PASS |
| `css/css-fonts/font-synthesis-style-oblique-only.html` | FAIL | PASS | FAIL |
| `css/css-fonts/font-synthesis-style-binary.html` | PASS | PASS | PASS |
| `css/css-fonts/italic-oblique-fallback.html` | FAIL | PASS | PASS |
| `css/css-fonts/oblique-last-resort-weight-selection.html` | PASS | FAIL | PASS |
| `css/css-fonts/oblique-request-italic-only-family-no-crash.html` | PASS | PASS | PASS |
| `css/css-fonts/matching/style-ranges-over-weight-direction.html` | PASS | PASS | FAIL |
| `css/css-fonts/matching/range-descriptor-reversed.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-variation-settings-inherit.html` | OK | OK | OK |
| `css/css-fonts/variations/font-descriptor-range-reversed.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-descriptor-range-reversed-002.html` | PASS | PASS | PASS |
| `css/css-fonts/variations/font-parse-numeric-stretch-style-weight.html` | OK | OK | OK |
| `css/css-fonts/font-face-range-order.html` | OK | OK | OK |
| `css/css-fonts/matching/fixed-stretch-style-over-weight.html` | PASS | PASS | FAIL |
| `css/css-fonts/matching/stretch-distance-over-weight-distance.html` | PASS | PASS | FAIL |
| `css/css-fonts/variations/font-shorthand.html` | OK | OK | OK |
