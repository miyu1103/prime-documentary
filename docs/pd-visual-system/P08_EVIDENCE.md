# P08 EVIDENCE — B3版（2.5D・歪みなし cutout）

- Phase `P08` / by claude-code / 2026-07-12 (JST)

## 実装（既存部品再利用・invariant14）
1. **深度生成**: `scripts/pd-visual-system/depth_generate_poc.py` = Depth Anything V2 **Small(Apache-2.0・商用OK)** standalone＋ViT-S重み(99MB→`D:\PD_AI_Models\depth`)・**GPU**。→ `remotion/public/timbs/SPN-0007_depth.png`(3840×2160・高品質・目視確認)。
2. **レイヤー分離**: `scripts/pd-visual-system/layer_cutout_poc.py` = 深度閾値→前景mask(feather)＋inpaint背景。→ `_p08/SPN-0007_{fg,bg}.png`(fg被覆29.6%)。
3. **2.5D合成**: `remotion/src/compositions/TimbsParallax.tsx` = 既存 `Parallax.tsx`(剛体translate+scale)に2層＋緩いKen-Burns。Root登録`TimbsParallax`。typecheck exit0。

## 品質判断（measure→verify・自己申告せず）
- ❌ **DepthStill(メッシュ変位)は鎖/縁を歪ませた**（`p08_check/depth_78.png`）→ owner制約不適合→**不採用**（`P08_FINDING.md`）。
- ✅ **Parallax cutout は鎖・天秤の縁がクリア＝歪みなし**（`p08_check/parallax_82.png` 目視）。剛体移動なので細部が壊れない。奥行きは層差＋Ken-Burnsで付与。
- 2.5D preview mp4 → 背景レンダ中。

## 受入基準（owner制約）
Small重みのみ(商用OK) ✅／背景scale小・横移動小・変位キャップ(amount46) ✅／feather mask ✅／**人物/建物/細部の歪みなし** ✅／穴なし(inpaint bg) ✅。

## rollback / 限界 / 次
- rollback: `TimbsParallax.tsx`＋`_p08/*`＋`SPN-0007_depth.png`＋Root追記を戻す。DepthStill等 既存は不変。
- 限界: 前景分離は深度閾値ベース（SAM2 box精密化は将来の精度アップ・SAM2はcu121導入済）。動きは控えめ（安全側）。
- 次 P09 = C1版（PD Evidence Room・Blender・設計=P09_PLAN.md）。
