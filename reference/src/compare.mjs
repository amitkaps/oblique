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
import { axis, label, synth } from "./outcome.mjs";

export const ENGINES = ["chrome", "firefox", "safari"];
const TOL = 1.5;

/** lean (px, positive = forward slant) an allowed outcome predicts, from the font's calibration */
export function predictedLean(o, font) {
  if (o.kind === "axis") return -o.value * font.pxPerSlntUnit; // slnt and CSS angle have opposite signs
  return Math.sign(o.angle) * Math.tan((Math.abs(o.angle) * Math.PI) / 180) * font.glyphHeightPx;
}

const SYNTH_MIN = 3;
const SYNTH_MAX = 90;

/**
 * What a measured lean looks like, in the same words as an expectation: `slnt 0`, `slnt -11`,
 * `synth ~14°`, or a stack of both. A lean alone is ambiguous (an axis at -5 and a 5deg synthesized
 * skew lean the same), so the cell narrows it down:
 *   - axis values the cell allows are always plausible;
 *   - axis values it forbids are plausible only if the engine FAILED the reftest: a pass means the
 *     glyph differs, pixel for pixel, from the forbidden axis rendering, so it is a synthesized skew;
 *   - a stacked rendering is an axis value plus about one default skew (14deg, ~22px);
 *   - anything else that leans is a synthesized skew, labelled with its angle.
 */
export function describeLean(cell, lean, font, reftest = null) {
  if (lean === null || lean === undefined) return null;
  const px = font.pxPerSlntUnit;
  const near = (v, t = TOL) => Math.abs(lean - v) <= t;
  if (near(0)) return label(axis(0));

  const allowedAxes = cell.allowed.filter((o) => o.kind === "axis").map((o) => o.value);
  const forbiddenAxes = (cell.plan?.mismatch ?? []).filter((o) => o.kind === "axis").map((o) => o.value);
  const plausible = new Set(allowedAxes);
  if (reftest !== "pass") for (const v of forbiddenAxes) plausible.add(v);
  for (const v of plausible) if (v !== 0 && near(-v * px)) return label(axis(v));

  const synth14 = Math.abs(predictedLean(synth(14), font));
  const stacked = [...new Set([...allowedAxes, ...forbiddenAxes, font.slnt[0]])]
    .filter((v) => v !== 0)
    .map((v) => ({ v, off: Math.abs(lean + v * px - synth14) })) // what is left over must be a forward default skew
    .filter((c) => c.off <= 3)
    .sort((x, y) => x.off - y.off)[0];
  if (stacked) return `${label(axis(stacked.v))} + synth`;

  if (Math.abs(lean) >= SYNTH_MIN) {
    const deg = Math.abs(lean) - synth14 <= TOL && synth14 - Math.abs(lean) <= TOL ? 14 : Math.round((Math.atan(Math.abs(lean) / font.glyphHeightPx) * 180) / Math.PI);
    return `synth ~${lean < 0 ? "-" : ""}${deg}\u00B0`;
  }
  return `lean ${lean}px`;
}

/**
 * Is a measured lean one the cell allows? Axis and upright outcomes predict an exact lean.
 * A synthesized skew has an engine-chosen angle (Firefox follows the request, Chrome and Safari
 * use their own), so any forward or backward skew of plausible size in the requested direction
 * counts, and it cannot be told apart from an axis by size alone.
 */
export function withinAllowed(cell, lean, font) {
  return cell.allowed.some((o) =>
    o.kind === "synth"
      ? Math.sign(lean) === Math.sign(o.angle) && Math.abs(lean) >= SYNTH_MIN && Math.abs(lean) <= SYNTH_MAX
      : Math.abs(predictedLean(o, font) - lean) <= TOL,
  );
}

export function readBrowserMatrix(path = join(ROOT, "results", "browser-matrix.md")) {
  const out = {};
  for (const line of readFileSync(path, "utf8").split("\n")) {
    if (!line.startsWith("|") || line.startsWith("|---") || line.includes("test_id")) continue;
    const c = line.split("|").slice(1, -1).map((s) => s.trim());
    if (c.length >= 5) (out[c[0]] ??= {})[c[1]] = c[4];
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
        label: describeLean(cell, lean, manifest.font, reftest),
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
