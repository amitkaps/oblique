# font-style matching with a variable `slnt` font

Tests for how a `font-style` request (`normal`, `italic`, `oblique`, `oblique <angle>`) is matched against an
`@font-face` `font-style` descriptor, and how the result is applied to a variable font's `slnt` axis:
[CSS Fonts 4, font style matching](https://drafts.csswg.org/css-fonts-4/#font-style-matching) and
[`font-synthesis-style`](https://drafts.csswg.org/css-fonts-4/#font-synthesis-style).

## How a test reads

Every test declares one face from `resources/Cairo.var.subset.ttf` (family name "Cairo Var OBLIQUE") with one
`font-style` descriptor, then draws the capital `I` with one `font-style` request. A reference draws the same glyph
from a plain face with the axis pinned, `font-variation-settings: 'slnt' N`, which wins over any style-derived
variation (CSS Fonts 4 7.2), so no reference depends on the matching under test. References are shared: a test links
one or more of `font-style-match-slnt{N}-ref.html` as `match` (any one may match) or `mismatch` (all must differ).

Where the spec allows several outcomes, for example a synthesized oblique, the test only forbids what the spec
forbids (`mismatch` references). Where the spec is silent there is no test.

## File names

`font-style-match-{request}-{descriptor}.html`

| request | use-site declaration | | descriptor | `@font-face` declaration |
|---|---|---|---|---|
| `normal` | `font-style: normal` | | `oblrange` | `oblique -11deg 11deg` (the font's own range) |
| `italic` | `font-style: italic` | | `oblbreak` | `oblique -14deg 14deg` (past the 14deg default of bare `oblique`) |
| `oblique` | `font-style: oblique` | | `oblonesided` | `oblique 0deg 10deg` |
| `obl11` | `font-style: oblique 11deg` | | `oblique` | `oblique` (no range) |
| `obl5` | `font-style: oblique 5deg` | | `normal` | `normal` |
| `obl45` | `font-style: oblique 45deg` (beyond every range) | | `auto` | omitted (the initial value, `auto`) |
| `oblm5` | `font-style: oblique -5deg` | | | |
| `italicnone` | `italic` with `font-synthesis-style: none` | | | |
| `oblnone` | `oblique` with `font-synthesis: none` | | | |

`*.tentative.html` (the `oblm5` requests) depends on how a negative angle maps to `slnt`, which the spec words only as
"negated values and opposite directions".

`font-style-match-auto-keyword-equals-omitted` and `font-style-match-backslant-normal-fallback` are single tests, not
part of the grid: `font-style: auto` in `@font-face` renders exactly like an omitted descriptor, and `normal` against a
face declared `oblique -20deg -5deg` falls back to -5deg (`slnt 5`).

## Font

`resources/Cairo.var.subset.ttf` is Cairo (SIL OFL 1.1, no Reserved Font Name) subset to the letters of `OBLIQUE` by
`tools/build-cairo-subset.sh`, the way `css/css-fonts/variations/resources/Inter.var.subset.ttf` is made. Axes: `slnt`
-11..11 and `wght` 200..1000, no `ital`. Cairo is used instead of Inter because Inter's `slnt` axis (-10..0) is
one-sided, so it cannot show forward against backward slants or a range that crosses 0. Italic fonts (an `ital` axis)
are out of scope; italic fallback is covered elsewhere in css-fonts.

`font-style-match.css` gives the tests a fixed-size, margin-free layout so pixel diffs do not depend on font metrics.
