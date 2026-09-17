# WPT coverage catalog: oblique / slnt / ital

Generated from `docs/coverage.json` by `scripts/render-coverage-docs.py` — do not hand-edit.

Audited 2026-09-18. Method: Local sparse WPT checkout (.wpt/css/css-fonts, vendored per scripts/setup-wpt.sh) was walked directly with `find`/`grep`, not GitHub search or wpt.fyi's browse UI, since search snippets are not exhaustive. Every *.html file under css/css-fonts/{, variations/, animations/, matching/, parsing/} was grepped for slnt/ital/oblique in filename and body (`'slnt'`/`'ital'` as font-variation-settings axis literals, plus oblique/italic in title/assert text) to build this list.

This catalogs every existing upstream WPT test that exercises oblique/slnt/ital matching, synthesis, or closely related parsing/animation, found by walking the vendored `css/css-fonts` tree directly (not by search-snippet sampling). Live pass/fail per engine, sourced from wpt.fyi, is in [`results/upstream-matrix.md`](../results/upstream-matrix.md) — kept separate because that data is refreshed on a schedule and this catalog is not.

| Path | Axis | Probes #209565? | Assertion |
|---|---|---|---|
| `css/css-fonts/variations/slnt-variable.html` | slnt | yes | CSS Test: Variable fonts with slant axis |
| `css/css-fonts/variations/slnt-backslant-variable.html` | slnt | yes | CSS Test: Variable fonts with slant axis |
| `css/css-fonts/variations/font-slant-1.html` | slnt | yes | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/font-slant-2a.html` | slnt | yes | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/font-slant-2b.html` | slnt | yes | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/font-slant-2c.html` | slnt | yes | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/font-slant-3.html` | slnt | yes | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/at-font-face-font-matching.html` | neither | no | Testing @font-face font matching logic introduced in CSS Fonts level 4 |
| `css/css-fonts/variations/font-style-parsing.html` | neither | no | Testing the new font-style values introduced in CSS Fonts level 4 |
| `css/css-fonts/variations/font-style-interpolation.html` | slnt | no | Testing the interpolation of new font-style values introduced in CSS Fonts level 4 |
| `css/css-fonts/animations/font-style-interpolation.html` | slnt | no | font-style interpolation |
| `css/css-fonts/font-face-style-auto-variable.html` | slnt | no | CSS Test: Support for font-style: auto in @font-face |
| `css/css-fonts/font-face-style-default-variable.html` | slnt | no | CSS Test: Support for font-style: auto in @font-face |
| `css/css-fonts/font-variation-settings-descriptor-01.html` | slnt | no | CSS Test: font-variation-settings descriptor |
| `css/css-fonts/parsing/font-variation-settings-valid.html` | slnt | no | CSS Fonts Module Level 4: parsing font-variation-settings with valid values |
| `css/css-fonts/synthetic-oblique-out-of-capabilities-range.html` | slnt | yes | Tests that font-style with angle outside of the 'slnt' range support by the font does not synthesize oblique faces. |
| `css/css-fonts/font-style-angle.html` | neither | no | Testing font-style angle's unit type consideration |
| `css/css-fonts/font-style-sign-function.html` | neither | no | CSS Fonts test: font-style with CSS sign() function |
| `css/css-fonts/test-synthetic-italic.html` | neither | no | CSS Test: Test for synthetic italic rendering |
| `css/css-fonts/test-synthetic-italic-2.html` | neither | no | CSS Test: Test for synthetic italics in vertical upright mode |
| `css/css-fonts/test-synthetic-italic-3.html` | neither | no | CSS Test: Test for synthetic italics in vertical upright mode |
| `css/css-fonts/font-synthesis-style.html` | neither | no | CSS Test: font-synthesis-style: none disables fake italic/oblique |
| `css/css-fonts/font-synthesis-style-oblique-only.html` | neither | no | CSS font-synthesis-style:oblique-only test |
| `css/css-fonts/font-synthesis-style-binary.html` | neither | no | CSS Test: font-synthesis-style: none disables fake italic/oblique |
| `css/css-fonts/italic-oblique-fallback.html` | neither | no | CSS Fonts testcase: oblique/italic fallback |
| `css/css-fonts/oblique-last-resort-weight-selection.html` | neither | no | CSS Fonts: weight selection among last-resort oblique faces |
| `css/css-fonts/oblique-request-italic-only-family-no-crash.html` | neither | no | CSS Fonts: oblique request with italic-only family does not crash |
| `css/css-fonts/matching/style-ranges-over-weight-direction.html` | neither | no | (no <meta name=assert> — see file) |
| `css/css-fonts/matching/range-descriptor-reversed.html` | neither | no | CSS Fonts Module Level 3: Property descriptor ranges |

## The `ital`-axis gap

**No existing WPT test under css/css-fonts/ exercises the OpenType 'ital' variation axis in any form.**

Verified 2026-09-18. Search method: find css/css-fonts -name '*.html' | xargs grep -l "'ital'" (and the double-quoted form) across the full sparse-checked-out tree (top level, variations/, animations/, matching/, parsing/), plus a filename-only grep for the 'ital' token, distinct from 'italic'/'oblique' substrings.

Result: The only matches anywhere in the tree are this repo's own tests under css/css-fonts/variable-oblique-interop/ital-axis/ (copied there by scripts/setup-wpt.sh, not upstream WPT content). Zero matches upstream.

This is the confirmed, current scope of this repo's own novel tests (`tests/ital-axis/`) — not duplicating upstream coverage, filling a real gap in it.
