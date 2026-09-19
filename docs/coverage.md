# WPT coverage catalog: oblique / slnt / ital

Generated from `docs/coverage.json` by `scripts/render-coverage-docs.py` — do not hand-edit.

Audited 2026-09-18. Method: Local sparse WPT checkout (.wpt/css/css-fonts, vendored per scripts/setup-wpt.sh) was walked directly with `find`/`grep`, not GitHub search or wpt.fyi's browse UI, since search snippets are not exhaustive. Every *.html file under css/css-fonts/{, variations/, animations/, matching/, parsing/} was grepped for slnt/ital/oblique in filename and body (`'slnt'`/`'ital'` as font-variation-settings axis literals, plus oblique/italic in title/assert text) to build this list.

## Evidence tiers

Not every finding in this catalog carries equal weight as motivating evidence. `priority_tier` on individual items below refers back to these three tiers:

**Tier 1:** Proven, reproducible, live today — a written test with a dated, recorded cross-engine result showing the failure actually happening.
**Tier 2:** Proven gap, root cause traced to a real font's real bug, test not yet written — the failure mode is confirmed to exist (via a real shipping font or the spec's own text) but no test demonstrates it yet.
**Tier 3:** Confirmed absent upstream, no known real-world font or pattern triggers it — spec-completeness, not evidence of real breakage; included for thoroughness, not prioritized.

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

This is the confirmed, current scope of this repo's own novel tests (`tests/oblique-style-matching/`) — not duplicating upstream coverage, filling a real gap in it.

## Coverage checklist status

Cross-references every item in `docs/spec.md`'s 14-item "Coverage checklist" against actual coverage — upstream WPT tests, this repo's own tests, or neither. Broader than the `probes_209565` flag above: an item can be fully covered without any single test specifically probing #209565's documented failure modes.

Audited 2026-09-18.

| Checklist item | Status | Test(s) |
|---|---|---|
| font-style: oblique matching a variable slnt axis | ✅ covered (upstream WPT) | `css/css-fonts/variations/slnt-variable.html`<br>`css/css-fonts/variations/font-slant-1.html` |
| Explicit oblique <angle> matching | ✅ covered (upstream WPT) | `css/css-fonts/variations/font-slant-2a.html`<br>`css/css-fonts/variations/font-slant-2b.html`<br>`css/css-fonts/variations/font-slant-2c.html`<br>`css/css-fonts/variations/slnt-backslant-variable.html`<br>`css/css-fonts/variations/font-parse-numeric-stretch-style-weight.html` |
| font-style ranges declared in @font-face | ✅ covered (upstream WPT) | `css/css-fonts/variations/font-descriptor-range-reversed.html`<br>`css/css-fonts/variations/font-descriptor-range-reversed-002.html`<br>`css/css-fonts/font-face-range-order.html`<br>`css/css-fonts/matching/range-descriptor-reversed.html` |
| | | _All are combined weight/stretch/style range tests, not style-only, but style is exercised in each._ |
| Bare oblique / default-angle (14deg) matching | ✅ covered (upstream WPT) (tier 1) | `css/css-fonts/variations/font-slant-1.html`<br>`css/css-fonts/variations/font-slant-2b.html`<br>`tests/oblique-style-matching/auto-derived-range-clamp.html`<br>`tests/oblique-style-matching/explicit-descriptor-range-clamp.html` |
| | | _Covered for both sub-cases now. Upstream (font-slant-1.html, font-slant-2b.html) covers an EXPLICITLY authored @font-face font-style descriptor range that excludes the default angle — PASS on Chrome/Firefox/Safari per results/upstream.json. This repo's own tests/oblique-style-matching/auto-derived-range-clamp.html (added 2026-09-18 as tests/font-style-oblique/auto-range-default-angle.html, renamed 2026-09-18 during the tests/oblique-style-matching/ consolidation — closing docs/coverage.json's confirmed_gaps 'auto-range-default-angle') covers the previously-missing AUTO-DERIVED-range case (no explicit descriptor, font-style:auto — the realistic deployment shape, matching how Cairo and most variable webfonts actually ship) — PASS on Chrome 153.0.8010.48 and Firefox 156.0, run 2026-09-18 (Safari not attempted, see confirmed_gaps entry for why). A second variant, tests/oblique-style-matching/auto-derived-range-clamp-cairo-symmetric.html (added 2026-09-19), re-runs the identical question on a font whose range is Cairo's exact symmetric -11..11 (not Inter's one-sided -10..0) — also PASS on Chrome/Firefox. Range shape alone therefore does not explain Cairo's original real-device finding; some other Cairo-specific factor would have to account for it if it still reproduces. tests/oblique-style-matching/explicit-descriptor-range-clamp.html (new 2026-09-18) is the explicit-descriptor contrast case, written for this suite's own side-by-side boundary-value table rather than to duplicate upstream — also PASS on Chrome/Firefox._ |
| italic vs oblique resolution differences | ✅ covered (upstream WPT) | `css/css-fonts/italic-oblique-fallback.html`<br>`css/css-fonts/oblique-request-italic-only-family-no-crash.html` |
| | | _Covered for static (non-variable) faces only; the variable-axis version of this question is items below (ital-axis specific), which are NOT covered upstream._ |
| italic on a font with only an ital axis (no slnt) — sets ital=1 | 🟡 covered (this repo only) (tier 1) | `tests/oblique-style-matching/italic-no-extra-synthesis.html` |
| | | _Zero upstream WPT coverage — part of the confirmed ital_axis_gap. Tier 1 (see evidence_tiers): a dated, live cross-engine result exists — Chrome 153 FAILs, Firefox 156 PASSes, recorded in results/browser-matrix.md — not just a theoretical gap._ |
| oblique on a font with only an ital axis — must NOT touch ital (per #12836) | 🟡 covered (this repo only) (tier 1) | `tests/oblique-style-matching/independence.html` |
| | | _Zero upstream WPT coverage — part of the confirmed ital_axis_gap. Tier 1: dated, recorded result (PASS on Chrome and Firefox), though per docs/investigation-log.md its font-synthesis:none setup makes the PASS less discriminating than italic-no-extra-synthesis.html's._ |
| Font exposing both slnt and ital — confirms independence per #12836 | 🟡 covered (this repo only) (tier 1) | `tests/oblique-style-matching/ital-slnt-independence-dual-axis.html` |
| | | _Closed 2026-09-18: resources/oblique-dual-axis.ttf (built via resources/build-fonts.py) is this project's first font with both a real slnt axis and a real ital axis. The test found a genuine, dated finding, not a clean pass: FAILS on Chrome 153.0.8010.48, PASSES on Firefox 156.0 (see results/browser-matrix.md and confirmed_gaps' combined-slnt-ital-font entry) — Chrome's automatic 'font-style: italic' resolution drives the slnt axis on this font instead of purely the ital axis, confirmed by isolating with explicit font-variation-settings overrides before concluding it wasn't a test-construction mistake._ |
| Single variable face covering normal + oblique | ✅ covered (upstream WPT) | `css/css-fonts/font-face-style-auto-variable.html`<br>`css/css-fonts/font-face-style-default-variable.html` |
| Separate normal/oblique faces (ambiguous-match hazard) | ❌ gap (tier 2) | — |
| | | _Previously marked covered-upstream citing the three matching/ tests below — wrong, corrected after reading all three in full (not inferring from title/filename): css/css-fonts/matching/style-ranges-over-weight-direction.html, css/css-fonts/matching/fixed-stretch-style-over-weight.html, and css/css-fonts/matching/stretch-distance-over-weight-distance.html every @font-face block in all three uses font-style: oblique <angle-or-range> — not one declares font-style: normal. They test precedence AMONG MULTIPLE OBLIQUE candidates (stretch/weight/style search direction and distance), never a same-family normal-vs-bare-oblique scenario. A fourth candidate, css/css-fonts/variations/at-font-face-font-matching.html, was also read in full as a near-miss check: its descriptorPriorityTest family uses font-style: italic (not oblique) and has no normal face either — also does not cover this. See confirmed_gaps' normal-plus-bare-oblique-same-family entry. Still open as of the 2026-09-18 tests/oblique-style-matching/ consolidation — that folder's own README.md explicitly flags this as NOT addressed by any file in it, rather than leaving the omission ambiguous._ |
| Font synthesis fallback behavior (font-synthesis) | ✅ covered (upstream WPT) | `css/css-fonts/font-synthesis-style.html`<br>`css/css-fonts/font-synthesis-style-oblique-only.html`<br>`css/css-fonts/font-synthesis-style-binary.html`<br>`css/css-fonts/test-synthetic-italic.html`<br>`css/css-fonts/oblique-last-resort-weight-selection.html` |
| | | _Covers font-synthesis fallback generally; the specific ital-axis spurious-synthesis failure mode (#209565) is only covered by this repo's tests/oblique-style-matching/italic-no-extra-synthesis.html — see the probes_209565 flag on individual tests above._ |
| Explicit font-variation-settings: 'slnt' <val> / 'ital' <val> | 🟡 partial (upstream WPT) | `css/css-fonts/font-variation-settings-descriptor-01.html` |
| | | _'slnt' explicit-value case is covered upstream. No upstream (or, currently, this-repo) test sets 'ital' explicitly via font-variation-settings — part of the ital_axis_gap._ |
| font-style + explicit axis value paired (recommended pattern) | 🟡 covered (this repo only) (tier 1) | `tests/oblique-style-matching/style-plus-explicit-variation-settings.html` |
| | | _Closed 2026-09-18: grounded in CSS Fonts 4 §7.2 'Feature and variation precedence', which lists font-variation-settings (the property) after font-style's implied variation in its explicit ascending-precedence ordering — so an explicit conflicting value must win. PASS on Chrome 153.0.8010.48 and Firefox 156.0, confirming both engines implement that ordering correctly for this case; see confirmed_gaps' font-style-plus-explicit-axis-pairing entry._ |
| Ancestor font-variation-settings inheritance/replacement behavior | ✅ covered (upstream WPT) | `css/css-fonts/variations/font-variation-settings-inherit.html` |

## Confirmed gaps (precise, verified by reading test content)

Narrower than a raw checklist-item miss — each of these states exactly which combination of factors is untested, confirmed by reading the actual content of the closest candidate tests, not by title or filename alone. Ordered by priority: not all gaps carry equal weight as motivating evidence — a gap traced to a live, documented production bug is stronger evidence than spec-completeness with no known real-world instance.

Audited 2026-09-18.

### 1. explicit-range-bare-keyword-synthesis-stacking

**Status:** test written and run — tests/oblique-style-matching/explicit-range-bare-keyword-synthesis-stacking.html + -ref.html, added 2026-09-19

**Priority tier:** 1

**Evidence tier:** written test, dated cross-engine result — a genuine reproduction, not a clean pass. FAIL on Chrome, PASS on Firefox, matching an independently-measured real production finding exactly

Distinct from auto-range-default-angle (which tests whether the slnt axis is clamped to the CORRECT value) — this tests whether the UA ALSO synthesizes an additional skew on top of an already-correctly-clamped axis, when the family does not lack an oblique face. Every earlier range-clamp test in this folder (auto-derived-range-clamp.html, auto-derived-range-clamp-cairo-symmetric.html, explicit-descriptor-range-clamp.html) sets font-synthesis:none specifically to isolate the clamp question from synthesis — which is exactly what made this bug invisible to them. This test is the first in the folder to leave font-synthesis at its default (auto), and it reproduces a real, independently-measured production bug: Chrome FAILs, Firefox PASSes.

**Why it matters:** CSS Fonts 4 section 2.8.2 (font-synthesis-style) says synthesis of oblique faces applies 'when a font family lacks oblique faces' (fetched from the raw spec HTML, 2026-09-19). The family under test does not lack one — it has a real slnt-axis face, correctly matched and clamped. Chromium's additional synthetic skew on top of that correctly-matched axis does not fit the spec's own stated condition for when synthesis should apply, and is a real, currently-shipping interop gap: vizchitra-fonts had to add an explicit use-site font-variation-settings value specifically to work around it (see compat.md's RECOMMENDED technique), rather than being able to rely on font-style matching alone.

**Corroborating evidence (independently measured, in a separate real production codebase (vizchitra-fonts), not just cited as a historical bug report):** vizchitra-fonts' Cairo face currently ships font-style: oblique -11deg 11deg (an explicit range matching its true fvar slnt bounds exactly — a deployment change from the bare/no-descriptor shape auto-range-default-angle targets). Requesting bare font-style: oblique against it (implied 14deg default, outside the range) measures shear ~0.44 in Chromium instead of the correct ~0.194 — roughly double, because Chromium correctly clamps slnt to -11 AND separately stacks a ~14deg synthetic skew on top. WebKit fails the same case a different way (discards the axis, synthesizes instead). Firefox measures correct. This repo's own test, built independently using a different (synthetic, not real Cairo) font, reproduces the identical pass/fail pattern: FAIL on Chrome, PASS on Firefox. (source: vizchitra-fonts/docs/compat.md ("Decision — UPDATED" section) and vizchitra-fonts/src/lib/fonts/slant.browser.test.ts ("the BARE oblique keyword against a ranged face is mishandled, even at the font's own true bounds"))

**Candidate test:** Done — see tests/oblique-style-matching/explicit-range-bare-keyword-synthesis-stacking.html. Not yet covered: the italic variant against the same face, which vizchitra-fonts measured as a THIRD distinct failure mode on WebKit (pure synthetic skew, no axis contribution at all — this test's own file requests bare italic too, but only Chrome/Firefox results are recorded here; Safari/WebKit's distinct failure mode is not independently confirmed by this repo). Also not covered: vizchitra-fonts' separate finding that Chromium/WebKit pick the WRONG FACE entirely (falls back to an upright normal sibling) for font-style: oblique 11deg against a family with both a normal and a bare-oblique face — this is a live, independently-measured real-world instance of the still-open normal-plus-bare-oblique-same-family gap below, not yet built as a test in this repo.

### 1. normal-plus-bare-oblique-same-family

**Priority tier:** 2

**Evidence tier:** proven gap, root cause traced to a real, MEASURED production hazard (not just an inferred workaround), test not yet written in this repo

No test constructs a same-family pairing of a font-style:normal face and a bare/unranged font-style:oblique face and checks that an angled request correctly selects the oblique face rather than falling back to normal.

**Why it matters:** Re-verified by reading (not title-inferring) all three matching/ tests previously credited with covering this checklist item (css/css-fonts/matching/style-ranges-over-weight-direction.html, fixed-stretch-style-over-weight.html, stretch-distance-over-weight-distance.html): every @font-face block in all three declares font-style: oblique <angle-or-range> — none declares font-style: normal. They test precedence AMONG MULTIPLE OBLIQUE CANDIDATES (stretch/weight/style search direction and distance), never a normal-vs-oblique same-family scenario. A fourth candidate, css/css-fonts/variations/at-font-face-font-matching.html, was also read in full as a near-miss: its descriptorPriorityTest family uses font-style: italic (not oblique) and has no normal face either. This checklist item (docs/spec.md's 'Separate normal/oblique faces (ambiguous-match hazard)') was previously marked covered-upstream citing those three tests — that was wrong and has been corrected (see checklist_mapping). The hazard itself is real and documented: it's the specific reason vizchitra-fonts' own production CSS avoids a single combined face.

**Corroborating evidence (first-party production practice AND a direct, measured browser test in that same codebase — updated 2026-09-19 from a weaker inferred-workaround citation):** vizchitra-fonts ships Cairo as TWO separate @font-face blocks under the same font-family name — one font-style:normal, one ranged font-style:oblique — rather than one combined face, specifically to avoid this hazard. Read past the inferred workaround: slant.browser.test.ts measures the hazard directly, not just documents the avoidance. Its CairoBoth family carries both a normal AND a bare-oblique face under one family (the OLD structure, before migrating to a declared range) and requests font-style: oblique 11deg — Chromium and WebKit pick the WRONG (normal) face and render upright (shear +0/-0, not even a partial lean); only Firefox resolves it correctly. This is a live, dated, cross-engine measurement of the exact scenario this gap describes, not an inference from the workaround's existence. (source: vizchitra-fonts' own fonts.css, plus vizchitra-fonts/src/lib/fonts/slant.browser.test.ts's directly measured test 'font-style: oblique 11deg against a family with BOTH normal and BARE oblique (historical)')

**Candidate test:** A reftest with one font-family containing two @font-face blocks sharing the same font-family name — one font-style: normal, one font-style: oblique (bare, unranged) — requesting an angled style (font-style: oblique or an explicit angle) and checking whether the correct (angled) face is chosen over the upright normal face.

### 2. italic-descriptor-exact-match-still-shears

**Status:** test written and run — tests/oblique-style-matching/matrix-italic-r5-italic.html + -ref.html, part of a 25-test batch systematically enumerating 5 @font-face font-style descriptor values x 7 use-site CSS patterns against resources/oblique-symmetric.ttf, added 2026-09-19

**Priority tier:** 1

**Evidence tier:** written test, dated cross-engine result — a genuine, isolated FAIL on Chrome, PASS on Firefox

A face declared font-style: italic (bare, binary descriptor — no numeric angle), on a font whose ONLY working axis is slnt (no ital axis), requested via <em> (implicit italic) with font-synthesis:none: Chrome renders sheared (activates the real slnt axis), Firefox renders genuinely upright. Verified against a reference forced to genuinely-upright via explicit font-variation-settings: 'slnt' 0 — NOT via implicit/default styling, which was independently confirmed unreliable here (this same face renders sheared even for a plain font-style: normal request, per matrix-italic-r7-italic.html, part of the same 25-test batch).

**Why it matters:** CSS Fonts 4's italic-matching branch (section 5.2) explicitly licenses axis-setting only 'for variable fonts with an ital axis' at its first stage — this face has no ital axis, only slnt, and the descriptor gives no explicit angle for slnt to map to. Chrome activating the axis anyway is not obviously licensed by that text. This is a narrow, specific gap in how 'binary' style descriptors (italic, with no numeric range) interact with fonts that only expose a numeric (slnt) axis, distinct from every other test in this suite which either declares an explicit range or omits the descriptor entirely.

**Corroborating evidence (same underlying phenomenon already documented for a different font shape in this repo's own suite):** italic-no-extra-synthesis.html established that Chrome over-applies styling for a font-style:italic request against an italic-declared face on an ital-axis font. This new test reproduces the identical polarity on a completely different font shape (slnt-axis only, no ital axis) — Chrome activates the real slnt axis for a face declared font-style:italic even for a request whose exact style already matches the descriptor, while Firefox renders genuinely upright. (source: tests/oblique-style-matching/italic-no-extra-synthesis.html (this repo, 2026-09-18) — same Chrome-FAIL/Firefox-PASS polarity, but on an ital-axis-only font, not a slnt-only one)

**Candidate test:** Done — see tests/oblique-style-matching/matrix-italic-r5-italic.html. The full 25-test batch (tests/oblique-style-matching/matrix-*.html, generated by resources/gen25.py) also confirms this is the ONLY divergent cell among all 25 systematically-enumerated (descriptor x use-site) combinations tested — every other cell agrees between Chrome and Firefox.

### 2. font-style-plus-explicit-axis-pairing

**Status:** test written and run — tests/oblique-style-matching/style-plus-explicit-variation-settings.html + -ref.html

**Priority tier:** 1

**Evidence tier:** written test, dated cross-engine result — PASS on both engines, confirming both correctly implement §7.2's precedence ordering

Closed: tests/oblique-style-matching/style-plus-explicit-variation-settings.html pairs font-style: oblique 5deg with a conflicting explicit font-variation-settings: 'slnt' -11 on the same rule and confirms the explicit value wins, per CSS Fonts 4 §7.2 'Feature and variation precedence' (font-variation-settings the property is listed after font-style's implied variation in that section's explicit ascending-precedence order).

**Why it matters:** The spec's recommended pattern for authors is to pair the two (e.g. font-style: italic; font-variation-settings: 'ital' 1;) for compatibility with non-variable fallback faces. This closes the general upstream-coverage gap and confirms both Chrome and Firefox resolve the conflict per §7.2's ordering — but, unlike auto-range-default-angle and normal-plus-bare-oblique-same-family, it still has no specific corroborating broken font or production practice behind it (lacks_corroborating_font: true) — a spec-completeness closure, not evidence a real author-facing bug was reproduced.

**No corroborating broken font** — unlike auto-range-default-angle, this gap is not tied to a specific known-broken font; it's a spec-recommended pattern that's simply untested.

**Candidate test:** Done — see tests/oblique-style-matching/style-plus-explicit-variation-settings.html.

### 3. combined-slnt-ital-font

**Status:** test written and run — tests/oblique-style-matching/ital-slnt-independence-dual-axis.html + -ref.html

**Priority tier:** 1

**Evidence tier:** written test, dated cross-engine result — and the result is a genuine, isolated FAIL on Chrome, not a clean pass

Closed as far as upstream WPT coverage goes, and the closure surfaced a real finding: tests/oblique-style-matching/ital-slnt-independence-dual-axis.html tests that 'italic' and 'oblique 11deg' each activate only their own axis on a font with both slnt and ital real. Firefox PASSes; Chrome FAILS — its automatic 'italic' resolution measurably drives the slnt axis on this font, not purely the ital axis.

**Why it matters:** The strongest direct test of #12836's independence claim (italic sets ital=1 and leaves slnt untouched; oblique sets slnt and leaves ital untouched) required a single font where both axes are real and distinguishable, so a test can prove the OTHER axis stayed at its default rather than merely asserting an axis was never referenced. Before trusting this as a real finding rather than a test-construction mistake: isolated it directly by forcing 'font-variation-settings: slnt 0' on top of Chrome's automatic italic resolution (using the already-confirmed font-variation-settings-overrides-font-style precedence) — the rendering collapsed to a plain unsheared rectangle, and forcing 'ital 1' instead restored full shear matching the explicit reference. No known real-world font combines both axes (this remains a purpose-built font, not a corroborated shipping-font case), but the Chrome finding itself is now real and dated, not spec-completeness — upgraded from tier 3 to tier 1.

**Corroborating fonts:**

- **resources/oblique-dual-axis.ttf (purpose-built)** — slnt range slnt -11..11, ital 0..1 (this project's first font exposing both axes for real, built specifically to close this gap — no known real-world font combines both, so this remains a purpose-built rather than corroborated-by-shipping-font case; source: tests/oblique-style-matching/resources/build-fonts.py)

**Candidate test:** Done — see tests/oblique-style-matching/ital-slnt-independence-dual-axis.html.

### 4. auto-range-default-angle

**Status:** test written and run — tests/oblique-style-matching/auto-derived-range-clamp.html + -ref.html (moved/renamed from tests/font-style-oblique/auto-range-default-angle.html during the 2026-09-18 consolidation), plus a second variant tests/oblique-style-matching/auto-derived-range-clamp-cairo-symmetric.html + -ref.html added 2026-09-19 using resources/oblique-symmetric.ttf (fvar slnt -11..11, matching Cairo's own range exactly)

**Priority tier:** 1

**Evidence tier:** written tests, dated cross-engine results on TWO range shapes (Inter's one-sided -10..0, and Cairo's exact symmetric -11..11) — both PASS on both engines, still not a reproduction of Cairo's bug

This gap is now closed as far as upstream WPT coverage goes, on two independent range shapes: tests/oblique-style-matching/auto-derived-range-clamp.html (Inter, one-sided -10..0) and tests/oblique-style-matching/auto-derived-range-clamp-cairo-symmetric.html (this repo's own font, symmetric -11..11 — Cairo's exact range). Both test a bare font-style:oblique/italic request against a font with NO explicit @font-face font-style descriptor. Chrome and Firefox correctly clamp to the font's own range boundary on BOTH shapes — PASS on both engines, both fonts, run 2026-09-18 and 2026-09-19 respectively.

**Why it matters:** This was the precise shape of Cairo's real-world bug (vizchitra-fonts/docs/compat.md): Cairo ships with no font-style descriptor, so the browser must derive its usable oblique range from Cairo's own slnt axis (-11 to 11), and the UA default angle (14deg) falls outside it. The first test built here (2026-09-18) used Inter's -10 to 0 range — one-sided, not Cairo's exact shape — and PASSed on Chrome/Firefox, with an explicit caveat that a one-sided-range PASS doesn't independently confirm or refute Cairo's own symmetric-range bug. The follow-up flagged in that caveat is now done: auto-derived-range-clamp-cairo-symmetric.html uses a purpose-built font (oblique-symmetric.ttf) whose fvar slnt range is exactly -11..11, matching Cairo's documented range. It also PASSes on both Chrome and Firefox (2026-09-19). Read this as: the auto-range-clamping mechanism now has two independent, PASSing, dated cross-engine results — one on a one-sided range, one on Cairo's exact symmetric range — so range shape alone does not explain Cairo's original real-device finding. Some other Cairo-specific factor (its STAT table, a different browser version, a platform-specific code path not exercised here) would have to account for the original bug if it still reproduces; this repo's synthetic fonts cannot rule that out. Was priority 1 / tier 2 before any test existed; now tier 1 on two independent shapes.

**Corroborating fonts:**

- **Cairo** — slnt range -11 to 11 (motivating case — the real-world bug this repo exists to document; source: vizchitra-fonts/docs/compat.md)
- **Inter-VF.subset.ttf / Inter.var.subset.ttf (WPT's own corpus)** — slnt range -10 to 0 (used as the test font for tests/oblique-style-matching/auto-derived-range-clamp.html — same auto-derived-range-excludes-default-angle shape as Cairo, but a one-sided (-10 to 0) rather than symmetric (-11 to 11) range; source: verified via fontTools fvar read, 2026-09-18)
- **Cairo.var.subset.ttf (real Cairo subset to the glyphs of OBLIQUE; replaced this repo's earlier purpose-built oblique-symmetric.ttf on 2026-09-19)** — slnt range -11 to 11 (used as the test font for tests/oblique-style-matching/auto-derived-range-clamp-cairo-symmetric.html — IS Cairo's own axis and metadata, so matches Cairo's own symmetric range exactly, not just the excludes-default-angle shape; source: verified via fontTools fvar read, 2026-09-19)

**Candidate test:** Done — see tests/oblique-style-matching/auto-derived-range-clamp.html and tests/oblique-style-matching/auto-derived-range-clamp-cairo-symmetric.html (the latter added 2026-09-19, using resources/oblique-symmetric.ttf's exact -11..11 range). Note for anyone extending this further: the first draft of the Cairo-symmetric test reused the word "slant" as its test glyph, copied from the Inter-based test — but oblique-symmetric.ttf's cmap only maps the letter 'A' (see resources/build-fonts.py:86), so that first draft silently fell back to a system font and both engines FAILed against a reference with the same silent fallback. Caught via pixel-diff forensics before recording any result; fixed by using 'A' as the test text, after which both engines PASS. Recorded here so the mistake isn't repeated.
