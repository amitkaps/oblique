// Turns cases/matrix.json into concrete cases (one per row x column) and runs the
// reference on each. Pure data plumbing: no expectation logic lives here.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { expected } from "./expected.mjs";

export const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..", "..");
export const TESTS_DIR = join(ROOT, "tests", "oblique-style-matching");
export const MATRIX_JSON = join(ROOT, "reference", "cases", "matrix.json");

/** Every generated test and reference starts with this; it keeps names unique across WPT's css/ tree. */
export const PREFIX = "font-style-match";

export function loadMatrix(path = MATRIX_JSON) {
  return JSON.parse(readFileSync(path, "utf8"));
}

/** The inline CSS the generated test puts on its paragraph. */
export function useSiteCss(row) {
  return `font-style: ${row.request};${row.extraCss ? " " + row.extraCss : ""}`;
}

export function cells(matrix) {
  const out = [];
  for (const row of matrix.rows) {
    for (const col of matrix.columns) {
      const exp = expected({
        faces: [{ id: "face", descriptor: col.descriptor }],
        font: { slnt: matrix.font.slnt, ital: matrix.font.ital },
        request: row.request,
        synthesis: row.synthesis ?? {},
        resolutions: matrix.resolutions,
      });
      // A test that leans on an assumption the spec text does not make is `.tentative` (WPT file-name flag).
      const tentative = exp.assumptions.length > 0 && exp.plan.match.length + exp.plan.mismatch.length > 0;
      out.push({
        address: `${col.address}${row.address}`,
        id: `${PREFIX}-${row.slug}-${col.slug}${tentative ? ".tentative" : ""}`,
        tentative,
        row,
        col,
        css: useSiteCss(row),
        expected: exp,
      });
    }
  }
  return out;
}
