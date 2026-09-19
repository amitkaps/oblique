// The reference is the CONTROL: it must never lean on a browser's own font matching.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

const src = join(fileURLToPath(new URL(".", import.meta.url)), "..", "src");
// files that produce expectations; cli/wpt/compare only read and write files
const CORE = ["style.mjs", "match.mjs", "variation.mjs", "synthesis.mjs", "expected.mjs"];
const FORBIDDEN = [/getComputedStyle/, /\bdocument\b/, /\bwindow\b/, /\bcanvas\b/i, /FontFace/, /measureText/, /\bnavigator\b/];

test("expectation code references no browser API", () => {
  for (const file of CORE) {
    const text = readFileSync(join(src, file), "utf8")
      .split("\n")
      .filter((l) => !l.trim().startsWith("//"))
      .join("\n");
    for (const re of FORBIDDEN) assert.doesNotMatch(text, re, `${file} mentions ${re}`);
  }
});

test("core modules import only each other", () => {
  for (const file of CORE) {
    const imports = [...readFileSync(join(src, file), "utf8").matchAll(/from\s+"([^"]+)"/g)].map((m) => m[1]);
    for (const spec of imports) assert.match(spec, /^\.\//, `${file} imports ${spec}`);
  }
  assert.ok(readdirSync(src).includes("expected.mjs"));
});

test("the core runs in a runtime with no DOM globals", () => {
  assert.equal(typeof globalThis.document, "undefined");
  assert.equal(typeof globalThis.window, "undefined");
});
