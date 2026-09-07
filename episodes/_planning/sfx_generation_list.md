# SFX / Ambience 生成リスト（ElevenLabs にそのまま渡す）

ステータス: **設計／前提・仮定**

## 前提・仮定

- 本書は `docs/audio-sfx-bgm-library-plan.md` の付随書。**ElevenLabs の SFX/ambience 生成にそのまま渡せる 1 音単位のリスト**。`docs/asset-priority-list.md` グループ D ＋ ドキュメンタリーで多用する音を網羅する。`docs/asset-generation-prompts.md` §3、`VIDEO_RULES.md` §11 と矛盾させない。
- **1音 = 1生成 = 1ファイル = 1 manifest エントリ**。命名 `AF-SFX-NNNN__<slug>.wav`（マスター）＋ `.mp3`（preview）。保存先 `H:\pd-media\assets\factory\sfx\`。`assets/asset_manifest.v001.json`（`type:"sfx"`）に登録。
- `AF-SFX-NNNN` の `NNNN` は**仮の候補ID**。実発番は asset_manifest 上の既存最大 +1 で昇順に確定する（本書の番号は並び順の目安）。
- 生成指示文は**英語・短く・具体的**。全文に共通で含める固定句（毎回末尾に付与）:
  `No music, no voice, no melody, no speech. Broadcast-clean, dry/minimal reverb. For a premium cinematic documentary.`
- 後処理（全音共通）: 先頭/末尾の不要無音をトリム（頭は実質ゼロ）、トゥルーピーク **-1 dBTP** を超えない、ambience は**シームレスループ**化（`loopable=true`）。
- SFX は `width=0/height=0`、`durationFrames = round(秒×30)`、`fps=30`、`hasAlpha=false`、`license="generated_owned"`（ElevenLabs 自社生成＝商用OK）。
- 末尾の注記（課金前承認 / 生成後 manifest 登録 / 重複生成しない）を必ず守る。

凡例: 推奨尺は秒。`grammar` は `docs/remotion-animation-component-roadmap.md` の motion grammar、`sceneType` は CANON 20 sceneType。

---

## A. whoosh（soft / normal / fast）— 3 種 ×バリアント

| 候補ID | slug | 用途（grammar / sceneType） | 英語 生成指示文（+共通固定句） | 推奨尺 | ファイル名 |
|---|---|---|---|---|---|
| AF-SFX-0001 | whoosh_soft_a | whip_transition(soft) / emotional_pause | A soft, gentle airy whoosh, smooth air movement, low energy | 0.6s | `AF-SFX-0001__whoosh_soft_a.wav` |
| AF-SFX-0002 | whoosh_soft_b | whip_transition(soft) / emotional_pause | A soft slow whoosh, breathy air pass, subtle and calm | 0.8s | `AF-SFX-0002__whoosh_soft_b.wav` |
| AF-SFX-0003 | whoosh_normal_a | whip_transition / transition_bridge | A clean cinematic transition whoosh, mid energy air movement | 0.5s | `AF-SFX-0003__whoosh_normal_a.wav` |
| AF-SFX-0004 | whoosh_normal_b | whip_transition / transition_bridge | A standard whoosh for a scene transition, crisp air swish | 0.5s | `AF-SFX-0004__whoosh_normal_b.wav` |
| AF-SFX-0005 | whoosh_fast_a | fast_push_in / opening_hook, turning_point | A fast aggressive whoosh, quick sharp air movement, high energy | 0.3s | `AF-SFX-0005__whoosh_fast_a.wav` |
| AF-SFX-0006 | whoosh_fast_b | fast_push_in / opening_hook, turning_point | A very fast snappy whoosh, rapid swish, punchy | 0.3s | `AF-SFX-0006__whoosh_fast_b.wav` |

## B. hit / low hit / bass accent — 3 種 ×バリアント

| 候補ID | slug | 用途 | 英語 生成指示文（+共通固定句） | 推奨尺 | ファイル名 |
|---|---|---|---|---|---|
| AF-SFX-0007 | hit_normal_a | impact_zoom / data_reveal, turning_point | A clean cinematic impact hit, punchy and tight, mid-weight | 0.4s | `AF-SFX-0007__hit_normal_a.wav` |
| AF-SFX-0008 | hit_normal_b | impact_zoom / data_reveal, turning_point | A short impact hit, dry and percussive, clear transient | 0.4s | `AF-SFX-0008__hit_normal_b.wav` |
| AF-SFX-0009 | low_hit_a | impact_zoom / turning_point, problem_statement | A deep low impact hit with sub-bass weight, heavy and dramatic | 0.6s | `AF-SFX-0009__low_hit_a.wav` |
| AF-SFX-0010 | low_hit_b | impact_zoom / turning_point, problem_statement | A heavy low boom hit, strong sub-bass, cinematic weight | 0.7s | `AF-SFX-0010__low_hit_b.wav` |
| AF-SFX-0011 | bass_accent_a | impact_zoom / turning_point, ending | A low bass accent, short sub rumble swell, subtle weight | 0.8s | `AF-SFX-0011__bass_accent_a.wav` |
| AF-SFX-0012 | bass_accent_b | impact_zoom / turning_point, ending | A deep bass accent drop, restrained low-end emphasis | 0.9s | `AF-SFX-0012__bass_accent_b.wav` |

## C. pop / tick — 2 種 ×バリアント

| 候補ID | slug | 用途 | 英語 生成指示文（+共通固定句） | 推奨尺 | ファイル名 |
|---|---|---|---|---|---|
| AF-SFX-0013 | pop_a | soft_reveal / data_reveal, evidence_board | A short clean pop sound for a UI reveal, soft and pleasant, not harsh | 0.2s | `AF-SFX-0013__pop_a.wav` |
| AF-SFX-0014 | pop_b | soft_reveal / data_reveal, evidence_board | A subtle bubble-like pop for an element appearing, gentle | 0.2s | `AF-SFX-0014__pop_b.wav` |
| AF-SFX-0015 | tick_a | number_countup / timeline, data_reveal | A crisp short tick like a clock or counter, clean and dry | 0.15s | `AF-SFX-0015__tick_a.wav` |
| AF-SFX-0016 | tick_b | number_countup / timeline, data_reveal | A light mechanical tick, single click, sharp transient | 0.15s | `AF-SFX-0016__tick_b.wav` |
| AF-SFX-0017 | tick_end | number_countup(終端) / data_reveal | A final tick with a soft confirming accent, end of count | 0.3s | `AF-SFX-0017__tick_end.wav` |

## D. riser / sweep — 2 種 ×バリアント

| 候補ID | slug | 用途 | 英語 生成指示文（+共通固定句） | 推奨尺 | ファイル名 |
|---|---|---|---|---|---|
| AF-SFX-0018 | riser_a | flash_transition / opening_hook, turning_point | A rising tension riser, building suspense, ending on a clean cutoff | 3.0s | `AF-SFX-0018__riser_a.wav` |
| AF-SFX-0019 | riser_b | flash_transition / opening_hook, turning_point | A short build-up riser swelling into an impact point | 2.5s | `AF-SFX-0019__riser_b.wav` |
| AF-SFX-0020 | sweep_a | whip_transition / transition_bridge | A filtered sweep transition, smooth spectral whoosh, airy | 1.0s | `AF-SFX-0020__sweep_a.wav` |
| AF-SFX-0021 | sweep_b | whip_transition / transition_bridge | A noise sweep for a transition, soft rising then falling | 1.2s | `AF-SFX-0021__sweep_b.wav` |

## E. glitch / paper slide / camera click — 各 2 ×バリアント

| 候補ID | slug | 用途 | 英語 生成指示文（+共通固定句） | 推奨尺 | ファイル名 |
|---|---|---|---|---|---|
| AF-SFX-0022 | glitch_a | glitch_transition / reenactment, abstract_emotion | A short digital glitch, brief stuttering electronic artifact, restrained | 0.4s | `AF-SFX-0022__glitch_a.wav` |
| AF-SFX-0023 | glitch_b | glitch_transition / turning_point, problem_statement | A subtle glitch sweep, digital noise burst, not harsh | 0.5s | `AF-SFX-0023__glitch_b.wav` |
| AF-SFX-0024 | paper_slide_a | evidence_reveal / evidence_board, quote | A paper sliding sound, single sheet moving across a desk, dry foley | 0.6s | `AF-SFX-0024__paper_slide_a.wav` |
| AF-SFX-0025 | paper_slide_b | evidence_reveal / evidence_board, quote | A page turn / paper shuffle, single crisp foley event | 0.7s | `AF-SFX-0025__paper_slide_b.wav` |
| AF-SFX-0026 | camera_click_a | evidence_reveal / reenactment, evidence_board | A camera shutter click, single dry mechanical snap | 0.3s | `AF-SFX-0026__camera_click_a.wav` |
| AF-SFX-0027 | camera_click_b | evidence_reveal / reenactment, evidence_board | A photo camera shutter with a soft mechanical recoil, single event | 0.3s | `AF-SFX-0027__camera_click_b.wav` |

## F. ambience（環境音ベッド・loopable）— 5 種 ×バリアント

> すべて `loopable=true`、前景イベント音を含めない（薄いベッド）。`durationFrames` は尺×30 だが、編集側でループ。

| 候補ID | slug | 用途（sceneType） | 英語 生成指示文（+共通固定句） | 推奨尺 | ファイル名 |
|---|---|---|---|---|---|
| AF-SFX-0028 | amb_dark_room_a | emotional_pause, abstract_emotion | A dark quiet room tone ambience bed, low subtle hum, tense atmosphere, seamless loop, no foreground events | 20s | `AF-SFX-0028__amb_dark_room_a.wav` |
| AF-SFX-0029 | amb_dark_room_b | emotional_pause, abstract_emotion | A deep ominous room ambience, faint air movement, unsettling calm, seamless loop | 25s | `AF-SFX-0029__amb_dark_room_b.wav` |
| AF-SFX-0030 | amb_courtroom_murmur_a | quote, evidence_board, turning_point | A courtroom murmur ambience, distant indistinct crowd chatter, formal hall reverb, seamless loop, no clear words | 20s | `AF-SFX-0030__amb_courtroom_murmur_a.wav` |
| AF-SFX-0031 | amb_courtroom_murmur_b | quote, evidence_board | A quiet public hall ambience with low crowd murmur, settling room, seamless loop, no intelligible speech | 25s | `AF-SFX-0031__amb_courtroom_murmur_b.wav` |
| AF-SFX-0032 | amb_office_hum_a | company_profile, reenactment, explanation | An office ambience bed, quiet HVAC hum and faint distant activity, neutral, seamless loop, no clear voices | 20s | `AF-SFX-0032__amb_office_hum_a.wav` |
| AF-SFX-0033 | amb_office_hum_b | company_profile, explanation | A modern office room tone, soft electrical hum and air conditioning, seamless loop | 25s | `AF-SFX-0033__amb_office_hum_b.wav` |
| AF-SFX-0034 | amb_city_street_a | place_intro, timeline | A city street ambience, distant traffic and urban hum, no sirens, seamless loop, no foreground events | 25s | `AF-SFX-0034__amb_city_street_a.wav` |
| AF-SFX-0035 | amb_city_street_b | place_intro | A calm city background ambience, far traffic and faint wind, neutral urban bed, seamless loop | 25s | `AF-SFX-0035__amb_city_street_b.wav` |
| AF-SFX-0036 | amb_night_a | emotional_pause, ending, abstract_emotion | A quiet night ambience, faint wind and distant low tone, calm and sparse, seamless loop, no animals | 25s | `AF-SFX-0036__amb_night_a.wav` |
| AF-SFX-0037 | amb_night_b | emotional_pause, ending | A still night room tone with very faint outdoor air, somber calm, seamless loop | 25s | `AF-SFX-0037__amb_night_b.wav` |

---

## 合計の目安数

| カテゴリ | 種類 | バリアント込み 本数 |
|---|---|---|
| A. whoosh（soft/normal/fast） | 3 | 6 |
| B. hit / low hit / bass accent | 3 | 6 |
| C. pop / tick（+tick_end） | 2(+1) | 5 |
| D. riser / sweep | 2 | 4 |
| E. glitch / paper slide / camera click | 3 | 6 |
| F. ambience（dark room/courtroom/office/city/night） | 5 | 10 |
| **SFX/ambience 合計** | | **37 音** |

> **目安総数 = 37 音**（SFX 約 27 ＋ ambience 10）。`docs/asset-priority-list.md` グループ D（小計 31）を踏襲しつつ、各 2〜3 バリアント・ambience 5 種化で拡張した値。BGM（SUNO・5テーマ×各2＝10曲）は別ルート（`docs/audio-sfx-bgm-library-plan.md` §3）。**音 初期目標 全体 ≈ 47 点**（SFX/ambience 37 ＋ BGM 10）。

---

## 注記（必須・厳守）

1. **課金前にオーナー承認**: ElevenLabs は外部課金 API。生成の実行前に、本リストの**バッチ単位**でオーナー承認を取る（VIDEO_RULES §8・`.claude/rules/16`・メモのコスト方針）。承認なしに大量生成しない。idempotency キー＋予算チェックを伴う。
2. **生成後 manifest 登録**: 生成した各音を `assets/asset_manifest.v001.json`（`type:"sfx"`）へ登録する。最低フィールド = `id / type:"sfx" / subtype / path / previewPath / sourceTool:"elevenlabs" / durationFrames / fps:30 / width:0 / height:0 / hasAlpha:false / loopable / mood / intensity / useCases / compatibleSceneTypes / colorTone:"neutral" / tags / sourcePrompt(指示文) / negativePrompt:null / seed:null / license:"generated_owned" / createdAt / notes / checksum("sha256:...")`。
3. **重複生成しない**: 生成前に必ず manifest を検索（subtype/用途/指示文の類似）。既存で足りれば生成せず `useCases` を追記。確定した `AF-SFX-NNNN` は不変（上書き禁止）。差し替えは新 ID で発番し旧 ID はアーカイブ（削除しない）。
