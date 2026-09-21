# Draft: one csswg-drafts issue

Ready to paste into <https://github.com/w3c/csswg-drafts/issues/new>. Rationale, the alternatives that were
rejected and the per-engine cost: [rewording.md](rewording.md). Everything below is measured by this repo
(Chrome 153.0.8010.48, Firefox 156.0, Safari 27.0, macOS 15.8).

---

**Title:** [css-fonts-4] `font-style` matching: the applied value is unspecified when an oblique or italic request
selects a face with an oblique value of 0

## Summary

§5.2 specifies precisely which **face** is selected when a family has no oblique or italic face: the request falls
through to "oblique values less than or equal to 0deg are checked in descending order" and the upright face is
selected. It does not specify what **value is applied** to that face once it is selected: its default (upright),
the font's own `slnt` axis, or a synthesized shear at the requested angle.

The two `oblique` branches immediately above do specify this, in one sentence:

> For variable fonts with a `slnt` axis, a match is created by setting the `slnt` value with the specified oblique
> value. Otherwise, if `font-synthesis-style` has the value `auto`, then a fallback match is produced by geometric
> shearing to the specified oblique value. The `ital` axis is not used to satisfy an oblique request.

The fall-through steps have no equivalent sentence, and §2.3 ("a synthetic oblique face **will** be generated")
and §5.2's closing paragraph ("user agents **may** create artificial oblique faces") pull in different directions.

Two related gaps follow, depending on whether the selected face's `font-style` descriptor is `normal` (its applied
`slnt` range is clamped to 0 by §4.4) or `auto` / omitted (for which §4.4 says "clamping does not occur"). They are
filed together because the second is defined in terms of the first, but the proposed clauses are separate and can
be resolved separately.

## Test setup

One real variable font, the [Cairo](https://fonts.google.com/specimen/Cairo) subset (`slnt` -11..11, no `ital`
axis), one `@font-face` rule, one element. Measurements are the lean of the capital `I` at 8em: upright 0px,
`slnt -11` 16px, `slnt -5` 7px, a synthetic 14deg skew 21px, a synthetic 45deg skew 82px. `font-synthesis` is left
at its default (`auto`) except where noted. Each row below is also a reftest.

Grid, per-engine results and the reference implementation of §5.2: <https://oblique.amitkaps.com> ·
<https://github.com/amitkaps/oblique>. Tests: `tests/oblique-style-matching/matrix-*.html`.

## Gap 1: the face's descriptor is `normal`

```css
@font-face { font-family: T; src: url(Cairo.var.subset.ttf); font-style: normal; }
p { font-family: T; font-style: oblique 5deg; }   /* or italic, oblique, oblique 11deg, 45deg, -5deg */
```

The `normal` descriptor replaces the style implied by the font data (§4.4), so the applied `slnt` is clamped to 0
and the font's real axis cannot satisfy the request. That leaves upright or a synthesized shear, and the spec
permits both.

| Request | Chrome | Firefox | Safari |
|---|---|---|---|
| `italic` | 21px, synth 14deg | 21px | 21px |
| `oblique` | 21px, synth 14deg | 21px | 21px |
| `oblique 11deg` | 0px, upright | 16px, a shear (a mismatch reftest against real `slnt -11` passes) | 0px |
| `oblique 5deg` | 0px | 7px | 0px |
| `oblique 45deg` | 21px, shear stopped at 14deg | 82px, shear at 45deg | 21px |
| `oblique -5deg` | 0px | -7px | 0px |

All six rows are conformant in all three engines. Chrome and Safari appear to apply an undocumented 14deg
threshold below which they do not synthesize at all; Firefox synthesizes at the requested angle. The two rows
where the three engines agree (`italic`, `oblique`) agree by coincidence: nothing in the text requires it.

### Proposed clause 1

> If the value of `font-style` is `oblique` or `italic` and the face selected by the steps above has an oblique
> value of 0 (including a face whose `font-style` descriptor is `normal`), the `slnt` and `ital` axes are not used:
> the face is rendered at its default value. If `font-synthesis-style` has the value `auto`, a synthetic oblique
> face is then produced by geometric shearing to the requested oblique value (14deg for `italic` and for `oblique`
> without an angle). If `font-synthesis-style` has the value `none`, no synthesis occurs and the face renders
> upright.

This resolves §2.3's "will be generated" against §5.2's "may create" in favour of the former, mirrors the sentence
already present in the two `oblique` branches, and introduces no new mechanism. It preserves the behaviour all
three engines already share on `italic` and bare `oblique`, and makes it durable rather than accidental.

A related sentence would be useful in the same place: "geometric shearing to the specified oblique value" already
says the shear is at the requested angle, but Chrome and Safari stop at 14deg for `oblique 45deg`. Stating that a
synthesized shear is not subject to the clamping of §4.4 and §7.2 - there is no axis and no font capability to
clamp it to - would settle that row too.

## Gap 2: the face's descriptor is `auto` or omitted, and the request is `italic`

```css
@font-face { font-family: T; src: url(Cairo.var.subset.ttf); }   /* font-style: auto */
p { font-family: T; font-style: italic; }
```

§4.4 scopes `auto`'s two clauses separately: the face is selected as if `normal`, but "clamping does not occur", so
the applied value is limited only by the font - here `slnt` -11..11. Three outcomes are permitted, and the engines
take two of them:

| Request | Chrome | Firefox | Safari |
|---|---|---|---|
| `italic` | 16px, `slnt -11` | 16px, `slnt -11` | 0px, upright |
| `italic` with `font-synthesis-style: none` | 16px, `slnt -11` | 16px, `slnt -11` | 0px, upright |

The second row is identical to the first in all three engines, so the divergence is about whether the `slnt` axis
may satisfy an italic request at all, not about synthesis. For comparison, `font-style: oblique` on the same face
is `slnt -11` in all three engines and is decided by the spec - so under the reading Safari implements, `italic`
and `oblique` render differently on a font whose only slant axis is `slnt`, with no italic face anywhere to
distinguish them.

The text supports either reading. For upright: the italic steps never mention `slnt`, and the oblique branches say
"The `ital` axis is not used to satisfy an oblique request", whose converse is never stated. For `slnt -11`: §2.3
says `italic` "matches against a font that is labeled as an italic face, or an oblique face if one does not
exist", §5.2 says "an italic value of 1 must map to the same value that an oblique angle of 11deg maps to", and
§7.2 applies "the closest matching value as determined by the font matching algorithm".

### Proposed clause 2

> If the value of `font-style` is `italic` and the selected face has no `ital` axis and is not labelled italic, but
> exposes a `slnt` axis whose applied range is not restricted to 0 (as is the case for a face whose `font-style`
> descriptor is `auto` or omitted), a match is created by setting the `slnt` value to the value that an italic
> value of 1 maps to, clamped to the range supported by the font. No synthetic oblique face is produced in this
> case, whatever the value of `font-synthesis-style`.

The value is not new: 11deg is fixed by the existing common-scale sentence, and the clamp to the font's own range
is what §7.2 already prescribes. The no-synthesis half matters for the same reason the clamping rule does: once a
real axis match exists, §2.3's "if no oblique faces exist" is not satisfied, and a shear must not be stacked on the
axis.

## Why one issue

Both clauses fill the same hole - the algorithm names the selected face but not the applied value - in two
adjacent fall-through branches, and gap 2 is defined by reference to gap 1 ("selected as if `normal`", but
unclamped). A reviewer needs the same context for either. They are kept as two separate clauses so that one can be
adopted without the other.

## Precedent

w3c/csswg-drafts#9391 closed a structurally identical gap - behaviour that was implicit and had been read three
ways - by reordering and adding sentences to these same branches (commits `6f7c48d`, "Clarified that font
variations do not count as font synthesis", and `ac67b72`, "Distinguished use of varfont `slnt` axis from
synthetic obliquing"), rather than by introducing new machinery. The same shape of fix is proposed here.

Related: #7999 (the origin of #9391; in that thread the author scopes the no-synthesis intent to declarations
"that would not restrict the range to 0", which leaves a `normal`-declared face outside it, while the normative
text has no such exception), #9389, #9390, #3125, #12836.

## What adoption would cost

Over the 56 items this repo scores, before any engine changes: Firefox stays at 56/56 - it already renders both
proposed clauses - Chrome drops from 50 to 47 (the three explicit-angle rows of gap 1 it leaves upright) and
Safari from 50 to 45 (the same three, plus both rows of gap 2). Interoperability, scored as all three engines
rendering the same permitted thing, is 44/56 today. Six of the twelve non-interoperable items are these two gaps;
the other six are cells the spec already decides and Chrome and Safari get wrong (a synthetic skew stacked on a
matched `slnt` axis), which belong in browser trackers, not here.
