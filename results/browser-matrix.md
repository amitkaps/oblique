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
| auto-derived-range-clamp-cairo-symmetric | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| auto-derived-range-clamp-cairo-symmetric | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| explicit-range-bare-keyword-synthesis-stacking | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt status: FAIL |
| explicit-range-bare-keyword-synthesis-stacking | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-auto-r2-auto | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-auto-r5-auto | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-auto-r7-auto | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r2-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r4-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r5-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt status: FAIL |
| matrix-italic-r6-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r7-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r1-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r2-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r3-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r4-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r5-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r6-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r7-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r1-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r2-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r3-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r4-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r5-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r6-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r7-oblique-bare | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquerange-r3-oblique-range | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquerange-r5-oblique-range | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquerange-r6-oblique-range | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-auto-r2-auto | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-auto-r5-auto | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-auto-r7-auto | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r2-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r4-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r5-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r6-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-italic-r7-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r1-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r2-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r3-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r4-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r5-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r6-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-normal-r7-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r1-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r2-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r3-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r4-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r5-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r6-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquebare-r7-oblique-bare | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquerange-r3-oblique-range | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquerange-r5-oblique-range | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |
| matrix-obliquerange-r6-oblique-range | firefox | 156.0 | no (emulated/Playwright) | pass | wpt status: PASS |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no (emulated/Playwright)`.
