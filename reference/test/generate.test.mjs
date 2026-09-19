// The committed tests and manifest must be exactly what the generator produces from
// cases/matrix.json: nobody edits generated files by hand, and nobody forgets to
// regenerate after changing the reference.
import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { generate } from "../src/wpt.mjs";
import { loadMatrix, MATRIX_DIR, cells } from "../src/cases.mjs";

test("committed files equal the generator's output", () => {
  const { files } = generate(loadMatrix());
  for (const [name, content] of files) {
    assert.ok(existsSync(join(MATRIX_DIR, name)), `missing ${name}: run \`node src/cli.mjs generate\``);
    assert.equal(readFileSync(join(MATRIX_DIR, name), "utf8"), content, `${name} is stale`);
  }
  const stale = readdirSync(MATRIX_DIR).filter((n) => /^matrix-/.test(n) && !files.has(n));
  assert.deepEqual(stale, []);
});

test("addresses are unique, column letter + row number", () => {
  const seen = new Set();
  for (const c of cells(loadMatrix())) {
    assert.match(c.address, /^[A-Z]+[0-9]+$/);
    assert.ok(!seen.has(c.address), c.address);
    seen.add(c.address);
  }
});

test("every generated reftest has at least one reference, and the refs it links exist", () => {
  const { files } = generate(loadMatrix());
  for (const [name, content] of files) {
    if (!name.endsWith(".html") || /-(not)?ref\.html$/.test(name)) continue;
    const links = [...content.matchAll(/<link rel="(?:match|mismatch)" href="([^"]+)"/g)].map((m) => m[1]);
    assert.ok(links.length > 0, name);
    for (const l of links) assert.ok(files.has(l), `${name} links ${l}`);
  }
});

test("no generated test sets font-synthesis (a matched request must not be synthesized)", () => {
  const { files } = generate(loadMatrix());
  for (const [name, content] of files) {
    if (!name.endsWith(".html")) continue;
    const body = content.replace(/<!--[\s\S]*?-->/g, "");
    assert.doesNotMatch(body, /font-synthesis[a-z-]*\s*:/, name); // a declaration, not the spec link
  }
});
