# Rewording

Where the spec allows more than one rendering, what tightening would decide it, and which tightening to ask for.

Eight of the 54 cells are `spec*`: the matching algorithm permits several outcomes, so a test can forbid some
of them but cannot pin one. They are not eight separate questions. They are two, and both have the same shape:
**§5.2 says which face is selected and nothing says what value is applied to it.** The adjacent `oblique`
branches do say ("a match is created by setting the slnt value with the specified oblique value. Otherwise, if
`font-synthesis-style` has the value `auto`, then a fallback match is produced by geometric shearing"); the
branches these cells land in do not.

Measurements are the lean of the capital `I` at 8em on the Cairo subset (`slnt` -11..11): upright 0px, `slnt -11`
16px, `slnt -5` 7px, a synthetic 14deg skew 21px, a synthetic 45deg skew 82px. Chrome 153.0.8010.48,
Firefox 156.0, Safari 27.0. Cell addresses and the grid: [findings.md](findings.md).

## The two gaps

| Gap | Cells | Descriptor | Request | Allowed now | Chrome | Firefox | Safari |
|---|---|---|---|---|---|---|---|
| 1 | E2, E3, E4, E5, E6, E7 | `normal` | `italic`, `oblique`, `oblique <angle>` | `slnt 0` or `synth` | upright, except E2/E3/E6 | shears, at about the requested angle | upright, except E2/E3/E6 |
| 2 | F2, F8 | `auto` (omitted) | `italic` | `slnt 0`, `slnt -11` or `synth` | `slnt -11` | `slnt -11` | upright |

Six of the eight are not interoperable today (E4, E5, E6, E7, F2, F8); the two that agree (E2, E3) agree by
coincidence, not by guarantee.

## Gap 1: a `normal`-declared face, given an oblique or italic request

### Where the latitude comes from

1. §4.4: the descriptor "is used in place of the style implied by the underlying font data", and applied variation
   values "will be clamped to both the values specified in these descriptors ... as well as the values supported by
   the font file itself". A `normal` descriptor is `oblique 0deg 0deg`, so the applied `slnt` is clamped to 0: the
   font's real axis cannot satisfy the request, however wide it is.
2. §5.2: with no positive oblique face in the family, the request falls through to "oblique values less than or
   equal to 0deg are checked in descending order", which selects this face. The branch stops there. No sentence
   says what is applied to it.
3. §2.3 says synthesis **will** be generated ("If no oblique faces exist, and `font-synthesis-style` has the value
   `auto`, a synthetic oblique face will be generated"); §5.2's closing paragraph says a UA **may** ("user agents
   may create artificial oblique faces, if this is permitted by the value of the `font-synthesis` property").

(2) plus (3) is the whole gap: upright and synthesized are both conformant. This is the largest pool of untested
latitude in the grid — five cells with an explicit or implied angle, and three engines split two to one.

### Observed

| Cell | Request | Chrome | Firefox | Safari |
|---|---|---|---|---|
| E2 | `italic` | 21px (synth 14deg) | 21px | 21px |
| E3 | `oblique` | 21px (synth 14deg) | 21px | 21px |
| E4 | `oblique 11deg` | 0px (upright) | 16px (a shear, not the axis: the mismatch reftest against real `slnt -11` passes) | 0px |
| E5 | `oblique 5deg` | 0px | 7px | 0px |
| E6 | `oblique 45deg` | 21px (shear stopped at 14deg) | 82px (shear at 45deg) | 21px |
| E7 | `oblique -5deg` | 0px | -7px | 0px |

Chrome and Safari synthesize only when the requested angle is 14deg or more; Firefox synthesizes at whatever was
asked. Nothing in the text supports a 14deg threshold, and nothing forbids one.

### The candidates

| # | Tightening | E2-E7 become | Newly failing |
|---|---|---|---|
| T1 | Synthesis is **required** when no oblique face exists and `font-synthesis-style: auto` | one outcome: a shear at the requested angle | Chrome and Safari on E4, E5, E7 |
| T2 | Synthesis is **forbidden** for a face whose descriptor restricts the range to 0 | one outcome: upright | Firefox on E2-E7; Chrome and Safari on E2, E3, E6 |
| T3 | The literal §5.2 reading: the `slnt` step has no exception for a range restricted to 0, so the axis match is made (clamped to 0) and shearing is never reached | upright only | the same as T2, and it contradicts §4.4's "must only apply synthetic styling in cases where the font descriptors imply this is needed" |
| T4 | Say nothing; note that both are allowed | unchanged | nobody, and the six cells stay amber forever |

T2 and T3 arrive at the same rendering by different routes and both break the one behaviour all three engines
already share (E2, E3: `italic` and bare `oblique` on a `normal` face are synthesized everywhere). They also make
`font-style: italic` a no-op on the most common declaration an author writes, which is the outcome §2.3 was
written to prevent. T4 is what the grid measures today: conformance of 89-100% over an interop of 79%.

### The ideal: T1, stated as an applied-value sentence in the branch

> If the value of `font-style` is `oblique` or `italic` and the face selected by the steps above has an oblique
> value of 0 (including a face whose `font-style` descriptor is `normal`), the `slnt` and `ital` axes are not used:
> the face is rendered at its default value. If `font-synthesis-style` has the value `auto`, a synthetic oblique
> face is then produced by geometric shearing to the requested oblique value (14deg for `italic` and for `oblique`
> without an angle). If `font-synthesis-style` has the value `none`, no synthesis occurs and the face renders
> upright.

It mirrors the sentence already in the two `oblique` branches, adds no mechanism, keeps the E2/E3 behaviour all
three engines ship, resolves §2.3 against §5.2 in favour of the more specific text, and gives the author the
slant they asked for.

**The rider, which T1 does not settle by itself.** "Geometric shearing to the specified oblique value" says the
shear is at the requested angle. E6 shows Chrome and Safari stopping at 14deg for `oblique 45deg`. If the clause
is adopted, it should also say that a synthesized shear is *not* subject to the clamping of §4.4 and §7.2 (there
is no axis and no font capability to clamp to), which makes Firefox's 82px the only correct E6 rendering. Worth
stating; not worth testing yet, since a reftest cannot build a synthetic shear to compare against. Keep it as one
sentence in the issue and leave E6 measured rather than asserted.

## Gap 2: an `auto` descriptor (or none), given an italic request

### Where the latitude comes from

§4.4 scopes `auto`'s two clauses separately: for selection the face is treated as `normal`; for variation clamping
"clamping does not occur". So selection reaches this face through the same last step as gap 1, but the applied
value is *not* clamped to 0 - only to what the font supports, which here is `slnt` -11..11. Three outcomes survive:

- **upright** - the italic steps of §5.2 never mention `slnt`, and the oblique branches say "The ital axis is not
  used to satisfy an oblique request"; read as symmetric, `slnt` is not used to satisfy an italic request either.
- **`slnt -11`** - §5.2's closing paragraph: a UA that does not distinguish italic from oblique maps both onto a
  common scale in which "an italic value of 1 must map to the same value that an oblique angle of 11deg maps to",
  and §7.2 applies "the closest matching value as determined by the font matching algorithm", unclamped.
- **synth** - no oblique face exists, so §2.3 permits a skew.

F8 is the same cell with `font-synthesis-style: none`, which removes only the third option. Chrome, Firefox and
Safari render F2 and F8 identically to each other, so the split is about the axis, not about synthesis.

### The candidates

| # | Tightening | F2, F8 become | Newly failing |
|---|---|---|---|
| U1 | An italic request that reaches the oblique stages is satisfied by the `slnt` axis at the value italic 1 maps to (11deg, i.e. `slnt -11`), clamped only by the font | `slnt -11` | Safari on F2 and F8 |
| U2 | The converse of the existing sentence: the `slnt` axis is not used to satisfy an italic request | upright, plus optional synth on F2 | Chrome and Firefox on F2 and F8 |
| U3 | Say nothing | unchanged | nobody |

### The ideal: U1

Three reasons beyond the two-to-one engine split:

- **It makes F2 equal F3.** Bare `oblique` on the same `auto` face is `slnt -11` in all three engines today, and
  the spec decides it. Under U2, `font-style: italic` and `font-style: oblique` would render differently on a font
  whose only slant axis is `slnt` - the distinction §2.3 draws is between an italic *face* and an oblique one, and
  there is no italic face here to distinguish.
- **§2.3 already says so for selection**: `italic` "matches against a font that is labeled as an italic face, or an
  oblique face if one does not exist". An unclamped `auto` face *is* the oblique face here.
- **The value is not a new invention**: 11deg is fixed by the existing common-scale sentence, and the clamp to the
  font's own range is the rule §7.2 already applies.

U1 must also say that no synthesis is stacked on top, for the same reason the A and C columns fail in Chrome and
Safari today: a real axis match was found, so §2.3's "if no oblique faces exist" is not satisfied.

Proposed text:

> If the value of `font-style` is `italic` and the selected face has no `ital` axis and is not labelled italic, but
> exposes a `slnt` axis whose applied range is not restricted to 0 (as is the case for a face whose `font-style`
> descriptor is `auto` or omitted), a match is created by setting the `slnt` value to the value that an italic
> value of 1 maps to, clamped to the range supported by the font. No synthetic oblique face is produced in this
> case, whatever the value of `font-synthesis-style`.

## What both clauses would cost

Over the 56 items the site scores (54 cells and 2 standalone tests):

| Engine | Conforming today | After adoption, before any engine change |
|---|---|---|
| Chrome | 50 (89%) | 47 - loses E4, E5, E7 |
| Firefox | 56 (100%) | 56 - it already renders both proposed clauses |
| Safari | 50 (89%) | 45 - loses E4, E5, E7, F2, F8 |
| Interop | 44 (79%) | the eight `spec*` cells become decidable; 50 once all three comply, and 56 once Chrome and Safari also fix the six cells the spec already decides (A2, A3, A6, C2, C3, C6) |

Firefox implementing both clauses already is the argument to make in the issue: this is not a proposal for new
behaviour, it is a proposal to write down the one of the shipped behaviours that is coherent with the rest of the
algorithm.

## Not reworded here

- **The `italic` slope, 14deg versus 11deg.** `oblique-last-resort-weight-selection` treats an italic request as
  14deg; the text says an 11deg threshold. That is a *selection* question (which face wins), not an applied-value
  one, and it changes cells outside this grid. Separate issue.
- **`oblique-only` (#9390)** and **the italic-to-oblique fallback (#9389)**: open already, and the reference
  carries both as switchable resolutions.
- **An italic-declared face on a `slnt`-only font.** Dropped with the italic columns, no font to test it on.
- **The A and C column failures.** Chrome and Safari stack a synthetic skew on a matched axis there. The spec
  decides those cells; they are engine bugs, not wording gaps, and belong in browser trackers, not the CSSWG.

## One issue, not two

Both gaps are the same sentence missing from two adjacent branches, and gap 2's behaviour is defined in terms of
gap 1's ("selected as if `normal`, but not clamped"). Filed as one issue with two clearly separated clauses, so a
reviewer reads the context once and can still accept one clause without the other:
[issue.md](issue.md).
