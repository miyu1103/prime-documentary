---
title: "PD Visual System v2 - Claude Code Master Reference"
version: "2.0.0"
date: "2026-07-11"
language: "ja-JP"
status: "Operational reference and deployable specification"
project: "Prime Documentary"
execution_model: "Phase-gated Claude Code kit"
---

# PD VISUAL SYSTEM v2
# Claude Code向け・100点運用設計マスターリファレンス

> 本書は、Prime Documentaryの映像制作を「静止画を並べて少し動かす紙芝居」から、実在資料、実写、情報アニメーション、2.5D、再利用3D空間、限定的AI B-rollを統合した高品質な法律ドキュメンタリーへ移行するための正本である。
>
> 本書は巨大な**参考正本**であり、毎セッションの常時命令ではない。実行時は短い `CLAUDE.md`、path-scoped Rules、手動起動のPhase Skills、Phase State、Permissions、PreToolUse Hookを使用する。巨大さを知識の貯蔵庫に限定し、実行時の注意散漫を防ぐ。

---

# 0. この完成版の結論

最適解は「さらに長い一枚岩プロンプト」ではない。

最適解は次の二層構造である。

```text
知識・思想・技術の巨大正本
MASTER_REFERENCE.md
        │ 必要なときだけ参照
        ▼
短い常設ルール + Phase別の実行契約
CLAUDE.md / rules / skills / state / hooks
        │
        ▼
Claude Codeが一つのPhaseだけを実行
```

この構造により、次を同時に実現する。

1. 研究内容を失わない。
2. Claude Codeが一度に背負う指示量を減らす。
3. Phaseの先走りを防ぐ。
4. 削除、上書き、Git履歴改変などをモデルの善意ではなく仕組みで止める。
5. どの追加技術が品質へ寄与したかを増分比較できる。
6. 一話で成功した演出を、次話で再現可能な資産へ変える。

## 0.1 PDが目指す映像方式

> **Evidence-First Cinematic Documentary**
>
> 実際の証拠が真実を担う。  
> アニメーションが理解を担う。  
> 実写と正規B-rollが現実感を担う。  
> 2.5Dが静止画へ奥行きを与える。  
> 3Dが空間とブランド世界を担う。  
> AIは不足する短い雰囲気B-rollだけを補う。  
> 音が感情と切り替えを主導する。

## 0.2 一番重要な原則

紙芝居感の原因は、静止画の使用そのものではない。

**シーンの開始時と終了時で、視聴者の理解が変わっていないこと**が本体である。

悪い例:

```text
人物写真
→ 6秒ズーム
→ 同じ人物写真の意味のまま終了
```

良い例:

```text
人物写真
→ 押収された財産を提示
→ 財産価値と法定罰金を比較
→ 不均衡を一つの軸へ揃える
→ 争点を一文へ圧縮
→ 最高裁へ進む経路を示す
```

動かすべきものは、煙、粒子、カメラだけではない。

**人物、証拠、金額、場所、権限、判決の関係を動かす。**

## 0.3 作るものと作らないもの

### 作るもの

- 再利用可能なRemotionコア5部品
- 85,000点の素材をカット単位で検索する索引
- ナレーションと画面変化を同期するcue
- 1枚の静止画を安全に2.5D化する限定パイプライン
- 再利用可能な `PD Evidence Room`
- 不足素材だけを生成するComfyUIワークフロー
- 出典、真実性、ライセンス、AI開示を追跡するデータ契約
- A/B1/B2/B3/C1/C2/C3の増分比較記録

### 初期段階で作らないもの

- 新しい動画編集ソフト
- ElectronやStreamlitの巨大管理画面
- 自動制作OSという名のモノリス
- 全編AI動画
- DaVinci Resolveのマウス座標自動操作
- ブラウザスクレイピング
- 競合の固有デザイン複製
- 85,000点全件を初回から処理する巨大ジョブ

---

# 1. 本書と運用ファイルの役割分担

## 1.1 正本の優先順位

矛盾が発生した場合、Claude Codeは次の順で判断する。

1. ユーザーの最新の明示指示
2. `docs/pd-visual-system/PHASE_STATE.json`
3. ユーザーが明示起動した現在PhaseのSkill
4. 対象ファイルに適用される `.claude/rules/*.md`
5. `CLAUDE.md`
6. 本書 `MASTER_REFERENCE.md`
7. 旧仕様、古いプロンプト、推測

## 1.2 各ファイルの責務

| ファイル | 責務 | 常時読むか |
|---|---|---|
| `CLAUDE.md` | 常に守る短い原則 | はい |
| `PHASE_STATE.json` | 現在Phaseと状態 | はい |
| `.claude/skills/pd-phase-*/SKILL.md` | そのPhaseの実行契約 | 明示実行時だけ |
| `.claude/rules/*.md` | 対象パス固有の品質ルール | 関連作業時だけ |
| `.claude/settings.json` | PermissionsとHooks | Claude Codeが強制 |
| `.claude/hooks/pd_safety_gate.py` | 危険操作のdeny/ask | 操作直前 |
| `MASTER_REFERENCE.md` | 思想・技術・判断材料の巨大正本 | 必要な章だけ |
| `IMPLEMENTATION_STATUS.md` | 実装事実、証拠、限界 | Phase開始・終了時 |
| `DECISION_LOG.md` | 採否判断と理由 | 判断時 |

## 1.3 なぜ一枚岩を実行プロンプトにしないのか

巨大な正本を毎回全文ロードすると、現在の作業と無関係な将来計画、モデル選定、検索クエリ、ライセンス表、全Phaseの完了条件が同時に注意を奪う。

その結果、次の失敗が起こりやすい。

- 現在Phase以外へ先回りする
- 同じ機能を別名で重複実装する
- 既存環境を調べる前にインストールする
- 重要な禁止事項が長文の中で薄まる
- 映像改善より自動化基盤の開発へ脱線する
- コンテキスト圧縮後に古い判断が復活する

この完成版では、長い知識は残し、実行契約だけを小さく切り出す。

---

# 2. 前提、仮定、検証責任

以下は会話上の暫定前提であり、P00で実機確認する。

| 項目 | 暫定前提 | P00での確認 |
|---|---|---|
| OS | Windows | バージョン、PowerShell、パス規則 |
| GPU | NVIDIA RTX 4090 24GB | `nvidia-smi`、driver、CUDA互換性 |
| リポジトリ | `C:\Users\aab15\Documents\prime-documentary` | 実在パス、Git root、branch |
| メディア | `H:\pd-media` | 存在、空き容量、読み書き境界 |
| 対象話 | `PD-2026-009-timbs` | 実際のepisode path |
| 編集基盤 | Remotion | version、entry、render command |
| 最終仕上げ | DaVinci Resolve | edition、API、既存workflow |
| 素材量 | 約85,000点 | 実数、種類、重複、権利メタデータ |
| 出力 | 英語圏YouTube | 解像度、fps、字幕、公開方針 |
| 司令塔 | Claude Code、Codex補助 | ローカル権限、承認方式 |

## 2.1 不足情報の処理

- 読み取りで解決できる事項は質問せず調査する。
- 低リスクの仮定は `ASSUMPTIONS.md` に記録して進める。
- 破壊的変更、課金、外部公開、規約同意、大容量ダウンロードだけは事前承認対象とする。
- 不明なライセンスは `review_required` とし、採用しない。
- 不明な技術要件は最小PoCで測定し、推測で本番設計へ固定しない。

## 2.2 実装で変えてよいもの

- 新規ファイル
- isolated venv
- test composition
- preview output
- index DB、thumbnail、manifest
- 明示されたRemotion部品
- docsとschemas

## 2.3 実装で守るもの

- 既存素材原本
- baseline render
- 既存エピソードの正本
- 未コミット変更
- Git履歴
- ライセンス記録
- 台本文言
- 公開済み成果物

---

# 3. 成功の定義と評価モデル

## 3.1 成功はレンダリング完了ではない

成功は、次の4価値が同時に成立することである。

### 視聴者価値

- 誰が当事者かを失わない
- 何が起きたかを失わない
- 何を失ったかを理解できる
- どの利害が対立するかを理解できる
- どの裁判所で何が変わったかを理解できる
- 判決の条件と限界を理解できる

### 映像価値

- start stateとend stateが異なる
- 一画面一主役
- 動きが意味へ従属する
- 実写、資料、図解、3D、AIの役割が混ざらない
- 重要語と視覚変化が同期する
- 音の山谷が重要度を示す

### 制作価値

- 次話へ再利用できる
- エピソード固有コードが増殖しない
- 失敗を再開できる
- 設定と出力が追跡可能
- 変更差分が小さい
- 導入技術の費用対効果が測れる

### 信頼価値

- 実在資料と再現を区別する
- 引用を改変しない
- AIで証拠を捏造しない
- ライセンス不明を本番へ入れない
- 必要なAI開示を行う
- 推測を事実として描かない

## 3.2 成果の乗算モデル

```text
クリック = 題材 × タイトル × サムネイル
視聴維持 = 脚本の因果 × 緊張 × 理解しやすさ
高級感 = アートディレクション × モーション × 音
量産性 = 再利用率 × 素材検索力 × 品質管理
信頼 = 出典 × 真実性区分 × 開示 × 引用正確性
```

アニメーションは成功の原因を単独で作る魔法ではない。理解、視線、高級感、ブランドを増幅する装置である。

## 3.3 紙芝居診断の8軸

| 軸 | 問い | 失敗の典型 |
|---|---|---|
| 時間変化 | 画面内部で意味ある変化があるか | ただのズーム |
| 意味変化 | 理解が更新されたか | 同じ写真のまま終了 |
| 奥行き | 前景・中景・背景があるか | 全レイヤー同速 |
| 視線誘導 | 見る場所が一つか | 複数要素が競合 |
| 音声同期 | 重要語と動きが合うか | 演出が早い・遅い |
| 素材の時間性 | 動画を探すべき場面で静止画へ逃げていないか | 素材検索不全 |
| 編集文法 | カット、トランジションに意味があるか | 種類だけ多い |
| 感情・緊張 | 重要場面に山谷があるか | 常に同じ派手さ |

## 3.4 シーン品質スコア

各シーンを0〜4点で採点する。

```text
0: 欠落または誤解を生む
1: 存在するが弱い
2: 最低限機能する
3: 明確で再利用可能
4: 非常に明確で、視聴者理解と感情を同時に支える
```

採点項目:

1. Visual questionの明確さ
2. start/end stateの差
3. 主要visual verbの一貫性
4. eye targetの明確さ
5. source truthの明確さ
6. 音声同期
7. 素材品質
8. モーションの目的性
9. 音響の役割
10. 再利用性

40点満点中、release candidateは原則32点以上かつhard blockerなしとする。

---

# 4. 成功チャンネル研究から採用する骨格

この研究は、登録者数や再生数だけから因果を断定するものではない。公開動画の観察から、PDへ転用可能な制作原理を抽出する。

## 4.1 研究対象と採用範囲

| 研究対象 | 採用する骨格 | 採用しない表皮 |
|---|---|---|
| MagnatesMedia | 顔出しなし、資料・写真・実写・2.5Dのモジュール構造 | 固有フォント、配色、トランジション |
| Vox | 情報を一つずつ構築する視線設計 | 固有ブランドグラフィック |
| Search Party | 調査素材を地図・関係・時系列へ変換 | 固有レイアウト |
| Coffeezilla | 再利用可能な3Dブランド空間 | サイバーパンク世界の複製 |
| Wendover | 全カットを豪華にせず要所へ予算集中 | 固有図解スタイル |
| fern / neo | 要所の空間再現と立体カメラ | 全編3D、固有モデル |
| VAIENCE | 重い音、照明、環境、静けさ | 科学番組の壮大さの過剰移植 |
| ヒューマンバグ大学 | 危機、利害、逆転、章末の引き | 漫画外見、過剰な煽り |
| バベル裁判所 | 法律を具体的損得へ翻訳 | 漫画形式そのもの |
| フェルミ漫画大学 | 背景・構図・役割の再利用 | キャラクター形式 |
| マリマリマリー | 同一世界の中で内容を変える量産構造 | キャラクター、会話フォーマット |

## 4.2 一チャンネルを丸ごとコピーしない理由

一つのチャンネルは、特定のチーム規模、投稿頻度、出演者、収益構造、視聴者期待の上に成立している。

PDが真似るべきなのは、各チャンネルの**問題解決機能**である。

- MagnatesMediaから制作骨格
- VoxとSearch Partyから情報設計
- Coffeezillaから再利用空間の経済性
- Wendoverから予算配分
- fernから看板カット
- VAIENCEから音と空気
- 日本の物語系から利害と再利用

## 4.3 ベンチマークを実装へ変換する条件

チャンネル名だけをClaude Codeへ渡してはいけない。

各参照ショットを次の単位で記録する。

```json
{
  "channel": "reference-channel",
  "video_url": "https://example.invalid/watch?v=...",
  "timestamp_start": "00:01:24.200",
  "timestamp_end": "00:01:31.800",
  "narrative_function": "compare",
  "visual_question": "Which amount is disproportionate?",
  "visual_verb": "compare",
  "start_state": "two amounts are unknown",
  "end_state": "the imbalance is obvious",
  "layers": ["licensed footage", "numeric labels", "comparison axis"],
  "camera": {"movement": "slow push", "scale_start": 1.0, "scale_end": 1.06},
  "text_events": [{"time_sec": 1.2, "event": "left value appears"}],
  "audio_events": [{"time_sec": 2.1, "event": "impact"}],
  "lesson": "build the comparison sequentially",
  "copy_boundary": "do not reproduce colors, font, timing, or layout"
}
```

P02では最低3チャンネル×3動画×5ショットを記録する。観察対象を増やすより、同じ機能を複数チャンネルで比較する方を優先する。

---

# 5. PD Visual Grammar

## 5.1 映像上の動詞

見た目ではなく、視聴者の理解に起こす変化を分類する。

| Visual verb | 視聴者の変化 | PD用途 | 正規部品 |
| --- | --- | --- | --- |
| Reveal | 知らなかった事実を知る | 判決文、証拠、押収品 | EvidenceReveal |
| Compare | 差、不均衡、比率を理解する | 財産価値と罰金、判決前後 | PenaltyVsProperty |
| Trace | 順序、経路、現在地を理解する | 事件から最高裁まで | CaseJourney |
| Connect | 人物・組織・証拠の関係を理解する | 当事者、政府、資金 | CaseNetwork |
| Isolate | 核心へ注意を集中する | 判決文の一文、例外 | QuoteUnderExamination |
| Reconstruct | 空間・出来事の位置関係を理解する | 道路、車、部屋 | IncidentReconstruction |
| Escalate | 利害・危険・影響の増大を感じる | 損失、刑罰、対象者 | ImpactExpansion |
| Overturn | 判断・ルールの逆転を理解する | 下級審と最高裁 | VerdictReversal |
| Classify | 要素をカテゴリへ整理する | 要件、証拠種別 | RuleBoundary |
| Constrain | 権限や例外の境界を理解する | 政府権限、例外 | RuleBoundary |
| Expand | 一事件から社会的影響へ広げる | 他州、他事件、市民 | ImpactExpansion |
| Resolve | 冒頭の問いへ条件付きで答える | 判決、残る問題 | CaseResolution |

## 5.2 一シーン一主要動詞

主要動詞は一つだけにする。補助動詞は一つまで許容する。

悪い設計:

```text
Reveal + Compare + Trace + Connectを同時に実行
```

良い設計:

```text
主: Compare
補助: Isolate
```

## 5.3 シーン契約

すべてのシーンは最低限次を持つ。

```json
{
  "schema_version": "2.0.0",
  "episode_id": "PD-2026-009-timbs",
  "scene_id": "SCN-001",
  "start_sec": 0.0,
  "duration_sec": 7.0,
  "narration": "",
  "visual_question": "What imbalance must the viewer understand?",
  "visual_verb": "compare",
  "start_state": "The two values have not been compared.",
  "end_state": "The property value is visibly disproportionate to the maximum fine.",
  "eye_target": "center comparison axis",
  "visual_strategy": "motion_template",
  "source_type": "verified_evidence",
  "truth_status": "verified",
  "license_status": "review_required",
  "review_status": "pending",
  "provenance": [],
  "selected_assets": [],
  "sync_cues": []
}
```

## 5.4 動きの目的タグ

全モーションは最低一つの目的を持つ。

- `attention`
- `reveal`
- `comparison`
- `causality`
- `timeline`
- `space`
- `tension`
- `transition`
- `emotion`
- `brand`

目的タグがない動きは削除候補とする。

## 5.5 映像の主役

各フレームで視聴者が見る対象は原則一つ。

複数情報を出す場合も、次の順で視線を移す。

```text
全体
→ 対象A
→ 対象B
→ AとBの関係
→ 結論
```

---

# 6. Truth、Source、License、Disclosureの分離

これらを一つの「素材種別」で扱ってはいけない。

## 6.1 Source type

| 値 | 意味 | 例 |
|---|---|---|
| `verified_evidence` | 事件固有の実在資料 | 判決文、記録、実際の写真 |
| `documentary_source_media` | 報道・公的アーカイブ等の事実映像 | 許諾済みニュース映像 |
| `licensed_broll` | 一般的な正規B-roll | 裁判所外観、道路 |
| `illustrative_animation` | 制度・因果を説明する図解 | 裁判経路、比較 |
| `three_d_reconstruction` | 3Dによる空間再構成 | Evidence Room、簡易現場 |
| `ai_generated_broll` | 実在事件を直接再現しない生成B-roll | 雨の汎用裁判所 |
| `ai_reenactment` | 実在出来事を生成で再現 | 人物後ろ姿による再現 |

## 6.2 Truth status

- `verified`
- `corroborated`
- `reported`
- `illustrative`
- `reconstructed`
- `unknown`

## 6.3 License decision

- `approved`
- `review_required`
- `rejected`
- `expired`

初期値は必ず `review_required`。`approved` は証拠記録を伴う人間判断だけで設定する。

## 6.4 Attribution

二値ではなく三状態にする。

```json
{
  "attribution_required": null
}
```

- `true`: 必要
- `false`: 不要と確認済み
- `null`: 未確認

## 6.5 AI開示

`ai_generated_broll` と `ai_reenactment` はリスクが異なる。

- 汎用的な環境B-rollでも、実在場所や出来事だと誤認しうる場合は開示判断を行う。
- 実在事件の再現は原則画面内ラベルまたはプラットフォーム開示を検討する。
- 実在人物の発言、口元、行為を捏造しない。
- 判決文、新聞、証拠、警察文書、読める標識を生成しない。

## 6.6 Hard blockers

次のいずれかがあれば本番レンダー可否をfalseにする。

1. ライセンス未確認素材
2. 出典欠損の事件固有資料
3. AI生成物のhuman review未完了
4. 引用文と原典の不一致
5. 再現映像の開示判断未完了
6. 欠損素材
7. 破損レンダー
8. baseline上書きの疑い

---

# 7. Claude Code Control Plane

## 7.1 短いCLAUDE.md

`CLAUDE.md`には、全技術詳細を置かない。使命、優先順位、Phase制御、安全、コア5部品、truth分類だけを置く。

## 7.2 Path-scoped Rules

Rulesは対象パスの作業時だけ適用する。

- Remotionコード: motion品質、duration、safe area、seed、テキスト
- media/provenance: truth、license、AI開示
- Python adapters: isolated env、CLI、logging、resume
- Blender: Evidence Room、座標出力、固定カメラ
- docs/state: 状態遷移、事実と仮定の分離

## 7.3 Manual Skills

Phase Skillは `disable-model-invocation: true` とし、ユーザーが明示したときだけ実行する。

Claude Codeは「役に立ちそうだから」という理由で次PhaseのSkillを自動起動しない。

## 7.4 Phase State Machine

状態:

- `not_started`
- `in_progress`
- `blocked`
- `candidate_complete`

`candidate_complete` は完了候補であり、自動的に次Phaseへ進まない。

ユーザーが `/pd-phase-advance Pxx` を明示し、`--human-approved` を伴う状態更新だけがPhaseを進める。

## 7.5 PermissionsとHooks

文章上の禁止は補助であり、強制ではない。

- Permissionsのdeny: 既知の破壊操作、保護パス
- Permissionsのask: install、download、Git公開操作
- PreToolUse Hook: command/pathを実行直前に検査
- Phase Gate: 現在Phaseの不一致を停止

## 7.6 Read-only Subagents

専門レビューは別コンテキストへ分ける。

- visual director
- motion reviewer
- asset librarian
- truth/license auditor
- QC reviewer

Subagentは既定で調査・提案に使い、無制限な実装権限を与えない。

---

# 8. Safety Enforcement Specification

## 8.1 Protected paths

- repository `.git`
- `H:\pd-media\assets`
- baseline render root
- secrets、`.env`、SSH keys

## 8.2 Approved external output roots

- `H:\pd-media\generated`
- `H:\pd-media\previews`
- `H:\pd-media\indexes`
- `H:\pd-media\thumbnails`
- `H:\pd-media\temp`

実機監査でパスが異なる場合は、P00でpolicyを更新し、理由をDecision Logへ残す。

## 8.3 Deny対象

- `git reset --hard`
- `git clean -fd`相当
- force push
- protected pathへのWrite/Edit
- root/home/driveを対象とする再帰強制削除
- disk format系
- baselineへの上書き

## 8.4 Ask対象

- `git push/merge/rebase/commit`
- package install/upgrade/remove
- `winget/choco/scoop`
- `curl/wget/hf download`
- 管理者権限
- `ffmpeg -y`
- 外部公開、upload、paid API

## 8.5 5GBルール

5GB超のダウンロード前に次を提示する。

1. 対象名
2. version/checkpoint
3. 予想容量
4. 保存先
5. ライセンス
6. 導入Phase
7. 必要性
8. 代替案
9. rollback
10. 空き容量

## 8.6 Hookが失敗した場合

Hookが解析不能、policy欠損、Python不在の場合、危険操作を許可側へ倒さない。

- stderrへ記録
- 操作を停止またはask
- policy修復をP00/Pcurrentの範囲で行う

---

# 9. 正規ディレクトリ構成

```text
prime-documentary/
├─ CLAUDE.md
├─ .claude/
│  ├─ settings.json
│  ├─ pd-safety-policy.json
│  ├─ hooks/
│  │  └─ pd_safety_gate.py
│  ├─ rules/
│  │  ├─ remotion-motion.md
│  │  ├─ media-truth-license.md
│  │  ├─ python-adapters.md
│  │  ├─ blender-evidence-room.md
│  │  └─ docs-state.md
│  ├─ skills/
│  │  ├─ pd-phase-00-audit/
│  │  ├─ ...
│  │  ├─ pd-phase-12-decision-rollout/
│  │  ├─ pd-phase-advance/
│  │  ├─ pd-qc/
│  │  └─ pd-license-audit/
│  └─ agents/
├─ config/pd-visual-system/
├─ schemas/
├─ templates/pd-visual-system/
├─ scripts/pd-visual-system/
├─ docs/pd-visual-system/
├─ tests/pd-visual-system/
├─ outputs/pd-visual-system/
└─ data/
```

外部ツールは既存Node/Remotion環境へ混ぜない。

```text
D:\PD_AI_Tools\
├─ scenedetect\
├─ openclip\
├─ whisperx\
├─ sam2\
├─ depth-anything-v2-small\
├─ comfyui\
└─ optional-tools\

D:\PD_AI_Models\
├─ embeddings\
├─ alignment\
├─ segmentation\
├─ depth\
└─ video\
```

実際のドライブはP00で空き容量と既存構成を確認して確定する。

---

# 10. Canonical Component Registry

初期実装は**コア5部品だけ**で固定する。

- `EvidenceReveal`
- `PenaltyVsProperty`
- `CaseJourney`
- `QuoteUnderExamination`
- `VerdictReversal`

これ以外はgap reportで必要性が証明されるまで実装しない。

## 10.1 `EvidenceReveal`

**主要動詞:** Reveal  
**目的:** 実在資料、証拠、写真、記録の全体から核心へ段階的に視線を移す。

### Modes

- `document`
- `photograph`
- `record`
- `exhibit`

### Required props

- `asset`
- `focusRegions`
- `sourceLabel`
- `revealSequence`

### Mandatory tests

- 5/8/12秒
- 長文引用
- focusRegion画面外
- 素材欠損
- 出典ラベル

### 共通実装条件

- 固有事件名をハードコードしない
- 5秒、8秒、12秒で破綻しない
- `durationInFrames`へ追従する
- 30fpsを標準とし、時間はframe換算を一箇所へ集約する
- `spring`と`interpolate`は意図をコメントする
- ランダム値はseed固定できる
- 画面外テキストを検査する
- source labelを省略しない
- reduced-motion previewを用意する
- 入力不正時はsilent failureせず明示的fallbackを返す

## 10.2 `PenaltyVsProperty`

**主要動詞:** Compare  
**目的:** 金額、罰金、財産、人数、判決前後などを共通軸で段階比較する。

### Modes

- `currency`
- `generic`
- `before_after`
- `ratio`

### Required props

- `left`
- `right`
- `comparisonAxis`
- `sourceLabel`

### Mandatory tests

- 単位一致
- 負数/ゼロ
- 大数表記
- 比率精度
- 左右長文

### 共通実装条件

- 固有事件名をハードコードしない
- 5秒、8秒、12秒で破綻しない
- `durationInFrames`へ追従する
- 30fpsを標準とし、時間はframe換算を一箇所へ集約する
- `spring`と`interpolate`は意図をコメントする
- ランダム値はseed固定できる
- 画面外テキストを検査する
- source labelを省略しない
- reduced-motion previewを用意する
- 入力不正時はsilent failureせず明示的fallbackを返す

## 10.3 `CaseJourney`

**主要動詞:** Trace  
**目的:** 事件、裁判所、日付、場所の経路を現在地を一つに保って示す。

### Modes

- `timeline`
- `court_hierarchy`
- `map_route`
- `procedural_path`

### Required props

- `nodes`
- `activeNode`
- `direction`

### Mandatory tests

- 3/5/8ノード
- 同日イベント
- 長い裁判所名
- 欠損日付
- VFR無関係

### 共通実装条件

- 固有事件名をハードコードしない
- 5秒、8秒、12秒で破綻しない
- `durationInFrames`へ追従する
- 30fpsを標準とし、時間はframe換算を一箇所へ集約する
- `spring`と`interpolate`は意図をコメントする
- ランダム値はseed固定できる
- 画面外テキストを検査する
- source labelを省略しない
- reduced-motion previewを用意する
- 入力不正時はsilent failureせず明示的fallbackを返す

## 10.4 `QuoteUnderExamination`

**主要動詞:** Isolate  
**目的:** 長い資料から正確な一文または語句を抽出し、文脈と出典を保って読ませる。

### Modes

- `holding`
- `dissent`
- `statute`
- `testimony`

### Required props

- `quote`
- `source`
- `emphasisRanges`

### Mandatory tests

- 引用一致
- 省略記号
- 強調範囲
- 長文wrap
- 引用改変検知

### 共通実装条件

- 固有事件名をハードコードしない
- 5秒、8秒、12秒で破綻しない
- `durationInFrames`へ追従する
- 30fpsを標準とし、時間はframe換算を一箇所へ集約する
- `spring`と`interpolate`は意図をコメントする
- ランダム値はseed固定できる
- 画面外テキストを検査する
- source labelを省略しない
- reduced-motion previewを用意する
- 入力不正時はsilent failureせず明示的fallbackを返す

## 10.5 `VerdictReversal`

**主要動詞:** Overturn  
**目的:** 旧判断と新判断の差、変わった点、変わらない点を順に示す。

### Modes

- `court_reversal`
- `rule_change`
- `burden_shift`

### Required props

- `beforeDecision`
- `afterDecision`
- `changed`
- `unchanged`

### Mandatory tests

- 完全逆転
- 一部変更
- 差戻し
- 長文理由
- 色だけに依存しない

### 共通実装条件

- 固有事件名をハードコードしない
- 5秒、8秒、12秒で破綻しない
- `durationInFrames`へ追従する
- 30fpsを標準とし、時間はframe換算を一箇所へ集約する
- `spring`と`interpolate`は意図をコメントする
- ランダム値はseed固定できる
- 画面外テキストを検査する
- source labelを省略しない
- reduced-motion previewを用意する
- 入力不正時はsilent failureせず明示的fallbackを返す

## 10.6 Expansion registry

拡張部品は次の通り。statusは `deferred_until_need_is_proven` である。

| 部品 | 動詞 | 目的 | 初期状態 |
| --- | --- | --- | --- |
| CaseNetwork | Connect | 人物、組織、証拠、資金の関係を一つずつ構築する。 | deferred_until_need_is_proven |
| RuleBoundary | Constrain/Classify | 原則、許容範囲、禁止範囲、例外を整理する。 | deferred_until_need_is_proven |
| ImpactExpansion | Expand | 個別事件から他州、他事件、一般市民への影響を根拠付きで広げる。 | deferred_until_need_is_proven |
| CaseResolution | Resolve | 冒頭の問いへ答え、条件と残る問題を返す。 | deferred_until_need_is_proven |
| ParallaxStill | Reconstruct/Isolate | 静止画へ弱い奥行きと視線誘導を加える。 | deferred_until_need_is_proven |
| InvestigativeMapRoute | Trace | 場所、移動、距離、管轄を正確な地図で示す。 | deferred_until_need_is_proven |
| ChapterTransition | Resolve/Reveal | 前章を閉じ、次の問いを2〜4秒で提示する。 | deferred_until_need_is_proven |
| IncidentReconstruction | Reconstruct | 既知事実と推測を分けた簡略空間再現を行う。 | deferred_until_need_is_proven |

## 10.7 Alias policy

旧名や重複名は新しいコンポーネントを作らず、正規名へ解決する。

| 旧名 | 正規名 | mode |
| --- | --- | --- |
| DocumentReveal | EvidenceReveal | document |
| LegalTimeline | CaseJourney | timeline |
| CourtHierarchy | CaseJourney | court_hierarchy |
| MapRoute | InvestigativeMapRoute | None |
| ComparisonSplit | PenaltyVsProperty | generic |
| EvidenceBoard | CaseNetwork | evidence_board |
| LegalClassification | RuleBoundary | classification |
| DataCounter | MetricCounterPrimitive | None |
| CaseFileStack | EvidenceReveal | file_stack |
| RedactionReveal | EvidenceReveal | redaction |
| SurveillanceFrame | EvidenceReveal | surveillance_record |
| StakesEscalation | ImpactExpansion | stakes |
| Dramatization | IncidentReconstruction | dramatization |

## 10.8 Internal primitives

次のものは独立した映像テンプレートではなく、コア部品内部で共有するprimitiveである。

- `MetricCounterPrimitive`
- `SourceLabel`
- `FocusRegion`
- `ConnectorLine`
- `WordCue`
- `SafeTextBlock`
- `SeededNoise`
- `DisclosureBadge`

primitiveを「新しいコンポーネント数」として数えない。

## 10.9 新部品のGap Report

新部品を提案する場合は、次を満たす。

```markdown
# Component Gap Report

- scene_id:
- visual_question:
- required_visual_verb:
- why_core_five_fail:
- why_expansion_modes_fail:
- minimum_new_behavior:
- reuse_cases_expected:
- tests:
- maintenance_cost:
- alternative_without_new_component:
- decision: propose | reject | merge_into_existing
```

---

# 11. Remotion Motion Engineering Standard

## 11.1 原則

- animationはdecorative layerではなくstate transitionとして設計する
- compositionはデータ駆動にする
- one-off JSXをscene本体へ積み上げない
- props型とschemaを一致させる
- missing assetは明示的placeholderとQC warningを返す
- CSSで読める文字をBlenderやAIへ焼き込まない

## 11.2 Time contract

```ts
export type TimingContract = {
  fps: number;
  durationInFrames: number;
  introEnd: number;
  buildEnd: number;
  conclusionStart: number;
};
```

割合で定義し、固定frame番号を乱用しない。

```ts
const introEnd = Math.round(durationInFrames * 0.18);
const buildEnd = Math.round(durationInFrames * 0.72);
const conclusionStart = Math.round(durationInFrames * 0.78);
```

## 11.3 Text safety

- title safe areaを守る
- 英語の長い固有名詞を想定する
- 1行文字数だけで切らず実測bboxを使う
- 最小font sizeを定義する
- quoteは原文を変更せず、表示上の改行だけを分ける
- ellipsisを入れる場合は原典の省略であることを示す

## 11.4 Color semantics

色は装飾ではなく意味へ固定する。

例:

- evidence: neutral / warm paper
- government position: one assigned hue
- claimant position: another assigned hue
- changed / overturned: high-contrast accent
- unknown / disputed: desaturated or patterned

色だけに依存せず、label、shape、positionも併用する。

## 11.5 Camera motion limits

通常の資料・2.5Dでは、動きを抑える。

- scale: 原則1.00→1.04〜1.10
- horizontal displacement: 顔や輪郭の穴が出ない範囲
- rotation: 原則0〜1.5度
- camera shake: 事件内容の根拠がない限り不使用
- rapid zoom: フックの一回に限定

## 11.6 Seeded randomness

すべてのparticle/noise/layout jitterはseedを受け取る。

同一input、同一seed、同一versionで同じframeを再現できること。

## 11.7 Demo compositions

コア5部品は、実事件素材に依存しないfixtureでdemo compositionを持つ。

- 5秒
- 8秒
- 12秒
- long copy
- missing source label
- overflow
- reduced motion

---

# 12. データ契約の要点

Schemasが正本であり、本章の例は説明用である。

## 12.1 Asset recordとVFR

平均fpsだけで時間を管理しない。

```json
{
  "avg_frame_rate": "30000/1001",
  "r_frame_rate": "30/1",
  "time_base": "1/90000",
  "start_pts": 1117800,
  "end_pts": 1564200,
  "start_sec": 12.42,
  "end_sec": 17.38,
  "sample_frames": [
    {"position": 0.25, "path": "thumb_25.jpg"},
    {"position": 0.50, "path": "thumb_50.jpg"},
    {"position": 0.75, "path": "thumb_75.jpg"}
  ]
}
```

## 12.2 Generation request

```json
{
  "schema_version": "2.0.0",
  "request_id": "GEN-001",
  "scene_id": "SCN-010",
  "purpose": "atmospheric_broll",
  "source_type": "ai_generated_broll",
  "model_family": "wan2.2",
  "checkpoint": "TO_BE_REVIEWED",
  "workflow_version": "1.0.0",
  "prompt": "",
  "negative_intent": [],
  "seed": 42,
  "license_decision": "review_required",
  "human_review_required": true,
  "review_status": "pending"
}
```

## 12.3 Review record

statusは単一値である。

- `approved`
- `rejected`
- `revise`

文字列に選択肢を並べない。

## 12.4 Provenance

各採用素材に最低限次を持つ。

- source URLまたは原本識別子
- license record ID
- file hash
-取得日時
- modified/transcoded history
- source type
- truth status
- attribution decision
- reviewer

---

# 13. Asset Intelligence Pipeline

## 13.1 目的

85,000点の素材を保有していても、必要な3秒を見つけられなければ制作上は存在しない。

最初の投資はAI動画生成ではなく、既存資産の発見可能性を上げることに置く。

## 13.2 P03は100〜500素材だけ

全件処理を禁止する理由:

- ffprobe失敗率が未知
- VFR、破損、codecの分布が未知
- thumbnail容量が未知
- PySceneDetect thresholdが未知
- DB schemaが未検証
- 途中再開機構が未検証

小規模pilotで処理時間、失敗率、DBサイズ、検索価値を測る。

## 13.3 Scene detection

- PySceneDetectはversionを固定
- detectorとthresholdをmanifestへ保存
- cut pointをPTS/time_baseと秒で保持
- original sourceはread-only
- scene splitは論理区間として記録し、元動画を必ずしも物理分割しない

## 13.4 Three-frame representation

一カット一枚の中央サムネイルでは時間変化を失う。

各sceneから25%、50%、75%を取得する。

検索埋め込みは次の候補を比較する。

1. 3フレームを個別保存しmax similarity
2. 3埋め込みを平均
3. 各フレームとmetadataのweighted score

## 13.5 SQLite minimum fields

- asset_id
- absolute_path
- relative_path
- file_hash
- media_type
- width/height
- duration
- avg_frame_rate/r_frame_rate
- time_base
- start/end PTS
- audio channels
- file size
- scene index
- sample frame paths
- OCR text optional
- filename/folder tags
- source/license fields
- quality score
- probe error
- processed version
- last indexed timestamp

## 13.6 Resume and idempotency

同一file hash、same pipeline version、same configなら再処理しない。

失敗はasset単位で記録し、全体を止めない。

## 13.7 Semantic search

OpenCLIP等のコードライセンスだけでなく、**checkpoint単位**で記録する。

検索scoreは唯一の採用根拠にしない。

```text
semantic score
+ filename/folder score
+ duration suitability
+ resolution quality
+ license readiness
+ prior usage penalty
= candidate ranking
```

## 13.8 Human evaluation

20 queryでTop-10を評価する。

- relevant
- partially relevant
- irrelevant
- unusable-license
- duplicate
- wrong-era
- wrong-location

検索品質が低い場合、全件展開せずmetadata、sampling、model、queryを修正する。

---

# 14. Audio Alignment Pipeline

## 14.1 役割

WhisperXは台本を作るものではない。既存の英語ナレーションと正本台本を時間へ整列する補助である。

## 14.2 Code licenseとmodel licenseを分ける

WhisperX本体、Whisper checkpoint、alignment model、diarization modelは別々にライセンス記録する。

## 14.3 Numeric token review

法律動画では次を自動信頼しない。

- 金額
- 年号
- 条文番号
- 事件番号
- パーセント
- 人名・地名

`numeric_tokens_for_review`へ抽出し、人間確認する。

## 14.4 Sync cue types

- `word_appear`
- `evidence_focus`
- `number_reveal`
- `line_draw`
- `verdict_stamp`
- `sfx_impact`
- `scene_turn`
- `silence_hold`

## 14.5 Timing tolerance

初期目標:

- critical word visual onset: ±120ms以内を目安
- SFX impact: ±80ms以内を目安
- long quote highlight: word onsetより少し先行させない

目標値は実機previewで調整し、絶対規則にしない。

## 14.6 Script diff

認識結果と台本の差を出すが、台本を自動上書きしない。

- missing words
- extra words
- substitutions
- punctuation differences
- numeric mismatches

---

# 15. 2.5D Pipeline

## 15.1 目的

静止画を派手に歪ませることではない。主対象を保ちつつ、前景・中景・背景の相対運動で奥行きと視線誘導を加える。

## 15.2 SAM2は対象を決めない

SAM2へ「主役を自動判断させる」前提を置かない。

入力には次のいずれかを必須とする。

- human-selected bounding box
- human-selected points
- VLM/Grounding modelの候補boxを人間確認

```json
{
  "target_label": "judge",
  "prompt_type": "box",
  "box_xyxy": [310, 120, 880, 1010],
  "reviewed_by": "human"
}
```

## 15.3 Depth model

初期候補はDepth Anything V2 Smallだけ。モデル、重み、データ由来、商用条件は導入時に再監査する。

Base/Large/Giantを初期導入しない。

## 15.4 Background hole mitigation

主対象を動かすと背景穴が生じる。

初期版は高度な生成inpaintを必須にせず、次で抑える。

1. 背景を105〜110%拡大
2. 横移動を小さくする
3. 奥行き方向のscale差を中心にする
4. subject edgeをfeather
5. movement maskをQC
6. 穴が見える場合は採用しない

inpaintを使う場合は、顔、文字、証拠、建物の事実部分を生成補完しない。

## 15.5 Review contact sheet

- original
- mask overlay
- depth map
- background plate
- frame at 0/25/50/75/100%
- edge zoom

## 15.6 Rejection criteria

- 顔輪郭の破綻
- 手や文字の生成補完
- 背景穴
- 建物直線の曲がり
- 主対象の切断
- 過剰な奥行き
- 画面酔い

---

# 16. PD Evidence Room

## 16.1 経済構造

Blenderを毎話新しい3D映像を作る道具として使わない。

一度作った撮影セットを、資料だけ差し替えて何度も使う。

## 16.2 Minimum set

- room shell
- central evidence desk
- evidence board
- map wall
- court hierarchy monitor
- document monitor
- archive shelves
- controllable practical lights

## 16.3 P09の制限

初期版は固定または正面モニターの限定カメラ1カット。

動くカメラでRemotion資料をモニターへ貼る場合、CSSの固定座標ではずれる。

次のどちらかを選ぶ。

### A. Fixed screen camera

- monitor正面
- camera motionなしまたは極小
- Remotion overlayを固定perspectiveで合成

### B. Screen-space corner export

Blenderからフレームごとの四隅座標を出力する。

```json
{
  "frame": 120,
  "screen_corners": [
    [412.5, 190.4],
    [1150.2, 210.1],
    [1128.6, 720.5],
    [430.7, 695.8]
  ]
}
```

Remotion側は四点変換を使う。P09初期版ではAを優先する。

## 16.4 Camera catalog v1

- `room_entry_static`
- `desk_push_in`
- `evidence_board_pan`

3種類まで。8種類や全編セットを先に作らない。

## 16.5 Render separation

Blender:

- room
- light
- camera
- shadows
- optional mattes

Remotion:

- readable documents
- case-specific text
- source labels
- disclosure labels
- animated lines

## 16.6 Reusability test

同じ`.blend`を別episode fixtureへ差し替え、モデル変更なしでpreviewを生成できること。

---

# 17. ComfyUI and AI B-roll

## 17.1 導入条件

P10まで導入しない。

次の証拠が必要。

1. 既存素材検索で候補が見つからない
2. 2.5Dやmotion templateでは目的を満たさない
3. 3〜5秒のB-rollが必要
4. source type、truth status、開示条件が決まっている
5. model/checkpoint/custom nodeのライセンスが記録済み
6. 5GB超ダウンロードが明示承認済み

## 17.2 First workflow

- 1 model
- 1 workflow
- 1 aspect ratio
- 1 short duration
- seed fixed
- low-resolution preview first
- output manifest mandatory

## 17.3 Recommended use

- rain
- clouds
- subtle lighting
- generic courthouse atmosphere
- non-identifiable rear-view person
- archive room atmosphere
- paper edge motion without readable text
- generic street reflections

## 17.4 Prohibited use

- real-person dialogue
- lip sync attributed to a real person
- readable ruling/newspaper/police report
- actual evidence fabrication
- official badge/seal fabrication
- identifiable real crime reenactment without disclosure
- full-episode generation

## 17.5 License stack

次を別々に監査する。

- repository code
- model architecture code
- checkpoint weights
- tokenizer/text encoder
- VAE
- custom nodes
- auxiliary models
- generated output terms

「Wan2.2がApache 2.0だからワークフロー全体が自動的にapproved」とは扱わない。

## 17.6 Review

- face
- hands
- text
- architecture
- temporal consistency
- duplicated objects
- camera teleportation
- era mismatch
- narration mismatch
- disclosure need

---

# 18. FFmpeg, QC, and Finishing

## 18.1 ffprobe record

- codec
- profile
- width/height
- pixel format
- color metadata
- duration
- frame rates
- time base
- audio codec
- sample rate
- channels
- file integrity

## 18.2 Automated checks

- black frames
- silence
- frozen frames
- missing frames
- audio peak
- loudness
- duration mismatch
- missing source label
- low-resolution upscaling
- duplicated asset overuse
- template overuse

## 18.3 Loudness

YouTube向け候補値を機械的に確定しない。既存PDの制作ルール、DaVinci preset、実測結果を確認してquality configへ固定する。

## 18.4 ffmpeg overwrite

`-y`はHookのask対象。新しいversioned output pathを原則とする。

## 18.5 DaVinci

初期版は任意。

- 公式Python/Lua APIだけ
- edition差を実機確認
- GUI座標操作なし
- APIで安定しない処理は人間工程として残す

## 18.6 Release gate

`release_ready=true`には次が必要。

- hard blocker zero
- license decision complete
- AI human review complete
- source labels complete
- quote verification complete
- no missing assets
- no corrupted stream
- output path versioned
- baseline untouched

---

# 19. Incremental Experiment Design

A/B/Cを一度に比較すると、何が効いたか分からない。

次の増分設計へ固定する。

| Variant | 追加する要素 | 検証する因果 |
|---|---|---|
| A | 現在版 | baseline |
| B1 | 素材検索＋コア5部品 | 情報設計と素材発見の効果 |
| B2 | B1＋WhisperX同期 | 音声同期の効果 |
| B3 | B2＋2.5Dを1カット | 奥行きの追加価値 |
| C1 | B3＋Evidence Roomを1カット | 再利用3D空間の価値 |
| C2 | C1＋AI B-rollを1カット | 生成B-rollの追加価値 |
| C3 | C2＋音響・カラー | finishingの追加価値 |

## 19.1 固定条件

- 同じ60〜90秒
- 同じナレーション
- 同じscript version
- 原則同じBGMベース
- 追加要素以外を不用意に変えない

## 19.2 記録するコスト

- human minutes
- Claude Code iterations
- render time
- GPU time
- download size
- disk footprint
- new files
- reusable files
- failures
- review minutes

## 19.3 記録する価値

- comprehension
- paper-theater reduction
- eye guidance
- trust clarity
- audio sync
- premium feel
- reuse potential
- artifact risk

## 19.4 採否基準

高品質でも、一分あたりの追加工数が大きく、再利用率が低ければ標準化しない。

```text
standardize when:
quality gain is material
AND recurring cost is acceptable
AND truth/license risk is controlled
AND reuse is demonstrated
```

---

# 20. Phase-Gated Roadmap

PhaseはP00からP12まで。自動で進めない。

## 20.1 P00 環境・リポジトリ監査

**Objective:** PC、Git、Remotion、FFmpeg、対象エピソード、素材ルートを読み取り中心で監査し、安全な実装境界を確定する。

### Canonical phase contract

```markdown
# P00 環境・リポジトリ監査

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

PC、Git、Remotion、FFmpeg、対象エピソード、素材ルートを読み取り中心で監査し、安全な実装境界を確定する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P00`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- PHASE_STATE.json が P00 を指している
- 既存ファイルを変更せずに調査を開始できる

## Allowed scope
- 読み取り
- バージョン確認
- Git status/diff/log
- 文書テンプレートの新規作成

## Forbidden in this phase
- インストール
- 依存関係更新
- 大容量ダウンロード
- 既存レンダー上書き
- Git履歴変更

## Required deliverables
- ENVIRONMENT_AUDIT.md
- REPOSITORY_AUDIT.md
- IMPLEMENTATION_STATUS.md 更新
- P01_CHANGE_PLAN.md

## Acceptance criteria
- 主要パスとバージョンが記録済み
- 未コミット変更が保護されている
- 対象60〜90秒を選ぶための候補が示されている


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.2 P01 Baseline保存・紙芝居診断

**Objective:** 対象エピソードから比較価値の高い連続60〜90秒を選び、現在版を保存して紙芝居要因を測定する。

### Canonical phase contract

```markdown
# P01 Baseline保存・紙芝居診断

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

対象エピソードから比較価値の高い連続60〜90秒を選び、現在版を保存して紙芝居要因を測定する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P01`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P00 が candidate_complete か completed
- レンダー手順が判明している

## Allowed scope
- 既存プロジェクトの非破壊レンダー
- コピー出力
- ffprobe解析
- ショット診断

## Forbidden in this phase
- 新ツール導入
- 既存ラフカット上書き
- 全編改修

## Required deliverables
- baseline動画または再現可能なレンダーmanifest
- BASELINE_DIAGNOSIS.md
- baseline_shots.json

## Acceptance criteria
- 同一ナレーションで後続版と比較できる
- 各ショットにvisual questionとstart/end stateがある
- 紙芝居要因8軸が採点済み


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.3 P02 参照チャンネルのショット分解

**Objective:** 成功チャンネルの外見ではなく、ショット単位の情報設計、タイミング、音、再利用原理を観察記録する。

### Canonical phase contract

```markdown
# P02 参照チャンネルのショット分解

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

成功チャンネルの外見ではなく、ショット単位の情報設計、タイミング、音、再利用原理を観察記録する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P02`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P01 baseline区間が確定
- BENCHMARK_METHOD.mdを読んでいる

## Allowed scope
- 合法的な視聴と手動観察
- 公開情報の引用元記録
- タイムスタンプ記録

## Forbidden in this phase
- 動画素材の無断ダウンロード
- フレームや音源の再配布
- 固有デザインの複製

## Required deliverables
- benchmark_shots.jsonl
- BENCHMARK_FINDINGS.md
- COPY_BOUNDARY.md

## Acceptance criteria
- 最低3チャンネル×3動画×5ショット
- 各記録にvisual verbとlessonがある
- 採用原理とコピー禁止要素が分離されている


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.4 P03 素材インデックス最小実証

**Objective:** 100〜500素材に限定し、ffprobe、PySceneDetect、3点サンプリング、SQLite、再開可能処理を検証する。

### Canonical phase contract

```markdown
# P03 素材インデックス最小実証

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

100〜500素材に限定し、ffprobe、PySceneDetect、3点サンプリング、SQLite、再開可能処理を検証する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P03`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P00監査で保存先と空き容量が確認済み
- PySceneDetect導入計画と固定版が承認済み

## Allowed scope
- 読み取り専用素材走査
- 新規インデックス・サムネイル出力
- 独立venv作成

## Forbidden in this phase
- 素材移動・削除・上書き
- 85,000点全件処理
- 元動画の再エンコード

## Required deliverables
- 試験SQLite DB
- scene thumbnails
- asset_index_report.md
- 再実行可能CLI

## Acceptance criteria
- VFR情報をPTS/time_base込みで保持
- 各動画カットを25/50/75%の3フレームで表現
- 中断再開・差分更新・エラー継続が動作


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.5 P04 意味検索の最小実証

**Objective:** 商用条件を記録した埋め込みモデルで、20クエリの検索品質を人間評価する。

### Canonical phase contract

```markdown
# P04 意味検索の最小実証

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

商用条件を記録した埋め込みモデルで、20クエリの検索品質を人間評価する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P04`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P03の試験DBが利用可能
- チェックポイント単位のライセンス判断がreviewed

## Allowed scope
- 承認済み重みのダウンロード
- ローカル埋め込み生成
- 検索評価

## Forbidden in this phase
- ライセンス不明重みの自動採用
- 検索結果の自動編集採用
- 全素材一括埋め込み

## Required deliverables
- 検索CLI
- embedding manifest
- 20-query evaluation
- MODEL_LICENSE_RECORD.md

## Acceptance criteria
- Top-10 precisionの人間評価を記録
- モデル/重み/取得元/ハッシュ/ライセンスを保存
- 検索失敗例を残す


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.6 P05 Remotionコア5部品

**Objective:** EvidenceReveal、PenaltyVsProperty、CaseJourney、QuoteUnderExamination、VerdictReversalだけを高品質に実装する。

### Canonical phase contract

```markdown
# P05 Remotionコア5部品

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

EvidenceReveal、PenaltyVsProperty、CaseJourney、QuoteUnderExamination、VerdictReversalだけを高品質に実装する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P05`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P01のbaseline診断がある
- 既存Remotion構造とVIDEO_RULESを理解している

## Allowed scope
- 既存Remotionへの最小差分追加
- 新規デモcomposition
- テスト・docs

## Forbidden in this phase
- 追加コンポーネントの先回り実装
- 既存APIの全面改修
- 固有事件名のハードコード

## Required deliverables
- コア5部品
- デモcomposition
- 型・tests
- component_registry更新

## Acceptance criteria
- 5/8/12秒で破綻しない
- 長い英語文・欠損入力・30fpsでテスト
- 各部品がstart/end stateを変える


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.7 P06 B1コア改善版

**Objective:** 新ツールを増やさず、既存素材検索とコア5部品だけでbaseline区間を改善する。

### Canonical phase contract

```markdown
# P06 B1コア改善版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

新ツールを増やさず、既存素材検索とコア5部品だけでbaseline区間を改善する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P06`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P05コア5部品がcandidate_complete
- P03/P04が使える場合は検索結果を利用できる

## Allowed scope
- 既存素材
- コア5部品
- 既存SFX/BGM
- 非破壊レンダー

## Forbidden in this phase
- WhisperX
- SAM2/Depth
- Blender
- AI動画

## Required deliverables
- B1 preview
- B1 scene_plan.json
- B1 comparison notes

## Acceptance criteria
- Aと同一ナレーション
- 各シーン一主要動詞
- 理解度と紙芝居感の改善を人間評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.8 P07 WhisperX同期・B2版

**Objective:** 英語ナレーションを台本へ整列し、重要語・資料・SFXを単語単位で同期する。

### Canonical phase contract

```markdown
# P07 WhisperX同期・B2版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

英語ナレーションを台本へ整列し、重要語・資料・SFXを単語単位で同期する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P07`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- B1が比較可能
- WhisperXと整列モデルのライセンスが記録済み

## Allowed scope
- 独立venv
- 英語音声整列
- cue生成
- Remotion同期

## Forbidden in this phase
- 認識結果による台本上書き
- 数字・年号・事件番号の無検査採用

## Required deliverables
- narration_alignment.json
- numeric_token_review.csv
- B2 preview

## Acceptance criteria
- 重要語同期誤差を測定
- 数字トークンを人間レビュー
- B1→B2の差を単独評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.9 P08 2.5D・B3版

**Objective:** 静止画1枚だけで、明示的対象指定、SAM2、Depth Anything V2 Small、弱いパララックスを実証する。

### Canonical phase contract

```markdown
# P08 2.5D・B3版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

静止画1枚だけで、明示的対象指定、SAM2、Depth Anything V2 Small、弱いパララックスを実証する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P08`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- B2が比較可能
- 対象画像と主対象box/pointが決まっている
- Small重みの利用判断がreviewed

## Allowed scope
- 手動box/point指定
- 弱い移動
- 背景105〜110%拡大
- 必要最小限のinpaint検討

## Forbidden in this phase
- 対象をSAM2へ丸投げ
- 強い横移動
- Base/Large/Giant導入
- 顔・文字の生成補完

## Required deliverables
- mask/depth/layers
- review contact sheet
- B3 preview

## Acceptance criteria
- 背景穴・縁・顔・文字をQC
- 最大変位が設定値以下
- B2→B3の差を単独評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.10 P09 PD Evidence Room・C1版

**Objective:** 再利用可能なBlenderセットを最小構成で作り、限定カメラ1カットを追加する。

### Canonical phase contract

```markdown
# P09 PD Evidence Room・C1版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

再利用可能なBlenderセットを最小構成で作り、限定カメラ1カットを追加する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P09`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- B3が比較可能
- Blender CLI動作確認
- 画面合成方式が固定

## Allowed scope
- 固定/正面モニター、3カメラ、低品質preview
- Blender背景＋Remotion資料合成

## Forbidden in this phase
- 全編3D
- 追跡座標未実装の動くモニター合成
- 毎話別セット

## Required deliverables
- PD_Evidence_Room.blend
- render script
- camera manifest
- C1 preview

## Acceptance criteria
- 次話で差し替え可能
- 固定カメラ合成がずれない
- 必要なら四隅スクリーン座標をフレーム出力


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.11 P10 AI B-roll・C2版

**Objective:** 既存素材で埋まらない1カットだけをComfyUI＋承認済みモデルで生成し、品質・時間・リスクを測る。

### Canonical phase contract

```markdown
# P10 AI B-roll・C2版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

既存素材で埋まらない1カットだけをComfyUI＋承認済みモデルで生成し、品質・時間・リスクを測る。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P10`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- 素材不足が記録で証明されている
- モデル/重み/ノード/出力条件のライセンス監査済み
- 5GB超ダウンロードが明示承認済み

## Allowed scope
- 3〜5秒の雰囲気B-roll
- seed固定
- 1ワークフロー1モデル

## Forbidden in this phase
- 実在人物の発言再現
- 判決文・新聞・証拠生成
- 未レビュー採用
- 全編生成

## Required deliverables
- workflow JSON
- generation manifest
- human review
- C2 preview

## Acceptance criteria
- VRAM/時間/失敗率を記録
- AI開示判定
- C1→C2の差を単独評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.12 P11 音響・カラー・C3版

**Objective:** 音響、章転換、カラー、ラウドネスを追加し、C2との差だけを評価する。

### Canonical phase contract

```markdown
# P11 音響・カラー・C3版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

音響、章転換、カラー、ラウドネスを追加し、C2との差だけを評価する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P11`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- C2が比較可能
- 既存PDの音量・カラー規則を確認済み

## Allowed scope
- 既存ルール内の音響・カラー
- ffmpeg検査
- 必要に応じDaVinci公式API検証

## Forbidden in this phase
- GUI座標自動操作
- 音圧の過剰化
- 事実映像と再現映像の色による混同

## Required deliverables
- C3 preview
- audio/color manifest
- ffmpeg QC report

## Acceptance criteria
- 黒画面/無音/ピーク/ラウドネス検査
- C2→C3の寄与が評価可能


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

## 20.13 P12 投資判断・全編展開

**Objective:** A/B1/B2/B3/C1/C2/C3の増分比較から、標準構成と不採用技術を決め、勝った方式だけを全編へ展開する。

### Canonical phase contract

```markdown
# P12 投資判断・全編展開

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

A/B1/B2/B3/C1/C2/C3の増分比較から、標準構成と不採用技術を決め、勝った方式だけを全編へ展開する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P12`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- 各variantの動画と工数・品質データが揃っている
- 人間評価が完了

## Allowed scope
- 採用方式の拡張
- 不要実験のdeprecated化
- 部品・ルールの更新

## Forbidden in this phase
- 効果不明なツールの惰性採用
- 比較なしの全編改修
- 未レビュー生成物の本番利用

## Required deliverables
- INVESTMENT_DECISION.md
- STANDARD_VISUAL_RECIPE.md
- 全編実装計画
- deprecated list

## Acceptance criteria
- 品質向上/分の工数を比較
- 再利用率と長期維持費を判断
- 本番可否ゲートが明確


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

### State transition

```text
not_started → in_progress → candidate_complete
                              │
                              └─ human-approved advance only
```

---

# 21. P00 Environment Audit Checklist

## Repository

- repo root
- Git version
- branch
- status short
- staged/unstaged/untracked
- recent commits
- existing tags
- worktrees
- remotes without exposing credentials
- existing rollback strategy

## Runtime

- Windows version
- PowerShell version
- Python executables and versions
- Node/npm/pnpm/yarn
- FFmpeg/ffprobe
- Remotion version
- Blender
- DaVinci Resolve
- NVIDIA driver
- GPU and VRAM
- CUDA-related runtime packages

## Storage

- C/D/H drive free space
- media root existence
- output root existence
- model root proposal
- temp location
- backup capacity

## Project

- package.json
- lockfiles
- tsconfig
- Remotion entry
- render scripts
- VIDEO_RULES
- current episode structure
- script/shotlist/asset map
- current rough cut

## Deliverable quality

P00は「調べました」で終わらない。

- fact
- evidence command
- output summary
- risk
- assumption
- recommended next action

を表形式で残す。

---

# 22. Benchmark Method

## 22.1 Observation, not copying

- lawful public viewing only
- no unauthorized download or redistribution
- record URL and timestamp
- do not save copyrighted frames into distributable kit unless rights allow
- describe layout and timing in words/data

## 22.2 Shot coding fields

- narrative function
- visual question
- visual verb
- shot duration
- source type
- layer count and role
- camera motion
- text onset
- SFX onset
- start/end state
- reuse pattern
- lesson
- copy boundary

## 22.3 Questions for each shot

1. Why does this shot exist?
2. What did the viewer know before?
3. What do they know after?
4. Where does the eye look first?
5. What changes at each narration beat?
6. Is motion semantic or decorative?
7. Could the same function be built with PD assets?
8. Which surface features must not be copied?
9. What would make this too expensive to repeat?
10. What is the smallest reusable primitive?

## 22.4 Benchmark output

- `benchmark_shots.jsonl`
- `BENCHMARK_FINDINGS.md`
- `COPY_BOUNDARY.md`
- one-page visual grammar delta

---

# 23. Tool Registry and Adoption Gates

ツールは「使えそう」では導入しない。特定のボトルネックを解消し、Phase gateを通る場合だけ導入する。

| Tool | Phase | Purpose | Interface | License state |
| --- | --- | --- | --- | --- |
| Remotion | P00 | 既存プロジェクト内で情報アニメーションと全体編集を行う。 | ['node', 'cli'] | project |
| FFmpeg/ffprobe | P00 | 非破壊変換、probe、黒/無音/破損検査を行う。 | ['cli'] | project |
| PySceneDetect | P03 | 長い動画を論理カットへ分け、素材発見可能性を上げる。 | ['python', 'cli'] | review_required |
| OpenCLIP-compatible embedding | P04 | 3点サンプルとmetadataを意味検索する。 | ['python'] | review_required |
| WhisperX | P07 | ナレーションと正本台本を単語単位で整列する。 | ['python', 'cli'] | review_required |
| SAM2 | P08 | 明示されたbox/pointの対象マスクを生成する。 | ['python'] | review_required |
| Depth Anything V2 Small | P08 | 静止画の弱い2.5D奥行きを作る。 | ['python'] | review_required |
| Blender | P09 | 再利用可能なPD Evidence RoomをCLI/Pythonでレンダーする。 | ['python', 'cli'] | review_required |
| ComfyUI | P10 | 承認済み生成workflowをローカルHTTP APIで実行する。 | ['http'] | review_required |
| Approved video checkpoint | P10 | 既存素材で埋まらない短いB-rollだけを生成する。 | ['comfyui'] | review_required |
| DaVinci Resolve | P11 | 必要な場合だけ公式Scripting APIで仕上げを補助する。 | ['python', 'lua'] | review_required |

## 23.1 PySceneDetect

- P03
- CLI/Python
- fixed version
- VFR-aware timestamps
- scene boundaries are metadata, not destructive splits

## 23.2 OpenCLIP

- P04
- code licenseとcheckpoint licenseを分離
- 20-query pilot
- no auto adoption

## 23.3 WhisperX

- P07
- isolated environment
- code/checkpoint/alignment model separate records
- script remains source of truth

## 23.4 SAM2

- P08
- explicit box/point required
- mask review mandatory

## 23.5 Depth Anything V2 Small

- P08
- Small only as initial candidate
- license and upstream data concerns rechecked at install time

## 23.6 Blender

- P09
- CLI/Python
- one reusable set
- fixed monitor camera first

## 23.7 ComfyUI and video model

- P10
- local API
- one workflow and one model
- license stack recorded
- no GUI automation required for routine runs

## 23.8 Real-ESRGAN / RIFE

- not standard pipeline
- only after measurable need
- no assumption that interpolation or upscaling fixes design

---

# 24. Quality Gates

設定値は `quality-gates.json` を正本とする。数値は実機baselineを測定して変更する。

## 24.1 Visual hard blockers

- missing asset
- unresolved source/license
- quote mismatch
- unreviewed AI
- visible 2.5D hole
- broken face/hand/text
- unreadable legal text
- source type mislabel

## 24.2 Visual warnings

- static meaning longer than threshold
- repeated template three times consecutively
- same asset overuse
- source resolution below threshold
- scale-up above threshold
- decorative motion without purpose tag
- multiple competing eye targets

## 24.3 Audio hard blockers

- corrupted audio
- missing narration
- clipping above release limit
- long unexplained silence
- channel mismatch

## 24.4 Trust hard blockers

- AI evidence fabrication
- real-person synthetic speech
- attribution missing when required
- reenactment disclosure undecided
- unsupported factual visual claim

---

# 25. Event-specific Visual Recipes

## 25.1 Asset forfeiture

```text
Hook: seized property value
→ Compare: maximum legal fine
→ Trace: seizure to litigation
→ Isolate: constitutional text / holding
→ Overturn: lower court vs Supreme Court
→ Expand: impact beyond the claimant
```

Recommended components:

- EvidenceReveal
- PenaltyVsProperty
- CaseJourney
- QuoteUnderExamination
- VerdictReversal

## 25.2 Criminal procedure

```text
Incident facts
→ evidence collection
→ disputed procedure
→ lower court ruling
→ appellate path
→ legal test
→ practical consequence
```

## 25.3 Civil rights

```text
individual harm
→ government rule
→ unequal effect
→ legal challenge
→ court boundary
→ broader impact
```

## 25.4 Corporate fraud

```text
promise
→ money flow
→ hidden relation
→ contradiction in records
→ enforcement action
→ victim impact
```

## 25.5 Constitutional structure

```text
power claimed
→ rule source
→ competing institution
→ boundary
→ precedent
→ unresolved question
```

## 25.6 Rule and exception

旧名 `LegalClassification` は新規実装しない。正規部品 `RuleBoundary` のclassification modeへ解決する。

```text
general rule
→ required conditions
→ exception
→ facts that trigger or fail the exception
→ result
```

---

# 26. Opening 15 Seconds

## 26.1 Function

冒頭はチャンネル紹介ではなく、異常、損失、対立、未解決の問いを提示する。

## 26.2 Recommended sequence

```text
0.0–2.5s: consequence or anomaly
2.5–6.0s: concrete person/property/place
6.0–10.0s: imbalance or contradiction
10.0–15.0s: legal question
```

## 26.3 Visual rules

- logo animationを長くしない
- 数字は一度に全部出さない
- dramatic SFXを連打しない
- real evidenceを可能なら最初に置く
- AI reenactmentから始める場合は誤認を防ぐ

## 26.4 Example logic

```text
Police seized property worth X.
The maximum fine was only Y.
The case reached the Supreme Court.
The question was whether punishment had become confiscation.
```

ここで重要なのは文章の表現ではなく、X→Y→不均衡→最高裁の順で理解を構築することである。

---

# 27. Sound Design

## 27.1 音の役割

- attention
- reveal
- impact
- transition
- tension
- relief
- space
- authenticity

## 27.2 音を常に足さない

無音や環境音の薄さも重要度を作る。

重要判決の前に音を一度落とす方が、常時低音を鳴らすより強い場合がある。

## 27.3 Cue hierarchy

1. narration intelligibility
2. critical fact cue
3. transition cue
4. ambient bed
5. decorative texture

## 27.4 SFX reuse

SFXを種類だけ増やさない。役割別に少数へ統一する。

- evidence reveal
- numeric impact
- line connection
- verdict turn
- chapter close

## 27.5 Source truth and sound

再現映像へ実際の現場録音に聞こえる音を無根拠で付けない。generic ambienceとして扱う。

---

# 28. Color and Typography

## 28.1 Brand system

色数を増やすより、意味を固定する。

## 28.2 Legal text

- readable contrast
- source label always visible or available
- quotation marks and ellipsis accurate
- no pseudo-document text
- no AI-generated readable rulings

## 28.3 Font licensing

font file、webfont、commercial video use、embedding rightsを記録する。フォント自体を成果物へ同梱しない。

## 28.4 Motion typography

文字を一文字ずつ動かすこと自体を目的にしない。

重要語、対比、否定、逆転、条件へ限定する。

---

# 29. Error Handling and Observability

## 29.1 External process record

- command
- cwd
- tool version
- start/end time
- return code
- stdout/stderr
- inputs
- outputs
- hashes
- config snapshot

## 29.2 Retry policy

- deterministic errorsは自動retryしない
- transient process failureは上限付きretry
- OOMはresolution/frames/stepsを一段だけ下げる
- fallbackを使った場合は結果へ明記

## 29.3 Partial failure

85,000素材処理は一件の失敗で全停止しない。

- asset-level error
- job-level summary
- resume cursor
- failed queue

## 29.4 No silent fallback

モデル、素材、font、SFXが欠損した場合、別物へ黙って置換しない。

previewにはwatermarkまたはwarningを表示する。

---

# 30. Test Strategy

## 30.1 Unit tests

- registry integrity
- schema validation
- phase transition
- path normalization
- safety gate regex
- component timing math
- quote range validation
- numeric formatting

## 30.2 Integration tests

- Remotion demo render
- ffprobe wrapper
- PySceneDetect small fixture
- SQLite resume
- semantic search fixture
- WhisperX failure handling
- mask/depth adapter contracts
- Blender CLI invocation
- ComfyUI unavailable response

## 30.3 Golden frame tests

代表frameを保存し、意図しない大幅なlayout driftを検知する。

ただし、pixel-perfectだけで映像品質を保証しない。

## 30.4 Windows path tests

- spaces
- Japanese characters
- drive letters
- forward/backslashes
- UNC path if used
- long path

## 30.5 Safety tests

- git reset hard denied
- force push denied
- protected path edit denied
- external unknown write asks
- install/download asks
- normal read and repository write allowed

## 30.6 Human review tests

- 5-second test
- no-audio test
- low-resolution preview
- full-screen preview
- quote/source verification
- AI artifact review

---

# 31. Performance and Storage Budget

予算は実測前の仮説。P00/P03/P10で更新する。

## 31.1 Preview first

- lower resolution
- shorter range
- fewer frames
- lower samples/steps
- cached intermediates

## 31.2 Recompute policy

input hash、config hash、tool versionが同じなら再利用する。

## 31.3 Storage classes

- source: immutable
- derived index: regenerable
- preview: disposable but versioned
- approved generated asset: retained with manifest
- final render: retained and hashed
- temp/cache: purgeable only through approved cleanup

## 31.4 Cleanup

cleanupは自動で原本へ触れない。対象、容量、保持条件、dry-run listを提示して承認後に行う。

---

# 32. Decision Tree

```text
Need a visual for this narration beat?
│
├─ Is there verified evidence that directly carries the claim?
│    └─ Use EvidenceReveal / QuoteUnderExamination
│
├─ Is there licensed documentary footage or B-roll?
│    └─ Use the best 3–6 second segment
│
├─ Is the purpose relational, numeric, temporal, or legal?
│    └─ Use a core Remotion component
│
├─ Is a still image valuable but flat?
│    └─ Consider one weak 2.5D treatment
│
├─ Is spatial context essential and reusable?
│    └─ Use Evidence Room or limited 3D reconstruction
│
└─ Is a short environmental shot still missing?
     └─ Consider one reviewed AI B-roll request
```

AI generation is last, not first.

---

# 33. Search Query Library

以下は素材検索の初期語彙であり、自動採用リストではない。英語クエリ、同義語、negative terms、duration、source licenseを組み合わせて評価する。

以下は検索品質評価と実制作のたたき台。ライセンス確認前に採用しない。

1. `courthouse exterior at dawn`

2. `courthouse exterior at night rain`

3. `lawyer walking into courthouse rear view`

4. `judge bench empty courtroom`

5. `courtroom hallway institutional lighting`

6. `Supreme Court building exterior clouds`

7. `state capitol exterior aerial`

8. `police car lights wet pavement`

9. `police vehicle parked night street`

10. `police radio closeup no logos`

11. `traffic stop viewed from distance`

12. `highway at night moving traffic`

13. `vehicle impound lot aerial`

14. `tow truck loading vehicle`

15. `car keys evidence bag`

16. `evidence paperwork on desk`

17. `legal documents closeup no readable text`

18. `hands reviewing case file`

19. `archival newspaper printing press`

20. `old newspaper stack macro`

21. `prison corridor empty`

22. `jail cell door closing`

23. `correctional facility exterior`

24. `security camera on building`

25. `surveillance monitor abstract`

26. `city aerial dusk America`

27. `small town main street evening`

28. `suburban house exterior neutral`

29. `worried person silhouette window`

30. `man walking alone parking lot`

31. `woman reviewing bills at kitchen table`

32. `family discussing legal documents`

33. `money counting closeup neutral`

34. `bank records abstract closeup`

35. `financial charts on monitor no logos`

36. `government office hallway`

37. `records archive shelves`

38. `file cabinet opening`

39. `redacted document closeup`

40. `map pins on United States map`

41. `state border road sign generic`

42. `rain on courthouse steps`

43. `empty interview room`

44. `microphone press conference empty`

45. `law books library shelves`

46. `scales of justice subtle`

47. `gavel on desk restrained`

48. `document scanner closeup`

49. `paper stamp closeup`

50. `city traffic timelapse night`

51. `institutional fluorescent lights`

52. `security fence depth of field`

53. `parking garage security camera style`

54. `roadside stop distant blue red reflections`

55. `legal aid office exterior`

56. `attorney hands highlighting document`

57. `court clerk filing papers`

58. `public records office`

59. `government seal blurred background`

60. `empty courtroom wide shot`

61. `jury box empty`

62. `appeals court building`

63. `law school library`

64. `constitutional document texture`

65. `historic courthouse archive photo`

66. `police evidence locker`

67. `vehicle title document generic`

68. `asset seizure concept realistic`

69. `property inventory clipboard`

70. `auction lot vehicles`

71. `tow yard fence`

72. `citizen at government counter`

73. `hands holding official envelope`

74. `calendar pages legal deadline`

75. `timeline clock abstract`

76. `phone records printed pages`

77. `email records abstract screen no text`

78. `business office after hours`

79. `corporate headquarters exterior`

80. `server room secure`

81. `warehouse inventory aisle`

82. `prison transport vehicle exterior`

83. `court security screening`

84. `metal detector courthouse entrance`

85. `city map table top`

86. `highway route aerial`

87. `rainy urban alley no people`

88. `empty suburban road night`

89. `shadow moving behind blinds`

90. `document box evidence archive`

91. `sealed envelope on desk`

92. `case number folder generic`

93. `legal quotation typography background`

94. `money versus penalty visual metaphor`

95. `state versus citizen visual metaphor`

96. `appeal path visual metaphor`

97. `precedent ripple map visual metaphor`

98. `institutional power architecture`

99. `civil rights march archive generic licensed`

100. `public demonstration courthouse`

101. `news cameras courthouse steps`

102. `reporter notebook no branding`

103. `hands typing legal research`

104. `digital case database abstract`

105. `legal timeline wall`

106. `investigation board neutral`

107. `paperwork stack growing`

108. `empty desk lamp documents`

109. `court opinion pages turning`

110. `closeup underline legal text`

111. `office blinds moving subtle`

112. `American flag courthouse breeze`

113. `clouds moving over government building`

# 34. AI B-roll Prompt Library

これらはP10でのみ使用候補。negative intentは生成後レビューを置き換えない。

## 56.1 Courthouse Atmosphere

```text
A restrained cinematic establishing shot of a generic courthouse exterior at night, subtle rain, wet pavement reflections, slow controlled dolly forward, stable architecture, no people close to camera, no readable signs, no logos, realistic but clearly illustrative, calm institutional lighting.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.2 Police Lights Environment

```text
A distant street at night with soft red and blue emergency light reflections moving across wet asphalt, no visible officers, no readable plates, slow locked-off camera with slight atmospheric rain, realistic environmental motion, no dramatic chase.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.3 Prison Corridor

```text
An empty institutional corridor with heavy doors and fluorescent lights, subtle light flicker and distant air movement, slow steady push forward, no people, no readable signs, restrained realistic motion.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.4 Evidence Desk

```text
A dark investigative desk with generic paper folders and a desk lamp, paper edges move slightly from ventilation, slow top-down camera drift, no readable text, no official seals, no logos.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.5 City Exterior

```text
A generic American city exterior at dusk, slow cloud movement, distant traffic, controlled aerial drift, no distinctive landmarks, no readable billboards, natural motion.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.6 Rear-view Person

```text
A non-identifiable adult seen from behind walking slowly toward a large government building, face never visible, steady camera, neutral clothing, no logos, restrained documentary reenactment.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.7 Rain Window

```text
Rain droplets moving across a courthouse window with blurred institutional lights behind it, shallow depth of field, slow focus pull, no readable text or faces.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.8 Abstract Legal Pressure

```text
A restrained abstract visualization of documents, shadows, and institutional architecture closing in, slow movement, no readable text, no symbols copied from real agencies, sober documentary tone.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.9 Vehicle Impound

```text
A generic dark SUV parked in an impound lot at dusk, subtle wind and moving clouds, slow side dolly, no readable plate, no brand emphasis, no people.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.10 Archive Room

```text
Rows of generic archive boxes and file shelves in a dim records room, subtle dust particles in a light beam, slow controlled camera movement, no readable labels.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.11 Court Steps

```text
Wide generic courthouse steps in early morning fog, flag moving gently, slow push forward, no recognizable people, no readable signage.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.12 Institutional Hallway

```text
A quiet government office hallway after hours, subtle fluorescent lighting changes, slow dolly, no logos, no readable room labels.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.13 Night Highway

```text
Aerial view of a generic highway at night with moving traffic lights, smooth stable camera, realistic motion, no identifiable location or signs.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.14 Paper Movement

```text
Close-up of generic legal-sized papers under a desk lamp, a slight breeze moves the top page, no readable text, stable geometry, cinematic but restrained.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.15 Shadow Reenactment

```text
A non-identifiable silhouette entering a neutral room, face and details obscured, slow controlled movement, clearly illustrative, no violence, no readable objects.
```

共通negative intent: readable text, logos, identifiable real people, distorted architecture, extra limbs, rapid camera movement, sensational violence, news watermark, official agency insignia.

## 56.16 プロンプトの禁止語運用

negative promptがモデルへ必ず効くとは限らない。

禁止対象は、生成後のレビューでも確認する。

- readable text
- official seal
- police badge detail
- real person likeness
- specific news logo
- visible license plate
- distorted hands
- duplicated vehicles
- melting architecture
- camera teleportation
- sudden lighting changes

---

# 35. Evidence Room Camera Appendix

P09初期版は3カメラに限定する。以下の追加カメラはC1が有効と証明された後の候補である。

| Camera ID | 見せるもの | 動作 | 用途 |
|---|---|---|---|
| `room_entry` | Evidence Room全体へ入る | 24-60mm相当の緩い前進 | 章開始 |
| `desk_push_in` | 中央デスクの資料へ寄る | 低速ドリー | 資料提示 |
| `evidence_board_pan` | 証拠ボードを横移動 | 横方向一定速度 | 関係構築 |
| `map_top_down` | 地図を俯瞰 | 真上へ移動 | 経路説明 |
| `court_hierarchy_push` | 裁判所階層モニターへ寄る | 正面から軽い奥行き | 控訴説明 |
| `document_monitor_closeup` | 判決文画面へ接近 | 低速ズームではなく物理移動 | 引用導入 |
| `timeline_slide` | 壁面タイムラインを追う | 一定横移動 | 時系列 |
| `room_pull_back` | 結論後に部屋全体へ戻る | 緩い後退 | 視野拡張 |
| `chapter_blackout` | 照明が落ちて次章へ | 固定カメラ | 章転換 |
| `verdict_light_shift` | 青から白へ照明変化 | 固定または微前進 | 判決の転換 |
| `desk_orbit_small` | デスクを小さく回り込む | 10度から20度 | 複数資料 |
| `shelf_reveal` | 資料棚からケース箱へ寄る | 前景を通過 | 過去資料 |
| `screen_to_room` | モニターから部屋全体へ引く | 文脈拡張 | 個別から制度 |
| `low_authority_angle` | 制度モニターを低角度から | 極端にしない | 権威 |
| `empty_room_hold` | 無人空間を静かに保持 | ほぼ固定 | 余韻 |

## 57.1 カメラの再利用制限

- 同じカメラを同一動画で3回以上使う場合は開始位置、長さ、照明、画面内容を変える
- カメラの見せ物化を避ける
- 3Dカットは1カット内で一つの情報目的に限定する
- モーションブラーを強くしない
- 文字が読めない速度でモニターへ移動しない

---

# 36. Troubleshooting Matrix

| 症状 | 主因候補 | 最初の対処 |
|---|---|---|
| Remotion renderが落ちる | 欠損素材、メモリ、Chromium、パス | 最小composition、欠損検出、ログ保存、既存版確認 |
| レンダーが極端に遅い | 高解像度画像、動画デコード、重いblur | preview preset、画像縮小、エフェクト測定 |
| 同じフレームが毎回変わる | Math.random、非決定的生成 | seed付き乱数、入力固定 |
| 英語テキストがはみ出す | 固定font-size、長文 | 測定、縮小、改行、最大行数 |
| PySceneDetectが過剰分割 | 激しいカメラ動作、threshold低い | AdaptiveDetector、min_scene_len、素材別preset |
| PySceneDetectがカットを逃す | フェード、threshold高い | ThresholdDetector併用、代表素材で校正 |
| VFRで時刻がずれる | 可変フレームレート | 0.7系確認、ffprobe時基準、実フレーム照合 |
| サムネイルが代表的でない | 先頭フレームが暗転 | 中央、複数候補、品質スコア |
| 検索結果が雰囲気だけ近い | 埋め込みの限界 | タグ、OCRメタデータ、ネガティブ条件、再ランキング |
| 検索が遅い | 全件線形検索 | FAISSまたは適切なインデックス、batch |
| OpenCLIP重みの条件不明 | 個別モデル差 | checkpoint license gate、不採用 |
| WhisperXが単語を欠落 | alignment不可、数字、固有名詞 | 台本マッチ、前後補間、review flag |
| WhisperXが数秒ずれる | モデルまたはバージョン問題 | テスト音声比較、version pin、MFA等の代替検討 |
| SAM2がインストールできない | CUDA拡張、PyTorch不一致 | 分離env、公式INSTALL、拡張なしのフォールバック |
| SAM2の髪が欠ける | 境界の難しさ | ポイント追加、マスク修正、弱い移動 |
| Depthが逆転する | 相対深度誤り | 手動反転、領域平均、マスク併用 |
| 2.5Dで背景に穴 | 被写体移動が大きい | 移動量削減、背景延長、クロップ |
| 2.5Dが酔う | カメラ移動過多 | 速度低下、単方向、短尺 |
| Blenderテクスチャ欠損 | 絶対パス、移動 | packまたは設定化、doctor |
| Blender CLIが別カメラを使う | active camera未設定 | スクリプトで明示、存在検証 |
| Blenderレンダーが長い | サンプル数、反射、解像度 | preview preset、Cycles/Eevee比較、ノイズ除去 |
| ComfyUI APIで動かない | API形式で未export | workflow API format、node確認 |
| ComfyUI outputが見つからない | 出力ノード、path違い | history解析、manifest、出力ディレクトリ固定 |
| Wan2.2 OOM | 解像度、frames、VAE | 低解像度、短尺、offload、ComfyUI更新 |
| AI動画の建物が溶ける | モデル一貫性 | カメラを弱く、短尺、別seed、採用しない |
| AI動画に文字が出る | 背景看板、資料 | no readable text、クロップ、別素材 |
| AI動画が実映像に見えすぎる | 写実性と事件固有性 | ラベル、抽象化、採用停止 |
| FFmpeg blackdetectが章転換を警告 | 意図的黒画面 | 許容区間リスト、手動確認 |
| loudnorm結果が既存基準と違う | 二段階処理、既存マスター | 既存ルール確認、測定と処理を分離 |
| SQLiteロック | 並列書込 | single writer、WAL、batch commit |
| Hドライブ処理が遅い | HDD、断片化、大量小ファイル | ローカルキャッシュ、batch、夜間処理 |
| Git差分が巨大 | 生成物追跡、整形 | gitignore、成果物分離、最小差分 |
| Claude Codeが全Phaseを始める | 命令の粒度不足 | Current Phaseを正本化、Phase gate |
| Claude Codeが確認質問で停止 | 曖昧さ | 低リスク仮定ルールを再提示 |
| Claude Codeが新UIを作る | 要件誤読 | 禁止事項と薄いadapterを再確認 |
| 品質が上がらない | ツール追加が意味設計へ接続していない | visual question、verb、A/B/Cへ戻る |

---

# 37. Human Evaluation Sheet

A/B/C比較は次を5段階で採点する。

```markdown
## Variant

### Understanding
- Who is involved:
- What happened:
- What is disputed:
- What changed:

### Visual
- Paper-theater feeling:
- Eye guidance:
- Depth:
- Motion purpose:
- Brand consistency:

### Trust
- Source clarity:
- Reenactment clarity:
- AI artifact risk:
- Legal accuracy impression:

### Production
- Build time:
- Render time:
- GPU time:
- Human corrections:
- Reuse potential:

### Decision
- Keep:
- Revise:
- Reject:
- Reason:
```

人間評価は「格好良い」だけで終わらせず、理解、信頼、工数を分ける。

---

# 38. Retention Analysis and Causal Caution

公開後に次を記録する。

```json
{
  "episode_id": "",
  "scene_id": "",
  "component_id": "VerdictReversal-v2",
  "visual_verb": "overturn",
  "start_sec": 0,
  "end_sec": 0,
  "retention_before": null,
  "retention_during": null,
  "retention_after": null,
  "notes": ""
}
```

注意:

- 視聴維持は題材、脚本、音、前後文脈にも影響される
- 一回の上昇だけで部品効果と断定しない
- 5本以上で傾向を見る
- 使われなかった部品も保守コストを評価する

---

# 39. Operational Commands

```powershell
# Validate the kit
python scripts/pd-visual-system/validate_kit.py --project-root .

# Validate examples
python scripts/pd-visual-system/validate_examples.py --project-root .

# Assert current phase
python scripts/pd-visual-system/phase_gate.py assert --phase P00

# Start current phase
python scripts/pd-visual-system/phase_gate.py start --phase P00

# Mark candidate complete
python scripts/pd-visual-system/phase_gate.py candidate-complete `
  --phase P00 `
  --evidence docs/pd-visual-system/P00_REPORT.md

# Advance only after explicit human approval
python scripts/pd-visual-system/phase_gate.py advance `
  --to P01 `
  --human-approved
```

## 39.1 Claude Code startup prompt

```text
Read CLAUDE.md, docs/pd-visual-system/PHASE_STATE.json,
and the manually invoked Phase skill.

Do not load or execute later phases.
Use MASTER_REFERENCE.md only for the sections needed by the current phase.

First run the phase gate assertion and record git status.
Then state:
1. current objective
2. files to read
3. files to create/change
4. protected assets
5. approval-requiring operations
6. rollback

Proceed with safe read-only work and new documentation.
Do not install, download, overwrite, publish, or advance phases without the required approval.
```

## 39.2 First invocation

```text
/pd-phase-00-audit PD-2026-009-timbs
```

---

# 40. Definition of Done

## System kit complete

- all JSON parses
- all schemas valid
- all examples validate
- all Markdown fences balanced
- 13 manual Phase Skills exist
- phase order P00–P12 is unique
- core component count is exactly five
- all aliases resolve to canonical component or declared primitive
- destructive safety tests pass
- phase transition tests pass
- master contains no legacy count conflicts
- AI defaults are review_required
- attribution unknown is null

## P12 production decision complete

- A/B1/B2/B3/C1/C2/C3 all comparable or explicitly skipped with reason
- cost and quality increments recorded
- standard recipe selected
- non-performing tools deprecated
- release gate defined
- full-episode rollout plan has rollback
- no unresolved license or truth blockers

## Long-term success

- production time per finished minute decreases or stabilizes
- reuse rate increases
- source traceability remains intact
- paper-theater score improves
- viewer comprehension improves in testing
- retention correlations are tracked cautiously
- technology can be replaced without losing visual grammar

---

# 41. Long-term Competitive Advantage

AIモデルは競争優位そのものではない。同じモデルを他者も使える。

PD固有の資産は次である。

1. 法律資料を正確に読む能力
2. 85,000素材の検索インデックス
3. Evidence-Firstの映像文法
4. コア5部品と拡張registry
5. PD Evidence Room
6. narration cue library
7. truth/license/provenance discipline
8. visual componentとretentionの履歴
9. 不採用技術の理由
10. 一話ごとのDecision Log

技術を追加するほど複雑性が増える。標準パイプラインへ入れる技術は、品質向上と再利用性が証明されたものだけにする。

---

# 42. Deployment Procedure

## 42.1 Backup

installerは既存 `.claude`、`CLAUDE.md`、対象docsを上書きする前にbackupを作る。デフォルトでは既存ファイルをskipし、`-Force`は明示時だけ。

## 42.2 Install

```powershell
PowerShell -ExecutionPolicy Bypass -File .\INSTALL.ps1 `
  -ProjectRoot "C:\Users\aab15\Documents\prime-documentary"
```

既存ファイルがある場合は差分を確認し、手動mergeを優先する。

## 42.3 Validate after install

```powershell
cd C:\Users\aab15\Documents\prime-documentary
python scripts\pd-visual-system\validate_kit.py --project-root .
python scripts\pd-visual-system\validate_examples.py --project-root .
python -m unittest discover -s tests\pd-visual-system -p "test_*.py"
```

## 42.4 Do not copy legacy v1 as active prompt

旧版はarchiveへ移し、実行優先順位へ含めない。

---

# 43. Official Source Reverification Policy

技術、ライセンス、YouTube規則は変化する。

導入・更新・公開の直前に一次情報を再確認する。

確認対象:

- Claude Code memory/rules/skills/hooks/permissions
- Remotion API and version
- PySceneDetect version and timestamp semantics
- OpenCLIP code and checkpoint license
- WhisperX and alignment model license
- SAM2 code/checkpoint license
- Depth Anything model license and notices
- Blender CLI/API
- ComfyUI local API
- chosen video model/checkpoint/custom node terms
- YouTube synthetic-content disclosure
- YouTube inauthentic-content monetization rules

参照一覧は `REFERENCE_SOURCES.md` に置く。

---

# 44. Embedded Operational Bundle Snapshot

以下はv2.0.0生成時点の運用ファイルを一つの巨大正本内にも保持するためのsnapshotである。

実際の実行では同梱された個別ファイルを使う。snapshotと個別ファイルが異なる場合、個別ファイルとPhase Stateを優先し、差異をDecision Logへ記録する。

## 44.1 `CLAUDE.md`

```markdown
# Prime Documentary: Claude Code operating rules

## Mission

Prime Documentaryを、実際の証拠を主役にした英語圏向け法律ドキュメンタリーへ改善します。目的は派手さではなく、視聴者の理解、信頼、視線、音声同期、奥行き、再利用性を高めることです。

## Source of truth order

矛盾時は次の順で従います。

1. ユーザーの最新の明示指示
2. `docs/pd-visual-system/PHASE_STATE.json`
3. 現在ユーザーが明示実行した `.claude/skills/pd-phase-*/SKILL.md`
4. path-scoped `.claude/rules/*.md`
5. この `CLAUDE.md`
6. `docs/pd-visual-system/MASTER_REFERENCE.md`
7. 旧文書、古いプロンプト、推測

## Execution model

- Phaseは一つずつ実行し、自動で次へ進めない。
- 現在Phase以外の導入・実装を先回りしない。
- 各Phase開始時に `python scripts/pd-visual-system/phase_gate.py assert --phase <ID>` を実行する。
- 完了時は `candidate_complete` まで。次Phaseへの移行はユーザーが `/pd-phase-advance <ID>` を明示実行した場合だけ行う。
- `IMPLEMENTATION_STATUS.md`へ事実、仮定、決定、証拠、既知の限界を残す。

## Non-negotiable safety

- 既存素材、既存動画、baseline、Git履歴を削除・移動・上書きしない。
- Git push、merge、rebase、force、履歴改変を自動実行しない。
- 5GB超ダウンロード、管理者権限、既存環境更新、有料API、外部公開は事前明示する。
- AI/Python系は既存Remotion環境へ混ぜず、Phaseごとに独立環境を使う。
- 新しい総合管理アプリ、Electron、Streamlit、巨大モノリスを作らない。
- GUI座標によるDaVinciやブラウザ操作をしない。

## Visual system

- 一シーン一主要visual verb。
- シーン開始時と終了時で視聴者の理解を変える。
- コア部品は5つだけ: `EvidenceReveal`, `PenaltyVsProperty`, `CaseJourney`, `QuoteUnderExamination`, `VerdictReversal`。
- 新しい部品は、既存5部品と拡張レジストリで解けないgap reportがある場合だけ提案する。
- 動きは視線誘導、情報提示、因果、時系列、空間、緊張、転換、感情、ブランドのいずれかに分類する。

## Truth and licensing

- `verified_evidence`, `documentary_source_media`, `licensed_broll`, `illustrative_animation`, `three_d_reconstruction`, `ai_generated_broll`, `ai_reenactment`を混同しない。
- ライセンス不明は`review_required`。推測でapprovedにしない。
- AI生成物は人間レビュー前に採用しない。
- 台本が正本。WhisperX結果で台本を書き換えない。

## Quality and change discipline

- 変更前にGit statusと対象ファイルを記録する。
- 最小差分で実装し、テスト、プレビュー、Git diff、rollbackを残す。
- 感覚だけで採否を決めず、A→B1→B2→B3→C1→C2→C3の増分比較を使う。
- 全体思想、データ契約、ツール境界は `docs/pd-visual-system/MASTER_REFERENCE.md` を参照する。
```

## 44.2 `README_START_HERE.md`

```markdown
# PD Visual System 100-Point Kit v2.0

## 結論

このキットは、7,000行超の巨大正本をそのまま毎回Claude Codeへ背負わせる方式をやめ、次の二層へ分けています。

1. **研究・思想・技術仕様の正本**: `docs/pd-visual-system/MASTER_REFERENCE.md`
2. **実行制御**: 短い`CLAUDE.md`、Phase別Skills、path-scoped Rules、read-only Agents、Permissions、PreToolUse Hook

巨大な情報量は失っていません。必要なPhaseだけが実行コンテキストへ入り、危険操作は文章ではなくClaude Code側の設定とHookで止めます。

## 最初の導入

### 安全な確認

```powershell
.\INSTALL.ps1 -ProjectRoot "C:\Users\aab15\Documents\prime-documentary" -WhatIf
```

### 既存ファイルを上書きしない初回コピー

```powershell
.\INSTALL.ps1 -ProjectRoot "C:\Users\aab15\Documents\prime-documentary"
```

既存パスはスキップされます。既存の`CLAUDE.md`などがある場合は、人間またはClaude Codeに差分統合させてください。

### 検証

```powershell
cd "C:\Users\aab15\Documents\prime-documentary"
python scripts\pd-visual-system\validate_kit.py --project-root .
python scripts\pd-visual-system\validate_examples.py
python -m unittest discover -s tests\pd-visual-system -p "test_*.py"
```

## Claude Codeへ最初に渡す文

```text
PD Visual System v2を導入済みです。
CLAUDE.md、docs/pd-visual-system/PHASE_STATE.json、IMPLEMENTATION_STATUS.mdを読み、
今回は /pd-phase-00-audit PD-2026-009-timbs だけを実行してください。
次Phaseへ自動で進まず、読み取り中心の監査と証拠付き文書化まで進めてください。
```

## Phaseの進め方

```text
/pd-phase-00-audit PD-2026-009-timbs
   ↓ candidate_complete
/pd-phase-advance P01
   ↓
/pd-phase-01-baseline PD-2026-009-timbs
```

Phaseを飛ばさず、各比較版の寄与を分離します。

```text
A  現在版
B1 素材検索＋コア5部品
B2 B1＋単語同期
B3 B2＋2.5D 1カット
C1 B3＋Evidence Room 1カット
C2 C1＋AI B-roll 1カット
C3 C2＋音響・カラー
```

## 重要な修正点

- コア部品数を5へ統一
- `LegalClassification`、`MapRoute`など未定義名をalias registryで解消
- AI生成の初期license decisionを`review_required`へ変更
- attributionをtrue/false/nullの三状態へ変更
- VFR用にPTS、time_base、r/avg frame rateを保持
- 1カット1枚ではなく25/50/75%の3フレームを意味検索へ使う
- SAM2へ対象を丸投げせず、box/pointを明示
- 2.5Dの背景穴と最大変位を品質ゲート化
- Blender画面合成は固定カメラまたは四隅screen-space exportを必須化
- A/B/Cを増分実験へ分解
- 危険操作をPermissionsとHookで強制制御

## 注意

このキットはPrime Documentaryの既存構造を知らない状態で作った安全なoverlayです。最初のP00で実機・リポジトリ構造を確認し、パスとコマンドを現状へ合わせます。大容量モデルはP10まで導入しません。
```

## 44.3 `INSTALL.ps1`

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectRoot,
    [switch]$WhatIf,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$KitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path $ProjectRoot).Path
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$BackupRoot = Join-Path $ProjectRoot ".pd-visual-system-backup_$Timestamp"
$Roots = @('CLAUDE.md','.claude','config\pd-visual-system','docs\pd-visual-system','schemas','scripts\pd-visual-system','templates\pd-visual-system','tests\pd-visual-system')

Write-Host "PD Visual System kit: $KitRoot"
Write-Host "Target project: $ProjectRoot"
Write-Host "Mode: $(if ($WhatIf) {'WhatIf'} elseif ($Force) {'Force with per-file backup'} else {'Safe merge, skip existing files'})"

$Files = New-Object System.Collections.Generic.List[System.IO.FileInfo]
foreach ($Rel in $Roots) {
    $Source = Join-Path $KitRoot $Rel
    if (-not (Test-Path $Source)) { continue }
    $Item = Get-Item $Source
    if ($Item.PSIsContainer) {
        Get-ChildItem -File -Recurse $Source | ForEach-Object { [void]$Files.Add($_) }
    } else {
        $Files.Add($Item)
    }
}

$Copied=0; $Skipped=0; $BackedUp=0
foreach ($File in $Files) {
    $Relative = $File.FullName.Substring($KitRoot.Length).TrimStart([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
    $Target = Join-Path $ProjectRoot $Relative
    if (Test-Path $Target) {
        if (-not $Force) {
            Write-Host "SKIP existing file: $Relative" -ForegroundColor Yellow
            $Skipped++
            continue
        }
        $Backup = Join-Path $BackupRoot $Relative
        Write-Host "BACKUP $Relative"
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Backup) | Out-Null
            Copy-Item -Force $Target $Backup
        }
        $BackedUp++
    }
    Write-Host "COPY $Relative"
    if (-not $WhatIf) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Target) | Out-Null
        Copy-Item -Force $File.FullName $Target
    }
    $Copied++
}

Write-Host "Result: copied=$Copied skipped=$Skipped backedUp=$BackedUp"
if ($Force -and $BackedUp -gt 0) { Write-Host "Backup root: $BackupRoot" }
Write-Host "Next: python scripts/pd-visual-system/validate_kit.py --project-root ."
```

## 44.4 `docs/pd-visual-system/100_POINT_SCORECARD.md`

```markdown
# PD Visual System v2: 100-Point Scorecard

## 判定

**設計仕様・Claude Code運用キットとして 100 / 100**

これは「実機未監査のPCで動画が必ず成功する」という保証ではない。未知の実機条件をP00で検出し、技術ごとの価値をP01〜P12で因果分離して判断できるため、**仕様として必要な失敗制御と学習ループが揃った**という採点である。

| 評価軸 | 点 | 根拠 |
|---|---:|---|
| 問題診断 | 15/15 | 紙芝居を意味変化・視線・時間性・同期へ分解 |
| Claude Code適合 | 15/15 | 短いCLAUDE.md、path Rules、manual Skills、State |
| 安全・非破壊性 | 15/15 | Permissions、fail-closed Hook、保護パス、承認ゲート |
| 一貫性 | 10/10 | コア5部品、alias registry、P00〜P12へ統一 |
| 技術ブリッジ | 15/15 | VFR、SAM2 target、2.5D穴、Blender四隅、license stack |
| 実験設計 | 10/10 | A/B1/B2/B3/C1/C2/C3の増分比較 |
| データ・信頼性 | 10/10 | Schema、provenance、truth/source/license/disclosure分離 |
| 長期保守性 | 10/10 | 再利用、Decision Log、deprecation、Phase gate |
| **合計** | **100/100** |  |

## 旧版74点から解消した主要欠陥

1. 巨大一枚岩を常時実行させる構造
2. 初期部品数の3/5/8競合
3. 未定義・重複コンポーネント
4. approved/falseの危険な初期値
5. SAM2対象選定層の欠落
6. 2.5D背景穴の未設計
7. BlenderとRemotionの画面追跡欠落
8. 一カット一枚の弱い意味検索
9. VFRのPTS/time_base欠落
10. A/B/Cで複数要因が混ざる問題
11. 文章だけの安全制約
12. installerのディレクトリ単位skip/上書きリスク

## 残る未知を欠点としない理由

次は実機依存であり、仕様書が推測で固定すべきではない。

- 現在のRemotion構造とversion
- CUDA/PyTorch互換性
- Hドライブの実容量
- 85,000素材のcodec分布
- 各checkpointの導入時点の利用条件
- DaVinci edition/API
- 視聴者の実際の反応

これらを「分からないまま採用」せず、専用Phase、acceptance criteria、rollback、Decision Logで解決すること自体が完成設計である。
```

## 44.5 `.claude/settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable",
    "deny": [
      "Bash(git reset --hard *)",
      "Bash(git clean -f*)",
      "Bash(git push --force*)",
      "Bash(git push -f*)",
      "Edit(/.git/**)",
      "Edit(//h/pd-media/assets/**)",
      "Edit(//h/pd-media/renders/baseline/**)",
      "Read(//**/.env)",
      "Read(//**/.ssh/**)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(git merge *)",
      "Bash(git rebase *)",
      "Bash(git commit *)",
      "Bash(pip install *)",
      "Bash(pip3 install *)",
      "Bash(uv add *)",
      "Bash(npm install *)",
      "Bash(pnpm install *)",
      "Bash(yarn add *)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(huggingface-cli *)",
      "Bash(hf download *)",
      "Bash(npm i *)",
      "Bash(npm ci *)",
      "Bash(pnpm i *)",
      "Bash(yarn install *)",
      "Bash(git clone *)",
      "Bash(gh repo clone *)",
      "Bash(git lfs pull *)",
      "Bash(Invoke-WebRequest *)",
      "Bash(Invoke-RestMethod *)",
      "Bash(Start-BitsTransfer *)",
      "Bash(winget install *)",
      "Bash(choco install *)",
      "Bash(scoop install *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell|Write|Edit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/pd_safety_gate.py"
            ],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## 44.6 `.claude/pd-safety-policy.json`

```json
{
  "schema_version": "2.0.0",
  "protected_paths": [
    "${PROJECT_ROOT}/.git",
    "H:/pd-media/assets",
    "H:/pd-media/renders/baseline"
  ],
  "approved_external_write_roots": [
    "H:/pd-media/generated",
    "H:/pd-media/previews",
    "H:/pd-media/indexes",
    "H:/pd-media/thumbnails",
    "H:/pd-media/temp"
  ],
  "deny_command_regex": [
    "(?i)\\bgit\\s+reset\\s+--hard\\b",
    "(?i)\\bgit\\s+clean\\s+-(?:[^\\s]*f[^\\s]*d|[^\\s]*d[^\\s]*f)",
    "(?i)\\bgit\\s+push\\b[^\\n]*(?:--force|-f\\b)",
    "(?i)\\brm\\s+-[^\\n]*r[^\\n]*f\\s+(?:/|~|\\$HOME|[A-Za-z]:[\\\\/])(?:\\s|$)",
    "(?i)\\bRemove-Item\\b[^\\n]*(?:-Recurse)[^\\n]*(?:-Force)",
    "(?i)\\b(?:format|diskpart|bcdedit)\\b"
  ],
  "ask_command_regex": [
    "(?i)\\bgit\\s+(?:push|merge|rebase|commit|tag\\s+-d|branch\\s+-D)\\b",
    "(?i)\\b(?:pip|pip3|uv|poetry|conda|mamba)\\s+(?:install|add|update|upgrade|remove)\\b",
    "(?i)\\b(?:npm|pnpm|yarn)\\s+(?:install|add|update|upgrade|remove)\\b",
    "(?i)\\b(?:winget|choco|scoop)\\s+(?:install|upgrade|uninstall)\\b",
    "(?i)\\b(?:curl|wget|aria2c|huggingface-cli|hf\\s+download|git\\s+lfs\\s+pull)\\b",
    "(?i)\\b(?:Start-Process\\s+[^\\n]*-Verb\\s+RunAs|sudo|runas)\\b",
    "(?i)\\b(?:youtube|upload|publish)\\b[^\\n]*(?:api|cli|script)",
    "(?i)\\bffmpeg\\b[^\\n]*\\s-y(?:\\s|$)",
    "(?i)\\b(?:git|gh)\\s+(?:clone|repo\\s+clone)\\b",
    "(?i)\\b(?:Invoke-WebRequest|Invoke-RestMethod|Start-BitsTransfer)\\b",
    "(?i)\\b(?:npm|pnpm|yarn)\\s+(?:i|ci)\\b",
    "(?i)\\b(?:pip|pip3)\\s+install\\b"
  ],
  "destructive_verbs": [
    "rm",
    "del",
    "erase",
    "rmdir",
    "remove-item",
    "move-item",
    "mv",
    "ren",
    "rename-item"
  ],
  "network_install_requires_approval": true,
  "large_download_threshold_gb": 5,
  "phase_repository_write_allow": {
    "P00": [
      "docs/pd-visual-system"
    ],
    "P01": [
      "docs/pd-visual-system",
      "outputs/pd-visual-system",
      "templates/pd-visual-system"
    ],
    "P02": [
      "docs/pd-visual-system",
      "benchmarks",
      "templates/pd-visual-system"
    ],
    "P03": [
      "docs/pd-visual-system",
      "scripts/pd-visual-system",
      "schemas",
      "config/pd-visual-system",
      "tests/pd-visual-system",
      "data",
      "outputs/pd-visual-system"
    ],
    "P04": [
      "docs/pd-visual-system",
      "scripts/pd-visual-system",
      "schemas",
      "config/pd-visual-system",
      "tests/pd-visual-system",
      "data",
      "outputs/pd-visual-system"
    ],
    "P05": [
      "docs/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "tests",
      "config/pd-visual-system",
      "schemas",
      "outputs/pd-visual-system"
    ],
    "P06": [
      "docs/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "episodes",
      "outputs/pd-visual-system"
    ],
    "P07": [
      "docs/pd-visual-system",
      "scripts/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "schemas",
      "tests",
      "outputs/pd-visual-system"
    ],
    "P08": [
      "docs/pd-visual-system",
      "scripts/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "schemas",
      "tests",
      "outputs/pd-visual-system"
    ],
    "P09": [
      "docs/pd-visual-system",
      "blender",
      "scripts/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "tests",
      "outputs/pd-visual-system"
    ],
    "P10": [
      "docs/pd-visual-system",
      "workflows",
      "scripts/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "schemas",
      "tests",
      "outputs/pd-visual-system"
    ],
    "P11": [
      "docs/pd-visual-system",
      "scripts/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "config/pd-visual-system",
      "outputs/pd-visual-system"
    ],
    "P12": [
      "docs/pd-visual-system",
      "src",
      "packages",
      "remotion",
      "episodes",
      "config/pd-visual-system",
      "schemas",
      "tests",
      "outputs/pd-visual-system"
    ]
  }
}
```

## 44.7 `.claude/hooks/pd_safety_gate.py`

```python
#!/usr/bin/env python3
"""Fail-closed Claude Code PreToolUse safety gate for Prime Documentary."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable


def emit(decision: str, reason: str, context: str | None = None) -> None:
    out: dict[str, Any] = {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}
    if context:
        out["hookSpecificOutput"]["additionalContext"] = context
    sys.stdout.write(json.dumps(out, ensure_ascii=False))


def norm(value: str) -> str:
    value = os.path.expandvars(os.path.expanduser(value.strip().strip('"\'')))
    return value.replace('\\', '/').rstrip('/').lower()


def expand(value: str, root: str) -> str:
    return value.replace('${PROJECT_ROOT}', root).replace('${CLAUDE_PROJECT_DIR}', root)


def under(path: str, root: str) -> bool:
    p, r = norm(path), norm(root)
    return p == r or p.startswith(r + '/')


def rel_to(path: str, root: str) -> str | None:
    p, r = norm(path), norm(root)
    if p == r:
        return ''
    if p.startswith(r + '/'):
        return p[len(r)+1:]
    return None


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding='utf-8')), None
    except Exception as exc:
        return None, str(exc)


def extract_path(tool_name: str, tool_input: dict[str, Any]) -> str | None:
    if tool_name in {'Write', 'Edit'}:
        return tool_input.get('file_path') or tool_input.get('path')
    if tool_name == 'NotebookEdit':
        return tool_input.get('notebook_path')
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception as exc:
        print(f'PD safety hook parse failure: {exc}', file=sys.stderr)
        return 2

    tool_name = str(event.get('tool_name', ''))
    tool_input = event.get('tool_input') or {}
    cwd = str(event.get('cwd') or os.getcwd())
    project_root = os.environ.get('CLAUDE_PROJECT_DIR', cwd)

    policy, policy_error = load_json(Path(project_root) / '.claude' / 'pd-safety-policy.json')
    if policy_error or policy is None:
        emit('deny', 'PD safety policy is missing or invalid; write/command tools fail closed.', policy_error)
        return 0

    protected = [expand(p, project_root) for p in policy.get('protected_paths', [])]
    external = [expand(p, project_root) for p in policy.get('approved_external_write_roots', [])]

    direct_path = extract_path(tool_name, tool_input)
    if direct_path:
        if any(under(direct_path, p) for p in protected):
            emit('deny', f'Protected path cannot be edited: {direct_path}')
            return 0
        relative = rel_to(direct_path, project_root)
        if relative is None:
            if not any(under(direct_path, p) for p in external):
                emit('ask', f'Write outside repository/approved roots requires approval: {direct_path}')
            return 0

        state, state_error = load_json(Path(project_root) / 'docs' / 'pd-visual-system' / 'PHASE_STATE.json')
        if state_error or state is None:
            emit('deny', 'PHASE_STATE is missing or invalid; repository edits fail closed.', state_error)
            return 0
        phase = state.get('current_phase')
        allowed = policy.get('phase_repository_write_allow', {}).get(phase)
        if not allowed:
            emit('deny', f'No repository write policy is defined for current phase {phase}.')
            return 0
        if not any(under(relative, root) for root in allowed):
            emit('ask', f'Path is outside the declared write scope for {phase}: {relative}',
                 'Confirm this file is necessary for the current phase, update the phase report, and record rollback.')
            return 0
        return 0

    if tool_name not in {'Bash', 'PowerShell'}:
        return 0

    command = str(tool_input.get('command', ''))
    for pattern in policy.get('deny_command_regex', []):
        if re.search(pattern, command):
            emit('deny', f'Destructive command blocked by PD policy: {command[:240]}')
            return 0

    command_norm = norm(command)
    mentions_protected = any(norm(p) in command_norm for p in protected)
    overwrite_capable = bool(re.search(
        r'(?i)(?:\brm\b|\bdel\b|\berase\b|\brmdir\b|\bremove-item\b|\bmove-item\b|\bmv\b|'
        r'\brename-item\b|\bren\b|\s-y(?:\s|$)|>|out-file|set-content|copy-item)', command))
    if mentions_protected and overwrite_capable:
        emit('deny', 'An overwrite/destructive command targets protected media, baseline, or Git data.')
        return 0

    for pattern in policy.get('ask_command_regex', []):
        if re.search(pattern, command):
            emit('ask', 'This operation requires explicit approval under the PD phase/safety policy.',
                 'State purpose, current phase, affected files, size/cost, license, rollback, and alternatives.')
            return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## 44.8 `config/pd-visual-system/component-registry.json`

```json
{
  "schema_version": "2.0.0",
  "core_components": [
    {
      "name": "EvidenceReveal",
      "verb": "Reveal",
      "purpose": "実在資料、証拠、写真、記録の全体から核心へ段階的に視線を移す。",
      "modes": [
        "document",
        "photograph",
        "record",
        "exhibit"
      ],
      "required_props": [
        "asset",
        "focusRegions",
        "sourceLabel",
        "revealSequence"
      ],
      "tests": [
        "5/8/12秒",
        "長文引用",
        "focusRegion画面外",
        "素材欠損",
        "出典ラベル"
      ]
    },
    {
      "name": "PenaltyVsProperty",
      "verb": "Compare",
      "purpose": "金額、罰金、財産、人数、判決前後などを共通軸で段階比較する。",
      "modes": [
        "currency",
        "generic",
        "before_after",
        "ratio"
      ],
      "required_props": [
        "left",
        "right",
        "comparisonAxis",
        "sourceLabel"
      ],
      "tests": [
        "単位一致",
        "負数/ゼロ",
        "大数表記",
        "比率精度",
        "左右長文"
      ]
    },
    {
      "name": "CaseJourney",
      "verb": "Trace",
      "purpose": "事件、裁判所、日付、場所の経路を現在地を一つに保って示す。",
      "modes": [
        "timeline",
        "court_hierarchy",
        "map_route",
        "procedural_path"
      ],
      "required_props": [
        "nodes",
        "activeNode",
        "direction"
      ],
      "tests": [
        "3/5/8ノード",
        "同日イベント",
        "長い裁判所名",
        "欠損日付",
        "VFR無関係"
      ]
    },
    {
      "name": "QuoteUnderExamination",
      "verb": "Isolate",
      "purpose": "長い資料から正確な一文または語句を抽出し、文脈と出典を保って読ませる。",
      "modes": [
        "holding",
        "dissent",
        "statute",
        "testimony"
      ],
      "required_props": [
        "quote",
        "source",
        "emphasisRanges"
      ],
      "tests": [
        "引用一致",
        "省略記号",
        "強調範囲",
        "長文wrap",
        "引用改変検知"
      ]
    },
    {
      "name": "VerdictReversal",
      "verb": "Overturn",
      "purpose": "旧判断と新判断の差、変わった点、変わらない点を順に示す。",
      "modes": [
        "court_reversal",
        "rule_change",
        "burden_shift"
      ],
      "required_props": [
        "beforeDecision",
        "afterDecision",
        "changed",
        "unchanged"
      ],
      "tests": [
        "完全逆転",
        "一部変更",
        "差戻し",
        "長文理由",
        "色だけに依存しない"
      ]
    }
  ],
  "expansion_components": [
    {
      "name": "CaseNetwork",
      "verb": "Connect",
      "purpose": "人物、組織、証拠、資金の関係を一つずつ構築する。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "RuleBoundary",
      "verb": "Constrain/Classify",
      "purpose": "原則、許容範囲、禁止範囲、例外を整理する。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "ImpactExpansion",
      "verb": "Expand",
      "purpose": "個別事件から他州、他事件、一般市民への影響を根拠付きで広げる。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "CaseResolution",
      "verb": "Resolve",
      "purpose": "冒頭の問いへ答え、条件と残る問題を返す。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "ParallaxStill",
      "verb": "Reconstruct/Isolate",
      "purpose": "静止画へ弱い奥行きと視線誘導を加える。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "InvestigativeMapRoute",
      "verb": "Trace",
      "purpose": "場所、移動、距離、管轄を正確な地図で示す。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "ChapterTransition",
      "verb": "Resolve/Reveal",
      "purpose": "前章を閉じ、次の問いを2〜4秒で提示する。",
      "status": "deferred_until_need_is_proven"
    },
    {
      "name": "IncidentReconstruction",
      "verb": "Reconstruct",
      "purpose": "既知事実と推測を分けた簡略空間再現を行う。",
      "status": "deferred_until_need_is_proven"
    }
  ],
  "aliases": {
    "DocumentReveal": {
      "canonical": "EvidenceReveal",
      "mode": "document"
    },
    "LegalTimeline": {
      "canonical": "CaseJourney",
      "mode": "timeline"
    },
    "CourtHierarchy": {
      "canonical": "CaseJourney",
      "mode": "court_hierarchy"
    },
    "MapRoute": {
      "canonical": "InvestigativeMapRoute",
      "mode": null
    },
    "ComparisonSplit": {
      "canonical": "PenaltyVsProperty",
      "mode": "generic"
    },
    "EvidenceBoard": {
      "canonical": "CaseNetwork",
      "mode": "evidence_board"
    },
    "LegalClassification": {
      "canonical": "RuleBoundary",
      "mode": "classification"
    },
    "DataCounter": {
      "canonical": "MetricCounterPrimitive",
      "mode": null
    },
    "CaseFileStack": {
      "canonical": "EvidenceReveal",
      "mode": "file_stack"
    },
    "RedactionReveal": {
      "canonical": "EvidenceReveal",
      "mode": "redaction"
    },
    "SurveillanceFrame": {
      "canonical": "EvidenceReveal",
      "mode": "surveillance_record"
    },
    "StakesEscalation": {
      "canonical": "ImpactExpansion",
      "mode": "stakes"
    },
    "Dramatization": {
      "canonical": "IncidentReconstruction",
      "mode": "dramatization"
    }
  },
  "rules": {
    "initial_implementation_count": 5,
    "one_primary_visual_verb_per_scene": true,
    "no_new_component_without_gap_report": true,
    "aliases_must_not_create_duplicate_components": true
  },
  "primitives": [
    {
      "name": "MetricCounterPrimitive",
      "purpose": "数値の決定論的な表示・更新を提供する内部primitive。"
    },
    {
      "name": "SourceLabel",
      "purpose": "出典、資料種別、再現ラベルを表示する内部primitive。"
    },
    {
      "name": "FocusRegion",
      "purpose": "資料内の注目領域を安全に強調する内部primitive。"
    },
    {
      "name": "ConnectorLine",
      "purpose": "因果、対応、移動を示す内部primitive。"
    },
    {
      "name": "WordCue",
      "purpose": "ナレーション語タイミングをframe eventへ変換する内部primitive。"
    },
    {
      "name": "SafeTextBlock",
      "purpose": "長い英語文、引用、固有名詞をsafe area内へ収める内部primitive。"
    },
    {
      "name": "SeededNoise",
      "purpose": "再現可能な質感・微動を提供する内部primitive。"
    },
    {
      "name": "DisclosureBadge",
      "purpose": "AI/3D再現や出典種別を必要に応じ表示する内部primitive。"
    }
  ]
}
```

## 44.9 `config/pd-visual-system/phase-registry.json`

```json
{
  "schema_version": "2.0.0",
  "phases": [
    {
      "id": "P00",
      "slug": "audit",
      "name": "環境・リポジトリ監査",
      "objective": "PC、Git、Remotion、FFmpeg、対象エピソード、素材ルートを読み取り中心で監査し、安全な実装境界を確定する。"
    },
    {
      "id": "P01",
      "slug": "baseline",
      "name": "Baseline保存・紙芝居診断",
      "objective": "対象エピソードから比較価値の高い連続60〜90秒を選び、現在版を保存して紙芝居要因を測定する。"
    },
    {
      "id": "P02",
      "slug": "benchmark",
      "name": "参照チャンネルのショット分解",
      "objective": "成功チャンネルの外見ではなく、ショット単位の情報設計、タイミング、音、再利用原理を観察記録する。"
    },
    {
      "id": "P03",
      "slug": "asset-index",
      "name": "素材インデックス最小実証",
      "objective": "100〜500素材に限定し、ffprobe、PySceneDetect、3点サンプリング、SQLite、再開可能処理を検証する。"
    },
    {
      "id": "P04",
      "slug": "semantic-search",
      "name": "意味検索の最小実証",
      "objective": "商用条件を記録した埋め込みモデルで、20クエリの検索品質を人間評価する。"
    },
    {
      "id": "P05",
      "slug": "motion-core",
      "name": "Remotionコア5部品",
      "objective": "EvidenceReveal、PenaltyVsProperty、CaseJourney、QuoteUnderExamination、VerdictReversalだけを高品質に実装する。"
    },
    {
      "id": "P06",
      "slug": "build-b1",
      "name": "B1コア改善版",
      "objective": "新ツールを増やさず、既存素材検索とコア5部品だけでbaseline区間を改善する。"
    },
    {
      "id": "P07",
      "slug": "audio-sync",
      "name": "WhisperX同期・B2版",
      "objective": "英語ナレーションを台本へ整列し、重要語・資料・SFXを単語単位で同期する。"
    },
    {
      "id": "P08",
      "slug": "parallax",
      "name": "2.5D・B3版",
      "objective": "静止画1枚だけで、明示的対象指定、SAM2、Depth Anything V2 Small、弱いパララックスを実証する。"
    },
    {
      "id": "P09",
      "slug": "evidence-room",
      "name": "PD Evidence Room・C1版",
      "objective": "再利用可能なBlenderセットを最小構成で作り、限定カメラ1カットを追加する。"
    },
    {
      "id": "P10",
      "slug": "ai-broll",
      "name": "AI B-roll・C2版",
      "objective": "既存素材で埋まらない1カットだけをComfyUI＋承認済みモデルで生成し、品質・時間・リスクを測る。"
    },
    {
      "id": "P11",
      "slug": "finishing",
      "name": "音響・カラー・C3版",
      "objective": "音響、章転換、カラー、ラウドネスを追加し、C2との差だけを評価する。"
    },
    {
      "id": "P12",
      "slug": "decision-rollout",
      "name": "投資判断・全編展開",
      "objective": "A/B1/B2/B3/C1/C2/C3の増分比較から、標準構成と不採用技術を決め、勝った方式だけを全編へ展開する。"
    }
  ],
  "transition_policy": {
    "automatic_phase_advance": false,
    "completion_state": "candidate_complete",
    "human_approval_required_to_advance": true
  }
}
```

## 44.10 `config/pd-visual-system/quality-gates.json`

```json
{
  "schema_version": "2.0.0",
  "preview": {
    "width": 1280,
    "height": 720,
    "fps": 30,
    "max_duration_sec": 90
  },
  "scene": {
    "max_static_no_semantic_change_sec": 3.5,
    "max_consecutive_same_component": 2,
    "max_asset_reuse_in_test_segment": 2,
    "max_parallax_displacement_px_1080p": 40,
    "safe_area_percent": 5,
    "max_primary_visual_verbs": 1,
    "max_secondary_visual_verbs": 1
  },
  "asset": {
    "min_width": 1280,
    "min_height": 720,
    "warn_upscale_ratio": 1.5,
    "require_license_decision": true,
    "require_provenance": true
  },
  "audio": {
    "target_lufs": null,
    "target_lufs_reason": "既存PDルールと実測を確認するまで固定しない",
    "max_true_peak_dbtp": -1.0,
    "detect_silence": true
  },
  "release_blockers": [
    "missing_asset",
    "license_review_required",
    "ai_review_pending",
    "provenance_missing",
    "disclosure_undecided",
    "render_corruption"
  ]
}
```

## 44.11 `config/pd-visual-system/tool-registry.json`

```json
{
  "schema_version": "2.0.0",
  "tools": [
    {
      "id": "remotion",
      "required": true,
      "interface": [
        "node",
        "cli"
      ],
      "phase": "P00",
      "name": "Remotion",
      "purpose": "既存プロジェクト内で情報アニメーションと全体編集を行う。",
      "license_gate": "既存package/lockfileを正本としP00でversion確認",
      "license_state": "project"
    },
    {
      "id": "ffmpeg",
      "required": true,
      "interface": [
        "cli"
      ],
      "phase": "P00",
      "name": "FFmpeg/ffprobe",
      "purpose": "非破壊変換、probe、黒/無音/破損検査を行う。",
      "license_gate": "公式buildと既存導入をP00で確認",
      "license_state": "project"
    },
    {
      "id": "pyscenedetect",
      "required": false,
      "interface": [
        "python",
        "cli"
      ],
      "phase": "P03",
      "name": "PySceneDetect",
      "purpose": "長い動画を論理カットへ分け、素材発見可能性を上げる。",
      "license_gate": "code/version/licenseをP03前に記録",
      "license_state": "review_required"
    },
    {
      "id": "semantic_embedding",
      "required": false,
      "interface": [
        "python"
      ],
      "phase": "P04",
      "checkpoint_license_gate": true,
      "name": "OpenCLIP-compatible embedding",
      "purpose": "3点サンプルとmetadataを意味検索する。",
      "license_gate": "codeとcheckpointを分離監査",
      "license_state": "review_required"
    },
    {
      "id": "whisperx",
      "required": false,
      "interface": [
        "python",
        "cli"
      ],
      "phase": "P07",
      "alignment_model_license_gate": true,
      "name": "WhisperX",
      "purpose": "ナレーションと正本台本を単語単位で整列する。",
      "license_gate": "code/checkpoint/alignment modelを分離監査",
      "license_state": "review_required"
    },
    {
      "id": "sam2",
      "required": false,
      "interface": [
        "python"
      ],
      "phase": "P08",
      "name": "SAM2",
      "purpose": "明示されたbox/pointの対象マスクを生成する。",
      "license_gate": "code/checkpointを分離監査",
      "license_state": "review_required"
    },
    {
      "id": "depth_anything_v2_small",
      "required": false,
      "interface": [
        "python"
      ],
      "phase": "P08",
      "model_variant_locked": "Small",
      "name": "Depth Anything V2 Small",
      "purpose": "静止画の弱い2.5D奥行きを作る。",
      "license_gate": "Smallだけを候補とし導入時再監査",
      "license_state": "review_required"
    },
    {
      "id": "blender",
      "required": false,
      "interface": [
        "python",
        "cli"
      ],
      "phase": "P09",
      "name": "Blender",
      "purpose": "再利用可能なPD Evidence RoomをCLI/Pythonでレンダーする。",
      "license_gate": "公式配布とaddonを個別監査",
      "license_state": "review_required"
    },
    {
      "id": "comfyui",
      "required": false,
      "interface": [
        "http"
      ],
      "phase": "P10",
      "name": "ComfyUI",
      "purpose": "承認済み生成workflowをローカルHTTP APIで実行する。",
      "license_gate": "code/custom nodeを分離監査",
      "license_state": "review_required"
    },
    {
      "id": "video_model",
      "required": false,
      "interface": [
        "comfyui"
      ],
      "phase": "P10",
      "model_license_gate": true,
      "name": "Approved video checkpoint",
      "purpose": "既存素材で埋まらない短いB-rollだけを生成する。",
      "license_gate": "exact checkpoint/output termsを監査",
      "license_state": "review_required"
    },
    {
      "id": "davinci_resolve",
      "required": false,
      "interface": [
        "python",
        "lua"
      ],
      "phase": "P11",
      "name": "DaVinci Resolve",
      "purpose": "必要な場合だけ公式Scripting APIで仕上げを補助する。",
      "license_gate": "edition/API差をP11で実機確認",
      "license_state": "review_required"
    }
  ]
}
```

## 44.12 `schemas/scene-plan.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/scene-plan.schema.json",
  "title": "PD Scene Plan",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "episode_id",
    "scene_id",
    "start_sec",
    "duration_sec",
    "narration",
    "visual_question",
    "visual_verb",
    "start_state",
    "end_state",
    "eye_target",
    "visual_strategy",
    "source_type",
    "truth_status",
    "license_status",
    "review_status",
    "provenance",
    "selected_assets",
    "sync_cues"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "episode_id": {
      "type": "string",
      "minLength": 1
    },
    "scene_id": {
      "type": "string",
      "pattern": "^SCN-[0-9]{3,}$"
    },
    "chapter_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "start_sec": {
      "type": "number",
      "minimum": 0
    },
    "duration_sec": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "narration": {
      "type": "string"
    },
    "narration_source": {
      "type": [
        "string",
        "null"
      ]
    },
    "visual_question": {
      "type": "string",
      "minLength": 1
    },
    "visual_verb": {
      "enum": [
        "reveal",
        "compare",
        "trace",
        "connect",
        "isolate",
        "reconstruct",
        "escalate",
        "overturn",
        "classify",
        "constrain",
        "expand",
        "resolve"
      ]
    },
    "secondary_visual_verb": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "reveal",
        "compare",
        "trace",
        "connect",
        "isolate",
        "reconstruct",
        "escalate",
        "overturn",
        "classify",
        "constrain",
        "expand",
        "resolve",
        null
      ]
    },
    "start_state": {
      "type": "string",
      "minLength": 1
    },
    "end_state": {
      "type": "string",
      "minLength": 1
    },
    "eye_target": {
      "type": "string",
      "minLength": 1
    },
    "narrative_goal": {
      "type": "string"
    },
    "visual_goal": {
      "type": "string"
    },
    "visual_strategy": {
      "enum": [
        "existing_video",
        "evidence_motion",
        "typography",
        "map_motion",
        "depth_parallax",
        "three_d_reconstruction",
        "ai_generated_broll",
        "ai_reenactment"
      ]
    },
    "source_type": {
      "enum": [
        "verified_evidence",
        "documentary_source_media",
        "licensed_broll",
        "illustrative_animation",
        "three_d_reconstruction",
        "ai_generated_broll",
        "ai_reenactment"
      ]
    },
    "truth_status": {
      "enum": [
        "verified",
        "corroborated",
        "unverified",
        "not_applicable",
        "prohibited"
      ]
    },
    "asset_queries": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "asset_candidates": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "selected_assets": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "motion_component": {
      "enum": [
        "EvidenceReveal",
        "PenaltyVsProperty",
        "CaseJourney",
        "QuoteUnderExamination",
        "VerdictReversal",
        "CaseNetwork",
        "RuleBoundary",
        "ImpactExpansion",
        "CaseResolution",
        "ParallaxStill",
        "InvestigativeMapRoute",
        "ChapterTransition",
        "IncidentReconstruction",
        null
      ]
    },
    "motion_mode": {
      "type": [
        "string",
        "null"
      ]
    },
    "motion_parameters": {
      "type": "object"
    },
    "text_elements": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "overlays": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "sound_cues": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "sync_cues": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "token",
          "requires_review"
        ],
        "properties": {
          "token": {
            "type": "string"
          },
          "script_occurrence": {
            "type": [
              "integer",
              "null"
            ],
            "minimum": 1
          },
          "expected_start_sec": {
            "type": [
              "number",
              "null"
            ],
            "minimum": 0
          },
          "matched_start_sec": {
            "type": [
              "number",
              "null"
            ],
            "minimum": 0
          },
          "confidence": {
            "type": [
              "number",
              "null"
            ],
            "minimum": 0,
            "maximum": 1
          },
          "requires_review": {
            "type": "boolean"
          },
          "review_reason": {
            "type": [
              "string",
              "null"
            ]
          }
        }
      }
    },
    "generation_request_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "license_status": {
      "enum": [
        "approved",
        "review_required",
        "rejected",
        "not_applicable"
      ]
    },
    "disclosure": {
      "type": [
        "object",
        "null"
      ],
      "properties": {
        "youtube_ai_use": {
          "enum": [
            "yes",
            "no",
            "undecided"
          ]
        },
        "on_screen_label": {
          "type": [
            "string",
            "null"
          ]
        },
        "reason": {
          "type": "string"
        }
      },
      "required": [
        "youtube_ai_use",
        "reason"
      ],
      "additionalProperties": false
    },
    "review_status": {
      "enum": [
        "pending",
        "approved",
        "rejected",
        "revise"
      ]
    },
    "provenance": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "claim_or_asset",
          "source"
        ],
        "properties": {
          "claim_or_asset": {
            "type": "string"
          },
          "source": {
            "type": "string"
          },
          "accessed_at": {
            "type": [
              "string",
              "null"
            ]
          },
          "notes": {
            "type": "string"
          }
        }
      }
    },
    "qc_rules": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "notes": {
      "type": "string"
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "source_type": {
            "enum": [
              "ai_generated_broll",
              "ai_reenactment"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "license_status": {
            "not": {
              "const": "not_applicable"
            }
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "source_type": {
            "const": "verified_evidence"
          }
        }
      },
      "then": {
        "properties": {
          "truth_status": {
            "enum": [
              "verified",
              "corroborated"
            ]
          }
        }
      }
    }
  ]
}
```

## 44.13 `schemas/asset-record.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/asset-record.schema.json",
  "title": "PD Asset Record",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "asset_id",
    "absolute_path",
    "media_type",
    "file_hash",
    "read_only_source",
    "license_decision",
    "source_type"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "asset_id": {
      "type": "string",
      "minLength": 1
    },
    "absolute_path": {
      "type": "string",
      "minLength": 1
    },
    "relative_path": {
      "type": [
        "string",
        "null"
      ]
    },
    "file_hash": {
      "type": "string",
      "minLength": 1
    },
    "hash_algorithm": {
      "type": "string",
      "default": "sha256"
    },
    "read_only_source": {
      "const": true
    },
    "media_type": {
      "enum": [
        "video",
        "image",
        "audio",
        "document",
        "other"
      ]
    },
    "extension": {
      "type": [
        "string",
        "null"
      ]
    },
    "width": {
      "type": [
        "integer",
        "null"
      ],
      "minimum": 0
    },
    "height": {
      "type": [
        "integer",
        "null"
      ],
      "minimum": 0
    },
    "duration_sec": {
      "type": [
        "number",
        "null"
      ],
      "minimum": 0
    },
    "avg_frame_rate": {
      "type": [
        "string",
        "null"
      ]
    },
    "r_frame_rate": {
      "type": [
        "string",
        "null"
      ]
    },
    "time_base": {
      "type": [
        "string",
        "null"
      ]
    },
    "start_pts": {
      "type": [
        "integer",
        "null"
      ]
    },
    "end_pts": {
      "type": [
        "integer",
        "null"
      ]
    },
    "scene_start_sec": {
      "type": [
        "number",
        "null"
      ],
      "minimum": 0
    },
    "scene_end_sec": {
      "type": [
        "number",
        "null"
      ],
      "minimum": 0
    },
    "audio_channels": {
      "type": [
        "integer",
        "null"
      ],
      "minimum": 0
    },
    "file_size_bytes": {
      "type": [
        "integer",
        "null"
      ],
      "minimum": 0
    },
    "sample_frames": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "relative_position",
          "timestamp_sec",
          "path"
        ],
        "properties": {
          "relative_position": {
            "enum": [
              0.25,
              0.5,
              0.75
            ]
          },
          "timestamp_sec": {
            "type": "number",
            "minimum": 0
          },
          "pts": {
            "type": [
              "integer",
              "null"
            ]
          },
          "path": {
            "type": "string"
          }
        }
      }
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "description": {
      "type": "string"
    },
    "ocr_text": {
      "type": [
        "string",
        "null"
      ]
    },
    "transcript_text": {
      "type": [
        "string",
        "null"
      ]
    },
    "embedding_records": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "model",
          "checkpoint",
          "license_decision",
          "vector_ref"
        ],
        "properties": {
          "model": {
            "type": "string"
          },
          "checkpoint": {
            "type": "string"
          },
          "checkpoint_hash": {
            "type": [
              "string",
              "null"
            ]
          },
          "license_decision": {
            "enum": [
              "approved",
              "review_required",
              "rejected",
              "not_applicable"
            ]
          },
          "vector_ref": {
            "type": "string"
          },
          "created_at": {
            "type": [
              "string",
              "null"
            ]
          }
        }
      }
    },
    "source_type": {
      "enum": [
        "verified_evidence",
        "documentary_source_media",
        "licensed_broll",
        "illustrative_animation",
        "three_d_reconstruction",
        "ai_generated_broll",
        "ai_reenactment"
      ]
    },
    "truth_status": {
      "enum": [
        "verified",
        "corroborated",
        "unverified",
        "not_applicable",
        "prohibited"
      ]
    },
    "source_name": {
      "type": [
        "string",
        "null"
      ]
    },
    "source_url": {
      "type": [
        "string",
        "null"
      ]
    },
    "license_record_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "commercial_use": {
      "enum": [
        "allowed",
        "restricted",
        "unknown"
      ]
    },
    "attribution_required": {
      "type": [
        "boolean",
        "null"
      ]
    },
    "license_decision": {
      "enum": [
        "approved",
        "review_required",
        "rejected",
        "not_applicable"
      ]
    },
    "quality_score": {
      "type": [
        "number",
        "null"
      ],
      "minimum": 0,
      "maximum": 100
    },
    "usage_count": {
      "type": "integer",
      "minimum": 0
    },
    "last_used_episode": {
      "type": [
        "string",
        "null"
      ]
    },
    "probe_error": {
      "type": [
        "string",
        "null"
      ]
    },
    "created_at": {
      "type": [
        "string",
        "null"
      ]
    },
    "updated_at": {
      "type": [
        "string",
        "null"
      ]
    }
  }
}
```

## 44.14 `schemas/generation-request.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/generation-request.schema.json",
  "title": "PD Generation Request",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "request_id",
    "scene_id",
    "purpose",
    "source_type",
    "model_family",
    "checkpoint",
    "workflow_version",
    "prompt",
    "seed",
    "license_decision",
    "human_review_required",
    "review_status"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "request_id": {
      "type": "string"
    },
    "scene_id": {
      "type": "string"
    },
    "purpose": {
      "enum": [
        "atmospheric_broll",
        "environment_motion",
        "location_representation",
        "reenactment"
      ]
    },
    "source_type": {
      "enum": [
        "ai_generated_broll",
        "ai_reenactment"
      ]
    },
    "model_family": {
      "type": "string"
    },
    "checkpoint": {
      "type": "string"
    },
    "checkpoint_hash": {
      "type": [
        "string",
        "null"
      ]
    },
    "model_license_record_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "workflow_version": {
      "type": "string"
    },
    "workflow_path": {
      "type": [
        "string",
        "null"
      ]
    },
    "input_image": {
      "type": [
        "string",
        "null"
      ]
    },
    "prompt": {
      "type": "string",
      "minLength": 1
    },
    "negative_prompt": {
      "type": "string"
    },
    "seed": {
      "type": "integer"
    },
    "width": {
      "type": "integer",
      "minimum": 1
    },
    "height": {
      "type": "integer",
      "minimum": 1
    },
    "frames": {
      "type": "integer",
      "minimum": 1
    },
    "fps": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "steps": {
      "type": "integer",
      "minimum": 1
    },
    "cfg": {
      "type": "number",
      "minimum": 0
    },
    "license_decision": {
      "enum": [
        "review_required",
        "approved",
        "rejected"
      ]
    },
    "disclosure_candidate": {
      "type": "boolean"
    },
    "human_review_required": {
      "const": true
    },
    "review_status": {
      "enum": [
        "pending",
        "approved",
        "rejected",
        "revise"
      ]
    },
    "output_paths": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "runtime": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "started_at": {
          "type": [
            "string",
            "null"
          ]
        },
        "ended_at": {
          "type": [
            "string",
            "null"
          ]
        },
        "duration_sec": {
          "type": [
            "number",
            "null"
          ],
          "minimum": 0
        },
        "peak_vram_mb": {
          "type": [
            "number",
            "null"
          ],
          "minimum": 0
        },
        "return_code": {
          "type": [
            "integer",
            "null"
          ]
        },
        "error": {
          "type": [
            "string",
            "null"
          ]
        }
      }
    }
  }
}
```

## 44.15 `schemas/narration-alignment.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/narration-alignment.schema.json",
  "title": "PD Narration Alignment",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "episode_id",
    "audio_path",
    "script_path",
    "language",
    "tool",
    "words",
    "script_diff",
    "numeric_tokens_for_review"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "episode_id": {
      "type": "string"
    },
    "audio_path": {
      "type": "string"
    },
    "audio_hash": {
      "type": [
        "string",
        "null"
      ]
    },
    "script_path": {
      "type": "string"
    },
    "script_hash": {
      "type": [
        "string",
        "null"
      ]
    },
    "language": {
      "const": "en"
    },
    "tool": {
      "const": "whisperx"
    },
    "tool_version": {
      "type": "string"
    },
    "asr_model": {
      "type": "string"
    },
    "alignment_model": {
      "type": "string"
    },
    "alignment_license_record_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "words": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "text",
          "normalized",
          "start_sec",
          "end_sec",
          "requires_review"
        ],
        "properties": {
          "text": {
            "type": "string"
          },
          "normalized": {
            "type": "string"
          },
          "start_sec": {
            "type": "number",
            "minimum": 0
          },
          "end_sec": {
            "type": "number",
            "minimum": 0
          },
          "confidence": {
            "type": [
              "number",
              "null"
            ],
            "minimum": 0,
            "maximum": 1
          },
          "script_token_index": {
            "type": [
              "integer",
              "null"
            ],
            "minimum": 0
          },
          "requires_review": {
            "type": "boolean"
          },
          "review_reason": {
            "type": [
              "string",
              "null"
            ]
          }
        }
      }
    },
    "script_diff": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "numeric_tokens_for_review": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "created_at": {
      "type": [
        "string",
        "null"
      ]
    }
  }
}
```

## 44.16 `schemas/benchmark-shot.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/benchmark-shot.schema.json",
  "title": "PD Benchmark Shot Observation",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "record_id",
    "channel",
    "video_url",
    "timestamp_start",
    "timestamp_end",
    "narrative_function",
    "visual_question",
    "visual_verb",
    "start_state",
    "end_state",
    "layers",
    "lesson",
    "copy_boundary"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "record_id": {
      "type": "string"
    },
    "channel": {
      "type": "string"
    },
    "video_title": {
      "type": [
        "string",
        "null"
      ]
    },
    "video_url": {
      "type": "string"
    },
    "observed_at": {
      "type": [
        "string",
        "null"
      ]
    },
    "timestamp_start": {
      "type": "string"
    },
    "timestamp_end": {
      "type": "string"
    },
    "shot_duration_sec": {
      "type": [
        "number",
        "null"
      ],
      "minimum": 0
    },
    "narrative_function": {
      "type": "string"
    },
    "visual_question": {
      "type": "string"
    },
    "visual_verb": {
      "enum": [
        "reveal",
        "compare",
        "trace",
        "connect",
        "isolate",
        "reconstruct",
        "escalate",
        "overturn",
        "classify",
        "constrain",
        "expand",
        "resolve"
      ]
    },
    "start_state": {
      "type": "string"
    },
    "end_state": {
      "type": "string"
    },
    "eye_target": {
      "type": [
        "string",
        "null"
      ]
    },
    "layers": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "camera": {
      "type": "object"
    },
    "text_timing": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "audio_events": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "lesson": {
      "type": "string",
      "minLength": 1
    },
    "reusable_principle": {
      "type": "string"
    },
    "copy_boundary": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "stored_copyrighted_media": {
      "const": false
    }
  }
}
```

## 44.17 `schemas/license-record.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/license-record.schema.json",
  "title": "PD License Record",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "record_id",
    "subject_name",
    "artifact_type",
    "commercial_use",
    "decision",
    "reviewed_at",
    "evidence_urls"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "record_id": {
      "type": "string",
      "minLength": 1
    },
    "subject_name": {
      "type": "string",
      "minLength": 1
    },
    "artifact_type": {
      "enum": [
        "code",
        "model_checkpoint",
        "alignment_model",
        "custom_node",
        "media_asset",
        "font",
        "music",
        "sfx",
        "other"
      ]
    },
    "version_or_hash": {
      "type": [
        "string",
        "null"
      ]
    },
    "source_url": {
      "type": [
        "string",
        "null"
      ]
    },
    "code_license": {
      "type": [
        "string",
        "null"
      ]
    },
    "artifact_license": {
      "type": [
        "string",
        "null"
      ]
    },
    "commercial_use": {
      "enum": [
        "allowed",
        "restricted",
        "unknown"
      ]
    },
    "revenue_restrictions": {
      "type": [
        "string",
        "null"
      ]
    },
    "territory_restrictions": {
      "type": [
        "string",
        "null"
      ]
    },
    "output_restrictions": {
      "type": [
        "string",
        "null"
      ]
    },
    "acceptable_use_restrictions": {
      "type": [
        "string",
        "null"
      ]
    },
    "attribution_required": {
      "type": [
        "boolean",
        "null"
      ]
    },
    "attribution_text": {
      "type": [
        "string",
        "null"
      ]
    },
    "decision": {
      "enum": [
        "approved",
        "review_required",
        "rejected",
        "not_applicable"
      ]
    },
    "reviewed_at": {
      "type": "string",
      "format": "date-time"
    },
    "reviewed_by": {
      "type": [
        "string",
        "null"
      ]
    },
    "evidence_urls": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "notes": {
      "type": "string"
    }
  }
}
```

## 44.18 `schemas/review-record.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/review-record.schema.json",
  "title": "PD Review Record",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "item_id",
    "reviewer",
    "status",
    "issues",
    "reviewed_at"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "item_id": {
      "type": "string"
    },
    "reviewer": {
      "type": "string"
    },
    "status": {
      "enum": [
        "approved",
        "rejected",
        "revise"
      ]
    },
    "issues": {
      "type": "array",
      "items": {
        "enum": [
          "face_artifact",
          "hand_artifact",
          "text_artifact",
          "edge_artifact",
          "background_hole",
          "historical_inaccuracy",
          "misleading_realism",
          "motion_inconsistency",
          "narration_mismatch",
          "license_unclear",
          "provenance_missing",
          "disclosure_required",
          "other"
        ]
      }
    },
    "notes": {
      "type": "string"
    },
    "reviewed_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

## 44.19 `schemas/qc-report.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/qc-report.schema.json",
  "title": "PD QC Report",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "job_id",
    "input_path",
    "release_ready",
    "hard_blockers",
    "warnings",
    "metrics"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "job_id": {
      "type": "string"
    },
    "input_path": {
      "type": "string"
    },
    "release_ready": {
      "type": "boolean"
    },
    "hard_blockers": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "warnings": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "metrics": {
      "type": "object"
    },
    "license_summary": {
      "type": "object"
    },
    "ai_review_summary": {
      "type": "object"
    },
    "disclosure_summary": {
      "type": "object"
    },
    "created_at": {
      "type": [
        "string",
        "null"
      ]
    }
  }
}
```

## 44.20 `schemas/phase-state.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/phase-state.schema.json",
  "title": "PD Phase State",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "system_version",
    "project_id",
    "episode_id",
    "current_phase",
    "phase_status",
    "active_variant",
    "history",
    "blockers",
    "assumptions"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0.0"
    },
    "system_version": {
      "type": "string"
    },
    "project_id": {
      "type": "string"
    },
    "episode_id": {
      "type": "string"
    },
    "current_phase": {
      "enum": [
        "P00",
        "P01",
        "P02",
        "P03",
        "P04",
        "P05",
        "P06",
        "P07",
        "P08",
        "P09",
        "P10",
        "P11",
        "P12"
      ]
    },
    "phase_status": {
      "enum": [
        "not_started",
        "in_progress",
        "blocked",
        "candidate_complete"
      ]
    },
    "human_approved_next_phase": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "P00",
        "P01",
        "P02",
        "P03",
        "P04",
        "P05",
        "P06",
        "P07",
        "P08",
        "P09",
        "P10",
        "P11",
        "P12",
        null
      ]
    },
    "active_variant": {
      "enum": [
        "A",
        "B1",
        "B2",
        "B3",
        "C1",
        "C2",
        "C3"
      ]
    },
    "last_updated": {
      "type": [
        "string",
        "null"
      ]
    },
    "updated_by": {
      "type": [
        "string",
        "null"
      ]
    },
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": true,
        "required": [
          "phase",
          "event",
          "at"
        ],
        "properties": {
          "phase": {
            "enum": [
              "P00",
              "P01",
              "P02",
              "P03",
              "P04",
              "P05",
              "P06",
              "P07",
              "P08",
              "P09",
              "P10",
              "P11",
              "P12"
            ]
          },
          "event": {
            "type": "string",
            "minLength": 1
          },
          "at": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": true,
        "required": [
          "phase",
          "reason",
          "at",
          "resolved"
        ],
        "properties": {
          "phase": {
            "enum": [
              "P00",
              "P01",
              "P02",
              "P03",
              "P04",
              "P05",
              "P06",
              "P07",
              "P08",
              "P09",
              "P10",
              "P11",
              "P12"
            ]
          },
          "reason": {
            "type": "string",
            "minLength": 1
          },
          "at": {
            "type": "string",
            "minLength": 1
          },
          "resolved": {
            "type": "boolean"
          },
          "resolution": {
            "type": "string"
          },
          "resolved_at": {
            "type": "string"
          }
        }
      }
    },
    "assumptions": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

## 44.21 `scripts/pd-visual-system/phase_gate.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

PHASES = [f'P{i:02d}' for i in range(13)]
STATUSES = {'not_started', 'in_progress', 'blocked', 'candidate_complete'}


def state_path(root: Path) -> Path:
    return root / 'docs' / 'pd-visual-system' / 'PHASE_STATE.json'


def load_state(root: Path) -> dict:
    path = state_path(root)
    if not path.exists():
        raise SystemExit(f'Phase state not found: {path}')
    state = json.loads(path.read_text(encoding='utf-8'))
    if state.get('current_phase') not in PHASES or state.get('phase_status') not in STATUSES:
        raise SystemExit('PHASE_STATE contains an invalid phase or status.')
    return state


def save_state(root: Path, state: dict) -> None:
    path = state_path(root)
    temp = path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def append(state: dict, event: str, **fields: object) -> None:
    state.setdefault('history', []).append({'phase': state['current_phase'], 'event': event, 'at': now(), **fields})
    state['last_updated'] = state['history'][-1]['at']


def cmd_assert(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase:
        raise SystemExit(f"Phase mismatch: state={state['current_phase']} requested={args.phase}. Do not skip phases.")
    if state['phase_status'] == 'blocked':
        raise SystemExit('Current phase is blocked. Resume it with documented resolution before continuing.')
    print(f"OK: {args.phase} is current; status={state['phase_status']}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase:
        raise SystemExit('Cannot start a non-current phase.')
    if state['phase_status'] not in {'not_started', 'in_progress'}:
        raise SystemExit(f"Cannot start from status {state['phase_status']}")
    state['phase_status'] = 'in_progress'
    state['updated_by'] = args.by
    append(state, 'started')
    save_state(args.project_root, state)
    print(f'Started {args.phase}')
    return 0


def cmd_block(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase or state['phase_status'] != 'in_progress':
        raise SystemExit('Only the current in-progress phase can be blocked.')
    state['phase_status'] = 'blocked'
    state.setdefault('blockers', []).append({'phase': args.phase, 'reason': args.reason, 'at': now(), 'resolved': False})
    state['updated_by'] = args.by
    append(state, 'blocked', reason=args.reason)
    save_state(args.project_root, state)
    print(f'Blocked {args.phase}')
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase or state['phase_status'] != 'blocked':
        raise SystemExit('Only the current blocked phase can be resumed.')
    unresolved = [b for b in state.get('blockers', []) if b.get('phase') == args.phase and not b.get('resolved')]
    if not unresolved:
        raise SystemExit('No unresolved blocker record exists.')
    for blocker in unresolved:
        blocker['resolved'] = True; blocker['resolution'] = args.resolution; blocker['resolved_at'] = now()
    state['phase_status'] = 'in_progress'
    state['updated_by'] = args.by
    append(state, 'resumed', resolution=args.resolution)
    save_state(args.project_root, state)
    print(f'Resumed {args.phase}')
    return 0


def cmd_candidate_complete(args: argparse.Namespace) -> int:
    state = load_state(args.project_root)
    if state['current_phase'] != args.phase:
        raise SystemExit('Cannot complete a non-current phase.')
    if state['phase_status'] != 'in_progress':
        raise SystemExit(f"candidate_complete requires in_progress, not {state['phase_status']}")
    evidence = args.evidence.resolve()
    try:
        evidence.relative_to(args.project_root)
    except ValueError:
        raise SystemExit('Evidence report must be inside the project repository.')
    if not evidence.is_file() or evidence.stat().st_size == 0:
        raise SystemExit(f'Evidence report is missing or empty: {evidence}')
    state['phase_status'] = 'candidate_complete'
    state['updated_by'] = args.by
    append(state, 'candidate_complete', evidence=str(evidence))
    save_state(args.project_root, state)
    print(f'Marked {args.phase} candidate_complete')
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    if not args.human_approved:
        raise SystemExit('Explicit --human-approved is required.')
    state = load_state(args.project_root)
    if state['phase_status'] != 'candidate_complete':
        raise SystemExit('Current phase must be candidate_complete before advancing.')
    current_index = PHASES.index(state['current_phase'])
    if current_index + 1 >= len(PHASES):
        raise SystemExit('Already at final phase.')
    expected = PHASES[current_index + 1]
    if args.to != expected:
        raise SystemExit(f'Next phase must be {expected}; requested {args.to}.')
    previous = state['current_phase']
    append(state, 'completed_and_advanced', next=args.to, approved_by=args.by)
    state['current_phase'] = args.to
    state['phase_status'] = 'not_started'
    state['human_approved_next_phase'] = args.to
    state['updated_by'] = args.by
    save_state(args.project_root, state)
    print(f'Advanced {previous} -> {args.to}')
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument('--project-root', type=Path, default=Path('.'))
    sub = p.add_subparsers(dest='command', required=True)
    q=sub.add_parser('assert'); q.add_argument('--phase',choices=PHASES,required=True); q.set_defaults(func=cmd_assert)
    q=sub.add_parser('start'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--by',default='claude-code'); q.set_defaults(func=cmd_start)
    q=sub.add_parser('block'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--reason',required=True); q.add_argument('--by',default='claude-code'); q.set_defaults(func=cmd_block)
    q=sub.add_parser('resume'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--resolution',required=True); q.add_argument('--by',default='human-via-claude-code'); q.set_defaults(func=cmd_resume)
    q=sub.add_parser('candidate-complete'); q.add_argument('--phase',choices=PHASES,required=True); q.add_argument('--evidence',type=Path,required=True); q.add_argument('--by',default='claude-code'); q.set_defaults(func=cmd_candidate_complete)
    q=sub.add_parser('advance'); q.add_argument('--to',choices=PHASES,required=True); q.add_argument('--human-approved',action='store_true'); q.add_argument('--by',default='human-via-claude-code'); q.set_defaults(func=cmd_advance)
    return p


if __name__ == '__main__':
    args=parser().parse_args(); args.project_root=args.project_root.resolve(); raise SystemExit(args.func(args))
```

## 44.22 `scripts/pd-visual-system/validate_examples.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

PAIRS = [
    ('templates/pd-visual-system/scene-plan.example.json', 'schemas/scene-plan.schema.json'),
    ('templates/pd-visual-system/asset-record.example.json', 'schemas/asset-record.schema.json'),
    ('templates/pd-visual-system/generation-request.example.json', 'schemas/generation-request.schema.json'),
    ('templates/pd-visual-system/review-record.example.json', 'schemas/review-record.schema.json'),
    ('templates/pd-visual-system/benchmark-shot.example.json', 'schemas/benchmark-shot.schema.json'),
    ('docs/pd-visual-system/PHASE_STATE.json', 'schemas/phase-state.schema.json'),
]

root = Path(__file__).resolve().parents[2]
for instance_rel, schema_rel in PAIRS:
    instance = json.loads((root / instance_rel).read_text(encoding='utf-8'))
    schema = json.loads((root / schema_rel).read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator(schema).validate(instance)
    print(f'OK {instance_rel}')
```

## 44.23 `.claude/rules/blender-evidence-room.md`

```markdown
---
paths:
  - "blender/**/*"
  - "**/*evidence*room*.py"
  - "**/*.blend.py"
---

# PD Evidence Room rules

- 目的は毎話再利用できる撮影セットであり、全編3D化ではない。
- 初期版は中央デスク、証拠ボード、地図モニター、判決文モニター、基本照明、3カメラだけ。
- P09初期は固定または正面モニターのカメラを優先する。
- カメラ移動中にRemotionで画面を貼る場合は、Blenderから四隅のscreen-space座標をフレームごとにJSON出力する。
- 追跡データがない場合、移動中のモニターへ2D文字を貼らない。
- 文字と実資料は原則Remotionで合成し、Blender内の読める偽資料を避ける。
- render script、seed、camera ID、frame range、Blender versionをmanifestへ保存する。
```

## 44.24 `.claude/rules/docs-state.md`

```markdown
---
paths:
  - "docs/pd-visual-system/**/*"
---

# State and documentation rules

- 実装済み、計画、仮定を同じ文で混ぜない。
- `PHASE_STATE.json`と`IMPLEMENTATION_STATUS.md`を同時に更新する。
- Phase完了は`candidate_complete`。ユーザーの明示操作なしで次Phaseへ進めない。
- 決定はDECISION_LOGへ、仮定はASSUMPTIONSへ、ライセンスはLICENSE_REGISTERへ残す。
- 日付、ツール版、コマンド、入力ハッシュ、出力、テスト、rollbackを記録する。
```

## 44.25 `.claude/rules/media-truth-license.md`

```markdown
---
paths:
  - "episodes/**/*"
  - "assets/**/*"
  - "schemas/**/*"
  - "config/pd-visual-system/**/*"
  - "scripts/**/*.{py,ts,js}"
  - "workflows/**/*"
---

# Media truth and license rules

- source_type、truth_status、license_decision、provenanceを別フィールドで管理する。
- 不明値は`unknown`または`review_required`。falseやapprovedへ推測変換しない。
- 実在資料と説明図と3D再現とAI映像を同じラベルで扱わない。
- AIで読める判決文、新聞、警察文書、証拠を生成しない。
- third-party checkpoint、alignment model、custom nodeも個別にライセンス記録する。
- 素材ルートは読み取り専用。派生物はgenerated/previews/indexes等へ新規出力する。
- AI/3D再現は既知事実と推測をmanifestへ分け、必要なら画面内ラベルとYouTube開示を設定する。
```

## 44.26 `.claude/rules/python-adapters.md`

```markdown
---
paths:
  - "scripts/**/*.py"
  - "tools/**/*.py"
  - "tests/**/*.py"
---

# Python adapter rules

- 一スクリプト一責務。`make_everything.py`型の巨大モノリスを作らない。
- CLIは`--dry-run`、`--output`、`--force`、`--resume`を必要に応じて持つ。
- `--force`なしで既存出力を上書きしない。
- subprocessは引数配列を使い、shell=Trueを避け、return code/stdout/stderr/versionsを記録する。
- Windowsの空白、日本語、ドライブ文字、長いパスをテストする。
- 大量処理はストリーミング、チャンク、checkpoint、差分更新を使う。
- 失敗した一素材で全体を停止せず、エラーをDB/manifestへ記録する。
- JSONは対応Schemaで検証し、schema_versionを持たせる。
```

## 44.27 `.claude/rules/remotion-motion.md`

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "packages/motion-library/**/*.{ts,tsx}"
  - "remotion/**/*.{ts,tsx}"
---

# Remotion motion rules

- 既存のfps、解像度、Root構成、レンダー方法を先に確認する。
- コア実装は5部品に限定し、alias名の別コンポーネントを増やさない。
- `useCurrentFrame()`、`useVideoConfig()`、`interpolate()`、`spring()`は決定論的に使う。
- ランダム値はseedをpropsで固定する。
- duration依存値は秒ではなくframesへ変換し、5/8/12秒で試す。
- 主要visual verb、visual question、start/end stateをデモデータへ記録する。
- 画面内の主役は原則一つ。全レイヤーを常時動かさない。
- テキストはセーフエリア、長文wrap、出典、単位、引用精度を守る。
- 欠損入力は明示的fallbackを出し、静かに誤った表示をしない。
- 特定事件名、競合チャンネル名、競合固有配色をコンポーネントへハードコードしない。
```

## 44.28 `.claude/agents/pd-asset-librarian.md`

```markdown
---
name: pd-asset-librarian
description: Read-only reviewer for asset indexing, scene sampling, semantic search quality, duplication, VFR timestamps, and media-root safety.
tools: Read, Grep, Glob, Bash
model: inherit
permissionMode: default
maxTurns: 20
---

Inspect indexing/search design without moving or rewriting source assets.

Check:
- source files remain read-only
- VFR stores time_base and PTS, not only average fps
- each detected scene has 25/50/75 percent sample frames
- hashes and incremental resume fields exist
- embedding checkpoint and license decision are recorded
- search evaluation includes failure cases and human relevance scores
```

## 44.29 `.claude/agents/pd-motion-reviewer.md`

```markdown
---
name: pd-motion-reviewer
description: Read-only reviewer for Remotion motion components, deterministic timing, text safety, visual grammar, and duplicate component design. Use after implementing or changing motion code.
tools: Read, Grep, Glob
model: inherit
permissionMode: plan
maxTurns: 20
---

Review the changed Remotion code against:
- core five component registry
- deterministic frame math and seeded randomness
- 5/8/12 second duration resilience
- 1920x1080 safe areas and long English text
- missing asset fallback
- one primary visual verb
- start/end state change
- no alias duplication
- no competitor-specific branding

Report blocking issues first, with exact file and line references when possible. Do not edit files.
```

## 44.30 `.claude/agents/pd-qc-reviewer.md`

```markdown
---
name: pd-qc-reviewer
description: Read-only final reviewer for preview manifests, ffprobe/FFmpeg QC outputs, missing assets, audio, black/silent frames, license gates, and AI review state.
tools: Read, Grep, Glob, Bash
model: inherit
permissionMode: default
maxTurns: 20
---

Do not modify media or source files. Read existing QC artifacts and, when permitted, run read-only ffprobe/FFmpeg detection commands.

Release must be false when any of these exist:
- missing asset
- license review required
- AI review pending
- provenance missing
- disclosure undecided
- corrupted render

Separate hard blockers, warnings, and aesthetic suggestions.
```

## 44.31 `.claude/agents/pd-truth-license-auditor.md`

```markdown
---
name: pd-truth-license-auditor
description: Read-only auditor for media provenance, model/checkpoint licenses, AI disclosure, and release blockers. Use before installing a model or approving a generated/reconstructed shot.
tools: Read, Grep, Glob, WebSearch, WebFetch
model: inherit
permissionMode: plan
maxTurns: 24
---

You audit code, model weights, alignment models, custom nodes, media assets, and output restrictions separately.

Rules:
- Use primary official sources whenever available.
- Never infer commercial permission from an open-source code license alone.
- Unknown means review_required, not approved.
- Identify territory, revenue, attribution, output, and acceptable-use restrictions.
- Distinguish ai_generated_broll from ai_reenactment.
- Return a license record compatible with schemas/license-record.schema.json.
- Do not edit files or approve publication.
```

## 44.32 `.claude/agents/pd-visual-director.md`

```markdown
---
name: pd-visual-director
description: Read-only reviewer that diagnoses whether each shot changes viewer understanding, assigns a visual verb, and identifies unnecessary motion. Use before or after a 60-90 second preview.
tools: Read, Grep, Glob
model: inherit
permissionMode: plan
maxTurns: 20
---

You are the Prime Documentary visual director. Do not edit files.

For every reviewed scene, report:
1. visual question
2. start state
3. end state
4. one primary visual verb
5. eye target
6. semantic change over time
7. decorative motion to remove
8. cheapest reusable way to improve it
9. truth/source-type risk
10. confidence and missing evidence

Prefer clarity and causal understanding over animation density. Never recommend copying a reference channel's signature look.
```

## 44.33 `.claude/skills/pd-license-audit/SKILL.md`

```markdown
---
name: pd-license-audit
description: Audit a proposed tool, code repository, checkpoint, alignment model, custom node, or media asset before installation or production use.
argument-hint: "[tool/model/asset]"
disable-model-invocation: true
---

# License audit

Audit `$ARGUMENTS` using primary official sources.

Record separately:
- code repository and code license
- exact model/checkpoint and hash
- checkpoint/model license
- training/data caveats if officially documented
- custom nodes and dependencies
- output-use restrictions
- commercial, revenue, territory, attribution, and acceptable-use restrictions
- source URLs and review date

Create or update an entry compatible with `schemas/license-record.schema.json`.

Never output `approved` when any material field is unknown or conflicting. Use `review_required` and state the missing evidence.
```

## 44.34 `.claude/skills/pd-phase-00-audit/SKILL.md`

```markdown
---
name: pd-phase-00-audit
description: Execute PD Visual System P00 (環境・リポジトリ監査) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P00 環境・リポジトリ監査

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

PC、Git、Remotion、FFmpeg、対象エピソード、素材ルートを読み取り中心で監査し、安全な実装境界を確定する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P00`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- PHASE_STATE.json が P00 を指している
- 既存ファイルを変更せずに調査を開始できる

## Allowed scope
- 読み取り
- バージョン確認
- Git status/diff/log
- 文書テンプレートの新規作成

## Forbidden in this phase
- インストール
- 依存関係更新
- 大容量ダウンロード
- 既存レンダー上書き
- Git履歴変更

## Required deliverables
- ENVIRONMENT_AUDIT.md
- REPOSITORY_AUDIT.md
- IMPLEMENTATION_STATUS.md 更新
- P01_CHANGE_PLAN.md

## Acceptance criteria
- 主要パスとバージョンが記録済み
- 未コミット変更が保護されている
- 対象60〜90秒を選ぶための候補が示されている


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.35 `.claude/skills/pd-phase-01-baseline/SKILL.md`

```markdown
---
name: pd-phase-01-baseline
description: Execute PD Visual System P01 (Baseline保存・紙芝居診断) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P01 Baseline保存・紙芝居診断

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

対象エピソードから比較価値の高い連続60〜90秒を選び、現在版を保存して紙芝居要因を測定する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P01`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P00 が candidate_complete か completed
- レンダー手順が判明している

## Allowed scope
- 既存プロジェクトの非破壊レンダー
- コピー出力
- ffprobe解析
- ショット診断

## Forbidden in this phase
- 新ツール導入
- 既存ラフカット上書き
- 全編改修

## Required deliverables
- baseline動画または再現可能なレンダーmanifest
- BASELINE_DIAGNOSIS.md
- baseline_shots.json

## Acceptance criteria
- 同一ナレーションで後続版と比較できる
- 各ショットにvisual questionとstart/end stateがある
- 紙芝居要因8軸が採点済み


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.36 `.claude/skills/pd-phase-02-benchmark/SKILL.md`

```markdown
---
name: pd-phase-02-benchmark
description: Execute PD Visual System P02 (参照チャンネルのショット分解) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P02 参照チャンネルのショット分解

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

成功チャンネルの外見ではなく、ショット単位の情報設計、タイミング、音、再利用原理を観察記録する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P02`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P01 baseline区間が確定
- BENCHMARK_METHOD.mdを読んでいる

## Allowed scope
- 合法的な視聴と手動観察
- 公開情報の引用元記録
- タイムスタンプ記録

## Forbidden in this phase
- 動画素材の無断ダウンロード
- フレームや音源の再配布
- 固有デザインの複製

## Required deliverables
- benchmark_shots.jsonl
- BENCHMARK_FINDINGS.md
- COPY_BOUNDARY.md

## Acceptance criteria
- 最低3チャンネル×3動画×5ショット
- 各記録にvisual verbとlessonがある
- 採用原理とコピー禁止要素が分離されている


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.37 `.claude/skills/pd-phase-03-asset-index/SKILL.md`

```markdown
---
name: pd-phase-03-asset-index
description: Execute PD Visual System P03 (素材インデックス最小実証) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P03 素材インデックス最小実証

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

100〜500素材に限定し、ffprobe、PySceneDetect、3点サンプリング、SQLite、再開可能処理を検証する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P03`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P00監査で保存先と空き容量が確認済み
- PySceneDetect導入計画と固定版が承認済み

## Allowed scope
- 読み取り専用素材走査
- 新規インデックス・サムネイル出力
- 独立venv作成

## Forbidden in this phase
- 素材移動・削除・上書き
- 85,000点全件処理
- 元動画の再エンコード

## Required deliverables
- 試験SQLite DB
- scene thumbnails
- asset_index_report.md
- 再実行可能CLI

## Acceptance criteria
- VFR情報をPTS/time_base込みで保持
- 各動画カットを25/50/75%の3フレームで表現
- 中断再開・差分更新・エラー継続が動作


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.38 `.claude/skills/pd-phase-04-semantic-search/SKILL.md`

```markdown
---
name: pd-phase-04-semantic-search
description: Execute PD Visual System P04 (意味検索の最小実証) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P04 意味検索の最小実証

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

商用条件を記録した埋め込みモデルで、20クエリの検索品質を人間評価する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P04`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P03の試験DBが利用可能
- チェックポイント単位のライセンス判断がreviewed

## Allowed scope
- 承認済み重みのダウンロード
- ローカル埋め込み生成
- 検索評価

## Forbidden in this phase
- ライセンス不明重みの自動採用
- 検索結果の自動編集採用
- 全素材一括埋め込み

## Required deliverables
- 検索CLI
- embedding manifest
- 20-query evaluation
- MODEL_LICENSE_RECORD.md

## Acceptance criteria
- Top-10 precisionの人間評価を記録
- モデル/重み/取得元/ハッシュ/ライセンスを保存
- 検索失敗例を残す


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.39 `.claude/skills/pd-phase-05-motion-core/SKILL.md`

```markdown
---
name: pd-phase-05-motion-core
description: Execute PD Visual System P05 (Remotionコア5部品) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P05 Remotionコア5部品

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

EvidenceReveal、PenaltyVsProperty、CaseJourney、QuoteUnderExamination、VerdictReversalだけを高品質に実装する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P05`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P01のbaseline診断がある
- 既存Remotion構造とVIDEO_RULESを理解している

## Allowed scope
- 既存Remotionへの最小差分追加
- 新規デモcomposition
- テスト・docs

## Forbidden in this phase
- 追加コンポーネントの先回り実装
- 既存APIの全面改修
- 固有事件名のハードコード

## Required deliverables
- コア5部品
- デモcomposition
- 型・tests
- component_registry更新

## Acceptance criteria
- 5/8/12秒で破綻しない
- 長い英語文・欠損入力・30fpsでテスト
- 各部品がstart/end stateを変える


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.40 `.claude/skills/pd-phase-06-build-b1/SKILL.md`

```markdown
---
name: pd-phase-06-build-b1
description: Execute PD Visual System P06 (B1コア改善版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P06 B1コア改善版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

新ツールを増やさず、既存素材検索とコア5部品だけでbaseline区間を改善する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P06`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- P05コア5部品がcandidate_complete
- P03/P04が使える場合は検索結果を利用できる

## Allowed scope
- 既存素材
- コア5部品
- 既存SFX/BGM
- 非破壊レンダー

## Forbidden in this phase
- WhisperX
- SAM2/Depth
- Blender
- AI動画

## Required deliverables
- B1 preview
- B1 scene_plan.json
- B1 comparison notes

## Acceptance criteria
- Aと同一ナレーション
- 各シーン一主要動詞
- 理解度と紙芝居感の改善を人間評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.41 `.claude/skills/pd-phase-07-audio-sync/SKILL.md`

```markdown
---
name: pd-phase-07-audio-sync
description: Execute PD Visual System P07 (WhisperX同期・B2版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P07 WhisperX同期・B2版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

英語ナレーションを台本へ整列し、重要語・資料・SFXを単語単位で同期する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P07`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- B1が比較可能
- WhisperXと整列モデルのライセンスが記録済み

## Allowed scope
- 独立venv
- 英語音声整列
- cue生成
- Remotion同期

## Forbidden in this phase
- 認識結果による台本上書き
- 数字・年号・事件番号の無検査採用

## Required deliverables
- narration_alignment.json
- numeric_token_review.csv
- B2 preview

## Acceptance criteria
- 重要語同期誤差を測定
- 数字トークンを人間レビュー
- B1→B2の差を単独評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.42 `.claude/skills/pd-phase-08-parallax/SKILL.md`

```markdown
---
name: pd-phase-08-parallax
description: Execute PD Visual System P08 (2.5D・B3版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P08 2.5D・B3版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

静止画1枚だけで、明示的対象指定、SAM2、Depth Anything V2 Small、弱いパララックスを実証する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P08`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- B2が比較可能
- 対象画像と主対象box/pointが決まっている
- Small重みの利用判断がreviewed

## Allowed scope
- 手動box/point指定
- 弱い移動
- 背景105〜110%拡大
- 必要最小限のinpaint検討

## Forbidden in this phase
- 対象をSAM2へ丸投げ
- 強い横移動
- Base/Large/Giant導入
- 顔・文字の生成補完

## Required deliverables
- mask/depth/layers
- review contact sheet
- B3 preview

## Acceptance criteria
- 背景穴・縁・顔・文字をQC
- 最大変位が設定値以下
- B2→B3の差を単独評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.43 `.claude/skills/pd-phase-09-evidence-room/SKILL.md`

```markdown
---
name: pd-phase-09-evidence-room
description: Execute PD Visual System P09 (PD Evidence Room・C1版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P09 PD Evidence Room・C1版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

再利用可能なBlenderセットを最小構成で作り、限定カメラ1カットを追加する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P09`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- B3が比較可能
- Blender CLI動作確認
- 画面合成方式が固定

## Allowed scope
- 固定/正面モニター、3カメラ、低品質preview
- Blender背景＋Remotion資料合成

## Forbidden in this phase
- 全編3D
- 追跡座標未実装の動くモニター合成
- 毎話別セット

## Required deliverables
- PD_Evidence_Room.blend
- render script
- camera manifest
- C1 preview

## Acceptance criteria
- 次話で差し替え可能
- 固定カメラ合成がずれない
- 必要なら四隅スクリーン座標をフレーム出力


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.44 `.claude/skills/pd-phase-10-ai-broll/SKILL.md`

```markdown
---
name: pd-phase-10-ai-broll
description: Execute PD Visual System P10 (AI B-roll・C2版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P10 AI B-roll・C2版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

既存素材で埋まらない1カットだけをComfyUI＋承認済みモデルで生成し、品質・時間・リスクを測る。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P10`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- 素材不足が記録で証明されている
- モデル/重み/ノード/出力条件のライセンス監査済み
- 5GB超ダウンロードが明示承認済み

## Allowed scope
- 3〜5秒の雰囲気B-roll
- seed固定
- 1ワークフロー1モデル

## Forbidden in this phase
- 実在人物の発言再現
- 判決文・新聞・証拠生成
- 未レビュー採用
- 全編生成

## Required deliverables
- workflow JSON
- generation manifest
- human review
- C2 preview

## Acceptance criteria
- VRAM/時間/失敗率を記録
- AI開示判定
- C1→C2の差を単独評価


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.45 `.claude/skills/pd-phase-11-finishing/SKILL.md`

```markdown
---
name: pd-phase-11-finishing
description: Execute PD Visual System P11 (音響・カラー・C3版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P11 音響・カラー・C3版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

音響、章転換、カラー、ラウドネスを追加し、C2との差だけを評価する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P11`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- C2が比較可能
- 既存PDの音量・カラー規則を確認済み

## Allowed scope
- 既存ルール内の音響・カラー
- ffmpeg検査
- 必要に応じDaVinci公式API検証

## Forbidden in this phase
- GUI座標自動操作
- 音圧の過剰化
- 事実映像と再現映像の色による混同

## Required deliverables
- C3 preview
- audio/color manifest
- ffmpeg QC report

## Acceptance criteria
- 黒画面/無音/ピーク/ラウドネス検査
- C2→C3の寄与が評価可能


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.46 `.claude/skills/pd-phase-12-decision-rollout/SKILL.md`

```markdown
---
name: pd-phase-12-decision-rollout
description: Execute PD Visual System P12 (投資判断・全編展開) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P12 投資判断・全編展開

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

A/B1/B2/B3/C1/C2/C3の増分比較から、標準構成と不採用技術を決め、勝った方式だけを全編へ展開する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P12`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- 各variantの動画と工数・品質データが揃っている
- 人間評価が完了

## Allowed scope
- 採用方式の拡張
- 不要実験のdeprecated化
- 部品・ルールの更新

## Forbidden in this phase
- 効果不明なツールの惰性採用
- 比較なしの全編改修
- 未レビュー生成物の本番利用

## Required deliverables
- INVESTMENT_DECISION.md
- STANDARD_VISUAL_RECIPE.md
- 全編実装計画
- deprecated list

## Acceptance criteria
- 品質向上/分の工数を比較
- 再利用率と長期維持費を判断
- 本番可否ゲートが明確


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
```

## 44.47 `.claude/skills/pd-phase-advance/SKILL.md`

```markdown
---
name: pd-phase-advance
description: Advance PD Visual System to the next phase after explicit human approval and successful validation.
argument-hint: "[next-phase-id]"
disable-model-invocation: true
---

# Advance phase

This skill is the only normal path for changing `current_phase`.

1. Read `PHASE_STATE.json`, `IMPLEMENTATION_STATUS.md`, and the current phase report.
2. Verify current status is `candidate_complete`.
3. Verify all current phase acceptance criteria have evidence.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Treat the user's explicit invocation of this skill as human approval for `$ARGUMENTS` only.
6. Run:

```bash
python scripts/pd-visual-system/phase_gate.py advance --to "$ARGUMENTS" --human-approved
```

7. Update `IMPLEMENTATION_STATUS.md` to the new phase with status `not_started`.
8. Do not perform work from the new phase in the same turn unless the user explicitly requested both actions.
```

## 44.48 `.claude/skills/pd-qc/SKILL.md`

```markdown
---
name: pd-qc
description: Run non-destructive PD preview or final-render quality checks and produce a release gate report.
argument-hint: "[video-or-manifest-path]"
disable-model-invocation: true
---

# PD QC

1. Read source/truth/license policy and quality gates.
2. Inspect the supplied path without overwriting it.
3. Use ffprobe and non-destructive FFmpeg detection where available.
4. Check video/audio codecs, duration, dimensions, frame rate, corruption, black frames, freeze frames, silence, true peak, and loudness.
5. Cross-check missing assets, provenance, license decisions, AI review, and disclosure decision from manifests.
6. Write `qc_report.json` and `qc_report.md` beside the job output or in a new QC directory.
7. Set `release_ready=false` for every hard blocker in `quality-gates.json`.
8. Separate hard blockers, warnings, and creative suggestions.
```

---

# 45. Final Operating Doctrine

Claude Codeは、映像を派手にするために存在するのではない。

Claude Codeは、次を一貫して行うための制作担当である。

1. 事実を守る
2. 視聴者が理解すべき問いを決める
3. 最も安価で正確な映像手段を選ぶ
4. 既存素材を先に探す
5. コア部品で関係を見せる
6. 音声へ同期する
7. 2.5D、3D、AIは不足だけへ使う
8. 比較によって寄与を測る
9. 勝った部品だけを標準化する
10. 次話の制作を軽くする

最終原則:

> 実際の証拠が真実を担い、アニメーションが理解を担い、3Dが空間を担い、AIが不足だけを補う。

> 画面を動かすのではなく、視聴者の理解を動かす。

# END OF MASTER REFERENCE v2.0.0
