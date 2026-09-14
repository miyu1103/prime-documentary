// tyler bespoke FigureBeats 共有ユーティリティ（決定論・§2.4）。
// Math.random 禁止 → mulberry32 シード。useCurrentFrame 駆動前提。

/** 秒 → フレーム（fps から算出・フレーム直書き禁止方針に適合） */
export const sec = (fps: number, s: number): number => Math.round(fps * s);

/** 決定論的 PRNG（seed 固定 → Codex 再現性を破壊しない） */
export const mulberry32 = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** イージング済み 0..1（等速線形の代替・cubic out） */
export const easeOutCubic = (x: number): number => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);

/** 通貨整形（$780,000,000 等・グリフはコンポーネント側で発光表示） */
export const money = (n: number): string => '$' + Math.round(n).toLocaleString('en-US');
