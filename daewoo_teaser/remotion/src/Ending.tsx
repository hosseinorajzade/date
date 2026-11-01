import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {EN, RED} from './fonts';
import {clamp, f} from './fx';
import TL from './timeline.json';

// Logo reveal on black: impact burst -> wordmark wiped in by a light edge -> red symbol pops on the beat
// -> neon underline + www.Daewoo.ir -> specular sweep -> fade to black.
const LOGO_W = 3467;
const SPLIT = 2512; // x where the red symbol starts in daewoo_logo.png
const WM_W = 2508;
const LOGO_H = 575;

export const Ending: React.FC = () => {
  const local = useCurrentFrame();
  const {fps} = useVideoConfig();
  const L = TL.logo;
  const t0 = f(L.impact);
  const wm0 = f(L.wordmark[0]) - t0;
  const wm1 = f(L.wordmark[1]) - t0;
  const sym = f(L.symbol) - t0;
  const url = f(L.url) - t0;
  const fo0 = f(L.fadeOut[0]) - t0;
  const fo1 = f(L.fadeOut[1]) - t0;

  const W = 800;
  const k = W / LOGO_W;
  const H = LOGO_H * k;
  const left = (1080 - W) / 2;
  const top = 860 - H / 2;

  const burst = interpolate(local, [0, 3, 22], [0, 1, 0], clamp);
  const wipe = interpolate(local, [wm0, wm1], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const wmBlur = interpolate(local, [wm0, wm1 + 4], [10, 0], clamp);
  const symS = spring({frame: local - sym, fps, config: {damping: 11, stiffness: 160, mass: 0.7}});
  const symGlow = interpolate(local, [sym, sym + 3, sym + 25], [0, 1, 0.25], clamp);
  const line = interpolate(local, [sym + 2, sym + 20], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const urlIn = interpolate(local, [url, url + 14], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const sheen = interpolate(local, [sym + 30, sym + 52], [-0.3, 1.3], clamp);
  const fade = interpolate(local, [fo0, fo1], [1, 0], {...clamp, easing: Easing.in(Easing.quad)});
  const edgeX = left + wipe * WM_W * k;

  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{opacity: fade}}>
        {/* impact burst */}
        <AbsoluteFill
          style={{
            opacity: burst,
            background: `radial-gradient(circle at 50% 45%, rgba(255,255,255,0.55) 0%, rgba(227,0,27,0.55) 18%, rgba(227,0,27,0.12) 45%, rgba(0,0,0,0) 70%)`,
            transform: `scale(${1 + local * 0.03})`,
          }}
        />
        {/* wordmark, wiped in left -> right */}
        <div style={{position: 'absolute', left, top, width: WM_W * k, height: H, clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`, filter: `blur(${wmBlur}px)`}}>
          <Img src={staticFile('img/logo_wordmark.png')} style={{width: WM_W * k, height: H}} />
        </div>
        {/* light edge riding the wipe */}
        {wipe > 0 && wipe < 1 ? (
          <div
            style={{
              position: 'absolute',
              left: edgeX - 4,
              top: top - 40,
              width: 8,
              height: H + 80,
              background: '#fff',
              boxShadow: `0 0 20px #fff, 0 0 50px ${RED}, 0 0 110px ${RED}`,
              borderRadius: 4,
            }}
          />
        ) : null}
        {/* red symbol pops on the beat */}
        <div
          style={{
            position: 'absolute',
            left: left + SPLIT * k,
            top,
            width: (LOGO_W - SPLIT) * k,
            height: H,
            opacity: local >= sym ? Math.min(1, symS * 1.5) : 0,
            transform: `scale(${0.35 + 0.65 * symS})`,
            filter: `drop-shadow(0 0 ${8 + symGlow * 30}px rgba(227,0,27,${0.5 + symGlow * 0.5}))`,
          }}
        >
          <Img src={staticFile('img/logo_symbol.png')} style={{width: '100%', height: '100%'}} />
        </div>
        {/* specular sheen across the whole logo, masked to its shape */}
        <div
          style={{
            position: 'absolute',
            left,
            top,
            width: W,
            height: H,
            WebkitMaskImage: `url(${staticFile('img/daewoo_logo.png')})`,
            WebkitMaskSize: '100% 100%',
            maskImage: `url(${staticFile('img/daewoo_logo.png')})`,
            maskSize: '100% 100%',
            background: `linear-gradient(105deg, rgba(255,255,255,0) ${sheen * 100 - 12}%, rgba(255,255,255,0.85) ${sheen * 100}%, rgba(255,255,255,0) ${sheen * 100 + 12}%)`,
            mixBlendMode: 'screen',
          }}
        />
        {/* neon underline */}
        <div
          style={{
            position: 'absolute',
            left: 540 - (W / 2) * line,
            top: top + H + 46,
            width: W * line,
            height: 3,
            background: RED,
            boxShadow: `0 0 10px ${RED}, 0 0 26px ${RED}, 0 0 60px rgba(227,0,27,0.7)`,
            borderRadius: 2,
          }}
        />
        {/* url */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: top + H + 86,
            textAlign: 'center',
            fontFamily: EN,
            fontWeight: 700,
            fontSize: 46,
            letterSpacing: 4,
            color: 'rgba(255,255,255,0.88)',
            opacity: urlIn,
            transform: `translateY(${(1 - urlIn) * 18}px)`,
            filter: `blur(${(1 - urlIn) * 6}px)`,
          }}
        >
          www.Daewoo.ir
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
