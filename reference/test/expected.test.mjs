// The reference's verdict for the single-face Cairo grid, cell by cell, with the
// clause that decides each. These pin down the reasoning, not the browsers.
import { test } from "node:test";
import assert from "node:assert/strict";
import { expected } from "../src/expected.mjs";

const font = { slnt: [-11, 11], ital: null };
const run = (descriptor, request, extra = {}) =>
  expected({ faces: [{ id: "f", descriptor }], font, request, ...extra });
const keys = (e) => e.allowed.map((o) => (o.kind === "axis" ? `slnt=${o.value}` : o.kind)).sort();

test("normal request: a normal, auto or in-range face is upright; a face declared oblique 14deg is not", () => {
  assert.deepEqual(keys(run("normal", "normal")), ["slnt=0"]);
  assert.deepEqual(keys(run(undefined, "normal")), ["slnt=0"]);
  assert.deepEqual(keys(run("oblique -11deg 11deg", "normal")), ["slnt=0"]);
  // bare oblique = a one-point range at 14deg: the closest value to 0 is 14, then the font limits it to -11
  assert.deepEqual(keys(run("oblique", "normal")), ["slnt=-11"]);
  assert.equal(run("oblique", "normal").status, "specified");
});

test("a normal-declared face never reaches the real axis, whatever the font can do", () => {
  for (const request of ["italic", "oblique", "oblique 11deg"]) {
    const e = run("normal", request);
    assert.ok(!keys(e).includes("slnt=-11"), request);
    assert.deepEqual(keys(e), ["slnt=0", "synth"], request); // synthesis permitted, not required
    assert.equal(e.status, "constrained");
    assert.deepEqual(e.plan.mismatch.map((o) => o.kind + (o.value ?? "")), ["axis-11"]);
  }
});

test("font-synthesis-style: none removes the synthesized outcome, leaving upright only", () => {
  const e = run("normal", "oblique 11deg", { synthesis: { fontSynthesisStyle: "none" } });
  assert.deepEqual(keys(e), ["slnt=0"]);
  const s = run("normal", "italic", { synthesis: { fontSynthesis: "weight" } }); // no `style` token
  assert.deepEqual(keys(s), ["slnt=0"]);
});

test("oblique-only forbids synthesizing for italic but allows it for oblique", () => {
  assert.deepEqual(keys(run("normal", "italic", { synthesis: { fontSynthesisStyle: "oblique-only" } })), ["slnt=0"]);
  assert.deepEqual(keys(run("normal", "oblique", { synthesis: { fontSynthesisStyle: "oblique-only" } })), ["slnt=0", "synth"]);
});

test("a range face reaches the axis at the clamped value and is never synthesized on top", () => {
  for (const request of ["italic", "oblique", "oblique 11deg", "oblique 14deg", "oblique 45deg"]) {
    const e = run("oblique -11deg 11deg", request);
    assert.deepEqual(keys(e), ["slnt=-11"], request);
    assert.equal(e.status, "specified");
  }
  assert.deepEqual(keys(run("oblique -11deg 11deg", "oblique -8deg")), ["slnt=8"]); // the sign flips
  assert.deepEqual(keys(run("oblique -11deg 11deg", "oblique 5deg")), ["slnt=-5"]);
});

test("an italic-declared face on a slnt-only font permits upright or the axis (5.2: italic 1 = oblique 11deg)", () => {
  const e = run("italic", "italic");
  assert.deepEqual(keys(e), ["slnt=-11", "slnt=0"]);
  assert.equal(e.status, "unspecified");
});

test("an auto face on a slnt font: an oblique request sets the axis to the requested angle, unclamped by the descriptor, never sheared", () => {
  // 4.4: auto selects "as if normal" but "clamping does not occur"; 5.2: a slnt font matches by the axis
  for (const [request, slnt] of [["oblique", -11], ["oblique 11deg", -11], ["oblique 10deg", -10], ["oblique 5deg", -5], ["oblique 45deg", -11], ["oblique -5deg", 5], ["oblique -11deg", 11]]) {
    const e = run(undefined, request);
    assert.deepEqual(keys(e), [`slnt=${slnt}`], request);
    assert.equal(e.status, "specified", request);
    assert.equal(e.allowed.some((o) => o.kind === "synth"), false, request);
  }
  assert.deepEqual(keys(run(undefined, "oblique 0deg")), ["slnt=0"]);
  assert.equal(run(undefined, "normal").status, "specified");
});

test("an auto face and an italic request stays open: upright, the axis, or a synthesized skew", () => {
  const e = run(undefined, "italic");
  assert.deepEqual(keys(e), ["slnt=-11", "slnt=0", "synth"]);
  assert.equal(e.status, "unspecified");
});

test("an auto face on a font WITHOUT a slnt axis is a normal face: shearing is the only oblique", () => {
  const e = expected({ faces: [{ id: "f", descriptor: undefined }], font: { slnt: null, ital: null }, request: "oblique 10deg" });
  assert.deepEqual(keys(e), ["slnt=0", "synth"]);
});

test("font-variation-settings wins over the font-style variations (7.2)", () => {
  for (const d of [undefined, "normal", "italic", "oblique", "oblique -11deg 11deg"]) {
    assert.deepEqual(keys(run(d, "normal", { fvs: { slnt: -11 } })), ["slnt=-11"], String(d));
  }
  assert.deepEqual(keys(run("normal", "normal", { fvs: { slnt: -40 } })), ["slnt=-11"]); // the font still limits it
});

test("an ital-axis font: an italic face sets ital 1, and an oblique request never uses ital", () => {
  const f = { slnt: null, ital: [0, 1] };
  const e = expected({ faces: [{ id: "f", descriptor: "italic" }], font: f, request: "italic" });
  assert.deepEqual(e.allowed, [{ kind: "axis", axis: "ital", value: 1 }]);
});

test("font-synthesis never disables a real axis: variable fonts do not count as synthesis (2.8, csswg-drafts 6f7c48d)", () => {
  for (const [descriptor, request] of [[undefined, "oblique"], ["oblique", "oblique"], ["oblique -11deg 11deg", "oblique"], ["oblique -11deg 11deg", "italic"]]) {
    for (const synthesis of [{ fontSynthesis: "none" }, { fontSynthesisStyle: "none" }]) {
      const e = run(descriptor, request, { synthesis });
      assert.deepEqual(keys(e), ["slnt=-11"], `${descriptor} ${request} ${JSON.stringify(synthesis)}`);
    }
  }
});

test("C (normal-declared) oblique requests are a recorded hedge: the axis is forbidden, upright or synthesized is allowed", () => {
  // The literal 5.2 text (slnt match first, shearing only "Otherwise") would make these upright only;
  // csswg-drafts#7999's author scopes the no-synthesis intent to declarations that do not restrict the
  // range to 0. Text and intent disagree, so neither is asserted (docs/findings.md, "Open").
  for (const request of ["oblique", "oblique 5deg", "oblique 45deg", "oblique -5deg"]) {
    assert.deepEqual(keys(run("normal", request)), ["slnt=0", "synth"], request);
  }
});

test("italic on a face with an oblique range applies the stage's closest value, never the 14deg keyword default (7.2)", () => {
  // A wider range would let 14deg through if it were a second candidate; the font's own limit hides it here
  const wide = expected({ faces: [{ id: "f", descriptor: "oblique -20deg 20deg" }], font: { slnt: [-30, 30], ital: null }, request: "italic" });
  assert.deepEqual(keys(wide), ["slnt=-11"]);
  assert.equal(wide.status, "specified");
});

test("italic + oblique-only against a face with a real oblique range: the range face is still the match (ED text)", () => {
  // The demotion of real oblique faces is csswg-drafts#9390, a resolution that is off by default.
  const oo = { synthesis: { fontSynthesisStyle: "oblique-only" } };
  for (const [descriptor, want] of [["oblique -11deg 11deg", "slnt=-11"], ["oblique -20deg 20deg", "slnt=-11"], ["oblique -5deg 5deg", "slnt=-5"]]) {
    const e = run(descriptor, "italic", oo);
    assert.deepEqual(keys(e), [want], descriptor);
    assert.equal(e.status, "specified", descriptor);
  }
  // with the resolution on the range face falls to the <= 0 stage and applies 0
  const on = expected({ faces: [{ id: "f", descriptor: "oblique -11deg 11deg" }], font, request: "italic", ...oo, resolutions: { obliqueOnlyDemotesRealObliqueFaces: true } });
  assert.deepEqual(keys(on), ["slnt=0"]);
});

test("italic on an auto face maps to 11deg at most, never the 14deg keyword default", () => {
  const wideFont = { slnt: [-20, 20], ital: null };
  const e = expected({ faces: [{ id: "f", descriptor: undefined }], font: wideFont, request: "italic" });
  assert.deepEqual(keys(e), ["slnt=-11", "slnt=0", "synth"]);
  assert.equal(e.status, "constrained");
});
