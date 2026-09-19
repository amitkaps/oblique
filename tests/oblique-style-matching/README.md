# oblique-style-matching

The single folder that would be proposed to WPT (`css/css-fonts/variable-oblique-interop/`). No PR is open.
This README is not copied into `.wpt/`.

```
matrix/       46 generated reftests + matrix.manifest.json (never edited by hand)
standalone/   15 hand-written tests: 14 older ones kept while they are re-based on the Cairo subset, and the `auto` equivalence test
resources/    fonts (each with a .headers sidecar for WPT) and the scripts that build them
oblique-matching.css   shared fixed-size layout, so pixel diffs do not depend on font metrics
```

## matrix/

Columns are the `@font-face` `font-style` descriptor (A omitted, B `normal`, C `italic`, D bare `oblique`,
E `oblique -11deg 11deg`); rows are the use-site request (1 `normal`, 2 `italic`, 3 `oblique`,
4 `oblique 11deg`, 5 `<em>`, 6 `font-variation-settings: 'slnt' -11`, 7 `oblique 5deg`, 8 `oblique 45deg`,
9 `oblique -5deg`, 10 `italic` with `font-synthesis-style: none`, 11 `oblique` with `font-synthesis: none`,
12 `italic` with `font-synthesis-style: oblique-only`). A cell is `A2`; its file is
`matrix-{row slug}-{column slug}.html` (`matrix-italic-oblrange.html`). Every cell uses
`resources/Cairo.var.subset.ttf` and the capital `I`.

`reference/` decides what each cell may render and `mise run generate` writes the files. Each cell is one of:

- **specified**: one outcome, one `match` reference.
- **constrained**: several outcomes, or synthesis, are allowed; the test forbids only what the spec forbids
  (several `match` references, or `mismatch` references).
- **unspecified**: no file; the spec is silent, so the cell is only measured (`scripts/survey.py`).

References are plain faces with the axis pinned through `font-variation-settings`, so they never depend on the
descriptor under test. Only rows 10 to 12 set `font-synthesis`; that is their point. Results and what they mean: [../../docs/findings.md](../../docs/findings.md).

## standalone/

Each test quotes the CSS Fonts 4 clause it checks. They use several fonts, which is what the re-basing is
meant to remove; their expectations were not re-derived with the reference.

| Test | Font | Claim |
|---|---|---|
| `slnt-axis-activation` | FontStyleTest-slnt-VF (WPT's) | `oblique` activates `slnt` (baseline) |
| `auto-derived-range-clamp` | Inter subset (WPT's) | no descriptor: default angle clamps to the font's range |
| `auto-derived-range-clamp-cairo-symmetric` | Cairo | same, on Cairo's -11..11 |
| `explicit-descriptor-range-clamp` | oblique-onesided-neg | explicit descriptor range clamps |
| `boundary-11deg-ascending`, `-descending` | Cairo | the 11deg search boundaries |
| `boundary-0deg-normal-fallback` | oblique-nozero | `normal` 3-stage fallback |
| `multi-branch-fallback-chain` | oblique-nozero | `italic` 4-stage fallback |
| `italic-oblique-equivalence` | oblique-dual-axis | `oblique 11deg` against an italic-only face |
| `style-plus-explicit-variation-settings` | Cairo | `font-variation-settings` after `font-style` (7.2) |
| `ital-slnt-independence-dual-axis` | oblique-dual-axis | `ital` and `slnt` are independent |
| `independence`, `italic-no-extra-synthesis` | IdentTestItal | `italic` sets `ital`, no extra synthesis |
| `auto-keyword-equals-omitted` | Cairo | `font-style: auto` in `@font-face` renders exactly like an omitted descriptor (4.4: `auto` is the initial value), for seven requests. Says nothing about which rendering is right, so it holds even where the spec is open (italic on `auto`). Not a matrix column: it would repeat column D |
| `explicit-range-bare-keyword-synthesis-stacking` | Cairo | no synthesis on top of a clamped axis (same claim as cells A2/A3) |

## resources/

| Font | Built by | Notes |
|---|---|---|
| `Cairo.var.subset.ttf` | `build-cairo-subset.sh` | Real Cairo (SIL OFL 1.1, no Reserved Font Name) subset to the letters of `OBLIQUE`, the way WPT's `Inter.var.subset.ttf` subsets Inter. `slnt` -11..11, `wght` 200..1000, no `ital`; both axes and all layout and variation tables kept |
| `Inter.var.subset.ttf`, `FontStyleTest-slnt-VF.woff2` | copied from WPT | used by two standalone tests |
| `IdentTestItal.ttf` | `build-ident-ital-font.py` | one glyph, `ital` axis only |
| `oblique-onesided-neg.ttf`, `oblique-nozero.ttf`, `oblique-dual-axis.ttf` | `build-fonts.py` | purpose-built: `slnt` -10..0; 5..20; -11..11 with `ital` |

The purpose-built fonts use one glyph, a rectangle sheared by a `gvar` delta, so a wrong axis gives a
pixel-visible difference. `slnt` and `ital` shear different edges on purpose. Rebuilding the purpose-built
fonts changes the bytes (timestamps), so the committed files are the reference.
