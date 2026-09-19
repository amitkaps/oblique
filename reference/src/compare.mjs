// compareResults: judge recorded browser results against the reference's expectation.
//
// Two independent signals per engine:
//   reftest  the pass/fail recorded in results/browser-matrix.md for the cell's WPT test
//            (present only for `specified` and `constrained` cases)
//   lean     the measured lean of the glyph (results/survey.json, from scripts/survey.py),
//            judged against the lean each ALLOWED outcome predicts. This works for every
//            case, including `unspecified` ones, and cross-checks the reftest.
//
// Classification of a cell across engines:
//   agrees               every measured engine is inside the allowed set
//   diverges-from-spec   some engines are outside it, at least one inside
//   reference-suspect    EVERY measured engine is outside it: more likely a wrong or
//                        incomplete reference (or a spec gap) than three browser bugs
//   inconclusive         no results recorded for the cell

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { ROOT, TESTS_DIR } from "./cases.mjs";

export const ENGINES = ["chrome", "firefox", "safari"];
const TOL = 1.5;

/** lean (px) an allowed outcome predicts, from the font's calibration */
export function predictedLean(o, font) {
  if (o.kind === "upright") return 0;
  if (o.kind === "axis") return Math.abs(o.value) * font.pxPerSlntUnit;
  return Math.tan((o.angle * Math.PI) / 180) * font.glyphHeightPx;
}

/** What a measured lean looks like, for reporting. */
export function leanLabel(lean, font) {
  const axisMax = Math.abs(font.slnt[0]) * font.pxPerSlntUnit;
  const synth14 = predictedLean({ kind: "synth", angle: 14 }, font);
  const near = (v, t) => Math.abs(lean - v) <= t;
  if (near(0, TOL)) return "upright";
  if (near(axisMax, TOL)) return `axis ${font.slnt[0]}`;
  if (near(synth14, TOL)) return "synthetic 14deg";
  if (near(axisMax + synth14, 3)) return "stacked (axis + synthetic)";
  return `lean ${lean}px`;
}

export function withinAllowed(cell, lean, font) {
  return cell.allowed.some((o) => Math.abs(predictedLean(o, font) - lean) <= TOL);
}

export function readBrowserMatrix(path = join(ROOT, "results", "browser-matrix.md")) {
  const out = {};
  for (const line of readFileSync(path, "utf8").split("\n")) {
    if (!line.startsWith("|") || line.startsWith("|---") || line.includes("test_id")) continue;
    const c = line.split("|").slice(1, -1).map((s) => s.trim());
    if (c.length >= 5) (out[c[0]] ??= {})[c[1]] = c[4]; // later rows win
  }
  return out;
}

/** {engine: version} of the latest recorded row per engine. */
export function readEngineVersions(path = join(ROOT, "results", "browser-matrix.md")) {
  const out = {};
  for (const line of readFileSync(path, "utf8").split("\n")) {
    if (!line.startsWith("|") || line.startsWith("|---") || line.includes("test_id")) continue;
    const c = line.split("|").slice(1, -1).map((s) => s.trim());
    if (c.length >= 5 && ENGINES.includes(c[1])) out[c[1]] = c[2];
  }
  return out;
}

export function compare(manifest, matrixResults, survey) {
  return manifest.cells.map((cell) => {
    const per = {};
    for (const e of ENGINES) {
      const reftest = cell.wpt ? matrixResults[cell.id]?.[e] ?? null : null;
      const lean = survey?.engines?.[e]?.cells?.[cell.id] ?? null;
      const leanOk = lean === null ? null : withinAllowed(cell, lean, manifest.font);
      const verdicts = [reftest ? reftest === "pass" : null, leanOk].filter((v) => v !== null);
      per[e] = {
        reftest,
        lean,
        label: lean === null ? null : leanLabel(lean, manifest.font),
        ok: verdicts.length ? verdicts.every(Boolean) : null,
      };
    }
    const measured = ENGINES.filter((e) => per[e].ok !== null);
    const bad = measured.filter((e) => !per[e].ok);
    let classification = "inconclusive";
    if (measured.length) {
      if (!bad.length) classification = "agrees";
      else if (bad.length === measured.length && measured.length > 1) classification = "reference-suspect";
      else classification = "diverges-from-spec";
    }
    return { address: cell.address, id: cell.id, status: cell.status, per, classification };
  });
}

export function loadSurvey() {
  const p = join(ROOT, "results", "survey.json");
  return existsSync(p) ? JSON.parse(readFileSync(p, "utf8")) : null;
}

export function loadManifest() {
  return JSON.parse(readFileSync(join(TESTS_DIR, "matrix.manifest.json"), "utf8"));
}

export function report(rows, manifest) {
  const cell = (r, e) => {
    const p = r.per[e];
    if (p.ok === null) return "-";
    const tag = p.ok ? "ok" : "OUT";
    return `${tag}${p.label ? " " + p.label : ""}${p.reftest ? ` [${p.reftest}]` : ""}`;
  };
  const lines = [`${"cell".padEnd(5)}${"status".padEnd(13)}${"chrome".padEnd(32)}${"firefox".padEnd(32)}${"safari".padEnd(32)}classification`];
  for (const r of rows) {
    lines.push(`${r.address.padEnd(5)}${r.status.padEnd(13)}${cell(r, "chrome").padEnd(32)}${cell(r, "firefox").padEnd(32)}${cell(r, "safari").padEnd(32)}${r.classification}`);
  }
  const counts = {};
  for (const r of rows) counts[r.classification] = (counts[r.classification] ?? 0) + 1;
  lines.push("", Object.entries(counts).map(([k, v]) => `${k}: ${v}`).join("  |  "));
  return lines.join("\n");
}
