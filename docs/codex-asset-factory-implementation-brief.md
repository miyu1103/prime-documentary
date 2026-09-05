# Codex 実装指示書 — Phase 2（Asset Factory をコードに実装）

ステータス: 実装指示（未着手）／前提: Phase 1（Motion最小エンジン+MotionDemo）の後に実施。設計は `docs/asset-factory.md` `docs/asset-manifest-schema.md` `docs/production-workflow.md` `docs/scene-plan-schema.md`。

鉄則：**既存の選定ロジック・本番データを壊さない。素材棚は“候補プールに足す”だけ（置換しない）。** 外部有料サービスを増やさない。秘密情報を書かない。

---

## 0. 目的
「先に大量に貯めた素材棚（Asset Factory）から、Scene Plan / Shot Recipe が**選べる**」状態をコードで実現する。
すでに `scripts/build_factory_library.py` が `H:\pd-media\assets\factory\<category>\` に素材を貯め、`assets/asset_manifest.v001.json`（`AF-<CAT>-NNNN`）に登録済み。`scripts/select_factory_assets.py` で検索もできる。これを**スキーマで検証**し、**取り込みに接続**する。

## 1. 触ってよいファイル
- 新規 `schemas/asset-manifest.schema.json`（`docs/asset-manifest-schema.md` のドラフトJSON Schemaをそのまま実体化）。
- 新規 `scripts/validate_asset_manifest.py`（manifestをschemaで検証。既存 `scripts/validate_episode.py` の作法に合わせる）。
- 既存 `scripts/import_to_remotion.py`（**追記のみ**：素材が足りない場面の**フォールバック候補**として factory プールを混ぜる。既存の選定順は変えない＝AI画像>実写>既存ストック…の後ろに factory を足す）。
- 新規 `scripts/enrich_asset_manifest.py`（任意）：各assetに `compatibleSceneTypes` / `colorTone` / `mood` をカテゴリとサブタイプから推定して埋める（`select_factory_assets.py` の CAT_SCENE を流用）。

## 2. 触らないファイル
- 既存 `schemas/*`（asset/scene-plan等は**変更しない**。manifestは新schemaで別管理）。
- 既存の本番データ `remotion/src/data/*_roughcut.ts`、各話 `shotlist`/`asset_map`/台本。
- `.env`・鍵。`H:\pd-media`（読むのみ、コミットしない）。

## 3. 作業
1. **schema実体化**：`docs/asset-manifest-schema.md` のドラフトを `schemas/asset-manifest.schema.json` として作成。`id` は `^AF-[A-Z_]+-[0-9]{4}$`、`type` は14カテゴリenum、`sourceTool`/`license`/`mood`/`intensity`/`colorTone` の値域を反映。**stock取得分（sourceTool="stock"）も通るように** enumに `stock` を含める（既存manifestを壊さない）。
2. **検証**：`validate_asset_manifest.py` で `assets/asset_manifest.v001.json` 全件を検証。落ちる項目（width/height/durationFramesがnull等）は**任意フィールド**として許容（必須にしない）。
3. **取り込み接続**：`import_to_remotion.py` に「factory候補プール」をマージ。`build_usable_assets.py` が共有棚をマージしているのと同じ発想で、**rights_status=allowed のみ**・既存候補が足りない場面だけ補完。**既存の割り当て結果が変わらない**ことをdiffで確認。
4. （任意）`enrich_asset_manifest.py` で `compatibleSceneTypes` 等を付与し、`select_factory_assets.py` の精度を上げる。

## 4. 守ること
- 既存の本番ラフカット（timbs等）の `*_roughcut.ts` の中身が**この変更だけでは変わらない**こと（足りない場面の補完が無い限り）。差分を見せる。
- 商用OK・権利記録のある素材だけをタイムラインに入れる（`license` 必須・実在人物の肖像なし）。
- `python` 実行は `./.venv/Scripts/python.exe`。cp932対策で日本語出力時は `sys.stdout.reconfigure(encoding="utf-8")`。

## 5. 確認方法
- `./.venv/Scripts/python.exe scripts/validate_asset_manifest.py`（全件PASS、件数表示）。
- `./.venv/Scripts/python.exe scripts/select_factory_assets.py --scene-type explanation --limit 10`（棚から候補が返る）。
- 既存 `validate_episode.py 9〜15` が**引き続きPASS**（壊していない）。

## 6. 最後に出すもの
- 変更/新規ファイル一覧、検証結果（manifest件数・PASS）、`import_to_remotion` 接続の差分要約、既存検証がPASSのままであること。

---
この後、Phase 4（three/lottie/高度トランジション・要依存導入）→ Phase 5（Scene Plan→素材選択→本番適用）。詳細は `docs/remotion-animation-component-roadmap.md` と `docs/production-workflow.md`。
