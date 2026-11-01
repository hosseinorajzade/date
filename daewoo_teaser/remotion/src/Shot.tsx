import React from 'react';
import {AbsoluteFill, OffthreadVideo, random, staticFile, useCurrentFrame} from 'remotion';
import {Fx, fxAt} from './fx';

// One shot: the clip plus camera motion and the cut effects (whip, zoom/spin smear, RGB split, slices).
// `inCamera` children share the clip's transform (things that must stick to the footage);
// `children` are drawn in screen space above it.
export const Shot: React.FC<{
  clip: string;
  trimBefore: number;
  startFrame: number; // global frame where this shot starts
  durationInFrames: number;
  camera: (p: number) => {scale: number; x?: number; y?: number; rot?: number};
  inCamera?: (local: number, global: number) => React.ReactNode;
  videoFilter?: string;
  children?: React.ReactNode;
}> = ({clip, trimBefore, startFrame, durationInFrames, camera, inCamera, videoFilter, children}) => {
  const local = useCurrentFrame();
  const g = startFrame + local;
  const fx: Fx = fxAt(g);
  const cam = camera(local / Math.max(1, durationInFrames - 1));
  const id = `s${startFrame}_${local}`;

  const transform = `translate(${fx.tx + (cam.x ?? 0)}px, ${fx.ty + (cam.y ?? 0)}px) rotate(${fx.rot + (cam.rot ?? 0)}deg) scale(${fx.scale * cam.scale})`;
  const filters: string[] = [];
  if (fx.blurX > 0.5 || fx.blurY > 0.5) filters.push(`url(#blur_${id})`);
  if (fx.rgb > 0.5) filters.push(`url(#rgb_${id})`);
  if (fx.bright !== 1) filters.push(`brightness(${fx.bright.toFixed(3)})`);
  if (videoFilter) filters.push(videoFilter);

  const video = (style?: React.CSSProperties) => (
    <OffthreadVideo src={staticFile(`clips/${clip}`)} trimBefore={trimBefore} muted style={{width: 1080, height: 1920, ...style}} />
  );

  // radial / rotational smear: stacked copies at slightly larger scale or angle
  const smear: React.ReactNode[] = [];
  const nSmear = fx.zoomBlur > 0.05 || fx.spinBlur > 0.05 ? 5 : 0;
  for (let i = 1; i <= nSmear; i++) {
    const s = 1 + i * 0.045 * fx.zoomBlur;
    const r = i * 2.2 * fx.spinBlur;
    smear.push(
      <AbsoluteFill key={`sm${i}`} style={{opacity: 0.42 / i ** 0.7, transform: `rotate(${r}deg) scale(${s})`}}>
        {video()}
      </AbsoluteFill>,
    );
  }

  // glitch slices: horizontal bands offset sideways
  const slices: React.ReactNode[] = [];
  if (fx.slices > 0.05) {
    const n = 7;
    for (let i = 0; i < n; i++) {
      const r1 = random(`sl${fx.seed}_${i}`);
      if (r1 < 0.35) continue;
      const top = random(`st${fx.seed}_${i}`) * 92;
      const h = 2 + random(`sh${fx.seed}_${i}`) * 9;
      const dx = (random(`sx${fx.seed}_${i}`) - 0.5) * 220 * fx.slices;
      slices.push(
        <AbsoluteFill
          key={`sl${i}`}
          style={{clipPath: `inset(${top}% 0 ${Math.max(0, 100 - top - h)}% 0)`, transform: `translateX(${dx}px)`}}
        >
          {video({filter: i % 2 ? 'hue-rotate(-20deg) saturate(1.6)' : 'brightness(1.4)'})}
        </AbsoluteFill>,
      );
    }
  }

  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <svg width="0" height="0" style={{position: 'absolute'}}>
        <defs>
          <filter id={`blur_${id}`} x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation={`${fx.blurX.toFixed(1)} ${fx.blurY.toFixed(1)}`} />
          </filter>
          <filter id={`rgb_${id}`} colorInterpolationFilters="sRGB">
            <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
            <feOffset in="r" dx={fx.rgb} dy={fx.rgb * 0.15} result="r2" />
            <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g" />
            <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b" />
            <feOffset in="b" dx={-fx.rgb} dy={-fx.rgb * 0.15} result="b2" />
            <feBlend in="r2" in2="g" mode="screen" result="rg" />
            <feBlend in="rg" in2="b2" mode="screen" />
          </filter>
        </defs>
      </svg>
      <AbsoluteFill style={{transform, transformOrigin: '50% 50%'}}>
        <AbsoluteFill style={{filter: filters.join(' ') || undefined}}>
          {video()}
          {smear}
          {slices}
        </AbsoluteFill>
        {inCamera ? inCamera(local, g) : null}
      </AbsoluteFill>
      {children}
    </AbsoluteFill>
  );
};
