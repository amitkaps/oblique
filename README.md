# Oblique

Do Chrome, Firefox and Safari match `font-style` (`normal`, `italic`, `oblique`, `slnt`) the way CSS Fonts 4
says? This repo answers that with tests, and the tests are staged as a possible
[web-platform-tests](https://github.com/web-platform-tests/wpt) contribution. **No WPT PR is open.**
Live results: <https://oblique.amitkaps.com>.

It grew out of the VizChitra/Cairo font investigation
([fonts.vizchitra.com/compat](https://fonts.vizchitra.com/compat)), which measured real-world bugs; this repo
generalises them.

## How it works

```
reference/cases/matrix.json   7 @font-face descriptors (A-G) x 12 use-site requests (1-12)
        |
reference/                    JS implementation of the CSS Fonts 4 matching rules: what may each cell render?
        |  mise run generate
tests/oblique-style-matching/ WPT reftests, one per cell the spec can decide (matrix/)
        |
Chrome, Firefox (wpt run) + Safari (safaridriver)  ->  results/browser-matrix.md
        |
site/                         the grid, live in your browser, with pass/fail per engine  ->  oblique.amitkaps.com
```

The browser is the system under test; the reference never asks one. All 84 cells use one real font, the
[Cairo](https://fonts.google.com/specimen/Cairo) variable font (SIL OFL, `slnt` -11..11) subset to the letters
of `OBLIQUE`, and test the capital `I`, which shears cleanly. A cell is written `A2`: column A, row 2.

## Current result

Chrome, Firefox and Safari agree with the spec in 73 of 84 cells. Where a face is declared with a range (the font's own,
or narrower), `italic`, bare `oblique`, `<em>` and `oblique 45deg` make Chrome stack a synthetic skew on top of the real axis,
and Safari do the same or drop the axis; Firefox is correct. A range wider than the font's own passes in all three. In one
more case, `italic` with `font-synthesis-style: oblique-only` against a `normal` face, Chrome and Safari synthesize when the
spec forbids it. Details, the claims that were withdrawn, and what is open: [docs/findings.md](docs/findings.md).

## Run it

```
mise run install && mise run test     # reference implementation
mise run generate                     # regenerate the WPT tests from the reference
mise run wpt-setup && mise run wpt-chrome && mise run wpt-firefox && mise run safari
mise run site-dev                     # the page, locally
```

Setup, the Safari method, and gotchas: [docs/running.md](docs/running.md). All tasks: `mise tasks`.

## Layout

| Path | What |
|---|---|
| `reference/` | the reference implementation, its tests, the saved spec text ([README](reference/README.md)) |
| `tests/oblique-style-matching/matrix/` | generated reftests and manifest; never edited by hand |
| `tests/oblique-style-matching/standalone/` | 8 additional hand-written tests: four `ital`-axis ones waiting for a real font, three awaiting matrix columns, and the `auto` equivalence test |
| `tests/oblique-style-matching/resources/` | fonts and the scripts that build them |
| `results/` | `browser-matrix.md` (recorded runs), `survey.json` (measured lean per cell) |
| `site/` | the page: `index.html`, `style.css`, `render.mjs` (a Vite plugin that renders the grid) |
| `scripts/` | WPT setup and sync, run and record, Safari replay, lean survey |
| `docs/` | findings, a review of the reference against the spec, and how to run |

## Prior art

- Interop proposal, 2022: <https://github.com/web-platform-tests/interop/issues/64>
- WebKit bug: <https://bugs.webkit.org/show_bug.cgi?id=209565>
- Chromium bug: <https://issues.chromium.org/issues/40681464>
- Spec discussions: <https://github.com/w3c/csswg-drafts/issues/12836>, <https://github.com/w3c/csswg-drafts/issues/3125>
- Community test page: <https://arrowtype.github.io/vf-slnt-test/>

LICENSE: BSD-3-Clause, as WPT requires.
