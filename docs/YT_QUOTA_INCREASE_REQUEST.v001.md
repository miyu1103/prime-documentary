# YouTube Data API クォータ引き上げ申請（v001・2026-08-03）

## なぜ必要か（実測）

2026-08-03、1日10,000ユニットを使い切って停止した。API本人の応答：

```
403  "The request cannot be completed because you have exceeded your quota."
```

読み取り1ユニットすら通らない状態。内訳（実測）：

| 作業 | ユニット | アップロード換算 |
|---|---|---|
| 再生リスト整備 42本 | 2,364 | 1.5本 |
| 説明欄・チャプター 42本 | 約2,250 | 1.4本 |
| 動画アップロード 2本 | 3,200 | 2本 |
| サムネ・字幕・監査 | 約900 | 0.6本 |
| **合計** | **約8,700** | |

`videos.insert` が 1,600 ユニットなので、**アップロードだけなら1日6本が上限**。運用作業を1つでも挟むと3〜4本に落ちる。毎日1本の投稿計画に対して余裕がない。

---

## 申請先

Google Cloud Console → 該当プロジェクト → **APIとサービス → YouTube Data API v3 → 割り当て**
→ 「割り当ての増加をリクエスト」

または **YouTube API Services - Audit and Quota Extension Form**
https://support.google.com/youtube/contact/yt_api_form

## 申請時に必要な情報

| 項目 | 値 |
|---|---|
| GCP プロジェクト番号 | **575149180320** |
| API | YouTube Data API v3 |
| チャンネル | Prime Documentary（UCuQPtAz1rca9eJ4xhvX0yKA） |
| 現在の割り当て | 10,000 units/day |
| 希望する割り当て | **50,000 units/day** |

50,000 を希望する根拠：1日1本の投稿（1,600）＋公開後の説明欄・再生リスト・字幕の保守（1本あたり約150）＋週次の読み取り監査（約1,500）＋制作中の複数話の下書き投稿。実運用のピークが約12,000〜15,000で、3倍の余裕を見た値。

---

## 申請文（英語・そのまま貼れます）

> **Use case**
>
> Prime Documentary is a single-channel documentary studio publishing one long-form film per day
> (28–30 minutes) on YouTube. Everything is produced and published by the channel owner; the API
> is used only against our own channel.
>
> We use the API for three things:
>
> 1. **Uploading our own finished films** as private videos with a scheduled `publishAt`, so that
>    publication happens at a fixed time each day (`videos.insert`, 1,600 units each).
> 2. **Maintaining our own back catalogue** — chapter blocks and internal links in descriptions,
>    caption tracks, and series playlists (`videos.update`, `playlistItems.insert`, `captions.insert`).
> 3. **Reading our own channel's public statistics** for a weekly production review
>    (`videos.list`, `playlistItems.list`).
>
> **Why the current quota is not sufficient**
>
> The daily 10,000-unit allocation is exhausted by roughly three uploads once ordinary catalogue
> maintenance is included. On 2026-08-03 we spent 2,364 units placing 42 existing videos into
> series playlists and approximately 2,250 units adding chapter markers and internal links to the
> same 42 descriptions — necessary one-time housekeeping — which left room for only two of the
> three uploads scheduled that day. A single `videos.insert` at 1,600 units means the cap is six
> uploads per day with no operational headroom at all.
>
> We are not requesting quota to access other channels' data, to bulk-download content, or to
> operate at scale on behalf of third parties. Every call is against `mine=true` or an explicit
> allowlist containing only our own channel id, and the allowlist is enforced in code before any
> write.
>
> **Requested quota**: 50,000 units/day.
>
> **Compliance**
>
> - All uploaded content is original work produced by the channel owner.
> - Uploads are created as `private` with a scheduled `publishAt`; nothing is published without
>   an explicit per-release approval record.
> - No credentials, tokens or user data are shared, stored outside the owner's machine, or used
>   for any channel other than our own.
> - We do not use the API to circumvent any YouTube feature, and we do not automate any action
>   that the YouTube Terms of Service reserve to the user interface (for example end screens and
>   cards, which we set manually).

---

## 申請の通しやすさについて（正直に）

- 審査には**数週間かかることがある**。今日明日の解決策にはならない。
- 却下されることもある。その場合は理由が返るので、書き直して再申請できる。
- **通らなくても運用は回る**。下の代替策で足りる。

---

## 申請中にとる代替策

**① ブラウザから手動アップロード**
API を使わないので**ユニット消費ゼロ・本数無制限**。急ぐときはこれが確実。

**② アップロードの日と保守の日を分ける**
今日の失敗はこれをやらなかったこと。42本の説明欄更新は一度きりの作業で、もう繰り返さない。

**③ 投稿前に残量を測る**
`videos.insert` を撃つ前に、残りユニットから「今日はあと何本いけるか」を出す。
これは `upload_schedule_case_v001.py` に組み込む。
