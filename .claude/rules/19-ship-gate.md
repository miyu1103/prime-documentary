# Ship Gate (binding on every thread)

長尺エピソードは、独立ゲートが実レンダのバイト列を測定して緑の受領書を出すまで予約・投稿しない。自己申告の「完了」は禁止（CLAUDE invariant 13/15）。

- 手順: `check_final_acceptance.py <ep> --render <mp4> --emit-receipt` → `09_package/acceptance_receipt.v001.json`。
- 予約は `upload_schedule_case_v001.py --ep <slug>` のみ。受領書の `video_sha256` がファイルと一致し、許容ハード不合格が `runtime_band`（唯一のオーナー承認偏差）だけの時しか投稿しない。
- チェックやしきい値を通すために緩めない。詳細は `docs/PD_SHIP_GATE.md`。
- アニメは必須要件: `CaseFilm` は設計トランジション＋モーションブラー(Trail)＋マスク切り上がり文字。`animation_density` が機械フロア。紙芝居・左右スイープ線・黄ウォッシュ・ただのズームは不可。
- 素材の被り禁止: `footage_diversity`（distinct≥0.40／再利用≤4／天秤等の汎用象徴≤2）。ビルダーは不足点数を警告する。
- 長尺の画像は Codex のみ（SDXLを勝手に起動しない）。
