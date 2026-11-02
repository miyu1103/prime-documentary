# サムネ用「感情の顔」プロンプト — EP52〜59（v001 / 2026-08-01）

Codex に**このファイルだけ**渡せば着手できます。設計書もリポジトリも読む必要はありません。

## 共通仕様（全8枚に適用）

- **出力**: 1920×1080 PNG、16:9
- **保存先**: `H:\pd-media\assets\ai\<slug>\thumb\<SLUG>_FACE_v001.png`（slug は各節の見出しに記載）
- **構図（CTR_PLAYBOOK §4A）**:
  - 顔ひとつだけ。**顔の高さが画面高の 50〜65%**。**目線が上から1/3の線**、あごが下から1/3付近
  - 顔は**左右どちらかの1/3に寄せる**。反対側の**約40%は空ける**（後で文字を入れる。何も置かない）
  - 背景は**暗く・彩度を落とし・強くぼかす**。顔だけ明るい
  - 顔の輪郭に**暖色のリムライト**（背景から分離させる）
- **画づくり**: シネマティック、被写界深度浅め、フィルムグレイン薄く、実写風だが**実在の人物に似せない**
- **絶対禁止**: 実在人物の肖像／文字・ロゴ・透かし／血・傷・拷問の描写／子どもの顔／手錠で拘束された屈辱的構図／複数の顔
- **表情が命**: 中立の顔は不可。**指定した感情を強く**出す（涙・呆然・恐怖・怒り）
- **ネガティブ**: `text, watermark, logo, extra faces, deformed hands, cartoon, 3d render, plastic skin, oversaturated, cluttered background, sharp background`

---

## EP52 morton — slug `morton`
**瞬間**: 25年後、隠されていた息子の証言記録を初めて自分の目で読む父。
**プロンプト**:
> Cinematic close portrait of a weathered white man in his mid-50s, Texas, plain work shirt, holding a single sheet of paper just below frame; his face caught in the second of stunned disbelief — eyes wide and wet, mouth slightly open, jaw slack, decades of held-back grief breaking through. Warm rim light from the left edge separates him from a very dark, desaturated, heavily blurred office interior. Face fills about 60% of the frame height, positioned in the right third, eyes on the upper-third line; the left 40% of the frame is empty dark negative space. Shallow depth of field, subtle film grain, photographic, not a real person.

## EP53 norfolk — slug `norfolk`
**瞬間**: 11時間の取り調べの果て、やっていない罪を認めてしまった直後の若い水兵。
**プロンプト**:
> Cinematic close portrait of an exhausted white man aged about 22 with a short military haircut, plain white t-shirt, in a windowless room at 4am; utterly spent — red-rimmed eyes staring at nothing, tear tracks dried on his cheeks, shoulders collapsed, the blank stare of someone who has just agreed to something untrue. Cold overhead source plus a warm rim light on the right edge; background almost black, desaturated, heavily blurred. Face fills about 58% of the frame height, in the left third, eyes on the upper-third line; the right 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

## EP54 flowers — slug `flowers`
**瞬間**: 6度目の裁判の判決を待つ、23年を court で失った男。
**プロンプト**:
> Cinematic close portrait of a Black man in his early 40s in a plain buttoned shirt, seated in a dim courthouse corridor in Mississippi; the expression is worn defiance held together by exhaustion — eyes fixed straight ahead and glassy, jaw set, one deep breath held. Warm rim light along the left edge, very dark desaturated blurred wooden interior behind. Face fills about 60% of the frame height, in the right third, eyes on the upper-third line; the left 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

## EP55 burge — slug `burge`
**瞬間**: 取調室で自分の身に起きたことを、誰も信じてくれないと悟った瞬間。**暴力そのものは描かない。**
**プロンプト**:
> Cinematic close portrait of a Black man in his late 20s, plain undershirt, in a bare Chicago police interview room lit only by one hanging bulb; the face shows dread and disbelief — eyes lifted toward something off-frame, brow tight, lips parted as if a question was cut off. No injuries, no restraints, no blood, nothing violent in frame. Warm rim light on the right edge against an almost black, desaturated, heavily blurred room. Face fills about 60% of the frame height, in the left third, eyes on the upper-third line; the right 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

## EP56 postoffice — slug `postoffice`
**瞬間**: 端末の画面に、自分が触れてもいない2,000ポンドの不足が表示された瞬間。
**プロンプト**:
> Cinematic close portrait of a white British woman in her early 50s, cardigan over a plain blouse, standing behind a village post-office counter at night; her face lit from below by a computer screen — the moment of cold disbelief, eyes narrowed at the display, colour draining, one hand half-raised toward the screen just below frame. Warm rim light on the left edge; the shop behind her is dark, desaturated, heavily blurred. Face fills about 58% of the frame height, in the right third, eyes on the upper-third line; the left 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

## EP57 fieldtest — slug `fieldtest`
**瞬間**: 路上で、2ドルの試薬が青く変わったのを見せられた瞬間。
**プロンプト**:
> Cinematic close portrait of a white woman in her mid-30s, plain top, sitting in the passenger seat of a car on a Houston roadside at night; blue and red light washes across her face from outside as she looks toward something being held up just off-frame — pure alarm, eyes wide, breath caught, the beginning of a protest she knows will not work. Warm rim light on the right edge, the car interior behind almost black and heavily blurred. Face fills about 60% of the frame height, in the left third, eyes on the upper-third line; the right 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

## EP58 lejeune — slug `lejeune`
**瞬間**: 娘を亡くしてから十数年後、基地の水質記録を初めて手にした父。
**プロンプト**:
> Cinematic close portrait of a white man in his early 50s with a short military bearing, plain shirt, standing in a dim kitchen; he holds a plain glass of water at chest height, just entering frame, and stares at it — grief and slow-building anger together, eyes wet and unblinking, mouth a hard line. Warm rim light on the left edge; the kitchen behind is very dark, desaturated, heavily blurred. Face fills about 60% of the frame height, in the right third, eyes on the upper-third line; the left 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

## EP59 robosigning — slug `robosigning`
**瞬間**: 現金で買った自分の家の玄関に、銀行の南京錠が掛かっているのを見た瞬間。
**プロンプト**:
> Cinematic close portrait of a white man in his early 60s, work jacket, standing on the porch of a Florida house at dusk; he looks down at a padlock on his own front door just below frame — disbelief hardening into fury, brows drawn, jaw clenched, one breath from shouting. Warm rim light on the right edge; the house behind is dark, desaturated, heavily blurred. Face fills about 60% of the frame height, in the left third, eyes on the upper-third line; the right 40% is empty dark negative space. Shallow depth of field, film grain, photographic, not a real person.

---

## 納品後にこちらでやること
1. `scripts/build_thumbs_ctr_v2.py --slug <slug> --face <生成画像>` で組版（4語・白＋黄／顔と反対側の空きスペース）
2. `check_thumb_subject_luma.py` で可読性検査（文字高≥150px・輪郭≥12px・被写体輝度≥60）
3. 合格したものだけを `thumbnail.selected.v001.png` に採用し、公開前に差し替え

**各話1枚で十分です。** 表情違いで2〜3枚あれば私の側で選べるので、余裕があれば複数枚ください。
