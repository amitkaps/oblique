# Browser results

One row per (test, engine): the current result of this repo's own runs. Rows are written by
`scripts/record-results.py` (Chrome and Firefox, from `wpt run`) and `scripts/safari-replay.py --record`
(Safari), never by hand. Recording a test again replaces its row, and rows for tests that no longer exist
are dropped; git keeps the history. See `docs/running.md`.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
| matrix-italic-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italic-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblonesided | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italic-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblonesided | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italic-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-italic-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italic-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblonesided | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-italicnone-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-italicnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-italicnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblonesided | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-normal-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-normal-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-normal-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblonesided | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl11-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl11-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl11-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl45-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblonesided | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-obl45-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblonesided | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl45-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-obl45-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl45-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblonesided | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-obl5-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-obl5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-obl5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblique-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblonesided | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-oblique-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblonesided | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblique-oblrange | chrome | 153.0.8010.48 | no | fail | wpt status: FAIL |
| matrix-oblique-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblique-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblonesided | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblm5-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblm5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblm5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-auto | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-normal | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblbreak | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblique | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblonesided | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| matrix-oblnone-oblrange | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| matrix-oblnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| matrix-oblnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| standalone-auto-keyword-equals-omitted | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| standalone-auto-keyword-equals-omitted | firefox | 156.0 | no | pass | wpt status: PASS |
| standalone-auto-keyword-equals-omitted | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| standalone-backslant-normal-fallback | chrome | 153.0.8010.48 | no | pass | wpt status: PASS |
| standalone-backslant-normal-fallback | firefox | 156.0 | no | pass | wpt status: PASS |
| standalone-backslant-normal-fallback | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |

`result` ∈ `pass` / `fail` / `untested`.
`real_device` ∈ `yes` / `no`.
