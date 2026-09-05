# ローカルCodex プロンプト — 第12話(arbitration) 制作〜YouTubeアップロード直前までノンストップ【確定版 v001 / そのまま貼る】

> 確定状況（2026-06-23・Claude確認済み）
> - 第12話 `PD-2026-012-arbitration`（AT&T Mobility v. Concepcion 2011 / Epic Systems v. Lewis 2018 / 強制仲裁条項＋集団訴訟放棄）。state=script_verified・validate_episode 12 PASS。タイトル「The Fine Print That Took Away Your Right to Sue」。
> - 本編AI画像 生成済み前提：`H:\pd-media\assets\ai\arbitration\SPN-XXXX*.png`。サムネ6案 生成済み前提：`H:\pd-media\assets\ai\thumbs\arbitration\THUMB-01..06.png`。
> - 仕上げ設計＝`08_edit/edit_design.v001.md`（4部構成・全25ショットの意味あるアニメ＋§6 Premium実装＋**§7 ファクトリ本格活用**）、音声＝`06_audio/audio_cue_sheet.v001.md`。**この2本＋ `VIDEO_RULES.md` ＋ `FACTORY_INVENTORY.md` に従う**。
> - アニメは **Premium級コード演出（`ArbitrationPremium.tsx`）が主役**＋**DL済みファクトリ素材をふんだんに加飾**（テーマ別b-roll/背景/光・粒子・vfx/質感）で“美しくダイナミック”に。
> - **中立厳守**：critics（"forced arbitration＝裁判所の扉を閉じる"）と defenders（"速い・安い・合意済み"）を同尺・同トーンで公平に。地の文は中立語（mandatory / pre-dispute arbitration）。実在判事の肖像なし。

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第12話 PD-2026-012-arbitration を、制作から"YouTubeアップロード直前"まで一気通貫（ノンストップ）で**仕上げてください。slug=`arbitration`。
**唯一の停止点は「YouTubeアップロード直前」**（最終動画＋パッケージを用意して停止→オーナーが1回確認→アップロード/公開はオーナー操作）。それ以外の中間レビューでは止まらない。

## ★最重要
- フルアクセス（全権限・自動承認）で起動。許可待ち・中間レビュー待ち・ナレ課金待ちで**止まらない**。
- **4部構成・尺 約12分（11.5〜12.5分）**：①フック(本編ハイライト約10カット・各1〜2秒・新規制作しない)→②オープニング(`BrandOpening`)→③本編(4幕)→④エンディング(結末＋シリーズ統合＋次回予告=DNA＋CTA)。本編ナレ＋フック＋エンディング＋幕間の“ひと呼吸”で約12分に寄せる（台本は変えない・間延びさせない）。
- 先に4部の骨組み→中身→最後に「4部か・約12分か」を確認してから書き出す。

## まず読む（台本・claims・注釈はロック＝変更禁止。誤りはSTOP報告）
- `episodes/PD-2026-012-arbitration/08_edit/edit_design.v001.md`（仕上げ設計＝最重要。§2 全ショットのアニメ表／§3 字幕レイアウト／§6 Premium実装／**§7 ファクトリ本格活用の SPN→theme/subtype 割り当て表**）
- `episodes/PD-2026-012-arbitration/06_audio/audio_cue_sheet.v001.md`（音声4層＋ダッキング）
- `episodes/_planning/VIDEO_RULES.md`（§0/§4/§8/§10/§12/§13）, `episodes/_planning/FACTORY_INVENTORY.md`（棚のテーマ/サブタイプ）
- `episodes/PD-2026-012-arbitration/03_script/script.en.v001.md`（[VO:]）, `04_scenes/shotlist.v001.json`, `04_scenes/asset_map.v001.md`
- 雛形：`remotion/src/compositions/CarpenterPremium.tsx`（MadoffPremium/MappPremium も）

## 手順（1〜9はノンストップ。止まるのは10だけ）
1. **素材ステージング**: `./.venv/Scripts/python.exe scripts/import_to_remotion.py 12 --write` → `remotion/public/arbitration/` へAI画像/実写。`coded/cards=0` 確認。
2. **ファクトリ素材をふんだん取り込み（§7 の割り当てどおり）**: テーマ別に
   `./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme documents_paper --kind video`（同様に legal_court / finance_money / urban_night / atmosphere_symbolic / surveillance_tech と light/vfx/particle/texture/loops）→ トーンの合う商用OK(license=allowed)を `remotion/public/arbitration/factory/` へコピー。
3. **★ArbitrationPremium 作成**（最重要）: `remotion/src/compositions/ArbitrationPremium.tsx` を新規（CarpenterPremium雛形）。
   - 意味あるアニメ＝edit_design §2/§6 どおり（**Vote 5–4**：SPN-0013 Concepcion・SPN-0016 Epic、年表1925/2011/2018、TwoColumn critics/defenders、**BigNumber $30→tens of millions**、扉が閉じる/束ねる⇔1人ずつ 等）。SceneArt/Motion/Grain/Bookends/Carpenterビズ再利用。
   - **ファクトリを三層で重ねる（§7）**：背景プレート(documents_paper/legal_court/urban_night)＋light/vfx/particleオーバーレイ(screen/add)＋texture(overlay)。山場(0013/0016)は god_rays＋light_streaks で**ため→開放**＋SFX同期。
   - **美しくダイナミック**＝全カットに `MovingStage`/`CameraRig`（寄り引き/パララックス＋spring/easeイージング）。加飾は控えめ（1カット1〜2層・主役を食わない）。
   - **中立**：critics/defenders を同尺・同トーン。実在人物の肖像なし。SPNは shotlist の章割りで並べる。
   - `Root.tsx` に `ArbitrationPremium`（id="ArbitrationPremium"・ハイフンのみ）登録。
4. **自己確認（止まらない）**: `cd remotion && npm run studio` → `ArbitrationPremium`。演出/4部/約12分/**字幕とテロップ非重複**/critics=defenders公平 を自分で確認しOKなら次へ。
5. **ナレーション（課金気にせず実行）**: [VO:]→ElevenLabs→ draft/master を `H:\pd-media\episodes\PD-2026-012-arbitration\06_voice\` へ、索引 `06_audio/narration_index.v001.json`、`ArbitrationPremium` にナレ連結。
6. **音＆字幕（audio_cue_sheet 準拠）**: BGM(Suno)＋SFX＋環境音をダッキング（−14LUFS/TP≤−1）。
   - **字幕は forced alignment でナレと“ぴったり同期”（ズレ≤約120ms・一字一句一致）** → `08_edit/captions.v001.srt`(+.json)。
   - **見やすさ**：48〜60px・太字・白文字＋濃い縁取り/影＋半透明黒帯(不透明度~55〜70%)・最大2行・下部安全帯・1〜2行送り（高速点滅切替しない）。テロップ/出典と**非重複**。
7. **サムネ（CTR最大化が選定基準・止まらない）**: `THUMB-01..06` を **クリック率最大化の観点で評価**し（高コントラスト/単一明快な被写体/感情/可読の大文言余白/モバイル視認）最強の1枚を自動選定。`thumb_prompts.v001.md` の**タイトル3案(A/B/C)を全部** `ThumbnailFrame` で 1280×720 書き出し → `10_thumbnail/`、メタ `09_package/title_thumbnail_candidates.v001.json`（各案のCTR評価を併記）。**全候補を残しA/B差し替え可**。
8. **最終レンダー**: `cd remotion && npm run render ArbitrationPremium out/arbitration_premium.mp4 --crf=14`（CPU/libx264・1920×1080・NVENC不可）→ `H:\pd-media\episodes\PD-2026-012-arbitration\08_edit\arbitration_premium_v001.mp4`。QC（尺≒12分/−14LUFS/字幕同期/critics=defenders）を `08_edit/renders/final.v001.qc.json`。
9. **パッケージ（pd-package）**: タイトル(A/B/C)/説明/チャプター/字幕/タグ/権利マニフェスト/`youtube_meta` を `09_package/` に作成。
   - **公開予約は `2026-06-27T12:00:00+09:00`（JST 6/27 12:00）** を `youtube_meta`（`scheduled_at_local`/`scheduled_at_utc`=`2026-06-27T03:00:00Z`・privacy=private→公開予約）に設定。
   - 商用OK・実在人物の肖像なしを `rights_manifest` で確認。**ここで停止し「アップロード準備完了」を完成動画＋パッケージのパス付きで報告。**
10.【唯一のSTOP＝YouTubeアップロード】**アップロード／公開予約（6/27 12:00 JST）はオーナーが完成動画を確認後にオーナー操作/承認でのみ実行**（invariant 2）。Codexは自動で越えない。
各ステップでコミット（`H:\pd-media` と `remotion/public` はGit管理外。軽量成果物のみ）。

## ノンストップ運用
- 手順1〜9はオーナー確認を挟まず一気に通す。詰まっても止めず自分で判断して進め、最後にまとめて報告。
- 止まるのは手順10（アップロード）だけ。承認なしに越えない。
- 例外で即STOP：台本/claims の重大な事実誤り、権利・実在人物の肖像リスク、**critics/defenders の中立が崩れる場合**。

## この話の厳守
- **中立**＝forced arbitration は critics の語として帰属（地の文は mandatory/pre-dispute arbitration）。critics と defenders を同尺・同トーン。経験的論点（コスト/速度/結果）は未決着として扱う。
- 実在人物・判事の肖像なし（象徴・タイポで代替）。一般ストックは「事件の実物」として提示しない（illustrative）。台本・claims 不改変。

## 最初のアクション
手順1から開始し、手順1→9をノンストップで実行（素材→ファクトリ取り込み→ArbitrationPremium実装→ナレ→音/字幕→サムネ→最終レンダー→パッケージ※予約6/27 12:00 JST）→ 手順10の手前で停止して「アップロード準備完了」を報告。
