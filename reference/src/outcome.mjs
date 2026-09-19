// The vocabulary of an expectation, in one place.
//
// An outcome is what the glyph ends up as:
//   { kind: 'axis', axis: 'slnt', value: n }   the real axis is set to n (slnt 0 is upright)
//   { kind: 'synth', angle }                   a synthesized geometric skew (size is engine-specific)
// A real axis value AND a synthetic skew together ("stacked") is never an allowed outcome.
//
// Everything that names, files or draws an outcome goes through this module: the generator
// (test and reference files), the manifest the site reads, `classes`, and `compare`.
// The axis form is the common language on purpose: font-variation-settings: 'slnt' -11 is what
// every reference pins, and row 6 of the grid shows it works in every engine.

export const axis = (value, name = "slnt") => ({ kind: "axis", axis: name, value: value === 0 ? 0 : value }); // never -0
export const synth = (angle) => ({ kind: "synth", angle });

/** slnt 0: the glyph is not slanted. Not a separate kind, just the axis at zero. */
export const UPRIGHT = axis(0);
export const isUpright = (o) => o.kind === "axis" && o.axis === "slnt" && o.value === 0;

/** identity, for de-duplicating and comparing outcomes */
export const key = (o) => (o.kind === "synth" ? "synth" : `${o.axis}=${o.value}`);

/** short label: `slnt -11`, `slnt 0`, `synth` */
export const label = (o) => (o.kind === "synth" ? "synth" : `${o.axis} ${o.value}`);

/** longer label for comments in generated files */
export const describe = (o) => (o.kind === "synth" ? `synth (a synthesized ${o.angle}deg skew)` : label(o));

/** file-name token of a reference: slnt0, slnt-11 */
export const token = (o) => `${o.axis}${o.value}`;

/** CSS that pins the axis, which is how every reference is drawn */
export const pinCss = (o) => `font-variation-settings: '${o.axis}' ${o.value};`;

/**
 * The line a cell shows: what the reference expects, on one line.
 *   decided   the spec pins one outcome:            `slnt -11`
 *   open      it allows several (or forbids some):  `slnt 0 / -11 / synth`  (shown with a star)
 * Axis outcomes come first, then synth; a repeated axis name is written once.
 */
export function specLine(status, allowed) {
  const axes = allowed.filter((o) => o.kind === "axis");
  const parts = axes.map((o, i) => (i > 0 && o.axis === axes[i - 1].axis ? String(o.value) : label(o)));
  if (allowed.some((o) => o.kind === "synth")) parts.push("synth");
  return { decided: status === "specified", text: parts.join(" / ") };
}
