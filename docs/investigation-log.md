# Findings

> This is the full investigation trail. For the current state, see
> [oblique.amitkaps.com](https://oblique.amitkaps.com) or
> [`docs/summary.md`](summary.md).

## 1. Prior Art Status

_Verified 2026-09-18, directly against live sources (browser/tool fetches
and a raw grep of the published spec text — not recalled from spec.md or
from the vizchitra-fonts investigation)._

### WebKit #209565 — STILL OPEN

- **Status: NEW, unassigned.** Most recent activity: comment #6, 2025-03-05.
- Covers both axes: for fonts with a `slnt` axis, `font-style: italic`
  synthesizes slant instead of activating the axis, and `font-style: oblique`
  mishandles signed angles; for fonts with an `ital` axis, `font-style:
  italic` activates the axis but *also* applies a spurious 20° synthesized
  slant on top, and `font-style: oblique` synthesizes slant instead of
  consulting the axis at all.
- Matches spec.md's caveat ("STILL OPEN as of last check") — confirmed
  current, not stale.

### Chromium #40681464 — In Progress (Accepted), not fixed, not shipped

- **Title:** "font-style: italic doesn't activate the ital axis of variable
  fonts."
- **Identity confirmed, not just title-matched:** this is the *same* bug as
  `bugs.chromium.org/p/chromium/issues/detail?id=1064756`, which
  `vizchitra-fonts/docs/compat.md` cites separately as though it were a
  different Chromium bug — it is not. Confirmed via the raw issue-tracker
  JSON payload (`issues.chromium.org/issues/40681464`), independent of the
  title match: the reporter (`st...@thundernixon.com` — Stephen Nixon, the
  same individual who filed WebKit #209565 in 2020) is identical, the
  `FoundIn-80/81/82/83` labels line up with the bug's original 2020 Chromium
  version range, and the two CL numbers recorded on the issue
  (`6965375`, `8179764`) are the same CLs referenced in the csswg-drafts
  #12836 thread. Two independent sources naming identical CL numbers plus a
  reporter match is stronger evidence than a title string alone. Cite this
  as one bug with two historical tracker identifiers (Monorail `1064756` →
  Buganizer `40681464`), never as two distinct bugs.
- **Status: In Progress / Accepted** (priority P2, severity S4), assigned to
  `hj...@gmail.com`, with two pending fix CLs (`6965375`, `8179764` — the
  second explicitly reviving the first) neither of which has landed.
  **Not fixed, not shipped in any Chrome version** — do not cite it as
  fixed, per spec.md's own instruction. Last activity **2026-08-31**, the
  same date csswg-drafts PR #14412 merged (below) — the spec clarification
  and a renewed push on the Chromium fix are evidently coordinated, but the
  fix itself remains outstanding.
- **Cross-vendor visibility:** Microsoft (`se...@microsoft.com`, plus a
  `msft-consider` label) is CC'd on the issue — worth noting in this repo's
  eventual Interop proposal as evidence of existing cross-vendor interest,
  not just a Chromium/WebKit-only concern.

### csswg-drafts #12836 — RESOLVED, and the wording is live in the published spec

- **Issue status:** closed, via merged PR
  [w3c/csswg-drafts#14412](https://github.com/w3c/csswg-drafts/pull/14412),
  merged **2026-08-31**.
- **Confirmed independently**, not just from the PR description: fetched the
  raw HTML of `https://drafts.csswg.org/css-fonts-4/` and grepped it
  directly for the resolution wording. Both sentences are present in the
  published draft today:
  - Under the `font-style: italic` matching steps: *"For variable fonts with
    an ital axis, a match is created by setting the ital value to 1."*
  - Under the `oblique` matching steps: *"The ital axis is not used to
    satisfy an oblique request."*
- This confirms spec.md's framing exactly: `font-style: italic` sets `ital`
  to 1; `font-style: oblique` sets `slnt` and leaves `ital` untouched. The
  two are independent, and this is now normative spec text, not just an
  agreed-but-unpublished issue resolution — the core premise this whole repo
  is built on is sound and current as of today.

### Practical implication for this repo

The independence between `ital` and `slnt` is spec-confirmed and safe to
test against as ground truth. Both engines' actual conformance is still
catching up (WebKit: open, unassigned; Chromium: accepted and in progress,
two pending CLs, not yet landed) — which is exactly the interoperability gap
this repo exists to document with reproducible tests, not a reason to hold
off writing them.

## 2. Spec requirement → test → matrix result → upstream status → Interop relevance

| Spec requirement | Test(s) | Matrix result | Upstream status | Interop relevance |
|---|---|---|---|---|
| Bare `font-style: oblique` activates a variable font's `slnt` axis, matching the value an equivalent explicit `font-variation-settings: 'slnt'` would produce (css-fonts-4 §5.2 oblique matching) | `tests/oblique-style-matching/slnt-axis-activation.html` + `-ref.html` (reftest) | **PASS** — Chrome 153.0.8010.37, Firefox 156.0 — see `results/browser-matrix.md` | not yet upstreamed | core `slnt` claim; motivates re-opening web-platform-tests/interop#64 |
| `font-style: oblique` must NOT activate a variable font's `ital` axis when the matched face exposes only `ital` (css-fonts-4 §5.2, per #12836's "the ital axis is not used to satisfy an oblique request") | `tests/oblique-style-matching/independence.html` + `-ref.html` (reftest) | **PASS** — Chrome 153.0.8010.37, Firefox 156.0 — see `results/browser-matrix.md` | not yet upstreamed | half of the core interoperability claim for `ital`/`slnt` independence |
| `font-style: italic` against a variable `ital`-axis face must set `ital`=1 and synthesize nothing further on top of that real match (css-fonts-4 §5.2 + general "don't synthesize when a face already matches" rule) | `tests/oblique-style-matching/italic-no-extra-synthesis.html` + `-ref.html` (reftest) | **FAIL** on Chrome 153.0.8010.37, **PASS** on Firefox 156.0 — see `results/browser-matrix.md` | not yet upstreamed | **reproduces WebKit #209565's documented ital-axis failure mode live, in Chrome, while Firefox already conforms** — direct evidence Chromium #40681464's fix (in progress, two pending CLs per this doc's Prior Art Status) has not shipped, and that this is a real, currently-live two-out-of-three interop gap, not a hypothetical one |
| Bare `font-style: oblique`/`italic` (UA default angle) resolves against an AUTO-DERIVED `slnt` range (no explicit `@font-face font-style` descriptor) by clamping into the font's own fvar-declared range — the precise shape of Cairo's real-world bug (vizchitra-fonts/docs/compat.md) | `tests/oblique-style-matching/auto-derived-range-clamp.html` + `-ref.html` (reftest) | **PASS** on Chrome 153.0.8010.48 and Firefox 156.0 (2026-09-18); Safari not attempted | not yet upstreamed | **closes `docs/coverage.json`'s `auto-range-default-angle` confirmed gap for upstream-coverage purposes** — both engines correctly clamp on this font shape (Inter, one-sided `-10..0` range). Does **not** independently re-confirm or refute Cairo's own exact bug, which used a symmetric `-11..11` range — see the caveat in `docs/coverage.json`'s updated gap entry before citing this as evidence Cairo's bug no longer reproduces |

_Table grows as more worked examples are added. `italic-no-extra-synthesis`
was added after review flagged that `independence.html` forces
`font-synthesis: none`, which masks rather than probes the exact spurious-
synthesis failure #209565 documents — see the note below. `auto-range-
default-angle` was added to close the highest-priority tier-2 gap
identified during the coverage-catalog audit — its result (a clean PASS)
narrowed rather than confirmed the original Cairo-motivated hypothesis; see
"Evidence tiers" below for how this changes the tiering.

**Note on matrix rows:** all three tests above were run 2026-09-18 via the
**official WPT test runner** (`./wpt run`, vendored locally per
`scripts/setup-wpt.sh` — see README.md's "Running the tests"), against
system Chrome (153.0.8010.37) and system Firefox (156.0) on this machine,
and recorded via `scripts/record-results.py` directly from each run's
`--log-wptreport` JSON — not hand-transcribed. Getting the runner working on
this machine required a `PIP_CONSTRAINT` workaround for an unrelated
`cryptography`-build failure in wpt's own venv bootstrap (documented in
README.md) — this affects only wpt's own tooling, not this repo's tests.

**The first two tests (PASS on both engines) do not, on their own, mean
either engine fully implements the #12836 resolution.** Both were reviewed
for what they actually probe: `slnt-axis-activation` checks a genuinely
signed-angle case (bare `oblique` must resolve to the correct negative
`slnt` value, not just any slant), so its PASS is meaningful. But the
original `independence.html` only checks that `oblique` leaves `ital`
untouched *with synthesis forced off* — it cannot distinguish "no synthesis
was needed" from "synthesis was suppressed," so it does not probe WebKit
#209565's specific documented ital-axis failure ("`italic` activates the
[ital] axis but ALSO applies a spurious 20° synthesized slant on top").
`italic-no-extra-synthesis.html` was added specifically to probe that,
leaving `font-synthesis` at its default so any spurious synthesis is free
to happen — and on Chrome, it does: **Chrome 153 fails it**, reproducing
that exact failure mode live. **Firefox 156 passes it** — independently
verified beyond the wptreport status by driving `geckodriver` directly and
comparing screenshots pixel-for-pixel (the same purpose-built font showing
its real parallelogram glyph, identical between test and reference — see
"Safari" below for why that extra verification step matters and isn't
paranoia). This gives a genuine, currently-live two-of-three interop split
— Firefox conformant, Chrome's fix in progress but not shipped, WebKit's
bug open and unassigned — exactly the kind of gap this repo exists to
document with reproducible evidence rather than assert from memory.

## Safari — attempted, no reliable result (root cause found: genuine flakiness, not a font bug)

Safari was run via `./wpt run safari` (real Safari 27.0, via `safaridriver`,
not Playwright's WebKit — see vizchitra-fonts/docs/compat.md's caveat that
those are not the same engine). All three tests reported FAIL, identically
across four separate `wpt run` invocations — but this section explains why
**none of those three FAILs were recorded**. The investigation went through
several wrong turns before landing on the actual cause; documented in full,
including the wrong turns, because "measured, not assumed" (the standard
vizchitra-fonts/docs/compat.md itself holds to) cuts both ways — a FAIL
that isn't understood is not evidence, and neither is a first plausible
explanation that turns out to be wrong.

**Ruled out, in order** (kept as real fixes regardless — none was the
actual cause, but none was wrong to do):

1. **Font-loading race** — added the standard WPT `reftest-wait` +
   `document.fonts.ready` pattern to all six test/ref files. No change.
2. **Font MIME type** — `wpt serve` has no `.ttf`/`.woff2` entries in its
   `content_types` table at all (confirmed by reading
   `tools/wptserve/wptserve/constants.py`), so both fonts were served as
   `application/octet-stream`. Added `.headers` sidecar files declaring
   `font/ttf` / `font/woff2` (WPT's own convention). No change.
3. **`STAT` table, `OS/2.fsType`, variable-font machinery, contour winding
   direction** — each investigated and ruled out in turn (a static,
   non-variable version of the glyph failed identically; a
   clockwise-rewound version failed identically; WPT's own working font
   turned out to share our font's `fsType` value, disproving that theory
   outright).

**What actually explains it, confirmed decisively:** isolating
`slnt-axis-activation` alone (WPT's own official, pristine `FontStyleTest-
slnt-VF.woff2` — no custom font of ours involved at all) through `wpt run
safari` **still FAILs**, with the exact same screenshot hash as every
previous run. That single fact already rules out every font-specific theory
above — the font was never the problem. Driving `safaridriver` directly via
raw WebDriver calls (bypassing `wpt run` entirely) to test the *same* page
three times, identically (fresh session, fresh navigation, identical 3-second
wait each time) produced **two different outcomes**: trial 1 rendered the
wrong (system fallback) font, trials 2 and 3 rendered the correct custom
font — byte-for-byte matching the reference either way. A longer, continuous
19.5-second wait within a single un-renavigated session did not resolve a
stuck wrong render, and forcing an explicit repaint (`window.resizeBy` +
reading `offsetHeight`) didn't either. **This is genuine, real
nondeterminism in Safari/WebKit's font-loading-to-compositor pipeline when
driven via `safaridriver` WebDriver automation** — not a deterministic bug
with a discoverable root cause. Four unlucky `wpt run` invocations in a row
is well within what that kind of flakiness produces.

**No Safari row is recorded in `results/browser-matrix.md` for any of the
three tests.** A result that's genuinely a coin-flip under WebDriver
automation isn't usable interoperability evidence in either direction —
recording a FAIL would misrepresent Safari (which, per the passing trials,
likely does the right thing), and recording a PASS from a single lucky run
would be just as unfounded. **This also means the earlier framing in
`README.md`'s "Known issue" section blaming `fontTools`-generated TTFs
specifically was wrong and has been corrected** — that was one plausible
theory built on too few trials before the isolation test (an unmodified
WPT font, alone, still failing) disproved it.

**For whoever picks this up next:** this looks like a real, reportable
WebKit/`safaridriver` bug (font activation racing against the WebDriver
screenshot command, independent of font validity) rather than anything
fixable from this repo's side. Before spending more time on it: search
`bugs.webkit.org` for existing reports of flaky/stale font rendering in
`safaridriver` screenshots specifically (distinct from #209565, which is
about which axis gets activated, not about rendering nondeterminism). If
none exists, this trial data (3 identical trials, 2 different outcomes) is
enough to file one. A real physical macOS device running the actual Safari
UI (not `safaridriver` automation) would be the way to get a trustworthy
manual reading in the meantime, matching vizchitra-fonts/docs/compat.md's
own reason for keeping a manual `/compat` page alongside automated tests.

## Existing WPT coverage

_Audited 2026-09-18 — see [`docs/coverage.md`](coverage.md) (generated from
[`docs/coverage.json`](coverage.json)) for the full catalog, and
[`results/upstream-matrix.md`](../results/upstream-matrix.md) for live
per-engine results sourced from [wpt.fyi](https://wpt.fyi)._

This repo's original plan (spec.md v2) assumed WPT had little coverage of
oblique/`slnt` matching and planned to write new tests across five
categories from scratch. A direct walk of the vendored `css/css-fonts` tree
(not a search-snippet sample) found that assumption wrong: **37 existing
upstream tests** touch `slnt`, oblique matching, or closely related
synthesis/parsing.

`docs/coverage.json`'s `checklist_mapping` cross-references every one of
spec.md's original 14-item coverage checklist against this catalog (broader
than the `probes_209565` flag — an item can be fully covered without any
single test targeting that specific bug). Result: **11 of 14 items are
covered** (9 upstream, 2 by this repo's own `ital`-axis tests only) — down
from an earlier "12 of 14" after "Separate normal/oblique faces
(ambiguous-match hazard)" was found to be wrongly marked covered (see gap 2
below).

**Four confirmed, currently-open gaps** were found — logged in
`docs/coverage.json`'s `confirmed_gaps` field, more precise than a raw
checklist-item miss because each was verified by reading the actual content
of the closest candidate test, not its title:

1. **`auto-range-default-angle`** (now closed — see §2's test-result table
   above) — no test combined an *auto-derived* oblique range (no explicit
   `@font-face font-style` descriptor — the realistic deployment shape)
   with a *bare* `font-style: oblique` or `font-style: italic` request on a
   font whose real range excludes the UA default angle. This is the
   precise shape of Cairo's real-world bug (vizchitra-fonts/docs/compat.md):
   Cairo ships with no `font-style` descriptor, so its usable range comes
   entirely from its own `slnt` axis (-11 to 11), and the default angle
   (14deg) falls outside it. Initial review of this catalog credited
   `font-slant-1.html` and `synthetic-oblique-out-of-capabilities-range.html`
   with covering this — **that was wrong**, corrected after checking the
   actual test content. A test now exists
   (`tests/oblique-style-matching/auto-derived-range-clamp.html`) and passes on
   Chrome/Firefox — see §2 and "Evidence tiers" below for the full,
   caveated result.
2. **`normal-plus-bare-oblique-same-family`** — no test constructs a
   same-family pairing of a `font-style: normal` face and a bare/unranged
   `font-style: oblique` face and checks that an angled request correctly
   selects the oblique face. This checklist item was previously marked
   covered, citing three `matching/` tests
   (`style-ranges-over-weight-direction.html`, `fixed-stretch-style-over-weight.html`,
   `stretch-distance-over-weight-distance.html`) — **wrong**, corrected
   after reading all three in full: every `@font-face` block in all three
   uses `font-style: oblique <angle-or-range>`, none uses `normal`. They
   test precedence *among multiple oblique candidates*, never a
   normal-vs-oblique scenario. Corroborated by vizchitra-fonts' own
   `fonts.css`, which ships two separate `@font-face` blocks (one `normal`,
   one ranged `oblique`) specifically to avoid this hazard.
3. **`font-style-plus-explicit-axis-pairing`** — no test pairs `font-style`
   with an explicit `font-variation-settings` axis override on the same
   declaration and checks the resulting precedence.
4. **`combined-slnt-ital-font`** — no font anywhere (WPT's corpus or this
   repo's own resources) exposes both a real `slnt` axis and a real `ital`
   axis together, needed to test #12836's independence claim in its
   strongest form.

See `docs/coverage.md`'s "Confirmed gaps" section for the full detail on
each, including candidate test designs, priority, and evidence tier.

### A live finding, not a gap: three `matching/` tests fail on Safari today

Separate from the checklist audit, scoping a `scripts/sync-wpt-results.py
--paths` run to the 13 upstream tests most central to this repo's `slnt`
claim (the 7 `slnt`/`font-slant-*` tests, all three `matching/` precedence
tests, and the 3 range-descriptor-normalization tests) surfaced a real,
dated, currently-live result that wasn't previously called out in prose
anywhere, even though it's been visible in the raw synced data and on the
dashboard's table all along:

**10 of the 13 pass cleanly across Chrome, Firefox, and Safari. The other
3 — all three `matching/` precedence tests
(`style-ranges-over-weight-direction.html`, `fixed-stretch-style-over-weight.html`,
`stretch-distance-over-weight-distance.html`) — PASS on Chrome and Firefox
but FAIL on Safari**, per wpt.fyi's own stable CI (Chrome 153.0.8010.47,
Firefox 156.0, Safari 27.0, run ids 5204236987269120 / 5096862033117184 /
6240852912635904, queried via `GET /api/runs?label=stable&max-count=1&product=<x>`
then `GET /api/search?run_ids=<ids>&q=<filename>`, 2026-09-18).

This is not a coverage gap — these tests exist and run — it's evidence
that Safari currently doesn't correctly implement the stretch-over-style-
over-weight search-direction precedence rule these three tests check. It's
tier-1-grade evidence (a written test, a dated cross-engine result, a real
currently-live failure) by the same standard as
`tests/oblique-style-matching/italic-no-extra-synthesis.html`, just discovered via
wpt.fyi sync rather than a test this repo authored. Same Safari-provenance
caveat as elsewhere in this document applies: this is wpt.fyi's own CI
run, not this repo's flaky local `safaridriver` investigation, so it's
good evidence, not a single unverified local result.

The same audit confirmed the inverse for `ital`: **zero** existing WPT tests
anywhere under `css/css-fonts/` reference the `ital` variation axis in any
form (search method and result logged in `docs/coverage.json`'s
`ital_axis_gap` field). This is now the repo's primary reason to author new
tests at all — `tests/oblique-style-matching/` fills a real, confirmed gap, rather than
duplicating coverage that already exists.

Given this, the repo's ongoing value shifts from "write new tests broadly"
to: track existing WPT coverage's live status via wpt.fyi
(`scripts/sync-wpt-results.py`, scheduled daily,
`results/upstream-matrix.md`), and keep authoring new tests specifically
for the confirmed gaps. See `docs/spec.md`'s "Scope update (v3)" section
and README.md's "Live coverage dashboard" section for the mechanics.

See "4. Evidence tiers for the Interop proposal" below for how these
findings — this section's and the earlier worked-example results — are
weighted for the proposal, rather than treated as equally strong.

## 3. Proposed Interop scope statement

Scope: variable-font style matching for both the `slnt` and `ital` axes,
scoped together on the basis that css-fonts-4 (per the resolution of
[csswg-drafts#12836](https://github.com/w3c/csswg-drafts/issues/12836),
merged into the published draft 2026-08-31) treats them as independent,
well-defined axes with distinct matching rules — `italic` activates `ital`,
`oblique` activates `slnt`, and neither touches the other. The original 2022
Interop proposal ([web-platform-tests/interop#64](https://github.com/web-platform-tests/interop/issues/64))
was closed without acceptance for lack of WPT test coverage; this repo's
purpose is to supply that coverage, generically (not tied to any one font or
vendor), so the proposal can be re-raised on firmer ground.

Four confirmed gaps back this scope now (up from three — see "Evidence
tiers" below): `auto-range-default-angle` (now closed with a written,
run test), `normal-plus-bare-oblique-same-family` (newly confirmed — see
below), `font-style-plus-explicit-axis-pairing`, and
`combined-slnt-ital-font`. The proposal leads with the tier-1 and tier-2
evidence below (already proven live, or root-caused and corroborated
pending a written test) and explicitly excludes tier-3 findings from its
scope — those are logged for completeness, not cited as impact evidence.

## 4. Evidence tiers for the Interop proposal

Not every finding in this repo carries equal weight as motivating evidence
for the proposal above. `docs/coverage.json`'s top-level `evidence_tiers`
field defines three tiers; every checklist item and confirmed gap in that
file carries a `priority_tier` back-referencing this list, so an item's
weight is stated, not left for a reader to infer from tone.

**Tier 1 — proven, reproducible, live today.** A written test with a dated,
recorded cross-engine result showing the failure actually happening:

- `tests/oblique-style-matching/italic-no-extra-synthesis.html` — **fails on Chrome
  153.0.8010.37, passes on Firefox 156.0**, recorded 2026-09-18 in
  `results/browser-matrix.md`. This is the strongest evidence this repo
  has: a live, currently-reproducible interop gap.
- `tests/oblique-style-matching/independence.html` — passes on both Chrome and Firefox,
  also dated and recorded, though (per section 2 above) its
  `font-synthesis: none` setup makes the PASS less discriminating than
  `italic-no-extra-synthesis.html`'s.
- **`tests/oblique-style-matching/auto-derived-range-clamp.html`** — added
  2026-09-18 to close the `auto-range-default-angle` gap (below). Passes
  on Chrome 153.0.8010.48 and Firefox 156.0. **This graduated the gap from
  tier 2 to tier 1**, but note the result is a clean PASS, not a
  reproduction — see its entry below for why that doesn't fully close the
  question this gap was motivated by.

**Tier 2 — proven gap, root cause traced to a real bug or documented
production hazard, test not yet written.** The failure mode is confirmed
to exist, but no test demonstrates it yet:

- **`normal-plus-bare-oblique-same-family`** (`docs/coverage.json`'s
  `confirmed_gaps`, priority 1 — now the recommended next worked example).
  No test constructs a same-family pairing of a `font-style: normal` face
  and a bare/unranged `font-style: oblique` face and checks that an angled
  request correctly selects the oblique face rather than falling back to
  upright. **This checklist item was previously marked
  `covered-upstream`, citing three `matching/` tests — that was wrong**,
  corrected after reading all three in full (not inferring from
  title/filename): `css/css-fonts/matching/style-ranges-over-weight-direction.html`,
  `fixed-stretch-style-over-weight.html`, and
  `stretch-distance-over-weight-distance.html` all declare every
  `@font-face` block with `font-style: oblique <angle-or-range>` — none
  declares `font-style: normal`. They test precedence *among multiple
  oblique candidates* (stretch/weight/style search direction and
  distance), never a normal-vs-oblique same-family scenario. A fourth
  candidate, `at-font-face-font-matching.html`, was also read in full as a
  near-miss: its `descriptorPriorityTest` family uses `font-style: italic`
  (not `oblique`) and has no `normal` face either. **Corroborating
  evidence is first-party, not a third-party font** (a different kind of
  corroboration than `auto-range-default-angle`'s Cairo/Inter citations):
  vizchitra-fonts' own `fonts.css` ships Cairo as two separate
  `@font-face` blocks under the same family — one `normal`, one ranged
  `oblique` — rather than one combined face, specifically because
  Chromium/WebKit have been observed picking the wrong (upright) face for
  an angled request in that scenario (vizchitra-fonts/docs/compat.md's
  historical-hazard note). This is the repo's own operational workaround
  for the exact hazard this gap describes.
- **`font-style-plus-explicit-axis-pairing`** (`docs/coverage.json`'s
  `confirmed_gaps`, priority 2). A real, spec-recommended author pattern
  (pairing `font-style` with an explicit `font-variation-settings`
  override for fallback compatibility) that's untested anywhere. Has **no
  specific corroborating broken font or production practice** behind it
  (`docs/coverage.json` marks this `lacks_corroborating_font: true`) — a
  different kind of gap (recommended-pattern-untested vs.
  bug-with-known-cause) than the one above, and shouldn't be read as
  carrying the same evidentiary weight.

**Tier 1, with a caveat — `auto-range-default-angle`, now closed but not
confirmatory.** `docs/coverage.json`'s `confirmed_gaps` (priority 4, now
that it's done) — this **was** the recommended next worked example and now
has one: `tests/oblique-style-matching/auto-derived-range-clamp.html`. This is
directly Cairo's own documented real-world failure mode
(vizchitra-fonts/docs/compat.md: no `font-style` descriptor authored, so
the UA must derive the oblique range from Cairo's own `slnt` axis (-11 to
11), and the default angle (14deg) falls outside it). The closest upstream
test, `font-slant-1.html`, was checked directly and confirmed **not** to
cover this — it tests the identical default-angle-outside-range question,
but only for an explicitly authored descriptor range (and passes on
Chrome/Firefox/Safari per `results/upstream.json`, synced 2026-09-17T23:17
UTC — that Safari result is from wpt.fyi's own GitHub Actions CI run, a
distinct and more controlled environment than this repo's local
`safaridriver` investigation, see "Safari — attempted, no reliable result"
above). **The new test — using WPT's own `Inter.var.subset.ttf` (`slnt`
range -10 to 0, verified via `fontTools`) — PASSES on both Chrome
153.0.8010.48 and Firefox 156.0, run 2026-09-18.** Read this carefully:
the general upstream-coverage gap is closed, and the clamping mechanism
this gap worried about works correctly on both engines for Inter's shape
— but Inter's range is one-sided (-10 to 0), not Cairo's symmetric
(-11 to 11), so **this result does not independently re-confirm or refute
Cairo's own original real-device finding**. If Cairo's exact bug is worth
re-verifying, the next step is the same test against a font with Cairo's
actual symmetric range (or Cairo itself, subsetted) — not yet done.

**Tier 3 — confirmed absent, spec-completeness, no known real-world
instance.**

- **`combined-slnt-ital-font`** (priority 3). No font anywhere — WPT's
  corpus or this repo's own resources — exposes both a real `slnt` axis
  and a real `ital` axis together (`docs/coverage.json` marks this
  `real_world_font_exists: false`). Worth closing for completeness (it's
  the strongest possible direct test of #12836's independence claim), but
  it is **not evidence of real-world impact** and the proposal should not
  cite it as such.

### Next worked examples, in priority order

1. ~~`auto-range-default-angle`~~ — **done**, see above (Chrome/Firefox
   PASS; Cairo's exact symmetric range still unverified if worth
   revisiting).
2. **`normal-plus-bare-oblique-same-family`** — still the only one of the
   four original confirmed gaps not yet closed. Explicitly **not**
   addressed by the `tests/oblique-style-matching/` consolidation below —
   flagged in that folder's own README rather than left ambiguous.
3. ~~`font-style-plus-explicit-axis-pairing`~~ — **done**, see §5 below.
4. ~~`combined-slnt-ital-font`~~ — **done**, see §5 below — closing it
   surfaced a real, dated Chrome-only finding, not a clean pass.

## 5. `tests/oblique-style-matching/` — consolidation and two new findings (2026-09-18)

This project's own tests were consolidated from their earlier scattered
locations (`tests/font-style-oblique/`, `tests/ital-axis/`, both now
removed) into a single `tests/oblique-style-matching/` folder — the
candidate for a future WPT PR — and extended with 8 new test files covering
the CSS Fonts 4 §5.2 boundary-value table and §7.2 precedence question that
weren't tested anywhere before. Full design rationale, the boundary-value
table, and the font-shape table are in
[`tests/oblique-style-matching/README.md`](../tests/oblique-style-matching/README.md),
not duplicated here.

Every new spec claim was grounded by fetching CSS Fonts 4's raw HTML
directly (`https://drafts.csswg.org/css-fonts-4/`) and extracting the exact
normative text for §5.2 "Matching font styles" and §7.2 "Feature and
variation precedence" — not paraphrased from memory or from this project's
own earlier, less precise summaries.

Two genuine, dated, cross-engine findings came out of writing and running
these 8 new tests (Chrome 153.0.8010.48, Firefox 156.0; Safari attempted
twice via local `safaridriver` and not recorded — see "Safari — attempted,
no reliable result" above, same root cause, same discipline):

- **`ital-slnt-independence-dual-axis.html` FAILS on Chrome, PASSES on
  Firefox.** `resources/oblique-dual-axis.ttf` is this project's first font
  with both a real `slnt` axis and a real `ital` axis. Before trusting this
  as a real finding, it was isolated directly: forcing
  `font-variation-settings: 'slnt' 0` on top of Chrome's automatic
  `font-style: italic` collapses the rendering to a plain unsheared
  rectangle, and forcing `'ital' 1` instead restores full shear matching
  the explicit reference. That means Chrome's automatic `italic`
  resolution is driving the `slnt` axis on this font, not purely `ital` —
  a fresh, reverse-direction instance of the same class of axis-crosstalk
  bug WebKit #209565 documents.
- **`italic-oblique-equivalence.html` FAILS on BOTH Chrome and Firefox.**
  An earlier draft of this test added a decoy `font-style: normal` face to
  the family, reasoning a wrong-face selection would then be visually
  unmistakable — that was a genuine test-construction mistake, not a
  Chrome finding: a `normal`-declared face implicitly carries an oblique
  value of 0, reachable by the oblique&ge;11deg branch's own first search
  stage ("...until 0 is hit") before the italic fallback step is ever
  reached, so the decoy changed which branch stage resolved the request.
  Corrected (decoy removed, confirmed via isolation that the fallback step
  itself works correctly on Chrome). After that fix, the test still fails
  on both engines — the fallback step works, but the resulting render
  doesn't match explicit `'ital' 1`, the same under-sheared/offset
  signature as the dual-axis finding above. Unlike that finding, this
  one's root cause is **not** fully isolated per-engine — recorded
  honestly as a live, dated, two-engine finding, not a fully diagnosed
  one, per this project's own "don't guess" discipline.

The other 10 files in the folder (including the four moved/consolidated
tests) pass on both Chrome and Firefox. Full per-file results:
[`results/browser-matrix.md`](../results/browser-matrix.md).

## 6. Re-verifying `auto-derived-range-clamp` on Cairo's exact range shape (2026-09-19)

`auto-derived-range-clamp.html` (section 5) closed the general WPT coverage
gap for "bare `oblique`/`italic` against an auto-derived `slnt` range that
excludes the UA default angle" — but `docs/coverage.json` flagged an
explicit caveat: the test font, Inter, has a one-sided range (`-10..0`),
not Cairo's real symmetric range (`-11..11`), so the PASS result didn't
independently confirm or refute whether Cairo's own real-world bug
(`vizchitra-fonts/docs/compat.md`) still reproduces.

That follow-up is now done:
[`auto-derived-range-clamp-cairo-symmetric.html`](../tests/oblique-style-matching/auto-derived-range-clamp-cairo-symmetric.html)
uses `resources/oblique-symmetric.ttf` (already built during the 2026-09-18
consolidation for the boundary-value tests), whose `fvar` `slnt` axis is
exactly `-11..11` — verified via fontTools, matching Cairo's documented
range precisely rather than just sharing its "excludes 14deg" shape.

**Result: PASS on both Chrome and Firefox** — identical outcome to the
Inter-range test. Range shape alone does not explain Cairo's original
real-device finding; if that bug still reproduces today, something other
than the auto-derived-range-clamping mechanism itself (Cairo's specific
`STAT` table, a different browser version, or some other Cairo-specific
factor) would have to account for it. `docs/coverage.json`'s
`auto-range-default-angle` gap now carries two independent, dated,
cross-engine PASS results — one per range shape — rather than one.

**A test-construction mistake caught before recording any result:** the
first draft of this test copied its rendered text ("slant") from the
Inter-based test. `oblique-symmetric.ttf` is a purpose-built font whose
`setupCharacterMap` only maps the letter `'A'`
(`resources/build-fonts.py:86`) — it has no glyphs for `s`, `l`, `n`, or
`t`. That draft silently fell back to a system font on both the test page
and its reference (same fallback on both sides), and `wpt run` reported
FAIL on both Chrome and Firefox with a 2932-pixel diff. Before trusting
that as a real finding, a standalone probe page comparing bare
`oblique`/`italic` against explicit `font-variation-settings: 'slnt' -11`
made it obvious the custom font wasn't rendering distinctly at all in any
of the five variants — confirming a construction bug, not a genuine
divergence from the Inter-range result. Fixed by rendering `'A'` instead
of `'slant'`; both engines then PASS. Not corrected silently — recorded
here per this project's "measured, not assumed" discipline, same as the
two mistakes caught in section 5.

## 7. A different bug shape found by reading a sibling project's own browser tests (2026-09-19)

Reviewing `vizchitra-fonts/docs/compat.md` and
`vizchitra-fonts/src/lib/fonts/slant.browser.test.ts` directly (a separate,
real production codebase's own measured cross-engine matrix, not a third-
party bug report) surfaced that Cairo's deployment has moved on since this
repo's earlier citations: it no longer ships with no `font-style`
descriptor. It now declares an **explicit** range matching its own true
`slnt` bounds exactly — `font-style: oblique -11deg 11deg` — specifically
because the bare/auto-derived shape turned out to have its own separate
trap (see below).

That sibling project's own measured matrix documents a bug this repo's
existing tests structurally cannot see: **once the `slnt` axis is
correctly clamped to a declared range's boundary, Chromium separately
stacks an additional synthetic skew on top of it.** Requesting bare
`font-style: oblique` (implied 14deg, outside the declared -11..11 range)
against Cairo measures shear ≈0.44 in Chromium instead of the correct
≈0.194 — roughly double, because the axis clamp itself is correct but an
extra synthetic skew is added on top. WebKit fails the same case a
different way (discards the axis, synthesizes instead). Only Firefox
measures correct.

**Why none of this repo's prior range-clamp tests caught this:**
`auto-derived-range-clamp.html`, `auto-derived-range-clamp-cairo-
symmetric.html`, and `explicit-descriptor-range-clamp.html` all set
`font-synthesis: none` — a deliberate isolation choice, to answer "did
automatic `slnt` matching alone pick the right value?" independent of
synthesis. That isolation is exactly what makes Chromium's stacking
mechanism impossible to trigger. It's not a per-font or per-range-shape
gap like section 6's — it's structural to every test in this folder that
suppresses synthesis.

**New test:**
[`explicit-range-bare-keyword-synthesis-stacking.html`](../tests/oblique-style-matching/explicit-range-bare-keyword-synthesis-stacking.html)
reproduces the shape faithfully: `resources/oblique-symmetric.ttf`
(already built for section 6's test) with an **explicit** `font-style:
oblique -11deg 11deg` descriptor matching its own true bounds, bare
`oblique`/`italic` requested, `font-synthesis` deliberately left at its
default (the first test in this folder to do so). Grounded in CSS Fonts 4
§2.8.2 (`font-synthesis-style`): synthesis of oblique faces is specified to
apply "when a font family lacks oblique faces" (fetched from the raw spec
HTML, 2026-09-19) — this family does not lack one.

**Result: FAIL on Chrome, PASS on Firefox** — verified with pixel
measurement before trusting it (same discipline as every other finding in
this file): a probe page comparing bare `oblique` under default synthesis
against the same request under `font-synthesis: none` and against an
explicit `font-variation-settings: 'slnt' -11` showed 36px of top-vs-bottom
shear for the default-synthesis case, vs. 20px (identical) for the other
two — a real, visible ~1.8× over-slant, not a test-construction artifact.
This exactly matches the independently-measured Chrome-FAIL/Firefox-PASS
pattern in `vizchitra-fonts`' own test suite, despite using a completely
different (synthetic, purpose-built) font. Safari attempted, `safaridriver`
binary unavailable in this environment — not recorded, per this project's
established Safari policy.

**Two related findings surfaced but not yet built as tests here**, flagged
rather than silently dropped: `vizchitra-fonts`' own matrix separately
measures (1) a third, distinct WebKit failure mode for the `italic`
variant of this same shape (a pure ~14deg synthetic skew with **no** axis
contribution at all, unlike Chromium's stack-on-top-of-a-correct-axis
shape) — not independently confirmed here, since Safari/WebKit could not
be run; and (2) a live, measured reproduction of this repo's still-open
`normal-plus-bare-oblique-same-family` gap (§5.2's bare-oblique-on-a-
same-family-with-a-normal-sibling hazard) — Chromium and WebKit pick the
wrong, upright face entirely in that case. Both are now cited as
corroborating evidence in `docs/coverage.json`, neither has a test in this
repo yet.
