# Oblique 
variable font oblique interop — Build Spec (v2)

## Purpose
Independent research/test repo turning CSS Fonts 4 findings from the VizChitra
font compatibility investigation into reproducible, upstreamable
interoperability tests, feeding an Interop proposal. Font- and vendor-neutral.
Cairo/VizChitra is the motivating case, not the subject.

Reference: https://fonts.vizchitra.com/compat
Available on GitHub: https://github.com/vizchitra/fonts

Scope: variable-font style matching for **both `slnt` and `ital` axes**
(now scopeable together — spec ambiguity resolved, see Prior Art), `slnt`/`ital`
axis handling, and font synthesis interoperability.

## Prior art (cite in docs/findings.md, do not re-litigate)
- Interop proposal: https://github.com/web-platform-tests/interop/issues/64
  (2022, closed without acceptance — lacked WPT test coverage; this repo supplies it)
- WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=209565
  (STILL OPEN as of last check — status NEW, unassigned. Re-verify before writing findings.md.)
- Chromium bug: https://issues.chromium.org/issues/40681464
  (fix CL passed CQ dry-run per csswg-drafts#12836 — VERIFY ACTUAL SHIP STATUS/VERSION before citing as fixed)
- Spec ambiguity, now resolved: https://github.com/w3c/csswg-drafts/issues/12836
  (clarifies: `font-style: italic` → sets `ital` axis to 1; `font-style: oblique` →
  sets `slnt` axis; the two are independent) — VERIFY this wording actually
  merged into the published css-fonts-4 draft, not just agreed in the issue thread
- Original spec ambiguity (superseded by #12836): https://github.com/w3c/csswg-drafts/issues/3125
- Community test suite: https://arrowtype.github.io/vf-slnt-test/ (reference behavior, not upstreamable itself)

## Non-goals
- Not a general compatibility framework.
- Not a permanent home for tests — everything here is staged to graduate into WPT.
- No opinions on whether a feature *should* exist — only whether behavior is interoperable per spec.

## First task: verify prior art before writing any test
Before scaffolding, the agent must:
1. Fetch current status of WebKit #209565 (open/closed, any recent activity).
2. Fetch current status of Chromium #40681464 (fixed? which version? confirm via
   the linked CL merge status, not just CQ dry-run).
3. Confirm csswg-drafts #12836's proposed wording is actually merged into
   https://drafts.csswg.org/css-fonts-4/ (search the published spec text for
   the `ital` axis clarification sentence).
4. Record all three findings in `docs/findings.md` under a "Prior Art Status"
   section with today's date, before writing any test files. If any status
   contradicts what's stated above, use the freshly-verified status.

## Repo structure

oblique/
├── LICENSE # BSD-3-Clause (required for WPT upstreaming)
├── README.md
├── tests/
│ ├── font-style-oblique/
│ ├── oblique-range/
│ ├── synthesis/
│ ├── variation-settings/
│ └── ital-axis/ # NEW — now in scope per resolved #12836
├── docs/
│ └── findings.md
└── results/
└── browser-matrix.md


No WPT checkout included. WPT is external test-runner infrastructure only.
No `fonts/` directory initially. Reuse WPT's existing variable test fonts
(need at least one font with a real `slnt` axis and one with a real `ital`
axis — check WPT's font corpus for both before assuming one exists).
Create a purpose-built font only if no existing WPT font can make a given
assertion deterministic — document the reason in that test's own README.

## Test format
- WPT-shaped from the start: **reftest pairs** (`*.html` + `*-ref.html`), not
  standalone visual pages. Prefer `testharness.js` boolean assertions over
  visual reftests wherever the behavior is programmatically checkable (e.g.
  computed `font-variation-settings` value) — reserve reftests for cases where
  only rendered slant angle can distinguish pass/fail.
- Every test file opens with a comment block citing:
  - the exact CSS Fonts 4 algorithm step it targets,
  - which prior-art issue (above) motivated it,
  - a one-line description of what a pass means.
- Parametrize angles/ranges where the assertion doesn't require Cairo's
  specific bounds — use generic values so tests aren't Cairo-specific.
- `ital`-axis tests must assert the #12836 resolution specifically: `italic`
  sets `ital`=1 and leaves `slnt` untouched; `oblique` sets `slnt` and leaves
  `ital` untouched. This independence is the core interoperability claim to test.

## Coverage checklist
- [ ] `font-style: oblique` matching a variable `slnt` axis
- [ ] Explicit `oblique <angle>` matching
- [ ] `font-style` ranges declared in `@font-face`
- [ ] Bare `oblique` / default-angle (14deg) matching
- [ ] `italic` vs `oblique` resolution differences
- [ ] `italic` on a font with only an `ital` axis (no `slnt`) — sets `ital`=1
- [ ] `oblique` on a font with only an `ital` axis — must NOT touch `ital` (per #12836)
- [ ] Font exposing both `slnt` and `ital` — confirms independence per #12836
- [ ] Single variable face covering normal + oblique
- [ ] Separate normal/oblique faces (ambiguous-match hazard)
- [ ] Font synthesis fallback behavior (`font-synthesis`)
- [ ] Explicit `font-variation-settings: 'slnt' <val>` / `'ital' <val>`
- [ ] `font-style` + explicit axis value paired (recommended pattern)
- [ ] Ancestor `font-variation-settings` inheritance/replacement behavior

## Methodology (pipeline, enforce in README)
1. Identify one CSS Fonts 4 normative requirement (cite spec section + prior-art issue).
2. Write one focused, WPT-compatible test (reftest or testharness) for it.
3. Run via the official WPT runner (not custom Playwright/vitest).
4. Record result in `results/browser-matrix.md` using the fixed schema (below).
5. Once stable and reviewed, upstream the test file(s) to WPT via PR.
6. Aggregate upstreamed + accepted tests into an Interop proposal draft in `docs/findings.md`.

## `results/browser-matrix.md` schema
Fixed columns, one row per (test, engine, version):

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no (emulated/Playwright)`.

## docs/findings.md structure
1. Prior Art Status (from the verification task above — dated)
2. Spec requirement → test(s) → matrix result → upstream status → Interop relevance, one row per requirement
3. Proposed Interop scope statement (slnt + ital, citing #12836 as spec basis)

## Definition of done for v0 scaffold
- Prior-art verification task completed and logged in docs/findings.md.
- Repo structure above created, LICENSE in place.
- One fully worked example under `tests/font-style-oblique/` AND one under
  `tests/ital-axis/` (test + ref/harness + spec-citation comment) to establish
  the pattern for both axes.
- `results/browser-matrix.md` created with schema header, no rows yet.
- README states purpose, non-goals, prior art links, and the six-step pipeline verbatim.

Right — nested triple-backtick fences inside the outer block. Here's the fix, using indented code instead of nested fences:

# Task: Add a scoped WPT checkout to variable-font-oblique-interop

## Context
The repo builds tests meant to run under the official WPT test runner. Rather than depending on an external, separately-maintained WPT clone, vendor a minimal, scoped copy directly into this repo so `./wpt run` works out of the box for anyone who clones it.

## Steps

**1.** From the repo root, clone WPT shallow + sparse into a gitignored working location (not committed as a git submodule — just the files needed to run tests):

    git clone --depth 1 --filter=blob:none --sparse \
      https://github.com/web-platform-tests/wpt.git .wpt
    cd .wpt
    git sparse-checkout set css/css-fonts tools resources
    cd ..

**2.** Add `.wpt/` to `.gitignore` — this is fetched infrastructure, not repo content, and stays out of version control (consistent with "No WPT checkout included" in the original build spec; this scopes that decision to "not committed," not "never present locally").

**3.** Add a `scripts/setup-wpt.sh` (or equivalent) that performs step 1 idempotently — check if `.wpt/` exists first, skip if so — so contributors and CI can run one command to get a working checkout.

**4.** Update `tests/*/README` or the top-level `README.md` with the run instructions:

    ./scripts/setup-wpt.sh
    cp tests/font-style-oblique/*.html .wpt/css/css-fonts/variable-oblique-interop/
    cd .wpt
    ./wpt install chrome browser
    ./wpt install firefox browser
    ./wpt run chrome css/css-fonts/variable-oblique-interop/ --log-wptreport=../results/latest-chrome.json
    ./wpt run firefox css/css-fonts/variable-oblique-interop/ --log-wptreport=../results/latest-firefox.json

Safari (macOS only, requires one-time "Allow Remote Automation" in Safari's Develop menu):

    ./wpt run safari css/css-fonts/variable-oblique-interop/

**5.** Add a small script or documented step that parses the `--log-wptreport` JSON output and appends rows to `results/browser-matrix.md` in the fixed schema already defined (`test_id | engine | version | real_device | result | notes`) — don't hand-transcribe results.

## Constraints
- Do not commit `.wpt/` or any of its contents.
- Do not widen the sparse-checkout scope beyond `css/css-fonts`, `tools`, `resources` unless a specific test needs another WPT directory (e.g. shared test fonts under `fonts/`) — if so, extend `git sparse-checkout set` explicitly and note why in the setup script's comments.
- This setup step does not replace or duplicate the existing `tests/`, `docs/`, `results/` structure — it only adds the means to *run* what's already there against the official runner.