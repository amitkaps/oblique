// The site's coverage matrix, rendered to static HTML at build time (a Vite plugin).
//
// @font-face `font-style` descriptor (columns A, B, C...) x use-site request (rows 1, 2, 3...),
// one cell per pair, all against one font (Cairo subset, capital I).
//
// Everything about the grid comes from tests/oblique-style-matching/matrix/matrix.manifest.json,
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
import { TESTS_DIR, MATRIX_DIR, STANDALONE_DIR } from "../reference/src/cases.mjs";
import { pinCss } from "../reference/src/outcome.mjs";
import {
  compare,
  loadManifest,
  loadSurvey,
  readBrowserMatrix,
  readEngineVersions,
} from "../reference/src/compare.mjs";

const FONT_FILE = join(TESTS_DIR, "resources", "Cairo.var.subset.ttf");
const TEST_URL_BASE = "https://github.com/amitkaps/oblique/blob/main/tests/oblique-style-matching/";
const MATRIX_URL = TEST_URL_BASE + "matrix/";
const STANDALONE_URL = TEST_URL_BASE + "standalone/";
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
      if (!existsSync(join(MATRIX_DIR, name)))
        throw new Error(`site: ${name} (cell ${cell.address}) is missing: run \`pnpm generate\``);
    }
    if (cell.wpt && !results[cell.id])
      throw new Error(`site: ${cell.id} (cell ${cell.address}) has no row in results/browser-matrix.md: run and record it first`);
  }
  const onDisk = new Set(readdirSync(MATRIX_DIR).filter((n) => n.startsWith("matrix-") && isTestFile(n)).map((n) => n.slice(0, -5)));
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
  const ref = `<span class="ov-control" style="${esc(`${family} ${pinCss(matches[0])}`)}">${SPECIMEN_WORD}</span>`;
  return `<div class="overlap">${ref}${test}</div>`;
}

/** what one engine did in one cell: the ring (pass, fail, observed) and the words for what it rendered */
function engineView(cell, results, verdict) {
  return ENGINES.map((e) => {
    const v = verdict[cell.address][e.key];
    let ring;
    if (cell.wpt) ring = reftestStatus(results, cell.id, e.key);
    else ring = v.label == null ? "not-run" : v.ok === false ? "fail" : "observed"; // untested, but outside what the spec allows
    return { engine: e, ring: ring === "pass" || ring === "fail" || ring === "observed" ? ring : "unknown", label: v.label ?? "not run" };
  });
}

const badge = (view) =>
  `<span class="b-badge ${view.ring}" title="${esc(`${view.engine.label}: ${view.label}`)}"><img class="logo" src="/browsers/${view.engine.id}.svg" alt="${esc(view.engine.label)}"></span>`;

/**
 * What the engines did. When all three did the same, one line; when they differ, a line each, so
 * disagreement is what stands out.
 */
function engineLines(views) {
  const same = views.every((v) => v.label === views[0].label && v.ring === views[0].ring && v.label !== "not run");
  if (same) {
    return `<div class="eng-line ${views[0].ring}"><span class="rings" title="Chromium, Firefox and Safari, all the same">${views.map(badge).join("")}</span><span class="eng-val">${esc(views[0].label)}</span></div>`;
  }
  return views.map((v) => `<div class="eng-line ${v.ring}">${badge(v)}<span class="eng-val">${esc(v.label)}</span></div>`).join("");
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
  const verdict = Object.fromEntries(compare(manifest, results, survey).map((r) => [r.address, r.per]));
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
    out.push(`<th><span class="addr">${esc(c.address)}</span><span class="col-name">${esc(c.name)}</span><code>${esc(c.code)}</code><span class="col-note">${esc(c.note)}</span></th>`);
  out.push("</tr></thead><tbody>");
  for (const row of rows) {
    const lines = row.lines.map(esc).join("<br>");
    out.push(`<tr><th scope="row"><span class="row-num">${esc(row.address)}</span> <code>${lines}</code></th>`);
    for (const col of columns) {
      const cell = byAddr[`${col.address}${row.address}`];
      const res = perCell[cell.address];
      const url = MATRIX_URL + (cell.wpt ? cell.files[0] : "matrix.manifest.json");
      // every cell says what the reference expects on one line, then what the engines did
      const line = cell.spec;
      const spec = `<span class="spec ${line.decided ? "spec-decided" : "spec-open"}" title="${esc(cell.why.join("; "))}">${line.decided ? "spec:" : "spec*:"} ${esc(line.text)}</span>`;
      out.push(
        `<td class="status-${cellStatus(cell, res)}"><span class="cell-addr">${esc(cell.address)}</span>` +
          `<a class="specimen-link" href="${esc(url)}" title="${esc(cell.id)}">${specimen(manifest, cell)}</a>` +
          `<div class="cell-tags">${spec}${engineLines(engineView(cell, results, verdict))}</div></td>`,
      );
    }
    out.push("</tr>");
  }
  out.push("</tbody></table></div>");
  out.push(
    '<ul class="legend">' +
      '<li><span class="b-badge pass"></span> pass</li>' +
      '<li><span class="b-badge fail"></span> fail</li>' +
      '<li><span class="b-badge observed"></span> observed: no test, the spec allows several outcomes</li>' +
      '<li><span class="b-badge unknown"></span> not run</li>' +
      '<li class="legend-note">Each engine line is what it rendered; three rings on one line means all three did the same. A red ring on an untested cell means what it did is outside what the spec allows. ' +
      '<strong>spec:</strong> the spec decides, one rendering. <strong>spec*:</strong> it allows any of these. ' +
      '<code>slnt -11</code> is an 11&deg; forward slant (CSS angle and <code>slnt</code> have opposite signs), <code>slnt 0</code> is upright, ' +
      '<code>synth</code> is a synthesized skew (<code>~14&deg;</code> its angle), <code>+ synth</code> is one stacked on the axis. Click a specimen for its test file.</li>' +
      "</ul>",
  );
  const ver = ENGINES.map((e) => {
    const v = versions[e.key];
    return `<li><img class="logo" src="/browsers/${e.id}.svg" alt="">${esc(e.label)} ${v ? esc(v) : "&mdash; not run"}</li>`;
  });
  out.push(`<ul class="legend legend-versions">${ver.join("")}</ul>`);
  return out.join("");
}

const cellClass = (pass, total) => (total === 0 ? "none" : pass === total ? "all" : pass === 0 ? "zero" : "some");
const pct = (pass, total) => (total ? `${Math.round((100 * pass) / total)}%` : "");

/** one row of the results grid: a description and one cell per engine */
const gridRow = (first, engineCells, cls = "") =>
  `<div class="rrow ${cls}"><div class="rdesc">${first}</div>${engineCells.map((c) => `<div class="rcell ${c.cls}">${c.html}</div>`).join("")}</div>`;

/**
 * Where the spec leaves the outcome open: do the engines still render the same thing? Where all three
 * converge, that is evidence the spec could simply say so; where they differ, it is the list to take to CSSWG.
 */
function renderAgreement(manifest, results, survey) {
  const verdict = Object.fromEntries(compare(manifest, results, survey).map((r) => [r.address, r.per]));
  const open = manifest.cells.filter((c) => c.status !== "specified");
  const labels = (c) => ENGINES.map((e) => verdict[c.address][e.key].label);
  const agree = open.filter((c) => labels(c).every((l) => l != null && l === labels(c)[0]));
  const differ = open.filter((c) => !agree.includes(c));
  const row = (c) => {
    const col = manifest.columns.find((x) => x.slug === c.column);
    const rw = manifest.rows.find((x) => x.slug === c.row);
    const desc = `<span class="addr">${esc(c.address)}</span> ${esc(col.name)} <code>${esc(rw.lines.join(" "))}</code> <span class="spec spec-open">spec*: ${esc(c.spec.text)}</span>`;
    return gridRow(desc, ENGINES.map((e) => ({ cls: "", html: esc(verdict[c.address][e.key].label ?? "not run") })), "rtest");
  };
  const group = (title, cells) =>
    `<div class="rrow rhead rsection"><div class="rdesc">${title} (${cells.length})</div>${ENGINES.map(() => '<div class="rcell"></div>').join("")}</div>${cells.map(row).join("")}`;
  return (
    `<div class="agree"><p><strong>Where the spec is open,</strong> all three engines render the same in <strong>${agree.length} of ${open.length}</strong> cells. ` +
    `Where they converge, the spec could say so; where they differ is the list to take to the spec authors.</p>` +
    `<details class="ragree"><summary>Show the ${open.length} cells</summary><div class="rgrid">${group("All three agree", agree)}${group("The engines differ", differ)}</div></details></div>`
  );
}

/**
 * The results, in the shape wpt.fyi uses: a row per @font-face descriptor with passes over tests for each
 * engine, opening to the tests behind it, a total with a percentage, then the hand-written tests.
 * Only cells with a WPT test count; the ones the spec leaves open are listed, never scored.
 */
function renderResults(manifest, results, survey) {
  const verdict = Object.fromEntries(compare(manifest, results, survey).map((r) => [r.address, r.per]));
  const passed = (id, key) => reftestStatus(results, id, key) === "pass";
  const total = Object.fromEntries(ENGINES.map((e) => [e.key, { pass: 0, n: 0 }]));
  const out = [];
  out.push(
    `<div class="rgrid"><div class="rrow rhead"><div class="rdesc">Description</div>${ENGINES.map((e) => `<div class="rcell"><img class="hlogo" src="/browsers/${e.id}.svg" alt="">${esc(e.label)}</div>`).join("")}</div>`,
  );

  for (const col of manifest.columns) {
    const tested = manifest.cells.filter((c) => c.column === col.slug && c.wpt);
    const open = manifest.cells.filter((c) => c.column === col.slug && !c.wpt);
    const frac = ENGINES.map((e) => {
      const pass = tested.filter((c) => passed(c.id, e.key)).length;
      total[e.key].pass += pass;
      total[e.key].n += tested.length;
      return { cls: cellClass(pass, tested.length), html: `${pass} / ${tested.length}`, pass };
    });
    const anyFail = frac.some((f) => f.cls !== "all");
    const lines = tested
      .map((c) => {
        const row = manifest.rows.find((r) => r.slug === c.row);
        const cells = ENGINES.map((e) => {
          const ok = passed(c.id, e.key);
          const did = !ok ? `<span class="did">${esc(verdict[c.address][e.key].label ?? "")}</span>` : "";
          return { cls: ok ? "all" : "zero", html: `${ok ? "pass" : "fail"}${did}` };
        });
        const desc = `<a class="addr" href="${esc(MATRIX_URL + c.files[0])}">${esc(c.address)}</a> <code>${esc(row.lines.join(" "))}</code> <span class="spec ${c.spec.decided ? "spec-decided" : "spec-open"}">${c.spec.decided ? "spec:" : "spec*:"} ${esc(c.spec.text)}</span>`;
        return gridRow(desc, cells, "rtest");
      })
      .join("");
    const note = open.length ? `<div class="rnote">Not scored, the spec leaves them open: ${open.map((c) => esc(c.address)).join(", ")}</div>` : "";
    out.push(
      `<details class="rgroup"${anyFail ? " open" : ""}><summary>${gridRow(`<span class="addr">${esc(col.address)}</span> <span class="col-name">${esc(col.name)}</span> <code>${esc(col.code)}</code>`, frac, "rsum")}</summary>${lines}${note}</details>`,
    );
  }
  out.push(
    gridRow("<strong>Total</strong>", ENGINES.map((e) => {
      const t = total[e.key];
      return { cls: cellClass(t.pass, t.n), html: `<strong>${t.pass} / ${t.n}</strong> &middot; ${pct(t.pass, t.n)}` };
    }), "rtotal"),
  );

  // hand-written tests, one row each, then their own total
  const ids = readdirSync(STANDALONE_DIR).filter(isTestFile).map((n) => n.slice(0, -5)).sort();
  const extra = Object.fromEntries(ENGINES.map((e) => [e.key, 0]));
  out.push(`<div class="rrow rhead rsection"><div class="rdesc">Additional tests</div>${ENGINES.map(() => "<div class=\"rcell\"></div>").join("")}</div>`);
  for (const id of ids) {
    const cells = ENGINES.map((e) => {
      const ok = passed(id, e.key);
      if (ok) extra[e.key]++;
      return { cls: ok ? "all" : "zero", html: ok ? "pass" : "fail" };
    });
    out.push(gridRow(`<a href="${esc(STANDALONE_URL + id + ".html")}">${esc(id)}</a>`, cells, "rtest"));
  }
  out.push(
    gridRow("<strong>Additional total</strong>", ENGINES.map((e) => ({
      cls: cellClass(extra[e.key], ids.length),
      html: `<strong>${extra[e.key]} / ${ids.length}</strong> &middot; ${pct(extra[e.key], ids.length)}`,
    })), "rtotal"),
  );
  out.push("</div>");
  return out.join("") + renderAgreement(manifest, results, survey);
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
          .replace("<!--RESULTS-->", () => renderResults(manifest, results, survey));
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
