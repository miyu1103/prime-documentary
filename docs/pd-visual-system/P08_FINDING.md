# P08 FINDING — 2.5D PoC（正直な中間結果）

- Phase `P08` / 2026-07-12 (JST) / by claude-code

## 実証できたこと ✅
- **Depth Anything V2 Small（Apache-2.0・商用OK）で深度生成が稼働**。standalone `depth_anything_v2` パッケージ＋ViT-S重み(99MB→`D:\PD_AI_Models\depth`)、**GPU(cuda)**。transformers版問題を回避。
- `scripts/pd-visual-system/depth_generate_poc.py`（`<name>_depth.png`規約・atomic・--dry-run/force）。
- `remotion/public/timbs/SPN-0007_depth.png`（3840×2160）= **高品質**（天秤/車/皿の前景と暗い背景が明瞭に分離・目視確認）。

## 見つけた問題 ⚠（オーナー制約に照らして不採用）
- 既存 **`DepthStill`（@remotion/three メッシュ変位）で2.5D化すると、鎖・天秤の縁など細い構造がギザギザに歪む**（`outputs/pd-visual-system/p08_check/depth_78.png` で顕著）。
- これは owner制約「人物/建物が歪むほど動かさない・穴/縁が見えたら不採用」に**抵触**。P08設計(`P08_PLAN.md`)の警告どおり＝**メッシュ変位は細部を歪ませる**。
- `DepthStill` は共有本番部品（EP29等が使用）で displacement は内部計算・propで下げられない → **弄らない**（波及回避）。

## 正しい本番路線（P08_PLAN 準拠・次の実装）
- **既存 `Parallax.tsx`（フラット層 cutout）を再利用**＝歪ませない。
- **SAM2（導入済 cu121 GPU）で box指定の前景マスク**→ fg cutout(RGBA・feather)＋bg plate(穴埋め)。Depth Small が前後関係を決定。
- 2層を `Parallax`（bg 1.05-1.10・小さい横移動・変位キャップ）へ。box契約 `{target_label,prompt_type:"box",box_xyxy,review_required:true}`。

## 判断
- **深度capabilityはP08として完了扱い可**（生成・品質・GPU・商用ライセンス実証）。
- **「歪みのない2.5Dショット」はParallax-cutout実装が必要**（SAM2マスク＋bg穴埋め＋Parallax層＋新harness）。これは追加ビルド＝owner判断で着手。
- 歪んだDepthStill版は**出荷しない**（p08_check は不採用サンプルとして保存）。
