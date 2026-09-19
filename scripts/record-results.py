"""Parse a `wpt run --log-wptreport=<path>.json` report and append rows to
results/browser-matrix.md in the fixed schema already defined there
(test_id | engine | version | real_device | result | notes). Never
hand-transcribe results into that file — this is the only writer.

Usage (from repo root):
  uv run scripts/record-results.py results/latest-chrome.json
  uv run scripts/record-results.py results/latest-firefox.json --real-device
  uv run scripts/record-results.py results/latest-safari.json --real-device --notes "iPhone XR, Safari 18.7"

--real-device marks rows as real_device=yes (e.g. an actual Safari run on a
physical device, matching vizchitra-fonts/docs/compat.md's convention).
Omit it for `wpt run`'s own automated browser instances (chrome/firefox
launched by the runner itself): those are "no", they are real browser
binaries driven by automation, not a hands-on physical-device check.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = REPO_ROOT / "results" / "browser-matrix.md"

WPT_STATUS_TO_SCHEMA = {
    "OK": "pass",
    "PASS": "pass",
    "FAIL": "fail",
    "ERROR": "fail",
    "TIMEOUT": "fail",
    "CRASH": "fail",
    "PRECONDITION_FAILED": "untested",
    "NOTRUN": "untested",
}


def test_id_from_path(test_path: str) -> str:
    # wptreport test paths are the WPT-tree-relative URL path, e.g.
    # "/css/css-fonts/variable-oblique-interop/slnt-axis-activation.html".
    return Path(test_path).stem


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="wptreport JSON file")
    parser.add_argument("--real-device", action="store_true",
                         help="mark rows as real_device=yes (see module docstring)")
    parser.add_argument("--notes", default="", help="free-text notes column")
    args = parser.parse_args()

    with args.report.open() as f:
        report = json.load(f)

    run_info = report.get("run_info", {})
    engine = run_info.get("product", "unknown")
    version = run_info.get("browser_version", run_info.get("version", "unknown"))
    real_device = "yes" if args.real_device else "no"

    rows = []
    for result in report.get("results", []):
        status = result.get("status", "NOTRUN")
        schema_result = WPT_STATUS_TO_SCHEMA.get(status, "untested")
        test_id = test_id_from_path(result["test"])
        note = args.notes or f"wpt status: {status}"
        rows.append(f"| {test_id} | {engine} | {version} | {real_device} | {schema_result} | {note} |")

    if not rows:
        print("record-results: no results found in report, nothing appended", file=sys.stderr)
        return

    # Insert directly after the table's header-separator line (the line of
    # dashes right below the column headers), not at EOF — the schema notes
    # and enum captions live below the table, and a blind append would land
    # rows after them, breaking the table.
    lines = MATRIX_PATH.read_text().splitlines()
    sep_index = next(
        i for i, line in enumerate(lines) if line.startswith("|---")
    )
    # Existing data rows (if any) are contiguous lines starting with "|"
    # right after the separator; insert new rows after the last of those.
    insert_at = sep_index + 1
    while insert_at < len(lines) and lines[insert_at].startswith("|"):
        insert_at += 1
    lines[insert_at:insert_at] = rows
    MATRIX_PATH.write_text("\n".join(lines) + "\n")

    print(f"record-results: appended {len(rows)} row(s) to {MATRIX_PATH}")


if __name__ == "__main__":
    main()
