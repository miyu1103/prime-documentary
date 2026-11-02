import React from 'react';
import {BrandEndcard, ENDCARD_SEC} from '../components/Bookends';

/**
 * Preview wrapper for the canonical BrandEndcard (now the adopted "派手" look).
 * 正典は components/Bookends.tsx。ここはプレビュー用に呼ぶだけ（ロジック重複なし）。
 */

export const endingBrushupDurationInFrames = (fps: number) =>
  Math.round(ENDCARD_SEC * fps);

export const EndingBrushupPreview: React.FC = () => <BrandEndcard />;
