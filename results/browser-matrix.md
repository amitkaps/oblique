# Browser compatibility matrix

Fixed columns, one row per (test, engine, version). Filled in as tests are
run via the official WPT runner — see `docs/spec.md`'s Methodology.

| test_id | engine | version | real_device | result | notes |
|---|---|---|---|---|---|
| slnt-axis-activation | chrome | 153.0.8010.37 | no (emulated/Playwright) | pass | wpt run, official runner, system Chrome via --binary |
| independence | chrome | 153.0.8010.37 | no (emulated/Playwright) | pass | wpt run, official runner, system Chrome via --binary |
| italic-no-extra-synthesis | chrome | 153.0.8010.37 | no (emulated/Playwright) | fail | wpt run, official runner, system Chrome via --binary — reproduces WebKit #209565's documented ital-axis spurious-synthesis failure; see docs/findings.md |
| slnt-axis-activation | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system Firefox via --binary |
| independence | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system Firefox via --binary |
| italic-no-extra-synthesis | firefox | 156.0 | no (emulated/Playwright) | pass | wpt run, official runner, system Firefox via --binary |

`result` ∈ `pass` / `fail` / `synthesis-fallback` / `untested`.
`real_device` ∈ `yes` / `no (emulated/Playwright)`.
