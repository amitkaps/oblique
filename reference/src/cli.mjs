// reference/src/cli.mjs
//   node src/cli.mjs generate            write the tests and manifest
//   node src/cli.mjs generate --check    fail (exit 1) if the files on disk differ
//   node src/cli.mjs classes             the branch each case exercises
//   node src/cli.mjs compare             expected vs recorded browser results
import { readdirSync, readFileSync, writeFileSync, rmSync, existsSync } from "node:fs";
import { join } from "node:path";
import { loadMatrix, MATRIX_DIR, cells } from "./cases.mjs";
import { generate } from "./wpt.mjs";
import { compare, loadManifest, loadSurvey, readBrowserMatrix, report } from "./compare.mjs";

const isGenerated = (name) => /^matrix-.*\.html$/.test(name) || name === "matrix.manifest.json";

function runGenerate(check) {
  const { files } = generate(loadMatrix());
  const problems = [];
  for (const [name, content] of files) {
    const path = join(MATRIX_DIR, name);
    const current = existsSync(path) ? readFileSync(path, "utf8") : null;
    if (current !== content) {
      problems.push(current === null ? `missing ${name}` : `differs ${name}`);
      if (!check) writeFileSync(path, content);
    }
  }
  for (const name of readdirSync(MATRIX_DIR).filter(isGenerated)) {
    if (!files.has(name)) {
      problems.push(`stale ${name}`);
      if (!check) rmSync(join(MATRIX_DIR, name));
    }
  }
  const html = [...files.keys()].filter((n) => n.endsWith(".html") && !n.includes("-ref") && !n.includes("-notref")).length;
  if (check) {
    if (problems.length) {
      console.error(`generate --check: ${problems.length} difference(s):\n  ${problems.join("\n  ")}`);
      process.exit(1);
    }
    console.log(`generate --check: ${files.size} files up to date (${html} tests)`);
  } else {
    console.log(`generate: ${html} tests, ${files.size} files (${problems.length} written or removed)`);
  }
}

function runClasses() {
  const groups = new Map();
  for (const c of cells(loadMatrix())) {
    const k = `${c.expected.status} | ${c.expected.stage} | ${c.expected.allowed.map((o) => (o.kind === "axis" ? `${o.axis}=${o.value}` : o.kind)).join(",")}`;
    groups.set(k, [...(groups.get(k) ?? []), c.address]);
  }
  for (const [k, v] of [...groups].sort()) console.log(`${v.join(" ").padEnd(30)} ${k}`);
}

const [cmd, ...rest] = process.argv.slice(2);
if (cmd === "generate") runGenerate(rest.includes("--check"));
else if (cmd === "classes") runClasses();
else if (cmd === "compare") {
  const manifest = loadManifest();
  console.log(report(compare(manifest, readBrowserMatrix(), loadSurvey()), manifest));
}
else {
  console.error("usage: cli.mjs generate [--check] | classes | compare");
  process.exit(2);
}
