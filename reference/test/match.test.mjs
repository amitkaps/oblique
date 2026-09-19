// Rule-by-rule tests of matchFontStyle, each built from the spec text in
// reference/spec/css-fonts-4-excerpts.txt ("5.2 ... (verbatim)"). Faces are named for
// what they are; the assertion is the order the spec's stages pick them.
import { test } from "node:test";
import assert from "node:assert/strict";
import { matchFontStyle } from "../src/match.mjs";
import { parseDescriptor, parseRequest } from "../src/style.mjs";

const face = (id, descriptor) => ({ id, style: parseDescriptor(descriptor) });
const pick = (request, faces, opts) => matchFontStyle(parseRequest(request), faces, opts).faces.map((f) => f.id);

/** Repeatedly eliminate the selected face; returns the order the spec would choose them. */
function order(request, faces, opts) {
  const out = [];
  let rest = [...faces];
  while (rest.length) {
    const chosen = pick(request, rest, opts);
    out.push(chosen[0]);
    rest = rest.filter((f) => f.id !== chosen[0]);
  }
  return out;
}

test("oblique request >= 11deg: above ascending, then below descending, then italic, then oblique <= 0", () => {
  // shaped like the spec's "oblique 40deg" example: D, E, C, then italic, then B, then A
  const family = [
    face("A", "oblique -10deg"),
    face("B", "oblique -5deg"),
    face("C", "oblique 30deg"),
    face("D", "oblique 45deg"),
    face("E", "oblique 60deg"),
    face("I", "italic"),
  ];
  assert.deepEqual(order("oblique 40deg", family), ["D", "E", "C", "I", "B", "A"]);
});

test("oblique request in [0, 11): below descending, then above ascending, then italic, then oblique <= 0", () => {
  const family = [face("N", "normal"), face("L", "oblique 3deg"), face("H", "oblique 8deg"), face("I", "italic")];
  assert.deepEqual(order("oblique 5deg", family), ["L", "H", "I", "N"]);
});

test("a face whose range contains the requested angle wins outright", () => {
  const family = [face("N", "normal"), face("R", "oblique -11deg 11deg"), face("P", "oblique 10deg")];
  assert.deepEqual(pick("oblique 10deg", family), ["R", "P"]); // both contain 10 -> a tie, later stages decide
  assert.deepEqual(pick("oblique 0deg", family), ["N", "R"]);
});

test("the bare keyword is 14deg, so a face declared oblique (14deg) satisfies it", () => {
  assert.deepEqual(pick("oblique", [face("N", "normal"), face("O", "oblique")]), ["O"]);
  assert.deepEqual(pick("oblique", [face("N", "normal"), face("R", "oblique -11deg 11deg")]), ["R"]); // nearest: 11
});

test("normal request: oblique >= 0 ascending, italic, oblique < 0 descending", () => {
  const family = [face("O20", "oblique 20deg"), face("I", "italic"), face("Om5", "oblique -5deg"), face("Om9", "oblique -9deg")];
  assert.deepEqual(order("normal", family), ["O20", "I", "Om5", "Om9"]);
});

test("italic request: italic first, then oblique >= 11 ascending / below descending, then oblique <= 0", () => {
  assert.deepEqual(pick("italic", [face("N", "normal"), face("I", "italic")]), ["I"]);
  assert.deepEqual(pick("italic", [face("N", "normal"), face("O5", "oblique 5deg")]), ["O5"]);
  assert.deepEqual(pick("italic", [face("O5", "oblique 5deg"), face("O15", "oblique 15deg")]), ["O15"]);
  assert.deepEqual(pick("italic", [face("N", "normal")]), ["N"]);
});

test("negative angles mirror the positive steps with opposite directions", () => {
  const family = [face("R", "oblique -11deg 0deg"), face("N", "normal"), face("P", "oblique 5deg")];
  assert.deepEqual(pick("oblique -8deg", family), ["R"]);
  const far = [face("N", "normal"), face("P", "oblique 5deg"), face("M", "oblique -20deg")];
  assert.deepEqual(pick("oblique -8deg", far), ["M"]);
});

test("a reversed descriptor range is accepted and ordered (range-descriptor-reversed.html)", () => {
  assert.deepEqual(pick("oblique 5deg", [face("R", "oblique 10deg 0deg")]), ["R"]);
});

test("auto and an omitted descriptor are selected as if normal", () => {
  assert.deepEqual(pick("normal", [face("A", undefined), face("O", "oblique 10deg")]), ["A"]);
  assert.deepEqual(pick("oblique 10deg", [face("A", "auto"), face("O", "oblique 10deg")]), ["O"]);
});

test("the matching set that remains keeps every face containing the found value", () => {
  const family = [face("R1", "oblique 0deg 20deg"), face("R2", "oblique 10deg 30deg")];
  assert.deepEqual(pick("oblique 15deg", family), ["R1", "R2"]);
});

test("italic-value-1 gap: reaching an italic face from an oblique < 11 request is flagged", () => {
  const r = matchFontStyle(parseRequest("oblique 5deg"), [face("N", "normal"), face("I", "italic")].slice(1).concat(face("Z", "oblique -3deg")));
  assert.equal(r.faces[0].id, "I");
  assert.ok(r.assumptions.some((a) => a.startsWith("italic-value-1-gap")));
});
