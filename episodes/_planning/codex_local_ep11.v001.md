# ローカルCodex プロンプト — 第11話(mahanoy) 制作〜YouTubeアップロード直前までノンストップ【確定版 v001 / そのまま貼る】

> 確定状況（2026-06-22・Claude確認済み）
> - 第11話 `PD-2026-011-mahanoy`（Mahanoy Area School District v. B.L. / 学校外SNS投稿と生徒の言論の自由）。state=script_verified・validate_episode 11 PASS。
> - 本編AI画像 生成済み前提：`H:\pd-media\assets\ai\mahanoy\SPN-XXXX*.png`。サムネ6案 生成済み前提：`H:\pd-media\assets\ai\thumbs\mahanoy\THUMB-01..06.png`。
> - 仕上げ設計＝`08_edit/edit_design.v001.md`（4部構成・全28ショットの意味あるアニメ＋§6 Premium実装＋加飾レイヤ）、音声＝`06_audio/audio_cue_sheet.v001.md`（4層＋ダッキング）。**この2本＋ `VIDEO_RULES.md` に従う**。
> - アニメは **Premium級コード演出（`MahanoyPremium.tsx`）が主役**＋**DL済みファクトリ素材を加飾**（背景/光/粒子/vfx/質感）で“美しくダイナミック”に。
> - **広告安全（最重要）**：投稿の罵倒語は音声・字幕・画面のどこにも出さない（常にCENSORED）。未成年含め実在人物の肖像なし。

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第11話 PD-2026-011-mahanoy を、制作から“YouTubeアップロード直前”まで一気通貫（ノンストップ）で**仕上げてください。slug=`mahanoy`。
**唯一の停止点は「YouTubeアップロード直前」**（最終動画＋パッケージを用意して停止→オーナーが1回確認→アップロード/公開はオーナー操作）。それ以外の中間レビューでは止まらない。

## ★最重要
- フルアクセス（全権限・自動承認）で起動。許可待ち・中間レビュー待ち・ナレ課金待ちで**止まらない**。
- **4部構成・尺 約12分（11.5〜12.5分）**：①フック(本編ハイライト約10カット・各1〜2秒・新規制作しない)→②オープニング(`BrandOpening`)→③本編(4幕)→④エンディング(結末＋次回予告＋CTA)。本編ナレ＋フック＋エンディング＋幕間の“ひと呼吸”で約12分に寄せる（台本は変えない・間延びさせない）。
- 先に4部の骨組み→中身→最後に「4部か・約12分か」を確認してから書き出す。

## まず読む（台本・claims・注釈はロック＝変更禁止。誤りはSTOP報告）
- `episodes/PD-2026-011-mahanoy/08_edit/edit_design.v001.md`（仕上げ設計＝最重要。§2 全ショットのアニメ表／§3 字幕レイアウト／§6 Premium実装＋加飾レイヤ）
- `episodes/PD-2026-011-mahanoy/06_audio/audio_cue_sheet.v001.md`（音声4層＋ダッキング）
- `episodes/_planning/VIDEO_RULES.md`（§0/§4/§8/§10/§12/§13＝ノンストップ運用・ファクトリ活用・尺12分・美しくダイナミックなアニメ・字幕同期/可読性）
- `episodes/PD-2026-011-mahanoy/03_script/script.en.v001.md`（[VO:]＝ナレ本文）, `04_scenes/shotlist.v001.json`, `04_scenes/asset_map.v001.md`
- 雛形：`remotion/src/compositions/CarpenterPremium.tsx`（GideonPremium/MadoffPremium も）

## 手順（1〜9はノンストップ。止まるのは10だけ）
1. **素材ステージング**: `./.venv/Scripts/python.exe scripts/import_to_remotion.py 11 --write`
   → AI画像/実写を `remotion/public/mahanoy/` へ。`coded/cards=0` 確認。`mahanoy_roughcut.ts` は下見用。
2. **ファクトリ加飾素材の選定**: `./.venv/Scripts/python.exe scripts/select_factory_assets.py` で**トーンの合う** backgrounds/light/particle/vfx/texture/loops を抽出 → `remotion/public/mahanoy/factory/` へコピー（商用OK=licenseがallowedのみ）。
3. **★MahanoyPremium 作成**（最重要）: `remotion/src/compositions/MahanoyPremium.tsx` を新規（CarpenterPremium雛形）。
   - 意味あるアニメ＝edit_design §6 の **SPN→部品割り当て表**どおり（**Vote は 8–1 に改変**、SPN-0012「校門がスマホ光で溶解」、SPN-0014 山場=年表→8–1→出典594 U.S.180、SPN-0017 いじめ/脅迫/カンニング点灯、SPN-0018 単独反対 等）。SceneArt/Motion/Grain/Bookends/Carpenterビズを再利用。
   - **美しくダイナミック**＝全カットに `MovingStage`/`CameraRig`（寄り引き/パララックス＋spring/easeイージング）。ファクトリ素材を **背景プレート＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)** で重ね奥行きと光を出す（加飾は控えめ・主役を食わない）。山場は**ため→開放**＋SFX同期。
   - **広告安全**：投稿の罵倒語は出さない（CENSORED帯を常時）。実在人物の肖像なし。SPNは**章順**に並べる（§1注記）。
   - `Root.tsx` に `MahanoyPremium`（id="MahanoyPremium"・ハイフンのみ）登録。
4. **自己確認（止まらない）**: `cd remotion && npm run studio` → `MahanoyPremium`。演出/4部/約12分/**字幕とテロップ非重複**/罵倒語ゼロ を自分で確認しOKなら次へ。
5. **ナレーション（課金気にせず実行）**: [VO:]→ElevenLabs→ draft/master を `H:\pd-media\episodes\PD-2026-011-mahanoy\06_voice\` へ、索引 `06_audio/narration_index.v001.json`、`MahanoyPremium` にナレ連結。
6. **音＆字幕（audio_cue_sheet 準拠）**: BGM(Suno)＋SFX＋環境音をダッキング（−14LUFS/TP≤−1）。
   - **字幕は forced alignment でナレと“ぴったり同期”（ズレ≤約120ms・一字一句一致）** → `08_edit/captions.v001.srt`(+.json)。
   - **見やすさ**：48〜60px・太字・白文字＋濃い縁取り/影＋半透明黒帯・最大2行・下部安全帯・1〜2行送り。テロップ/出典と**非重複**。罵倒語は字幕にも出さない。
7. **サムネ（自動選定・止まらない）**: `THUMB-01..06` から CTR最強の1枚を自動選定し、`thumb_prompts.v001.md` のタイトル3案を全部 `ThumbnailFrame` で 1280×720 書き出し → `10_thumbnail/`、メタ `09_package/title_thumbnail_candidates.v001.json`。全候補を残し差し替え可。
8. **最終レンダー**: `cd remotion && npm run render MahanoyPremium out/mahanoy_premium.mp4 --crf=14`（CPU/libx264・1920×1080・NVENC不可）→ `H:\pd-media\episodes\PD-2026-011-mahanoy\08_edit\mahanoy_premium_v001.mp4`。QC（尺≒12分/−14LUFS/字幕同期/罵倒語ゼロ）を `08_edit/renders/final.v001.qc.json`。
9. **パッケージ（pd-package）**: タイトル/説明/チャプター/字幕/タグ/権利マニフェスト/`youtube_meta` を `09_package/` に作成（商用OK・実在人物の肖像なしを `rights_manifest` で確認）。**ここで停止し「アップロード準備完了」を報告**（完成動画＋パッケージのパスを提示）。
10.【唯一のSTOP＝YouTubeアップロード】**アップロード・公開予約（6/24以降）はオーナーが完成動画を確認後にオーナー操作/承認でのみ実行**（invariant 2）。Codexは自動で越えない。
各ステップでコミット（`H:\pd-media` と `remotion/public` はGit管理外。軽量成果物のみ）。

## ノンストップ運用
- 手順1〜9はオーナー確認を挟まず一気に通す。詰まっても止めず自分で判断して進め、最後にまとめて報告。
- 止まるのは手順10（アップロード）だけ。承認なしに越えない。
- 例外で即STOP：台本/claims の重大な事実誤り、権利・実在人物の肖像リスク、**投稿罵倒語が混入しそうな場合**。

## この話の厳守
- **広告安全**＝投稿の罵倒語は音声・字幕・画面のどこにも出さない（常にCENSORED）。
- 中立（学校の権限 vs 生徒の声・多数意見/例外/Thomas反対を公平）。実在人物（未成年のBrandi Levy・各判事）の肖像なし＝象徴のみ。台本・claims 不改変。

## 最初のアクション
手順1から開始し、手順1→9をノンストップで実行（素材→ファクトリ加飾→MahanoyPremium実装→ナレ→音/字幕→サムネ→最終レンダー→パッケージ）→ 手順10の手前で停止して「アップロード準備完了」を報告。
