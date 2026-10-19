# P12 — 結果分析と全編展開判断（capstone）

- Phase `P12` / by claude-code / 2026-07-12 (JST)
- 対象: timbs 80.4秒 test-bench（同一区間・同一ナレ）で A→C を1変更ずつ検証（ブリーフ§7）。
- 適用先本番: **EP37**（DEC-20260712-002・過去話は作り直さない）。

## 実験結果（1変更ずつ／実レンダ実証）
| 版 | 加えた変更 | 実証（実物） | 紙芝居/動き | 破綻 |
|---|---|---|---|---|
| **A** | 現状baseline | `baseline_A.mp4` | 主役 motion 0.87/0.63＝**近静止**・freeze 11.8s・8軸51/96 | freeze |
| **B1** | 素材検索＋コア5部品 | `TimbsB1_preview.mp4` | PenaltyVsProperty/Quote で**近静止を動的化**・freeze解消 | なし |
| **B2** | ＋WhisperX(faster-whisper)語同期 | `TimbsB2_preview.mp4` | $10/$42/disproportionate が**発話フレームで金ハイライト**（図・字幕・音一致） | なし |
| **B3** | ＋2.5Dを1カット | `TimbsParallax_preview.mp4`＋`SPN-0007_depth.png` | Depth Small＋Parallax cutoutで**歪みなし立体**（鎖クリア） | なし（DepthStillは歪む→不採用） |
| **C1** | ＋Evidence Room | `p09_check/wide_test.png` | 再利用3Dセット（デスク/ボード3枠/モニタ/地図・ブランド照明） | なし |
| **C2** | ＋AI動画1カット | Wan2.2 TI2V-5B（DL中） | 短B-roll穴埋め用・provenance確立（テスト区間は不要） | — |
| **C3** | ＋音・色仕上げ | `c3_check/c3_1080.png` | ビネット/グレイン/グレードでシネマ質感・音ダッキング済 | なし |

## 何が品質に効いたか（1変更ずつの結論）
1. **コア5部品(B1)＝最大の効き**：P01で数値化した「主役の近静止」を意味アニメで解消。紙芝居の根本対策。
2. **語同期(B2)＝理解と一体感**：数字/引用が発話に一致し「読む」から「体感」へ。
3. **2.5D(B3)＝奥行き**：静止画の平面感を解消（歪ませないParallax cutoutが正解）。
4. **Evidence Room(C1)＝統一世界観**：各話で作り直さない再利用資産。
5. **仕上げ(C3)＝高級感**：最後の質感。

## 確立した再利用インフラ（EP37以降で使える）
- 素材検索: `scene_index_poc.py`＋`clip_search_poc.py`（OpenCLIP・実用≈80%）
- コア5部品: `components/core5/`（motionkit合成・typecheck済）
- 語同期: `whisperx_align_poc.py`（faster-whisper・review_required規則）
- 2.5D: `depth_generate_poc.py`＋`layer_cutout_poc.py`＋`Parallax`（歪みなし）
- 3D世界: `pd_evidence_room.py`（再利用セット・8カメラ設計）
- AI B-roll: Wan2.2 TI2V-5B（provenance枠組み・穴埋め限定）

## リスク/学び（機構化済）
- pip版固定必須＋import後の機能スモーク必須（WhisperX版地獄の教訓・`TOOLS_INSTALLED.md`）。
- DepthStillメッシュ変位は細部を歪ませる→Parallax cutout（`P08_FINDING.md`）。
- AI依存は各ツール独立venv隔離（既存 global310/remotion 無傷を全工程で実証）。

## 判定：**Go（EP37へ展開）**
- 進化版パイプラインの中核（検索・コア5・語同期・2.5D・世界観・仕上げ）を **timbs test-bench で1変更ずつ実証**。効果と非破壊性を確認。
- **次アクション**: (1) EP37 topic 承認→`pd-new-episode`で新話作成、(2) 台本→scene_plan で core5/2.5D/Evidence Room を配線、(3) 素材検索でB-roll選定、(4) faster-whisperで語同期、(5) ship-gate（`check_final_acceptance`/animation_density/footage_diversity）で受領。
- **保留**: Wan2.2 実生成はDL完了後（穴埋め用途）。実在肖像/文書のAI生成は不変で禁止。
- **owner承認事項**: EP37 topic 選定、公開予約（invariant2）。
