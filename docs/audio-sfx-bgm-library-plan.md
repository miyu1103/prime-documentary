# Audio: SFX / Ambience / BGM ライブラリ調達・運用計画

ステータス: **設計（未実装）**

## 前提・仮定

- 本書は「音の4層（ナレ＋BGM＋SFX＋環境音）」を**Scene が来る前に先回りで大量に貯める**ための調達・運用設計。`docs/asset-priority-list.md` のグループ D（SFX）と `docs/asset-generation-prompts.md` §3-4、`episodes/_planning/VIDEO_RULES.md` §11（音4層＋ダッキング）に**整合させ、矛盾させない**。
- **登録済みツールだけで成立させる**（`docs/cost-control-policy.md` §1）。新規有料サービス・新規素材サブスクは前提にしない。クレカ必須の無料トライアルも使わない。
  - **SFX / ambience の主力 = ElevenLabs**（SFX 生成・効果音・環境音）。
  - **BGM / テーマ音楽の主力 = SUNO**（生成トラックを「素材として取り込む」＝CLAUDE.md §11、`cost-control-policy.md` §2.4）。
  - ナレーション（master）は ElevenLabs だが本書の主対象外（課金前承認は VIDEO_RULES §8）。
- **既存の取得 API（Pexels / Pixabay）は画像・動画のみで音声は取れない。** 音は ElevenLabs/SUNO の別ルートで賄う。無料・商用OKの音源は**補助**に留め、API キー未登録のものは前提にしない（手動取得のみ・後述の権利記録必須）。
- 保存先（CANON）:
  - SFX / ambience 本体 = `H:\pd-media\assets\factory\sfx\`。Asset id は `AF-SFX-NNNN`。`assets/asset_manifest.v001.json`（`docs/asset-manifest-schema.md` の `type: "sfx"`）に登録。
  - BGM は既存の music ライブラリ運用に合わせる（`schemas/music-track.schema.json`、`track_id` = `MUS-NNNN`）。
- 秘密情報（API キー・トークン・Cookie 等）は本書・manifest・ログに一切書かない（CLAUDE.md invariant 3）。
- パスは論理 URI を優先（`.claude/rules/14`）。本書の Windows パスは保存先の物理位置の説明であり、manifest には `artifact://` / `<media>` 相対で格納する。

---

## 1. 音の4層モデル（VIDEO_RULES §11 と一致）

| 層 | 役割 | 調達元（主力） | 保存・登録先 | id |
|---|---|---|---|---|
| ナレーション | 主役。常に明瞭。課金前承認 | ElevenLabs（master） | エピソード成果物（`schemas/asset.schema.json`） | `VC-NNNN`（CLAUDE.md §8） |
| BGM | テーマ音楽。控えめ。フックで上げ・ナレ中は下げる | **SUNO** | music ライブラリ（`schemas/music-track.schema.json`） | `MUS-NNNN` |
| SFX（効果音） | カット/リビール/数字・テロップ出現の短いヒット。要所のみ | **ElevenLabs** | `H:\pd-media\assets\factory\sfx\` ＋ asset_manifest | `AF-SFX-NNNN` |
| 環境音（ambience） | 場面の世界観を支える薄いベッド（法廷ざわめき・街・夜・オフィス等） | **ElevenLabs** | `H:\pd-media\assets\factory\sfx\` ＋ asset_manifest | `AF-SFX-NNNN` |

- **Asset First（先に貯める）**: SFX/ambience/BGM は**話を跨いで再利用できる**ので、少数精鋭でも全話をカバーできる（`asset-priority-list.md` D グループ・`cost-control-policy.md` §5）。エピソードごとに作り直さない。
- **ミックスはダッキング必須**（§5）。ナレが鳴っている間は BGM・環境音を下げ、ナレ最優先（VIDEO_RULES §11）。

---

## 2. ElevenLabs：SFX / ambience 生成の具体運用

### 2.1 1音 = 1生成（原子性）

- **1つの音 = 1回の生成 = 1ファイル = 1 manifest エントリ**。複数の音を1ファイルに混ぜない（再利用・差し替えが効かなくなる）。
- 指示文は「**何の音か・長さ・質感・不要素（no music/voice/melody）**」を明記（`asset-generation-prompts.md` §3.1 の雛形に従う）。
- 具体的な生成リスト本体は `episodes/_planning/sfx_generation_list.md`（ElevenLabs にそのまま渡す形）。本書は方針・運用ルールを定義する。

### 2.2 命名規則

- ファイル名: `AF-SFX-NNNN__<slug>.<ext>`（例 `AF-SFX-0007__whoosh_normal.wav`）。
  - `NNNN` は asset_manifest 上で**昇順に発番**（既存最大 +1）。スラグは英小文字＋アンダースコア。
  - 拡張子: **編集用マスターは `.wav`（48kHz/24bit 推奨）**、配信・プレビュー用に `.mp3` を派生（`previewPath`）。
- manifest 登録（`docs/asset-manifest-schema.md` の `type: "sfx"`）。SFX は非映像なので `width=0 / height=0`、`durationFrames = round(秒 × 30)`、`fps=30`、`hasAlpha=false`。ambience は `loopable=true`。

### 2.3 後処理（長さ・無音・正規化）

- **長さ**: SFX は 0.2–1.5s（whoosh/hit/pop/tick/sweep/glitch）、riser は 2–4s、ambience は 10–30s（loopable bed）。
- **無音処理**: 先頭・末尾の不要な無音をトリム。**頭は実質ゼロ**（フレーム同期で `atFrame` 発火するため遅延を作らない）。ambience は**シームレスループ**（クロスフェードで継ぎ目を消す）。
- **正規化（目安・最終ミックスでの上限管理は編集側）**:
  - **トゥルーピーク上限 = -1 dBTP**（クリップ防止）。
  - SFX 単体ラウドネス目安 ≈ -16 〜 -14 LUFS（要所アクセント）。ambience は控えめに ≈ -23 〜 -20 LUFS（ベッド）。
  - 最終的なナレ最優先のラウドネス整合とダッキングは**編集/ミックス工程**で行い（§5）、素材段階では「-1 dBTP を超えない・極端な無音/ノイズが無い」ことだけ担保する。

### 2.4 課金前承認ゲート（必須）

- ElevenLabs は外部課金 API。**生成の実行前にオーナー承認**を取る（VIDEO_RULES §8「ナレ課金前」と同じ精神を SFX 生成にも適用、`.claude/rules/16` 承認境界、メモのコスト方針）。
- 承認の単位 = `episodes/_planning/sfx_generation_list.md` の**バッチ**（何音を生成するか・想定回数）。承認なしに大量生成しない。
- 外部課金は idempotency キー＋予算チェックを伴う（CLAUDE.md invariant 5、`.claude/rules/11`）。

### 2.5 冪等（二重生成しない）

- **生成前に manifest を検索**（用途/プロンプト類似/subtype）して、既存 SFX で足りないか確認（`cost-control-policy.md` §3）。足りれば生成しない＝`useCases` に新用途を追記するだけ。
- 同じ音（同 subtype・同質感）を二度作らない。`AF-SFX-NNNN` は一度確定したら不変（承認済み成果物は上書きしない＝`.claude/rules/05,12`）。差し替えが要る場合は**新 ID で新規発番**し、旧 ID はアーカイブ（削除しない）。
- 冪等キーの考え方: `subtype + intensity + 秒数レンジ` が一致する既存があれば「再利用」。

---

## 3. SUNO：BGM 運用

### 3.1 テーマ別に複数曲を棚に育てる

- **テーマ（mood）= 5系統**（VIDEO_RULES の語彙・music schema の `category`/`mood` に整合）:

| テーマ | 用途（sceneType 目安） | music schema `category` 目安 |
|---|---|---|
| 緊張（tension） | turning_point, problem_statement, opening_hook 後半 | `tension_build` |
| 荘厳（majestic/solemn） | chapter_title, opening, ending の格調 | `opening` / `outro` |
| 哀感（somber） | emotional_pause, abstract_emotion, 悲劇の幕 | `somber` |
| 解決（resolve/reveal） | solution_reveal, data_reveal の着地, ending 前向き | `reveal` |
| 中立（neutral bed） | explanation, company_profile, 本編の薄い下地 | `explainer_bed` |

- **初期目標 = 5テーマ × 各2曲 = 10曲**（合理的仮定）。シリーズが進むほど棚を育て、エピソードごとの新規生成を逓減させる（`cost-control-policy.md` §2.4）。

### 3.2 ループ点・尺・フェード

- BGM は**ループ可能な構造**で作る（SUNO プロンプトに `loopable sections`、`asset-generation-prompts.md` §4）。`schemas/music-track.schema.json` の `loopable=true` を記録。
- 尺は本編の幕に合わせ**長め**（最低 60s 以上を目安）に確保し、編集側で必要尺にトリム/ループ。フェードイン/アウトは編集側で付与（素材は素のループを保持）。
- `bpm`/`energy`/`duration_sec`/`mood` を music schema に記録し、検索・選曲を効かせる。

### 3.3 再利用ルール（毎回作らない）

- **1エピソード専用にしない。** mood 別の定番トラックを棚に育て、`reuse_count` / `last_used_episode` を更新（music schema フィールド）。
- 新規生成前に**必ず music ライブラリを検索**。同 mood の重複は代表を決め、残りはアーカイブ（生成し続けない）。
- SUNO トラックは**「素材として取り込む」**（プログラム生成は前提にしない＝CLAUDE.md §11）。`source: "suno"` / `suno_origin: true` / `suno_prompt` / `rights_basis`（商用利用可の根拠）を記録。
- SUNO も外部生成のため、**生成バッチは課金前にオーナー承認**（§2.4 と同じ扱い）。

---

## 4. Remotion での使い方（フレーム同期・ダッキング）

- SFX は `docs/remotion-animation-component-roadmap.md` の **`audio/SfxCue`（単発をフレーム発火）/ `audio/SfxScheduler`（複数キューを同期配置）** で鳴らす。`sfxPresets.ts` の論理名（`impact_low` / `whoosh` / `tick` / `click_soft` / `ambient_room` 等）→ 相対 src を解決し `staticFile()` 参照。
- **motion grammar との同期**（`motionPresets.ts`）: 例 `impact_zoom` → `impact_low`、`flash_transition` → `impact_riser`、`number_countup` 終端 → `tick_end`、`keyword_punch` → `click_soft`、`whip_transition`/`pull_out` → `whoosh`。SFX は motion の `sfx` 参照で発火し、`atFrame` でカット/リビールに合わせる。
- ambience は `ambient_room` 等を**シーン尺いっぱいに低音量で敷く**（loopable）。前景イベント音を含めない（`asset-generation-prompts.md` §3.2）。
- **BGM ダッキング**: ナレ（master）が鳴る区間で BGM・ambience のゲインを自動的に下げる（VIDEO_RULES §11 ダッキング必須）。実装はミックス工程（§5）。Remotion 側はトラックの論理配置と相対ゲインを持ち、最終ラウドネス整合は書き出し前の音声ミックスで確定。

---

## 5. ミックス / ダッキング方針（最終整合）

- **ナレ最優先**: ナレが鳴っている間、BGM・ambience を一定量ダッキング（目安 -8 〜 -12 dB）。ナレ無音区間で戻す。クリップ/ノイズ無し（VIDEO_RULES §11、§0 美しさ最優先）。
- **層別の目安ゲイン**（最終ミックス・要調整）: ナレ = 0 dB 基準、SFX = 要所でナレを邪魔しない範囲のアクセント、BGM = ナレ下で控えめ、ambience = 最も薄いベッド。
- 最終配信ラウドネスは編集/書き出し工程で整える（素材段階は -1 dBTP を超えないことのみ担保＝§2.3）。書き出しは最高画質方針と同様、**品質最優先**（VIDEO_RULES §3）。

---

## 6. 無料・商用OK音源（補助・手動取得のみ）の権利記録

- **位置づけ = 補助**。主力は ElevenLabs/SUNO。無料・商用OK音源は、ElevenLabs で代替しにくい実音（特定環境音など）に限り**手動取得**で使うことがある。API キー未登録のサービスを自動取得の前提にしない。
- **使ってよい条件**（VIDEO_RULES §5、メモ「権利確認」）:
  - ライセンスが**商用利用可**であることをサイト上で確認できる（CC0 / royalty-free 等）。
  - 大量ダウンロード（サイト丸ごと）はしない＝規約違反・BAN 回避（VIDEO_RULES §5）。
- **必須の権利記録**（1点ずつ）: **出典 URL / 作者 / ライセンス種別 / 取得日 / sha256（content hash）**。asset_manifest の `license`（`cc0`/`royalty_free`/…）＋ `notes`（出典・作者・取得日）＋ `checksum: "sha256:..."` に格納。
- **禁止事項（絶対）**:
  - **権利不明・規約違反の音源は使わない**（自動でタイムラインに入れない＝review 送り、VIDEO_RULES §5）。
  - 通常の YouTube/TikTok/Instagram/X、ニュース/TV/映画/アニメ/MV/スポーツ映像等からの**無断取得は使わない**（VIDEO_RULES §5 の禁止取得元）。
  - クレカ必須の無料トライアルや、商用可否が確認できないサービスを使わない。
- ElevenLabs/SUNO 生成素材（MJ/Suno 同様の自社生成）は商用利用可で問題なし＝`license: "generated_owned"`（asset_manifest）/ `source:"suno"`＋`rights_basis`（music）。メモ「権利確認」の例外（生成素材は OK）に一致。

---

## 7. 初期に揃える目標数（Asset First・合理的仮定）

`docs/asset-priority-list.md` グループ D（SFX 小計 31）を**音の調達の基準**として踏襲しつつ、ambience を 5 種に拡張し、BGM を加えた音全体の初期目標を示す。

| 区分 | 内容 | 初期目標数 | 調達元 | 備考 |
|---|---|---|---|---|
| SFX（whoosh/hit/pop/tick/riser/sweep/glitch/paper/camera 等） | D グループ各種 ×バリアント | 約 26 | ElevenLabs | 各2〜3バリアント。`sfx_generation_list.md` 準拠 |
| ambience（環境音ベッド） | dark room / courtroom murmur / office hum / city street / night | **5 種**（各1、必要に応じ各2） | ElevenLabs | loopable bed。本書で D の ambience を 5 種へ拡張 |
| BGM（テーマ音楽） | 緊張 / 荘厳 / 哀感 / 解決 / 中立 | **5テーマ × 各2 = 10曲** | SUNO | music ライブラリ登録 |
| **音 初期目標 合計** | | **約 41 点** | | SFX≈26 ＋ ambience 5〜10 ＋ BGM 10 |

- **目安総数 ≈ 40〜45 点**（SFX 約26 ＋ ambience 5（最大10）＋ BGM 10）。`asset-priority-list.md` の SFX 小計 31（SFX＋ambience を含む）と整合し、ambience を 5 種に明示拡張、BGM 10 を加えた値。
- まず P0（whoosh/hit/low hit/pop/tick/riser/ambience dark、BGM 緊張・中立）を優先して揃えれば、最初の 1 話を音 4 層で通せる、という想定。実数は 1 話作って使用率・不足を計測し調整（`cost-control-policy.md` §3 の重複検知指標で監視）。

---

## 8. 運用チェックリスト（コピペ可能）

```
# Audio asset — 生成/取得前チェック
層: [ ]SFX [ ]ambience(ElevenLabs)  [ ]BGM(SUNO)  [ ]無料商用OK音源(手動・補助)
用途(sceneType/grammar): __________

[ ] 棚（asset_manifest / music ライブラリ）を検索し、再利用可能な既存音を確認した
[ ] 既存音で代替不可と確認した（不可の理由を1行記録）
[ ] 1音=1生成・命名 AF-SFX-NNNN__<slug>（SFX/ambience）/ MUS-NNNN（BGM）に従う
[ ] 課金前にオーナー承認を取った（ElevenLabs/SUNO のバッチ単位）
[ ] 後処理: 無音トリム / -1 dBTP 超えない / ambience はシームレスループ
[ ] 無料商用OK音源の場合: 出典URL・作者・ライセンス・取得日・sha256 を記録した
[ ] 権利不明・規約違反・禁止取得元の音は使わない（review 送り）
[ ] 生成後: manifest へ id/sourceTool/path/previewPath/license/checksum/useCases を登録
[ ] コスト超過になる場合: 日本語で停止して確認する
```

---

## 9. 参照

- `episodes/_planning/VIDEO_RULES.md` §11 — 音4層＋ダッキング（上位制約）。
- `docs/asset-priority-list.md` グループ D — SFX 数量・優先度の基準。
- `docs/asset-generation-prompts.md` §3-4 — ElevenLabs / SUNO 生成プロンプト雛形。
- `docs/asset-manifest-schema.md` — `type:"sfx"` の登録フィールド（SFX/ambience）。
- `schemas/music-track.schema.json` — BGM トラックの登録スキーマ。
- `docs/remotion-animation-component-roadmap.md` — `SfxCue`/`SfxScheduler`/`sfxPresets`。
- `docs/cost-control-policy.md` — Asset First・重複検知・追加課金の例外プロセス。
- `episodes/_planning/sfx_generation_list.md` — ElevenLabs にそのまま渡す SFX/ambience 生成リスト。
