"""The site's coverage matrix: @font-face `font-style` descriptor (columns) x
use-site CSS (rows), one test per cell, all against one font
(tests/oblique-style-matching/resources/Cairo.var.subset.ttf).

Imported by generate-site-data.py. Everything here is data + rendering; the
per-engine results themselves come from results/browser-matrix.md (this
repo's own `wpt run` results), never from upstream wpt.fyi data.

Each populated cell holds exactly ONE test. Where a single test file already
exercises two cells (it has two paragraphs), both cells point at it and say
so with a "shared file" tag rather than pretending to per-paragraph results.

verify_matrix() fails loudly, same discipline as verify_category_mapping():
every cell's test must exist, be recorded in browser-matrix.md, and its HTML
must actually contain the descriptor and use-site CSS the cell claims.
"""
import hashlib
import html
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests" / "oblique-style-matching"
FONT_SRC = TESTS_DIR / "resources" / "Cairo.var.subset.ttf"
FONT_PUBLIC = REPO_ROOT / "site" / "public" / "Cairo.var.subset.ttf"
TEST_URL_BASE = "https://github.com/amitkaps/oblique/blob/main/tests/oblique-style-matching/"

# Column = what the @font-face declares. `css` is the descriptor line the
# tests use (None = no font-style descriptor at all, which is defined as
# `auto`). The id also names the live specimen's font-family ("ob-<id>").
COLUMNS = [
    {"id": "auto", "css": None, "code": "@font-face { /* font-style omitted */ }",
     "note": "Descriptor omitted, which is defined as auto: matched as if normal"},
    {"id": "normal", "css": "font-style: normal;", "code": "@font-face { font-style: normal; }",
     "note": "Declared upright"},
    {"id": "italic", "css": "font-style: italic;", "code": "@font-face { font-style: italic; }",
     "note": "Declared italic (binary, no angle)"},
    {"id": "oblique-bare", "css": "font-style: oblique;", "code": "@font-face { font-style: oblique; }",
     "note": "Declared oblique, no range"},
    {"id": "oblique-range", "css": "font-style: oblique -11deg 11deg;",
     "code": "@font-face { font-style: oblique -11deg 11deg; }",
     "note": "Declared oblique with the font's true slnt range"},
]

# Row = the use-site CSS. `lines` is what the header shows; `css` is the
# inline style the live specimen applies (None for <em>, which gets
# `font-style: italic` from the UA stylesheet); `em` marks the <em> row.
# `check` = the declarations every test in that row must contain.
ROWS = [
    {"num": 1, "id": "italic", "lines": ["font-style: italic;"],
     "css": "font-style: italic;", "check": ["font-style: italic"]},
    {"num": 2, "id": "oblique", "lines": ["font-style: oblique;"],
     "css": "font-style: oblique;", "check": ["font-style: oblique"]},
    {"num": 3, "id": "oblique-angle", "lines": ["font-style: oblique 11deg;", "font-synthesis: none;"],
     "css": "font-style: oblique 11deg; font-synthesis: none;",
     "check": ["font-style: oblique 11deg", "font-synthesis: none"]},
    {"num": 4, "id": "oblique-synth-off", "lines": ["font-style: oblique;", "font-synthesis: none;"],
     "css": "font-style: oblique; font-synthesis: none;",
     "check": ["font-style: oblique", "font-synthesis: none"]},
    {"num": 5, "id": "em", "lines": ["<em>", "font-synthesis: none;"],
     "css": "font-synthesis: none;", "em": True, "check": ["<em>", "font-synthesis: none"]},
    {"num": 6, "id": "slnt", "lines": ["font-variation-settings: 'slnt' -11;"],
     "css": "font-variation-settings: 'slnt' -11;", "check": ["font-variation-settings: \"slnt\" -11"]},
    {"num": 7, "id": "normal", "lines": ["font-style: normal;", "font-synthesis: none;"],
     "css": "font-style: normal; font-synthesis: none;",
     "check": ["font-style: normal", "font-synthesis: none"]},
]

# The pink layer of each specimen: what the test's own reference renders.
REF_CSS = {
    "upright": "",
    "slnt-11": "font-variation-settings: 'slnt' -11;",
    "slnt-0": "font-variation-settings: 'slnt' 0;",
}

_SHARED = "shared file"


def _c(test_id, ref, css=None, check=None, tags=()):
    """One populated cell. `css`/`check` override the row's own when the
    test's actual CSS differs (e.g. it ran with synthesis off in a row that
    otherwise leaves it at the default); `ref` = 'mismatch' for reftests
    that assert the test must NOT match an upright rendering."""
    return {"test": test_id, "ref": ref, "css": css, "check": check, "tags": list(tags)}


# (column id, row id) -> cell. Absent = no test on THIS font yet (blank).
CELLS = {
    # auto: descriptor omitted
    ("auto", "italic"): _c("auto-derived-range-clamp-cairo-symmetric", "slnt-11",
                           css="font-style: italic; font-synthesis: none;",
                           check=["font-style: italic", "font-synthesis: none"],
                           tags=[_SHARED, "synthesis off"]),
    ("auto", "oblique"): _c("matrix-auto-r2-auto", "slnt-11"),
    ("auto", "oblique-angle"): _c("boundary-11deg-ascending", "slnt-11"),
    ("auto", "oblique-synth-off"): _c("auto-derived-range-clamp-cairo-symmetric", "slnt-11",
                                      tags=[_SHARED]),
    ("auto", "em"): _c("matrix-auto-r5-auto", "slnt-11", css="", check=["<em>"],
                       tags=["synthesis default"]),
    ("auto", "slnt"): _c("style-plus-explicit-variation-settings", "slnt-11",
                         css="font-style: oblique 5deg; font-variation-settings: 'slnt' -11;",
                         check=["font-style: oblique 5deg", "font-variation-settings: \"slnt\" -11"],
                         tags=["combo with oblique 5deg", "synthesis off"]),
    ("auto", "normal"): _c("matrix-auto-r7-auto", "upright", css="font-style: normal;",
                           check=["font-style: normal"], tags=["synthesis default"]),
    # normal
    ("normal", "italic"): _c("matrix-normal-r1-normal", "mismatch"),
    ("normal", "oblique"): _c("matrix-normal-r2-normal", "mismatch"),
    ("normal", "oblique-angle"): _c("matrix-normal-r3-normal", "upright"),
    ("normal", "oblique-synth-off"): _c("matrix-normal-r4-normal", "upright"),
    ("normal", "em"): _c("matrix-normal-r5-normal", "upright"),
    ("normal", "slnt"): _c("matrix-normal-r6-normal", "slnt-11"),
    ("normal", "normal"): _c("matrix-normal-r7-normal", "upright"),
    # italic (row 1 and 3 have no test on this font yet)
    ("italic", "oblique"): _c("matrix-italic-r2-italic", "slnt-11"),
    ("italic", "oblique-synth-off"): _c("matrix-italic-r4-italic", "slnt-11"),
    ("italic", "em"): _c("matrix-italic-r5-italic", "slnt-0"),
    ("italic", "slnt"): _c("matrix-italic-r6-italic", "slnt-11"),
    ("italic", "normal"): _c("matrix-italic-r7-italic", "slnt-11"),
    # oblique (bare)
    ("oblique-bare", "italic"): _c("matrix-obliquebare-r1-oblique-bare", "slnt-11"),
    ("oblique-bare", "oblique"): _c("matrix-obliquebare-r2-oblique-bare", "slnt-11"),
    ("oblique-bare", "oblique-angle"): _c("matrix-obliquebare-r3-oblique-bare", "slnt-11"),
    ("oblique-bare", "oblique-synth-off"): _c("matrix-obliquebare-r4-oblique-bare", "slnt-11"),
    ("oblique-bare", "em"): _c("matrix-obliquebare-r5-oblique-bare", "slnt-11"),
    ("oblique-bare", "slnt"): _c("matrix-obliquebare-r6-oblique-bare", "slnt-11"),
    ("oblique-bare", "normal"): _c("matrix-obliquebare-r7-oblique-bare", "slnt-11"),
    # oblique <range> (rows 4 and 7 have no test on this font yet)
    ("oblique-range", "italic"): _c("explicit-range-bare-keyword-synthesis-stacking", "slnt-11",
                                    tags=[_SHARED]),
    ("oblique-range", "oblique"): _c("explicit-range-bare-keyword-synthesis-stacking", "slnt-11",
                                     tags=[_SHARED]),
    ("oblique-range", "oblique-angle"): _c("matrix-obliquerange-r3-oblique-range", "slnt-11"),
    ("oblique-range", "em"): _c("matrix-obliquerange-r5-oblique-range", "slnt-11"),
    ("oblique-range", "slnt"): _c("matrix-obliquerange-r6-oblique-range", "slnt-11"),
}

ENGINES = [
    {"id": "chromium", "result_key": "chrome", "label": "Chromium"},
    {"id": "firefox", "result_key": "firefox", "label": "Firefox"},
    {"id": "safari", "result_key": "safari", "label": "Safari"},
]

SPECIMEN_WORD = "OBLIQUE"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("'", '"'))


def _face_block(text: str) -> str:
    m = re.search(r"@font-face\s*\{(.*?)\}", text, re.S)
    return re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S) if m else ""


def verify_matrix(matrix_by_id: dict):
    """Fail loudly on any drift between this table and the tests on disk."""
    col_ids = {c["id"] for c in COLUMNS}
    row_ids = {r["id"] for r in ROWS}
    for (col, row) in CELLS:
        if col not in col_ids or row not in row_ids:
            raise RuntimeError(f"coverage_matrix: cell {(col, row)!r} uses an unknown column/row id")

    cols = {c["id"]: c for c in COLUMNS}
    rows = {r["id"]: r for r in ROWS}
    used_tests = set()
    for (col, row), cell in CELLS.items():
        tid = cell["test"]
        used_tests.add(tid)
        path = TESTS_DIR / f"{tid}.html"
        ref_path = TESTS_DIR / f"{tid}-ref.html"
        if not path.exists() or not ref_path.exists():
            raise RuntimeError(f"coverage_matrix: cell {(col, row)!r} names {tid!r}, but "
                               f"{path.name} / {ref_path.name} is missing from {TESTS_DIR}")
        if tid not in matrix_by_id:
            raise RuntimeError(f"coverage_matrix: {tid!r} has no row in results/browser-matrix.md "
                               f"— run and record it first")
        text = _norm(path.read_text())
        if FONT_SRC.name not in text:
            raise RuntimeError(f"coverage_matrix: {tid!r} does not use {FONT_SRC.name}")
        face = _norm(_face_block(path.read_text()))
        desc = cols[col]["css"]
        if desc is None:
            if "font-style" in face:
                raise RuntimeError(f"coverage_matrix: {tid!r} is in the auto column but its "
                                   f"@font-face declares a font-style")
        elif _norm(desc) not in face:
            raise RuntimeError(f"coverage_matrix: {tid!r} is in the {col!r} column but its "
                               f"@font-face does not contain {desc!r}")
        check = cell["check"] if cell["check"] is not None else rows[row]["check"]
        for token in check:
            if _norm(token) not in text:
                raise RuntimeError(f"coverage_matrix: {tid!r} is in row {row!r} but does not "
                                   f"contain {token!r}")

    # every matrix-*.html test on disk must appear in the grid, so a newly
    # generated test can't silently go unshown
    on_disk = {p.name[:-5] for p in TESTS_DIR.glob("matrix-*.html") if not p.name.endswith("-ref.html")}
    if on_disk - used_tests:
        raise RuntimeError(f"coverage_matrix: matrix-* test(s) on disk not placed in the grid: "
                           f"{sorted(on_disk - used_tests)}")


def sync_font(strict_check=True):
    """Copy the test font to site/public/ so the page's live specimens use
    the exact file the tests do. Copied, not symlinked (Vite/deploy copy)."""
    FONT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FONT_SRC, FONT_PUBLIC)
    a = hashlib.sha256(FONT_SRC.read_bytes()).hexdigest()
    b = hashlib.sha256(FONT_PUBLIC.read_bytes()).hexdigest()
    if strict_check and a != b:
        raise RuntimeError("coverage_matrix: site font copy differs from the test font")


def build_cell_results(matrix_by_id, status_fn):
    """{(col,row): {'chrome': status, 'firefox': ..., 'safari': ...}}"""
    out = {}
    for key, cell in CELLS.items():
        out[key] = {e["result_key"]: status_fn(cell["test"], matrix_by_id, e["result_key"])
                    for e in ENGINES}
    return out


def cell_status(results: dict) -> str:
    """Border colour: only engines that were actually run count, so a cell
    isn't marked uncertain just because Safari has no stable run yet."""
    vals = {v for v in results.values() if v in ("pass", "fail")}
    if "fail" in vals:
        return "fail"
    if vals == {"pass"}:
        return "pass"
    return "unknown"


def _summary(cell_results):
    covered = len(CELLS)
    total = len(COLUMNS) * len(ROWS)
    diverge = [k for k, r in cell_results.items()
               if r["chrome"] != r["firefox"] and {r["chrome"], r["firefox"]} <= {"pass", "fail"}]
    return covered, total, diverge, len({CELLS[k]["test"] for k in diverge})


def font_face_css() -> str:
    """One @font-face per column, all the same file: the live specimens."""
    out = []
    for c in COLUMNS:
        line = f"  font-style: {c['css'].split(': ', 1)[1]}" if c["css"] else ""
        out.append(f'@font-face {{ font-family: "ob-{c["id"]}"; src: url("/Cairo.var.subset.ttf");{line} }}')
    return "\n".join(out)


def _specimen(col, row, cell) -> str:
    e = html.escape
    css = cell["css"] if cell["css"] is not None else row["css"]
    is_em = row.get("em", False)
    family = f"font-family: 'ob-{col['id']}';"
    word = e(SPECIMEN_WORD)
    inner = f"<em>{word}</em>" if is_em else word
    test = f'<span class="ov-test" style="{e(family + " " + css)}">{inner}</span>'
    if cell["ref"] == "mismatch":
        return f'<div class="overlap overlap-single">{test}</div>'
    ref_style = family + " " + REF_CSS[cell["ref"]]
    ref = f'<span class="ov-control" style="{e(ref_style)}">{word}</span>'
    return f'<div class="overlap">{ref}{test}</div>'


def _badges(results: dict) -> str:
    e = html.escape
    lis = []
    for eng in ENGINES:
        status = results[eng["result_key"]]
        cls = {"pass": "pass", "fail": "fail"}.get(status, "unknown")
        word = {"pass": "pass", "fail": "fail"}.get(status, "not run")
        lis.append(
            f'<li class="b-badge {cls}" title="{e(eng["label"])}: {word}">'
            f'<img class="logo" src="/browsers/{eng["id"]}.svg" alt="{e(eng["label"])}"></li>'
        )
    return f'<ul class="verdicts">{"".join(lis)}</ul>'


def render_matrix_html(cell_results: dict, versions: dict) -> str:
    e = html.escape
    covered, total, diverge, diverge_tests = _summary(cell_results)
    parts = []

    div_txt = ""
    if diverge:
        div_txt = (f" &middot; <strong>{len(diverge)} cell{'s' if len(diverge) != 1 else ''} "
                   f"where Chrome and Firefox disagree</strong> ({diverge_tests} distinct "
                   f"test{'s' if diverge_tests != 1 else ''})")
    parts.append(f'<p class="matrix-count">{covered} of {total} cells have a test{div_txt}</p>')

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
        parts.append(f'<th><code>{e(c["code"])}</code><span class="col-note">{e(c["note"])}</span></th>')
    parts.append("</tr></thead><tbody>")

    for row in ROWS:
        lines = "<br>".join(e(l) for l in row["lines"])
        parts.append(f'<tr><th scope="row"><span class="row-num">{row["num"]}.</span> <code>{lines}</code></th>')
        for col in COLUMNS:
            key = (col["id"], row["id"])
            cell = CELLS.get(key)
            if cell is None:
                parts.append('<td class="status-blank"><span class="blank-cell">&mdash;</span>'
                             '<span class="cell-tags">no test yet</span></td>')
                continue
            res = cell_results[key]
            url = TEST_URL_BASE + cell["test"] + ".html"
            tags = "".join(f'<span class="tag">{e(t)}</span>' for t in cell["tags"])
            if cell["ref"] == "mismatch":
                tags += '<span class="tag">must differ from upright</span>'
            parts.append(
                f'<td class="status-{cell_status(res)}">'
                f'<a class="specimen-link" href="{e(url)}" title="{e(cell["test"])}">'
                f'{_specimen(col, row, cell)}</a>'
                f'{_badges(res)}'
                f'<div class="cell-tags">{tags}</div></td>'
            )
        parts.append("</tr>")
    parts.append("</tbody></table></div>")

    parts.append(
        '<ul class="legend">'
        '<li><span class="b-badge pass"></span> pass</li>'
        '<li><span class="b-badge fail"></span> fail</li>'
        '<li><span class="b-badge unknown"></span> not run</li>'
        '<li class="legend-note">Hover a circle for the engine. Click a specimen for its test file.</li>'
        "</ul>"
    )
    ver = []
    for eng in ENGINES:
        v = versions.get(eng["result_key"])
        ver.append(f'<li><img class="logo" src="/browsers/{eng["id"]}.svg" alt="">'
                   f'{e(eng["label"])} {e(v) if v else "&mdash; not run"}</li>')
    parts.append(f'<ul class="legend legend-versions">{"".join(ver)}</ul>')
    return "".join(parts)
