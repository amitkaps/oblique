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
| Auto-derived `slnt` range + bare `oblique`/`italic` keyword | ✅ closed — tier 1 | Cairo's real-world bug shape: no explicit `@font-face font-style` descriptor, UA default angle falls outside the font's own range | [`auto-derived-range-clamp`](../tests/oblique-style-matching/auto-derived-range-clamp.html) |
| Same-family `normal` face + bare `oblique` face | ❌ open — tier 2, priority 1 | vizchitra-fonts ships Cairo as two separate `@font-face` blocks specifically to avoid engines picking the wrong face; no test proves the hazard | not yet written |
| `font-style` paired with an explicit `font-variation-settings` axis override | ✅ closed — tier 1 | Grounded in §7.2's explicit precedence ordering; PASS on Chrome/Firefox, confirming both implement it correctly | [`style-plus-explicit-variation-settings`](../tests/oblique-style-matching/style-plus-explicit-variation-settings.html) |
| A font exposing both `slnt` and `ital` together | ✅ closed — tier 1 | Closing it surfaced a real Chrome-only finding, not a clean pass — see Live findings below | [`ital-slnt-independence-dual-axis`](../tests/oblique-style-matching/ital-slnt-independence-dual-axis.html) |

## Live findings

| Finding | Chrome | Firefox | Safari | Source |
|---|---|---|---|---|
| `italic` on an `ital`-only font (no `slnt`) sets `ital`, no spurious synthesis | ❌ FAIL | ✅ PASS | not run | [`results/browser-matrix.md`](../results/browser-matrix.md) — reproduces WebKit #209565's documented failure mode |
| `italic`/`oblique` each activate only their own axis on a font with both `slnt` and `ital` | ❌ FAIL | ✅ PASS | not run | [`results/browser-matrix.md`](../results/browser-matrix.md) — Chrome's automatic `italic` resolution measurably drives `slnt`, isolated and confirmed, not guessed |
| `oblique 11deg` against an italic-only face falls back correctly, but doesn't match explicit `ital=1` | ❌ FAIL | ❌ FAIL | not run | [`results/browser-matrix.md`](../results/browser-matrix.md) — fails on both engines; root cause not fully isolated per-engine, recorded honestly as such |
| Three `matching/` precedence tests (stretch/weight/style search direction) | ✅ PASS | ✅ PASS | ❌ FAIL | wpt.fyi CI, see [`results/upstream-matrix.md`](../results/upstream-matrix.md) — a live, dated, cross-engine finding, not a coverage gap |

## `ital`-axis upstream coverage

Zero. No test anywhere in upstream WPT's `css/css-fonts` tree exercises the
`ital` variation axis in any form — confirmed by a full-tree grep, not
sampling (see `docs/coverage.json`'s `ital_axis_gap`). This repo's
`tests/oblique-style-matching/` exists specifically to fill that gap (among
others) — see its own README for the full boundary-value and font-shape
tables.

## Deferred

Retaining sync history over time (a changelog of past `results/upstream.json`
snapshots) was considered and deliberately deferred — it cuts against this
page's goal of staying short and glanceable. `results/upstream.json` is
still overwritten, not appended, on every sync; only the current snapshot's
`synced_at` timestamp is shown. Revisit if "how has this changed over time"
becomes a real question worth answering.
