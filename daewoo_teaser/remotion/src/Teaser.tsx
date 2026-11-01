import React from 'react';
import {AbsoluteFill, interpolate, random, Sequence, useCurrentFrame} from 'remotion';
import {BottomGradient, Caption} from './Caption';
import {COPY} from './copy';
import {Ending} from './Ending';
import {RED, loadFonts} from './fonts';
import {clamp, f, overlaysAt} from './fx';
import {Shot} from './Shot';
import {CharismaBehind, DialBloom, NeonTrace, Typing} from './Specials';
import TL from './timeline.json';

loadFonts();

type Cam = (p: number) => {scale: number; x?: number; y?: number; rot?: number};
const lerp = (a: number, b: number) => (p: number) => a + (b - a) * p;
// gentle per-shot camera moves on top of the footage's own motion
const CAMERA: Record<string, Cam> = {
  s1: (p) => ({scale: lerp(1.0, 1.05)(p)}),
  s2: (p) => ({scale: lerp(1.05, 1.08)(p)}),
  s3: (p) => ({scale: lerp(1.0, 1.06)(p)}),
  s4: (p) => ({scale: lerp(1.05, 1.0)(p)}),
  s5: (p) => ({scale: lerp(1.0, 1.08)(p)}),
  s6: (p) => ({scale: lerp(1.0, 1.04)(p)}),
  s7: (p) => ({scale: lerp(1.02, 1.08)(p)}),
  s8: (p) => ({scale: lerp(1.06, 1.0)(p), rot: lerp(0, -2)(p)}),
  s9: (p) => ({scale: lerp(1.0, 1.05)(p)}),
  s10: (p) => ({scale: lerp(1.0, 1.12)(p)}),
};

const GradientFade: React.FC<{dur: number; strong?: boolean}> = ({dur, strong}) => {
  const fr = useCurrentFrame();
  const o = Math.min(interpolate(fr, [0, 8], [0, 1], clamp), interpolate(fr, [dur - 8, dur], [1, 0], clamp));
  return (
    <>
      <BottomGradient opacity={o} />
      {strong ? <BottomGradient opacity={o * 0.7} /> : null}
    </>
  );
};

const Overlays: React.FC = () => {
  const g = useCurrentFrame();
  const o = overlaysAt(g);
  return (
    <>
      {o.red > 0 ? <AbsoluteFill style={{background: RED, opacity: o.red * 0.75, mixBlendMode: 'screen'}} /> : null}
      {o.white > 0 ? <AbsoluteFill style={{background: '#fff', opacity: o.white}} /> : null}
      {o.sweep !== null ? (
        <AbsoluteFill style={{mixBlendMode: 'screen'}}>
          <div
            style={{
              position: 'absolute',
              top: -400,
              left: -300 + o.sweep * 1700,
              width: 70,
              height: 2800,
              transform: 'rotate(18deg)',
              background: 'linear-gradient(to right, rgba(227,0,27,0) 0%, rgba(255,60,70,0.9) 35%, #fff 50%, rgba(255,60,70,0.9) 65%, rgba(227,0,27,0) 100%)',
              boxShadow: `0 0 60px 30px rgba(227,0,27,0.65), 0 0 180px 90px rgba(227,0,27,0.35)`,
            }}
          />
        </AbsoluteFill>
      ) : null}
      {o.lines > 0.05 ? (
        <AbsoluteFill style={{mixBlendMode: 'screen', opacity: o.lines}}>
          {Array.from({length: 5}).map((_, i) => {
            const y = random(`ln${g}_${i}`) * 1920;
            const h = 2 + random(`lh${g}_${i}`) * 10;
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: 0,
                  right: 0,
                  top: y,
                  height: h,
                  background: i % 2 ? 'rgba(255,40,60,0.75)' : 'rgba(200,240,255,0.55)',
                }}
              />
            );
          })}
        </AbsoluteFill>
      ) : null}
    </>
  );
};

const Vignette: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.5) 100%)'}} />
);

export const Teaser: React.FC = () => {
  const ty = TL.typing;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {TL.shots
        .filter((s) => s.clip)
        .map((s) => {
          const from = f(s.start);
          const dur = f(s.end) - from;
          const trimBefore = f(s.clipOffset);
          let inCamera: ((l: number, g: number) => React.ReactNode) | undefined;
          if (s.id === 's2') inCamera = (l, g) => <CharismaBehind local={l} global={g} dur={dur} trimBefore={trimBefore} />;
          if (s.id === 's3') inCamera = (l) => <NeonTrace local={l} />;
          if (s.id === 's5') inCamera = (l) => <DialBloom local={l} />;
          return (
            <Sequence key={s.id} from={from} durationInFrames={dur} name={s.id}>
              <Shot clip={s.clip as string} trimBefore={trimBefore} startFrame={from} durationInFrames={dur} camera={CAMERA[s.id]} inCamera={inCamera} />
            </Sequence>
          );
        })}
      <Sequence from={0} durationInFrames={f(38)} name="vignette">
        <Vignette />
      </Sequence>
      {TL.titles.map((t) => {
        const c = COPY[t.key];
        const dur = f(t.out) - f(t.in);
        return (
          <Sequence key={t.key} from={f(t.in)} durationInFrames={dur} name={`title ${t.key}`}>
            <GradientFade dur={dur} strong={t.key === 'addItem'} />
            <Caption title={c.title} desc={c.desc} durationInFrames={dur} titleSize={c.size} />
          </Sequence>
        );
      })}
      <Sequence from={f(ty.start) - 6} durationInFrames={f(ty.out) - f(ty.start) + 6} name="typing gradient">
        <GradientFade dur={f(ty.out) - f(ty.start) + 6} />
      </Sequence>
      <Sequence from={f(ty.start)} durationInFrames={f(ty.out) - f(ty.start)} name="typing">
        <Typing text={ty.text} stepFrames={ty.step * TL.fps} dur={f(ty.out) - f(ty.start)} />
      </Sequence>
      <Sequence from={f(38)} durationInFrames={f(TL.total) - f(38)} name="ending">
        <Ending />
      </Sequence>
      <Overlays />
    </AbsoluteFill>
  );
};
