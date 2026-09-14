# Asset Priority List（先に大量生成すべき素材リスト）

ステータス: **設計（未実装）**

## 前提・仮定

- 本書は `docs/asset-factory.md`（Asset Factory 設計）の付随書。**「Scene が来る前に、棚に先回りで貯めておくべき素材」を優先度・数量つきで列挙**する。
- グループ A〜G は CANON のツール役割・14カテゴリ・20 sceneType に写像する。語彙は CANON 統一。
- 優先度: **P0 = MVP に必須（最初に作る）／P1 = 早期に欲しい／P2 = 後追いで拡充**。
- 数量は**合理的仮定**。根拠の基本方針:
  - PD は 12 分前後・約 4.5 秒切替 → 1話あたり概ね 130〜160 カット（VIDEO_RULES §3）。
  - 背景・人物などは「同じ絵の使い回しは飽きる」ため **mood × 複数枚**で多様性を確保。
  - SFX・図解パーツ・装飾枠は **話を跨いで使い回せる**ので、少数精鋭でも全話カバー可能。
- **MVP の定義（仮定）**: 最初の 1〜2 話（縦長 12 分）をファクトリー主体でラフカットまで通せる素材量。
- 「実在人物の肖像なし」「画面文字なし（テキストは Remotion 側で重畳）」を全素材で厳守。

---

## グループ別優先度・数量

表の見方:
- 数量 = MVP 初期目標（先に作る最低ライン）。括弧内は将来拡充の目安。
- カテゴリ = `docs/asset-factory.md` の14カテゴリ名。
- ツール = 生成ツール（CANON 役割）。

### A. 共通ベース素材（全話に薄く重なる土台）— 最優先 P0

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| film grain（粒状ノイズ overlay） | P0 | 3（→6） | 合成/Runway | vfx_overlays | 全 |
| vignette（周辺減光） | P0 | 2 | Midjourney/合成 | vfx_overlays | 全 |
| dust（舞うほこり・黒背景） | P0 | 3 | Midjourney→動/Runway | particle_assets | emotional_pause, abstract_emotion, 全 |
| smoke（煙・黒背景） | P0 | 4 | Midjourney→動/Runway | particle_assets | turning_point, abstract_emotion, opening_hook |
| particle field（漂う粒子ループ） | P0 | 3 | Runway/SDXL動 | particle_assets | abstract_emotion, emotional_pause |
| light leak（光漏れ） | P0 | 4 | Midjourney(静)/合成(動) | light_assets | turning_point, ending, opening_hook |
| bokeh（玉ボケループ） | P0 | 3 | Midjourney→動 | particle_assets | emotional_pause, abstract_emotion |
| noise/scanline（走査線・ノイズ） | P1 | 2 | 合成 | vfx_overlays | reenactment, evidence_board |
| paper texture（紙質感） | P0 | 3 | Midjourney | texture_assets | quote, evidence_board, chapter_title |
| atmosphere loop（暗い空気感の背景ループ） | P1 | 4 | Runway/SDXL動 | loops | explanation, emotional_pause, abstract_emotion |
| **A 小計** | | **34** | | | |

### B. 図解パーツ（モーショングラフィックの部品）— 最優先 P0

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| arrow（方向矢印・各角度） | P0 | 6 | SVG/Midjourney | diagram_assets | timeline, comparison, solution_reveal |
| line（直線・点線） | P0 | 4 | SVG | diagram_assets | timeline, evidence_board |
| relationship line（関係線・結線） | P0 | 4 | SVG | diagram_assets | evidence_board, comparison |
| bracket（くくり括弧） | P1 | 3 | SVG | diagram_assets | comparison, explanation |
| timeline dot（年表の点） | P0 | 3 | SVG | diagram_assets | timeline |
| node（ノード・円/箱） | P0 | 4 | SVG | diagram_assets | evidence_board, comparison |
| label（ラベル枠） | P0 | 4 | SVG/Midjourney | diagram_assets | 全情報系 |
| map pin（地図ピン） | P1 | 3 | SVG/Lottie | diagram_assets | place_intro, timeline |
| highlight box（強調枠） | P0 | 3 | SVG | diagram_assets | evidence_board, data_reveal |
| chart accent（グラフ装飾） | P1 | 3 | SVG | diagram_assets | data_reveal, comparison |
| number badge（数字バッジ） | P0 | 4 | SVG/Midjourney | diagram_assets | data_reveal, timeline |
| warning label（警告ラベル） | P2 | 2 | SVG/Lottie | diagram_assets | problem_statement, evidence_board |
| check icon（チェック） | P1 | 2 | SVG/Lottie | diagram_assets | comparison, solution_reveal |
| comparison divider（左右比較の仕切り） | P1 | 2 | SVG | diagram_assets | comparison |
| **B 小計** | | **47** | | | |

### C. 章タイトル / 字幕装飾枠（テキストは入れない・枠のみ）— 最優先 P0

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| chapter title frame（章扉枠） | P0 | 3 | Midjourney/合成 | typography_assets | chapter_title |
| lower third（下三分テロップ枠） | P0 | 3 | 合成 | typography_assets | character_profile, company_profile, explanation |
| keyword badge（キーワード枠） | P0 | 3 | 合成 | typography_assets | explanation, data_reveal |
| quote frame（引用枠） | P0 | 2 | Midjourney/合成 | typography_assets | quote |
| data reveal frame（数字リビール枠） | P0 | 2 | 合成 | typography_assets | data_reveal |
| title accent（タイトル装飾） | P1 | 2 | 合成 | typography_assets | opening_hook, chapter_title |
| subtitle emphasis（字幕強調装飾） | P1 | 2 | 合成 | typography_assets | quote, summary |
| **C 小計** | | **17** | | | |

### D. SFX（効果音）— 最優先 P0（話を跨いで全話再利用）

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| whoosh（標準） | P0 | 3 | ElevenLabs | sfx | transition_bridge, 全カット |
| fast whoosh（速い） | P0 | 2 | ElevenLabs | sfx | opening_hook, turning_point |
| soft whoosh（柔らかい） | P1 | 2 | ElevenLabs | sfx | emotional_pause |
| hit / impact（標準ヒット） | P0 | 3 | ElevenLabs | sfx | data_reveal, turning_point |
| low hit（重低音ヒット） | P0 | 2 | ElevenLabs | sfx | turning_point, problem_statement |
| pop（出現ポップ） | P0 | 2 | ElevenLabs | sfx | data_reveal, evidence_board |
| tick（時計/カウント） | P0 | 2 | ElevenLabs | sfx | timeline, data_reveal |
| riser（盛り上げ） | P0 | 2 | ElevenLabs | sfx | opening_hook, turning_point |
| ambience dark（暗い環境音） | P0 | 2 | ElevenLabs | sfx | emotional_pause, abstract_emotion |
| ambience office（オフィス環境音） | P1 | 1 | ElevenLabs | sfx | company_profile, reenactment |
| ambience city（街の環境音） | P1 | 1 | ElevenLabs | sfx | place_intro |
| paper slide（紙をめくる/滑らす） | P1 | 2 | ElevenLabs | sfx | evidence_board, quote |
| camera click（カメラシャッター） | P1 | 1 | ElevenLabs | sfx | reenactment, evidence_board |
| glitch（グリッチ） | P2 | 1 | ElevenLabs | sfx | reenactment, abstract_emotion |
| sweep（スイープ） | P1 | 2 | ElevenLabs | sfx | transition_bridge |
| bass accent（低音アクセント） | P1 | 2 | ElevenLabs | sfx | turning_point, ending |
| **D 小計** | | **31** | | | |

### E. Midjourney 静止画（分解的レイヤー前提・大量）— P0/P1

> mood 軸（仮定）= dark / tense / hopeful / neutral / somber の中から各素材で主要 2〜3 を用意。

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| documentary bg（汎用ドキュ背景） | P0 | mood×3 = 9 | Midjourney | backgrounds | explanation, problem_statement |
| business room（会議室/重役室） | P0 | 4 | Midjourney | backgrounds | company_profile, reenactment |
| office（オフィス） | P0 | 4 | Midjourney | backgrounds | company_profile, explanation |
| abstract dark cinematic（抽象・暗いシネマ） | P0 | 6 | Midjourney | backgrounds | abstract_emotion, chapter_title, opening_hook |
| technology（技術・装置・基板） | P1 | 4 | Midjourney | backgrounds | solution_reveal, explanation |
| emotional landscape（情景・風景） | P0 | 5 | Midjourney | backgrounds | emotional_pause, place_intro, ending |
| investigative board（捜査ボード/証拠） | P0 | 3 | Midjourney | backgrounds | evidence_board |
| 人物（顔を特定しない・後ろ姿/シルエット/手元） | P0 | 6 | Midjourney | parallax_layers/backgrounds | character_profile, reenactment |
| 前景ぼかし（被写界深度の前ボケ） | P1 | 4 | Midjourney | parallax_layers | place_intro, emotional_pause |
| 光（窓光/逆光パーツ） | P1 | 3 | Midjourney | light_assets | turning_point, ending |
| 煙（静止の煙パーツ） | P1 | 3 | Midjourney | particle_assets | abstract_emotion, turning_point |
| **E 小計** | | **51** | | | |

### F. Runway 見せ場動画（決め所だけ・高コスト）— P1

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| opening（冒頭の象徴カット） | P0 | 2 | Runway | ai_video_shots | opening_hook |
| turning point（転換点） | P1 | 2 | Runway | ai_video_shots | turning_point |
| emotional pause（情感の間） | P1 | 2 | Runway | ai_video_shots | emotional_pause |
| ending（締め） | P1 | 2 | Runway | ai_video_shots | ending |
| reenactment（再現の動き） | P1 | 2 | Runway | ai_video_shots | reenactment |
| symbolic cut（象徴的カット） | P2 | 2 | Runway | ai_video_shots | abstract_emotion, turning_point |
| abstract mood（抽象ムード） | P2 | 2 | Runway | ai_video_shots | abstract_emotion |
| **F 小計** | | **14** | | | |

### G. Lottie（手動DL・ローカル JSON のみ・API/有料なし）— P1/P2

| 素材 | 優先 | MVP数量 | ツール | カテゴリ | 対応 sceneType |
|---|---|---|---|---|---|
| arrow（矢印アニメ） | P1 | 2 | LottieFiles(手動DL) | lottie_assets | timeline, solution_reveal |
| line draw（線が描かれる） | P1 | 2 | LottieFiles | lottie_assets | timeline, evidence_board |
| loading（読み込み） | P2 | 1 | LottieFiles | lottie_assets/ui_motion_assets | reenactment, data_reveal |
| check（チェック完了） | P1 | 1 | LottieFiles | lottie_assets | comparison, solution_reveal |
| warning（警告） | P2 | 1 | LottieFiles | lottie_assets | problem_statement |
| map pin（地図ピン落下） | P1 | 1 | LottieFiles | lottie_assets | place_intro, timeline |
| chart（グラフ描画） | P1 | 2 | LottieFiles | lottie_assets | data_reveal, comparison |
| business icon（ビジネス系アイコン） | P2 | 2 | LottieFiles | lottie_assets | company_profile, explanation |
| UI accent（UI装飾） | P2 | 1 | LottieFiles | ui_motion_assets | evidence_board, data_reveal |
| chapter decoration（章装飾アニメ） | P2 | 1 | LottieFiles | lottie_assets | chapter_title |
| **G 小計** | | **14** | | | |

---

## MVP 初期目標（合計）

| グループ | 内容 | MVP 数量 |
|---|---|---|
| A | 共通ベース素材 | 34 |
| B | 図解パーツ | 47 |
| C | 章タイトル/字幕装飾枠 | 17 |
| D | SFX | 31 |
| E | Midjourney 静止画 | 51 |
| F | Runway 見せ場動画 | 14 |
| G | Lottie | 14 |
| **合計** | | **約 208 点** |

> **概算 MVP 初期目標 = 約 200〜210 点**（仮定）。内訳の重心は **P0 が約 6 割**。
> まず P0 のみ（概算 約 120〜130 点）を揃えれば、最初の1話を「背景・overlay・図解・装飾枠・SFX はファクトリー、見せ場は Runway 少量、B-roll/実景は既存実写プール」という構成でラフカットまで通せる、という想定。
> F（Runway）は高コストのため、**MVP では P0 の opening 2 点を優先**し、他は実素材プールや SDXL ループで代替しつつ段階追加する。

### 数量仮定の根拠メモ

- B・C・D は **episode 横断で再利用される汎用部品**なので、少数（合計 ~95）で全話の情報系・装飾・効果音をほぼカバーできると仮定。
- A・E は **見た目の多様性**が retention に効くため mood × 複数で多めに確保。
- G の Lottie は手動DLのため数を絞り、図解は基本 B（SVG/Remotion 描画）で賄う方針（Lottie は補助）。
- 実数は最初の1話を作って **使用率・不足カテゴリ**を計測し、`docs/asset-factory.md` §4.3 の棚卸しサイクルで調整する。

---

## 参照

- `docs/asset-factory.md` — カテゴリ仕様・manifest・運用ルール・importer 接続。
- `docs/asset-generation-prompts.md` — 各素材の生成プロンプト雛形。
- `episodes/_planning/VIDEO_RULES.md` — 制作ルール（数量・品質の上位制約）。
