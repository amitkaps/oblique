"""Sync live upstream WPT results from wpt.fyi's public API for every test
catalogued in docs/coverage.json, and write them to results/upstream.json.

This is the only writer of results/upstream.json, and results/upstream.json
is the only source docs/upstream-matrix.md is rendered from (via
scripts/render-upstream-matrix.py) — never hand-transcribe a wpt.fyi result
into any markdown file, same discipline as scripts/record-results.py for
this repo's own locally-run tests.

This is deliberately kept separate from results/browser-matrix.md: that file
is "we ran this ourselves" (via the local WPT runner, scripts/record-results.py),
this one is "wpt.fyi ran this continuously upstream" (via wpt.fyi's own CI).
Merging the two tables would misrepresent provenance.

wpt.fyi API used (read the endpoint's own behavior, not a cached assumption):
  GET /api/runs?label=stable&max-count=1&product=<chrome|firefox|safari>
    -> latest stable run per browser (run id, browser_version, created_at)
  GET /api/search?run_ids=<id,id,id>&q=<test filename>
    -> per-test single-letter legacy status per run, in `results[].legacy_status`

The legacy single-letter status codes map onto wpt.fyi's shared/statuses.go
TestStatus enum (P=Pass, O=Ok, E=Error, T=Timeout, N=NotRun, F=Fail, C=Crash,
S=Skip, A=Assert); unrecognized codes are passed through rather than dropped,
per the "fail loudly, don't swallow" rule below.

A failed or incomplete sync exits non-zero and prints why — this script never
writes a partial or stale results/upstream.json over a good one.

Usage (from repo root):
  uv run scripts/sync-wpt-results.py
"""

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COVERAGE_PATH = REPO_ROOT / "docs" / "coverage.json"
OUTPUT_PATH = REPO_ROOT / "results" / "upstream.json"

WPT_FYI_API = "https://wpt.fyi/api"
PRODUCTS = ["chrome", "firefox", "safari"]

STATUS_CODE_MEANING = {
    "P": "PASS",
    "O": "OK",
    "E": "ERROR",
    "T": "TIMEOUT",
    "N": "NOTRUN",
    "F": "FAIL",
    "C": "CRASH",
    "S": "SKIP",
    "A": "ASSERT",
}


def fetch_json(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status} from {url}")
            return json.loads(resp.read())
    except urllib.error.URLError as e:
        raise RuntimeError(f"request to {url} failed: {e}") from e


def latest_stable_runs() -> dict:
    """One latest-stable run per product, keyed by product name."""
    runs = {}
    for product in PRODUCTS:
        url = f"{WPT_FYI_API}/runs?label=stable&max-count=1&product={product}"
        data = fetch_json(url)
        if not data:
            raise RuntimeError(
                f"wpt.fyi returned zero stable runs for product={product} — "
                "cannot sync without a baseline run for every product"
            )
        runs[product] = data[0]
    return runs


def query_results(run_ids: list, test_filename: str) -> list:
    """legacy_status list for the single result row matching test_filename,
    in the same order as run_ids. wpt.fyi's `q=` matches by substring against
    the test path, so a distinctive filename (not a bare directory) is
    required to get exactly one row back.
    """
    ids = ",".join(str(i) for i in run_ids)
    url = f"{WPT_FYI_API}/search?run_ids={ids}&q={test_filename}"
    data = fetch_json(url)
    for row in data.get("results", []):
        if row["test"].endswith("/" + test_filename):
            return row["legacy_status"]
    return None


def main():
    coverage = json.loads(COVERAGE_PATH.read_text())
    tests = coverage["tests"]

    print(f"sync-wpt-results: resolving latest stable runs for {PRODUCTS}...")
    runs = latest_stable_runs()
    run_ids = [runs[p]["id"] for p in PRODUCTS]
    for p in PRODUCTS:
        print(f"  {p}: {runs[p]['browser_version']} (run {runs[p]['id']}, "
              f"created {runs[p]['created_at']})")

    synced = []
    errors = []
    for test in tests:
        filename = test["path"].rsplit("/", 1)[-1]
        try:
            legacy_status = query_results(run_ids, filename)
        except RuntimeError as e:
            errors.append(f"{test['path']}: {e}")
            continue

        if legacy_status is None:
            errors.append(f"{test['path']}: no matching row in wpt.fyi search response")
            continue

        per_product = {}
        for product, status_entry in zip(PRODUCTS, legacy_status):
            code = status_entry.get("status", "")
            per_product[product] = {
                "status": STATUS_CODE_MEANING.get(code, f"UNKNOWN({code})"),
                "browser_version": runs[product]["browser_version"],
            }
        synced.append({"path": test["path"], "results": per_product})

    if errors:
        print("sync-wpt-results: FAILED — errors querying wpt.fyi:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(
            f"sync-wpt-results: {len(errors)}/{len(tests)} test(s) failed to sync; "
            f"not writing {OUTPUT_PATH} (refusing to publish partial/stale data as current)",
            file=sys.stderr,
        )
        sys.exit(1)

    output = {
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "run_metadata": {
            p: {"id": runs[p]["id"], "browser_version": runs[p]["browser_version"],
                "created_at": runs[p]["created_at"]}
            for p in PRODUCTS
        },
        "tests": synced,
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")
    print(f"sync-wpt-results: wrote {len(synced)} test result(s) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
