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
| `css/css-fonts/variations/font-slant-2c.html` | slnt | no | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/font-slant-3.html` | slnt | no | CSS test: mapping of font-style:oblique to opentype 'slnt' axis |
| `css/css-fonts/variations/at-font-face-font-matching.html` | neither | no | Testing @font-face font matching logic introduced in CSS Fonts level 4 |
| `css/css-fonts/variations/font-style-parsing.html` | neither | no | Testing the new font-style values introduced in CSS Fonts level 4 |
| `css/css-fonts/variations/font-style-interpolation.html` | slnt | no | Testing the interpolation of new font-style values introduced in CSS Fonts level 4 |
| `css/css-fonts/animations/font-style-interpolation.html` | slnt | no | font-style interpolation |
| `css/css-fonts/font-face-style-auto-variable.html` | slnt | no | CSS Test: Support for font-style: auto in @font-face |
| `css/css-fonts/font-face-style-default-variable.html` | slnt | no | CSS Test: Support for font-style: auto in @font-face |
| `css/css-fonts/font-variation-settings-descriptor-01.html` | slnt | no | CSS Test: font-variation-settings descriptor |
| `css/css-fonts/parsing/font-variation-settings-valid.html` | slnt | no | CSS Fonts Module Level 4: parsing font-variation-settings with valid values |
| `css/css-fonts/synthetic-oblique-out-of-capabilities-range.html` | slnt | no | Tests that font-style with angle outside of the 'slnt' range support by the font does not synthesize oblique faces. |
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
| `css/css-fonts/variations/font-variation-settings-inherit.html` | neither | no | Testing the inheritance of the font-variation-settings property |
| `css/css-fonts/variations/font-descriptor-range-reversed.html` | neither | no | CSS Test: Matching @font-face font-weight, font-style, and font-stretch descriptors with reversed ranges |
| `css/css-fonts/variations/font-descriptor-range-reversed-002.html` | neither | no | CSS Test: Matching @font-face font-weight, font-style, and font-stretch descriptors with reversed ranges |
| `css/css-fonts/variations/font-parse-numeric-stretch-style-weight.html` | slnt | no | (no <title>/<meta assert> — see file) |
| `css/css-fonts/font-face-range-order.html` | neither | no | CSS Fonts Module Level 3: Order of values in @font-face range descriptors |
| `css/css-fonts/matching/fixed-stretch-style-over-weight.html` | neither | no | (no <title>/<meta assert> — see file) |
| `css/css-fonts/matching/stretch-distance-over-weight-distance.html` | neither | no | (no <title>/<meta assert> — see file) |
| `css/css-fonts/variations/font-shorthand.html` | slnt | no | Testing font shorthand for new values introduced in CSS Fonts level 4 |

## The `ital`-axis gap

**No existing WPT test under css/css-fonts/ exercises the OpenType 'ital' variation axis in any form.**

Verified 2026-09-18. Search method: find css/css-fonts -name '*.html' | xargs grep -l "'ital'" (and the double-quoted form) across the full sparse-checked-out tree (top level, variations/, animations/, matching/, parsing/), plus a filename-only grep for the 'ital' token, distinct from 'italic'/'oblique' substrings.

Result: The only matches anywhere in the tree are this repo's own tests under css/css-fonts/variable-oblique-interop/ital-axis/ (copied there by scripts/setup-wpt.sh, not upstream WPT content). Zero matches upstream.

This is the confirmed, current scope of this repo's own novel tests (`tests/ital-axis/`) — not duplicating upstream coverage, filling a real gap in it.

## Coverage checklist status

Cross-references every item in `docs/spec.md`'s 14-item "Coverage checklist" against actual coverage — upstream WPT tests, this repo's own tests, or neither. Broader than the `probes_209565` flag above: an item can be fully covered without any single test specifically probing #209565's documented failure modes.

Audited 2026-09-18.

| Checklist item | Status | Test(s) |
|---|---|---|
| font-style: oblique matching a variable slnt axis | ✅ covered (upstream WPT) | `css/css-fonts/variations/slnt-variable.html`<br>`css/css-fonts/variations/font-slant-1.html` |
| Explicit oblique <angle> matching | ✅ covered (upstream WPT) | `css/css-fonts/variations/font-slant-2a.html`<br>`css/css-fonts/variations/font-slant-2b.html`<br>`css/css-fonts/variations/font-slant-2c.html`<br>`css/css-fonts/variations/slnt-backslant-variable.html`<br>`css/css-fonts/variations/font-parse-numeric-stretch-style-weight.html` |
| font-style ranges declared in @font-face | ✅ covered (upstream WPT) | `css/css-fonts/variations/font-descriptor-range-reversed.html`<br>`css/css-fonts/variations/font-descriptor-range-reversed-002.html`<br>`css/css-fonts/font-face-range-order.html`<br>`css/css-fonts/matching/range-descriptor-reversed.html` |
| | | _All are combined weight/stretch/style range tests, not style-only, but style is exercised in each._ |
| Bare oblique / default-angle (14deg) matching | 🟡 partial (upstream WPT) | `css/css-fonts/variations/font-slant-1.html`<br>`css/css-fonts/variations/font-slant-2b.html` |
| | | _Covered, and passing on all three engines, ONLY for the case where @font-face declares an EXPLICIT font-style descriptor range that excludes the default angle. The realistic deployment shape — no explicit descriptor at all (font-style:auto, the actual default), so the UA must derive the oblique range from the font's own fvar/STAT extremes, with a bare italic/oblique request whose default angle falls outside THAT auto-derived range — has zero upstream coverage. This is the precise shape of Cairo's real-world bug (per vizchitra-fonts/docs/compat.md): Cairo doesn't hand-author a font-style descriptor, so its usable range comes entirely from its own slnt axis (-11 to 11), and the UA default (14deg) falls outside it. See the standalone 'auto-range default-angle resolution' gap item below — reinstates Cairo as motivating evidence for a real, narrow, currently-unverified gap, not the general slnt story._ |
| italic vs oblique resolution differences | ✅ covered (upstream WPT) | `css/css-fonts/italic-oblique-fallback.html`<br>`css/css-fonts/oblique-request-italic-only-family-no-crash.html` |
| | | _Covered for static (non-variable) faces only; the variable-axis version of this question is items below (ital-axis specific), which are NOT covered upstream._ |
| italic on a font with only an ital axis (no slnt) — sets ital=1 | 🟡 covered (this repo only) | `tests/ital-axis/italic-no-extra-synthesis.html` |
| | | _Zero upstream WPT coverage — part of the confirmed ital_axis_gap._ |
| oblique on a font with only an ital axis — must NOT touch ital (per #12836) | 🟡 covered (this repo only) | `tests/ital-axis/independence.html` |
| | | _Zero upstream WPT coverage — part of the confirmed ital_axis_gap._ |
| Font exposing both slnt and ital — confirms independence per #12836 | ❌ gap | — |
| | | _No font anywhere in WPT's corpus or this repo's own resources exposes both a real slnt axis and a real ital axis together (confirmed by filename/content search of both .wpt/css/css-fonts font resources and tests/*/resources) — this is a genuine, currently-open gap, and the strongest direct test of #12836's independence claim would require building one. Candidate next worked example._ |
| Single variable face covering normal + oblique | ✅ covered (upstream WPT) | `css/css-fonts/font-face-style-auto-variable.html`<br>`css/css-fonts/font-face-style-default-variable.html` |
| Separate normal/oblique faces (ambiguous-match hazard) | ✅ covered (upstream WPT) | `css/css-fonts/matching/style-ranges-over-weight-direction.html`<br>`css/css-fonts/matching/fixed-stretch-style-over-weight.html`<br>`css/css-fonts/matching/stretch-distance-over-weight-distance.html` |
| Font synthesis fallback behavior (font-synthesis) | ✅ covered (upstream WPT) | `css/css-fonts/font-synthesis-style.html`<br>`css/css-fonts/font-synthesis-style-oblique-only.html`<br>`css/css-fonts/font-synthesis-style-binary.html`<br>`css/css-fonts/test-synthetic-italic.html`<br>`css/css-fonts/oblique-last-resort-weight-selection.html` |
| | | _Covers font-synthesis fallback generally; the specific ital-axis spurious-synthesis failure mode (#209565) is only covered by this repo's tests/ital-axis/italic-no-extra-synthesis.html — see the probes_209565 flag on individual tests above._ |
| Explicit font-variation-settings: 'slnt' <val> / 'ital' <val> | 🟡 partial (upstream WPT) | `css/css-fonts/font-variation-settings-descriptor-01.html` |
| | | _'slnt' explicit-value case is covered upstream. No upstream (or, currently, this-repo) test sets 'ital' explicitly via font-variation-settings — part of the ital_axis_gap._ |
| font-style + explicit axis value paired (recommended pattern) | ❌ gap | — |
| | | _No test found, upstream or in this repo, that pairs font-style with an explicit font-variation-settings axis override on the same declaration and checks the resulting precedence/consistency. Candidate next worked example._ |
| Ancestor font-variation-settings inheritance/replacement behavior | ✅ covered (upstream WPT) | `css/css-fonts/variations/font-variation-settings-inherit.html` |

## Confirmed gaps (precise, verified by reading test content)

Narrower than a raw checklist-item miss — each of these states exactly which combination of factors is untested, confirmed by reading the actual content of the closest candidate tests, not by title or filename alone. Ordered by priority: not all gaps carry equal weight as motivating evidence — a gap traced to a live, documented production bug is stronger evidence than spec-completeness with no known real-world instance.

Audited 2026-09-18.

### 1. auto-range-default-angle

**Evidence tier:** proven gap, root cause traced to a real font's real bug

No test combines an auto-derived (no explicit @font-face font-style descriptor) oblique range with a bare font-style:oblique or font-style:italic request (UA default angle, no explicit value) on a font whose actual fvar/STAT range excludes that default angle.

**Why it matters:** This is the precise shape of Cairo's real-world bug (vizchitra-fonts/docs/compat.md): Cairo ships with no font-style descriptor, so the browser must derive its usable oblique range from Cairo's own slnt axis (-11 to 11), and the UA default angle (14deg) falls outside it. The closest upstream test, css/css-fonts/variations/font-slant-1.html, tests exactly this default-angle-outside-range scenario INCLUDING the bare italic keyword — but only for a font-style descriptor that was EXPLICITLY authored in the @font-face rule, and it PASSES on Chrome/Firefox/Safari today. The auto-derived-range version of the same question — the version that actually matches how most variable webfonts (including Cairo) ship — is untested anywhere. Verified by reading css/css-fonts/font-face-style-auto-variable.html and font-face-style-default-variable.html directly: both use only explicit oblique <angle> values (10deg/5deg/0deg), never a bare keyword. Highest-priority next worked example: unlike the other two gaps, this one traces directly to a live, documented production bug rather than spec-completeness.

**Candidate test:** A reftest pairing a variable font with a real slnt axis whose range excludes 14deg (e.g. -11 to 11, matching Cairo, or the simpler -10 to 0 already present in WPT's Inter-VF.subset.ttf and Inter.var.subset.ttf — both verified via fontTools to have fvar slnt min=-10 max=0, confirmed 2026-09-18), NO explicit font-style descriptor in @font-face, and font-style: italic / font-style: oblique (bare) as the test declarations — checked against whatever angle the UA actually resolves the default to.

### 2. font-style-plus-explicit-axis-pairing

**Evidence tier:** confirmed gap, plausible real impact (untested spec-recommended author pattern)

No test pairs font-style with an explicit font-variation-settings axis override on the same declaration and checks the resulting precedence.

**Why it matters:** The spec's recommended pattern for authors is to pair the two (e.g. font-style: italic; font-variation-settings: 'ital' 1;) for compatibility with non-variable fallback faces, but no test verifies engines resolve any conflict between them consistently. Anyone following the spec's own compatibility advice is currently on unverified ground.

**Candidate test:** A reftest declaring font-style: oblique 10deg together with an explicit font-variation-settings: 'slnt' <different value> on the same rule, checking which wins (or whether they're required to agree).

### 3. combined-slnt-ital-font

**Evidence tier:** confirmed absent, spec-completeness, no known real-world instance

No font anywhere (WPT's corpus or this repo's own resources) exposes both a real slnt axis and a real ital axis together.

**Why it matters:** The strongest direct test of #12836's independence claim (italic sets ital=1 and leaves slnt untouched; oblique sets slnt and leaves ital untouched) requires a single font where both axes are real and distinguishable, so a test can prove the OTHER axis stayed at its default rather than merely asserting an axis was never referenced. Deprioritized relative to the other two gaps: no shipping font is known to combine both axes, so this is spec-completeness rather than evidence of real-world impact.

**Candidate test:** Extend tests/ital-axis/resources/build-font.py's approach (fontTools FontBuilder) to add a second gvar-driven axis, or find/build a WPT-compatible font exposing both.
