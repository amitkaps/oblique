// The site's coverage matrix, rendered to static HTML at build time (a Vite plugin).
//
// @font-face `font-style` descriptor (columns A, B, C...) x use-site request (rows 1, 2, 3...),
// one cell per pair, all against one font (Cairo subset, capital I).
//
// Everything about the grid comes from tests/oblique-style-matching/matrix.manifest.json,
// which reference/ generates from reference/cases/matrix.json: addresses, labels, what the
// reference algorithm expects in each cell, which cells have a WPT test. This file only reads
// that manifest and the recorded browser results; it never decides an expectation.
//
// Two kinds of cell (the manifest's `status`):
//   specified / constrained  the spec pins the outcome down enough for a WPT reftest. Circles
//                            show recorded reftest results (Chrome and Firefox from `wpt run`,
//                            Safari from scripts/safari-replay.py).
//   unspecified              the spec leaves it open: nothing to pass or fail. Circles show
//                            what each browser was MEASURED to do (results/survey.json).
//
// verifyMatrix() fails the build if the manifest, the tests on disk and the results disagree.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { ROOT, TESTS_DIR } from "../reference/src/cases.mjs";
import {
  leanLabel,
  loadManifest,
  loadSurvey,
  readBrowserMatrix,
  readEngineVersions,
} from "../reference/src/compare.mjs";

const FONT_FILE = join(TESTS_DIR, "resources", "Cairo.var.subset.ttf");
const TEST_URL_BASE = "https://github.com/amitkaps/oblique/blob/main/tests/oblique-style-matching/";
const SPECIMEN_WORD = "OBLIQUE";
const ENGINES = [
  { id: "chromium", key: "chrome", label: "Chromium" },
  { id: "firefox", key: "firefox", label: "Firefox" },
  { id: "safari", key: "safari", label: "Safari" },
];

const esc = (s) =>
  String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#x27;");

const isTestFile = (n) => n.endsWith(".html") && !/-(ref|notref)\.html$/.test(n);

function verifyMatrix(manifest, results) {
  const { columns, rows, cells } = manifest;
  if (cells.length !== columns.length * rows.length) throw new Error("site: the manifest is not exactly columns x rows");
  for (const cell of cells) {
    for (const name of cell.files) {
      if (!existsSync(join(TESTS_DIR, name)))
        throw new Error(`site: ${name} (cell ${cell.address}) is missing: run \`pnpm generate\``);
    }
    if (cell.wpt && !results[cell.id])
      throw new Error(`site: ${cell.id} (cell ${cell.address}) has no row in results/browser-matrix.md: run and record it first`);
  }
  const onDisk = new Set(readdirSync(TESTS_DIR).filter((n) => n.startsWith("matrix-") && isTestFile(n)).map((n) => n.slice(0, -5)));
  const expected = new Set(cells.filter((c) => c.wpt).map((c) => c.id));
  const extra = [...onDisk].filter((n) => !expected.has(n));
  const missing = [...expected].filter((n) => !onDisk.has(n));
  if (extra.length || missing.length)
    throw new Error(`site: matrix-* tests on disk disagree with the manifest: extra ${extra}, missing ${missing}`);
}

const reftestStatus = (results, id, key) => {
  const r = results[id]?.[key] ?? "not-run";
  return r === "pass" ? "pass" : r === "fail" ? "fail" : r === "not-run" ? "not-run" : "unknown";
};

const outcomeText = (o) => (o.kind === "upright" ? "upright" : o.kind === "synth" ? "synthesized skew" : `${o.axis} ${o.value}`);
const pinned = (o) => `font-variation-settings: 'slnt' ${o.kind === "upright" ? 0 : o.value};`;

function fontFaceCss(manifest) {
  return manifest.columns
    .map((c) => `@font-face { font-family: "ob-${c.slug}"; src: url("/Cairo.var.subset.ttf");${c.descriptor ? ` font-style: ${c.descriptor};` : ""} }`)
    .join("\n");
}

function specimen(manifest, cell) {
  const row = manifest.rows.find((r) => r.slug === cell.row);
  const col = manifest.columns.find((c) => c.slug === cell.column);
  const family = `font-family: 'ob-${col.slug}';`;
  const inner = row.em ? `<em>${SPECIMEN_WORD}</em>` : SPECIMEN_WORD;
  const test = `<span class="ov-test" style="${esc(`${family} ${cell.css}`)}">${inner}</span>`;
  const matches = cell.plan.match;
  if (!matches.length) return `<div class="overlap overlap-single">${test}</div>`; // the test can only say what it must not be
  // pink = the first reference the test would accept
  const ref = `<span class="ov-control" style="${esc(`${family} ${pinned(matches[0])}`)}">${SPECIMEN_WORD}</span>`;
  return `<div class="overlap">${ref}${test}</div>`;
}

function badges(manifest, survey, cell, perEngine) {
  const lis = ENGINES.map((eng) => {
    const status = perEngine[eng.key];
    const lean = survey.engines?.[eng.key]?.cells?.[cell.id];
    const label = lean == null ? null : leanLabel(lean, manifest.font);
    let cls, word;
    if (status === "observed") {
      cls = "observed";
      word = `observed: ${label}`;
    } else {
      cls = status === "pass" || status === "fail" ? status : "unknown";
      word = status === "pass" ? "pass" : status === "fail" ? "fail" : "not run";
      if (label && status === "fail") word += ` (measured: ${label})`;
    }
    return `<li class="b-badge ${cls}" title="${esc(`${eng.label}: ${word}`)}"><img class="logo" src="/browsers/${eng.id}.svg" alt="${esc(eng.label)}"></li>`;
  });
  return `<ul class="verdicts">${lis.join("")}</ul>`;
}

function cellStatus(cell, perEngine) {
  if (!cell.wpt) return "observed";
  const vals = new Set(Object.values(perEngine).filter((v) => v === "pass" || v === "fail"));
  if (vals.has("fail")) return "fail";
  return vals.size === 1 && vals.has("pass") ? "pass" : "unknown";
}

function renderMatrix(manifest, results, survey, versions) {
  const { columns, rows, cells } = manifest;
  const byAddr = Object.fromEntries(cells.map((c) => [c.address, c]));
  const perCell = {};
  for (const cell of cells) {
    perCell[cell.address] = Object.fromEntries(
      ENGINES.map((e) => [
        e.key,
        cell.wpt ? reftestStatus(results, cell.id, e.key) : survey.engines?.[e.key]?.cells?.[cell.id] != null ? "observed" : "not-run",
      ]),
    );
  }
  const tested = cells.filter((c) => c.wpt).length;
  const diverge = cells
    .filter((c) => c.wpt && Object.values(perCell[c.address]).includes("pass") && Object.values(perCell[c.address]).includes("fail"))
    .map((c) => c.address)
    .sort();

  const out = [];
  const divTxt = diverge.length
    ? ` &middot; <strong>${diverge.length} cell${diverge.length !== 1 ? "s" : ""} where the engines disagree with each other</strong> (${esc(diverge.join(", "))})`
    : "";
  out.push(
    `<p class="matrix-count">${cells.length} cells: ${tested} with a WPT test the spec can decide, ${cells.length - tested} the spec leaves open (observed only)${divTxt}</p>`,
  );
  out.push(
    '<pre class="face-block"><code>@font-face {\n  font-family: "Oblique Test";\n  src: url(Cairo.var.subset.ttf);  /* real Cairo, slnt -11..11, wght 200..1000 */\n  font-style: <em>&lt;column&gt;</em>;\n}</code></pre>',
  );
  out.push('<div class="matrix-wrap"><table class="matrix"><thead><tr><th></th>');
  for (const c of columns)
    out.push(`<th><span class="addr">${esc(c.address)}</span><code>${esc(c.code)}</code><span class="col-note">${esc(c.note)}</span></th>`);
  out.push("</tr></thead><tbody>");
  for (const row of rows) {
    const lines = row.lines.map(esc).join("<br>");
    out.push(`<tr><th scope="row"><span class="row-num">${esc(row.address)}</span> <code>${lines}</code></th>`);
    for (const col of columns) {
      const cell = byAddr[`${col.address}${row.address}`];
      const res = perCell[cell.address];
      const url = TEST_URL_BASE + (cell.wpt ? cell.files[0] : "matrix.manifest.json");
      let tags = "";
      if (cell.status !== "specified") {
        const allowed = cell.allowed.map(outcomeText).join(" / ");
        tags = `<span class="tag" title="${esc(cell.why.join("; "))}">spec allows: ${esc(allowed)}</span>`;
      }
      out.push(
        `<td class="status-${cellStatus(cell, res)}"><span class="cell-addr">${esc(cell.address)}</span>` +
          `<a class="specimen-link" href="${esc(url)}" title="${esc(cell.id)}">${specimen(manifest, cell)}</a>` +
          `${badges(manifest, survey, cell, res)}<div class="cell-tags">${tags}</div></td>`,
      );
    }
    out.push("</tr>");
  }
  out.push("</tbody></table></div>");
  out.push(
    '<ul class="legend">' +
      '<li><span class="b-badge pass"></span> pass</li>' +
      '<li><span class="b-badge fail"></span> fail</li>' +
      '<li><span class="b-badge observed"></span> observed (the spec allows it, nothing to pass or fail)</li>' +
      '<li><span class="b-badge unknown"></span> not run</li>' +
      '<li class="legend-note">Hover a circle for the engine and what it was measured to do. Click a specimen for its test file.</li>' +
      "</ul>",
  );
  const ver = ENGINES.map((e) => {
    const v = versions[e.key];
    return `<li><img class="logo" src="/browsers/${e.id}.svg" alt="">${esc(e.label)} ${v ? esc(v) : "&mdash; not run"}</li>`;
  });
  out.push(`<ul class="legend legend-versions">${ver.join("")}</ul>`);
  return out.join("");
}

/** The hand-written tests: every recorded id that is not a generated matrix cell and still exists on disk. */
function renderStandalone(results) {
  const ids = readdirSync(TESTS_DIR)
    .filter((n) => !n.startsWith("matrix-") && isTestFile(n))
    .map((n) => n.slice(0, -5))
    .sort();
  const rows = ids.map((id) => {
    const lis = ENGINES.map((e) => {
      const s = reftestStatus(results, id, e.key);
      const cls = s === "pass" || s === "fail" ? s : "unknown";
      return `<li class="b-badge ${cls}" title="${esc(`${e.label}: ${s}`)}"><img class="logo" src="/browsers/${e.id}.svg" alt="${esc(e.label)}"></li>`;
    });
    return `<tr><td><a href="${esc(TEST_URL_BASE + id + ".html")}">${esc(id)}</a></td><td><ul class="verdicts">${lis.join("")}</ul></td></tr>`;
  });
  return `<table class="standalone"><thead><tr><th>Test</th><th>Result</th></tr></thead><tbody>${rows.join("")}</tbody></table>`;
}

export function matrixPage() {
  const build = () => {
    const manifest = loadManifest();
    const results = readBrowserMatrix();
    const survey = loadSurvey() ?? { engines: {} };
    verifyMatrix(manifest, results);
    return { manifest, results, survey, versions: readEngineVersions() };
  };
  return {
    name: "oblique-matrix-page",
    transformIndexHtml: {
      order: "pre",
      handler(html) {
        const { manifest, results, survey, versions } = build();
        return html
          .replace("<!--MATRIX_FONT_FACE-->", () => fontFaceCss(manifest))
          .replace("<!--MATRIX-->", () => renderMatrix(manifest, results, survey, versions))
          .replace("<!--STANDALONE-->", () => renderStandalone(results));
      },
    },
    // the live specimens use the exact font file the tests do: served in dev, emitted in build
    configureServer(server) {
      server.middlewares.use("/Cairo.var.subset.ttf", (_req, res) => {
        res.setHeader("Content-Type", "font/ttf");
        res.end(readFileSync(FONT_FILE));
      });
    },
    generateBundle() {
      this.emitFile({ type: "asset", fileName: "Cairo.var.subset.ttf", source: readFileSync(FONT_FILE) });
    },
  };
}
