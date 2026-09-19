// CSS Fonts 4, "5.2 Matching font styles": the font-style steps of the face
// selection algorithm, transcribed from reference/spec/css-fonts-4-excerpts.txt
// ("5.2 ... (verbatim)"). This module only SELECTS a face. Whether the result
// gets a variation applied or a synthetic skew is decided by variation.mjs and
// synthesis.mjs, never here (the spec's own stage text mentions synthesis, but
// keeping it out of selection keeps each rule testable on its own).
//
// Only the font-style stage is modelled; width and weight matching, and
// unicode-range composite faces, are out of scope.
//
// A "face" is { id, style } where style comes from parseDescriptor(). For
// matching, normal and auto faces have the oblique value 0, an oblique face
// has an oblique range [lo, hi], and an italic face has the italic value 1.
//
// Resolutions applied on top of the spec text (each is a documented deviation
// from the published Editor's Draft, off by default, listed in `RESOLUTIONS`):
//   noItalicFallbackForOblique - csswg-drafts#9389: a request for `oblique` must
//     not fall back to a face labelled `italic` when other faces exist. The ED
//     text still lists "italic values" stages in the oblique branches; WPT's
//     css-fonts/italic-oblique-fallback.html asserts the resolution instead.
//   obliqueOnlyDemotesRealObliqueFaces - csswg-drafts#9390: under `font-synthesis-style:
//     oblique-only` an italic request treats REAL oblique faces as a last resort too. The ED
//     text is about synthesized faces ("they must not be used as fallback"); WPT's
//     font-synthesis-style-oblique-only.html asserts the broader reading. csswg-drafts#9390 is still open and proposes to change `none` in the same way.

import { ITALIC_VALUE } from "./style.mjs";

export const RESOLUTIONS = {
  noItalicFallbackForOblique: {
    issue: "https://github.com/w3c/csswg-drafts/issues/9389",
    effect: "an oblique request does not select an italic-labelled face while any other face exists",
  },
  obliqueOnlyDemotesRealObliqueFaces: {
    issue: "https://github.com/w3c/csswg-drafts/issues/9390",
    effect: "with font-synthesis-style: oblique-only, an italic request tries real positive-oblique faces only after every other stage",
  },
};

const hasOblique = (f) => f.style.kind !== "italic";
const isItalic = (f) => f.style.kind === "italic";

/** Pick, among `faces`, those whose oblique range yields the best value under `bestOf`. */
function pick(faces, valueOf, better) {
  let best = null;
  let bestFaces = [];
  for (const f of faces) {
    const v = valueOf(f);
    if (v === null) continue;
    if (best === null || better(v, best)) {
      best = v;
      bestFaces = [f];
    } else if (v === best) {
      bestFaces.push(f);
    }
  }
  return best === null ? null : { value: best, faces: bestFaces };
}

const asc = (v, best) => v < best;
const desc = (v, best) => v > best;

// -- oblique stage primitives (all over faces that have an oblique value) ----------------

/** faces whose oblique range contains v */
function obContains(faces, v) {
  const hit = faces.filter((f) => hasOblique(f) && f.style.lo <= v && v <= f.style.hi);
  return hit.length ? { value: v, faces: hit } : null;
}
/** "oblique values >= v checked in ascending order" (v inclusive) */
function obAscendingFrom(faces, v) {
  return pick(faces.filter(hasOblique), (f) => (f.style.hi >= v ? Math.max(f.style.lo, v) : null), asc);
}
/** "oblique values above v in ascending order" (strictly above) */
function obAscendingAbove(faces, v) {
  return pick(faces.filter(hasOblique), (f) => (f.style.lo > v ? f.style.lo : null), asc);
}
/** "oblique values below v in descending order until 0 is hit. Only positive values" */
function obDescendingPositiveBelow(faces, v) {
  return pick(
    faces.filter(hasOblique),
    (f) => (f.style.hi < v && f.style.hi > 0 ? f.style.hi : null),
    desc,
  );
}
/** "oblique values less than or equal to 0 checked in descending order" */
function obDescendingAtMostZero(faces) {
  return pick(faces.filter(hasOblique), (f) => (f.style.lo <= 0 ? Math.min(f.style.hi, 0) : null), desc);
}
/** "oblique values less than 0deg are checked in descending order" (normal request) */
function obDescendingNegative(faces) {
  return pick(faces.filter(hasOblique), (f) => (f.style.hi < 0 ? f.style.hi : null), desc);
}

// -- italic stage: every italic face has the single italic value 1 ------------------------
function itHit(faces, { includesOne }) {
  if (!includesOne) return null;
  const hit = faces.filter(isItalic);
  return hit.length ? { value: ITALIC_VALUE, faces: hit } : null;
}

const mirror = (f) => ({
  ...f,
  style: f.style.kind === "italic" ? f.style : { ...f.style, lo: -f.style.hi, hi: -f.style.lo },
});

/**
 * Select a face for a font-style request.
 *
 * @param {{kind:'normal'|'italic'|'oblique', angle:number|null}} request  from parseRequest()
 * @param {{id:string, style:object}[]} faces                              style from parseDescriptor()
 * @param {{synthesisStyle?:'auto'|'none'|'oblique-only', resolutions?:object}} [opts]
 * @returns {{faces:object[], stage:string, kind:'oblique'|'italic'|'last-resort',
 *            value:number|null, tried:string[], assumptions:string[], ambiguous:boolean}}
 */
export function matchFontStyle(request, faces, opts = {}) {
  const synthesisStyle = opts.synthesisStyle ?? "auto";
  const res = { noItalicFallbackForOblique: false, obliqueOnlyDemotesRealObliqueFaces: false, ...(opts.resolutions ?? {}) };
  const tried = [];
  const assumptions = [];
  const stages = []; // [label, () => hit | null, kind]

  if (request.kind === "normal") {
    // "If the value of font-style is normal: oblique >= 0 ascending; italic >= 0
    // ascending; oblique < 0 descending; italic < 0 descending."
    stages.push(["normal: oblique >= 0 ascending", () => obAscendingFrom(faces, 0), "oblique"]);
    stages.push(["normal: italic >= 0 ascending", () => itHit(faces, { includesOne: true }), "italic"]);
    stages.push(["normal: oblique < 0 descending", () => obDescendingNegative(faces), "oblique"]);
  } else if (request.kind === "italic") {
    // "italic: contains the italic value; oblique >= 11deg ascending then below 11deg
    // descending (positive only); italic <= 0; oblique <= 0 descending." The "italic <= 0" stage
    // is not modelled: every italic face has the italic value 1, so it can never match.
    stages.push(["italic: italic faces", () => itHit(faces, { includesOne: true }), "italic"]);
    const positiveOblique = [
      "italic: oblique >= 11deg ascending, then < 11deg descending",
      () => obAscendingFrom(faces, 11) ?? obDescendingPositiveBelow(faces, 11),
      "oblique",
    ];
    // Resolution (off by default): 2.8.2 oblique-only, read as "real oblique faces must not be used
    // as fallback if italic is specified". WPT's oblique-last-resort-weight-selection.html treats
    // them as a last resort (still usable when nothing else exists), so the positive-oblique stage
    // moves to the end instead of disappearing. The normal face (oblique 0) keeps its place in the
    // <= 0 stage. Without the resolution the stage keeps its place, as the ED text has it.
    const demote = synthesisStyle === "oblique-only" && res.obliqueOnlyDemotesRealObliqueFaces;
    if (!demote) stages.push(positiveOblique);
    stages.push(["italic: oblique <= 0 descending", () => obDescendingAtMostZero(faces), "oblique"]);
    if (demote) {
      stages.push([positiveOblique[0] + " (last resort under oblique-only)", positiveOblique[1], "oblique"]);
    }
  } else {
    // oblique <angle>
    const negative = request.angle < 0;
    const a = negative ? -request.angle : request.angle;
    const fs = negative ? faces.map(mirror) : faces;
    const back = (hit) =>
      hit && negative ? { value: -hit.value, faces: hit.faces.map((f) => faces.find((o) => o.id === f.id)) } : hit;
    if (negative) assumptions.push("negative-angle: spec says only 'negated values and opposite directions'");

    stages.push([`oblique ${request.angle}: faces containing the angle`, () => back(obContains(fs, a)), "oblique"]);
    stages.push([
      `oblique ${request.angle}: nearest oblique ${a >= 11 ? "(above ascending, then below descending)" : "(below descending, then above ascending)"}`,
      () =>
        back(
          a >= 11
            ? obAscendingAbove(fs, a) ?? obDescendingPositiveBelow(fs, a)
            : obDescendingPositiveBelow(fs, a) ?? obAscendingAbove(fs, a),
        ),
      "oblique",
    ]);
    if (!res.noItalicFallbackForOblique) {
      stages.push([
        `oblique ${request.angle}: italic faces`,
        () => {
          const h = itHit(fs, { includesOne: true });
          if (h && a < 11) {
            // "italic values below 1 descending until 0, followed by italic values above 1":
            // neither range contains exactly 1, so the text never reaches an italic-1 face here.
            assumptions.push("italic-value-1-gap: the a<11 italic stage text excludes an italic value of exactly 1");
          }
          if (h && negative) assumptions.push("negative-angle-italic-stage: mirrored italic values are not defined");
          return h;
        },
        "italic",
      ]);
    }
    stages.push([`oblique ${request.angle}: oblique <= 0 descending`, () => back(obDescendingAtMostZero(fs)), "oblique"]);
  }

  for (const [label, run, kind] of stages) {
    tried.push(label);
    const hit = run();
    if (hit) {
      return {
        faces: hit.faces,
        stage: label,
        kind,
        value: hit.value,
        tried,
        assumptions,
        ambiguous: assumptions.length > 0 && faces.length > 1,
      };
    }
  }

  // Nothing matched (for example an italic-only family under the 9389 resolution, or
  // oblique-only excluding the only face): "If no matching face exists" is undefined
  // for the style stage, and WPT's oblique-request-italic-only-family-no-crash.html
  // only requires that the family still renders. Use every face, flagged.
  tried.push("last resort: every remaining face");
  return {
    faces: [...faces],
    stage: "last resort",
    kind: "last-resort",
    value: null,
    tried,
    assumptions: [...assumptions, "last-resort: the spec does not define selection when no stage matches"],
    ambiguous: faces.length > 1,
  };
}
