import React from 'react';
import {AbsoluteFill, Easing, interpolate, interpolateColors, OffthreadVideo, random, staticFile, useCurrentFrame} from 'remotion';
import machinePolys from './machinePolys.json';
import s3Logo from './s3Logo.json';
import {EN, RED} from './fonts';
import {clamp} from './fx';

const polys = machinePolys as Record<string, number[][]>;

// S2: "Charisma" in big red neon, slightly blurred, sitting BEHIND the machine.
// Drawn over the footage, then the machine itself (same frame, clipped to its silhouette) is laid back on top.
export const CharismaBehind: React.FC<{local: number; global: number; dur: number; trimBefore: number}> = ({local, global, dur, trimBefore}) => {
  // neon-tube ignition flicker, then steady; fades and lifts out before the whip
  const flicker = [0, 1, 0.15, 0.9, 0.3, 1, 0.7, 1];
  const ign = local < flicker.length ? flicker[local] : 1;
  const out = interpolate(local, [dur - 15, dur - 6], [1, 0], clamp);
  const hum = 0.93 + 0.07 * random(`hum${Math.floor(local / 2)}`);
  const top = 362 - local * 0.9;
  const scale = 1 + local * 0.0005;
  const poly = polys[String(global)];
  return (
    <>
      <AbsoluteFill style={{mixBlendMode: 'screen', opacity: ign * out * hum}}>
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top,
            textAlign: 'center',
            fontFamily: EN,
            fontWeight: 900,
            fontSize: 200,
            lineHeight: 1,
            letterSpacing: 6,
            color: RED,
            transform: `scale(${scale})`,
            filter: `blur(${2.5 + (1 - out) * 10}px)`,
            textShadow: `0 0 14px ${RED}, 0 0 40px ${RED}, 0 0 90px rgba(227,0,27,0.75), 0 0 160px rgba(227,0,27,0.45)`,
          }}
        >
          Charisma
        </div>
      </AbsoluteFill>
      {poly && local < dur - 6 ? (
        <AbsoluteFill style={{clipPath: `polygon(${poly.map(([x, y]) => `${x}px ${y}px`).join(',')})`}}>
          <OffthreadVideo src={staticFile('clips/s12.mp4')} trimBefore={trimBefore} muted style={{width: 1080, height: 1920}} />
        </AbsoluteFill>
      ) : null}
    </>
  );
};

// S3: a red neon line drawn around the panel logo, following it as the camera slides.
const logoBoxes = s3Logo as (number[] | null)[];
export const NeonTrace: React.FC<{local: number}> = ({local}) => {
  const b = logoBoxes[Math.min(local, logoBoxes.length - 1)];
  if (!b) return null;
  const padX = 34;
  const padY = 26;
  const x = b[0] - padX;
  const y = b[1] - padY;
  const w = b[2] - b[0] + padX * 2;
  const h = b[3] - b[1] + padY * 2;
  const P = 2 * (w + h);
  const draw = interpolate(local, [6, 30], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const fade = interpolate(local, [60, 78], [1, 0], clamp);
  const flick = local < 10 ? (local % 3 === 1 ? 0.4 : 1) : 1;
  // head of the line travels clockwise from the top-left corner
  const s = draw * P;
  const pt = (d: number): [number, number] => {
    if (d <= w) return [x + d, y];
    if (d <= w + h) return [x + w, y + d - w];
    if (d <= 2 * w + h) return [x + w - (d - w - h), y + h];
    return [x, y + h - (d - 2 * w - h)];
  };
  const [hx, hy] = pt(Math.min(s, P - 0.01));
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, opacity: fade * flick, mixBlendMode: 'screen'}}>
      <defs>
        <filter id="neonGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" result="a" />
          <feGaussianBlur stdDeviation="18" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="b" />
            <feMergeNode in="a" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <rect
        x={x}
        y={y}
        width={w}
        height={h}
        rx={16}
        fill="none"
        stroke="#ff2a3c"
        strokeWidth={4.5}
        strokeDasharray={`${P} ${P}`}
        strokeDashoffset={P * (1 - draw)}
        filter="url(#neonGlow)"
      />
      <rect x={x} y={y} width={w} height={h} rx={16} fill="none" stroke="#ffd6da" strokeWidth={1.4} strokeDasharray={`${P} ${P}`} strokeDashoffset={P * (1 - draw)} />
      {draw > 0 && draw < 1 ? <circle cx={hx} cy={hy} r={7} fill="#fff" filter="url(#neonGlow)" /> : null}
    </svg>
  );
};

// S5: bloom on the dial ring; pulses when the ring flips to red on the 14.5 s beat.
export const DialBloom: React.FC<{local: number}> = ({local}) => {
  const pulse = interpolate(local, [12, 15, 30], [0, 1, 0.25], clamp);
  const base = 0.3 + pulse * 0.7;
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', opacity: base, filter: 'blur(22px) brightness(1.5) saturate(1.5)'}}>
      <OffthreadVideo src={staticFile('clips/s5.mp4')} trimBefore={0} muted style={{width: 1080, height: 1920}} />
    </AbsoluteFill>
  );
};

// S10: "Charisma 9Kg" typed letter by letter, bottom-right like the captions.
export const Typing: React.FC<{text: string; stepFrames: number; dur: number}> = ({text, stepFrames, dur}) => {
  const local = useCurrentFrame();
  const out = interpolate(local, [dur - 8, dur], [1, 0], clamp);
  const typedAt = (i: number) => Math.round(i * stepFrames);
  const lastTyped = text.split('').reduce((acc, _c, i) => (local >= typedAt(i) ? i : acc), -1);
  const done = local >= typedAt(text.length - 1) + 4;
  const cursorOn = !done || Math.floor(local / 8) % 2 === 0;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-end', padding: 120, opacity: out}}>
      <div dir="ltr" style={{fontFamily: EN, fontWeight: 900, fontSize: 118, lineHeight: 1.1, whiteSpace: 'nowrap', letterSpacing: 1}}>
        {text.split('').map((c, i) => {
          const age = local - typedAt(i);
          const vis = age >= 0;
          const k = interpolate(age, [0, 4], [0, 1], clamp);
          return (
            <span
              key={i}
              style={{
                position: 'relative',
                visibility: vis ? 'visible' : 'hidden',
                color: interpolateColors(k, [0, 1], [RED, '#FFFFFF']),
                filter: `blur(${(1 - k) * 8}px)`,
                textShadow: `0 0 12px ${RED}, 0 0 32px ${RED}, 0 0 70px rgba(227,0,27,0.6)`,
              }}
            >
              {c === ' ' ? ' ' : c}
              {i === lastTyped && cursorOn ? (
                <span style={{position: 'absolute', right: -22, top: '12%', width: 12, height: '78%', background: RED, boxShadow: `0 0 16px ${RED}, 0 0 36px ${RED}`}} />
              ) : null}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
