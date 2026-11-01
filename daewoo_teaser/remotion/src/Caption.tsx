import React from 'react';
import {AbsoluteFill, Easing, interpolate, interpolateColors, useCurrentFrame} from 'remotion';
import {EN, FA, RED} from './fonts';

// A run of text: Persian runs use Vazirmatn, Latin runs use Roboto and are
// bidi-isolated so things like "A+++" keep their order inside an RTL line.
export type Run = {t: string; en?: boolean};

const Runs: React.FC<{runs: Run[]; faWeight: number; enWeight: number}> = ({runs, faWeight, enWeight}) => (
  <>
    {runs.map((r, i) =>
      r.en ? (
        <span key={i} dir="ltr" style={{fontFamily: EN, fontWeight: enWeight, unicodeBidi: 'isolate'}}>
          {r.t}
        </span>
      ) : (
        <span key={i} style={{fontFamily: FA, fontWeight: faWeight}}>
          {r.t}
        </span>
      ),
    )}
  </>
);

export const SAFE = 120;

export const BottomGradient: React.FC<{opacity?: number}> = ({opacity = 1}) => (
  <AbsoluteFill
    style={{
      opacity,
      background:
        'linear-gradient(to top, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.55) 22%, rgba(0,0,0,0.18) 40%, rgba(0,0,0,0) 52%)',
    }}
  />
);

// Title appears red and blurred, then resolves to sharp white with a red glow.
// Description follows a few frames later at 80% white.
export const Caption: React.FC<{
  title: Run[];
  desc?: Run[];
  durationInFrames: number;
  titleSize?: number;
}> = ({title, desc, durationInFrames, titleSize = 92}) => {
  const f = useCurrentFrame();
  const ease = Easing.bezier(0.2, 0.7, 0.2, 1);

  const tIn = interpolate(f, [0, 7], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const tResolve = interpolate(f, [5, 20], [0, 1], {easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const out = interpolate(f, [durationInFrames - 7, durationInFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const color = interpolateColors(tResolve, [0, 1], [RED, '#FFFFFF']);
  const blur = interpolate(tResolve, [0, 1], [16, 0]) + out * 10;
  const glow = interpolate(tResolve, [0, 1], [1.6, 1]);
  const x = interpolate(tIn, [0, 1], [-30, 0]);

  const dIn = interpolate(f, [9, 22], [0, 1], {easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-end', padding: SAFE}}>
      <div dir="rtl" style={{width: 1080 - SAFE * 2, textAlign: 'right'}}>
        <div
          style={{
            color,
            fontSize: titleSize,
            lineHeight: 1.25,
            opacity: tIn * (1 - out),
            filter: `blur(${blur}px)`,
            transform: `translateX(${x}px)`,
            textShadow: `0 0 ${10 * glow}px ${RED}, 0 0 ${26 * glow}px ${RED}, 0 0 ${60 * glow}px rgba(227,0,27,0.65)`,
            whiteSpace: 'nowrap',
          }}
        >
          <Runs runs={title} faWeight={900} enWeight={900} />
        </div>
        {desc ? (
          <div
            style={{
              marginTop: 18,
              color: 'rgba(255,255,255,0.8)',
              fontSize: 40,
              lineHeight: 1.6,
              opacity: dIn * (1 - out),
              filter: `blur(${(1 - dIn) * 6 + out * 6}px)`,
              transform: `translateY(${(1 - dIn) * 16}px)`,
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              textWrap: 'balance',
              textShadow: '0 2px 12px rgba(0,0,0,0.6)',
            }}
          >
            <Runs runs={desc} faWeight={400} enWeight={700} />
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
