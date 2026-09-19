// The words an expectation is shown in. One vocabulary for the generator, the manifest, `classes`,
// `compare` and the site: `slnt 0` (upright), `slnt -11`, `synth`.
import { test } from "node:test";
import assert from "node:assert/strict";
import { axis, synth, UPRIGHT, isUpright, key, label, token, pinCss, specLine } from "../src/outcome.mjs";

test("upright is the axis at zero, not a separate kind", () => {
  assert.deepEqual(UPRIGHT, { kind: "axis", axis: "slnt", value: 0 });
  assert.ok(isUpright(axis(0)) && isUpright(axis(-0)) && !isUpright(axis(-11)) && !isUpright(synth(14)));
  assert.equal(Object.is(axis(-0).value, 0), true); // never -0
});

test("labels, keys, file tokens and pinning CSS", () => {
  assert.equal(label(UPRIGHT), "slnt 0");
  assert.equal(label(axis(-11)), "slnt -11");
  assert.equal(label(synth(14)), "synth");
  assert.equal(key(axis(-11)), "slnt=-11");
  assert.equal(token(UPRIGHT), "slnt0");
  assert.equal(token(axis(-11)), "slnt-11");
  assert.equal(pinCss(UPRIGHT), "font-variation-settings: 'slnt' 0;");
  assert.equal(pinCss(axis(-5)), "font-variation-settings: 'slnt' -5;");
});

test("a cell's line: one outcome when decided, a slash list when open, axis first, axis name written once", () => {
  assert.deepEqual(specLine("specified", [axis(-11)]), { decided: true, text: "slnt -11" });
  assert.deepEqual(specLine("constrained", [UPRIGHT, synth(14)]), { decided: false, text: "slnt 0 / synth" });
  assert.deepEqual(specLine("unspecified", [synth(14), UPRIGHT, axis(-11)]), { decided: false, text: "slnt 0 / -11 / synth" });
});
