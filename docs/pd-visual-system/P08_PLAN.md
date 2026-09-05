# P08 PLAN — 2.5D parallax（設計のみ・実行はP08到達＋venv導入後）

> エージェント調査(2026-07-12)。**実行しない**（現在P06）。P08で使う。

## 方針（invariant14＝二重実装しない）
- **既存 `remotion/src/components/Parallax.tsx` を再利用**（フラット層のcutout parallax＝owner制約「歪ませない・穴を出さない」に一致）。`DepthStill`(CaseFilm.tsx)のメッシュ変位は顔/建物を歪める→**使わない**。
- Parallax は `layers:{depth,node}[]`＋`translateX/scale`。`scale=1+depth*0.08`。**最小拡張**＝`scale?`/`dx?` オプションを足して「背景105-110%・最大変位キャップ」を明示（クローンしない）。

## モデル / ライセンス（重要）
- **Depth Anything V2 Small (ViT-S) のみ**＝**Apache-2.0 商用OK**。Base/Large/Giant＝CC-BY-NC＝**禁止**。
- 重み: HF `depth-anything/Depth-Anything-V2-Small-hf`（~99MB）。**使用前に LICENSE_REGISTER/MODEL_LICENSE_RECORD に reviewed 記録**（tool-registry が review_required）。
- 隔離venv `D:\PD_AI_Tools\DepthAnythingV2\.venv` / SAM2 `...\SAM2\.venv`（導入は背景実行中）。

## 既存資産（参照・重複しない）
- 深度生成の既存パターン: `scripts/gen_depth_maps.py`（DPT-large・`<name>_depth.png`規約）。
- 深度consumer: `CaseFilm.tsx DepthStill` / `Short.tsx DepthImageV` / harness `DepthTest.tsx`（Root登録）。depth PNGは hero と同じ `remotion/public/<slug>/` に `_depth.png`。

## 実装計画（1カットPoC＝SPN-0007）
- 対象 `remotion/public/timbs/SPN-0007.png`（3840×2160）。
- SAM2 が **box指定**で前景mask（丸投げ禁止）→ fg cutout(RGBA)＋bg plate(穴埋め・feather)。Depth Small が前後関係を決める。
- 2層を `Parallax` に投入。新harness `remotion/src/compositions/ParallaxTest.tsx`＋Root登録（preview限定・非出荷）。WebGL不要→concurrency制約なし。
- 層PNGは `remotion/public/timbs/_p08/`。

## スクリプト骨子（P08で作成）
- `scripts/pd-visual-system/depth_generate_poc.py`（Small・`_depth.png`・atomic・--dry-run/--force）＝隔離venv実行。
- `scripts/pd-visual-system/target_mask_poc.py`（SAM2・box→mask/fg/bg）。
- box契約 `outputs/pd-visual-system/P08/timbs/SPN-0007.targets.json`＝`{target_label,prompt_type:"box",box_xyxy,review_required:true}`。reviewed でなければ層を昇格しない。

## 安全制約（拘束）
Smallのみ／人手box＋review_required／弱い動き(bg1.05-1.10・変位キャップ)／feather・穴/縁/顔/建物歪みQC／既存Parallax再利用／隔離venv／H:読み取り専用／phase到達まで実行禁止。
