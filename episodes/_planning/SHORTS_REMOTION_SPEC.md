# 縦型ショート Remotion テンプレ 詳細仕様書（A）— 実装=Codex

目的：`SHORTS_EP1-8.md` / `SHORTS_EP9-15.md` の各ショートを**再現性高く量産**するための、縦型Remotionコンポジション仕様。
長尺の `RoughCut.tsx` と同じ思想：**1ショート＝1データファイル**を読み、テンプレが組み立てる。実装はCodex、本書が仕様。
品質ルールは `VIDEO_RULES.md`（§11 音・§12 アニメ・§13 字幕配置は長尺・ショート共通）に従う。

---

## 1. 基本仕様
- **解像度 1080×1920（9:16）／30fps／尺 35〜45秒。**
- 配色＝黒/紺/エレクトリックブルー/金（`remotion/src/brand.ts`）。見出し＝Impact系、本文＝Trebuchet系。
- 構成（ショート用）＝**フック→展開→オチ→CTA**（`SHORTS_EP*.md` の時間表どおり）。※12分構成は長尺のみ・適用しない。
- 画像は**必ず動かす**（静止禁止）。**フックは速いカット**、以降は1カット約3〜4秒。

## 2. 素材の場所（事前生成済みを前提）
- 縦AI画像：`H:\pd-media\assets\ai\shorts\shortNN\shortNN_01.png 〜 _07.png`（本編）／`shortNN_thumb.png`（サムネ）。
- importで `remotion/public/shorts/shortNN/` にコピーして使う（重メディアはH:、publicはGit管理外）。

## 3. データ契約（TypeScript型・テンプレが読む）
`remotion/src/compositions/Short.tsx` が export する型。各ショートの実体は `remotion/src/data/shortNN.ts`。
```ts
export type ShortBeat = {
  id: string;                 // 'hook' | 'b1' | 'b2' ... | 'cta'
  startSec: number;           // 開始秒（テンプレ側でframe換算）
  durSec: number;             // 表示秒
  src: string | null;         // staticFile相対パス（縦画像/動画）。nullはブランドカード
  kind: 'image' | 'video' | 'card';
  motion: 'kenburns' | 'parallax' | 'pushin' | 'video'; // 静止禁止
  telop?: string;             // 見出し/キーワード（上ゾーンに表示）。無ければ非表示
  fast?: boolean;             // フックの速いカット（true=短め+カット時SFX強め）
};
export type ShortData = {
  shortId: string;            // 'short09'
  episodeId: string;          // 'PD-2026-009-timbs'
  durationSec: number;        // = beats合計。35〜45
  narrationSrc: string | null;
  captions: { word: string; startSec: number; endSec: number }[] | null; // forced alignment結果
  bgmSrc: string | null;
  ambienceSrc?: string | null;
  sfx?: { atSec: number; src: string; gainDb?: number }[];
  ctaText?: string;           // 末尾CTA（例「本編はチャンネルへ」）
  beats: ShortBeat[];
};
export const shortDurationInFrames = (d: ShortData, fps: number) =>
  Math.max(1, Math.round(d.durationSec * fps));
```

## 4. レイアウト＆セーフエリア（字幕とテロップを**絶対に被らせない**）
1080×1920。プラットフォームUI（TikTok/YTショートの右ボタン・下部）を避ける。
- **上ゾーン＝テロップ/見出し（`beat.telop`）**：y ≈ **180〜560px**、中央寄せ、Impact大（80〜110px）、最大2行、金/白。動きを付けて出す。
- **下ゾーン＝字幕（ナレ字幕）**：y ≈ **1280〜1560px**（**下端から約360pxは空ける**＝UI回避）、中央、Trebuchet太、56〜68px、最大2行、半透明の帯。**上ゾーンと縦に完全分離（重ならない）。**
- **右端 約120px** と **下端 約300px** は重要要素を置かない（UI領域）。
- 出典/AI開示が要る時は **左上に小さく**（字幕帯と離す）。
- ブランド：上部に細いプログレスバー（任意・控えめ）。
- ルール：**テロップと字幕が同時でも、上＝テロップ／下＝字幕で住み分け。同じ帯に重ねない。**

## 5. コンポジション構造（`Short.tsx`）
```
<AbsoluteFill ink>
  <Series>  // beatごと（durSec×fps）
    各beat:
      kind=image → MovingImage(src, motion)    // Ken Burns/parallax/pushin（静止禁止）
      kind=video → Video(src, loop, muted)
      kind=card  → ブランドカード（telopのみ）
      + grade(縦グラデ) + Vignette + Grain
  </Series>
  // 全尺オーバーレイ：
  <TelopLayer beats={...}/>      // 上ゾーン、各beat.telopを時間で出す（アニメ）
  <CaptionLayer captions={...}/> // 下ゾーン、ナレに語単位同期（forced alignment）
  <Audio narration/> <Audio bgm volume(ducked)/> <Audio ambience/> {sfx...}
</AbsoluteFill>
```
- `MovingImage`/`Video`/grade/Grain/Vignette は長尺の `RoughCut.tsx` の実装を縦用に流用。
- 既存ブランド部品（`KineticType`/`DiagramFlow`/`CitationLowerThird`）を**意味のあるアニメ**に活用（§12）。
- **【重要】意味のあるアニメ（天秤/票/地図/年表/図解/数字）は MovingImage だけにせず、コード部品（`SceneArt`/`Motion`/`KineticType`/`DiagramFlow` 等）を背景の上にラップして出す。**各ビート種別への具体的な演出割当・縦用セーフエリア・新規縦コンポ（`VoteVertical` 等）は **`SHORTS_MOTION_DESIGN.md` を参照**。

## 6. 音（§11準拠・必須4層＋ダッキング）
- **ナレ**＝0dB基準・常に明瞭。**BGM**＝−16dB目安、ナレ中は−22dBへ自動ダッキング。**環境音**＝−24dB薄く。**SFX**＝カット/リビール/数字/テロップ出現に短く（−10〜−6dB、`beat.fast`は強め）。
- 実装：ナレの有無で BGM/ambience の `volume` を時間関数で下げる（簡易ダッキング）。クリップ無し。

## 7. 字幕（forced alignment）
- ナレ音声＋台本VOから**語単位タイムスタンプ**を作る（`scripts/gen_captions_forced.py` 系を流用、出力を `ShortData.captions` に格納）。
- `CaptionLayer` は現在時刻に応じて**1〜2行ずつ**表示（語ハイライトでも可）。**下ゾーン固定・テロップと非重複**。

## 8. データ生成（推奨ツール／Codex実装可）
- `scripts/build_short_data.py shortNN`：`SHORTS_EP*.md` のビート時間表＋ `H:\…\ai\shorts\shortNN\` の画像から `remotion/src/data/shortNN.ts` を生成（src割当・durSec・telop）。
  - もしくはCodexが時間表を見て手組みでも可。**numberは時間表の秒に一致させる。**
- 生成後 `Root.tsx` に `<Composition id="Short-shortNN" component={Short} durationInFrames={shortDurationInFrames(data)} fps=30 width=1080 height=1920 defaultProps={{data}}/>` を追加。

## 9. サムネ（縦・Still）
- `ShortThumb`（Still・1080×1920）：背景＝`shortNN_thumb.png`（文字なし）＋**大きな日本語文言**（`SHORTS_EP*.md`の「サムネ文言」）をImpactで重ねる。金/白・強コントラスト。
- 文字は中央〜やや上、UI領域（下/右）を避ける。

## 10. 書き出し
- `npm run render Short-shortNN out/shortNN.mp4 --crf=16`（CPU/libx264・1080×1920・30fps・NVENC不可）。
- サムネ：`npm run still ShortThumb-shortNN out/shortNN_thumb.png`。

## 11. 受け入れ基準（これを満たして“完成”）
- [ ] 1080×1920 / 30fps / 35〜45秒。
- [ ] **どのカットも動く**（静止なし）。フックは速いカット＋SFX。
- [ ] **字幕がナレと同期**し、**テロップと一度も被らない**（上＝テロップ／下＝字幕）。
- [ ] **音4層（ナレ＋BGM＋環境音＋SFX）**が入り、ナレ中はBGM/環境音がダッキング。
- [ ] 意味のあるアニメ（天秤/地図/票/年表/図解 等）が要所に入る。
- [ ] **実在人物の肖像なし**・中立・広告安全・ブランド配色。
- [ ] サムネ（縦・大文言）あり。CTAは本編リンク（URLはオーナー差し込み）。公開は6/24以降・各ゲートで停止。

## 12. Codex実装ステップ
> **指針**：意味のあるアニメはコード部品（`SceneArt`/`Motion`/`KineticType`/`DiagramFlow`）で出す。**MovingImage だけにしない。**各ショート・各ビートの演出割当と新規縦コンポ（`VoteVertical` 等・評決は話ごとに可変）は **`SHORTS_MOTION_DESIGN.md`** に詳細。
1. `Short.tsx`（本仕様3・4・5）と `MovingImage`/`TelopLayer`/`CaptionLayer` を実装（長尺部品を縦流用）。型チェック必須。
2. `build_short_data.py`（任意）→ `shortNN.ts` 生成、`Root.tsx` 登録。
3. ナレ（課金前承認）→ forced alignment → `captions`。BGM/SFX/環境音を用意しミックス（ダッキング）。
4. `Short-shortNN` を studio で確認（受け入れ基準）。`ShortThumb-shortNN` でサムネ。
5. 書き出し→初稿ゲートで停止。まず #1（short01）で1本通し、OKなら他に横展開。
