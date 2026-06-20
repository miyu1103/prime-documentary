# Remotion ラフカット・パイプライン（U1–U5）— Codex引き継ぎ手順

台本（script_verified・ロック）から **権利クリーンな素材だけ**でRemotionのラフカットを作り、人間が仕上げるための仕組み。
Claude側（左工程）が U1–U5 の道具と配線を用意済み。Codex（右工程）は本書の順で回し、各ゲートで止まる。

## 方針（オーナー確定）
- **しょぼい動画にしない＝静止で見せない。** AI画像(Codex/SDXL)は主役級に**たくさん使ってOK**。ただし全カット必ず動かす（Ken Burns/parallax）。実写動画は要所に。Runwayは高コストなので決め所だけ。
- **権利が最重要。** 商用利用可の素材のみ。出典/作者/ライセンス/取得日/使用シーン/sha256を台帳に記録。
  - **禁止取得元**＝通常のYouTube/TikTok/Instagram/X・ニュース/TV/映画/アニメ/MV/スポーツ/まとめ/Google画像 の無断取得（`build_usable_assets.py`がホストで自動BLOCK）。
  - **権利が曖昧な素材は自動投入しない**（review送り）。**`usable`だけ**がタイムラインに乗る。
- 完全自動で完成させない。**ラフカットまで**を効率化し、**人間が確認・修正して完成**。

## データの流れ
```
03_script/script.annotated.v001.json (ロック・台本)
  └─ U1 plan_scenes.py        → 04_scenes/shotlist.v001.json   (各スパン: 推奨素材/動き/検索KW/秒数/テロップ)
        └─ U2 fetch_stock.py  → 05_stock/stock_ledger.v001.json (Pexels/Pixabay取得＋権利記録) ※APIキー必要
              └─ U3 build_usable_assets.py → 05_stock/usable_assets.v001.json + review_queue.v001.json (権利ゲート)
                    └─ U4 import_to_remotion.py → remotion/public/<slug>/ にOK素材コピー ＋ remotion/src/data/<slug>_roughcut.ts
                          └─ U5 RoughCut (Remotion) → Studioでラフカット確認 → 人間仕上げ
```

## 実行手順（例: 第11話）
すべて `./.venv/Scripts/python.exe`。各スクリプトは **dry-run既定**、`--write`で書き込み（原子的）、ネットは U2 のみ。

1. **U1 シーン表**（生成済み。再生成する場合）
   `scripts/plan_scenes.py 11 --write`
2. **APIキー設定（U2の前提・無料）** … `<repo>/.env` に追記（コミットされない）:
   ```
   PEXELS_API_KEY=xxxx      # https://www.pexels.com/api/ 無料
   PIXABAY_API_KEY=xxxx     # https://pixabay.com/api/docs/ 無料
   ```
3. **U2 素材取得**（shotlistの検索KWでPexels/Pixabayから候補DL＋台帳記録）
   `scripts/fetch_stock.py 11 --write`            （`--images`で写真も、`--per-source 2`で件数増）
   `scripts/fetch_stock.py 11 --query "snapchat phone teen" --write`  （手動で足す場合）
   ※AI画像(Codex/SDXL)で作った素材も `05_stock/stock_ledger.v001.json` に同形式で1行追記すれば対象になる（source=ai_codex/ai_sdxl, commercial_use=allowed, sha256必須）。
4. **U3 権利ゲート**（usable/review/blockedに分類。**OKだけ通す**）
   `scripts/build_usable_assets.py 11 --write`     → `usable_assets.v001.json` / `review_queue.v001.json`
   reviewに落ちた素材は人間が確認し、OKなら台帳のライセンス/ハッシュを直して再実行。
5. **U4 取り込み**（usableだけ `remotion/public/<slug>/` にコピー＋ `<slug>_roughcut.ts` 生成）
   `scripts/import_to_remotion.py 11 --write`
   - 素材が無いスパンは `src=null` → RoughCutが**ブランドのモーションカード（テロップ）**を描画（タイムラインは常に完結）。
6. **U5 ラフカット確認**（Remotion）
   - Root.tsx に第11話=`RoughCut-mahanoy` を登録済み。別話は U4 出力後に同様の`<Composition>`を追記（importの行を真似る）。
   - `cd remotion && npm run studio` で `RoughCut-<slug>` を開く。
   - 動画=`OffthreadVideo`、画像=Ken Burns/parallaxで**必ず動く**、AI画像は「Reconstruction」表示、テロップは金ルールの下三分の一。
   - ナレ/BGMは `<slug>_roughcut.ts` の `narrationSrc`/`bgmSrc` にpublic相対パスを入れると載る（ElevenLabsナレは**課金前にオーナー承認**）。
7. **書き出し** … `npm run render RoughCut-<slug> out/<slug>_rough.mp4`（CPU/libx264）。**初稿はオーナーゲートで停止**。公開しない。

## ゲート（必ず止まる）
- ナレーション課金（ElevenLabs）前 / 初稿 / タイトル・サムネ / 公開。**第15話(Theranos)はR3=公開前に法務レビュー必須**・本人肖像/実映像禁止。

## 公開スケジュール（重要）
- YouTubeの予約投稿は **6/23 まで埋まっている**。**次の予約は 6/24 以降から**割り当てること。過去日や 6/23 以前に重ねない。
- 公開・予約はオーナー承認ゲート（公開前に停止）。第15話(Theranos)は加えて法務レビュー必須。

## 素材の使い回し（自動）
- `build_usable_assets.py` は、その話で取得した素材に加えて **共有ライブラリ `references/stock_manifest.json`（権利クリーン既存素材）も自動で取り込む**。Claudeが集めた素材・過去に取得した素材は捨てずに毎回候補になる。
- AI画像(Codex/SDXL)を足すときは `05_stock/stock_ledger.v001.json` に1行追記（source=ai_codex/ai_sdxl, commercial_use=allowed, sha256）→ 同様にゲートを通って使われる。

## 注意
- 重メディア（候補/コピー元）は `H:\pd-media`（git管理外）。`remotion/public/<slug>/` の採用素材だけがリポジトリに入る。
- `remotion/` の既存型エラーは `MadoffPremium.tsx`（別ワーカーの既存issue）だけ。**本パイプラインの追加分（RoughCut/Root/データ）は型クリーン**。
- スキーマ: `schemas/shotlist.schema.json`, `schemas/stock-ledger.schema.json`。各スクリプトは出力を自己検証する。
