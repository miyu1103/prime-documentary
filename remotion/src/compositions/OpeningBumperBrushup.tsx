import React from 'react';
import {BrandOpening, OPENING_SEC} from '../components/Bookends';

/**
 * Preview wrappers for the canonical BrandOpening (now the adopted "派手" look).
 * 正典は components/Bookends.tsx。ここはプレビュー用に文言を差し替えて表示するだけ（ロジック重複なし）。
 */

export const bumperBrushupDurationInFrames = (fps: number) =>
  Math.round(OPENING_SEC * fps);

/** EP6(Terry)を例にした採用版オープニング。 */
export const BumperBrushupPreview: React.FC = () => (
  <BrandOpening seriesLabel="PRIME DOCUMENTARY" title="Terry v. Ohio" subtitle="A street stop that redrew the line" />
);

/** 別話(Titan)でも同じ部品で出ることの確認用。 */
export const BrandOpeningOriginalPreview: React.FC = () => (
  <BrandOpening seriesLabel="Landmark Rights Cases" title="Titan" subtitle="The dive that never came back" />
);

/** EP17 OneCoin用の正規ブランドオープニング。 */
export const OneCoinBrandOpeningPreview: React.FC = () => (
  <BrandOpening seriesLabel="Prime Documentary" title="Nothing" subtitle="The Woman Who Sold a Coin That Did Not Exist" />
);
