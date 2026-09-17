# Oblique — Execution Plan (v0 scaffold)

## Purpose / scope recap

Oblique is an independent, font- and vendor-neutral research/test repo that
turns CSS Fonts 4 findings from the VizChitra font compatibility
investigation into reproducible, upstreamable interoperability tests, feeding
a future Interop proposal. Scope is variable-font style matching for **both**
the `slnt` and `ital` axes (now scopeable together — see csswg-drafts#12836)
plus font synthesis interoperability. It is not a general compatibility
framework, not a permanent home for tests (everything graduates into WPT),
and takes no position on whether a feature *should* exist — only whether
behavior is interoperable per spec.

Cairo/VizChitra is the motivating case, not the subject: the sibling repo
`/Users/amitkaps/code/vizchitra-fonts` (`docs/compat.md`) is where that
investigation actually happened and is a source of background/motivation and
technique, not a source of current bug status (see "Reusable context" below —
everything from it must still be re-verified live before being cited here).

## Reusable context from vizchitra-fonts (background only, re-verify before citing)

- **WebKit #209565** and **Chromium #1064756** are already cited in
  `vizchitra-fonts/docs/compat.md` as the concrete bugs behind "real Safari
  performs no automatic `font-style`→`slnt` mapping at all," confirmed there
  on a real iPhone XR (Safari 18.7). Useful lead for Step 0 below, but must
  still be freshly fetched — do not copy this status into findings.md as-is.
- **This repo's Chromium issue, #40681464, is a *different* bug** from
  #1064756. Keep them distinct in findings.md.
- **Shear-measurement methodology**: `vizchitra-fonts/src/lib/fonts/
  slant.browser.test.ts` screenshots a specimen and measures the shear of the
  rendered ink, because `slnt` barely moves advance widths (Cairo's `I` moves
  248→249 units per 1000 for either sign — advance-width comparison can't
  distinguish pass/fail). This is the concrete precedent for spec.md's
  reftest-vs-testharness split: reserve visual reftests for exactly this kind
  of case, prefer `testharness.js` boolean assertions everywhere else.
  Reuse the *principle*, not Cairo-specific numbers.
- **`docs/compat.md`'s measured results table** (bare `oblique` vs. ranged
  `oblique` vs. `font-variation-settings` `@font-face` descriptor vs.
  explicit use-site `slnt`, across Chromium/WebKit/Firefox) is a validated
  map of which behaviors are genuinely divergent across engines. Useful to
  prioritize which coverage-checklist items below get worked examples first
  — but every value must be re-parametrized generically; nothing in this
  repo's tests may be Cairo-specific.
- **Cairo (`google/fonts` `ofl/cairo`, pinned in
  `vizchitra-fonts/fonts.lock.json`) has a real `slnt` axis (−11–0–11) but no
  `ital` axis.** Confirms the font-corpus check (Step 2) is a real gate: a
  different font is required for the `ital`-axis worked example regardless
  of what else WPT's corpus has.
- **No `ital`, #12836, or #3125 references exist anywhere in
  vizchitra-fonts** — the `ital`-axis half of this repo's scope is new
  ground with no prior-art shortcut available.

## Step 0 — Prior-art verification (blocking; must complete before any test file)

1. Fetch current status of WebKit bug #209565 (open/closed, recent activity).
   Cross-check against the (stale) citation in vizchitra-fonts/docs/compat.md.
2. Fetch current status of Chromium issue #40681464 — confirm fixed/which
   version, via the linked CL's actual merge status, not just a CQ dry-run.
   Do not conflate with Chromium #1064756 (a different, related bug from the
   vizchitra investigation) — note both if both are relevant.
3. Confirm csswg-drafts #12836's proposed wording (which sets `font-style:
   italic` → `ital`=1 and `font-style: oblique` → `slnt`, independently) is
   actually merged into the published https://drafts.csswg.org/css-fonts-4/,
   not just agreed in the issue thread.
4. Record all findings in `docs/findings.md` under a "Prior Art Status"
   section, dated today. If any live status contradicts what's stated in
   spec.md or above, use the freshly-verified status. Cite
   vizchitra-fonts/docs/compat.md only as background/motivation, never as a
   current-status source.

**Gate: no test files are written until this step is logged in
`docs/findings.md`.**

## Step 1 — Repo scaffold

- Create the directory structure:
  ```
  oblique/
  ├── LICENSE                  # BSD-3-Clause — already present
  ├── README.md
  ├── tests/
  │   ├── font-style-oblique/
  │   ├── oblique-range/
  │   ├── synthesis/
  │   ├── variation-settings/
  │   └── ital-axis/           # NEW — in scope per resolved #12836
  ├── docs/
  │   └── findings.md
  └── results/
      └── browser-matrix.md
  ```
- Flesh out `README.md` with: purpose, non-goals, prior-art links (all from
  spec.md's Prior Art section), and the six-step methodology pipeline
  verbatim (see "Methodology" below).
- Create `results/browser-matrix.md` with only the fixed schema header (no
  rows yet):

  | test_id | engine | version | real_device | result | notes |
  |---|---|---|---|---|---|

  `result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
  `real_device` ∈ `yes` / `no (emulated/Playwright)`.

## Step 2 — Font corpus check

- Check WPT's existing variable-font test corpus for a font with a real
  `slnt` axis and a font with a real `ital` axis — do not assume either
  exists without checking.
- Cairo can inform the `slnt` worked example's design (it has a real `slnt`
  axis) but has no `ital` axis, so it cannot serve the `ital`-axis example.
- Only create a purpose-built font if no existing WPT font can make a given
  assertion deterministic; document the reason in that test's own README.

## Step 3 — Two worked examples (establish the pattern for both axes)

Test-format rules (from spec.md, apply to both examples):
- WPT-shaped from the start: reftest pairs (`*.html` + `*-ref.html`), not
  standalone visual pages.
- Prefer `testharness.js` boolean assertions over visual reftests wherever
  the behavior is programmatically checkable (e.g. computed
  `font-variation-settings` value); reserve reftests for cases where only
  rendered slant angle can distinguish pass/fail — apply the shear-measurement
  principle from `vizchitra-fonts/src/lib/fonts/slant.browser.test.ts` where
  a reftest is genuinely unavoidable, generalized to non-Cairo-specific
  parametrized values.
- Every test file opens with a comment block citing: the exact CSS Fonts 4
  algorithm step it targets, which prior-art issue motivated it, and a
  one-line description of what a pass means.
- Parametrize angles/ranges generically; nothing Cairo-specific.

Worked examples:
1. **`tests/font-style-oblique/`** — one fully worked reftest pair or
   testharness test (test + ref/harness + spec-citation comment), covering
   `font-style: oblique` matching a variable `slnt` axis. Use
   `docs/compat.md`'s results table (bare `oblique` vs. ranged `oblique` vs.
   `font-variation-settings` descriptor) to decide which specific behavior is
   most worth covering first — it's a validated map of what's actually
   divergent across engines.
2. **`tests/ital-axis/`** — one fully worked example asserting the #12836
   resolution specifically: `italic` sets `ital`=1 and leaves `slnt`
   untouched; `oblique` sets `slnt` and leaves `ital` untouched. This
   independence is the core interoperability claim to test, and has no
   vizchitra-fonts precedent to draw on — genuinely new test design.

## Step 4 — Run and record

- Run both worked examples via the official WPT runner (not custom
  Playwright/vitest).
- Record results as rows in `results/browser-matrix.md` using the fixed
  schema above.

## Step 5 — `docs/findings.md` aggregation

Structure:
1. Prior Art Status (from Step 0, dated).
2. Spec requirement → test(s) → matrix result → upstream status → Interop
   relevance, one row per requirement.
3. Proposed Interop scope statement (slnt + ital, citing #12836 as spec
   basis).

## Methodology (pipeline — state verbatim in README)

1. Identify one CSS Fonts 4 normative requirement (cite spec section +
   prior-art issue).
2. Write one focused, WPT-compatible test (reftest or testharness) for it.
3. Run via the official WPT runner (not custom Playwright/vitest).
4. Record result in `results/browser-matrix.md` using the fixed schema.
5. Once stable and reviewed, upstream the test file(s) to WPT via PR.
6. Aggregate upstreamed + accepted tests into an Interop proposal draft in
   `docs/findings.md`.

## Definition of done for v0 scaffold

- [ ] Prior-art verification task completed and logged in `docs/findings.md`.
- [ ] Repo structure created, `LICENSE` in place (already done).
- [ ] One fully worked example under `tests/font-style-oblique/` AND one
      under `tests/ital-axis/` (test + ref/harness + spec-citation comment)
      to establish the pattern for both axes.
- [ ] `results/browser-matrix.md` created with schema header, no rows yet.
- [ ] README states purpose, non-goals, prior-art links, and the six-step
      pipeline verbatim.

## Reference: full coverage checklist (beyond v0 — future work)

- [ ] `font-style: oblique` matching a variable `slnt` axis
- [ ] Explicit `oblique <angle>` matching
- [ ] `font-style` ranges declared in `@font-face`
- [ ] Bare `oblique` / default-angle (14deg) matching
- [ ] `italic` vs `oblique` resolution differences
- [ ] `italic` on a font with only an `ital` axis (no `slnt`) — sets `ital`=1
- [ ] `oblique` on a font with only an `ital` axis — must NOT touch `ital`
      (per #12836)
- [ ] Font exposing both `slnt` and `ital` — confirms independence per #12836
- [ ] Single variable face covering normal + oblique
- [ ] Separate normal/oblique faces (ambiguous-match hazard)
- [ ] Font synthesis fallback behavior (`font-synthesis`)
- [ ] Explicit `font-variation-settings: 'slnt' <val>` / `'ital' <val>`
- [ ] `font-style` + explicit axis value paired (recommended pattern)
- [ ] Ancestor `font-variation-settings` inheritance/replacement behavior
