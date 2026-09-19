// Naming what a browser did from the lean of the glyph (px, forward positive; calibration from the manifest font).
import { test } from "node:test";
import assert from "node:assert/strict";
import { describeLean } from "../src/compare.mjs";
import { axis, synth, UPRIGHT } from "../src/outcome.mjs";

const font = { slnt: [-11, 11], glyphHeightPx: 88, pxPerSlntUnit: 1.4545 };
const cell = (allowed, mismatch = []) => ({ allowed, plan: { match: [], mismatch } });
const decided = cell([axis(-11)]);

test("upright, a real axis, a synthesized default skew", () => {
  assert.equal(describeLean(decided, 0, font), "slnt 0");
  assert.equal(describeLean(decided, 16, font, "pass"), "slnt -11");
  assert.equal(describeLean(cell([axis(-5)]), 7, font, "pass"), "slnt -5");
  assert.equal(describeLean(cell([axis(5)]), -7, font, "pass"), "slnt 5"); // backslant
  assert.equal(describeLean(cell([UPRIGHT, synth(14)]), 21, font, "pass"), "synth ~14°");
});

test("stacked: an axis value plus a default skew, in Chrome's and Safari's measurements", () => {
  assert.equal(describeLean(decided, 36, font, "fail"), "slnt -11 + synth"); // 16 + ~20
  assert.equal(describeLean(cell([axis(-5)]), 27, font, "fail"), "slnt -5 + synth"); // 7 + ~20
  assert.equal(describeLean(cell([axis(5)]), 13, font, "fail"), "slnt 5 + synth"); // -7 + ~20
});

test("a synthesized skew at the requested angle keeps its angle (Firefox on a normal face)", () => {
  const normalFace = cell([UPRIGHT, synth(45)], [axis(-11)]);
  assert.equal(describeLean(normalFace, 82, font, "pass"), "synth ~43°");
});

test("a pass against a forbidden axis rendering means the skew is synthesized, a fail means it is the axis", () => {
  const normalFace = cell([UPRIGHT, synth(5)], [axis(-5), axis(-11)]);
  assert.equal(describeLean(normalFace, 7, font, "pass"), "synth ~5°"); // same lean as slnt -5, but the reftest passed
  assert.equal(describeLean(normalFace, 7, font, "fail"), "slnt -5");
});

test("nothing measured, nothing said", () => {
  assert.equal(describeLean(decided, null, font), null);
});

test("a backslant synthesized skew is not mistaken for a stack (Firefox on a normal face, oblique -5deg)", () => {
  const normalFace = cell([UPRIGHT, synth(-5)], [axis(5), axis(-11)]);
  assert.equal(describeLean(normalFace, -7, font, "pass"), "synth ~-5\u00B0");
});

import { cellState, sameRendering } from "../src/compare.mjs";

const eng = (label, lean, ok = true) => ({ label, lean, ok });
const per = (c, f, s) => ({ chrome: c, firefox: f, safari: s });

test("interop state: fail beats differ, differ needs every engine allowed but not all the same", () => {
  const up = eng("slnt 0", 0);
  assert.equal(cellState(per(up, up, up)), "same");
  assert.equal(cellState(per(up, eng("synth ~10°", 15), up)), "differ");
  assert.equal(cellState(per(up, eng("slnt -11", 16, false), up)), "fail");
  assert.equal(cellState(per(up, eng("slnt -11", 16, false), eng("synth ~14°", 21))), "fail");
  assert.equal(cellState(per(up, up, eng(null, null, null))), "unknown");
});

test("two synthesized skews within a few px are the same rendering; a skew and upright are not", () => {
  assert.equal(sameRendering(eng("synth ~14°", 21), eng("synth ~15°", 22)), true);
  assert.equal(sameRendering(eng("synth ~14°", 21), eng("synth ~43°", 82)), false);
  assert.equal(sameRendering(eng("synth ~14°", 21), eng("slnt 0", 0)), false);
  assert.equal(sameRendering(eng("slnt -11", 16), eng("slnt -11", 16)), true);
});
