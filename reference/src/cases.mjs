// Turns cases/matrix.json into concrete cases (one per row x column) and runs the
// reference on each. Pure data plumbing: no expectation logic lives here.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { expected } from "./expected.mjs";

export const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..", "..");
export const TESTS_DIR = join(ROOT, "tests", "oblique-style-matching");
export const MATRIX_DIR = join(TESTS_DIR, "matrix");
export const STANDALONE_DIR = join(TESTS_DIR, "standalone");
export const MATRIX_JSON = join(ROOT, "reference", "cases", "matrix.json");

export function loadMatrix(path = MATRIX_JSON) {
  return JSON.parse(readFileSync(path, "utf8"));
}

/** The inline CSS the generated test puts on its paragraph. */
export function useSiteCss(row) {
  if (row.fvs) return Object.entries(row.fvs).map(([axis, v]) => `font-variation-settings: '${axis}' ${v};`).join(" ");
  if (row.em) return row.extraCss ?? "";
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
        fvs: row.fvs ?? null,
        synthesis: row.synthesis ?? {},
        resolutions: matrix.resolutions,
      });
      out.push({
        address: `${col.address}${row.address}`,
        id: `matrix-${row.slug}-${col.slug}`,
        row,
        col,
        css: useSiteCss(row),
        expected: exp,
      });
    }
  }
  return out;
}
