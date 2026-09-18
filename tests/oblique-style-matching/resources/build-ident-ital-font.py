"""Build IdentTestItal[ital].ttf — a minimal purpose-built variable test font
with a single real `ital` axis and no `slnt` axis.

Why a purpose-built font: checked WPT's shared /fonts/ corpus and
css/css-fonts/{resources,variations/resources} for a variable font exposing
a real `ital` axis (0-27-2026) — none exists. WPT already carries
FontStyleTest-slnt-VF.woff2 (css/css-fonts/variations/resources) for `slnt`,
authored by Stephen Nixon for https://arrowtype.github.io/vf-slnt-test/, so
that font is reused for the font-style-oblique worked example instead of
building a second one. No equivalent exists for `ital`.

Design: one glyph ("upright"), rendered as a tall rectangle at ital=0. The
gvar delta at ital=1 shears the top edge of the rectangle to the right,
producing a recognizably different, deterministic silhouette (a parallelogram)
at ital=1 — the same "shear of rendered ink" principle documented in
vizchitra-fonts/docs/compat.md and used by WPT's own slnt-variable-ref.html,
generalized here to the `ital` axis so a reftest can tell upright from
italic-activated apart pixel-for-pixel.

Run from the repo root: uv run tests/oblique-style-matching/resources/build-ident-ital-font.py
"""

import os

from fontTools.fontBuilder import FontBuilder
from fontTools.otlLib.builder import buildStatTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables.TupleVariation import TupleVariation

UPM = 1000
GLYPH_NAME = "block"

# Upright master: a plain rectangle, x in [100,900], y in [0,700].
UPRIGHT_POINTS = [
    (100, 0), (900, 0), (900, 700), (100, 700),
]

# ital=1 delta: shear the top two points (y=700) right by 300 units,
# leave the bottom two points (y=0) untouched — turns the rectangle into
# an unmistakable parallelogram, deterministically distinguishable by pixel
# comparison at any reasonable font-size.
ITAL_DELTA_POINTS = [
    (0, 0), (0, 0), (300, 0), (300, 0),
]


def build():
    pen = TTGlyphPen(None)
    pen.moveTo(UPRIGHT_POINTS[0])
    for pt in UPRIGHT_POINTS[1:]:
        pen.lineTo(pt)
    pen.closePath()
    glyph = pen.glyph()

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder([".notdef", GLYPH_NAME])
    fb.setupCharacterMap({ord("A"): GLYPH_NAME})
    fb.setupGlyf({".notdef": TTGlyphPen(None).glyph(), GLYPH_NAME: glyph})
    fb.setupHorizontalMetrics({".notdef": (500, 0), GLYPH_NAME: (1000, 100)})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({
        "familyName": "Ital Axis Test",
        "styleName": "Regular",
    })
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800,
                usWinDescent=200, fsType=0)
    fb.setupPost()

    axes = [("ital", 0, 0, 1, "Italic")]
    instances = [
        {"location": {"ital": 0}, "stylename": "Regular"},
        {"location": {"ital": 1}, "stylename": "Italic"},
    ]
    fb.setupFvar(axes=axes, instances=instances)

    var = TupleVariation(
        axes={"ital": (0, 1, 1)},
        coordinates=ITAL_DELTA_POINTS + [None, None, None, None],
    )
    fb.setupGvar({GLYPH_NAME: [var]})

    # Good hygiene for a variable font (WPT's own FontStyleTest-slnt-VF.woff2
    # has one too) even though it turned out not to be required: an earlier
    # theory that Safari rejected this font specifically without a STAT
    # table was investigated and disproved — see docs/findings.md's "Safari
    # — attempted, no reliable result" section. The actual cause of Safari's
    # inconsistent rendering is unrelated to this font (genuine WebDriver-
    # automation flakiness, confirmed to affect WPT's own pristine font too).
    buildStatTable(fb.font, [
        {"tag": "ital", "name": "Italic", "values": [
            {"value": 0, "name": "Regular", "flags": 0x2},
            {"value": 1, "name": "Italic"},
        ]},
    ])

    out_dir = os.path.dirname(os.path.abspath(__file__))
    ttf_path = os.path.join(out_dir, "IdentTestItal.ttf")
    fb.save(ttf_path)
    print(f"wrote {ttf_path}")

    fb.font.flavor = "woff2"
    woff2_path = os.path.join(out_dir, "IdentTestItal.woff2")
    fb.font.save(woff2_path)
    print(f"wrote {woff2_path}")


if __name__ == "__main__":
    build()
