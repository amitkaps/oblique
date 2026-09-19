"""Measure how each browser actually renders every cell of the generated matrix.

For each cell in tests/oblique-style-matching/matrix/matrix.manifest.json this builds a probe
page (the same @font-face descriptor and use-site CSS as the generated test), loads it
in a real browser through WebDriver, screenshots it, and measures the LEAN of the
capital I: how far the top of the stem is displaced from its bottom, in pixels.

The lean is judged by reference/src/compare.mjs against the lean each outcome the
reference algorithm ALLOWS predicts. That gives a verdict for every cell, including the
`unspecified` ones that have no WPT test, and cross-checks the reftest results.

  upright        0 px          real slnt -11   ~16 px
  synthetic 14deg ~21 px       stacked (axis + synthetic) ~36 px

Usage (from repo root):
  uv run scripts/survey.py                          # chrome, firefox, safari
  uv run scripts/survey.py --engines chrome,firefox
Writes results/survey.json. Safari needs Remote Automation enabled (docs/running.md).
"""
import argparse
import base64
import io
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests" / "oblique-style-matching"
MANIFEST = TESTS_DIR / "matrix" / "matrix.manifest.json"
OUT = REPO_ROOT / "results" / "survey.json"
DRIVERS = REPO_ROOT / ".wpt" / "_venv3" / "bin"
HTTP_PORT = 18932
CROP_TOP = 8  # Safari's screenshots carry a dark line at the very top


def wd(port, method, path, body=None, timeout=120):
    r = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(r, timeout=timeout))["value"]


ENGINES = {
    "chrome": (
        [str(DRIVERS / "chrome" / "chromedriver"), "--port={port}"],
        {"browserName": "chrome", "goog:chromeOptions": {
            "args": ["--headless=new", "--hide-scrollbars", "--window-size=800,400"],
            "binary": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}},
    ),
    "firefox": (
        [str(DRIVERS / "geckodriver"), "--port", "{port}"],
        {"browserName": "firefox", "moz:firefoxOptions": {
            "args": ["-headless"], "binary": "/Applications/Firefox.app/Contents/MacOS/firefox"}},
    ),
    "safari": (["/usr/bin/safaridriver", "-p", "{port}"], {"browserName": "safari"}),
}
PORTS = {"chrome": 4461, "firefox": 4462, "safari": 4463}


def probe_html(manifest, cell):
    font = manifest["font"]
    desc = f"\n    font-style: {cell['descriptor']};" if cell["descriptor"] else ""
    row = next(r for r in manifest["rows"] if r["slug"] == cell["row"])
    style = f' style="{cell["css"]}"' if cell["css"] else ""
    inner = f"<em>{font['glyph']}</em>" if row.get("em") else font["glyph"]
    return f"""<!DOCTYPE html><html class="reftest-wait"><meta charset="utf-8">
<link rel="stylesheet" href="../oblique-matching.css">
<style>@font-face {{ font-family: "probe"; src: url('{font['file']}');{desc} }}
.test {{ font-family: "probe"; font-size: {font['fontSize']}; }}</style>
<script>document.fonts.ready.then(() => document.documentElement.classList.remove('reftest-wait'));</script>
<p class="test"{style}>{inner}</p>"""


def lean_of(png):
    img = Image.open(io.BytesIO(png)).convert("L")
    w, h = img.size
    img = img.crop((0, CROP_TOP, w, h))
    w, h = img.size
    px = img.load()
    rows = [y for y in range(h) if any(px[x, y] < 128 for x in range(w))]
    if not rows:
        return None
    top, bottom = min(rows) + 3, max(rows) - 3

    def left(y):
        return min(x for x in range(w) if px[x, y] < 128)

    return left(top) - left(bottom)


def survey_engine(engine, manifest, base_url, reps):
    cmd, caps = ENGINES[engine]
    port = PORTS[engine]
    driver = subprocess.Popen([c.format(port=port) for c in cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    try:
        session = wd(port, "POST", "/session", {"capabilities": {"alwaysMatch": caps}})
        sid, version = session["sessionId"], session["capabilities"].get("browserVersion", "?")
        cells = {}
        for cell in manifest["cells"]:
            leans = []
            for _ in range(reps):
                wd(port, "POST", f"/session/{sid}/url", {"url": f"{base_url}/matrix/probe-{cell['id']}.html"})
                deadline = time.time() + 10
                while time.time() < deadline:
                    waiting = wd(port, "POST", f"/session/{sid}/execute/sync", {
                        "script": "return document.documentElement.classList.contains('reftest-wait')", "args": []})
                    if not waiting:
                        break
                    time.sleep(0.05)
                leans.append(lean_of(base64.b64decode(wd(port, "GET", f"/session/{sid}/screenshot"))))
            if len(set(leans)) != 1:
                print(f"  {engine} {cell['address']}: unstable {leans}, not recorded", file=sys.stderr)
                continue
            cells[cell["id"]] = leans[0]
        wd(port, "DELETE", f"/session/{sid}")
        return {"version": version, "cells": cells}
    finally:
        driver.terminate()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engines", default="chrome,firefox,safari")
    ap.add_argument("--reps", type=int, default=2, help="repeat each cell; unstable cells are dropped")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    tmp = Path(tempfile.mkdtemp(prefix="survey-"))
    # same layout as tests/oblique-style-matching/: probes in matrix/, font in resources/
    (tmp / "matrix").mkdir()
    (tmp / "resources").mkdir()
    shutil.copy(TESTS_DIR / "resources" / Path(manifest["font"]["file"]).name, tmp / "resources")
    shutil.copy(TESTS_DIR / "oblique-matching.css", tmp / "oblique-matching.css")
    for cell in manifest["cells"]:
        (tmp / "matrix" / f"probe-{cell['id']}.html").write_text(probe_html(manifest, cell))

    http = subprocess.Popen([sys.executable, "-m", "http.server", str(HTTP_PORT), "--directory", str(tmp)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    result = {"_note": "Generated by scripts/survey.py: measured lean (px) per generated cell.", "engines": {}}
    try:
        for engine in args.engines.split(","):
            print(f"surveying {engine} ...")
            result["engines"][engine] = survey_engine(engine, manifest, f"http://localhost:{HTTP_PORT}", args.reps)
    finally:
        http.terminate()
        shutil.rmtree(tmp, ignore_errors=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
