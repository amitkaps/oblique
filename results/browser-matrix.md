# Browser compatibility matrix

Fixed columns, one row per (test, engine, version). Filled in as tests are
run via the official WPT runner — see `docs/spec.md`'s Methodology.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
| slnt-axis-activation | chrome | 153.0.8010.37 | no (emulated/Playwright) | pass | wpt run, official runner, system Chrome via --binary |
| independence | chrome | 153.0.8010.37 | no (emulated/Playwright) | pass | wpt run, official runner, system Chrome via --binary |
| italic-no-extra-synthesis | chrome | 153.0.8010.37 | no (emulated/Playwright) | fail | wpt run, official runner, system Chrome via --binary — reproduces WebKit #209565's documented ital-axis spurious-synthesis failure; see docs/investigation-log.md |
| slnt-axis-activation | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system Firefox via --binary |
| independence | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system Firefox via --binary |
| italic-no-extra-synthesis | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system Firefox via --binary |
| auto-derived-range-clamp | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| boundary-11deg-ascending | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| boundary-11deg-descending | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| independence | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt status: FAIL |
| italic-no-extra-synthesis | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt status: FAIL |
| italic-oblique-equivalence | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt status: FAIL |
| multi-branch-fallback-chain | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| slnt-axis-activation | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| style-plus-explicit-variation-settings | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| auto-derived-range-clamp | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| boundary-11deg-ascending | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| boundary-11deg-descending | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| independence | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| italic-no-extra-synthesis | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| italic-oblique-equivalence | firefox | 156.0 | no (emulated/Playwright) | fail | wpt status: FAIL |
| multi-branch-fallback-chain | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| slnt-axis-activation | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| style-plus-explicit-variation-settings | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no (emulated/Playwright)`.
