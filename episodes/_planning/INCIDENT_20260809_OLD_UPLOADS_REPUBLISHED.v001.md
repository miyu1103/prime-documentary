# インシデント: 4類型違反の旧アップロード5本が公開状態に戻っていた

**発見**: 2026-08-09 04:0x JST、チャンネルAPI実測（videos.list part=status）にて。
**対応済み**: 同時刻に videos.update で5本すべて private へ復帰（HTTP 200、独立GETで再確認済み）。

## 事実

8/5にオーナー判断で予約解除・非公開化した旧アップロードのうち、以下5本が
`privacyStatus=public` になっていた（publishAtなし＝即時公開状態）:

| videoId | 話 | 確認済みの4類型違反 |
|---|---|---|
| `dueMY2lSu8w` | willingham旧 | 実在の子どもの顔 (18:37) — 類型2 |
| `Gx_i5aMJWLM` | morton旧 | y2mate由来・Rebel News映像 — 類型1（著作権ストライク経路） |
| `6VL_mA6OiS0` | norfolk旧 | 実在の女子生徒2名 (3:21) — 類型2 |
| `0iDUT0gzBiQ` | flowers旧 | 実在の子どもの顔 (18:30-18:38) — 類型2 |
| `0sjw_1OxCVk` | postoffice旧 | 名札違反 — 類型3（修正版4FlCaOVpln0と重複公開でもあった） |

同時に、修正版 `PfdEpNQyaQQ`（flowers新・審査PASS）と `4FlCaOVpln0`（postoffice新・審査PASS）も
予約日（8/10・8/13 12:00 JST）を待たず public になっていた。**この2本は審査済みのため public のまま残した。**
burge旧 `Ew5bZNOk17E` / fieldtest旧 `FOdVK1qQE6w` は private のままで無事。

## 推定原因

オーナーは8/8前後、Codex に作業を委任していた（memphis EP64レンダー、シート再生成、
norfolk 仕上げジョブ起動 8/9 03:56 の痕跡あり）。オーナーの8/6指示
「今非公開になってる動画は早急に公開できるようにしてほしい。全部。」を、
**検査を通さず字義通り「全部即公開」として実行した**とみられる。
確定情報はない（YouTube APIは変更者・変更時刻を返さない）。

## 対応

- 5本を private へ復帰（2026-08-09 04:0x JST、200確認、再GET検証済み）。
- ロールバック: 各1回の videos.update で再公開可能（ただし4類型違反が入っている限り禁止）。

## 残存リスク（要オーナー対応）

**Codex の毎時自動セッションが動き続けている**（node kernel が毎時起動、直近 8/9 03:49）。
同じロジックが再実行されると、この5本が再び public に戻る可能性がある。

**2026-08-09 07:00頃 クローズ**: オーナーが「Codexは止まってる」と確認。再発経路は消滅。
念のため次セッション開始時に該当5本の privacyStatus を1回だけ再実測することを推奨。
