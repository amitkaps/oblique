#!/usr/bin/env bash
# Run the tests in the vendored WPT checkout in a locally installed Chrome or Firefox and
# record the results in results/browser-matrix.md.  Usage: scripts/wpt-run.sh chrome|firefox
#
# Safari is not run through wpt (it is unreliable there, see docs/running.md): use
# scripts/safari-replay.py.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
engine="${1:?usage: wpt-run.sh chrome|firefox}"

./scripts/sync-tests-to-wpt.sh

# wpt's first run builds a venv and cannot build the newest `cryptography` from source here;
# capping it keeps pip on a version with a wheel.
constraints="$(mktemp)"
echo "cryptography<=48.0.1" > "$constraints"
export PIP_CONSTRAINT="$constraints"

report="../results/latest-$engine.json"
folder=css/css-fonts/matching/font-style/
cd .wpt
rm -f "$report"
# wpt exits nonzero when any test fails, and failures are the data here: record whatever it
# reported. Only a run that produced no report is an error.
set +e
case "$engine" in
  chrome)
    ./wpt run chrome "$folder" \
      --binary="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --webdriver-binary=_venv3/bin/chrome/chromedriver --log-wptreport="$report" ;;
  firefox)
    # --yes: without it the first run waits on an interactive OpenH264 prompt forever
    ./wpt run --yes firefox "$folder" \
      --binary=/Applications/Firefox.app/Contents/MacOS/firefox \
      --webdriver-binary=_venv3/bin/geckodriver --log-wptreport="$report" ;;
  *) echo "unknown engine: $engine" >&2; exit 2 ;;
esac
wpt_status=$?
set -e
cd ..
if [ ! -s "results/latest-$engine.json" ]; then
  echo "wpt run produced no report (exit $wpt_status); nothing recorded" >&2
  exit 1
fi
uv run scripts/record-results.py "results/latest-$engine.json"
