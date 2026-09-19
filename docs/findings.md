# Findings

What the tests show and what is still open. Chrome 153.0.8010.48, Firefox 156.0, Safari 27.0
(macOS 15.8). The grid is the 5 `@font-face` descriptors (A to E) by 12 use-site requests (1 to 12)
on the Cairo `OBLIQUE` subset; a cell is written `E2` (column E, row 2).

## Confirmed failures

Five cells have a spec-decided outcome that Chrome and Safari get wrong; Firefox passes all of them.

### Cells E2, E3, E5 and E8: synthesis stacked on the axis

`italic`, bare `oblique` and `<em>` against a face declared `font-style: oblique -11deg 11deg`, with
`font-synthesis` left at its default. A real oblique face exists, so the spec (2.3 "if no oblique faces
exist" is not satisfied) says the axis must clamp to `slnt -11` and nothing may be synthesized on top.

| Engine | Result |
|---|---|
| Firefox | Correct: pure axis, 16px lean |
| Chrome | Stacks a synthetic skew on the clamped axis: 36px lean |
| Safari | `italic` and `<em>`: pure synthetic skew, no axis at all (21px). Bare `oblique`: stacks like Chrome (36px) |

Lean is measured at 8em on the capital `I`: upright 0px, real `slnt -11` 16px, synthetic 14deg 21px,
stacked 36px. The same behaviour was measured independently in the sibling `vizchitra-fonts` project.
Row 8 (`oblique 45deg`, past the font's range) fails the same way on the same face: Chrome and Safari stack
(36px), Firefox clamps to the axis (16px). Rows 10 and 11 (`E10`, `E11`) repeat rows 2 and 3 with
`font-synthesis-style: none` / `font-synthesis: none` and pass everywhere, so the failures are the synthetic skew
on top of the axis and nothing else.

### Cell B12: `oblique-only` synthesizes for an italic request

`font-style: italic` with `font-synthesis-style: oblique-only` against a face declared `normal`: 2.8.2 says a
synthesized oblique "must not be used as fallback if italic is specified", so the glyph must be upright. Firefox
is upright; Chrome and Safari synthesize (21px). Upstream `font-synthesis-style-oblique-only` fails on the same two
engines. Cell E12 (the same request on the explicit-range face) shows the stacking again in Chrome and Safari but
is only measured, because the reference is not sure what `oblique-only` does to a real oblique face.

## How a cell is decided

`reference/` implements the CSS Fonts 4 matching rules and returns the set of outcomes the spec allows
for a cell: `upright`, `axis slnt=n`, or `synth`. A stacked axis plus synthesis is never allowed.

| Status | Meaning | Cells now |
|---|---|---|
| specified | one testable outcome; a reftest with one `match` reference | 37 |
| constrained | several outcomes, or synthesis, are allowed but something is forbidden; several `match` references or a `mismatch` | 9 |
| unspecified | the spec excludes nothing testable; no test, browsers are only measured | 14 |

Two signals agree in every cell: the reftests (Chrome and Firefox via `wpt run`, Safari via
`scripts/safari-replay.py`) and a separate measurement of the glyph's lean (`scripts/survey.py`).
`mise run compare`: 54 of 60 cells agree, 6 diverge (E2, E3, E5, E8, B12, and E12 which has no test), none is `reference-suspect` (a cell every
engine fails, which would point at the reference or a spec gap rather than at three browsers).

Spec rules that decide cells (quoted in `reference/spec/css-fonts-4-excerpts.txt`):

- Bare `oblique` is a one-point range at 14deg; `normal` is `oblique 0deg`.
- A `font-style` descriptor "is used in place of the style implied by the underlying font data" (4.4), so
  a `normal`-declared face never reaches the `slnt` axis.
- `auto` (descriptor omitted): §4.4 scopes its two clauses separately. For *selection* the face is treated as
  normal; for *variation clamping* "clamping does not occur". So an oblique request on an `auto` face of a font
  with a `slnt` axis sets the axis to the requested angle, limited only by the font (§5.2: a variable font with
  `slnt` matches by the axis, shearing is only the fallback). Upstream `font-face-style-auto-variable` and
  `-default-variable` assert this and pass on all three engines, and cells A3 and A4 agree. Italic and `<em>` on
  an `auto` face stay open (§5.2's italic steps never set `slnt`), so A2 and A5 are only observed: Chrome and
  Firefox slant, Safari stays upright.
- `italic` has no defined angle: "the angle and direction of slant is unspecified" (2.3).
- Synthesis "will be generated" in 2.3 but a UA "may create" it in 5.2, so it is permitted, not required.
- CSS angle and OpenType `slnt` have opposite signs: `oblique 11deg` is `slnt -11`.
- Rows 1 to 9 never set `font-synthesis`: the spec synthesizes only for a missing face, so forcing it off
  would hide an engine that synthesizes on top of a matched face. Rows 10 to 12 exist to set it.
- The size of a synthesized skew is not tested (a reftest cannot build one). Observed: for `oblique 5deg` on a
  `normal` face Firefox skews about 5deg, Chrome and Safari leave it upright; for `oblique 45deg` Chrome and
  Safari skew 14deg while Firefox skews far more. 5.2 says "geometric shearing to the specified oblique value".

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

## The hand-written tests

The 14 tests in `tests/oblique-style-matching/standalone/` predate the matrix and use several fonts.
Their pass/fail is recorded but their expectations were not re-derived with the reference, so treat their
"Chrome fails" verdicts (`italic-no-extra-synthesis`, `ital-slnt-independence-dual-axis`,
`italic-oblique-equivalence`) as unchecked: two earlier claims of the same kind were withdrawn above.

## Open

1. **Grow the grid.** Rows 7 to 12 are in (`oblique 5deg`, `45deg`, `-5deg`, and the three synthesis rows).
   Held back: `oblique 10deg` and `-11deg` (same outcome as rows 7 and 9 on one face; useful once a family has
   several faces) and `oblique 5deg` plus `font-variation-settings` (the reference must model 7.2 for a non-normal
   request first). Columns come next, each reviewed as a table: `oblique 0deg 10deg`, `oblique 5deg`,
   `oblique -20deg -5deg`, `oblique -10deg 0deg`, then families of several faces. Addresses are permanent:
   append, never renumber.
2. **Multi-face families** (the real 11deg ordering among several faces) are implemented and unit-tested
   in `reference/`. They do not need another font: several `@font-face` rules can point at the same Cairo file
   with different descriptors, and which face was chosen shows in the lean because each descriptor clamps
   differently (for example faces `oblique 5deg` and `oblique 20deg`: `oblique 10deg` gives slnt -5,
   `oblique 11deg` gives slnt -11). Not yet in the grid.
3. **Re-base the hand-written tests** on the Cairo subset, judging each with the reference; the last unbuilt
   gap is a `normal` face plus a bare-`oblique` face in one family (the way vizchitra-fonts ships Cairo).
4. **Why `wpt run safari` is wrong** here was not isolated (a loading race was tested and ruled out).
5. **Real-device Safari** (iPhone, older versions) has never been run; vizchitra-fonts saw
   version-dependent behaviour (18.7 vs 27.0).
6. **File the spec questions** with CSSWG: synthesis "will" versus "may", italic on a `slnt`-only font,
   `auto` semantics, the 14deg-versus-11deg italic slope.
7. **Upstreaming.** No WPT PR is open. `tests/oblique-style-matching/` is the single folder that would be
   proposed.
