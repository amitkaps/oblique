// The reference must agree with what upstream WPT tests INTEND, read from each test's
// own comments and reference file (not from how browsers happen to render them: several
// of these tests fail on some engines, see results/upstream.json). Where the reference
// and a test disagree, that is recorded below as a known disagreement with the reason,
// not silently bent to fit.
import { test } from "node:test";
import assert from "node:assert/strict";
import { matchFontStyle } from "../src/match.mjs";
import { parseDescriptor, parseRequest, resolveSynthesisStyle } from "../src/style.mjs";

const face = (id, descriptor) => ({ id, style: parseDescriptor(descriptor) });
const pick = (request, faces, opts) => matchFontStyle(parseRequest(request), faces, opts).faces.map((f) => f.id);

// css/css-fonts/italic-oblique-fallback.html (asserts csswg-drafts#9389:
// "request for 'oblique' style should not fall back to a face labelled 'italic'")
test("italic-oblique-fallback.html: family with normal + oblique faces", () => {
  const fam = [face("normal", "normal"), face("oblique", "oblique")];
  assert.deepEqual(pick("oblique", fam), ["oblique"]);
  assert.deepEqual(pick("italic", fam), ["oblique"]); // italic falls back to oblique
});
test("italic-oblique-fallback.html: normal + italic faces (resolution 9389 on)", () => {
  const fam = [face("normal", "normal"), face("italic", "italic")];
  const res = { resolutions: { noItalicFallbackForOblique: true } };
  assert.deepEqual(pick("italic", fam, res), ["italic"]);
  assert.deepEqual(pick("oblique", fam, res), ["normal"]); // must NOT fall back to italic
});
test("italic-oblique-fallback.html: the published Editor's Draft text alone disagrees (documented)", () => {
  const fam = [face("normal", "normal"), face("italic", "italic")];
  // without the resolution the ED's oblique branch still lists an italic stage before oblique <= 0
  assert.deepEqual(pick("oblique", fam), ["italic"]);
});
test("italic-oblique-fallback.html: an italic-only family is used for every request", () => {
  const fam = [face("italic", "italic")];
  const res = { resolutions: { noItalicFallbackForOblique: true } };
  assert.deepEqual(pick("italic", fam, res), ["italic"]);
  assert.deepEqual(pick("oblique", fam, res), ["italic"]); // last resort, must not crash
});

// css/css-fonts/font-synthesis-style-oblique-only.html
test("font-synthesis-style-oblique-only.html: normal + oblique family", () => {
  const fam = [face("A", "normal"), face("B", "oblique")];
  const syn = (fontSynthesisStyle) => ({ synthesisStyle: resolveSynthesisStyle({ fontSynthesisStyle }) });
  assert.deepEqual(pick("normal", fam, syn("auto")), ["A"]);
  assert.deepEqual(pick("oblique", fam, syn("auto")), ["B"]);
  assert.deepEqual(pick("italic", fam, syn("auto")), ["B"]); // italic falls back to oblique
  assert.deepEqual(pick("italic", fam, syn("none")), ["B"]); // none: still a real-face fallback
  assert.deepEqual(pick("italic", fam, syn("oblique-only")), ["A"]); // oblique-only blocks it
});

// css/css-fonts/oblique-last-resort-weight-selection.html
// The test's comments say both faces must SURVIVE the slope filter for italic +
// oblique-only, because an italic request is treated as a 14deg slope (clamp(14, min, max):
// face1 [14,30] -> 14, face2 [5,14] -> 14). The spec text says oblique >= 11deg
// ascending: face1 yields 14, face2 (contains 11) yields 11, so only face2 survives.
test("oblique-last-resort-weight-selection.html: KNOWN DISAGREEMENT with the spec text", () => {
  const fam = [face("face1", "oblique 14deg 30deg"), face("face2", "oblique 5deg 14deg")];
  const got = pick("italic", fam, { synthesisStyle: "oblique-only" });
  assert.deepEqual(got, ["face2"], "the ED's 11deg threshold selects face2 alone");
  // the test intends both faces to survive (so weight can pick face1). Recorded, not fitted.
});
