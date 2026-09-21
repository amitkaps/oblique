// Renders one WPT reftest (plus references) per testable case, and the manifest that
// records what the reference expects for EVERY case, testable or not.
//
// Reftest semantics (web-platform-tests docs, "Multiple References"): with several links
// the test passes if at least one `match` reference matches AND every `mismatch`
// reference differs. So an allowed set of real outcomes becomes several match refs,
// and "anything but these" becomes mismatch refs.
//
// References never depend on the descriptor or the matching under test: each is a
// plain face with the axis PINNED through font-variation-settings, which 7.2 says wins.

import { cells, PREFIX } from "./cases.mjs";
import { describe, pinCss, token } from "./outcome.mjs";

const FONT_FAMILY = "Cairo Var OBLIQUE";
const STYLESHEET = `${PREFIX}.css`;

const esc = (s) => s.replaceAll("&", "&amp;").replaceAll("<", "&lt;");

function faceRule(matrix, descriptor) {
  const line = descriptor ? `\n    font-style: ${descriptor};` : "";
  return `  @font-face {
    font-family: "${FONT_FAMILY}";
    src: url('${matrix.font.file}');${line}
  }`;
}

function paragraph(cell, matrix) {
  const g = matrix.font.glyph;
  return `<p class="test" style="${cell.css}">${g}</p>`;
}

// One reference per outcome, shared by every test that needs it (WPT: "shared references are
// strongly encouraged"). The same file is a `match` for tests that allow the outcome and a
// `mismatch` for tests that forbid it.
export const refFile = (outcome) => `${PREFIX}-${token(outcome)}-ref.html`;

function refHtml(matrix, outcome) {
  return `<!DOCTYPE html>
<html lang="en">
<meta charset="utf-8">
<title>CSS Reference: ${describe(outcome)}</title>
<!--
  A plain face with the axis pinned through font-variation-settings, which wins over any
  style-derived variation (CSS Fonts 4 7.2), so this does not depend on the font-style
  descriptor or on the matching that the tests exercise.
-->
<link rel="stylesheet" href="${STYLESHEET}">
<style>
${faceRule(matrix, null)}
  .test {
    font-family: "${FONT_FAMILY}";
    font-size: ${matrix.font.fontSize};
    ${pinCss(outcome)}
  }
</style>

<p class="test">${matrix.font.glyph}</p>
`;
}

function testHtml(cell, matrix, refs) {
  const e = cell.expected;
  const allowed = e.allowed.map(describe).join("; ");
  const links = [
    `<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#font-style-matching">`,
    `<link rel="help" href="https://drafts.csswg.org/css-fonts-4/#font-synthesis-style">`,
    ...refs.map((r) => `<link rel="${r.kind}" href="${r.file}">`),
  ].join("\n");
  const rule = [
    e.plan.match.length ? `must render like one of: ${e.plan.match.map(describe).join(", ")}` : "",
    e.plan.mismatch.length ? `must NOT render like any of: ${e.plan.mismatch.map(describe).join(", ")}` : "",
  ].filter(Boolean).join("; ");
  const desc = cell.col.descriptor ? `font-style: ${cell.col.descriptor}` : "no font-style descriptor (auto)";
  const synthNote = cell.row.extraCss && /synthesis/.test(cell.row.extraCss)
    ? `The request also sets ${cell.row.extraCss}`
    : "font-synthesis is left at its default: a matched request must not be synthesized.";
  return `<!DOCTYPE html>
<html lang="en">
<meta charset="utf-8">
<title>CSS Test: ${esc(desc)} + ${esc(cell.row.lines.join(" "))}</title>
<!--
  @font-face ${desc}, request "${cell.row.request}". The reference algorithm permits: ${allowed}.
  ${e.why.join("\n  ")}${e.assumptions.length ? "\n  Assumption: " + e.assumptions.join("; ") : ""}
  ${synthNote}
-->
${links}
<meta name="assert"
  content="A face ${cell.col.descriptor ? `declared '${esc(desc)}'` : "with no font-style descriptor (auto)"}, requested with '${esc(cell.row.lines.join(" "))}', ${esc(rule)}.">
<link rel="stylesheet" href="${STYLESHEET}">
<style>
${faceRule(matrix, cell.col.descriptor)}
  .test {
    font-family: "${FONT_FAMILY}";
    font-size: ${matrix.font.fontSize};
  }
</style>

${paragraph(cell, matrix)}
`;
}

/** @returns {{files: Map<string,string>, manifest: object}} */
export function generate(matrix) {
  const files = new Map();
  const manifestCells = [];
  for (const cell of cells(matrix)) {
    const e = cell.expected;
    const refs = [
      ...e.plan.match.map((o) => ({ kind: "match", outcome: o, file: refFile(o) })),
      ...e.plan.mismatch.map((o) => ({ kind: "mismatch", outcome: o, file: refFile(o) })),
    ];
    const wpt = refs.length > 0;
    if (wpt) {
      files.set(`${cell.id}.html`, testHtml(cell, matrix, refs));
      for (const r of refs) if (!files.has(r.file)) files.set(r.file, refHtml(matrix, r.outcome));
    }
    manifestCells.push({
      address: cell.address,
      id: cell.id,
      row: cell.row.slug,
      column: cell.col.slug,
      request: cell.row.request,
      descriptor: cell.col.descriptor,
      css: cell.css,
      status: e.status,
      spec: e.spec,
      allowed: e.allowed,
      plan: e.plan,
      selected: e.selected,
      stage: e.stage,
      assumptions: e.assumptions,
      why: e.why,
      wpt,
      files: wpt ? [`${cell.id}.html`, ...refs.map((r) => r.file)] : [],
    });
  }
  const manifest = {
    _note: "GENERATED by reference/src/cli.mjs from reference/cases/matrix.json. Do not edit.",
    font: matrix.font,
    columns: matrix.columns,
    rows: matrix.rows,
    standalone: matrix.standalone ?? [],
    cells: manifestCells,
  };
  files.set("matrix.manifest.json", JSON.stringify(manifest, null, 2) + "\n");
  return { files, manifest };
}
