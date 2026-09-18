# Summary

This repo tracks whether CSS Fonts 4 `slnt`/`ital` variable-axis matching
for `font-style: oblique`/`italic` is interoperable across Chrome, Firefox,
and Safari. It catalogs existing upstream WPT coverage
([`docs/coverage.json`](coverage.json)), syncs live per-engine results from
[wpt.fyi](https://wpt.fyi) and this repo's own WPT runs, and supplies new
tests for the gaps that catalog confirms.

For the full narrative — every claim sourced, every wrong turn documented —
see [`docs/investigation-log.md`](investigation-log.md). This file is the
terse version; the live dashboard is
[oblique.amitkaps.com](https://oblique.amitkaps.com).

## Confirmed gaps

| Gap | Status | Why | Test |
|---|---|---|---|
| Auto-derived `slnt` range + bare `oblique`/`italic` keyword | ✅ closed — tier 1 | Cairo's real-world bug shape: no explicit `@font-face font-style` descriptor, UA default angle falls outside the font's own range | [`auto-range-default-angle`](../tests/font-style-oblique/auto-range-default-angle.html) |
| Same-family `normal` face + bare `oblique` face | ❌ open — tier 2, priority 1 | vizchitra-fonts ships Cairo as two separate `@font-face` blocks specifically to avoid engines picking the wrong face; no test proves the hazard | not yet written |
| `font-style` paired with an explicit `font-variation-settings` axis override | ❌ open — tier 2, priority 2 | Spec-recommended author pattern for fallback compatibility, currently unverified | not yet written |
| A font exposing both `slnt` and `ital` together | ❌ open — tier 3, priority 3 | No known real-world font combines both axes — spec-completeness, not evidence of impact | not yet written |

## Live findings

| Finding | Chrome | Firefox | Safari | Source |
|---|---|---|---|---|
| `italic` on an `ital`-only font (no `slnt`) sets `ital`, no spurious synthesis | ❌ FAIL | ✅ PASS | not run | [`results/browser-matrix.md`](../results/browser-matrix.md) — this repo's own test, reproduces WebKit #209565's documented failure mode |
| Three `matching/` precedence tests (stretch/weight/style search direction) | ✅ PASS | ✅ PASS | ❌ FAIL | wpt.fyi CI, see [`results/upstream-matrix.md`](../results/upstream-matrix.md) — a live, dated, cross-engine finding, not a coverage gap |

## `ital`-axis upstream coverage

Zero. No test anywhere in upstream WPT's `css/css-fonts` tree exercises the
`ital` variation axis in any form — confirmed by a full-tree grep, not
sampling (see `docs/coverage.json`'s `ital_axis_gap`). This repo's
`tests/ital-axis/` exists specifically to fill that gap.

## Deferred

Retaining sync history over time (a changelog of past `results/upstream.json`
snapshots) was considered and deliberately deferred — it cuts against this
page's goal of staying short and glanceable. `results/upstream.json` is
still overwritten, not appended, on every sync; only the current snapshot's
`synced_at` timestamp is shown. Revisit if "how has this changed over time"
becomes a real question worth answering.
