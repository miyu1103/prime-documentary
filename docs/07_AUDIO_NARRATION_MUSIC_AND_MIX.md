# 07 — Audio, Narration, Music and Mix

## 1. Audio Hierarchy

1. Narration intelligibility
2. Critical natural sound
3. Music
4. Decorative effects

音楽がナレーションを邪魔した場合、音楽が負ける。

## 2. Voice Profile

- provider
- voice alias
- provider voice ID
- language/accent
- model preference
- stability/style settings
- target pace
- emotional range
- pronunciation dictionary
- output format
- sample rate
- loudness target
- fallback voice
- licensing evidence
- last verified date

provider固有IDをepisodeへ散在させず、profile aliasで参照する。

## 3. Draft Voice vs Master Voice

### Draft

- 低コスト
- 高速
- 尺・構成確認用
- 台本変更前提

### Master

- 最終承認済み台本
- 高品質モデル
- 発音辞書適用
- QC必須
- 修正はチャンク単位

## 4. Chunking Algorithm

考慮：

- paragraph
- punctuation
- semantic completeness
- target character range
- chapter boundary
- quotation
- emotional direction
- pronunciation complexity
- anticipated revision risk

短すぎるチャンクは声の一貫性を失い、長すぎるチャンクは修正コストを上げる。

## 5. Narration Chunk Fields

- chunk_id
- script_span_ids
- display_text
- spoken_text
- pronunciation_entries
- context_before
- context_after
- emotion
- pace
- pause policy
- provider profile
- generation seed if supported
- output asset
- QC status
- revision

## 6. Pronunciation Dictionary

登録対象：

- 人名
- 地名
- 組織名
- 略語
- 専門用語
- 外国語
- 年代
- 数字
- 単位
- 固有の英語読み

表示テキストと読みテキストを分ける。

## 7. Voice QC

- 欠落
- 重複
- 読み間違い
- 不自然なポーズ
- 章間の音色変化
- clipping
- noise
- speed
- emotion overacting
- flat delivery
- leading/trailing cutoff
- loudness
- script mismatch
- seam artifact
- silence anomaly

問題チャンクだけ再生成。

## 8. Alignment

- word timestamps
- chunk start/end
- silence trimming policy
- crossfade
- breath preservation
- scene anchor points
- subtitle timing

全無音を機械的に削ると不自然になるため、意味のあるポーズを保持する。

## 9. Music Strategy

各動画のために毎回新曲を作る必要はない。

効率的な構造：

1. 商用利用可能なBGMをまとまった単位で生成・取得。
2. 音響・感情属性を自動解析。
3. ライブラリへ登録。
4. 動画の章機能へ自動選定。
5. 不足する用途セルだけ追加生成。

## 10. Music Asset Metadata

- track_id
- mood
- energy
- tension
- tempo
- key where useful
- texture
- era feel
- instrumentation
- loopability
- intro strength
- climax suitability
- dialogue friendliness
- rights status
- source
- creation date
- duration
- loudness
- reuse count
- prompt
- generation plan/license evidence

## 11. Music Coverage Matrix

例：

- mood：mystery / awe / tension / tragedy / reflection / resolution
- energy：low / medium / high
- texture：organic / orchestral / electronic / ambient
- duration：short / medium / long
- dialogue friendliness：high / medium
- climax：none / gradual / strong

一万曲を無目的に作るのではなく、不足セルを埋める。

## 12. Suno等の扱い

- 生成時の商用利用条件と契約状態を保存。
- ファイル、生成日、アカウントプラン、プロンプト、権利メモをmanifest化。
- 公式APIまたは明示的に許可された統合を優先。
- 非公式UI自動操作は規約・アカウントリスク評価まで無効。
- Web UI生成でも監視フォルダへダウンロード後、自動取り込み・解析・分類。
- 曲生成そのものより、選定・分類・再利用を自動化する。

## 13. Cue Functions

- question
- mystery
- discovery
- escalation
- threat
- tragedy
- reflection
- resolution
- aftermath
- silence

音楽は常時盛り上げるためではなく、章機能を支える。

## 14. SFX / Ambience

- location bed
- weather
- machinery
- crowd
- room tone
- transition hit
- low-frequency tension
- archival texture

説明を邪魔する過剰な効果音を避ける。

## 15. Mix QC

- clipping
- integrated loudness
- true peak
- narration consistency
- music ducking
- sudden noise floor
- stereo phase
- silent gaps
- cut clicks
- chunk seam
- SFX overuse
- chapter transition jump
- phone/headphone intelligibility

具体的数値はconfig化し、配信仕様の変化に対応する。
