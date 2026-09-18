"""Generate site/index.html (from site/template.html) and the intermediate
site/src/data/cards.json, the small curated dataset the page is built from.
Reads docs/coverage.json, results/upstream.json, and
results/browser-matrix.md; never the other way around. This is a distinct,
hand-curated schema (a handful of category cards, plain language, ~20-word
"why it matters"), not a pass-through of those verbose sources — same
discipline as scripts/render-coverage-docs.py.

The site has no client-side interactivity, so all markup — including the
per-test detail rows revealed by each category's <details>/<summary> — is
rendered here at build time, not by JS in the browser. Vite only
bundles/hashes the stylesheet.

TEST_CATEGORY assigns every one of docs/coverage.json's 37 cataloged
upstream tests to exactly one of 5 buckets (explicit angle/range,
auto-derived range, stretch/weight/style precedence, synthesis/parsing/
inheritance, ital-axis). docs/coverage.json has no existing "card group"
concept, so this script is the one place that decision is made — it fails
loudly if coverage.json ever adds/removes a test without this mapping being
updated to match, since a silent mismatch here would misrepresent status on
the public site.

Category-level pass/fail badges are computed from the FULL set of tests in
each bucket, not a cherry-picked subset — a category is only shown clean if
every one of its tests currently passes on that engine.

Usage (from repo root):
  uv run scripts/generate-site-data.py
"""

import html
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COVERAGE_PATH = REPO_ROOT / "docs" / "coverage.json"
UPSTREAM_PATH = REPO_ROOT / "results" / "upstream.json"
MATRIX_PATH = REPO_ROOT / "results" / "browser-matrix.md"
CARDS_JSON_PATH = REPO_ROOT / "site" / "src" / "data" / "cards.json"
TEMPLATE_PATH = REPO_ROOT / "site" / "template.html"
SITE_HTML_PATH = REPO_ROOT / "site" / "index.html"

STATUS_MAP = {"PASS": "pass", "OK": "pass", "FAIL": "fail", "ERROR": "fail",
              "TIMEOUT": "fail", "CRASH": "fail", "pass": "pass", "fail": "fail"}

WPT_GITHUB_BASE = "https://github.com/web-platform-tests/wpt/blob/master/"

# Every path here must exist in docs/coverage.json's `tests` array, and every
# path in that array must appear here exactly once — checked at load time.
TEST_CATEGORY = {
    # explicit-angle-range: explicit <angle>/range values, either via
    # font-style or a direct slnt/ital font-variation-settings value.
    "css/css-fonts/variations/slnt-variable.html": "explicit-angle-range",
    "css/css-fonts/variations/slnt-backslant-variable.html": "explicit-angle-range",
    "css/css-fonts/variations/font-slant-1.html": "explicit-angle-range",
    "css/css-fonts/variations/font-slant-2a.html": "explicit-angle-range",
    "css/css-fonts/variations/font-slant-2b.html": "explicit-angle-range",
    "css/css-fonts/variations/font-slant-2c.html": "explicit-angle-range",
    "css/css-fonts/font-variation-settings-descriptor-01.html": "explicit-angle-range",
    "css/css-fonts/matching/range-descriptor-reversed.html": "explicit-angle-range",
    "css/css-fonts/variations/font-descriptor-range-reversed.html": "explicit-angle-range",
    "css/css-fonts/variations/font-descriptor-range-reversed-002.html": "explicit-angle-range",
    "css/css-fonts/variations/font-parse-numeric-stretch-style-weight.html": "explicit-angle-range",
    "css/css-fonts/font-face-range-order.html": "explicit-angle-range",
    "css/css-fonts/variations/font-shorthand.html": "explicit-angle-range",
    # auto-derived-range: no explicit @font-face font-style descriptor.
    "css/css-fonts/font-face-style-auto-variable.html": "auto-derived-range",
    "css/css-fonts/font-face-style-default-variable.html": "auto-derived-range",
    "css/css-fonts/synthetic-oblique-out-of-capabilities-range.html": "auto-derived-range",
    # precedence: face selection among multiple candidates (stretch/weight/
    # style search direction and distance, italic-vs-oblique fallback).
    "css/css-fonts/italic-oblique-fallback.html": "precedence",
    "css/css-fonts/oblique-last-resort-weight-selection.html": "precedence",
    "css/css-fonts/oblique-request-italic-only-family-no-crash.html": "precedence",
    "css/css-fonts/matching/style-ranges-over-weight-direction.html": "precedence",
    "css/css-fonts/matching/fixed-stretch-style-over-weight.html": "precedence",
    "css/css-fonts/matching/stretch-distance-over-weight-distance.html": "precedence",
    # synthesis-parsing-inheritance: generic machinery — synthesis fallback,
    # parsing-only tests, animation/interpolation, inheritance.
    "css/css-fonts/variations/font-slant-3.html": "synthesis-parsing-inheritance",
    "css/css-fonts/variations/at-font-face-font-matching.html": "synthesis-parsing-inheritance",
    "css/css-fonts/variations/font-style-parsing.html": "synthesis-parsing-inheritance",
    "css/css-fonts/variations/font-style-interpolation.html": "synthesis-parsing-inheritance",
    "css/css-fonts/animations/font-style-interpolation.html": "synthesis-parsing-inheritance",
    "css/css-fonts/parsing/font-variation-settings-valid.html": "synthesis-parsing-inheritance",
    "css/css-fonts/font-style-angle.html": "synthesis-parsing-inheritance",
    "css/css-fonts/font-style-sign-function.html": "synthesis-parsing-inheritance",
    "css/css-fonts/test-synthetic-italic.html": "synthesis-parsing-inheritance",
    "css/css-fonts/test-synthetic-italic-2.html": "synthesis-parsing-inheritance",
    "css/css-fonts/test-synthetic-italic-3.html": "synthesis-parsing-inheritance",
    "css/css-fonts/font-synthesis-style.html": "synthesis-parsing-inheritance",
    "css/css-fonts/font-synthesis-style-oblique-only.html": "synthesis-parsing-inheritance",
    "css/css-fonts/font-synthesis-style-binary.html": "synthesis-parsing-inheritance",
    "css/css-fonts/variations/font-variation-settings-inherit.html": "synthesis-parsing-inheritance",
    # ital-axis: deliberately empty — see docs/coverage.json's ital_axis_gap.
}

# Short tags for docs/coverage.json's checklist_mapping items, keyed by the
# item's exact text there — used as small per-test-row labels, not the full
# checklist sentence.
CHECKLIST_SHORT_LABELS = {
    "font-style: oblique matching a variable slnt axis": "slnt matching",
    "Explicit oblique <angle> matching": "explicit angle",
    "font-style ranges declared in @font-face": "style ranges",
    "Bare oblique / default-angle (14deg) matching": "bare/default angle",
    "italic vs oblique resolution differences": "italic vs oblique",
    "italic on a font with only an ital axis (no slnt) — sets ital=1": "ital-only italic",
    "oblique on a font with only an ital axis — must NOT touch ital (per #12836)": "ital/slnt independence",
    "Font exposing both slnt and ital — confirms independence per #12836": "combined slnt+ital",
    "Single variable face covering normal + oblique": "single face normal+oblique",
    "Separate normal/oblique faces (ambiguous-match hazard)": "separate faces hazard",
    "Font synthesis fallback behavior (font-synthesis)": "synthesis fallback",
    "Explicit font-variation-settings: 'slnt' <val> / 'ital' <val>": "explicit slnt/ital value",
    "font-style + explicit axis value paired (recommended pattern)": "style+axis pairing",
    "Ancestor font-variation-settings inheritance/replacement behavior": "inheritance",
}


def load_coverage():
    return json.loads(COVERAGE_PATH.read_text())


def load_upstream():
    data = json.loads(UPSTREAM_PATH.read_text())
    by_path = {t["path"]: t["results"] for t in data["tests"]}
    return data, by_path


def load_matrix_results():
    """Parse results/browser-matrix.md's fixed-schema table into
    {test_id: {engine: latest_result}}. Later rows for the same
    (test_id, engine) overwrite earlier ones, since record-results.py
    appends new runs rather than replacing old rows."""
    rows = {}
    for line in MATRIX_PATH.read_text().splitlines():
        if not line.startswith("|") or line.startswith("|---") or "test_id" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        test_id, engine, _version, _real_device, result = cells[:5]
        rows.setdefault(test_id, {})[engine] = result
    return rows


def build_checklist_index(coverage: dict) -> dict:
    """{test_path: [short_label, ...]} reverse index of coverage.json's
    checklist_mapping, so each rendered test row can show which checklist
    item(s) it covers."""
    index = {}
    for item in coverage["checklist_mapping"]["items"]:
        label = CHECKLIST_SHORT_LABELS.get(item["item"], item["item"][:40])
        for path in item.get("tests", []):
            index.setdefault(path, []).append(label)
    return index


def verify_category_mapping(coverage: dict):
    catalog_paths = {t["path"] for t in coverage["tests"]}
    mapped_paths = set(TEST_CATEGORY)
    missing = catalog_paths - mapped_paths
    extra = mapped_paths - catalog_paths
    if missing:
        raise RuntimeError(
            f"generate-site-data: {len(missing)} path(s) in docs/coverage.json "
            f"have no TEST_CATEGORY entry: {sorted(missing)}"
        )
    if extra:
        raise RuntimeError(
            f"generate-site-data: TEST_CATEGORY has {len(extra)} path(s) not "
            f"in docs/coverage.json (stale mapping?): {sorted(extra)}"
        )


def matrix_status(test_id, matrix_by_id, engine):
    if test_id not in matrix_by_id:
        raise RuntimeError(
            f"generate-site-data: test_id {test_id!r} not found in "
            f"{MATRIX_PATH} — has it been run and recorded yet?"
        )
    result = matrix_by_id[test_id].get(engine, "not-run")
    return STATUS_MAP.get(result, "not-run" if result == "not-run" else "unknown")


def category_engine_counts(paths, upstream_by_path):
    """{engine: (pass_count, total)} across every test path in a category."""
    counts = {"chrome": [0, 0], "firefox": [0, 0], "safari": [0, 0]}
    for path in paths:
        if path not in upstream_by_path:
            raise RuntimeError(
                f"generate-site-data: path {path!r} not found in "
                f"{UPSTREAM_PATH} — re-run scripts/sync-wpt-results.py first"
            )
        for engine in counts:
            status = STATUS_MAP.get(upstream_by_path[path][engine]["status"], "unknown")
            counts[engine][1] += 1
            if status == "pass":
                counts[engine][0] += 1
    return {e: tuple(v) for e, v in counts.items()}


UPSTREAM_CATEGORIES = [
    {
        "id": "explicit-angle-range",
        "plain_name": "Explicit angle & range matching",
        "one_liner": "font-style: oblique <angle> and declared @font-face ranges resolve correctly.",
        "why_it_matters": "The most common, well-tested case — but Safari fails one test here today (see detail).",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
    },
    {
        "id": "auto-derived-range",
        "plain_name": "Auto-derived range (explicit angles only)",
        "one_liner": "No explicit @font-face descriptor — matching against the font's own fvar-derived range, always with an explicit angle.",
        "why_it_matters": "Clean upstream, but none of these use the bare oblique/italic keyword — that specific case was the real gap, closed by this project (see the linked card).",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
        "cross_link": "auto-range-default-angle",
    },
    {
        "id": "precedence",
        "plain_name": "Stretch/weight/style matching precedence",
        "one_liner": "Search direction and distance among multiple candidate faces, plus italic/oblique fallback.",
        "why_it_matters": "Every engine fails at least one test in this category today — not just Safari (see detail for which).",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-matching",
    },
    {
        "id": "synthesis-parsing-inheritance",
        "plain_name": "Synthesis, parsing & inheritance",
        "one_liner": "font-synthesis fallback, oblique-angle parsing, animation, and font-variation-settings inheritance.",
        "why_it_matters": "Generic machinery oblique/ital matching depends on — several tests here fail on every engine too (see detail).",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-synthesis-style",
    },
    {
        "id": "ital-axis-upstream",
        "plain_name": "ital axis coverage",
        "one_liner": "No upstream WPT test exercises the OpenType ital variation axis at all.",
        "why_it_matters": "Confirmed by a full-tree search, not sampling — the reason this project's own tests exist.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
        "empty_state": True,
    },
]

THIS_REPO_CARDS = [
    {
        "id": "slnt-axis-activation",
        "plain_name": "slnt axis activates on oblique request",
        "one_liner": "font-style: oblique on a variable font sets the slnt axis.",
        "why_it_matters": "Baseline sanity check the rest of this project's tests build on.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
        "tier": 1,
        "test_id": "slnt-axis-activation",
        "test_file": "tests/font-style-oblique/slnt-axis-activation.html",
    },
    {
        "id": "auto-range-default-angle",
        "plain_name": "Auto-derived range + bare oblique/italic",
        "one_liner": "Bare font-style: oblique against a font with no explicit descriptor, range excludes the UA default angle.",
        "why_it_matters": "Closes the real gap this project exists to close — Cairo's motivating bug shape, generalized.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
        "tier": 1,
        "test_id": "auto-range-default-angle",
        "test_file": "tests/font-style-oblique/auto-range-default-angle.html",
    },
    {
        "id": "italic-no-extra-synthesis",
        "plain_name": "italic on an ital-only font doesn't over-synthesize",
        "one_liner": "italic on a font with only an ital axis (no slnt) sets ital, doesn't also fake-slant.",
        "why_it_matters": "Chrome fails this today — a live, reproducing instance of WebKit #209565's documented failure mode.",
        "spec_link": "https://github.com/w3c/csswg-drafts/issues/12836",
        "tier": 1,
        "test_id": "italic-no-extra-synthesis",
        "test_file": "tests/ital-axis/italic-no-extra-synthesis.html",
        "badge": "candidate-for-upstreaming",
    },
    {
        "id": "ital-slnt-independence",
        "plain_name": "ital and slnt are independent axes",
        "one_liner": "oblique on an ital-only font must not touch ital, per #12836's resolution.",
        "why_it_matters": "Directly tests the spec ambiguity (#12836) this project's ital-axis work is built on.",
        "spec_link": "https://github.com/w3c/csswg-drafts/issues/12836",
        "tier": 1,
        "test_id": "independence",
        "test_file": "tests/ital-axis/independence.html",
        "badge": "candidate-for-upstreaming",
    },
    {
        "id": "normal-plus-bare-oblique-same-family",
        "plain_name": "normal + bare oblique face, same family",
        "one_liner": "An angled request must pick the oblique face, not fall back to the upright normal face.",
        "why_it_matters": "vizchitra-fonts ships two separate @font-face blocks specifically to dodge this untested hazard.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-matching",
        "tier": 2,
        "planned": True,
    },
    {
        "id": "font-style-plus-explicit-axis-pairing",
        "plain_name": "font-style paired with an explicit axis override",
        "one_liner": "The spec's own recommended author pattern for fallback compatibility, currently unverified.",
        "why_it_matters": "Anyone following the spec's own compatibility advice is on unverified ground.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-variation-settings-def",
        "tier": 2,
        "planned": True,
    },
    {
        "id": "combined-slnt-ital-font",
        "plain_name": "A font exposing both slnt and ital",
        "one_liner": "The strongest direct test of #12836's independence claim needs one font with both axes.",
        "why_it_matters": "No known real-world font combines both — spec-completeness, not real-world impact evidence.",
        "spec_link": "https://github.com/w3c/csswg-drafts/issues/12836",
        "tier": 3,
        "planned": True,
    },
]

STATUS_LABEL = {"pass": "PASS", "fail": "FAIL", "unknown": "?", "not-run": "not run"}
BADGE_LABEL = {
    "closed-by-this-project": "closed by this project",
    "candidate-for-upstreaming": "candidate for upstreaming — no PR yet",
    "planned": "planned, not yet written",
}


def engine_badge_label(engine_failures: set) -> tuple[str, str] | None:
    """Auto-computed category-level badge id/label from which engines have
    at least one failing test, so the badge always matches the full
    category count rather than a hand-picked headline engine."""
    if not engine_failures:
        return None
    if engine_failures == {"safari"}:
        return "safari-only-failure", "Safari-only failure"
    if engine_failures == {"chrome"}:
        return "chrome-only-failure", "Chrome-only failure"
    if engine_failures == {"firefox"}:
        return "firefox-only-failure", "Firefox-only failure"
    engines = "/".join(sorted(engine_failures, key=["chrome", "firefox", "safari"].index))
    return "cross-engine-failure", f"{engines} all have failing tests here"


def render_test_row(test: dict, upstream_by_path: dict, checklist_index: dict,
                     run_metadata: dict) -> str:
    e = html.escape
    path = test["path"]
    result = upstream_by_path[path]
    query = "&".join(f"run_id={run_metadata[eng]['id']}" for eng in ("chrome", "firefox", "safari"))
    wpt_fyi_url = f"https://wpt.fyi/results/{path}?{query}"
    parts = ['<div class="test-row">']
    parts.append(
        f'<a class="test-path" href="{e(WPT_GITHUB_BASE + path)}"><code>{e(path)}</code></a>'
    )
    parts.append(f'<p class="test-assertion" title="{e(test["notes"][:300])}">{e(test["title"])}</p>')
    parts.append('<div class="engines">')
    for engine in ("chrome", "firefox", "safari"):
        status = STATUS_MAP.get(result[engine]["status"], "unknown")
        label = STATUS_LABEL.get(status, status)
        parts.append(f'<span class="engine engine-{e(status)}">{e(engine)}: {e(label)}</span>')
    parts.append("</div>")
    tags = checklist_index.get(path, [])
    if tags:
        parts.append('<div class="checklist-tags">')
        for tag in tags:
            parts.append(f'<span class="tag">{e(tag)}</span>')
        parts.append("</div>")
    parts.append(f'<a class="wpt-fyi-link" href="{e(wpt_fyi_url)}">wpt.fyi result &rarr;</a>')
    parts.append("</div>")
    return "".join(parts)


def build_upstream_cards(coverage: dict, upstream_by_path: dict, run_metadata: dict,
                          checklist_index: dict):
    tests_by_path = {t["path"]: t for t in coverage["tests"]}
    cards = []
    for cat in UPSTREAM_CATEGORIES:
        card = {
            "id": cat["id"], "plain_name": cat["plain_name"], "one_liner": cat["one_liner"],
            "why_it_matters": cat["why_it_matters"], "spec_link": cat["spec_link"],
            "section": "upstream",
        }
        if cat.get("cross_link"):
            card["cross_link"] = cat["cross_link"]

        paths = sorted(p for p, c in TEST_CATEGORY.items() if c == cat["id"])
        if cat.get("empty_state") or not paths:
            card["results"] = None
            card["test_count"] = 0
            card["detail_html"] = ""
        else:
            counts = category_engine_counts(paths, upstream_by_path)
            card["results"] = {
                e: ("pass" if c[0] == c[1] else "fail") for e, c in counts.items()
            }
            card["result_counts"] = {e: f"{c[0]}/{c[1]}" for e, c in counts.items()}
            card["test_count"] = len(paths)
            failing_engines = {e for e, c in counts.items() if c[0] < c[1]}
            badge = engine_badge_label(failing_engines)
            if badge:
                card["badge"] = badge[0]
                BADGE_LABEL.setdefault(badge[0], badge[1])
            card["detail_html"] = "".join(
                render_test_row(tests_by_path[p], upstream_by_path, checklist_index, run_metadata)
                for p in paths
            )
        cards.append(card)
    return cards


def build_this_repo_cards(matrix_by_id):
    cards = []
    for c in THIS_REPO_CARDS:
        card = {
            "id": c["id"], "plain_name": c["plain_name"], "one_liner": c["one_liner"],
            "why_it_matters": c["why_it_matters"], "spec_link": c["spec_link"],
            "section": "this-repo", "tier": c["tier"],
        }
        if c.get("planned"):
            card["results"] = None
            card["badge"] = "planned"
        else:
            card["results"] = {
                "chrome": matrix_status(c["test_id"], matrix_by_id, "chrome"),
                "firefox": matrix_status(c["test_id"], matrix_by_id, "firefox"),
                "safari": matrix_status(c["test_id"], matrix_by_id, "safari"),
            }
            card["test_file"] = c["test_file"]
            if c.get("badge"):
                card["badge"] = c["badge"]
        cards.append(card)
    return cards


def render_card_html(card: dict) -> str:
    e = html.escape
    parts = [f'<article class="card" id="card-{e(card["id"])}">']
    parts.append(f'<h3>{e(card["plain_name"])}</h3>')
    parts.append(f'<p class="one-liner">{e(card["one_liner"])}</p>')

    if card["results"] is not None:
        parts.append('<div class="engines">')
        for engine in ("chrome", "firefox", "safari"):
            status = card["results"][engine]
            counts = card.get("result_counts", {}).get(engine)
            label = counts if (counts and status == "fail") else STATUS_LABEL.get(status, status)
            parts.append(
                f'<span class="engine engine-{e(status)}">{e(engine)}: {e(label)}</span>'
            )
        parts.append("</div>")
    else:
        empty_text = "Not yet written" if card.get("badge") == "planned" \
            else "0 upstream tests — confirmed by full-tree search"
        parts.append(f'<p class="empty-state">{e(empty_text)}</p>')

    if card.get("badge"):
        label = BADGE_LABEL.get(card["badge"], card["badge"])
        parts.append(f'<span class="badge badge-{e(card["badge"])}">{e(label)}</span>')

    parts.append(f'<p class="why-it-matters">{e(card["why_it_matters"])}</p>')

    links = [f'<a href="{e(card["spec_link"])}">spec</a>']
    if card.get("test_file"):
        url = f'https://github.com/amitkaps/oblique/blob/main/{card["test_file"]}'
        links.append(f'<a href="{e(url)}">test file</a>')
    if card.get("cross_link"):
        links.append(
            f'<a href="#card-{e(card["cross_link"])}">see how it was closed &rarr;</a>'
        )
    parts.append(f'<p class="card-links">{" &middot; ".join(links)}</p>')

    if card.get("detail_html"):
        parts.append(
            f'<details class="test-detail"><summary>Show {card["test_count"]} '
            f'individual test{"s" if card["test_count"] != 1 else ""}</summary>'
            f'<div class="test-list">{card["detail_html"]}</div></details>'
        )

    parts.append("</article>")
    return "".join(parts)


def main():
    if not UPSTREAM_PATH.exists():
        print(f"generate-site-data: {UPSTREAM_PATH} missing — run "
              f"scripts/sync-wpt-results.py first", file=sys.stderr)
        sys.exit(1)
    if not TEMPLATE_PATH.exists():
        print(f"generate-site-data: {TEMPLATE_PATH} missing", file=sys.stderr)
        sys.exit(1)

    coverage = load_coverage()
    verify_category_mapping(coverage)
    upstream_data, upstream_by_path = load_upstream()
    matrix_by_id = load_matrix_results()
    checklist_index = build_checklist_index(coverage)

    upstream_cards = build_upstream_cards(
        coverage, upstream_by_path, upstream_data["run_metadata"], checklist_index
    )
    this_repo_cards = build_this_repo_cards(matrix_by_id)

    # cards.json is an intermediate artifact for inspection/debugging, not
    # consumed by the page itself (rendered directly to HTML below) — drop
    # the pre-rendered detail_html blob from it to keep it readable.
    json_cards = [{k: v for k, v in c.items() if k != "detail_html"}
                  for c in upstream_cards + this_repo_cards]
    data = {
        "generated_note": "Generated by scripts/generate-site-data.py from "
                           "docs/coverage.json, results/upstream.json, and "
                           "results/browser-matrix.md — do not hand-edit.",
        "upstream_synced_at": upstream_data["synced_at"],
        "cards": json_cards,
    }
    CARDS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    CARDS_JSON_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"generate-site-data: wrote {len(data['cards'])} card(s) to {CARDS_JSON_PATH}")

    synced_label = f"Upstream results last synced {upstream_data['synced_at'][:16].replace('T', ' ')} UTC"
    page = TEMPLATE_PATH.read_text()
    page = page.replace("<!--SYNCED_BANNER-->", html.escape(synced_label))
    page = page.replace(
        "<!--CARDS_UPSTREAM-->", "".join(render_card_html(c) for c in upstream_cards)
    )
    page = page.replace(
        "<!--CARDS_THIS_REPO-->", "".join(render_card_html(c) for c in this_repo_cards)
    )
    SITE_HTML_PATH.write_text(page)
    print(f"generate-site-data: wrote {SITE_HTML_PATH}")


if __name__ == "__main__":
    main()
