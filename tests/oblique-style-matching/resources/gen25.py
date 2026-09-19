"""Generator for 25 test/ref pairs (matrix-*.html), one per cell of a
5-descriptor x 7-use-site enumeration against resources/Cairo.var.subset.ttf
(Cairo's shape), designed during a coverage-matrix session (2026-09-19) and
kept here as the record of how each reference's expected value was derived —
not part of the ongoing test-authoring toolchain otherwise. Each cell's
expected behavior was empirically measured first (pixel shear comparison,
Chrome + Firefox — see docs/investigation-log.md) before being encoded here
as a reference. Re-running this script regenerates the exact same 50 files;
it is idempotent, not a live/ongoing dependency of any other script.

All 25 use resources/Cairo.var.subset.ttf (Cairo itself, subset to the letters
of "OBLIQUE"; -11..11 slnt, no ital) and test the capital I, a plain
4-point stem, to keep this batch comparable across cells. (Originally built
against the purpose-built oblique-symmetric.ttf and its 'A' block glyph;
migrated to the real font once it was confirmed no result changed.)

Run from repo root: uv run tests/oblique-style-matching/resources/gen25.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

FONT = "resources/Cairo.var.subset.ttf"

DESCRIPTORS = {
    "auto": ("", "no font-style descriptor (auto)"),
    "normal": ("font-style: normal;", "font-style: normal"),
    "italic": ("font-style: italic;", "font-style: italic (bare, binary)"),
    "oblique-bare": ("font-style: oblique;", "font-style: oblique (bare, no angle)"),
    "oblique-range": ("font-style: oblique -11deg 11deg;", "font-style: oblique -11deg 11deg (explicit, matching true bounds)"),
}

# cell key -> (descriptor_id, use_site_css, use_site_desc, ref_kind, notes)
# ref_kind: "upright" | "slnt-11" | "MISMATCH-upright"
CELLS = [
    ("auto-r2", "auto", "font-style: oblique;", "bare font-style: oblique, default synthesis", "slnt-11",
     "Measured: 18px shear, identical to the slnt -11 baseline (18px) — clean clamp, no synthesis stacking. Extends the section-7 synthesis-stacking finding: that bug is specific to an EXPLICIT range descriptor, not the auto-derived case."),
    ("auto-r5", "auto", "", "USE_EM", "slnt-11",
     "em implies italic; auto-derived range consistently gets real-axis treatment (established by auto-derived-range-clamp*.html)."),
    ("auto-r7", "auto", "font-style: normal;", "font-style: normal", "upright",
     "normal request against an auto-derived (undeclared) single face resolves to the face's own default (upright), since 0deg is within the auto-derived range."),

    ("normal-r1", "normal", "font-style: italic;", "bare font-style: italic, default synthesis", "MISMATCH-upright",
     "Family lacks an italic/oblique face (this one is declared normal) — CSS Fonts 4 2.8.2 permits synthesis here. Measured: shear present (~16px) on both engines, not pinned to an exact value since synthetic-skew geometry is engine-defined — asserted as mismatch-vs-upright only."),
    ("normal-r2", "normal", "font-style: oblique;", "bare font-style: oblique, default synthesis", "MISMATCH-upright",
     "Same reasoning as normal-r1, oblique keyword instead of italic."),
    ("normal-r3", "normal", "font-style: oblique 11deg; font-synthesis: none;", "font-style: oblique 11deg, synthesis off", "upright",
     "Measured upright on both engines: with synthesis suppressed, a normal-declared face's real axis is not touched by an oblique request it doesn't match."),
    ("normal-r4", "normal", "font-style: oblique; font-synthesis: none;", "bare font-style: oblique, synthesis off", "upright",
     "Same as normal-r3, bare keyword."),
    ("normal-r5", "normal", "font-synthesis: none;", "USE_EM_SYNTHNONE", "upright",
     "em implies italic; with synthesis off, a normal-declared face renders upright — measured on both engines."),
    ("normal-r6", "normal", "font-variation-settings: 'slnt' -11;", "explicit font-variation-settings, bypassing font-style matching", "slnt-11",
     "Direct axis override works regardless of the declared font-style descriptor — sanity/completeness check."),
    ("normal-r7", "normal", "font-style: normal; font-synthesis: none;", "font-style: normal (exact match)", "upright",
     "Trivial baseline: a face declared normal, requested normal."),

    ("italic-r2", "italic", "font-style: oblique;", "bare font-style: oblique, default synthesis", "slnt-11",
     "An oblique request falls through to match this face via the italic branch's own oblique>=11 search's italic-fallback stage; measured 18px shear (matches real-axis baseline) on both engines — no divergence here, unlike the italic-keyword case (see italic-no-extra-synthesis.html)."),
    ("italic-r4", "italic", "font-style: oblique; font-synthesis: none;", "bare font-style: oblique, synthesis off", "slnt-11",
     "Same request as italic-r2 with synthesis suppressed — confirms the shear is real-axis, not synthetic."),
    ("italic-r5", "italic", "font-synthesis: none;", "USE_EM_SYNTHNONE", "slnt-0",
     "Cleaner re-isolation (via <em>, synthesis explicitly off) of the same divergence italic-no-extra-synthesis.html already documents for a DIFFERENT font shape (ital-axis-only). IMPORTANT construction note: an 'upright' reference built via implicit/default font-style (no override at all) is NOT reliable for this descriptor — verified directly that even an unstyled paragraph against this italic-declared face renders SHEARED on both engines (matching italic-r7's finding that this face's own declared identity gets applied regardless of the actual request). The reference here instead forces genuinely upright via an explicit font-variation-settings: 'slnt' 0, the only reliable way to pin this baseline. Measured: Chrome renders sheared for the em request (always applies this face's axis, matching its own italic identity, regardless of request — the same behavior italic-r7 documents for a plain 'normal' request too). Firefox renders upright specifically for an italic-style request (exact descriptor match needs no further axis work) even though it ALSO shears for a normal request against the same face (see italic-r7) — a narrower, request-specific distinction than a blanket 'Firefox never touches this axis' rule. EXPECTED TO FAIL ON CHROME."),
    ("italic-r6", "italic", "font-variation-settings: 'slnt' -11;", "explicit font-variation-settings, bypassing font-style matching", "slnt-11",
     "Direct axis override sanity check, italic-declared face."),
    ("italic-r7", "italic", "font-style: normal; font-synthesis: none;", "font-style: normal", "slnt-11",
     "Surprising but consistent on both engines: a normal request against a family whose only face is declared italic still renders slanted — once this face is selected as the only candidate (via the normal branch's own italic>=0 fallback stage), its own declared style is applied via the real axis regardless of the original request. Measured identically on Chrome and Firefox."),

    ("obliquebare-r1", "oblique-bare", "font-style: italic;", "bare font-style: italic, default synthesis", "slnt-11",
     "italic falls through to this face via the italic branch's oblique>=11 fallback stage; measured 18px shear (real axis) on both engines."),
    ("obliquebare-r2", "oblique-bare", "font-style: oblique;", "bare font-style: oblique, default synthesis", "slnt-11",
     "Bare oblique against a bare oblique-declared face (no explicit range) — same mechanism as auto-derived-range-clamp.html's premise, declared explicitly this time."),
    ("obliquebare-r3", "oblique-bare", "font-style: oblique 11deg; font-synthesis: none;", "font-style: oblique 11deg, synthesis off", "slnt-11",
     "Explicit angle against a bare oblique descriptor (no declared range to clamp against) — real axis set directly."),
    ("obliquebare-r4", "oblique-bare", "font-style: oblique; font-synthesis: none;", "bare font-style: oblique, synthesis off", "slnt-11",
     "Same as obliquebare-r2 with synthesis suppressed — confirms real-axis, not synthetic."),
    ("obliquebare-r5", "oblique-bare", "font-synthesis: none;", "USE_EM_SYNTHNONE", "slnt-11",
     "em implies italic; measured sheared (real axis) on both engines."),
    ("obliquebare-r6", "oblique-bare", "font-variation-settings: 'slnt' -11;", "explicit font-variation-settings, bypassing font-style matching", "slnt-11",
     "Direct axis override sanity check."),
    ("obliquebare-r7", "oblique-bare", "font-style: normal; font-synthesis: none;", "font-style: normal", "slnt-11",
     "Same pattern as italic-r7: a normal request against the only face in the family (declared oblique, bare) still renders slanted once that face is selected. Measured identically on both engines."),

    ("obliquerange-r3", "oblique-range", "font-style: oblique 11deg; font-synthesis: none;", "font-style: oblique 11deg, synthesis off", "slnt-11",
     "Explicit angle exactly at the declared range's own boundary — direct analog of boundary-11deg-ascending.html, with an explicit (not auto-derived) range descriptor."),
    ("obliquerange-r5", "oblique-range", "font-synthesis: none;", "USE_EM_SYNTHNONE", "slnt-11",
     "em implies italic; with synthesis explicitly off, the explicit-range descriptor's real axis is set directly with no risk of the synthesis-stacking bug (that bug requires synthesis to be allowed)."),
    ("obliquerange-r6", "oblique-range", "font-variation-settings: 'slnt' -11;", "explicit font-variation-settings, bypassing font-style matching", "slnt-11",
     "Direct axis override sanity check, explicit-range-declared face."),
]


USE_SITE_LABELS = {
    "USE_EM": "<em> (implicit italic via the UA stylesheet)",
    "USE_EM_SYNTHNONE": "<em> (implicit italic via the UA stylesheet), font-synthesis: none",
}


def use_site_html(use_site_css: str, use_site_desc: str) -> str:
    if use_site_desc == "USE_EM":
        return '<p class="test"><em>I</em></p>'
    if use_site_desc == "USE_EM_SYNTHNONE":
        return '<p class="test" style="font-synthesis: none"><em>I</em></p>'
    return f'<p class="test" style="{use_site_css}">I</p>'


def make_files(cell_id, desc_id, use_site_css, use_site_desc, ref_kind, notes):
    desc_css, desc_label = DESCRIPTORS[desc_id]
    use_site_label = USE_SITE_LABELS.get(use_site_desc, use_site_desc)
    test_p = use_site_html(use_site_css, use_site_desc)
    desc_css_line = f"\n    {desc_css}" if desc_css else ""
    name = f"matrix-{cell_id}-{desc_id}"

    mismatch = ref_kind.startswith("MISMATCH")
    base_kind = ref_kind.replace("MISMATCH-", "")
    ref_rel = "mismatch" if mismatch else "match"

    if base_kind == "upright":
        ref_style = ""
        pass_desc = "the reference (this same face's default, untouched rendering — upright)"
    elif base_kind == "slnt-0":
        ref_style = "font-variation-settings: 'slnt' 0;"
        pass_desc = "the reference, which forces genuinely upright via explicit font-variation-settings: 'slnt' 0 (not implicit default styling — see this cell's own comment for why)"
    else:  # slnt-11
        ref_style = "font-variation-settings: 'slnt' -11;"
        pass_desc = "the reference, which sets 'slnt' -11 directly"
    ref_style_line = f"\n    {ref_style}" if ref_style else ""

    title = f"CSS Test: {desc_label} + {use_site_label}"
    if mismatch:
        title += " (must NOT match a real-axis rendering)"

    test_html = f"""<!DOCTYPE html>
<html lang="en" class="reftest-wait">
<meta charset="utf-8" />
<title>{title}</title>
<!--
  Coverage-matrix cell: @font-face descriptor = "{desc_label}", use-site CSS
  = "{use_site_label}". Part of a systematic 5-descriptor x 7-use-site
  enumeration built for this folder's font-shape x use-site coverage matrix
  (see ../../scripts/generate-site-data.py's MATRIX_FONT_SHAPES /
  MATRIX_USE_SITE_COLUMNS, and docs/investigation-log.md for the full
  session this batch was built in).
  {notes}
-->
<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#font-style-matching" />
<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#descdef-font-face-font-style" />
<link rel="{ref_rel}" href="{name}-ref.html">
<meta name="assert"
  content="A face declared '{desc_label}', requested with '{use_site_label}',
  must {"NOT " if mismatch else ""}render the same as {pass_desc}." />
<link rel="stylesheet" href="oblique-matching.css">
<!-- Font: {FONT} — real Cairo subset (slnt -11..11, wght 200..1000, no ital); the test glyph is the capital I, a plain stem. See README.md's font shape table. -->
<style>
  @font-face {{
    font-family: "matrix test font";
    src: url('{FONT}');{desc_css_line}
  }}
  .test {{
    font-family: "matrix test font";
    font-size: 8em;
  }}
</style>
<script>
  document.fonts.ready.then(() => {{
    document.documentElement.classList.remove('reftest-wait');
  }});
</script>

{test_p}
"""

    ref_html = f"""<!DOCTYPE html>
<html lang="en" class="reftest-wait">
<meta charset="utf-8" />
<title>{title} (reference)</title>
<!--
  Reference: same face, {"default (untouched) rendering — upright" if base_kind == "upright" else ref_style}.
-->
<link rel="stylesheet" href="oblique-matching.css">
<style>
  @font-face {{
    font-family: "matrix test font";
    src: url('{FONT}');{desc_css_line}
  }}
  .test {{
    font-family: "matrix test font";
    font-size: 8em;{ref_style_line}
  }}
</style>
<script>
  document.fonts.ready.then(() => {{
    document.documentElement.classList.remove('reftest-wait');
  }});
</script>

<p class="test">I</p>
"""

    test_path = os.path.join(OUT, f"{name}.html")
    ref_path = os.path.join(OUT, f"{name}-ref.html")
    with open(test_path, "w") as f:
        f.write(test_html)
    with open(ref_path, "w") as f:
        f.write(ref_html)
    return name


if __name__ == "__main__":
    names = []
    for cell in CELLS:
        cell_id, desc_id, use_site_css, use_site_desc, ref_kind, notes = cell
        names.append(make_files(cell_id, desc_id, use_site_css, use_site_desc, ref_kind, notes))
    print(f"gen25: wrote {len(names)} test/ref pairs")
    for n in names:
        print(" ", n)
