# Browser compatibility matrix

Fixed columns, one row per (test, engine, version). Filled in as tests are
run via the official WPT runner — see `docs/running.md`. Rows are appended by `scripts/record-results.py` and
`scripts/safari-replay.py`, never by hand; when a test has several rows for an engine, the last wins.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
| slnt-axis-activation | chrome | 153.0.8010.37 | no | pass | wpt run, official runner, system Chrome via --binary |
| independence | chrome | 153.0.8010.37 | no | pass | wpt run, official runner, system Chrome via --binary |
| italic-no-extra-synthesis | chrome | 153.0.8010.37 | no | fail | wpt run, official runner, system Chrome via --binary — reproduces WebKit #209565's documented ital-axis spurious-synthesis failure |
| slnt-axis-activation | firefox | 156.0 | no | pass | wpt run, official runner, system Firefox via --binary |
| independence | firefox | 156.0 | no | pass | wpt run, official runner, system Firefox via --binary |
| italic-no-extra-synthesis | firefox | 156.0 | no | pass | wpt run, official runner, system Firefox via --binary |
| auto-derived-range-clamp | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| boundary-11deg-ascending | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| boundary-11deg-descending | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| independence | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| italic-no-extra-synthesis | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| italic-oblique-equivalence | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| multi-branch-fallback-chain | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| slnt-axis-activation | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| style-plus-explicit-variation-settings | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| auto-derived-range-clamp | firefox | 156.0 | no | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | firefox | 156.0 | no | pass | wpt status: PASS |
| boundary-11deg-ascending | firefox | 156.0 | no | pass | wpt status: PASS |
| boundary-11deg-descending | firefox | 156.0 | no | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | firefox | 156.0 | no | pass | wpt status: PASS |
| independence | firefox | 156.0 | no | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | firefox | 156.0 | no | pass | wpt status: PASS |
| italic-no-extra-synthesis | firefox | 156.0 | no | pass | wpt status: PASS |
| italic-oblique-equivalence | firefox | 156.0 | no | fail | wpt status: FAIL |
| multi-branch-fallback-chain | firefox | 156.0 | no | pass | wpt status: PASS |
| slnt-axis-activation | firefox | 156.0 | no | pass | wpt status: PASS |
| style-plus-explicit-variation-settings | firefox | 156.0 | no | pass | wpt status: PASS |
| auto-derived-range-clamp-cairo-symmetric | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| auto-derived-range-clamp-cairo-symmetric | firefox | 156.0 | no | pass | wpt status: PASS |
| explicit-range-bare-keyword-synthesis-stacking | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| explicit-range-bare-keyword-synthesis-stacking | firefox | 156.0 | no | pass | wpt status: PASS |
| auto-derived-range-clamp-cairo-symmetric | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-ascending | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-descending | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| explicit-range-bare-keyword-synthesis-stacking | chrome | 153.0.8010.48 | no | fail | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| style-plus-explicit-variation-settings | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| auto-derived-range-clamp-cairo-symmetric | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-ascending | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| boundary-11deg-descending | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| explicit-range-bare-keyword-synthesis-stacking | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| style-plus-explicit-variation-settings | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; default font-synthesis, real Cairo subset |
| auto-derived-range-clamp-cairo-symmetric | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| auto-derived-range-clamp | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| boundary-0deg-normal-fallback | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| boundary-11deg-ascending | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| boundary-11deg-descending | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| explicit-descriptor-range-clamp | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| explicit-range-bare-keyword-synthesis-stacking | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| independence | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| ital-slnt-independence-dual-axis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| italic-no-extra-synthesis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| italic-oblique-equivalence | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| multi-branch-fallback-chain | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| slnt-axis-activation | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| style-plus-explicit-variation-settings | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-normal | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblique | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblrange | chrome | 153.0.8010.48 | no | fail | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-normal | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblique | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblrange | chrome | 153.0.8010.48 | no | fail | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-auto | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-normal | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblique | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblrange | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-normal | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblique | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblrange | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-normal | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblique | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblrange | chrome | 153.0.8010.48 | no | fail | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-auto | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-italic | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-normal | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblique | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblrange | chrome | 153.0.8010.48 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-normal | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblique | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-oblrange | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-normal | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblique | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-italic-oblrange | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-auto | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-normal | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblique | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-normal-oblrange | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-normal | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblique | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-obl11-oblrange | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-normal | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblique | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-oblique-oblrange | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-auto | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-italic | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-normal | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblique | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-slnt-oblrange | firefox | 156.0 | no | pass | wpt run, official runner, system browser via --binary; generated from reference/, default font-synthesis |
| matrix-em-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no`.
