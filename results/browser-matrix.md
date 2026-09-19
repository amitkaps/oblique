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
| auto-derived-range-clamp-cairo-symmetric | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-ascending | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-descending | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| explicit-range-bare-keyword-synthesis-stacking | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| style-plus-explicit-variation-settings | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| auto-derived-range-clamp-cairo-symmetric | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-ascending | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-descending | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| explicit-range-bare-keyword-synthesis-stacking | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| style-plus-explicit-variation-settings | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| auto-derived-range-clamp-cairo-symmetric | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| auto-derived-range-clamp | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| boundary-0deg-normal-fallback | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| boundary-11deg-ascending | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| boundary-11deg-descending | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| explicit-descriptor-range-clamp | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| explicit-range-bare-keyword-synthesis-stacking | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| independence | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| ital-slnt-independence-dual-axis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| italic-no-extra-synthesis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| italic-oblique-equivalence | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| multi-branch-fallback-chain | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| slnt-axis-activation | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| style-plus-explicit-variation-settings | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-em-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblrange | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblrange | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-auto | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblrange | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblrange | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblrange | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-auto | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblrange | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblrange | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblrange | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-auto | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblrange | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblrange | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblrange | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-auto | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblrange | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-em-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-em-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-italic-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-italic-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-italic-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-normal-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-normal-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-normal-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-normal-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-obl11-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-obl11-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-obl11-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-oblique-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-oblique-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-oblique-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-slnt-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-slnt-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-slnt-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-slnt-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-slnt-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no (emulated/Playwright)`.
