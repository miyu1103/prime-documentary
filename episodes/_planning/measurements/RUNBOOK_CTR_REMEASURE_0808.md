# 8/8 CTR再測定 ランブック（所要10分・cookieの生きている数分間に全部やる）

7/25のサムネ19本+タイトル17本の刷新効果を測る日（2-4週間経過後）。**per-video CTRはStudio cookieが必要**（10-60分でローテートするので、エクスポートしたら即実行）。

## 手順
1. ブラウザで studio.youtube.com のアナリティクスを開く
2. DevTools → Network → `get_screen` リクエスト → 右クリック → Copy as cURL
3. cURLの `-b '...'` の中身（cookie文字列）を `secrets/studio_cookies.txt` に上書き保存（1行・BOMなし）
4. **すぐに** ターミナルで連続実行:
   ```
   cd C:\Users\aab15\Documents\prime-documentary
   python scripts\yt_studio_ctr.py
   python scripts\yt_studio_video_ctr.py
   python scripts\yt_studio_retention.py --source studio
   ```
5. Claude Codeに「8/8のCTR再測定結果を分析して。baseline=scripts/_yt_studio_video_ctr.json(7/25版はgit履歴)、判定ルールはCTR_PLAYBOOK.v002.mdとDEEP_RESEARCH_FINDINGS.v001.md §8-E3(present-tense vs time-jump A/B判定含む)」と依頼

## 判定して決めること
- 刷新19本のCTR 前後比較 → 改善しなかったものはB案（in-scene顔12-22%・非センシティブ話のみ）へ
- stakes-gap/現在形タイトル文法の勝敗（§8実験E3）
- Studio版リテンション曲線（初取得）とAPI版の突合
