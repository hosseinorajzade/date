import {Easing, interpolate, random} from 'remotion';
import TL from './timeline.json';

export const FPS = TL.fps;
export const f = (sec: number) => Math.round(sec * FPS);

// Per-frame effect parameters for the video layer of a shot, driven by the nearest cut.
export type Fx = {
  tx: number;
  ty: number;
  scale: number;
  rot: number;
  blurX: number;
  blurY: number;
  zoomBlur: number; // 0..1 radial (scale) smear
  spinBlur: number; // 0..1 rotational smear
  rgb: number; // px channel split
  slices: number; // 0..1 horizontal slice displacement
  bright: number; // brightness multiplier
  seed: number;
};

const NONE: Fx = {tx: 0, ty: 0, scale: 1, rot: 0, blurX: 0, blurY: 0, zoomBlur: 0, spinBlur: 0, rgb: 0, slices: 0, bright: 1, seed: 0};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const easeIn = Easing.in(Easing.cubic);

// d = global frame - cut frame (negative: outgoing shot, >= 0: incoming shot)
const effectAt = (type: string, d: number, cut: number): Partial<Fx> | null => {
  const seed = cut * 31 + d;
  switch (type) {
    case 'open': {
      if (d < 0 || d > 16) return null;
      const p = 1 - d / 16;
      return {rgb: 28 * p * p, slices: d < 8 ? 1 - d / 8 : 0, bright: 1 + 1.4 * Math.max(0, 1 - d / 5), scale: 1 + 0.06 * p, seed};
    }
    case 'whipH':
    case 'whipV': {
      if (d < -6 || d > 6) return null;
      const p = d < 0 ? easeIn((d + 7) / 7) : easeIn(1 - d / 7);
      const dist = (d < 0 ? -1 : 1) * p * 620;
      const blur = p * 70;
      return type === 'whipH'
        ? {tx: dist, blurX: blur, scale: 1 + 0.12 * p}
        : {ty: dist, blurY: blur, scale: 1 + 0.12 * p};
    }
    case 'flash': {
      if (d < -3 || d > 6) return null;
      return {bright: 1 + 1.2 * Math.max(0, 1 - Math.abs(d) / 4)};
    }
    case 'zoomIn': {
      if (d < -7 || d > 7) return null;
      const p = d < 0 ? easeIn((d + 8) / 8) : easeIn(1 - d / 8);
      return {scale: 1 + (d < 0 ? 0.5 : 0.35) * p, zoomBlur: p, bright: 1 + 0.25 * p};
    }
    case 'glitch': {
      if (d < -5 || d > 7) return null;
      const p = 1 - Math.abs(d + 0.5) / 7;
      const on = random(`g${seed}`) > 0.35 || d === 0 || d === -1;
      return {rgb: on ? 22 * p : 4 * p, slices: on ? p : 0, tx: on ? (random(`gx${seed}`) - 0.5) * 40 * p : 0, bright: 1 + 0.3 * p, seed};
    }
    case 'sweep': {
      if (d < -3 || d > 3) return null;
      const p = 1 - Math.abs(d) / 4;
      return {blurX: 6 * p, bright: 1 + 0.5 * p};
    }
    case 'redFlash': {
      if (d < -3 || d > 8) return null;
      return {bright: 1 + 0.6 * Math.max(0, 1 - Math.abs(d) / 5), scale: 1 + 0.04 * Math.max(0, 1 - Math.abs(d) / 6)};
    }
    case 'spin': {
      if (d < -7 || d > 8) return null;
      const p = d < 0 ? easeIn((d + 8) / 8) : easeIn(1 - d / 9);
      return {rot: (d < 0 ? 16 : -16) * p, scale: 1 + 0.3 * p, spinBlur: p, zoomBlur: p * 0.4};
    }
    case 'glitchOut': {
      if (d < -7 || d > -1) return null;
      const p = (d + 8) / 8;
      const on = random(`go${seed}`) > 0.3;
      return {rgb: 30 * p, slices: on ? p : 0.3 * p, tx: (random(`gox${seed}`) - 0.5) * 60 * p, bright: on ? 1 + 0.8 * p : 0.6, seed};
    }
    default:
      return null;
  }
};

export const fxAt = (globalFrame: number): Fx => {
  const out: Fx = {...NONE, seed: globalFrame};
  for (const tr of TL.transitions) {
    const cut = f(tr.t);
    const e = effectAt(tr.type, globalFrame - cut, cut);
    if (!e) continue;
    out.tx += e.tx ?? 0;
    out.ty += e.ty ?? 0;
    out.scale *= e.scale ?? 1;
    out.rot += e.rot ?? 0;
    out.blurX = Math.max(out.blurX, e.blurX ?? 0);
    out.blurY = Math.max(out.blurY, e.blurY ?? 0);
    out.zoomBlur = Math.max(out.zoomBlur, e.zoomBlur ?? 0);
    out.spinBlur = Math.max(out.spinBlur, e.spinBlur ?? 0);
    out.rgb = Math.max(out.rgb, e.rgb ?? 0);
    out.slices = Math.max(out.slices, e.slices ?? 0);
    out.bright *= e.bright ?? 1;
    if (e.seed !== undefined) out.seed = e.seed;
  }
  return out;
};

// Overlay intensities (screen-space) for the frame.
export const overlaysAt = (g: number) => {
  let white = 0;
  let red = 0;
  let sweep: number | null = null;
  let lines = 0;
  for (const tr of TL.transitions) {
    const d = g - f(tr.t);
    if (tr.type === 'open') white = Math.max(white, interpolate(d, [0, 1, 7], [1, 0.9, 0], clamp));
    if (tr.type === 'flash') white = Math.max(white, interpolate(d, [-3, -1, 0, 2, 7], [0, 0.6, 1, 0.55, 0], clamp));
    if (tr.type === 'redFlash') {
      red = Math.max(red, interpolate(d, [-3, -1, 0, 3, 10], [0, 0.6, 1, 0.5, 0], clamp));
      white = Math.max(white, interpolate(d, [-1, 0, 2], [0, 0.55, 0], clamp));
    }
    if (tr.type === 'sweep' && d >= -9 && d <= 7) sweep = (d + 9) / 16;
    if ((tr.type === 'glitch' || tr.type === 'glitchOut' || tr.type === 'open') && d >= -6 && d <= 6) {
      lines = Math.max(lines, 1 - Math.abs(d) / 7);
    }
  }
  return {white, red, sweep, lines};
};

export {clamp};
