# Findings

What the tests show and what is still open. Chrome 153.0.8010.48, Firefox 156.0, Safari 27.0
(macOS 15.8). The grid is 6 `@font-face` descriptors (A to F) by 9 use-site requests (1 to 9) on the
Cairo `OBLIQUE` subset (`slnt` -11..11); a cell is written `A2` (column A, row 2). Columns: A the font's own range
`oblique -11deg 11deg`, B past CSS's break-point `oblique -14deg 14deg`, C a narrow, one-sided range `oblique 0deg 10deg`,
D bare `oblique`, E `normal`, F `auto` (descriptor omitted). Rows: 1 `normal`, 2 `italic`, 3 `oblique`,
4 `oblique 11deg`, 5 `oblique 5deg`, 6 `oblique 45deg`, 7 `oblique -5deg`, 8 `italic` with
`font-synthesis-style: none`, 9 `oblique` with `font-synthesis: none`.

Scope: oblique and `slnt`. Italic fonts (an `ital` axis, an italic-declared face) are out of scope, see
[Dropped with italic fonts](#dropped-with-italic-fonts); `italic` is still a request (rows 2 and 8), because on a
`slnt` font it is resolved through the oblique branch.

Results, over the same 56 items in every column (54 cells and 2 standalone tests): Chrome 50 (89%), Firefox 56 (100%),
Safari 50 (89%). The counts are unchanged by the move of column B from `oblique -20deg 20deg` to
`oblique -14deg 14deg` on 2026-09-20: all 9 B cells pass in all three engines at either range. A pass can be loose,
so the site also scores **interop**: an item counts only when all three engines
render the same allowed thing. That is 44 of 56 (79%). Six cells fail (A2, A3, A6, C2, C3, C6) and six are amber: each
engine is allowed, but they chose differently (E4, E5, E6, E7, F2, F8). Two cells (F2, F8) have no WPT test, because
nothing in them can fail; they count as conforming for an engine that rendered anything.

## Confirmed failures

Six cells have a spec-decided outcome that Chrome and Safari get wrong; Firefox passes all of them.

### Ranges: A2, A3, A6, C2, C3, C6... synthesis stacked on the axis

`italic`, bare `oblique` and `oblique 45deg` against a face declared with a range: the spec (2.3 "if no oblique
faces exist" is not satisfied) says the axis must clamp and nothing may be synthesized on top.

| Engine | Result |
|---|---|
| Firefox | Correct: pure axis (16px lean at `slnt -11`, 15px at `slnt -10`) |
| Chrome | Stacks a synthetic skew on the axis: 36px at -11, 35px at -10 |
| Safari | `italic`: pure synthetic skew, no axis (21px). Bare `oblique` and `oblique 45deg`: stacks like Chrome |

Lean is measured at 8em on the capital `I`: upright 0px, real `slnt -11` 16px, `slnt -10` 15px, synthetic 14deg 21px.
The same behaviour was measured independently in the sibling `vizchitra-fonts` project.

The range columns tell the trigger apart:

| Column | Chrome and Safari fail | Pass |
|---|---|---|
| A: the font's own range, `-11deg 11deg` | rows 2, 3, 6 | `normal`, `oblique 11deg`, `5deg`, `-5deg`, synthesis off |
| C: narrow and one-sided, `0deg 10deg` | the same rows: 2, 3, 6 | the same, including `oblique -5deg`, which clamps to upright |
| B: past the break-point, `-14deg 14deg` | none | all 9 rows, in all three engines |

- **It is not the descriptor clamp.** In column C `oblique 11deg` is outside the range yet passes, while `italic` (which
  means 14deg), bare `oblique` and `oblique 45deg` fail. Requests up to the font's own limit (11) pass; requests past it
  fail, unless the descriptor reaches beyond the font's limit. Column C repeats column A's failures with different
  numbers (`slnt -10`), and its one new probe, a negative request clamped to the range's edge (C7), passes everywhere.
- **Declaring a range that reaches past the font's own limit avoids the stacked skew in all three engines.** This is
  the practical workaround. It rests on the measured cells, not on reading Chrome's or WebKit's source. The range
  need not be generous: column B declared `-20deg 20deg` until 2026-09-20 and now declares `-14deg 14deg`, the
  smallest range that clears the font's own limit (11) and still contains the 14deg CSS implies for bare `oblique`.
  Ranges are inclusive, and rows 2, 3 and 6 sit exactly on that boundary: all three engines treat it inclusively and
  all 9 rows pass at either range, so 14deg is enough and the slack at 20deg bought nothing.
- Rows 8 and 9 repeat rows 2 and 3 with `font-synthesis-style: none` / `font-synthesis: none` and pass everywhere, so
  the failure is the synthetic skew on top of the axis and nothing else.

## How a cell is decided

`reference/` implements the CSS Fonts 4 matching rules and returns the set of outcomes the spec allows
for a cell: `upright`, `axis slnt=n`, or `synth`. A stacked axis plus synthesis is never allowed.

| Status | Meaning | Cells now |
|---|---|---|
| specified | one testable outcome; a reftest with one `match` reference | 46 |
| constrained | several outcomes, or synthesis, are allowed but something is forbidden; several `match` references or a `mismatch` | 6 |
| unspecified | the spec excludes nothing testable; no test, browsers are only measured | 2 |

Two signals agree in every cell: the reftests (Chrome and Firefox via `wpt run`, Safari via
`scripts/safari-replay.py`) and a separate measurement of the glyph's lean (`scripts/survey.py`).
`mise run compare`: 48 of 54 cells agree, 6 diverge (the six failing cells above), none is `reference-suspect` (a cell every
engine fails, which would point at the reference or a spec gap rather than at three browsers).

Spec rules that decide cells (quoted in `reference/spec/css-fonts-4-excerpts.txt`):

- Bare `oblique` is a one-point range at 14deg; `normal` is `oblique 0deg`.
- A `font-style` descriptor "is used in place of the style implied by the underlying font data" (4.4), so
  a `normal`-declared face never reaches the `slnt` axis.
- `auto` (descriptor omitted): §4.4 scopes its two clauses separately. For *selection* the face is treated as
  normal; for *variation clamping* "clamping does not occur". So an oblique request on an `auto` face of a font
  with a `slnt` axis sets the axis to the requested angle, limited only by the font (§5.2: a variable font with
  `slnt` matches by the axis, shearing is only the fallback). Upstream `font-face-style-auto-variable` and
  `-default-variable` assert this and pass on all three engines, and cells F3 and F4 agree. Italic on an
  `auto` face stays open (§5.2's italic steps never set `slnt`), so F2 and F8 are only observed: Chrome and
  Firefox slant, Safari stays upright.
- `italic` has no defined angle: "the angle and direction of slant is unspecified" (2.3). An italic request on a
  face with an oblique range applies that stage's closest value (7.2), which is the 11deg threshold, not the
  14deg of a bare `oblique`.
- Synthesis "will be generated" in 2.3 but a UA "may create" it in 5.2, so it is permitted, not required.
- A variable font's axis is not synthesis: §2.8 says such fonts "do not count as font synthesis and their use is
  not affected by the font-synthesis property", and §5.2's oblique steps set `slnt` first and shear only as the
  "Otherwise" fallback (csswg-drafts commits `6f7c48d` and `ac67b72`, #9391, from #7999). So `font-synthesis: none`
  never disables the axis (A8, A9 and F9 stay on it in all three engines), and an out-of-range angle on an `auto`
  face stops at the font's limit (upstream `synthetic-oblique-out-of-capabilities-range`, passing 3 of 3).
- CSS angle and OpenType `slnt` have opposite signs: `oblique 11deg` is `slnt -11`.
- Rows 1 to 7 never set `font-synthesis`: the spec synthesizes only for a missing face, so forcing it off
  would hide an engine that synthesizes on top of a matched face. Rows 8 and 9 exist to set it.
- The size of a synthesized skew is not tested (a reftest cannot build one). Observed: for `oblique 5deg` on a
  `normal` face Firefox skews about 5deg, Chrome and Safari leave it upright; for `oblique 45deg` Chrome and
  Safari skew 14deg while Firefox skews far more. 5.2 says "geometric shearing to the specified oblique value".

## A recorded hedge: oblique requests on a `normal`-declared variable font

Cells E3, E4, E5, E6 and E7 allow upright or a synthesized skew and forbid the real axis. The reading that gives
this is 4.4 (the descriptor replaces the font data's style, so the applied value is clamped to 0) plus "synthetic
styling ... where the font descriptors imply this is needed". Two other readings disagree:

- **Literal §5.2:** the slnt step has no exception for a range restricted to 0, so the axis match is made, clamped
  to 0, and shearing is never reached. That makes E3 to E7 upright only, and all three engines fail them.
- **The author's scope in #7999:** the no-synthesis intent covers declarations "that would not restrict the range
  to 0", which excludes `normal`. That supports the hedge.

Text and stated intent disagree, so neither is asserted. `auto` differs from `normal` here: it is the font's own
range ("implicit `auto` ranges" in #7999), so it takes the axis and is never sheared.

## Where the spec allows several outcomes, do the engines agree?

Mostly not. Eight cells are `spec*` (E2, E3, E4, E5, E6, E7, F2, F8). A loose test passes them, but that does not
make them interoperable, so the site marks a cell amber when every engine is allowed and they still differ. All three
engines render the same in only two of the eight: a `normal` face given `italic` or bare `oblique` is synthesized at the default 14deg by all
three (E2, E3). In the other six they differ: an explicit angle on a `normal` face (E4, E5, E6, E7) is skewed by
Firefox at about the requested angle, while Chrome and Safari stay upright (or use 14deg for 45deg); italic on an
`auto` face (F2, F8) is slanted by Chrome and Firefox and upright in Safari. So where the spec is silent there is little
common behaviour for it to adopt. One font, three engine versions, matched by the lean of the glyph: evidence, not
proof.

## Dropped with italic fonts

The grid no longer has an italic-declared column, `<em>`, or `font-synthesis-style: oblique-only`, and there are no
`ital`-axis tests. No open-source font has both an `ital` and an oblique axis (the combination has long been a problem:
Recursive calls its italic `CRSV`, and Inter dropped it), so there is nothing real to test them on, and WPT already
covers italic fallback. What was learned before they went (in git history before commit `3666786`):

- The old `<em>` row measured identically to the `italic` row in all seven columns and three engines; the computed style is the same.
- `oblique-only` is an italic-request feature and its meaning is still being argued (csswg-drafts#9390 is open and
  proposes that `none` also block the italic-to-oblique fallback for real faces). The one cleanly decided cell, a
  `normal` face with an italic request, is Chrome and Safari synthesizing; upstream `font-synthesis-style-oblique-only`
  fails on the same two engines. The reference keeps the broad reading as an option that is off
  (`RESOLUTIONS.obliqueOnlyDemotesRealObliqueFaces`), which is also why row 9, `font-synthesis-style: none`, could change
  if #9390 is adopted.
- A `font-variation-settings: 'slnt' -11` row was dropped too: it gives `slnt -11` in every column, so it tests the
  precedence rule of 7.2, not font matching, and every reference pins the axis with it, so an engine that ignored it
  would fail every test at once.
- On an italic-declared face of a `slnt`-only font Firefox and Safari rendered `font-style: normal` slanted and
  `font-style: italic` upright, and Chrome slanted both. §5.2 lets a UA either distinguish italic from oblique (both
  upright) or map italic onto oblique 11deg (both slanted); the split follows neither, though that reading is an
  inference, since the "common scale" sentence is about matching, not the applied value. A question for the CSSWG.

## Claims withdrawn

Kept here so they are not repeated.

1. "Chrome fails an italic-declared face on a `slnt`-only font." The spec permits both upright (no `ital`
   axis, nothing applied) and slanted (italic 1 = oblique 11deg for a UA that does not distinguish them).
2. "Chrome and Safari fail `oblique 11deg` against a `normal`-declared face." Synthesis is permitted, not
   required.
3. Earlier tables lumped the bare-`oblique` column with the `italic` one. Bare `oblique` leans for a
   `normal` request because it is a 14deg point range.

## Where the reference disagrees with an upstream WPT test

`oblique-last-resort-weight-selection` treats an italic request as a 14deg slope; the spec text says an
11deg threshold, so the text selects a different face. Recorded as a known disagreement in
`reference/test/upstream.test.mjs`, not fitted. `italic-oblique-fallback` matches only with the published
resolution csswg-drafts#9389, and `font-synthesis-style-oblique-only` only with the broader reading of #9390; the
Editor's Draft text has not caught up with either (`RESOLUTIONS` in `reference/src/match.mjs`, both off by default).

## Standalone tests (group Z)

Two hand-written tests in `tests/oblique-style-matching/` sit under the results table, on the same Cairo font. Z1,
`standalone-auto-keyword-equals-omitted`, checks that `font-style: auto` and an omitted descriptor render identically
(passes on all three engines). Z2, `standalone-backslant-normal-fallback`, checks the third step of the `normal` branch:
against a face declared `oblique -20deg -5deg`, `normal` lands on `slnt 5` (passes on all three engines). Neither is
a column: Z1 would repeat column F, and a backslant column would put every forward request on the same value.

## Open

1. **Grow the grid, sparingly.** Each new column must exercise a behaviour no column has yet. Not adding: a
   symmetric narrow range (the same class as C), a backslant column (Z2 covers its one new behaviour), `oblique 10deg`
   and `-11deg` (same outcome as rows 5 and 7 on one face) and any `font-variation-settings` row (it tests the precedence
   rule of 7.2, not matching, and every reference already depends on it). Addresses were renumbered on 2026-09-20 when italic fonts
   were dropped; from here, append, never renumber.
2. **Multi-face families** (the real 11deg ordering among several faces) are implemented and unit-tested
   in `reference/`. They do not need another font: several `@font-face` rules can point at the same Cairo file
   with different descriptors, and which face was chosen shows in the lean because each descriptor clamps
   differently (for example faces `oblique 5deg` and `oblique 20deg`: `oblique 10deg` gives slnt -5,
   `oblique 11deg` gives slnt -11). A `normal` face plus a bare-`oblique` face in one family (the way vizchitra-fonts
   ships Cairo) is the other unbuilt gap. Not yet in the grid.
3. **Why `wpt run safari` is wrong** here was not isolated (a loading race was tested and ruled out).
4. **Real-device Safari** (iPhone, older versions) has never been run; vizchitra-fonts saw
   version-dependent behaviour (18.7 vs 27.0).
5. **File the spec questions** with CSSWG, most valuable first:
   - Synthesis "will be generated" (2.3) versus a UA "may create" it (5.2). This is the largest pool of untested
     latitude: E3, E4, E5, E6 and E7, where synthesis is permitted but not required. Making it mandatory would add
     "must not be upright" to those five and newly fail Chrome and Safari on E4, E5 and E7, which render the requested
     angle upright on a `normal` face. No upstream test asserts that synthesis is mandatory; the `font-synthesis-style*`
     tests only assert that `none` disables it.
   - Whether the slnt step of §5.2 applies to a face declared `normal` (the hedge above).
   - `auto` semantics: does italic on an `auto` face use the font's own range?
   - The 14deg-versus-11deg italic slope, and the meaning of `oblique-only` (#9390).
6. **Upstreaming.** No WPT PR is open. `tests/oblique-style-matching/` is the single folder that would be
   proposed.
