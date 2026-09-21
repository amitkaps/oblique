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
import { TESTS_DIR } from "../reference/src/cases.mjs";
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

const isTestFile = (n) => n.endsWith(".html") && !n.endsWith("-ref.html");

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
  for (const t of manifest.standalone ?? []) {
    if (!existsSync(join(TESTS_DIR, `${t.id}.html`))) throw new Error(`site: standalone test ${t.id} (${t.address}) is missing`);
    if (!results[t.id]) throw new Error(`site: ${t.id} (${t.address}) has no row in results/browser-matrix.md: run and record it first`);
  }
  const onDisk = new Set(readdirSync(TESTS_DIR).filter((n) => n.startsWith("font-style-match-") && isTestFile(n)).map((n) => n.slice(0, -5)));
  const expected = new Set([...cells.filter((c) => c.wpt).map((c) => c.id), ...(manifest.standalone ?? []).map((t) => t.id)]);
  const extra = [...onDisk].filter((n) => !expected.has(n));
  const missing = [...expected].filter((n) => !onDisk.has(n));
  if (extra.length || missing.length)
    throw new Error(`site: font-style-match-* tests on disk disagree with the manifest: extra ${extra}, missing ${missing}`);
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

/**
 * What one engine did in one cell: the ring and the words for what it rendered.
 *   pass    an allowed rendering, and (where the spec allows several) the same one every engine chose
 *   fail    a rendering the spec forbids
 *   differ  allowed, but the engines did not all choose the same: conformant, not interoperable
 *   unknown not measured
 * `untested` marks a cell with no WPT test (measured only); it changes the ring's line, not its colour.
 */
function engineView(cell, verdict, state) {
  return ENGINES.map((e) => {
    const v = verdict[cell.address][e.key];
    const ring = v.ok === null || v.label == null ? "unknown" : v.ok === false ? "fail" : state === "differ" ? "differ" : "pass";
    return { engine: e, ring, label: v.label ?? "not run", untested: !cell.wpt };
  });
}

const badge = (view) =>
  `<span class="b-badge ${view.ring}${view.untested ? " untested" : ""}" title="${esc(`${view.engine.label}: ${view.label}`)}"><img class="logo" src="/browsers/${view.engine.id}.svg" alt="${esc(view.engine.label)}"></span>`;

/**
 * What the engines did. When all three rendered the same, one line; otherwise a line each, so
 * disagreement is what stands out.
 */
function engineLines(views, state) {
  if (state === "same") {
    return `<div class="eng-line ${views[0].ring}"><span class="rings" title="Chromium, Firefox and Safari, all the same">${views.map(badge).join("")}</span><span class="eng-val">${esc(views[0].label)}</span></div>`;
  }
  return views.map((v) => `<div class="eng-line ${v.ring}">${badge(v)}<span class="eng-val">${esc(v.label)}</span></div>`).join("");
}

function renderMatrix(manifest, results, survey, versions) {
  const { columns, rows, cells } = manifest;
  const byAddr = Object.fromEntries(cells.map((c) => [c.address, c]));
  const rowsC = compare(manifest, results, survey);
  const verdict = Object.fromEntries(rowsC.map((r) => [r.address, r.per]));
  const state = Object.fromEntries(rowsC.map((r) => [r.address, r.state]));
  const list = (st) => rowsC.filter((r) => r.state === st).map((r) => r.address);
  const [same, fail, differ] = [list("same"), list("fail"), list("differ")];
  const untested = cells.filter((c) => !c.wpt).length;

  const out = [];
  out.push(
    `<p class="matrix-count">${cells.length} cells: <strong>${same.length} interoperable</strong> (all three engines render the same allowed thing) &middot; ` +
      `<strong class="c-fail">${fail.length} failing</strong> (${esc(fail.join(", "))}: an engine renders what the spec forbids) &middot; ` +
      `<strong class="c-differ">${differ.length} diverging</strong> (${esc(differ.join(", "))}: the spec allows several outcomes and the engines chose differently)` +
      `${untested ? `. ${untested} cells have no WPT test and are only measured` : ""}.</p>`,
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
      const url = TEST_URL_BASE + (cell.wpt ? cell.files[0] : "matrix.manifest.json");
      // every cell says what the reference expects on one line, then what the engines did
      const line = cell.spec;
      const spec = `<span class="spec ${line.decided ? "spec-decided" : "spec-open"}" title="${esc(cell.why.join("; "))}">${line.decided ? "spec:" : "spec*:"} ${esc(line.text)}</span>`;
      out.push(
        `<td class="status-${state[cell.address]}"><span class="cell-addr">${esc(cell.address)}</span>` +
          `<a class="specimen-link" href="${esc(url)}" title="${esc(cell.id)}">${specimen(manifest, cell)}</a>` +
          `<div class="cell-tags">${spec}${engineLines(engineView(cell, verdict, state[cell.address]), state[cell.address])}</div></td>`,
      );
    }
    out.push("</tr>");
  }
  out.push("</tbody></table></div>");
  out.push(
    '<ul class="legend">' +
      '<li><span class="b-badge pass"></span> pass: allowed, and all three engines render the same</li>' +
      '<li><span class="b-badge fail"></span> fail: the spec forbids what it rendered</li>' +
      '<li><span class="b-badge differ"></span> differ: each is allowed, but the engines chose differently (not interoperable)</li>' +
      '<li><span class="b-badge pass untested"></span> dashed: no WPT test, measured only</li>' +
      '<li><span class="b-badge unknown"></span> not run</li>' +
      '<li class="legend-note">Each engine line is what it rendered; three rings on one line means all three did the same. ' +
      '<strong>spec:</strong> the spec decides, one rendering. <strong>spec*:</strong> it allows several outcomes, so a test can only forbid some of them. ' +
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

/** one row of the results grid: a description, one cell per engine, then the interop cell */
const gridRow = (first, cells, cls = "") =>
  `<div class="rrow ${cls}"><div class="rdesc">${first}</div>${cells.map((c) => `<div class="rcell ${c.cls}">${c.html}</div>`).join("")}</div>`;

const interopCell = (state) =>
  state === "same" ? { cls: "all", html: "same" }
  : state === "differ" ? { cls: "differ", html: "differs" }
  : state === "fail" ? { cls: "zero", html: "fail" }
  : { cls: "none", html: "&ndash;" };

/**
 * The results, in the shape wpt.fyi uses: a row per @font-face descriptor, opening to the cells behind it, a
 * group Z for the hand-written tests, then a total with a percentage. Every column counts the same items (each
 * cell, and each standalone test). An engine column counts the ones where that engine renders an allowed
 * outcome, which a loose test can pass. The Interop column is stricter: all three engines must render the same
 * allowed thing, so a cell where the spec allows several outcomes and the engines chose differently is not
 * interoperable even though each engine passes.
 */
function renderResults(manifest, results, survey) {
  const rowsC = compare(manifest, results, survey);
  const verdict = Object.fromEntries(rowsC.map((r) => [r.address, r.per]));
  const state = Object.fromEntries(rowsC.map((r) => [r.address, r.state]));
  const passed = (id, key) => reftestStatus(results, id, key) === "pass";
  // an engine conforms in a cell when it renders an allowed outcome: a WPT pass, or, where no test can fail
  // (the spec excludes nothing testable), any measured rendering
  const conforms = (c, key) => (c.wpt ? passed(c.id, key) : verdict[c.address][key].ok !== false && verdict[c.address][key].label != null);
  const total = Object.fromEntries(ENGINES.map((e) => [e.key, { pass: 0, n: 0 }]));
  const interop = { same: 0, n: 0 };
  const out = [];
  out.push(
    `<div class="rgrid"><div class="rrow rhead"><div class="rdesc">Description</div>${ENGINES.map((e) => `<div class="rcell"><img class="hlogo" src="/browsers/${e.id}.svg" alt="">${esc(e.label)}</div>`).join("")}<div class="rcell">Interop</div></div>`,
  );

  for (const col of manifest.columns) {
    const all = manifest.cells.filter((c) => c.column === col.slug);
    const frac = ENGINES.map((e) => {
      const pass = all.filter((c) => conforms(c, e.key)).length;
      total[e.key].pass += pass;
      total[e.key].n += all.length;
      return { cls: cellClass(pass, all.length), html: `${pass} / ${all.length}`, pass };
    });
    const same = all.filter((c) => state[c.address] === "same").length;
    interop.same += same;
    interop.n += all.length;
    const sumCells = [...frac, { cls: cellClass(same, all.length), html: `${same} / ${all.length}` }];
    const anyBad = sumCells.some((f) => f.cls !== "all");
    const lines = all
      .map((c) => {
        const row = manifest.rows.find((r) => r.slug === c.row);
        const st = state[c.address];
        const cells = ENGINES.map((e) => {
          const v = verdict[c.address][e.key];
          const what = esc(v.label ?? "not run");
          if (!c.wpt) return conforms(c, e.key) ? { cls: st === "differ" ? "differ" : "all", html: `allowed<span class="did did-obs">${what}</span>` } : { cls: "zero", html: `fail<span class="did">${what}</span>` };
          if (!passed(c.id, e.key)) return { cls: "zero", html: `fail<span class="did">${what}</span>` };
          return st === "differ" ? { cls: "differ", html: `pass<span class="did did-differ">${what}</span>` } : { cls: "all", html: "pass" };
        });
        const link = c.wpt ? `<a class="addr" href="${esc(TEST_URL_BASE + c.files[0])}">${esc(c.address)}</a>` : `<span class="addr">${esc(c.address)}</span>`;
        const desc = `${link} <code>${esc(row.lines.join(" "))}</code> <span class="spec ${c.spec.decided ? "spec-decided" : "spec-open"}">${c.spec.decided ? "spec:" : "spec*:"} ${esc(c.spec.text)}</span>${c.wpt ? "" : ' <span class="notest">no test</span>'}`;
        return gridRow(desc, [...cells, interopCell(st)], "rtest");
      })
      .join("");
    out.push(
      `<details class="rgroup"${anyBad ? " open" : ""}><summary>${gridRow(`<span class="addr">${esc(col.address)}</span> <span class="col-name">${esc(col.name)}</span> <code>${esc(col.code)}</code>`, sumCells, "rsum")}</summary>${lines}</details>`,
    );
  }
  // group Z: the hand-written tests, which are not cells of the grid. Each is a single-outcome reftest, so a
  // pass in all three engines is the same rendering in all three
  const z = manifest.standalone ?? [];
  if (z.length) {
    const frac = ENGINES.map((e) => {
      const pass = z.filter((t) => passed(t.id, e.key)).length;
      total[e.key].pass += pass;
      total[e.key].n += z.length;
      return { cls: cellClass(pass, z.length), html: `${pass} / ${z.length}`, pass };
    });
    const allPass = (t) => ENGINES.every((e) => passed(t.id, e.key));
    const zSame = z.filter(allPass).length;
    interop.same += zSame;
    interop.n += z.length;
    const lines = z
      .map((t) => {
        const cells = ENGINES.map((e) => {
          const ok = passed(t.id, e.key);
          return { cls: ok ? "all" : "zero", html: ok ? "pass" : "fail" };
        });
        return gridRow(`<a class="addr" href="${esc(TEST_URL_BASE + t.id + ".html")}">${esc(t.address)}</a> ${esc(t.name)}`, [...cells, interopCell(allPass(t) ? "same" : "fail")], "rtest");
      })
      .join("");
    const zSum = [...frac, { cls: cellClass(zSame, z.length), html: `${zSame} / ${z.length}` }];
    out.push(
      `<details class="rgroup"${zSum.some((f) => f.cls !== "all") ? " open" : ""}><summary>${gridRow(`<span class="addr">Z</span> <span class="col-name">Standalone tests</span> <code>hand-written, not cells of the grid</code>`, zSum, "rsum")}</summary>${lines}</details>`,
    );
  }
  out.push(
    gridRow("<strong>Total</strong>", [
      ...ENGINES.map((e) => {
        const t = total[e.key];
        return { cls: cellClass(t.pass, t.n), html: `<strong>${t.pass} / ${t.n}</strong> &middot; ${pct(t.pass, t.n)}` };
      }),
      { cls: cellClass(interop.same, interop.n), html: `<strong>${interop.same} / ${interop.n}</strong> &middot; ${pct(interop.same, interop.n)}` },
    ], "rtotal"),
  );
  out.push("</div>");
  return out.join("");
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
