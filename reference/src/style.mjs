// Parsing of font-style values into the form the matching algorithm works on.
//
// Spec (CSS Fonts 4, reference/spec/css-fonts-4-excerpts.txt, "2.3 font-style"):
//   normal   -> a normal face; "This represents an oblique value of 0."
//   italic   -> an italic face
//   oblique <angle>?  -> "The lack of an <angle> represents 14deg."
// and for the @font-face descriptor (4.4): oblique <angle>{1,2} is a range, one
// angle is a range with identical endpoints, and `auto` is "selected as if the
// appropriate normal value is chosen" with "clamping does not occur".

export const DEFAULT_OBLIQUE_ANGLE = 14;
// 5.2: "an italic value of 1 must map to the same value that an oblique angle of
// 11deg maps to" (for UAs that do not distinguish italic from oblique).
export const ITALIC_VALUE = 1;
export const ITALIC_AS_OBLIQUE_ANGLE = 11;

const ANGLE = /^(-?\d+(?:\.\d+)?)deg$/;

function angle(token) {
  const m = ANGLE.exec(token);
  if (!m) throw new Error(`not an <angle>: ${JSON.stringify(token)}`);
  return Number(m[1]);
}

/**
 * Parse an @font-face font-style descriptor value. `undefined`/null means the
 * descriptor was omitted, which is defined as `auto`.
 * Returns { kind: 'auto'|'normal'|'italic'|'oblique', lo, hi }. lo/hi is the
 * oblique range in degrees (normal and auto count as oblique 0deg for matching).
 */
export function parseDescriptor(value) {
  if (value === undefined || value === null || value === "auto") {
    return { kind: "auto", lo: 0, hi: 0, source: value ?? "(omitted)" };
  }
  const t = value.trim().split(/\s+/);
  if (t[0] === "normal" && t.length === 1) return { kind: "normal", lo: 0, hi: 0, source: value };
  if (t[0] === "italic" && t.length === 1) return { kind: "italic", lo: 0, hi: 0, source: value };
  if (t[0] === "oblique") {
    if (t.length === 1) return { kind: "oblique", lo: 14, hi: 14, source: value };
    if (t.length <= 3) {
      const a = angle(t[1]);
      const b = t.length === 3 ? angle(t[2]) : a;
      // range-descriptor-reversed.html: a reversed range is accepted and ordered.
      return { kind: "oblique", lo: Math.min(a, b), hi: Math.max(a, b), source: value };
    }
  }
  throw new Error(`unsupported font-style descriptor: ${JSON.stringify(value)}`);
}

/** Parse the element's font-style. Returns { kind: 'normal'|'italic'|'oblique', angle }. */
export function parseRequest(value) {
  const t = value.trim().split(/\s+/);
  if (t[0] === "normal" && t.length === 1) return { kind: "normal", angle: 0, source: value };
  if (t[0] === "italic" && t.length === 1) return { kind: "italic", angle: null, source: value };
  if (t[0] === "oblique" && t.length === 1) {
    return { kind: "oblique", angle: DEFAULT_OBLIQUE_ANGLE, source: value };
  }
  if (t[0] === "oblique" && t.length === 2) return { kind: "oblique", angle: angle(t[1]), source: value };
  throw new Error(`unsupported font-style: ${JSON.stringify(value)}`);
}

/**
 * font-synthesis shorthand + font-synthesis-style longhand -> the style setting
 * that matters here: 'auto' | 'none' | 'oblique-only'.
 * (2.8.2: auto | none | oblique-only, initial auto. In the shorthand a `style`
 * keyword allows style synthesis and its absence, or `none`, disables it.)
 */
export function resolveSynthesisStyle({ fontSynthesis, fontSynthesisStyle } = {}) {
  if (fontSynthesisStyle) return fontSynthesisStyle;
  if (fontSynthesis === undefined || fontSynthesis === null) return "auto";
  const tokens = fontSynthesis.trim().split(/\s+/);
  if (tokens.includes("none")) return "none";
  return tokens.includes("style") ? "auto" : "none";
}
