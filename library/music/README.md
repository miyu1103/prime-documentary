# library/music — 再利用音楽ライブラリ（decisions/0002 §C）

音楽は毎回生成せず、ここに**タグ付きで一度だけ蓄積**して自動選曲する。

- `music_registry.v001.json` … トラック records の配列。各要素は `schemas/music-track.schema.json` 準拠。
- 実体の音声ファイル（wav/mp3）は**重いメディア＝SSD側**に置き、`asset_uri`（論理URI `artifact://...`）で参照する（rule14）。レジストリ JSON 自体は brain＝このリポに置く。
- 自動選曲は `src/pd_factory/library/selection.py:select_track`（カテゴリ一致＋mood/energy＋直近N本の被り回避、決定論的）。

## 生成手順（owner 一度きり）
1. `prompts/11_music_library_briefs.md` の8カテゴリ×プロンプト＋SFXを Suno で生成。
2. 各トラックを SSD に保存し、`music_registry.v001.json` に record を追記（`track_id`=`MUS-NNNN`/`SFX-NNNN`、`content_hash`、`rights_basis`、`verified_at`）。
3. `select_track` が場面 `function/mood/energy` から自動で選ぶ。
