# Browser compatibility matrix

Fixed columns, one row per (test, engine, version). Filled in as tests are
run via the official WPT runner — see `docs/running.md`. Rows are appended by `scripts/record-results.py` and
`scripts/safari-replay.py`, never by hand; when a test has several rows for an engine, the last wins.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
| independence | chrome | 153.0.8010.37 | no | pass | wpt run, official runner, system Chrome via --binary |
| italic-no-extra-synthesis | chrome | 153.0.8010.37 | no | fail | wpt run, official runner, system Chrome via --binary — reproduces WebKit #209565's documented ital-axis spurious-synthesis failure |
| independence | firefox | 156.0 | no | pass | wpt run, official runner, system Firefox via --binary |
| italic-no-extra-synthesis | firefox | 156.0 | no | pass | wpt run, official runner, system Firefox via --binary |
| boundary-0deg-normal-fallback | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| independence | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| italic-no-extra-synthesis | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| italic-oblique-equivalence | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| multi-branch-fallback-chain | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | firefox | 156.0 | no | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | firefox | 156.0 | no | pass | wpt status: PASS |
| independence | firefox | 156.0 | no | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | firefox | 156.0 | no | pass | wpt status: PASS |
| italic-no-extra-synthesis | firefox | 156.0 | no | pass | wpt status: PASS |
| italic-oblique-equivalence | firefox | 156.0 | no | fail | wpt status: FAIL |
| multi-branch-fallback-chain | firefox | 156.0 | no | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| explicit-descriptor-range-clamp | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| independence | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| ital-slnt-independence-dual-axis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| italic-no-extra-synthesis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| italic-oblique-equivalence | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| multi-branch-fallback-chain | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
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
| matrix-italicnone-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicobo-normal | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italicobo-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-obl5-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-italic | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-italic | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-italic | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-italic | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-normal | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| auto-keyword-equals-omitted | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| auto-keyword-equals-omitted | firefox | 156.0 | no | pass | wpt status: PASS |
| auto-keyword-equals-omitted | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-em-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italic-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicobo-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-normal-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-obl45-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-oblique-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-em-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-em-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-em-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-em-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-em-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italic-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italic-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicobo-normal | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italicobo-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicobo-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italicobo-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italicobo-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-obl45-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-obl45-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-italic | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-oblnarrow | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-oblique-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-oblique-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-italic | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-italic | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-oblnarrow | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-slnt-oblwide | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| auto-keyword-equals-omitted | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| independence | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| italic-no-extra-synthesis | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| italic-oblique-equivalence | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| multi-branch-fallback-chain | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-em-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicobo-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-italic | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-italic | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-italic | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-oblnarrow | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-slnt-oblwide | firefox | 156.0 | no | pass | wpt status: PASS |
| auto-keyword-equals-omitted | firefox | 156.0 | no | pass | wpt status: PASS |
| boundary-0deg-normal-fallback | firefox | 156.0 | no | pass | wpt status: PASS |
| explicit-descriptor-range-clamp | firefox | 156.0 | no | pass | wpt status: PASS |
| independence | firefox | 156.0 | no | pass | wpt status: PASS |
| ital-slnt-independence-dual-axis | firefox | 156.0 | no | pass | wpt status: PASS |
| italic-no-extra-synthesis | firefox | 156.0 | no | pass | wpt status: PASS |
| italic-oblique-equivalence | firefox | 156.0 | no | fail | wpt status: FAIL |
| multi-branch-fallback-chain | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-em-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-em-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-normal | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicobo-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblnarrow | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-italic | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblnarrow | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-slnt-oblwide | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| auto-keyword-equals-omitted | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| boundary-0deg-normal-fallback | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| explicit-descriptor-range-clamp | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| independence | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| ital-slnt-independence-dual-axis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| italic-no-extra-synthesis | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| italic-oblique-equivalence | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| multi-branch-fallback-chain | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no`.
