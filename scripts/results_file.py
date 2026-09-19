"""The one writer of results/browser-matrix.md: the CURRENT result per (test, engine).

Recording replaces the row for the same test and engine, and drops rows for tests that no
longer exist in tests/oblique-style-matching/. History is git's job, not this file's.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests" / "oblique-style-matching"
MATRIX_PATH = REPO_ROOT / "results" / "browser-matrix.md"

HEADER = """# Browser results

One row per (test, engine): the current result of this repo's own runs. Rows are written by
`scripts/record-results.py` (Chrome and Firefox, from `wpt run`) and `scripts/safari-replay.py --record`
(Safari), never by hand. Recording a test again replaces its row, and rows for tests that no longer exist
are dropped; git keeps the history. See `docs/running.md`.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
"""

FOOTER = """
`result` ∈ `pass` / `fail` / `untested`.
`real_device` ∈ `yes` / `no`.
"""


def _read():
    rows = {}
    if MATRIX_PATH.exists():
        for line in MATRIX_PATH.read_text().splitlines():
            if not line.startswith("|") or line.startswith("|---") or "test_id" in line:
                continue
            c = [x.strip() for x in line.split("|")[1:-1]]
            if len(c) >= 6:
                rows[(c[0], c[1])] = c[:6]
    return rows


def record(new_rows):
    """new_rows: [(test_id, engine, version, real_device, result, notes)]"""
    rows = _read()
    for r in new_rows:
        rows[(r[0], r[1])] = list(r)
    live = [rows[k] for k in sorted(rows) if (TESTS_DIR / f"{k[0]}.html").exists()]
    body = "\n".join("| " + " | ".join(v) + " |" for v in live)
    MATRIX_PATH.write_text(HEADER + body + "\n" + FOOTER)
    return len(live)
