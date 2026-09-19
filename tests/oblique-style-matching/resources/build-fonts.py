"""Build the 3 purpose-built variable test fonts the hand-written boundary/
range tests need: oblique-onesided-neg.ttf, oblique-nozero.ttf,
oblique-dual-axis.ttf. (A fifth, oblique-symmetric.ttf,
lived here until the -11..11 symmetric case moved to a subset of real Cairo:
see build-cairo-subset.sh.)

Same FontBuilder pipeline as build-ident-ital-font.py (single glyph, a
rectangle sheared by a gvar delta into a deterministic, pixel-distinguishable
parallelogram) — extended to parametrize the slnt axis range per font, and,
for oblique-dual-axis.ttf, to add a second real ital axis.

Sign convention (matches this project's existing established finding, e.g.
tests/oblique-style-matching/auto-derived-range-clamp.html's comment on
Inter.var.subset.ttf): CSS positive oblique <angle> maps to a NEGATIVE slnt
value. So here, at slnt = <font's minimum> (negative), the glyph shears
RIGHT (forward lean, like a positive CSS oblique angle); at slnt = <font's
maximum> (positive, when the range includes one), the glyph shears LEFT
(backslant, negative CSS angle).

slnt and ital shear different edges of the glyph on purpose: slnt shears the
BOTTOM edge, proportional to the requested angle; ital shears the TOP edge,
by a fixed offset at ital=1 (binary axis, same convention as
build-ident-ital-font.py's IdentTestItal.ttf). This is deliberate: if a bug
ever activated the wrong axis for a request (e.g. an oblique request
accidentally nudging ital, or vice versa), the two axes would NOT produce
visually identical output, so a reftest comparing against a reference that
sets the intended axis explicitly would actually catch it — a shear that
happened to look the same regardless of which axis moved would silently
mask exactly that class of bug.

Run from the repo root: uv run tests/oblique-style-matching/resources/build-fonts.py
"""

import os

from fontTools.fontBuilder import FontBuilder
from fontTools.otlLib.builder import buildStatTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables.TupleVariation import TupleVariation

UPM = 1000
GLYPH_NAME = "block"
MAX_SLNT_SHEAR = 350  # design units, at the axis extreme

# Upright master: a plain rectangle, x in [100,900], y in [0,700] — same
# base shape as build-ident-ital-font.py's IdentTestItal.ttf.
UPRIGHT_POINTS = [(100, 0), (900, 0), (900, 700), (100, 700)]

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def base_glyph():
    pen = TTGlyphPen(None)
    pen.moveTo(UPRIGHT_POINTS[0])
    for pt in UPRIGHT_POINTS[1:]:
        pen.lineTo(pt)
    pen.closePath()
    return pen.glyph()


def slnt_tuple(direction: str, shear_units: int) -> TupleVariation:
    """direction: 'min' (negative slnt, shear bottom right) or 'max'
    (positive slnt, shear bottom left). Bottom points are indices 0,1;
    top points (2,3) are untouched."""
    if direction == "min":
        deltas = [(-shear_units, 0), (-shear_units, 0), (0, 0), (0, 0)]
        axes = {"slnt": (-1, -1, 0)}
    else:
        deltas = [(shear_units, 0), (shear_units, 0), (0, 0), (0, 0)]
        axes = {"slnt": (0, 1, 1)}
    return TupleVariation(axes=axes, coordinates=deltas + [None, None, None, None])


def ital_tuple() -> TupleVariation:
    """Fixed 300-unit rightward shift of the TOP edge at ital=1 — same
    delta shape as build-ident-ital-font.py's IdentTestItal.ttf, reused
    here so ital's signature is consistent across every font in this
    suite that has the axis."""
    deltas = [(0, 0), (0, 0), (300, 0), (300, 0)]
    return TupleVariation(axes={"ital": (0, 1, 1)}, coordinates=deltas + [None, None, None, None])


def build(name: str, family: str, slnt_range: tuple, with_ital: bool):
    slnt_min, slnt_default, slnt_max = slnt_range

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder([".notdef", GLYPH_NAME])
    fb.setupCharacterMap({ord("A"): GLYPH_NAME})
    fb.setupGlyf({".notdef": TTGlyphPen(None).glyph(), GLYPH_NAME: base_glyph()})
    fb.setupHorizontalMetrics({".notdef": (500, 0), GLYPH_NAME: (1000, 100)})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": family, "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800,
                usWinDescent=200, fsType=0)
    fb.setupPost()

    axes = [("slnt", slnt_min, slnt_default, slnt_max, "Slant")]
    stat_axes = [{"tag": "slnt", "name": "Slant", "values": [
        {"value": slnt_default, "name": "Regular", "flags": 0x2},
        {"value": slnt_min, "name": "Slant Min"},
        {"value": slnt_max, "name": "Slant Max"},
    ]}]
    if with_ital:
        axes.append(("ital", 0, 0, 1, "Italic"))
        stat_axes.append({"tag": "ital", "name": "Italic", "values": [
            {"value": 0, "name": "Regular", "flags": 0x2},
            {"value": 1, "name": "Italic"},
        ]})
    fb.setupFvar(axes=axes, instances=[{"location": {a[0]: a[2] for a in axes}, "stylename": "Regular"}])

    tuples = []
    if slnt_min < slnt_default:
        tuples.append(slnt_tuple("min", MAX_SLNT_SHEAR))
    if slnt_max > slnt_default:
        tuples.append(slnt_tuple("max", MAX_SLNT_SHEAR))
    if with_ital:
        tuples.append(ital_tuple())
    fb.setupGvar({GLYPH_NAME: tuples})

    buildStatTable(fb.font, stat_axes)

    ttf_path = os.path.join(OUT_DIR, name)
    fb.save(ttf_path)
    print(f"wrote {ttf_path}  slnt=[{slnt_min},{slnt_default},{slnt_max}]"
          f"{' +ital[0,0,1]' if with_ital else ''}")


FONTS = [
    # name, family, (slnt min, default, max), with_ital
    ("oblique-onesided-neg.ttf", "Oblique Onesided Neg Test", (-10, 0, 0), False),
    # default (12) is deliberately NOT the min boundary (5): the fallback
    # tests that use this font (boundary-0deg-normal-fallback.html,
    # multi-branch-fallback-chain.html) both expect the search to clamp to
    # 5 — if default were also 5, a correct clamp and a browser that did
    # nothing at all would render pixel-identical (both upright), and the
    # test couldn't tell them apart.
    ("oblique-nozero.ttf", "Oblique Nozero Test", (5, 12, 20), False),
    ("oblique-dual-axis.ttf", "Oblique Dual Axis Test", (-11, 0, 11), True),
]


if __name__ == "__main__":
    for name, family, slnt_range, with_ital in FONTS:
        build(name, family, slnt_range, with_ital)
