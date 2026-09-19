// Composes matching (match.mjs), variation (variation.mjs) and synthesis
// (synthesis.mjs) into the expectation for one test case.
//
// The result is an ALLOWED SET of outcomes, because the spec leaves latitude in
// places. An outcome is one of:
//   { kind: 'upright' }                          the glyph is not slanted
//   { kind: 'axis', axis: 'slnt', value: n }     the real axis is set
//   { kind: 'synth', angle }                     a synthesized geometric skew
// A real axis value AND a synthetic skew together ("stacked") is never allowed.
//
// A WPT reftest can only express two kinds of assertion: "matches one of these
// references" (OR) and "differs from all of these references" (AND). Upright and
// real-axis outcomes can be built as references; a synthesized skew cannot (its angle
// and centre differ per engine). So:
//   synthesis not allowed -> `match` refs for the constructible allowed outcomes
//   synthesis allowed     -> `mismatch` refs for the constructible outcomes NOT allowed
// and the case is `unspecified` (no WPT file) when nothing constructible is excluded.
//
// status:
//   specified    exactly one constructible outcome is allowed
//   constrained  several are allowed (or synthesis is), but something is excluded
//   unspecified  nothing testable is excluded; observed by the survey only

import { parseDescriptor, parseRequest, resolveSynthesisStyle } from "./style.mjs";
import { matchFontStyle } from "./match.mjs";
import { resolveVariation, UPRIGHT, key, clamp } from "./variation.mjs";
import { resolveSynthesis } from "./synthesis.mjs";

/**
 * @param {object} c
 * @param {{id:string, descriptor?:string|null}[]} c.faces   the @font-face rules of the family
 * @param {{slnt:number[]|null, ital:number[]|null}} c.font  axes of the font file
 * @param {string} c.request                                  the element's font-style
 * @param {{slnt?:number}|null} [c.fvs]                        an explicit font-variation-settings
 * @param {{fontSynthesis?:string, fontSynthesisStyle?:string}} [c.synthesis]
 * @param {object} [c.resolutions]                            see RESOLUTIONS in match.mjs
 */
export function expected(c) {
  const faces = c.faces.map((f) => ({ id: f.id, style: parseDescriptor(f.descriptor) }));
  const request = parseRequest(c.request);
  const synthesisStyle = resolveSynthesisStyle(c.synthesis ?? {});
  const font = { slnt: c.font.slnt ?? null, ital: c.font.ital ?? null };

  const match = matchFontStyle(request, faces, { synthesisStyle, resolutions: c.resolutions });
  const variation = resolveVariation(match, request, font);
  const synth = resolveSynthesis(request, faces, synthesisStyle, { font });

  const why = [`selected face ${match.faces.map((f) => f.id).join(", ")} (stage: ${match.stage})`, ...variation.notes];
  let allowed = [...variation.allowed];
  const assumptions = [...match.assumptions, ...variation.assumptions];

  if (c.fvs && c.fvs.slnt !== undefined) {
    // 7.2: font-variation-settings is applied after the font-style variations, so it wins;
    // only the font's own range still limits it.
    if (request.kind !== "normal") throw new Error("fvs combined with a non-normal request is not modelled");
    const v = font.slnt ? clamp(c.fvs.slnt, font.slnt[0], font.slnt[1]) : 0;
    allowed = [v === 0 ? UPRIGHT : { kind: "axis", axis: "slnt", value: v }];
    why.push("font-variation-settings is applied after the font-style variations (7.2), so it decides the axis");
  } else if (synth.eligible) {
    allowed.push({ kind: "synth", angle: synth.angle });
    if (!allowed.some((o) => o.kind === "upright")) allowed.push(UPRIGHT);
    why.push(`synthesis permitted: ${synth.reason}; not required (2.3 "will be generated" vs 5.2 "may create")`);
  } else if (request.kind !== "normal") {
    why.push(`no synthesis: ${synth.reason}`);
  }

  const hasSynth = allowed.some((o) => o.kind === "synth");
  const constructible = allowed.filter((o) => o.kind !== "synth");
  // the outcomes a reference can be built for: upright, the font's full forward slant (an engine
  // that saturates the axis), and the axis value THIS request would set if the descriptor were
  // ignored (an engine that applies the request where the face forbids it)
  const universe = [UPRIGHT];
  const addAxis = (o) => o.kind === "axis" && !universe.some((u) => key(u) === key(o)) && universe.push(o);
  if (font.slnt && font.slnt[0] < 0) addAxis({ kind: "axis", axis: "slnt", value: font.slnt[0] });
  for (const o of variation.requestedAxis) addAxis(o);
  const allowedKeys = new Set(allowed.map(key));

  let plan;
  let status;
  if (!hasSynth) {
    plan = { match: constructible, mismatch: [] };
    status = constructible.length === 1 ? "specified" : universe.every((u) => allowedKeys.has(key(u))) ? "unspecified" : "constrained";
  } else {
    const forbidden = universe.filter((u) => !allowedKeys.has(key(u)));
    plan = { match: [], mismatch: forbidden };
    status = forbidden.length ? "constrained" : "unspecified";
  }
  if (status === "unspecified") plan = { match: [], mismatch: [] };

  return {
    status,
    allowed,
    plan,
    selected: match.faces.map((f) => f.id),
    stage: match.stage,
    ambiguous: match.ambiguous || variation.assumptions.length > 0,
    assumptions,
    why,
  };
}
