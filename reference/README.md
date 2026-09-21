# reference: CSS Fonts 4 font-style matching, as a control

An independent JavaScript implementation of the font-style parts of the CSS Fonts 4
matching algorithm. It computes, for a test case, what the spec says should happen. The
browser is the system under test; nothing here calls a browser API (`getComputedStyle`,
canvas, `FontFace`, ...), and `test/independence.test.mjs` enforces that.

```
cases/matrix.json  ->  expected()  ->  generateWpt  ->  tests/oblique-style-matching/font-style-match-{row}-{column}.html
 (rows x columns)     (this code)      (wpt.mjs)         + matrix.manifest.json
                                                              |
              wpt run (Chrome, Firefox) / scripts/safari-replay.py (Safari)
              scripts/survey.py  (measured lean, every cell)  ->  compare.mjs
```

Node 24 (pinned in `.mise.toml`), no dependencies. From the repo root (`mise run test`, `generate` and `compare` wrap the first, second and fourth):

| Command | What it does |
|---|---|
| `node --test reference/test/*.test.mjs` | unit tests: spec rules, upstream-test intent, independence, generated files up to date |
| `node reference/src/cli.mjs generate` | write the tests and manifest from `cases/matrix.json` |
| `node reference/src/cli.mjs generate --check` | fail if the committed files differ from what the generator produces |
| `node reference/src/cli.mjs classes` | which algorithm branch and outcome each cell exercises |
| `node reference/src/cli.mjs compare` | expected vs recorded results (`results/browser-matrix.md`, `results/survey.json`) |

## Files

| File | Role |
|---|---|
| `spec/css-fonts-4-excerpts.txt` | the spec text everything quotes, with URL, date and hash of the full page |
| `src/style.mjs` | parse descriptors and requests (`normal` = `oblique 0deg`; bare `oblique` = 14deg; `auto` = selected as if normal, but not clamped: 4.4) |
| `src/match.mjs` | the 5.2 face-selection stages, including the 11deg thresholds. Selects a face; does not synthesize |
| `src/variation.mjs` | 7.2: the applied `slnt`/`ital` value, clamped to the descriptor then the font; CSS angle to `slnt` flips the sign |
| `src/synthesis.mjs` | 2.8.2 `font-synthesis-style`: when a synthesized oblique is permitted |
| `src/outcome.mjs` | the vocabulary: outcomes (`slnt 0`, `slnt -11`, `synth`), their labels, file tokens, pinning CSS, and the one-line `spec: ...` / `spec*: ...` text each cell shows |
| `src/expected.mjs` | composes the three into an **allowed set of outcomes** and a status |
| `src/cases.mjs`, `src/wpt.mjs` | rows x columns to concrete cases; render the reftests and manifest |
| `src/compare.mjs` | judge recorded results and measured lean against the allowed set |

## The three statuses

The spec leaves latitude in places, so an expectation is a **set of allowed outcomes**
(`slnt 0` which is upright, `slnt -11`, `synth`), never a single guess. Every outcome is either an axis value or a
synthesized skew, and its words, file tokens and pinning CSS all come from `src/outcome.mjs`:

| Status | Meaning | Becomes |
|---|---|---|
| `specified` | exactly one testable outcome is allowed | a WPT reftest with one `match` reference |
| `constrained` | several are allowed, or synthesis is, but something is excluded | a reftest: several `match` refs (any one), or `mismatch` refs for what is forbidden |
| `unspecified` | nothing testable is excluded | no test: measured by `scripts/survey.py` and shown as "observed" |

A synthesized skew cannot be a reference (its angle differs per engine), so when synthesis
is allowed the test asserts only what is forbidden, for example "must not use the real axis".

## Where the spec is silent, the reference says so

- `assumptions` on a result record every choice the text does not make (the italic-value-1
  gap in the oblique < 11deg branch, mirrored italic stages for negative angles, how `auto`
  applies a value, ties).
- CSS Fonts 4 says both "a synthetic oblique face **will be** generated" (2.3) and "user
  agents **may** create artificial oblique faces" (5.2), so synthesis is reported as
  permitted, never required.
- `RESOLUTIONS` in `match.mjs` holds published resolutions the Editor's Draft text lags behind
  (csswg-drafts#9389: an oblique request must not fall back to an italic face). Off by default.

## Validating the reference

Upstream WPT tests are checked against what they INTEND (read from each test and its
reference), not against browsers, several of which fail them.
`test/upstream.test.mjs` covers `italic-oblique-fallback`, `font-synthesis-style-oblique-only`,
and records `oblique-last-resort-weight-selection` as a **known disagreement** with the spec
text (the test assumes an italic request is a 14deg slope; the text says 11deg).

## Adding a row or column

Append to `cases/matrix.json`; never renumber. An address (`A1`, `B2`) is a permanent label,
so inserting would silently rename tests and orphan recorded results. Then:

```
mise run generate && mise run test    # regenerate, check
# then mise run wpt-chrome, wpt-firefox, safari, survey (docs/running.md), and rebuild the site
```
