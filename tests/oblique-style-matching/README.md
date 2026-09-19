# oblique-style-matching

This folder is the single, self-contained candidate for a WPT PR: every test
this project has written for CSS Fonts 4 `font-style` matching (oblique,
italic, `slnt`/`ital` axes), consolidated from their earlier scattered
locations (`tests/font-style-oblique/`, `tests/ital-axis/`, both now
removed). **No WPT PR has been opened yet** — see `docs/summary.md`.

## Design rationale

Every test here traces its claim to one exact clause of CSS Fonts 4's
normative text — quoted verbatim in each file's own comment, fetched
directly from `https://drafts.csswg.org/css-fonts-4/` (not paraphrased from
memory) — either §5.2 "Matching font styles" (the face-selection/fallback
algorithm), §7.2 "Feature and variation precedence" (the
`font-variation-settings`-vs-`font-style` precedence question), or
csswg-drafts#12836's resolution (the `ital`/`slnt` independence question).
Where a claim couldn't be grounded this way — see
`italic-oblique-equivalence.html`'s comment for one case where an originally
planned testharness.js computed-value check turned out not to be
observable at all — the file says so directly rather than testing something
weaker than what it claims to.

Fonts follow the same deterministic-shear principle already established by
`tests/ital-axis/` before this consolidation (see `resources/
build-ident-ital-font.py`'s original rationale): a single glyph, a plain
rectangle at each axis's default, sheared by a `gvar` delta into a
pixel-distinguishable parallelogram elsewhere in the axis's range. `slnt`
and `ital` deliberately shear *different edges* of the glyph (bottom vs.
top, at different magnitudes) — see `resources/build-fonts.py`'s docstring
— specifically so a bug that activated the wrong axis would produce a real
pixel mismatch against the reference, not an accidental pass.

## Moved-file mapping

| Original path | New path | Why |
|---|---|---|
| `tests/font-style-oblique/slnt-axis-activation.html` | `slnt-axis-activation.html` | Baseline sanity test, not part of the boundary/clamp naming scheme — kept as-is, moved only. |
| `tests/font-style-oblique/auto-range-default-angle.html` | `auto-derived-range-clamp.html` | Renamed to fit this folder's boundary/clamp naming convention — it *is* the auto-derived-range clamp test the target structure calls for, not a separate file. |
| `tests/ital-axis/independence.html` | `independence.html` | `ital`-axis-specific; kept alongside rather than folded into the boundary/clamp names, since its font has only one axis — see `ital-slnt-independence-dual-axis.html` for the stronger, two-axis version of this same claim. |
| `tests/ital-axis/italic-no-extra-synthesis.html` | `italic-no-extra-synthesis.html` | Same reasoning as `independence.html`. |

## Boundary-value table (CSS Fonts 4 §5.2)

Every angle branch in the oblique sub-algorithm's text, and which file
covers it. Branch text is quoted verbatim in each covering file's own
comment — this table is a locator, not a restatement.

| Branch (exact requested angle / value) | Covering file(s) |
|---|---|
| `font-style: oblique`, angle ≥ 11deg (exact boundary) | `boundary-11deg-ascending.html` |
| `font-style: oblique`, angle ≤ -11deg (exact boundary) | `boundary-11deg-descending.html` |
| `font-style: oblique`, angle in [0deg, 11deg) | `explicit-descriptor-range-clamp.html` (bare-angle default clamps within this branch) |
| `font-style: oblique`, angle in (-11deg, 0deg] | `auto-derived-range-clamp.html` (bare-angle default clamps within this branch, negative side per this project's sign convention), `auto-derived-range-clamp-cairo-symmetric.html` (same branch, re-verified on Cairo's exact -11..11 range — see docs/coverage.json's `auto-range-default-angle` gap) |
| `font-style: italic`, full 4-stage fallback chain (italic search → oblique ≥11deg search → italic ≤0 search → oblique ≤0deg search) | `multi-branch-fallback-chain.html` |
| `font-style: italic`, single-stage real `ital`-axis match | `independence.html`, `italic-no-extra-synthesis.html` |
| `font-style: normal`, 3-stage fallback (oblique ≥0 ascending → italic ≥0 ascending → oblique <0 descending) | `boundary-0deg-normal-fallback.html` |
| `font-style: oblique 11deg` against an italic-only family (the oblique≥11deg branch's own "italic values ≥1" fallback step) | `italic-oblique-equivalence.html` |
| §7.2 "Feature and variation precedence" — `font-variation-settings` property vs. `font-style`'s implied variation | `style-plus-explicit-variation-settings.html` |
| `slnt`/`ital` independence on a font with both axes present (csswg-drafts#12836) | `ital-slnt-independence-dual-axis.html` |
| §2.8.2 "font-synthesis-style" — does the UA ALSO synthesize a skew on top of an already-correctly-clamped axis, on a face that does not lack an oblique face | `explicit-range-bare-keyword-synthesis-stacking.html` |

**Not separately covered here** (documented as still open, not silently
dropped): the "angle in [0,11) vs (-11,0]" branches' own internal
ascending/descending *search order* among multiple discrete oblique
candidates (as opposed to the single-range clamp cases above) would need a
multi-face family per branch — `multi-branch-fallback-chain.html` and
`boundary-0deg-normal-fallback.html` cover the `italic`/`normal` branches'
multi-stage chains this way, but the `oblique <angle>` branches' own
internal distance search among multiple *oblique* candidates specifically
is not yet built. `normal-plus-bare-oblique-same-family` (per
`docs/coverage.json`'s `confirmed_gaps`) remains open and is **not**
addressed by any file in this folder — flagged here explicitly rather than
left ambiguous.

## Font shape table

| Font | slnt range | ital | Real-world correspondence |
|---|---|---|---|
| `resources/Cairo.var.subset.ttf` | -11..11 (default 0), plus `wght` 200..1000 | no | **Real Cairo** (SIL OFL 1.1, no Reserved Font Name), subset to the glyphs of `OBLIQUE` by `resources/build-cairo-subset.sh`, the same way WPT's own `Inter.var.subset.ttf` is a subset of real Inter: cmap shrunk, both axes and all layout/variation tables kept. The tests render the capital `I`, a plain 4-point stem. Replaced the earlier purpose-built `oblique-symmetric.ttf` (block glyph) once every result was confirmed unchanged. |
| `resources/oblique-onesided-neg.ttf` | -10..0 (default 0) | no | Inter's shape — purpose-built minimal version; the *real* Inter font (`resources/Inter.var.subset.ttf`, used by `auto-derived-range-clamp.html`) is kept separately specifically because that test's whole point is using a real production font, not a synthetic stand-in. |
| `resources/oblique-onesided-pos.ttf` | 0..10 (default 0) | no | No known real-world instance — the mirror-image (sign-symmetry) counterpart to `oblique-onesided-neg.ttf`, built to test the negative-CSS-angle/backslant branches, which no font in this project's corpus otherwise exercises. |
| `resources/oblique-nozero.ttf` | 5..20 (default 12) | no | No known real-world instance — an all-backslant font whose range never includes 0deg, used to force deep fallback-chain traversal (see boundary-value table). Default is deliberately not the clamp target (5), so a correct clamp is visually distinct from doing nothing — see `resources/build-fonts.py`. |
| `resources/oblique-dual-axis.ttf` | -11..11 (default 0) | 0..1 (default 0) | No known real-world instance — built specifically to close `combined-slnt-ital-font`, the first font in this project with both axes genuinely present. |

`resources/FontStyleTest-slnt-VF.woff2` (WPT's own corpus, authored by
Stephen Nixon) and `resources/IdentTestItal.ttf`/`.woff2` (this project's
earlier purpose-built `ital`-only font) are also still used, by
`slnt-axis-activation.html` and `independence.html`/
`italic-no-extra-synthesis.html`/`italic-oblique-equivalence.html`
respectively — not superseded by the 5 fonts above.

## The generated matrix: `matrix-{row}-{column}.html`

Columns (A, B, C...) are the `@font-face` `font-style` descriptor (omitted, `normal`, `italic`,
bare `oblique`, `oblique -11deg 11deg`); rows (1, 2, 3...) are the use-site request
(`normal`, `italic`, `oblique`, `oblique 11deg`, `<em>`, `font-variation-settings: 'slnt' -11`).
A cell is its column letter and row number (`E2`), and its file is `matrix-{row slug}-{column slug}`
(`matrix-italic-oblrange.html`). All use `resources/Cairo.var.subset.ttf` and the capital `I`.

**These files are generated; do not edit them.** `reference/` (an independent JavaScript
implementation of CSS Fonts 4 font-style matching, see `reference/README.md`) decides what each
cell should render, `node reference/src/cli.mjs generate` writes the tests, and
`matrix.manifest.json` records the expectation for every cell, including the ones with no test.

- **Specified** cells pin one outcome and have a single `match` reference.
- **Constrained** cells are where the spec allows several outcomes (or a synthesized skew):
  the test only forbids what the spec forbids (several `match` refs, or `mismatch` refs).
- **Unspecified** cells have no file: the spec is silent, so they are only observed
  (`scripts/survey.py`), never passed or failed.

References are plain faces with the axis pinned through `font-variation-settings`, so they
never depend on the descriptor under test. No test sets `font-synthesis`: the spec synthesizes
only when a face is missing, so a matched request must not be synthesized, and forcing it off
would hide an engine that does.

Result today (30 cells: 21 tests, 9 observed): Firefox passes all 21; Chrome and Safari fail
3, cells E2, E3 and E5, the explicit-range face requested with `italic`, bare `oblique` and
`<em>` (Chrome stacks a synthetic skew on the clamped axis; Safari does the same for bare
`oblique` and drops the axis for `italic`/`<em>`). Full writeup: `docs/investigation-log.md`
section 12. The older hand-written tests (`boundary-11deg-*`, `auto-derived-range-clamp*`,
`style-plus-explicit-variation-settings`, ...) stay as regression tests and still force
`font-synthesis: none` to isolate the question each was written for.

## Safari

`wpt run safari` is unreliable here and is not used for results: it disagrees
with the actual rendering on about 20 of 44 tests and flips on 5 between
identical runs (`docs/investigation-log.md` section 11). Safari results come
from `scripts/safari-replay.py`, a direct `safaridriver` replay with exact pixel
comparison, 3 agreeing repetitions per test. Safari 27.0 passes 34 and fails 10;
the 6 grid cells it fails are `italic` and `<em>` on the auto face, `italic`,
`oblique` and `<em>` on the explicit-range face, and `oblique 11deg` on the
normal face.
