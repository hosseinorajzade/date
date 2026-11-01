import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BottomGradient, Caption} from './Caption';
import {COPY} from './copy';
import {EN, RED, loadFonts} from './fonts';

loadFonts();

const CASES = [
  {bg: 's3', key: 'directDrive'},
  {bg: 's4', key: 'modes'},
  {bg: 's6', key: 'energy'},
  {bg: 's7', key: 'jet'},
  {bg: 's8', key: 'addItem'},
  {bg: 's9', key: 'capacity'},
];

// Still used to check Persian shaping, bidi order and layout. `index` 0-5 = captions,
// 6 = "Charisma" title card, 7 = "Charisma 9Kg" end line. `frame` controls the animation phase.
export const TextTest: React.FC<{index: number}> = ({index}) => {
  if (index < 6) {
    const c = CASES[index];
    const copy = COPY[c.key];
    return (
      <AbsoluteFill style={{background: '#000'}}>
        <Img src={staticFile(`stills/${c.bg}.png`)} />
        <BottomGradient />
        <Caption title={copy.title} desc={copy.desc} durationInFrames={9999} titleSize={copy.size} />
      </AbsoluteFill>
    );
  }
  const word = index === 6 ? 'Charisma' : 'Charisma 9Kg';
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Img src={staticFile(index === 6 ? 'stills/s2.png' : 'stills/s10.png')} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            fontFamily: EN,
            fontWeight: 900,
            fontSize: index === 6 ? 210 : 130,
            color: index === 6 ? RED : '#fff',
            filter: index === 6 ? 'blur(2px)' : undefined,
            textShadow: `0 0 18px ${RED}, 0 0 50px ${RED}, 0 0 110px rgba(227,0,27,0.7)`,
            letterSpacing: index === 6 ? 4 : 2,
          }}
        >
          {word}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
