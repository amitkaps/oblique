"""Replay this folder's reftests in real Safari through safaridriver, directly.

Why this exists: `./wpt run safari` was measured to disagree with the actual
rendering (docs/running.md): ~20 of 44 tests reported FAIL
although a direct screenshot of the test and its reference is pixel-identical,
and it PASSED a test that really fails; 5 more flipped between two identical
runs. This script does what a reftest runner does, without wptrunner in the
way: load the test, wait for the `reftest-wait` class to clear, screenshot,
load each reference the same way, compare pixels exactly.

  rel="match"     passes only if the two screenshots are identical
  rel="mismatch"  passes only if they differ (all mismatch refs must differ)

Each test is replayed --reps times (default 3); a result is only reported if
every repetition agrees, otherwise it is marked flaky and never recorded.

Prerequisites: Safari > Develop > Allow Remote Automation ticked (or
`sudo safaridriver --enable`), and Safari fully quit before the first run if
sessions time out.

Usage (from repo root):
  uv run scripts/safari-replay.py            # print a table
  uv run scripts/safari-replay.py --record   # also append rows
                                                             # to results/browser-matrix.md
"""
import argparse
import base64
import io
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests" / "oblique-style-matching"
MATRIX_PATH = REPO_ROOT / "results" / "browser-matrix.md"
DRIVER_PORT = 4449
HTTP_PORT = 18931
CROP_TOP = 8  # Safari's screenshots carry a thin dark line at the very top


def wd(method, path, body=None, timeout=120):
    r = urllib.request.Request(
        f"http://127.0.0.1:{DRIVER_PORT}{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(r, timeout=timeout))["value"]


def screenshot(session, page):
    wd("POST", f"/session/{session}/url", {"url": f"http://localhost:{HTTP_PORT}/{page}"})
    deadline = time.time() + 10
    while time.time() < deadline:
        waiting = wd("POST", f"/session/{session}/execute/sync", {
            "script": "return document.documentElement.classList.contains('reftest-wait')",
            "args": [],
        })
        if not waiting:
            break
        time.sleep(0.05)
    png = base64.b64decode(wd("GET", f"/session/{session}/screenshot"))
    img = Image.open(io.BytesIO(png)).convert("RGB")
    w, h = img.size
    return img.crop((0, CROP_TOP, w, h))


def differs(a, b):
    return ImageChops.difference(a, b).getbbox() is not None


def test_pages():
    """(test id, page path relative to TESTS_DIR, [(rel, ref path relative to TESTS_DIR)])"""
    pages = []
    for folder in ("matrix", "standalone"):
        for path in sorted((TESTS_DIR / folder).glob("*.html")):
            if "-ref" in path.stem or "notupright" in path.stem or "notaxis" in path.stem:
                continue
            links = re.findall(r'<link rel="(match|mismatch)" href="([^"]+)"', path.read_text())
            if links:
                pages.append((path.stem, f"{folder}/{path.name}", [(rel, f"{folder}/{href}") for rel, href in links]))
    return pages


def replay_once(session, pages):
    results = {}
    for test_id, name, links in pages:
        test_img = screenshot(session, name)
        ok = True
        for rel, href in links:
            ref_img = screenshot(session, href)
            if (rel == "match") == differs(test_img, ref_img):
                ok = False
        results[test_id] = "pass" if ok else "fail"
    return results


def record(rows):
    lines = MATRIX_PATH.read_text().splitlines()
    sep = next(i for i, l in enumerate(lines) if l.startswith("|---"))
    at = sep + 1
    while at < len(lines) and lines[at].startswith("|"):
        at += 1
    lines[at:at] = rows
    MATRIX_PATH.write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--record", action="store_true", help="append stable results to results/browser-matrix.md")
    ap.add_argument("--prefix", default="", help="only replay tests whose id starts with this (e.g. matrix-)")
    ap.add_argument("--tests", default="", help="only replay these test ids (comma separated)")
    args = ap.parse_args()

    only = {t for t in args.tests.split(",") if t}
    pages = [p for p in test_pages() if p[0].startswith(args.prefix) and (not only or p[0] in only)]
    http = subprocess.Popen([sys.executable, "-m", "http.server", str(HTTP_PORT), "--directory", str(TESTS_DIR)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    driver = subprocess.Popen(["/usr/bin/safaridriver", "-p", str(DRIVER_PORT)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    runs = []
    try:
        caps = wd("POST", "/session", {"capabilities": {"alwaysMatch": {"browserName": "safari"}}})
        session, version = caps["sessionId"], caps["capabilities"]["browserVersion"]
        for _ in range(args.reps):
            runs.append(replay_once(session, pages))
        wd("DELETE", f"/session/{session}")
    finally:
        driver.terminate()
        http.terminate()

    stable, flaky = {}, []
    for test_id, _name, _links in pages:
        vals = {r[test_id] for r in runs}
        if len(vals) == 1:
            stable[test_id] = vals.pop()
        else:
            flaky.append(test_id)
    for test_id, res in stable.items():
        print(f"{res.upper():5} {test_id}")
    for test_id in flaky:
        print(f"FLAKY {test_id}")
    print(f"\nSafari {version}: {sum(v == 'pass' for v in stable.values())} pass, "
          f"{sum(v == 'fail' for v in stable.values())} fail, {len(flaky)} flaky "
          f"({args.reps} identical-condition repetitions)")

    if args.record:
        note = ("direct safaridriver replay of the reftest, exact pixel compare, "
                f"{args.reps} agreeing repetitions; `wpt run safari` disagreed, see "
                "docs/running.md")
        rows = [f"| {t} | safari | {version} | no (safaridriver automation) | {res} | {note} |"
                for t, res in stable.items()]
        record(rows)
        print(f"recorded {len(rows)} row(s) in {MATRIX_PATH}")


if __name__ == "__main__":
    main()
