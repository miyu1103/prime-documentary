// Register the brand premium fonts (owner-approved 2026-07-17) for the Remotion render.
// Injects @font-face via a <style> tag rather than delayRender()+FontFace.load(): the
// variable fonts (Oswald/Archivo) can hang FontFace.load() in the headless render worker,
// which timed out the 'load-brand-fonts' delayRender handle and crashed the whole render.
// A CSS @font-face with font-display:block is non-blocking to import, cannot crash the
// render, and Remotion still waits for document.fonts before capturing each frame.
import {staticFile} from 'remotion';

const CSS = `
@font-face { font-family: 'Oswald'; src: url('${staticFile('fonts/Oswald.ttf')}') format('truetype'); font-weight: 100 900; font-style: normal; font-display: block; }
@font-face { font-family: 'Anton'; src: url('${staticFile('fonts/Anton.ttf')}') format('truetype'); font-weight: 400; font-style: normal; font-display: block; }
@font-face { font-family: 'Archivo'; src: url('${staticFile('fonts/Archivo.ttf')}') format('truetype'); font-weight: 100 900; font-style: normal; font-display: block; }
`;

if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.setAttribute('data-brand-fonts', 'true');
  style.textContent = CSS;
  document.head.appendChild(style);
}
