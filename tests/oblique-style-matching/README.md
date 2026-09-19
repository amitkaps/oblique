# oblique-style-matching

The single folder that would be proposed to WPT (`css/css-fonts/variable-oblique-interop/`). No PR is open.
This README is not copied into `.wpt/`.

```
matrix-*.html           52 generated reftests (and their -ref / -notref files), never edited by hand
matrix.manifest.json    what the reference expects for every cell, generated with them
standalone-*.html       2 hand-written tests (see below)
resources/              the one font (Cairo subset, with a .headers sidecar for WPT) and the script that builds it
oblique-matching.css    shared fixed-size layout, so pixel diffs do not depend on font metrics
```

## The matrix

Columns are the `@font-face` `font-style` descriptor: A the font's own range `oblique -11deg 11deg`, B a wider range
`oblique -20deg 20deg`, C a narrow, one-sided range `oblique 0deg 10deg`, D bare `oblique`, E `normal`, F `auto`
(omitted). Rows are the use-site request: 1 `normal`, 2 `italic`, 3 `oblique`, 4 `oblique 11deg`,
5 `oblique 5deg`, 6 `oblique 45deg`, 7 `oblique -5deg`, 8 `italic` with `font-synthesis-style: none`,
9 `oblique` with `font-synthesis: none`. A cell is `A2`; its file is
`matrix-{row slug}-{column slug}.html` (`matrix-italic-oblrange.html`). Every cell uses `resources/Cairo.var.subset.ttf`
and the capital `I`.

`reference/` decides what each cell may render and `mise run generate` writes the files. Each cell is one of:

- **specified**: one outcome, one `match` reference.
- **constrained**: several outcomes, or synthesis, are allowed; the test forbids only what the spec forbids
  (several `match` references, or `mismatch` references).
- **unspecified**: no file; the spec is silent, so the cell is only measured (`scripts/survey.py`).

References are plain faces with the axis pinned through `font-variation-settings`, so they never depend on the
descriptor under test. Only rows 8 and 9 set `font-synthesis`; that is their point. Results and what they mean:
[../../docs/findings.md](../../docs/findings.md).

## Standalone tests

Shown as group Z at the bottom of the site's results. Each quotes the CSS Fonts 4 clause it checks and uses the same
Cairo font.

| Test | Claim |
|---|---|
| `standalone-auto-keyword-equals-omitted` (Z1) | `font-style: auto` renders exactly like an omitted descriptor (4.4: `auto` is the initial value), for seven requests. Holds even where the spec is open. Not a column: it would repeat column F |
| `standalone-backslant-normal-fallback` (Z2) | `normal` against a face declared `oblique -20deg -5deg`: no oblique value >= 0 and no italic face, so the third step of the `normal` branch picks -5deg, which is `slnt 5`. Not a column: every forward request would land on the same value |

## resources/

`Cairo.var.subset.ttf` is real Cairo (SIL OFL 1.1, no Reserved Font Name) subset to the letters of `OBLIQUE` by
`build-cairo-subset.sh`, the way WPT subsets Inter for its own tests. `slnt` -11..11, `wght` 200..1000, no `ital`;
both axes and all layout and variation tables kept.

Italic fonts (an `ital` axis, an italic-declared face) are out of scope: no open-source font has both an `ital` axis
and a `slnt` axis, and WPT already covers italic fallback. The purpose-built fonts and the tests that used them are
in git history before commit `3666786`.
