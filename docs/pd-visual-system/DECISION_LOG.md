# Decision Log

## Format

### DEC-YYYYMMDD-NNN: Title

- Date:
- Status: proposed | accepted | rejected | superseded
- Context:
- Decision:
- Alternatives:
- Consequences:
- Evidence:
- Revisit trigger:

---

### DEC-20260711-001: Execution architecture

- Date: 2026-07-11
- Status: accepted
- Context: 5,000行超の単一プロンプトは研究正本として有用だが、毎回の実行コンテキストとして重すぎる。
- Decision: 短いCLAUDE.md、path-scoped Rules、手動Phase Skills、read-only subagents、deterministic Hooks、巨大MASTER_REFERENCEへ分解する。
- Alternatives: 全文を毎回読み込む、一括自動化ツールを新規開発する。
- Consequences: 実行精度と安全性が上がる一方、Phase進行の明示操作が必要になる。
- Evidence: Claude Code公式のCLAUDE.md、Skills、Rules、Hooks、Subagentsの役割分担。
- Revisit trigger: Claude Codeの拡張機構が大きく変更された場合。

---

### DEC-20260712-002: 進化版パイプラインの適用対象を EP37+ とする（過去話は作り直さない）

- Date: 2026-07-12
- Status: accepted（owner明示指示）
- Context: owner指示「今までの動画はもういい。次のEP37から進化させればいい」。既存の PD-2026-009-timbs や 036-williams など公開/制作済みは reship しない。EP37 は未作成（最新=PD-2026-036-williams）。
- Decision: PD Visual System が作る**ツール/コア5部品/2.5D/Evidence Room/AI B-roll は再利用インフラ**として完成させ、**実制作への適用は次の新規 EP37 以降**とする。`PD-2026-009-timbs` は **R&D ベンチマーク（実験台）専用**として維持（80秒 baseline_A で各レバーの効果を安く測る）が、その動画自体は出荷しない。
- Alternatives: timbs を作り直して出荷する（owner否定）/ 036-williams に適用（未指示）。
- Consequences: P03/P04(素材検索)・P05(コア5部品)・P07/P08/P09/P10 は episode 非依存で継続。P06 以降の A/B/C 比較は timbs baseline を test-bench に使うが、**成果物の初適用は EP37**。EP37 は topic 承認後 `pd-new-episode` で作成。
- Evidence: 本セッションの owner メッセージ、`episodes/` に 037 不在、`baseline_A.mp4` / `BASELINE_DIAGNOSIS.md`。
- Revisit trigger: owner が適用対象を変更、または EP37 topic 確定時。
