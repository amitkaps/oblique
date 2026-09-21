# Browser results

One row per (test, engine): the current result of this repo's own runs. Rows are written by
`scripts/record-results.py` (Chrome and Firefox, from `wpt run`) and `scripts/safari-replay.py --record`
(Safari), never by hand. Recording a test again replaces its row, and rows for tests that no longer exist
are dropped; git keeps the history. See `docs/running.md`.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
| font-style-match-auto-keyword-equals-omitted | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-auto-keyword-equals-omitted | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-auto-keyword-equals-omitted | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-backslant-normal-fallback | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-backslant-normal-fallback | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-backslant-normal-fallback | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italic-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italic-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italic-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italic-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italic-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italic-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italic-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italic-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italic-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italic-oblonesided | chrome | 153.0.8010.53 | no | fail | wpt status: FAIL |
| font-style-match-italic-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italic-oblonesided | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italic-oblrange | chrome | 153.0.8010.53 | no | fail | wpt status: FAIL |
| font-style-match-italic-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italic-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italicnone-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italicnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italicnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italicnone-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italicnone-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italicnone-oblonesided | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-italicnone-oblrange | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-italicnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-normal-auto | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-normal-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-normal-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-normal-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-normal-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-normal-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-normal-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-normal-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-normal-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-normal-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-normal-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-normal-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-normal-oblonesided | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-normal-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-normal-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-normal-oblrange | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-normal-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-normal-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl11-auto | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl11-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl11-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl11-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl11-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl11-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl11-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl11-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl11-oblonesided | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl11-oblrange | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl11-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl45-auto | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl45-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl45-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl45-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl45-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl45-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl45-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl45-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl45-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl45-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl45-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl45-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl45-oblonesided | chrome | 153.0.8010.53 | no | fail | wpt status: FAIL |
| font-style-match-obl45-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl45-oblonesided | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl45-oblrange | chrome | 153.0.8010.53 | no | fail | wpt status: FAIL |
| font-style-match-obl45-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl45-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl5-auto | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl5-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl5-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl5-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl5-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl5-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl5-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl5-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl5-oblonesided | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-obl5-oblrange | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-obl5-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblique-auto | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblique-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblique-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblique-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblique-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblique-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblique-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblique-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblique-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblique-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblique-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblique-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblique-oblonesided | chrome | 153.0.8010.53 | no | fail | wpt status: FAIL |
| font-style-match-oblique-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblique-oblonesided | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblique-oblrange | chrome | 153.0.8010.53 | no | fail | wpt status: FAIL |
| font-style-match-oblique-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblique-oblrange | safari | 27.0 | no (safaridriver automation) | fail | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblm5-auto.tentative | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblm5-auto.tentative | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblm5-auto.tentative | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblm5-normal.tentative | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblm5-normal.tentative | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblm5-normal.tentative | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblm5-oblbreak.tentative | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblbreak.tentative | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblbreak.tentative | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblm5-oblique.tentative | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblique.tentative | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblique.tentative | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblm5-oblonesided.tentative | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblonesided.tentative | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblonesided.tentative | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblm5-oblrange.tentative | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblrange.tentative | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblm5-oblrange.tentative | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblnone-auto | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblnone-auto | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblnone-auto | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblnone-normal | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblnone-normal | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblnone-normal | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblnone-oblbreak | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblbreak | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblbreak | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblnone-oblique | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblique | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblique | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblnone-oblonesided | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblonesided | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblonesided | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |
| font-style-match-oblnone-oblrange | chrome | 153.0.8010.53 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblrange | firefox | 156.0 | no | pass | wpt status: PASS |
| font-style-match-oblnone-oblrange | safari | 27.0 | no (safaridriver automation) | pass | direct safaridriver replay of the reftest, exact pixel compare, 3 agreeing repetitions; `wpt run safari` disagreed, see docs/running.md |

`result` ∈ `pass` / `fail` / `untested`.
`real_device` ∈ `yes` / `no`.
