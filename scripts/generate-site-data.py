"""Generate site/index.html (from site/template.html) and the intermediate
site/src/data/cards.json, the small curated dataset the page is built from.
Reads docs/coverage.json, results/upstream.json, and
results/browser-matrix.md; never the other way around. This is a distinct,
hand-curated schema (a handful of cards, plain language, ~20-word "why it
matters"), not a pass-through of those verbose sources — same discipline as
scripts/render-coverage-docs.py.

The site has no client-side interactivity (no filters/toggles), so the card
markup is rendered here at build time, not by JS in the browser — the page
ships as plain static HTML, with Vite only bundling/hashing the stylesheet.

The card groupings (which upstream test paths represent which classification,
which this-repo tests belong to which tier) are hardcoded below: docs/coverage.json
has no existing "card group" concept, so this script is the one place that
decision is made, and it fails loudly if a path/id it expects to find is
missing from the source JSON — a silent mismatch here would misrepresent
status on the public site.

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


def load_upstream_results():
    data = json.loads(UPSTREAM_PATH.read_text())
    by_path = {t["path"]: t["results"] for t in data["tests"]}
    return by_path, data["synced_at"]


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


def aggregate_status(paths, upstream_by_path):
    """Worst-case per-engine status across a group of upstream test paths."""
    out = {"chrome": "pass", "firefox": "pass", "safari": "pass"}
    for path in paths:
        if path not in upstream_by_path:
            raise RuntimeError(
                f"generate-site-data: path {path!r} not found in "
                f"{UPSTREAM_PATH} — re-run scripts/sync-wpt-results.py first"
            )
        for engine in out:
            status = STATUS_MAP.get(upstream_by_path[path][engine]["status"], "unknown")
            if status == "fail":
                out[engine] = "fail"
            elif status == "unknown" and out[engine] == "pass":
                out[engine] = "unknown"
    return out


def matrix_status(test_id, matrix_by_id, engine):
    if test_id not in matrix_by_id:
        raise RuntimeError(
            f"generate-site-data: test_id {test_id!r} not found in "
            f"{MATRIX_PATH} — has it been run and recorded yet?"
        )
    result = matrix_by_id[test_id].get(engine, "not-run")
    return STATUS_MAP.get(result, "not-run" if result == "not-run" else "unknown")


UPSTREAM_CARDS = [
    {
        "id": "explicit-angle-range",
        "plain_name": "Explicit angle & range matching",
        "one_liner": "font-style: oblique <angle> and declared @font-face ranges resolve correctly.",
        "why_it_matters": "The most common, well-tested case — authors explicitly setting angles or descriptor ranges.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
        "paths": [
            "css/css-fonts/variations/font-slant-1.html",
            "css/css-fonts/variations/font-slant-2a.html",
            "css/css-fonts/variations/font-slant-2b.html",
            "css/css-fonts/variations/font-slant-2c.html",
            "css/css-fonts/variations/font-descriptor-range-reversed.html",
            "css/css-fonts/variations/font-descriptor-range-reversed-002.html",
        ],
    },
    {
        "id": "auto-range-default-angle-upstream",
        "plain_name": "Auto-derived range + bare oblique/italic",
        "one_liner": "No explicit descriptor — matching against the font's own fvar-derived range.",
        "why_it_matters": "Was a real gap (Cairo's shape) until this project closed it — see the matching card below.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-prop",
        "paths": ["css/css-fonts/font-face-style-auto-variable.html"],
        "badge": "closed-by-this-project",
        "cross_link": "auto-range-default-angle",
    },
    {
        "id": "stretch-weight-style-precedence",
        "plain_name": "Stretch/weight/style matching precedence",
        "one_liner": "Search direction and distance among multiple oblique candidate faces.",
        "why_it_matters": "Safari fails all three of these upstream tests today — a live, dated, cross-engine divergence.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-style-matching",
        "paths": [
            "css/css-fonts/matching/style-ranges-over-weight-direction.html",
            "css/css-fonts/matching/fixed-stretch-style-over-weight.html",
            "css/css-fonts/matching/stretch-distance-over-weight-distance.html",
        ],
        "badge": "safari-only-failure",
    },
    {
        "id": "synthesis-parsing-inheritance",
        "plain_name": "Synthesis, parsing & inheritance",
        "one_liner": "font-synthesis fallback, oblique-angle parsing, and font-variation-settings inheritance.",
        "why_it_matters": "Generic machinery oblique/ital matching depends on — not axis-specific, but a prerequisite.",
        "spec_link": "https://drafts.csswg.org/css-fonts-4/#font-synthesis-style",
        "paths": [
            "css/css-fonts/font-synthesis-style.html",
            "css/css-fonts/font-synthesis-style-binary.html",
            "css/css-fonts/variations/font-variation-settings-inherit.html",
        ],
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
        "engine_source": "matrix",
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
        "engine_source": "matrix",
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
        "engine_source": "matrix",
        "test_id": "italic-no-extra-synthesis",
        "test_file": "tests/ital-axis/italic-no-extra-synthesis.html",
        "badge": "proposed-for-upstreaming",
    },
    {
        "id": "ital-slnt-independence",
        "plain_name": "ital and slnt are independent axes",
        "one_liner": "oblique on an ital-only font must not touch ital, per #12836's resolution.",
        "why_it_matters": "Directly tests the spec ambiguity (#12836) this project's ital-axis work is built on.",
        "spec_link": "https://github.com/w3c/csswg-drafts/issues/12836",
        "tier": 1,
        "engine_source": "matrix",
        "test_id": "independence",
        "test_file": "tests/ital-axis/independence.html",
        "badge": "proposed-for-upstreaming",
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


def build_upstream_cards(upstream_by_path):
    cards = []
    for c in UPSTREAM_CARDS:
        card = {
            "id": c["id"], "plain_name": c["plain_name"], "one_liner": c["one_liner"],
            "why_it_matters": c["why_it_matters"], "spec_link": c["spec_link"],
            "section": "upstream",
        }
        if c.get("empty_state"):
            card["results"] = None
        else:
            card["results"] = aggregate_status(c["paths"], upstream_by_path)
        if c.get("badge"):
            card["badge"] = c["badge"]
        if c.get("cross_link"):
            card["cross_link"] = c["cross_link"]
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


STATUS_LABEL = {"pass": "PASS", "fail": "FAIL", "unknown": "?", "not-run": "not run"}
BADGE_LABEL = {
    "closed-by-this-project": "closed by this project",
    "safari-only-failure": "Safari-only failure",
    "proposed-for-upstreaming": "proposed for upstreaming",
    "planned": "planned, not yet written",
}


def render_card_html(card: dict) -> str:
    e = html.escape
    parts = [f'<article class="card" id="card-{e(card["id"])}">']
    parts.append(f'<h3>{e(card["plain_name"])}</h3>')
    parts.append(f'<p class="one-liner">{e(card["one_liner"])}</p>')

    if card["results"] is not None:
        parts.append('<div class="engines">')
        for engine in ("chrome", "firefox", "safari"):
            status = card["results"][engine]
            label = STATUS_LABEL.get(status, status)
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

    upstream_by_path, synced_at = load_upstream_results()
    matrix_by_id = load_matrix_results()

    upstream_cards = build_upstream_cards(upstream_by_path)
    this_repo_cards = build_this_repo_cards(matrix_by_id)

    data = {
        "generated_note": "Generated by scripts/generate-site-data.py from "
                           "docs/coverage.json, results/upstream.json, and "
                           "results/browser-matrix.md — do not hand-edit.",
        "upstream_synced_at": synced_at,
        "cards": upstream_cards + this_repo_cards,
    }
    CARDS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    CARDS_JSON_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"generate-site-data: wrote {len(data['cards'])} card(s) to {CARDS_JSON_PATH}")

    synced_label = f"Upstream results last synced {synced_at[:16].replace('T', ' ')} UTC"
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
