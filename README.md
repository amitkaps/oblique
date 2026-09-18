# Oblique

Variable font oblique interop — font- and vendor-neutral tracking of CSS
Fonts 4 `slnt`/`ital` axis matching interoperability, feeding a future
[web-platform-tests/interop](https://github.com/web-platform-tests/interop)
proposal. The VizChitra/Cairo font compatibility investigation
([fonts.vizchitra.com/compat](https://fonts.vizchitra.com/compat),
[github.com/vizchitra/fonts](https://github.com/vizchitra/fonts)) is the
motivating case, not the subject.

This repo does two things:

1. **Catalogs and continuously tracks existing WPT coverage** of
   oblique/`slnt`/`ital` matching — [`docs/coverage.md`](docs/coverage.md)
   lists every relevant upstream test, and
   [`results/upstream-matrix.md`](results/upstream-matrix.md) has their live
   per-engine pass/fail, synced from [wpt.fyi](https://wpt.fyi) on a
   schedule (see "Live coverage dashboard" below). Turns out WPT already
   covers `slnt` fairly well; it covers `ital` **not at all**.
2. **Supplies the tests upstream WPT is missing** for that confirmed
   `ital`-axis gap — a small set of novel tests under `tests/ital-axis/`,
   staged for upstreaming, following the same worked-example methodology as
   the rest of this repo.

Full build spec: [`docs/spec.md`](docs/spec.md). Execution plan:
[`docs/plan.md`](docs/plan.md). Current state, short version:
[`docs/summary.md`](docs/summary.md). Full investigation trail (every claim
sourced, every wrong turn documented): [`docs/investigation-log.md`](docs/investigation-log.md).
Coverage catalog: [`docs/coverage.md`](docs/coverage.md).

## Non-goals

- Not a general compatibility framework.
- Not a permanent home for tests — everything here is staged to graduate
  into WPT.
- No opinions on whether a feature *should* exist — only whether behavior
  is interoperable per spec.

## Prior art

- Interop proposal: https://github.com/web-platform-tests/interop/issues/64
  (2022, closed without acceptance — lacked WPT test coverage; this repo
  supplies it)
- WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=209565
- Chromium bug: https://issues.chromium.org/issues/40681464
- Spec ambiguity, now resolved: https://github.com/w3c/csswg-drafts/issues/12836
- Original spec ambiguity (superseded by #12836): https://github.com/w3c/csswg-drafts/issues/3125
- Community test suite: https://arrowtype.github.io/vf-slnt-test/ (reference
  behavior, not upstreamable itself)

Current verified status of each of the above is in
[`docs/investigation-log.md`](docs/investigation-log.md) — do not treat this
list's parenthetical notes as current; re-check the log, which is dated.

## Methodology

1. Identify one CSS Fonts 4 normative requirement (cite spec section +
   prior-art issue).
2. Write one focused, WPT-compatible test (reftest or testharness) for it.
3. Run via the official WPT runner (not custom Playwright/vitest).
4. Record result in `results/browser-matrix.md` using the fixed schema.
5. Once stable and reviewed, upstream the test file(s) to WPT via PR.
6. Aggregate upstreamed + accepted tests into an Interop proposal draft in
   `docs/investigation-log.md`.

## Running the tests

A minimal, scoped WPT checkout can be vendored locally (fetched
infrastructure, gitignored, never committed — see
[`scripts/setup-wpt.sh`](scripts/setup-wpt.sh)):

```
./scripts/setup-wpt.sh
mkdir -p .wpt/css/css-fonts/variable-oblique-interop/font-style-oblique
cp -r tests/font-style-oblique/*.html tests/font-style-oblique/resources \
  .wpt/css/css-fonts/variable-oblique-interop/font-style-oblique/
mkdir -p .wpt/css/css-fonts/variable-oblique-interop/ital-axis
cp -r tests/ital-axis/*.html tests/ital-axis/resources \
  .wpt/css/css-fonts/variable-oblique-interop/ital-axis/
cd .wpt
./wpt install chrome webdriver --channel stable
./wpt install firefox webdriver
./wpt run chrome css/css-fonts/variable-oblique-interop/ --log-wptreport=../results/latest-chrome.json
./wpt run firefox css/css-fonts/variable-oblique-interop/ --log-wptreport=../results/latest-firefox.json
```

Both `resources/` subdirectories (each test's font files) must be copied
alongside their `*.html`, not just the HTML — each test's `@font-face src`
is a relative `url('resources/...')`, so the test breaks silently without
its font. Don't pass `--install-fonts` unless a test specifically needs a
system-installed font (ours don't — they use embedded `@font-face` web
fonts): on macOS it can stall indefinitely waiting on a permission
interaction that never resolves in a non-interactive shell.

If you already have Chrome or Firefox installed system-wide, point at it
directly instead of `./wpt install <product> browser` (which downloads a
separate copy):

```
./wpt run chrome css/css-fonts/variable-oblique-interop/ \
  --binary="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --webdriver-binary=_venv3/bin/chrome/chromedriver \
  --log-wptreport=../results/latest-chrome.json

./wpt run --yes firefox css/css-fonts/variable-oblique-interop/ \
  --binary="/Applications/Firefox.app/Contents/MacOS/firefox" \
  --webdriver-binary=_venv3/bin/geckodriver \
  --log-wptreport=../results/latest-firefox.json
```

`--yes` is needed on Firefox's first run — without it, `wpt run` prompts
interactively to install the OpenH264 GMP plugin (irrelevant to these
tests) and hangs forever in a non-interactive shell.

**Known issue on some machines:** `./wpt run`'s first invocation bootstraps
its own Python venv and can fail building the `cryptography` package from
source (`error: failed to run custom build command for openssl-sys`) on
machines with no Rust/OpenSSL dev toolchain — reproduced on an Intel Mac in
this environment (no Homebrew available either). Pre-installing a
wheel-backed `cryptography` version into `.wpt/_venv3` does **not** help —
wpt's own installer force-upgrades past it regardless. What does work,
confirmed in this environment: cap the version with a `PIP_CONSTRAINT` file
before running, so pip's resolver never reaches for the unwheeled release:

```
echo "cryptography<=48.0.1" > /tmp/wpt-constraints.txt
PIP_CONSTRAINT=/tmp/wpt-constraints.txt ./wpt run chrome ...
```

(`cryptography` does publish prebuilt wheels — confirmed a `cp311-abi3`
universal2 wheel, forward-compatible with newer CPython via the stable ABI,
exists as of `48.0.1` — the underlying cause is that whatever *newer*
version wpt's dependency chain resolves to at install time has no wheel yet
for this platform, forcing a source build that then fails for lack of
Rust/OpenSSL.) Installing an older Python via `mise` does not help either —
abi3 wheels are forward-compatible across CPython versions, so the version
lacking a wheel lacks it regardless of which CPython minor version runs it.

Safari (macOS only, requires two one-time setup steps beyond Chrome/
Firefox — `wpt run` exempts chrome/firefox from the second one, but not
safari):

1. Enable Develop → "Allow Remote Automation" in Safari (or
   `sudo /usr/bin/safaridriver --enable`, which needs an interactive
   password prompt).
2. Add WPT's test subdomains to `/etc/hosts` (this is a real, if low-risk,
   edit to a shared system file — dozens of `127.0.0.1 *.test` aliases,
   nothing that touches real DNS or existing entries):
   ```
   cd .wpt
   ./wpt make-hosts-file | sudo tee -a /etc/hosts
   ```

```
./wpt run safari css/css-fonts/variable-oblique-interop/ \
  --webdriver-binary=/usr/bin/safaridriver \
  --log-wptreport=../results/latest-safari.json
```

**Before trusting a Safari result, read `docs/investigation-log.md`'s "Safari —
attempted, no reliable result" section.** In this environment, `wpt run`
reported all three tests FAIL identically across four runs. This is *not*
a font-validity problem (an early theory blaming `fontTools`-generated
fonts was investigated and disproved) — isolating WPT's own pristine
official test font alone, with no custom font of ours involved, still
FAILs under `wpt run safari`. Three identical trials driving `safaridriver`
directly (same page, same fresh-session setup, same wait) produced two
different outcomes. This is genuine nondeterminism in Safari/WebKit's
font-loading-to-compositor pipeline under WebDriver automation, not
something fixable from this repo. Don't trust a single `wpt run safari`
result in either direction; a real physical device running Safari's actual
UI (not `safaridriver`) is the trustworthy path, per
vizchitra-fonts/docs/compat.md's own reason for keeping a manual `/compat`
page.

Then record results into `results/browser-matrix.md` — never hand-transcribe:

```
uv run scripts/record-results.py results/latest-chrome.json
uv run scripts/record-results.py results/latest-firefox.json
```

`--real-device` is for a genuine physical-device run (e.g. `--webdriver-binary`
pointed at a real iPhone's Safari, matching vizchitra-fonts/docs/compat.md's
convention) — e.g. `--real-device --notes "iPhone XR, Safari 18.7"`. Desktop
Safari via `safaridriver` is not a real device; see the caveat above before
recording anything from it at all.

## Live coverage dashboard

[`docs/coverage.json`](docs/coverage.json) catalogs every existing upstream
WPT test relevant to oblique/`slnt`/`ital` (path, spec assertion, which axis
it touches, whether it plausibly probes WebKit #209565's documented failure
modes), built by walking the vendored `css/css-fonts` tree directly — not
sampled from search results. It also records the confirmed absence of any
`ital`-axis test anywhere upstream, with the search method used.

`scripts/sync-wpt-results.py` queries [wpt.fyi's public API](https://wpt.fyi/api)
for the latest-stable Chrome/Firefox/Safari run and writes structured,
per-test results to `results/upstream.json` — this is the **only** path
results enter the repo for upstream tests; nothing here is hand-transcribed.
It fails loudly (non-zero exit) on any API error rather than publish
partial or stale data as current.

`scripts/render-coverage-docs.py` renders `docs/coverage.md` and
`results/upstream-matrix.md` from that JSON (and copies both JSON files into
`docs/data/` for anyone browsing the raw data directly).

`scripts/generate-site-data.py` then renders the small, curated dataset the
public site actually needs (`site/src/data/cards.json` — a handful of cards,
plain-language descriptions, capped "why it matters" lines, not a
pass-through of the verbose sources above) and bakes it directly into
`site/index.html` from `site/template.html`. The site
([`site/`](site/), a static Vite project) has no client-side interactivity,
so there's no JS rendering step — the page ships as plain static HTML plus
one bundled stylesheet, built with `pnpm run build`. It's organized into two
visually distinct sections: tests already covered by upstream WPT, and new
tests this project wrote to fill confirmed gaps — never merged into one
table, so a visitor can tell at a glance which is which. It reads only
committed JSON snapshots at build time (never calls wpt.fyi live from the
browser), so staleness is visible via a prominent last-synced timestamp
rather than silently assumed current.

The site is published via GitHub Pages, serving the `docs/` folder (the
built `site/dist/` output is copied there), at
**https://oblique.amitkaps.com** (`docs/CNAME`; requires a DNS `CNAME`
record for that hostname pointing at `amitkaps.github.io`, set up outside
this repo).

A scheduled GitHub Actions workflow
([`.github/workflows/sync-wpt-results.yml`](.github/workflows/sync-wpt-results.yml))
re-runs the full pipeline daily and commits the refreshed data + rebuilt
site. To run it manually:

```
uv run scripts/sync-wpt-results.py
uv run scripts/render-coverage-docs.py
uv run scripts/generate-site-data.py
cd site && pnpm install && pnpm run build && cd ..
rm -rf docs/assets && cp -r site/dist/* docs/
```

`site/`'s toolchain (`node`, `pnpm`) is pinned in `.mise.toml`, the same way
the Python toolchain (`python`, `uv`) already is.

`results/upstream-matrix.md` (wpt.fyi-sourced, continuous, for pre-existing
upstream tests) is intentionally kept separate from
`results/browser-matrix.md` (this repo's own local WPT-runner results, for
its own novel tests) — one is "wpt.fyi ran this continuously upstream," the
other is "we ran this ourselves"; merging them would misrepresent
provenance.

## Repo structure

```
oblique/
├── LICENSE                  # BSD-3-Clause (required for WPT upstreaming)
├── README.md
├── .mise.toml                # pins python/uv AND node/pnpm versions
├── .github/workflows/
│   └── sync-wpt-results.yml # daily wpt.fyi sync, rebuilds + commits the site
├── scripts/
│   ├── setup-wpt.sh          # vendors a scoped, gitignored .wpt/ checkout
│   ├── record-results.py     # parses wptreport JSON into browser-matrix.md
│   ├── sync-wpt-results.py   # pulls live upstream results from wpt.fyi
│   ├── render-coverage-docs.py  # renders coverage.md/upstream-matrix.md
│   └── generate-site-data.py    # renders site/index.html + cards.json
├── tests/
│   ├── font-style-oblique/   # this repo's own novel tests (slnt side)
│   ├── oblique-range/
│   ├── synthesis/
│   ├── variation-settings/
│   └── ital-axis/            # the confirmed WPT gap this repo fills
├── site/                      # static Vite project — source of the public page
│   ├── template.html          # tracked source; generate-site-data.py fills it in
│   ├── src/style.css
│   ├── index.html             # generated — gitignored, see template.html
│   └── dist/                  # `pnpm run build` output — copied into docs/
├── docs/                      # published as GitHub Pages (oblique.amitkaps.com)
│   ├── index.html             # generated — copy of site/dist/index.html
│   ├── assets/                # generated — copy of site/dist/assets/
│   ├── CNAME                  # custom domain for GitHub Pages
│   ├── data/                  # generated copies of coverage.json/upstream.json
│   ├── spec.md
│   ├── plan.md
│   ├── summary.md            # short, current-state doc — start here
│   ├── investigation-log.md  # full narrative archive (was findings.md)
│   ├── coverage.md           # generated — see coverage.json
│   └── coverage.json         # source of truth for the coverage catalog
└── results/
    ├── browser-matrix.md      # this repo's own local WPT-runner results
    ├── upstream-matrix.md     # generated — see upstream.json
    └── upstream.json          # wpt.fyi-synced data, source of truth for the above
```

No WPT checkout is committed to this repo — WPT is external test-runner
infrastructure. `scripts/setup-wpt.sh` vendors a minimal, scoped copy into
a gitignored `.wpt/` for anyone who clones this repo to run tests locally;
see "Running the tests" above.
