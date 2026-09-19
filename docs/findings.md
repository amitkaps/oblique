# Findings

What the tests show and what is still open. Chrome 153.0.8010.48, Firefox 156.0, Safari 27.0
(macOS 15.8). The grid is the 5 `@font-face` descriptors (A to E) by 6 use-site requests (1 to 6)
on the Cairo `OBLIQUE` subset; a cell is written `E2` (column E, row 2).

## Confirmed failures: cells E2, E3, E5

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
These are the only cells where the spec decides the outcome and an engine gets it wrong.

## How a cell is decided

`reference/` implements the CSS Fonts 4 matching rules and returns the set of outcomes the spec allows
for a cell: `upright`, `axis slnt=n`, or `synth`. A stacked axis plus synthesis is never allowed.

| Status | Meaning | Cells now |
|---|---|---|
| specified | one testable outcome; a reftest with one `match` reference | 17 |
| constrained | several outcomes, or synthesis, are allowed but something is forbidden; several `match` references or a `mismatch` | 4 |
| unspecified | the spec excludes nothing testable; no test, browsers are only measured | 9 |

Two signals agree in every cell: the reftests (Chrome and Firefox via `wpt run`, Safari via
`scripts/safari-replay.py`) and a separate measurement of the glyph's lean (`scripts/survey.py`).
`mise run compare`: 27 cells agree, 3 diverge (E2, E3, E5), none is `reference-suspect` (a cell every
engine fails, which would point at the reference or a spec gap rather than at three browsers).

Spec rules that decide cells (quoted in `reference/spec/css-fonts-4-excerpts.txt`):

- Bare `oblique` is a one-point range at 14deg; `normal` is `oblique 0deg`.
- A `font-style` descriptor "is used in place of the style implied by the underlying font data" (4.4), so
  a `normal`-declared face never reaches the `slnt` axis.
- `auto` is "selected as if normal", and "clamping does not occur".
- `italic` has no defined angle: "the angle and direction of slant is unspecified" (2.3).
- Synthesis "will be generated" in 2.3 but a UA "may create" it in 5.2, so it is permitted, not required.
- CSS angle and OpenType `slnt` have opposite signs: `oblique 11deg` is `slnt -11`.
- No generated test sets `font-synthesis`: the spec synthesizes only for a missing face, so forcing it off
  would hide an engine that synthesizes on top of a matched face.

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

1. **Grow the grid.** Proposed, not built: rows `oblique 10deg`, `12deg`, `-8deg`, `-11deg`, `45deg` (past
   the font's range) and synthesis rows (`font-synthesis-style: none`, `font-synthesis: none`,
   `oblique-only`); columns `oblique 0deg 11deg`, `oblique 5deg 20deg`, `oblique -11deg 0deg`. Review as a
   table before generating. Addresses are permanent: append, never renumber.
2. **Multi-face families** (the real 11deg ordering among several faces) are implemented and unit-tested
   in `reference/` but cannot be told apart on screen with one font. Needs another OFL font subset: ask first.
3. **Re-base the hand-written tests** on the Cairo subset, judging each with the reference; the last unbuilt
   gap is a `normal` face plus a bare-`oblique` face in one family (the way vizchitra-fonts ships Cairo).
4. **Why `wpt run safari` is wrong** here was not isolated (a loading race was tested and ruled out).
5. **Real-device Safari** (iPhone, older versions) has never been run; vizchitra-fonts saw
   version-dependent behaviour (18.7 vs 27.0).
6. **File the spec questions** with CSSWG: synthesis "will" versus "may", italic on a `slnt`-only font,
   `auto` semantics, the 14deg-versus-11deg italic slope.
7. **Upstreaming.** No WPT PR is open. `tests/oblique-style-matching/` is the single folder that would be
   proposed.
