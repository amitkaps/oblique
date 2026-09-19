# Findings

What the tests show and what is still open. Chrome 153.0.8010.48, Firefox 156.0, Safari 27.0
(macOS 15.8). The grid is 7 `@font-face` descriptors (A to G) by 12 use-site requests (1 to 12) on the
Cairo `OBLIQUE` subset (`slnt` -11..11); a cell is written `A2` (column A, row 2). Columns: A the font's own range
`oblique -11deg 11deg`, B a wider range `oblique -20deg 20deg`, C a narrow range `oblique -5deg 5deg`, D bare
`oblique`, E `normal`, F `auto` (descriptor omitted), G `italic`.

## Confirmed failures

Eleven cells have a spec-decided outcome that Chrome and Safari get wrong; Firefox passes all of them.

### Ranges: A2, A3, A5, A8, A12, C2, C3, C5, C8, C12... synthesis stacked on the axis

`italic`, bare `oblique`, `<em>` and `oblique 45deg` against a face declared with a range: the spec (2.3 "if no oblique
faces exist" is not satisfied) says the axis must clamp and nothing may be synthesized on top.

| Engine | Result |
|---|---|
| Firefox | Correct: pure axis (16px lean at `slnt -11`, 7px at `slnt -5`) |
| Chrome | Stacks a synthetic skew on the axis: 36px at -11, 27px at -5 |
| Safari | `italic` and `<em>`: pure synthetic skew, no axis (21px). Bare `oblique` and `oblique 45deg`: stacks like Chrome |

Lean is measured at 8em on the capital `I`: upright 0px, real `slnt -11` 16px, `slnt -5` 7px, synthetic 14deg 21px.
The same behaviour was measured independently in the sibling `vizchitra-fonts` project.

The three range columns tell the trigger apart:

| Column | Chrome and Safari fail | Pass |
|---|---|---|
| A: the font's own range, `-11deg 11deg` | rows 2, 3, 5, 8, 12 | `normal`, `oblique 11deg`, `oblique 5deg`, `-5deg`, `font-variation-settings`, synthesis off |
| C: narrow range, `-5deg 5deg` | the same rows: 2, 3, 5, 8, 12 | the same |
| B: wider than the font, `-20deg 20deg` | none | all 12 rows, in all three engines |

- **It is not the descriptor clamp.** In column C `oblique 11deg` is outside the range yet passes, while `italic` (which
  means 14deg) and `oblique 45deg` fail. Requests up to the font's own limit (11) pass; requests past it fail, unless
  the descriptor reaches beyond the font's limit.
- **Declaring a range wider than the font's own avoids the stacked skew in all three engines.** This is the practical
  workaround. It rests on about 90 measured cells, not on reading Chrome's or WebKit's source.
- Rows 10 and 11 repeat rows 2 and 3 with `font-synthesis-style: none` / `font-synthesis: none` and pass everywhere, so
  the failure is the synthetic skew on top of the axis and nothing else.

### Cell E12: `oblique-only` synthesizes for an italic request

`font-style: italic` with `font-synthesis-style: oblique-only` against a face declared `normal`: 2.8.2 says a
synthesized oblique "must not be used as fallback if italic is specified", so the glyph must be upright. Firefox
is upright; Chrome and Safari synthesize (21px). Upstream `font-synthesis-style-oblique-only` fails on the same two
engines. Cell A12 (the same request on the font's own range) is the stacking again: 2.8.2 speaks of synthesized faces,
so the real oblique face still matches and the axis at -11 is the outcome. Reading `oblique-only` more broadly, so that
real oblique faces are also a last resort for italic (the reading behind the WPT test, csswg-drafts#9390), would make
A12, B12 and C12 upright, and all three engines contradict that. The reference keeps that reading as an option that
is off; see [review.md](review.md).

## How a cell is decided

`reference/` implements the CSS Fonts 4 matching rules and returns the set of outcomes the spec allows
for a cell: `upright`, `axis slnt=n`, or `synth`. A stacked axis plus synthesis is never allowed.

| Status | Meaning | Cells now |
|---|---|---|
| specified | one testable outcome; a reftest with one `match` reference | 62 |
| constrained | several outcomes, or synthesis, are allowed but something is forbidden; several `match` references or a `mismatch` | 9 |
| unspecified | the spec excludes nothing testable; no test, browsers are only measured | 13 |

Two signals agree in every cell: the reftests (Chrome and Firefox via `wpt run`, Safari via
`scripts/safari-replay.py`) and a separate measurement of the glyph's lean (`scripts/survey.py`).
`mise run compare`: 73 of 84 cells agree, 11 diverge (the eleven failing cells above), none is `reference-suspect` (a cell every
engine fails, which would point at the reference or a spec gap rather than at three browsers).

Spec rules that decide cells (quoted in `reference/spec/css-fonts-4-excerpts.txt`):

- Bare `oblique` is a one-point range at 14deg; `normal` is `oblique 0deg`.
- A `font-style` descriptor "is used in place of the style implied by the underlying font data" (4.4), so
  a `normal`-declared face never reaches the `slnt` axis.
- `auto` (descriptor omitted): §4.4 scopes its two clauses separately. For *selection* the face is treated as
  normal; for *variation clamping* "clamping does not occur". So an oblique request on an `auto` face of a font
  with a `slnt` axis sets the axis to the requested angle, limited only by the font (§5.2: a variable font with
  `slnt` matches by the axis, shearing is only the fallback). Upstream `font-face-style-auto-variable` and
  `-default-variable` assert this and pass on all three engines, and cells F3 and F4 agree. Italic and `<em>` on
  an `auto` face stay open (§5.2's italic steps never set `slnt`), so F2 and F5 are only observed: Chrome and
  Firefox slant, Safari stays upright.
- `italic` has no defined angle: "the angle and direction of slant is unspecified" (2.3).
- Synthesis "will be generated" in 2.3 but a UA "may create" it in 5.2, so it is permitted, not required.
- A variable font's axis is not synthesis: §2.8 says such fonts "do not count as font synthesis and their use is
  not affected by the font-synthesis property", and §5.2's oblique steps set `slnt` first and shear only as the
  "Otherwise" fallback (csswg-drafts commits `6f7c48d` and `ac67b72`, #9391, from #7999). So `font-synthesis: none`
  never disables the axis (A10, A11 and F11 stay on it in all three engines), and an out-of-range angle on an `auto`
  face stops at the font's limit (upstream `synthetic-oblique-out-of-capabilities-range`, passing 3 of 3).
- CSS angle and OpenType `slnt` have opposite signs: `oblique 11deg` is `slnt -11`.
- Rows 1 to 9 never set `font-synthesis`: the spec synthesizes only for a missing face, so forcing it off
  would hide an engine that synthesizes on top of a matched face. Rows 10 to 12 exist to set it.
- The size of a synthesized skew is not tested (a reftest cannot build one). Observed: for `oblique 5deg` on a
  `normal` face Firefox skews about 5deg, Chrome and Safari leave it upright; for `oblique 45deg` Chrome and
  Safari skew 14deg while Firefox skews far more. 5.2 says "geometric shearing to the specified oblique value".

## A recorded hedge: oblique requests on a `normal`-declared variable font

Cells E3, E4, E7, E8 and E9 allow upright or a synthesized skew and forbid the real axis. The reading that gives
this is 4.4 (the descriptor replaces the font data's style, so the applied value is clamped to 0) plus "synthetic
styling ... where the font descriptors imply this is needed". Two other readings disagree:

- **Literal §5.2:** the slnt step has no exception for a range restricted to 0, so the axis match is made, clamped
  to 0, and shearing is never reached. That makes E3 to E9 upright only, and all three engines fail them.
- **The author's scope in #7999:** the no-synthesis intent covers declarations "that would not restrict the range
  to 0", which excludes `normal`. That supports the hedge.

Text and stated intent disagree, so neither is asserted. `auto` differs from `normal` here: it is the font's own
range ("implicit `auto` ranges" in #7999), so it takes the axis and is never sheared.

## Where the spec is open, do the engines agree?

Of the 22 cells where the spec allows several outcomes, all three engines render the same in 10. If they converge, the spec
could simply say so; where they differ is the list to take to the spec authors. One font, three engine versions, matched by
the lean of the glyph, so this is evidence rather than proof.

- **Agree (10):** a `normal` face given `italic`, bare `oblique` or `<em>` is synthesized at the default 14deg by all three
  (E2, E3, E5); an italic-declared face on a `slnt`-only font takes the axis at -11 for a `normal` request, bare `oblique`,
  `oblique 11deg`, `5deg`, `45deg`, `-5deg` and `oblique` with synthesis off (G1, G3, G4, G7, G8, G9, G11).
- **Differ (12):** italic on an italic-declared face (G2, G5, G10, G12): Chrome takes the axis, Firefox and Safari stay upright.
  Italic on an `auto` face (F2, F5, F10, F12): Chrome and Firefox take the axis, Safari stays upright. An explicit small
  angle on a `normal` face (E4, E7, E8, E9): Firefox skews at the requested angle, Chrome and Safari stay upright (or use 14deg
  for 45deg).

**G1 against G2 is inconsistent.** Firefox and Safari render the italic-declared face slanted for `font-style: normal`
(G1, 16px) and upright for `font-style: italic` (G2, 0px); Chrome slants both. 5.2 lets a user agent either distinguish
italic from oblique (nothing to apply without an `ital` axis, so both upright) or map italic onto oblique 11deg (both
slanted). Read that way, neither gives 16 then 0, which makes asking for italic less italic than asking for normal. The
same split runs down the column in those two engines: italic requests (G2, G5, G10, G12) upright, oblique requests
(G3, G4, G7, G8, G9, G11) slanted. The measurement is fact; that no policy explains it is an inference, because the
"common scale" sentence is about matching, not the applied value. It is a question for the CSSWG, and no reftest can
decide it.

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
resolution csswg-drafts#9389, which the Editor's Draft text has not caught up with (`RESOLUTIONS` in
`reference/src/match.mjs`, off by default).

## Additional tests

Eight hand-written tests in `tests/oblique-style-matching/standalone/` sit under the results table.
`auto-keyword-equals-omitted` checks that `font-style: auto` and an omitted descriptor render identically (passes on all
three engines). Three (`explicit-descriptor-range-clamp`, `boundary-0deg-normal-fallback`, `multi-branch-fallback-chain`)
will be replaced by matrix columns. Four test the `ital` axis and wait for a real font that has one; their expectations were
not re-derived with the reference, so treat their verdicts (Chrome fails `italic-no-extra-synthesis` and
`ital-slnt-independence-dual-axis`, every engine fails `italic-oblique-equivalence`) as unchecked: two earlier claims of the
same kind were withdrawn above.

Seven earlier hand-written tests were deleted because the matrix covers them. Two of them (`auto-derived-range-clamp` and its
Cairo twin) failed in Safari only through their bare `italic` half, where the spec is open, so those failures were never findings.

## Open

1. **Grow the grid, sparingly.** Rows 7 to 12 are in (`oblique 5deg`, `45deg`, `-5deg`, and the three synthesis rows).
   Not adding: `oblique 10deg` and `-11deg` (same outcome as rows 7 and 9 on one face) and a `font-variation-settings`
   row with a non-normal request (font-variation-settings always wins by the cascade, and row 6 covers it). Columns are
   the open question: each new one must exercise a behaviour no column has yet. Candidates: a range narrower than the
   font (`oblique 0deg 5deg`, so a descriptor clamp differs clearly from a font clamp) and a backslant-only range (the
   last-resort stages), each reviewed as a table before it is added. Addresses are permanent: append, never renumber.
2. **Multi-face families** (the real 11deg ordering among several faces) are implemented and unit-tested
   in `reference/`. They do not need another font: several `@font-face` rules can point at the same Cairo file
   with different descriptors, and which face was chosen shows in the lean because each descriptor clamps
   differently (for example faces `oblique 5deg` and `oblique 20deg`: `oblique 10deg` gives slnt -5,
   `oblique 11deg` gives slnt -11). Not yet in the grid.
3. **A real `ital` font.** Find an OFL font with a real `ital` axis to subset, then move the four `ital` tests onto it
   and model `ital` on an `auto` face in the reference. The other unbuilt gap is a `normal` face plus a bare-`oblique`
   face in one family (the way vizchitra-fonts ships Cairo).
4. **Why `wpt run safari` is wrong** here was not isolated (a loading race was tested and ruled out).
5. **Real-device Safari** (iPhone, older versions) has never been run; vizchitra-fonts saw
   version-dependent behaviour (18.7 vs 27.0).
6. **File the spec questions** with CSSWG: synthesis "will" versus "may", italic on a `slnt`-only font,
   `auto` semantics (does italic on an `auto` face use the font's own range?), the 14deg-versus-11deg italic slope,
   and whether the slnt step of §5.2 applies to a face declared `normal` (the hedge above).
7. **Upstreaming.** No WPT PR is open. `tests/oblique-style-matching/` is the single folder that would be
   proposed.
