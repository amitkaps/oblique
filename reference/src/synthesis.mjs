// CSS Fonts 4, "2.8.2 font-synthesis-style" and the style-synthesis sentences of
// 2.3 / 5.2.
//   2.3  oblique: "If no oblique faces exist, and font-synthesis-style has the value
//        auto, a synthetic oblique face will be generated."
//   5.2  "For families that lack any italic or oblique faces, user agents may create
//        artificial oblique faces, if this is permitted by the value of the
//        font-synthesis property."
//   2.8  "Variable fonts ... do not count as font synthesis and their use is not affected by the
//        font-synthesis property" (csswg-drafts 6f7c48d, #9391): font-synthesis: none never
//        disables a real axis, it only removes the synthesized outcome.
//   5.2  a variable font with a slnt axis matches an oblique request by setting the axis (this
//        ordering: csswg-drafts ac67b72, #9391; before it the axis match needed synthesis auto);
//        "otherwise" a fallback match is made by geometric shearing. So an auto face on a
//        font with slnt is never sheared for an oblique request (4.4: auto does not clamp).
//   2.8.2 none: not allowed. oblique-only: allowed, "but they must not be used as
//        fallback if italic is specified".
// 2.3 says "will be generated" and 5.2 says "may create": whether synthesis is
// mandatory is not settled by the text, so a synthesized skew is reported as PERMITTED
// (and an unsynthesized rendering also stays allowed), never as required.
// Synthesis on top of a REAL oblique match is never permitted: it is only for
// families that lack the face (4.4: "synthetic styling ... only ... in cases where
// the font descriptors imply this is needed").

import { DEFAULT_OBLIQUE_ANGLE } from "./style.mjs";

/**
 * @param {{kind:string, angle:number|null}} request
 * @param {{id:string, style:{kind:string}}[]} family  every face in the family
 * @param {'auto'|'none'|'oblique-only'} synthesisStyle
 * @param {{font?: {slnt: number[]|null}}} [opts]  the font file's axes
 * @returns {{eligible:boolean, angle:number, reason:string}}
 */
export function resolveSynthesis(request, family, synthesisStyle, opts = {}) {
  const angle = request.kind === "oblique" ? request.angle : DEFAULT_OBLIQUE_ANGLE;
  const no = (reason) => ({ eligible: false, angle, reason });

  if (request.kind === "normal") return no("a normal request needs no oblique");
  if (request.kind === "oblique" && request.angle === 0) return no("oblique 0deg is upright");
  if (synthesisStyle === "none") return no("font-synthesis-style: none forbids synthesis");
  if (request.kind === "italic" && synthesisStyle === "oblique-only") {
    return no("oblique-only: a synthesized oblique must not stand in for italic");
  }

  if (request.kind === "oblique" && opts.font?.slnt && family.some((f) => f.style.kind === "auto")) {
    return no("an auto face on a font with a slnt axis is matched by the axis; shearing is only the fallback (5.2)");
  }
  const hasOblique = family.some((f) => f.style.kind === "oblique");
  const hasItalic = family.some((f) => f.style.kind === "italic");
  if (request.kind === "oblique" && hasOblique) return no("an oblique face exists (2.3)");
  if (request.kind === "italic" && (hasOblique || hasItalic)) {
    return no("the family has an italic or oblique face (5.2)");
  }
  return {
    eligible: true,
    angle,
    reason: request.kind === "oblique" ? "no oblique face exists (2.3)" : "the family lacks italic and oblique faces (5.2)",
  };
}
