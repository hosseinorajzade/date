import React from 'react';
import {Composition} from 'remotion';
import {TextTest} from './TextTest';
import {Teaser} from './Teaser';

export const Root: React.FC = () => (
  <>
    <Composition id="Teaser" component={Teaser} durationInFrames={1290} fps={30} width={1080} height={1920} />
    <Composition
      id="TextTest"
      component={TextTest}
      durationInFrames={60}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{index: 0}}
    />
  </>
);
