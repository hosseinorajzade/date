import React from 'react';
import {Composition} from 'remotion';
import {TextTest} from './TextTest';

export const Root: React.FC = () => (
  <>
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
