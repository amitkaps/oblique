"""The site's coverage matrix: @font-face `font-style` descriptor (columns A, B, C...)
x use-site request (rows 1, 2, 3...), one cell per pair, all against one font
(tests/oblique-style-matching/resources/Cairo.var.subset.ttf).

Everything about the grid comes from tests/oblique-style-matching/matrix.manifest.json,
which reference/ generates from reference/cases/matrix.json: the addresses, the labels,
what the CSS Fonts 4 reference algorithm expects in each cell, and which cells have a
WPT test. This module only reads that manifest and the recorded browser results; it
never decides an expectation.

Two kinds of cell (the manifest's `status`):
  specified / constrained  the spec pins the outcome down enough for a WPT reftest.
                           Circles show the recorded reftest results (Chrome and Firefox
                           from `wpt run`, Safari from scripts/safari-replay.py).
  unspecified              the spec leaves it open, so there is no test to pass or fail.
                           Circles show what each browser was MEASURED to do
                           (results/survey.json), as neutral "observed" markers.

verify_matrix() fails loudly if the manifest and the tests on disk or the recorded
results disagree.
"""
import hashlib
import html
import json
import math
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests" / "oblique-style-matching"
MANIFEST_PATH = TESTS_DIR / "matrix.manifest.json"
SURVEY_PATH = REPO_ROOT / "results" / "survey.json"
FONT_SRC = TESTS_DIR / "resources" / "Cairo.var.subset.ttf"
FONT_PUBLIC = REPO_ROOT / "site" / "public" / "Cairo.var.subset.ttf"
TEST_URL_BASE = "https://github.com/amitkaps/oblique/blob/main/tests/oblique-style-matching/"

MANIFEST = json.loads(MANIFEST_PATH.read_text())
COLUMNS = MANIFEST["columns"]
ROWS = MANIFEST["rows"]
CELLS = {c["address"]: c for c in MANIFEST["cells"]}
SURVEY = json.loads(SURVEY_PATH.read_text()) if SURVEY_PATH.exists() else {"engines": {}}

ENGINES = [
    {"id": "chromium", "result_key": "chrome", "label": "Chromium"},
    {"id": "firefox", "result_key": "firefox", "label": "Firefox"},
    {"id": "safari", "result_key": "safari", "label": "Safari"},
]
SPECIMEN_WORD = "OBLIQUE"


def verify_matrix(matrix_by_id: dict):
    """Fail loudly on any drift between the manifest, the tests on disk and the results."""
    if len(CELLS) != len(COLUMNS) * len(ROWS):
        raise RuntimeError("coverage_matrix: the manifest is not exactly columns x rows")
    for cell in CELLS.values():
        for name in cell["files"]:
            if not (TESTS_DIR / name).exists():
                raise RuntimeError(f"coverage_matrix: {name} (cell {cell['address']}) is missing: "
                                   f"run `node reference/src/cli.mjs generate`")
        if cell["wpt"] and cell["id"] not in matrix_by_id:
            raise RuntimeError(f"coverage_matrix: {cell['id']!r} (cell {cell['address']}) has no row in "
                               f"results/browser-matrix.md: run and record it first")
    on_disk = {p.name[:-5] for p in TESTS_DIR.glob("matrix-*.html")
               if "-ref" not in p.name and "-notref" not in p.name}
    expected = {c["id"] for c in CELLS.values() if c["wpt"]}
    if on_disk != expected:
        raise RuntimeError(f"coverage_matrix: matrix-* tests on disk disagree with the manifest: "
                           f"extra {sorted(on_disk - expected)}, missing {sorted(expected - on_disk)}")


def sync_font():
    """Copy the test font to site/public/ so the page's live specimens use the exact file
    the tests do. Copied, not symlinked (Vite and the deploy copy it)."""
    FONT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FONT_SRC, FONT_PUBLIC)
    if hashlib.sha256(FONT_SRC.read_bytes()).digest() != hashlib.sha256(FONT_PUBLIC.read_bytes()).digest():
        raise RuntimeError("coverage_matrix: site font copy differs from the test font")


def _lean_label(lean):
    """Name a measured lean, using the manifest's calibration (mirrors reference/src/compare.mjs)."""
    f = MANIFEST["font"]
    axis_max = abs(f["slnt"][0]) * f["pxPerSlntUnit"]
    synth14 = math.tan(math.radians(14)) * f["glyphHeightPx"]
    if abs(lean) <= 1.5:
        return "upright"
    if abs(lean - axis_max) <= 1.5:
        return f"real axis (slnt {f['slnt'][0]})"
    if abs(lean - synth14) <= 1.5:
        return "synthetic skew"
    if abs(lean - axis_max - synth14) <= 3:
        return "axis + synthetic (stacked)"
    return f"lean {lean}px"


def _measured(cell, engine_key):
    return SURVEY["engines"].get(engine_key, {}).get("cells", {}).get(cell["id"])


def build_cell_results(matrix_by_id, status_fn):
    """{address: {engine: status}}. Reftest cells: pass/fail/not-run from the recorded
    results. Unspecified cells: 'observed' when the survey measured them."""
    out = {}
    for addr, cell in CELLS.items():
        per = {}
        for e in ENGINES:
            key = e["result_key"]
            if cell["wpt"]:
                per[key] = status_fn(cell["id"], matrix_by_id, key)
            else:
                per[key] = "observed" if _measured(cell, key) is not None else "not-run"
        out[addr] = per
    return out


def cell_status(cell, results: dict) -> str:
    if not cell["wpt"]:
        return "observed"
    vals = {v for v in results.values() if v in ("pass", "fail")}
    if "fail" in vals:
        return "fail"
    if vals == {"pass"}:
        return "pass"
    return "unknown"


def _summary(cell_results):
    diverge = [a for a, r in cell_results.items()
               if CELLS[a]["wpt"] and {r["chrome"], r["firefox"], r["safari"]} >= {"pass", "fail"}]
    tested = sum(1 for c in CELLS.values() if c["wpt"])
    return tested, len(CELLS), diverge


def font_face_css() -> str:
    """One @font-face per column, all the same file: the live specimens."""
    out = []
    for c in COLUMNS:
        line = f" font-style: {c['descriptor']};" if c["descriptor"] else ""
        out.append(f'@font-face {{ font-family: "ob-{c["slug"]}"; src: url("/Cairo.var.subset.ttf");{line} }}')
    return "\n".join(out)


def _outcome_text(o):
    if o["kind"] == "upright":
        return "upright"
    if o["kind"] == "synth":
        return "synthesized skew"
    return f"{o['axis']} {o['value']}"


def _pinned(o):
    return f"font-variation-settings: 'slnt' {0 if o['kind'] == 'upright' else o['value']};"


def _specimen(cell) -> str:
    e = html.escape
    row = next(r for r in ROWS if r["slug"] == cell["row"])
    col = next(c for c in COLUMNS if c["slug"] == cell["column"])
    family = f"font-family: 'ob-{col['slug']}';"
    word = e(SPECIMEN_WORD)
    inner = f"<em>{word}</em>" if row.get("em") else word
    test = f'<span class="ov-test" style="{e(family + " " + cell["css"])}">{inner}</span>'
    matches = cell["plan"]["match"]
    if not matches:  # nothing to overlay: the test can only say what it must not be
        return f'<div class="overlap overlap-single">{test}</div>'
    # pink = the first reference the test would accept
    ref = f'<span class="ov-control" style="{e(family + " " + _pinned(matches[0]))}">{word}</span>'
    return f'<div class="overlap">{ref}{test}</div>'


def _badges(cell, results: dict) -> str:
    e = html.escape
    lis = []
    for eng in ENGINES:
        status = results[eng["result_key"]]
        lean = _measured(cell, eng["result_key"])
        label = None if lean is None else _lean_label(lean)
        if status == "observed":
            cls, word = "observed", f"observed: {label}"
        else:
            cls = {"pass": "pass", "fail": "fail"}.get(status, "unknown")
            word = {"pass": "pass", "fail": "fail"}.get(status, "not run")
            if label and status == "fail":
                word += f" (measured: {label})"
        lis.append(
            f'<li class="b-badge {cls}" title="{e(eng["label"])}: {e(word)}">'
            f'<img class="logo" src="/browsers/{eng["id"]}.svg" alt="{e(eng["label"])}"></li>'
        )
    return f'<ul class="verdicts">{"".join(lis)}</ul>'


def render_matrix_html(cell_results: dict, versions: dict) -> str:
    e = html.escape
    tested, total, diverge = _summary(cell_results)
    surveyed = total - tested
    parts = []

    div_txt = ""
    if diverge:
        div_txt = (f" &middot; <strong>{len(diverge)} cell{'s' if len(diverge) != 1 else ''} where the "
                   f"engines disagree with each other</strong> ({e(', '.join(sorted(diverge)))})")
    parts.append(
        f'<p class="matrix-count">{total} cells: {tested} with a WPT test the spec can decide, '
        f'{surveyed} the spec leaves open (observed only){div_txt}</p>'
    )

    parts.append(
        '<pre class="face-block"><code>'
        "@font-face {\n"
        '  font-family: "Oblique Test";\n'
        "  src: url(Cairo.var.subset.ttf);  /* real Cairo, slnt -11..11, wght 200..1000 */\n"
        "  font-style: <em>&lt;column&gt;</em>;\n"
        "}"
        "</code></pre>"
    )

    parts.append('<div class="matrix-wrap"><table class="matrix"><thead><tr><th></th>')
    for c in COLUMNS:
        parts.append(f'<th><span class="addr">{e(c["address"])}</span><code>{e(c["code"])}</code>'
                     f'<span class="col-note">{e(c["note"])}</span></th>')
    parts.append("</tr></thead><tbody>")

    for row in ROWS:
        lines = "<br>".join(e(l) for l in row["lines"])
        parts.append(f'<tr><th scope="row"><span class="row-num">{e(row["address"])}</span> <code>{lines}</code></th>')
        for col in COLUMNS:
            cell = CELLS[f"{col['address']}{row['address']}"]
            res = cell_results[cell["address"]]
            url = TEST_URL_BASE + (cell["files"][0] if cell["wpt"] else "matrix.manifest.json")
            tags = ""
            if cell["status"] != "specified":
                allowed = " / ".join(_outcome_text(o) for o in cell["allowed"])
                tags = f'<span class="tag" title="{e("; ".join(cell["why"]))}">spec allows: {e(allowed)}</span>'
            parts.append(
                f'<td class="status-{cell_status(cell, res)}">'
                f'<span class="cell-addr">{e(cell["address"])}</span>'
                f'<a class="specimen-link" href="{e(url)}" title="{e(cell["id"])}">{_specimen(cell)}</a>'
                f'{_badges(cell, res)}'
                f'<div class="cell-tags">{tags}</div></td>'
            )
        parts.append("</tr>")
    parts.append("</tbody></table></div>")

    parts.append(
        '<ul class="legend">'
        '<li><span class="b-badge pass"></span> pass</li>'
        '<li><span class="b-badge fail"></span> fail</li>'
        '<li><span class="b-badge observed"></span> observed (the spec allows it, nothing to pass or fail)</li>'
        '<li><span class="b-badge unknown"></span> not run</li>'
        '<li class="legend-note">Hover a circle for the engine and what it was measured to do. '
        'Click a specimen for its test file.</li>'
        "</ul>"
    )
    ver = []
    for eng in ENGINES:
        v = versions.get(eng["result_key"])
        ver.append(f'<li><img class="logo" src="/browsers/{eng["id"]}.svg" alt="">'
                   f'{e(eng["label"])} {e(v) if v else "&mdash; not run"}</li>')
    parts.append(f'<ul class="legend legend-versions">{"".join(ver)}</ul>')
    return "".join(parts)
