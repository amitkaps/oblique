"""Render docs/coverage.md and results/upstream-matrix.md from their JSON
sources (docs/coverage.json, results/upstream.json). Both markdown files are
generated output — edit the JSON, then re-run this script; don't hand-edit
the markdown, same discipline as scripts/record-results.py.

Usage (from repo root):
  uv run scripts/render-coverage-docs.py
"""

from pathlib import Path
import json
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
COVERAGE_PATH = REPO_ROOT / "docs" / "coverage.json"
UPSTREAM_JSON_PATH = REPO_ROOT / "results" / "upstream.json"
COVERAGE_MD_PATH = REPO_ROOT / "docs" / "coverage.md"
UPSTREAM_MD_PATH = REPO_ROOT / "results" / "upstream-matrix.md"
DASHBOARD_DATA_DIR = REPO_ROOT / "docs" / "data"


def render_coverage_md(coverage: dict) -> str:
    lines = [
        "# WPT coverage catalog: oblique / slnt / ital",
        "",
        "Generated from `docs/coverage.json` by "
        "`scripts/render-coverage-docs.py` — do not hand-edit.",
        "",
        f"Audited {coverage['audited_at']}. Method: {coverage['audit_method']}",
        "",
        "This catalogs every existing upstream WPT test that exercises "
        "oblique/slnt/ital matching, synthesis, or closely related "
        "parsing/animation, found by walking the vendored `css/css-fonts` "
        "tree directly (not by search-snippet sampling). Live pass/fail per "
        "engine, sourced from wpt.fyi, is in "
        "[`results/upstream-matrix.md`](../results/upstream-matrix.md) — "
        "kept separate because that data is refreshed on a schedule and "
        "this catalog is not.",
        "",
        "| Path | Axis | Probes #209565? | Assertion |",
        "|---|---|---|---|",
    ]
    for t in coverage["tests"]:
        probes = "yes" if t["probes_209565"] else "no"
        lines.append(
            f"| `{t['path']}` | {t['axis']} | {probes} | {t['title']} |"
        )

    gap = coverage["ital_axis_gap"]
    lines += [
        "",
        "## The `ital`-axis gap",
        "",
        f"**{gap['claim']}**",
        "",
        f"Verified {gap['verified_at']}. Search method: {gap['search_method']}",
        "",
        f"Result: {gap['result']}",
        "",
        "This is the confirmed, current scope of this repo's own novel "
        "tests (`tests/ital-axis/`) — not duplicating upstream coverage, "
        "filling a real gap in it.",
        "",
    ]

    mapping = coverage.get("checklist_mapping")
    if mapping:
        lines += [
            "## Coverage checklist status",
            "",
            "Cross-references every item in `docs/spec.md`'s 14-item "
            "\"Coverage checklist\" against actual coverage — upstream WPT "
            "tests, this repo's own tests, or neither. Broader than the "
            "`probes_209565` flag above: an item can be fully covered "
            "without any single test specifically probing #209565's "
            "documented failure modes.",
            "",
            f"Audited {mapping['audited_at']}.",
            "",
            "| Checklist item | Status | Test(s) |",
            "|---|---|---|",
        ]
        status_labels = {
            "covered-upstream": "✅ covered (upstream WPT)",
            "covered-by-this-repo-only": "🟡 covered (this repo only)",
            "partially-covered-upstream": "🟡 partial (upstream WPT)",
            "gap": "❌ gap",
        }
        for entry in mapping["items"]:
            status = status_labels.get(entry["status"], entry["status"])
            test_list = (
                "<br>".join(f"`{t}`" for t in entry["tests"])
                if entry["tests"]
                else "—"
            )
            row = f"| {entry['item']} | {status} | {test_list} |"
            lines.append(row)
            if entry.get("notes"):
                lines.append(f"| | | _{entry['notes']}_ |")
        lines.append("")

    return "\n".join(lines)


def render_upstream_md(upstream: dict | None) -> str:
    lines = [
        "# Upstream WPT results (wpt.fyi-sourced)",
        "",
        "Generated from `results/upstream.json` by "
        "`scripts/render-coverage-docs.py` — do not hand-edit.",
        "",
        "**This table is wpt.fyi's own continuous-integration data for "
        "pre-existing upstream WPT tests catalogued in "
        "[`docs/coverage.md`](../docs/coverage.md), fetched via "
        "`scripts/sync-wpt-results.py`.** It is a separate data source from "
        "[`results/browser-matrix.md`](browser-matrix.md), which records "
        "only tests *this repo* ran locally via the official WPT runner. "
        "Never merge the two — one is \"we ran this ourselves,\" the other "
        "is \"wpt.fyi ran this continuously upstream,\" and conflating them "
        "misrepresents provenance.",
        "",
    ]

    if upstream is None:
        lines += [
            "**Not yet synced.** Run `uv run scripts/sync-wpt-results.py` "
            "then re-run this script.",
            "",
        ]
        return "\n".join(lines)

    versions = ", ".join(
        f"{p}: {m['browser_version']}"
        for p, m in upstream["run_metadata"].items()
    )
    lines += [
        f"**Last synced: {upstream['synced_at']}** ({versions}). If this "
        "timestamp looks old, the scheduled sync (see "
        "`.github/workflows/sync-wpt-results.yml`) may have stopped — "
        "treat stale data as unverified, not as current status.",
        "",
        "| Path | Chrome | Firefox | Safari |",
        "|---|---|---|---|",
    ]
    for t in upstream["tests"]:
        r = t["results"]
        lines.append(
            f"| `{t['path']}` | {r['chrome']['status']} | "
            f"{r['firefox']['status']} | {r['safari']['status']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    coverage = json.loads(COVERAGE_PATH.read_text())
    COVERAGE_MD_PATH.write_text(render_coverage_md(coverage))
    print(f"render-coverage-docs: wrote {COVERAGE_MD_PATH}")

    upstream = (
        json.loads(UPSTREAM_JSON_PATH.read_text())
        if UPSTREAM_JSON_PATH.exists()
        else None
    )
    UPSTREAM_MD_PATH.write_text(render_upstream_md(upstream))
    print(f"render-coverage-docs: wrote {UPSTREAM_MD_PATH}")

    # docs/dashboard/index.html fetches these as same-origin static files —
    # copied here (not fetched cross-folder) so a GitHub Pages deploy scoped
    # to docs/ (the common case) is self-contained.
    DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(COVERAGE_PATH, DASHBOARD_DATA_DIR / "coverage.json")
    if UPSTREAM_JSON_PATH.exists():
        shutil.copyfile(UPSTREAM_JSON_PATH, DASHBOARD_DATA_DIR / "upstream.json")
    print(f"render-coverage-docs: copied data files into {DASHBOARD_DATA_DIR}")


if __name__ == "__main__":
    main()
