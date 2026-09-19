# Review of the reference implementation

An audit of `reference/` against CSS Fonts 4, done on 2026-09-20 against the live Editor's Draft. It asks two
things: is the implementation correct, and where it claims the spec leaves latitude, is that latitude real?

Summary: no algorithm bugs. The saved spec excerpts are exactly current. Latitude was overstated in two places,
one of which was masking a substantive interpretive choice, and the grid is under-constrained in a third place
that no single cell can express. The first two are fixed in the reference (each section says what changed); the
third is recorded in `docs/findings.md` as an observation and an open question.

## Spec fidelity

`curl -sL https://drafts.csswg.org/css-fonts-4/` hashes to `98604e6ac682cf04da8f53d21774b7fdbadac008772b15fc92986bcd971162f5`,
byte-identical to the hash recorded at the top of `reference/spec/css-fonts-4-excerpts.txt`. Re-extracting the live
page and diffing §2.3, §2.8, §2.8.2, §4.4, §5.2 and §7.2 against the excerpts shows them faithful, with no
paraphrase drift. The reference is reading current text.

## Correctness

48 of 48 unit tests pass; `generate --check` is clean at 142 files and 69 tests. The clamp order (descriptor, then
font, per §7.2), the CSS-to-`slnt` sign flip, the reversed-range swap (§4.4, "User agents must swap the computed
value of the startpoint and endpoint of the range"), and the negative-angle mirroring are all right.

Three spec stages are not implemented: the trailing "italic values less than or equal to 0 checked in descending
order" step in the normal, italic and both oblique branches of §5.2. They are provably inert here, because every
italic face carries the italic value exactly 1, so no such stage can ever fire; and because `resolveVariation`
branches on the face's descriptor kind rather than on the matched value's kind, a different winning stage would
give the same outcome anyway. The gap is worth a comment: the branch comment in `reference/src/match.mjs` listed
"italic <= 0" among the italic stages, but the code has no such stage. It now says so.

## Overstated latitude 1: the unconditional 14deg candidate

In `reference/src/variation.mjs`, the italic-request-on-an-oblique-face branch offers two candidate angles:

```js
for (const a of [match.value ?? ITALIC_AS_OBLIQUE_ANGLE, DEFAULT_OBLIQUE_ANGLE])
```

The second has no textual basis. 14deg is defined in §2.3 solely as the meaning of a bare `oblique` keyword; it is
never a value for an `italic` request. §7.2 is explicit that "the value applied is the closest matching value as
determined by the font matching algorithm", which is `match.value`, already computed. The only mapping the text
gives for italic is the 11deg one, which is already the `??` fallback. The justification in the code comment
("the angle and direction of slant is unspecified", §2.3) is about which face matches, not about what value to apply.

Removing it changes exactly A12, B12 and C12, and nothing else: in every other cell 11 and 14 clamp to the same
value. So it was dead latitude in 81 cells and load-bearing in three. It cannot be removed alone: the three cells
are load-bearing only because of the demotion below, which drives the applied value to 0, and the 14deg candidate
was quietly putting `slnt -11` back into the allowed set. Alone, its removal turns A12, B12 and C12 into hard
`slnt 0` tests that all three engines fail. **Applied** together with the next item.

## Overstated latitude 2: what that masks, the `oblique-only` demotion

`reference/src/match.mjs` demotes the real positive-oblique stage to a last resort when `font-synthesis-style` is
`oblique-only`. That rule is not in the Editor's Draft. Every occurrence of `oblique-only` in the live page is
framed around synthesis: §2.8.2 opens "This property controls whether user agents are allowed to synthesize oblique
font faces when a font family lacks oblique faces", and its value definition reads "Synthesis of oblique faces is
allowed, but **they** must not be used as fallback if italic is specified", where "they" are the synthesized faces.
The broader reading comes only from WPT's `font-synthesis-style-oblique-only.html` and csswg-drafts#9390.

This is structurally identical to `noItalicFallbackForOblique`, which the reference models correctly as an opt-in
`RESOLUTIONS` flag that is off by default. The demotion is hard-coded instead, so two equivalent situations are
handled two different ways.

The three readings, scored against `results/survey.json`:

| Reading | A12 / B12 / C12 | Firefox | Chrome | Safari |
|---|---|---|---|---|
| previous: demotion + the 14deg candidate | unspecified, unspecified, constrained | passes A12, B12, C12 | fails A12 and C12 (stacked) | fails A12 and C12 (skew, axis dropped) |
| demotion, no 14deg candidate | `slnt 0`, `slnt 0`, `slnt 0` | fails 3 | fails 3 | fails 3 |
| Editor's Draft text, no 14deg candidate | `slnt -11`, `slnt -11`, `slnt -5` | passes 3 | fails A12, C12 | fails A12, C12 |

The middle reading makes all three engines fail all three cells, which is `reference-suspect` by the category
`reference/src/compare.mjs` already defines. The last reading collapses row 12 onto row 2 and reproduces exactly the
pattern of A2, B2 and C2 and of every other range cell: Firefox correct, Chrome and Safari stacking a synthetic skew
on the axis. Before the change A12 and B12 had no reftest (the survey's lean check still flagged A12), and C12 had one
that allowed two outcomes. Now all three are specified reftests: A12 and C12 catch a bug the grid already confirms
elsewhere, and B12, which passes everywhere, guards the wider-range finding. D12 is unaffected either way, because
column D's `[14deg, 14deg]` range has no value at or below 0 for the demoted stage to fall through to.

In a single-face grid the demotion never changes which face is selected; it only changes which stage matches, and
so the applied value. That is the reason to default it off rather than an argument about the wording.

**Applied.** The demotion is now `RESOLUTIONS.obliqueOnlyDemotesRealObliqueFaces`, default off, turned on for the two
upstream `oblique-only` checks in `reference/test/upstream.test.mjs`. With it off, the only unit test that fails is
the upstream oblique-only intent test (plus the generated-files check until the files are regenerated).

`docs/findings.md` currently says A12 "is only measured, because the reference is not sure what `oblique-only` does to
a real oblique face", while the reference does assert outcomes for C12 (constrained) and D12 (specified) from that
same uncertain reading. Four structurally identical cells carry three different statuses; that is an artefact of the
14deg candidate interacting with clamping, not a distinction the spec draws.

## Overstated latitude 3: the G column is under-constrained across cells, not within them

The reference decides each cell independently, but §5.2's italic/oblique latitude is a property of the user agent,
not of the cell: "User agents are not required to distinguish between italic and oblique fonts. *In such user agents*,
the font-style matching steps above are performed by mapping both italic values and oblique angles onto a common
scale." A user agent picks one policy and applies it throughout, so the allowed sets in column G are correlated:

- **Distinguishes.** The italic face has the italic value 1, the font has no `ital` axis, so nothing is applied:
  G1 and G2 are both `slnt 0`.
- **Maps italic 1 onto oblique 11deg.** The face behaves as oblique `[11deg, 11deg]`: G1 and G2 are both `slnt -11`.

So the pair (G1, G2) would be (0px, 0px) or (16px, 16px). Chrome measures (16, 16). Firefox and Safari both measure
**(16, 0)**: slanted for `font-style: normal`, upright for `font-style: italic`, on the same `italic`-declared face.
The measurement is fact. That neither policy explains it is an inference: the "common scale" sentence is about
matching, and applying it to the applied value is an interpretation, so this is a question for the CSSWG, not a
verdict on the engines. It does mean asking for italic makes the glyph less italic than asking for normal. The same shape holds across the column, with G5, G10 and G12 (italic requests) at 0
and G3, G4, G7, G8, G9 and G11 (oblique requests) at 16.

`results/survey.json` already contains this. `docs/findings.md` split it across two bullets, G1 under "Agree" and G2
under "Differ", so the contradiction never surfaced; it now has its own paragraph. Asserting it as a cross-cell
invariant in `reference/src/compare.mjs` is possible without a reftest, but it would encode the interpretation as a
check, so it is deferred.

## Latitude that is real: leave these open

- **Synthesis, "will be generated" (§2.3) against "may create" (§5.2).** Forcing it to be mandatory for oblique
  requests would add "must not be upright" to E3, E4, E7, E8, E9 and to G3, G4, G7, G8, G9, and would newly fail
  Chrome and Safari on E7 and E9, which render `oblique 5deg` and `oblique -5deg` upright on a `normal` face. No
  upstream test asserts that synthesis is mandatory; the four `font-synthesis-style*` tests only assert that `none`
  disables it. Keeping it permitted is right. At ten cells this is now the largest pool of untested latitude, so it
  is the highest-value question to put to the CSSWG.
- **The E3 to E9 hedge** on a `normal`-declared face over a variable font is well reasoned and honestly recorded,
  including the scope point from csswg-drafts#7999.
- **F2, F5, F10 and F12** (`auto` plus italic) are genuinely open, and unlike column G the engines are
  self-consistent across them.
- **G9's mismatch-only test**, which forbids `slnt 5` for an `oblique -5deg` request on an italic face, is well
  built: it catches an engine that applies the request while ignoring the descriptor.

## Status accounting

59 specified, 10 constrained, 15 unspecified, applied consistently; `generate --check` agrees. One structural note:
the `universe` of constructible outcomes in `reference/src/expected.mjs` is built from upright, the font's *negative*
`slnt` extreme, and the axis value the request itself would set. It never includes the font's positive extreme except
by way of a negative-angle request, so an engine that saturated backwards on a forward request would not be caught.
No cell in the current grid needs it.

With the first two items applied, unspecified went from 15 to 13, constrained from 10 to 9 and specified from 59 to 62
(A12 and B12 became specified, C12 went from constrained to specified).
