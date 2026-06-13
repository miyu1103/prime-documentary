# HANDOFF — 引き継ぎメモ（新スレッド用）

最終更新: 2026-06-13 / 作成: 前スレッド（Value リポジトリに紐づくセッション）

このファイルは、**新しい Claude Code スレッド（`miyu1103/prime-documentary` に紐づくセッション）**が、
前の作業の続きをスムーズに始めるための引き継ぎです。まずこれを読んでください。

---

## 0. いちばん最初にやること（新スレッドのあなたへ）

ユーザーは「添付の `prime-documentary.bundle` を、このリポジトリ（`miyu1103/prime-documentary`）の
`main` ブランチに展開してコミット＆push」を依頼します。

手順の目安:
1. アップロードされた `prime-documentary.bundle` を取得する。
2. `git clone <bundle> restored` で中身を取り出す（履歴3コミットが入っている）。
3. その中身を、このリポジトリの作業ツリーへ展開し、`main` にコミットして push する。
   - 注意: バンドルのデフォルトブランチ名は `master`。このリポは `main` 運用なので
     `main` に合わせること。
4. push 後、`README.md` / `START_HERE.md` / このファイルを確認し、ユーザーに完了と確認方法を伝える。

> 補足: `docs/` は、前は Value リポの `.gitignore`（`config/*`, `docs/`）に巻き込まれて force-add が必要だった。
> このリポ（prime-documentary）の `.gitignore` は `docs/` を無視しないので、通常どおり add でOK。

---

## 1. このプロジェクトは何か

**Prime Documentary（PD）= 自律型ドキュメンタリー動画制作スタジオ**。
Claude Code に運用させる前提の「設計図＋憲法＋契約＋参照実装」一式（Edition 2）。
**Value（SES営業OS）とは完全に無関係な別プロジェクト。**

- 目的: 承認済みトピックが、調査→事実台帳→台本→場面→素材→音声→編集→QC→非公開アップロードまで
  自動で流れ、人間はポートフォリオ/高リスク/公開判断だけを行う制作システムにする。
- 詳細: `START_HERE.md` / `CLAUDE.md`(憲法) / `docs/00`〜`docs/41` / `PD_AUTONOMOUS_STUDIO_MASTER_SPEC_V2.md`

---

## 2. これまでに完了済みのこと（現状）

1. **ブループリント一式を取り込み**（zip → プロジェクト化）。229ファイル。
2. **現状監査レポート**を作成: `reports/TAKEOVER_AUDIT_2026-06-13.md`（BOOTSTRAP の A〜F）。
3. **実行可能な縦断パイプラインを実装**（新規）: `src/pd_factory/` に
   `provenance.py` / `episode_repo.py` / `generators.py` / `pipeline.py`、`cli.py` に `run`/`status`。
   - チェーン: `topic → research_plan → sources → claims → thesis → script → scene_plan
     → asset_plan → voice_plan → edit_plan → qc_report`
   - 不変リビジョン＋provenance＋sha256、冪等レジューム、部分再実行＋下流自動無効化、
     予算ゲート、承認ゲート遵守（自動承認しない）。**外部送信/LLM/課金/アップロード一切なし**。
   - 生成器は決定論的スタブ（事実をでっち上げない／プレースホルダは明示）。
     QC は `pass_with_warnings` を返し「実調査前は公開不可」と判定。
4. **監査ギャップ G1 を解消**: コード(`domain.py`)とスキーマの state enum 不一致を、
   後方互換の superset 化で統一（`schemas/common.schema.json` / `schemas/episode-manifest.schema.json`）。
5. 検証すべて green:
   - `PYTHONPATH=src python scripts/validate_examples.py` → 9 groups PASS
   - `PYTHONPATH=src python scripts/validate_all_v2.py` → VALIDATION PASSED
   - `PYTHONPATH=src python -m pytest -q` → 18 passed
   - `make demo` → 全工程生成／2回目は全skip（冪等）／claims起点の部分再実行で下流のみ再生成

git 履歴は3コミット:
`82434b4`(初期取込) → `e3b69bc`(監査＋パイプライン) → `6d46381`(G1解消)。

---

## 3. 経緯メモ（なぜ Value リポに痕跡があるか）

新規 GitHub リポ作成がそのセッションの権限（GitHub App）で不可だったため、一時的に
`miyu1103/value` の `claude/hopeful-volta-gqaeaq` ブランチ＋ PR #1 に置いていた。
このリポ（prime-documentary）が正式な置き場所。**Value 側の PR #1 / ブランチは無視・後で削除可**
（Value 本体ファイルは一切変更していない）。

---

## 4. 守るべき方針（CLAUDE.md 抜粋・重要）

- 事実の裏付けが無い記述を承認済み台本に入れない。プレースホルダは必ず明示。
- 承認なき公開なし。承認はリビジョン＋ハッシュ完全一致時のみ有効。
- 秘密情報をコミット/ログに出さない。破壊操作はスコープ＋dry-run＋バックアップ＋承認。
- 外部課金にはidempotencyキー＋予算チェック。承認済み成果物は上書きせず新リビジョン。
- 既存能力の二重実装をしない（既存を拡張できない理由を先に示す）。
- テスト/スキーマ/検証を黙って弱めない。

---

## 5. 次にやる価値が高いこと（優先順）

監査 F 章＋オーナー意向に基づく候補:

1. **（基盤の締め）** G1 は解消済み。残る編集判断: `audio_ready` と `voice_ready`/`music_ready` を
   1つの正準モデルに統合するか（オーナー判断・未決）。
2. **実リサーチアダプタ**: `gen_sources` / `gen_claims` を `docs/28`（Web取得の安全方針）準拠の
   本物の調査に置換。外部入力＋プロンプトインジェクション防御が必要になる最初の地点。
   → アダプタ＋プリフライト＋idempotency＋予算の裏に隔離すること。
3. **最小UI（オーナー要望）**: 「テーマ入力→ボタン→台本/場面/QC表示」の最小画面を1枚。
   いまの `pipeline.run_pipeline` をそのまま叩く薄いUIにする。
4. その後、SDXL（画像）→ ElevenLabs（音声）→ DaVinci（編集）→ YouTube（非公開アップロード）
   を順にアダプタ接続。各々プリフライト＋承認ゲート必須（勝手に本番ONしない）。

> オーナーの言葉: 「まだアプリ本体は無い。土台（設計＋中核エンジン）ができた段階」。
> 次の自然な一歩は **3（最小UI）** か **2（実リサーチ）**。着手前にオーナーに確認すること。

---

## 6. すぐ使えるコマンド

```bash
make demo       # サンプル1本を全工程生成（runs/ に出力・gitignored）
make test       # 18テスト
make validate   # パッケージ全体検証
PYTHONPATH=src python -m pd_factory.cli run   <episode_dir>
PYTHONPATH=src python -m pd_factory.cli run   <episode_dir> --from claims   # 部分再実行
PYTHONPATH=src python -m pd_factory.cli status <episode_dir>
```
