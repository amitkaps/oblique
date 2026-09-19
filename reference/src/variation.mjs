// CSS Fonts 4, "7.2 Feature and variation precedence" for the font-style step:
//   "The value applied is the closest matching value as determined by the font
//    matching algorithm. User agents must apply at most one value due to the
//    font-style property; both "ital" and "slnt" values must not be set together.
//    If the selected font is defined in an @font-face rule, then the values applied
//    at this step should be clamped to the value of the ... font-style descriptor ...
//    Then ... clamped (possibly again) to the values that are supported by the font."
// and 2.3: "the slnt variation is used to implement oblique values, and the ital
// variation with a value of 1 is used to implement the italic values", with the CSS
// angle and the OpenType slnt value having opposite signs (oblique 11deg -> slnt -11).
//
// The function returns every outcome the spec PERMITS, not a single guess: where the
// text leaves the value open the allowed set has more than one member and the reason
// is recorded in `notes` / `assumptions`.

import { ITALIC_AS_OBLIQUE_ANGLE, DEFAULT_OBLIQUE_ANGLE } from "./style.mjs";

export const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);

export const UPRIGHT = { kind: "upright" };
export const key = (o) =>
  o.kind === "upright" ? "upright" : o.kind === "synth" ? "synth" : `${o.axis}=${o.value}`;

/** CSS oblique angle -> outcome, through the font's own slnt range (sign flips). */
function slntOutcome(cssAngle, font) {
  if (!font.slnt) return UPRIGHT;
  const v = clamp(-cssAngle, font.slnt[0], font.slnt[1]);
  return v === 0 ? UPRIGHT : { kind: "axis", axis: "slnt", value: v };
}

function unique(outcomes) {
  const seen = new Set();
  return outcomes.filter((o) => (seen.has(key(o)) ? false : seen.add(key(o))));
}

/**
 * @param {object} match    result of matchFontStyle()
 * @param {{kind:string, angle:number|null}} request
 * @param {{slnt:number[]|null, ital:number[]|null}} font  the font file's own axes
 * @returns {{allowed:object[], notes:string[], assumptions:string[]}}
 */
export function resolveVariation(match, request, font) {
  const notes = [];
  const assumptions = [];
  const allowed = [];

  for (const face of match.faces) {
    const st = face.style;

    if (st.kind === "normal") {
      // A face declared normal is oblique 0deg; "the value for these font face style
      // attributes is used in place of the style implied by the underlying font data",
      // so whatever the font's slnt axis could do, the applied value is clamped to [0,0].
      notes.push("normal face: descriptor replaces the font data's style (4.4); applied value clamped to [0,0]");
      allowed.push(UPRIGHT);
    } else if (st.kind === "auto") {
      if (request.kind === "normal") {
        notes.push("auto face, normal request: selected as normal, applied value 0");
        allowed.push(UPRIGHT);
      } else if (request.kind === "oblique" && font.slnt) {
        // 4.4 scopes its two auto clauses separately: "for font selection purposes" the face is
        // selected as if normal, and "for variation axis clamping, clamping does not occur". So
        // the face is found as a normal face, but the value applied is the requested angle,
        // limited only by the font's own range. 5.2: "for variable fonts with a slnt axis, a
        // match is created by setting the slnt value with the specified oblique value";
        // geometric shearing is only the fallback when there is no axis. Upstream WPT
        // font-face-style-auto-variable.html and -default-variable.html assert the same
        // (auto applies the font's slant range; they pass on all three engines).
        notes.push("auto face, oblique request, font with slnt: the axis is set to the requested angle, limited by the font only (5.2, 4.4)");
        allowed.push(slntOutcome(request.angle, font));
      } else {
        // italic on an auto face is genuinely open: 5.2's italic steps never set slnt, the
        // face is a normal one, and "not required to distinguish italic from oblique" would
        // map italic 1 onto oblique 11deg. Upright, a synthesized skew and the axis all fit.
        assumptions.push("auto-italic: no step applies slnt for an italic request (5.2); UAs may map italic to oblique 11deg");
        allowed.push(UPRIGHT);
        if (request.kind === "oblique") allowed.push(slntOutcome(request.angle, font));
        else {
          allowed.push(slntOutcome(ITALIC_AS_OBLIQUE_ANGLE, font));
          allowed.push(slntOutcome(DEFAULT_OBLIQUE_ANGLE, font));
        }
      }
    } else if (st.kind === "italic") {
      if (font.ital) {
        notes.push("italic face on a font with an ital axis: the ital variation with value 1 implements italic (2.3)");
        allowed.push({ kind: "axis", axis: "ital", value: clamp(1, font.ital[0], font.ital[1]) });
      } else {
        // No ital axis: "ital ... is used to implement the italic values" leaves nothing to
        // apply. But 5.2 says UAs "are not required to distinguish between italic and
        // oblique" and then an italic value of 1 maps to oblique 11deg, which on a slnt
        // font is slnt -11. Both renderings are conformant.
        notes.push("italic face, no ital axis: nothing to set, or (UA not distinguishing italic/oblique, 5.2) italic 1 = oblique 11deg");
        allowed.push(UPRIGHT);
        allowed.push(slntOutcome(ITALIC_AS_OBLIQUE_ANGLE, font));
      }
    } else {
      // oblique face with descriptor range [lo, hi]; match.value is the closest value
      // the matching stage found (the requested angle when the range contains it).
      const { lo, hi } = st;
      if (request.kind === "italic") {
        // italic: "The angle and direction of slant is unspecified."
        notes.push("italic request on an oblique face: slant angle unspecified (2.3); use the stage's closest value or the 14deg default");
        for (const a of [match.value ?? ITALIC_AS_OBLIQUE_ANGLE, DEFAULT_OBLIQUE_ANGLE]) {
          allowed.push(slntOutcome(clamp(a, lo, hi), font));
        }
      } else {
        const a = match.kind === "oblique" && match.value !== null ? match.value : request.angle ?? 0;
        notes.push(`oblique face [${lo}, ${hi}]: closest matching value ${a}, clamped to the descriptor, then to the font`);
        allowed.push(slntOutcome(clamp(a, lo, hi), font));
      }
    }
  }

  if (match.faces.length > 1) assumptions.push("tie: more than one face remained; the UA may pick any");
  return { allowed: unique(allowed), notes, assumptions };
}
