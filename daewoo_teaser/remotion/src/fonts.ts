import {continueRender, delayRender, staticFile} from 'remotion';

const faces: Array<[string, string, string]> = [
  ['Vazirmatn', 'fonts/Vazirmatn-Black.woff2', '900'],
  ['Vazirmatn', 'fonts/Vazirmatn-ExtraBold.woff2', '800'],
  ['Vazirmatn', 'fonts/Vazirmatn-Regular.woff2', '400'],
  ['Roboto', 'fonts/Roboto-Bold.woff2', '700'],
  ['Roboto', 'fonts/Roboto-Black.woff2', '900'],
];

let loaded = false;

export const loadFonts = () => {
  if (loaded || typeof document === 'undefined') return;
  loaded = true;
  const handle = delayRender('fonts');
  Promise.all(
    faces.map(([family, file, weight]) => {
      const face = new FontFace(family, `url(${staticFile(file)}) format('woff2')`, {weight});
      (document.fonts as unknown as {add: (f: FontFace) => void}).add(face);
      return face.load();
    }),
  )
    .then(() => continueRender(handle))
    .catch((err) => {
      console.error(err);
      continueRender(handle);
    });
};

export const RED = '#E3001B';
export const FA = "'Vazirmatn', sans-serif";
export const EN = "'Roboto', sans-serif";
