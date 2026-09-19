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
| matrix-face-auto-use-em | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-oblique-11deg | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-slnt | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-em | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-oblique-11deg | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-slnt | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-em | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-oblique-11deg | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-slnt | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-em | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-oblique-11deg | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-slnt | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-em | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-italic | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-normal | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-oblique-11deg | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-oblique | chrome | 153.0.8010.48 | no (emulated/Playwright) | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-slnt | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| style-plus-explicit-variation-settings | chrome | 153.0.8010.48 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| auto-derived-range-clamp-cairo-symmetric | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-ascending | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-descending | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| explicit-range-bare-keyword-synthesis-stacking | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-em | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-oblique-11deg | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-auto-use-slnt | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-em | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-oblique-11deg | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-italic-use-slnt | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-em | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-oblique-11deg | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-normal-use-slnt | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-em | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-oblique-11deg | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-bare-use-slnt | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-em | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-italic | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-normal | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-oblique-11deg | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-oblique | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| matrix-face-oblique-range-use-slnt | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
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
| matrix-face-auto-use-em | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-auto-use-italic | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-auto-use-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-auto-use-oblique-11deg | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-auto-use-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-auto-use-slnt | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-italic-use-em | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-italic-use-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-italic-use-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-italic-use-oblique-11deg | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-italic-use-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-italic-use-slnt | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-normal-use-em | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-normal-use-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-normal-use-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-normal-use-oblique-11deg | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-normal-use-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-normal-use-slnt | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-bare-use-em | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-bare-use-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-bare-use-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-bare-use-oblique-11deg | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-bare-use-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-bare-use-slnt | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-range-use-em | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-range-use-italic | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-range-use-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-range-use-oblique-11deg | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-range-use-oblique | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| matrix-face-oblique-range-use-slnt | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| multi-branch-fallback-chain | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| slnt-axis-activation | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |
| style-plus-explicit-variation-settings | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/investigation-log.md section 11 |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no (emulated/Playwright)`.
