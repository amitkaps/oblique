# `tests/ital-axis/`

Tests the css-fonts-4 resolution of
[csswg-drafts#12836](https://github.com/w3c/csswg-drafts/issues/12836)
(merged into the published spec 2026-08-31 — see `docs/findings.md`):
`font-style: italic` sets a variable font's `ital` axis to 1 and leaves
`slnt` untouched; `font-style: oblique` sets `slnt` and leaves `ital`
untouched. The two axes are independent.

## Why a purpose-built font (`resources/IdentTestItal.ttf`)

Checked WPT's shared `/fonts/` corpus and `css/css-fonts/{resources,
variations/resources}` for a variable font exposing a real `ital` axis —
none exists. WPT does already carry `FontStyleTest-slnt-VF.woff2`
(`css/css-fonts/variations/resources/`, authored by Stephen Nixon for
[arrowtype.github.io/vf-slnt-test](https://arrowtype.github.io/vf-slnt-test/)),
which is reused for `tests/font-style-oblique/` instead of building a second
`slnt` font — but nothing equivalent exists for `ital`.

`resources/build-font.py` builds a minimal, deterministic test font with
`fontTools`: a single glyph (`block`, mapped to `A`) that is a plain
rectangle at `ital=0` and an unmistakable parallelogram at `ital=1` (the top
edge shears right by 300/1000 em via a `gvar` delta). This is the same
"compare rendered ink, not advance width" principle documented in
`vizchitra-fonts/docs/compat.md` and already used by WPT's own
`slnt-variable-ref.html` — generalized here to the `ital` axis so a reftest
can tell "did the `ital` axis actually activate" apart from "did nothing
happen," pixel-for-pixel, deterministically, with no dependency on any real
typeface's italic design.

Rebuild with `uv run tests/ital-axis/resources/build-font.py` from the repo
root (uses this repo's `pyproject.toml`/`uv.lock`, matching the
`mise`+`uv`-managed Python convention — never system Python, never conda).

## Two tests, two different failure modes

- **`independence.html`** — `oblique` must not activate `ital` at all. Forces
  `font-synthesis: none`, so it only proves the axis wasn't touched; it
  cannot tell "nothing needed to happen" apart from "synthesis was
  suppressed regardless."
- **`italic-no-extra-synthesis.html`** — `italic` must activate `ital`=1 and
  synthesize nothing further on top. Deliberately leaves `font-synthesis`
  at its default so a real bug is free to manifest. This is the one that
  actually probes WebKit #209565's documented ital-axis failure ("`italic`
  activates the axis but ALSO applies a spurious 20° synthesized slant on
  top") — and as of 2026-09-18 it **fails on Chrome 153**, live evidence
  that Chromium #40681464's fix has not shipped. See `docs/findings.md`.
