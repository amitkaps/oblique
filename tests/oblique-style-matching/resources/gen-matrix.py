"""Generator for the 30 test/ref sets (matrix-face-*-use-*.html): one per cell
of a 5-descriptor x 6-use-site grid, all against resources/Cairo.var.subset.ttf
(real Cairo, slnt -11..11, no ital) rendering the capital I.

Columns (what @font-face declares): auto (descriptor omitted), normal, italic,
oblique (bare), oblique <range> (-11deg 11deg).
Rows (the use-site CSS): normal, italic, oblique, oblique 11deg, <em>,
font-variation-settings: 'slnt' -11.

NO test sets font-synthesis. The spec's synthesis (CSS Fonts 4 2.8.2) applies
only when the family LACKS a suitable face, so a request that a declared face
satisfies must never synthesize; the default (synthesis on) is therefore the
stricter and more realistic condition, and it is the only one that can expose
a browser that synthesizes anyway (see the oblique-range column).

Expected values were derived from the spec's matching rules, then compared
with a measured rendering in Chrome and Firefox (see docs/investigation-log.md
section 10). Shear at 8em, top-vs-bottom lean of the stem: upright 0px,
real slnt -11 = 16px, synthetic 14deg skew = 21px, Chrome stacked = 36px.

Expected result per cell (`ref` kind):
  upright          the request should render upright (a plain reference)
  slnt-11          the request should reach the real axis at -11
  slnt-0           the request should NOT move the axis (explicit slnt 0)
  MISMATCH-notsynth  a normal face has no oblique face, so the UA synthesizes:
                   must differ from upright AND from the real axis
  MISMATCH-upright must differ from upright (synthetic skew at an explicit
                   angle is too close to the real axis to tell them apart)

Run from repo root: uv run tests/oblique-style-matching/resources/gen-matrix.py
Idempotent: re-running rewrites the same files.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONT = "resources/Cairo.var.subset.ttf"

# column id -> (descriptor css line or "", label)
COLS = {
    "auto": ("", "@font-face with no font-style descriptor (auto)"),
    "normal": ("font-style: normal;", "@font-face { font-style: normal }"),
    "italic": ("font-style: italic;", "@font-face { font-style: italic }"),
    "oblique-bare": ("font-style: oblique;", "@font-face { font-style: oblique }"),
    "oblique-range": ("font-style: oblique -11deg 11deg;", "@font-face { font-style: oblique -11deg 11deg }"),
}

# row id -> (use-site inline css or None for <em>, label)
ROWS = {
    "normal": ("font-style: normal;", "font-style: normal"),
    "italic": ("font-style: italic;", "font-style: italic"),
    "oblique": ("font-style: oblique;", "font-style: oblique (bare)"),
    "oblique-11deg": ("font-style: oblique 11deg;", "font-style: oblique 11deg"),
    "em": (None, "<em> (implicit italic from the UA stylesheet)"),
    "slnt": ("font-variation-settings: 'slnt' -11;", "font-variation-settings: 'slnt' -11"),
}

_AXIS = "slnt-11"
# (col, row) -> (ref kind, note). Every column x row is present: 30 cells.
GRID = {}
for row in ROWS:
    GRID[("auto", row)] = ("upright" if row == "normal" else _AXIS,
                           "No descriptor: engines derive the range from fvar, so the request reaches the real axis (clamped to -11 where the request exceeds it).")
    GRID[("oblique-bare", row)] = (_AXIS,
                                   "Bare-oblique face: the only candidate is selected and its declared oblique identity is applied through the real axis, whatever the request.")
for row in ROWS:
    ref = "upright" if row == "normal" else _AXIS
    GRID[("oblique-range", row)] = (ref, "Face declares the font's true range: the request lands on the real axis at -11, and must not be synthesized on top.")
    GRID[("italic", row)] = (_AXIS, "Italic-declared face on a slnt-only font (no ital axis).")
    GRID[("normal", row)] = ("MISMATCH-notsynth", "A face declared normal has no oblique face, whatever fvar says (the descriptor replaces the style implied by the font data, CSS Fonts 4 4.4), so the UA synthesizes.")

GRID[("normal", "normal")] = ("upright", "Exact match: a normal face for a normal request renders upright.")
GRID[("normal", "oblique-11deg")] = ("MISMATCH-upright", "A face declared normal has no oblique face, so an explicit angle is synthesized. Measured: Firefox synthesizes at the requested angle; Chrome renders upright (no synthesis at all for an explicit angle).")
GRID[("normal", "slnt")] = (_AXIS, "font-variation-settings sets the axis directly, bypassing font-style matching, whatever the descriptor.")
GRID[("italic", "normal")] = (_AXIS, "Measured on both engines: with an italic-declared face as the only candidate, even a normal request renders slanted. The face's declared style is applied via the real axis. Locked in as expected.")
GRID[("italic", "italic")] = ("slnt-0", "Italic request against an italic-declared face on a slnt-only font: an exact match needs no axis, and italic must not drive slnt (csswg-drafts#12836; section 5.2's italic axis step is scoped to fonts with an ital axis). Measured: Chrome drives slnt anyway (shears); Firefox stays upright.")
GRID[("italic", "em")] = ("slnt-0", "Same as the italic row, reached implicitly through <em>. Measured: Chrome shears, Firefox stays upright.")
GRID[("italic", "slnt")] = (_AXIS, "font-variation-settings sets the axis directly, whatever the descriptor.")
GRID[("oblique-bare", "normal")] = (_AXIS, "Measured on both engines: a normal request against the only face (declared bare oblique) still renders slanted, as with an italic-declared face.")
GRID[("oblique-range", "italic")] = (_AXIS, "Bare italic asks for the 14deg default, outside the declared range, so the axis clamps to -11. Chrome additionally synthesizes a skew on top (36px vs the expected 16px): the synthesis-stacking bug.")
GRID[("oblique-range", "oblique")] = (_AXIS, "Bare oblique likewise defaults to 14deg, outside the range. Chrome stacks a synthetic skew on top.")
GRID[("oblique-range", "em")] = (_AXIS, "<em> is implicit italic, so the same as the italic row. Chrome stacks a synthetic skew on top.")


def slug(col, row):
    return f"matrix-face-{col}-use-{row}"


def para(row, inner="I"):
    css, _ = ROWS[row]
    if css is None:
        return '<p class="test"><em>I</em></p>'
    return f'<p class="test" style="{css}">I</p>'


def face_block(desc):
    line = f"\n    {desc}" if desc else ""
    return f"""  @font-face {{
    font-family: "matrix test font";
    src: url('{FONT}');{line}
  }}"""


SCRIPT = """<script>
  document.fonts.ready.then(() => {
    document.documentElement.classList.remove('reftest-wait');
  });
</script>
"""


def ref_html(title, desc, kind_css, comment):
    override = f"\n    {kind_css}" if kind_css else ""
    return f"""<!DOCTYPE html>
<html lang="en" class="reftest-wait">
<meta charset="utf-8" />
<title>{title} (reference)</title>
<!--
  {comment}
-->
<link rel="stylesheet" href="oblique-matching.css">
<style>
{face_block(desc)}
  .test {{
    font-family: "matrix test font";
    font-size: 8em;{override}
  }}
</style>
{SCRIPT}
<p class="test">I</p>
"""


def write(path, text):
    with open(os.path.join(OUT, path), "w") as f:
        f.write(text)


def make(col, row):
    ref, note = GRID[(col, row)]
    desc, col_label = COLS[col]
    _, row_label = ROWS[row]
    name = slug(col, row)
    title = f"CSS Test: {col_label} + {row_label}"
    mismatch = ref.startswith("MISMATCH")
    if mismatch:
        title += " (must not render as a face-matched slant)"

    if ref == "MISMATCH-notsynth":
        links = (f'<link rel="mismatch" href="{name}-notupright-ref.html">\n'
                 f'<link rel="mismatch" href="{name}-notaxis-ref.html">')
        assertion = ("must NOT render upright (the UA synthesizes an oblique) and must NOT render "
                     "like the real slnt -11 axis (a face declared normal must not use the font's axis)")
    elif ref == "MISMATCH-upright":
        links = f'<link rel="mismatch" href="{name}-ref.html">'
        assertion = "must NOT render upright (the UA synthesizes an oblique at the requested angle)"
    else:
        links = f'<link rel="match" href="{name}-ref.html">'
        assertion = {
            "upright": "must render upright, the same as the reference (the face's default, untouched rendering)",
            "slnt-11": "must render the same as the reference, which sets 'slnt' -11 directly",
            "slnt-0": "must render the same as the reference, which pins 'slnt' 0 (upright): the request must not move the axis",
        }[ref]

    test = f"""<!DOCTYPE html>
<html lang="en" class="reftest-wait">
<meta charset="utf-8" />
<title>{title}</title>
<!--
  Coverage-matrix cell: column = "{col_label}", row = "{row_label}".
  One of 30 cells (5 @font-face descriptors x 6 use-site patterns) built
  for this folder's coverage matrix; see resources/gen-matrix.py for how
  each expected value was derived and docs/investigation-log.md section 10.
  font-synthesis is deliberately left at its default: the spec synthesizes
  only when the family lacks a suitable face, so a matched request must
  never synthesize, and forcing it off would hide a browser that does.
  {note}
-->
<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#font-style-matching" />
<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#descdef-font-face-font-style" />
<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#font-synthesis-style" />
{links}
<meta name="assert"
  content="A face declared '{col_label}', requested with '{row_label}',
  {assertion}." />
<link rel="stylesheet" href="oblique-matching.css">
<!-- Font: {FONT}: real Cairo subset (slnt -11..11, wght 200..1000, no ital); the test glyph is the capital I, a plain stem. -->
<style>
{face_block(desc)}
  .test {{
    font-family: "matrix test font";
    font-size: 8em;
  }}
</style>
{SCRIPT}
{para(row)}
"""
    write(f"{name}.html", test)

    if ref == "MISMATCH-notsynth":
        write(f"{name}-notupright-ref.html",
              ref_html(title, desc, "", "Reference: the same face, default (untouched) rendering: upright."))
        write(f"{name}-notaxis-ref.html",
              ref_html(title, desc, "font-variation-settings: 'slnt' -11;",
                       "Reference: the same face with the real axis set directly to slnt -11."))
        return 3
    kind_css = {"upright": "", "MISMATCH-upright": "",
                "slnt-11": "font-variation-settings: 'slnt' -11;",
                "slnt-0": "font-variation-settings: 'slnt' 0;"}[ref]
    comment = {"upright": "Reference: the same face, default rendering: upright.",
               "MISMATCH-upright": "Reference: the same face, default rendering: upright.",
               "slnt-11": "Reference: the same face with 'slnt' set directly to -11.",
               "slnt-0": "Reference: the same face with 'slnt' pinned to 0: genuinely upright. (Not implicit default styling: an italic-declared face renders sheared even unstyled.)"}[ref]
    write(f"{name}-ref.html", ref_html(title, desc, kind_css, comment))
    return 2


if __name__ == "__main__":
    assert len(GRID) == len(COLS) * len(ROWS) == 30, len(GRID)
    n = 0
    for col in COLS:
        for row in ROWS:
            n += make(col, row)
    print(f"gen-matrix: wrote 30 tests ({n} files)")
