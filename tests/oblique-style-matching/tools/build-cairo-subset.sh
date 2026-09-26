#!/usr/bin/env bash
# Rebuild Cairo.var.subset.ttf: Cairo's variable font (slnt -11..11, wght
# 200..1000) cut down to the glyphs of "OBLIQUE" — the site's display word;
# the tests themselves render only the "I".
#
# Same approach as WPT's own Inter.var.subset.ttf (css/css-fonts/variations/
# resources/): shrink the cmap, keep the real font's structure — both axes,
# gvar/avar/HVAR/MVAR/STAT, layout tables, and the OFL name records.
# Cairo (github.com/Gue3bara/Cairo) is SIL OFL 1.1 with no Reserved Font Name,
# so a subset may keep the name.
#
# Usage: tools/build-cairo-subset.sh /path/to/Cairo[slnt,wght].ttf
set -euo pipefail

src="${1:?usage: build-cairo-subset.sh /path/to/Cairo[slnt,wght].ttf}"
out="$(dirname "${BASH_SOURCE[0]}")/../resources/Cairo.var.subset.ttf"

uv run --with fonttools pyftsubset "$src" \
  --text="OBLIQUE" \
  --layout-features='*' \
  --notdef-outline \
  --name-IDs='*' \
  --output-file="$out"
echo "wrote $out"
