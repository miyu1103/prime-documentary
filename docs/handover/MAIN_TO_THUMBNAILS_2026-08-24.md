# Main thread → Thumbnail lane, 2026-08-24

**Make the thumbnails for EP71 through EP76 — six episodes — to the standard you set on
EP77–EP82.** Everything you need is already on disk. Details are yours; this note is the ask, the
inputs, and the two things that would waste your time if nobody said them.

---

## The ask

Six episodes, all finished or nearly finished films, all going out between 26 and 31 August:

| | slug | episode dir | publishes |
|---|---|---|---|
| EP71 | oroville | `episodes/PD-2026-071-oroville` | 8/26 |
| EP74 | itaewon | `episodes/PD-2026-074-itaewon` | 8/27 |
| EP75 | lahaina | `episodes/PD-2026-075-lahaina` | 8/28 |
| EP76 | morandi | `episodes/PD-2026-076-morandi` | 8/29 |
| EP72 | lacmegantic | `episodes/PD-2026-072-lacmegantic` | 8/30 |
| EP73 | uri | `episodes/PD-2026-073-uri` | 8/31 |

Deliver to `episodes/<EPID>/09_package/thumbnail.selected.v001.png`, 1280×720.
**Overwrite what is there.** What is there now is mine, it is placeholder, and it is meant to be
replaced — see "Why you and not me" below.

## Why you and not me

I looked at your EP77–EP82 set beside my five. Yours is a different standard and the difference is
not subtle:

* **two or three words, one of them red.** `A LOOSE / WIRE.` `FAILED / BEFORE.` `STILL / ABOARD.`
  Mine carry an explanatory second line — "the railway's own minimum was nine" — which nobody reads
  at 320 px. You cut the explanation; I kept it.
* **type left third, subject right two thirds, every time.** Six of yours side by side read as one
  channel. Mine are centred and the type sits on top of the picture.
* **one object, close.** A worn drill bit, a yoke, a bow, an oiled stone. Not one establishing shot
  in the set.
* **colour is designed** — deep blue with a single warm or red accent. Mine is white type with a
  black rim and no colour idea at all.

So: yours. Mine stay only until yours land.

## What is already on disk

**Commissioned CTR-first plates, six per episode**, in `episodes/<EPID>/10_thumbnail/T01.png` …
`T06.png` (EP74 has eight, from an earlier session, in its own naming). These were ordered on the
brief in `episodes/_planning/THUMBNAIL_ORDERS_2026-08-24/` — faces allowed and wanted, subject
filling half the frame, warm light against cold, clear space for type. Use them, re-order them, or
ignore them; the orders name what each concept was for.

**Headline candidates already checked against the record**, in `config/thumbnails/<slug>.json`.
Every one carries a `provenance` field naming the script line or ledger row it came from, and each
has been through `check_packaging_claims.py`. Take the words, change the words, but if you write a
new claim, run it through that script — a thumbnail states a claim, and `factual_support` is one of
the four classes that can stop a ship.

**The films themselves**, if you want a frame or a fact:
`episodes/<EPID>/08_edit/<slug>_final_bgm.v001.mp4` and
`episodes/_planning/EP<NN>_<slug>_FACTS_LEDGER.v*.md`.

## Two things that will cost you a round trip if I do not say them

Both measured today, both the hard way.

1. **The readability gate wants a 150 px letter, and a 150 px FONT does not make one.** Cap height
   is about 0.72 of the font size, so it takes ~215 px type. At that size a line holds roughly eight
   characters inside 1180 px — which is exactly why your two-word headlines work and my sentences do
   not. Check with:
   `py -3.11 scripts/check_thumb_subject_luma.py --ep <EPID> --thumb <png>`
2. **A bright area in the plate counts as an un-outlined "bright core" and scores the whole
   thumbnail outline 0 px.** A white card and an overcast sky both did it to me. Two fixes that
   work: keep the plate's highlights under luma ~185, and stroke the type properly (a ring of
   offset copies looks outlined and measures as zero — the gate dilates the bright core and asks
   how far the darkness extends, and overlapping copies leave no continuous rim).

There is a generic compositor at `scripts/build_case_thumbnails_from_plates.py` if it is useful
(`--slug <slug>`, reads `config/thumbnails/<slug>.json`, refuses a headline it cannot set inside
the frame rather than clipping it). Use it or don't — the deliverable is the PNG.

## Timing, and why nothing is blocked on you

The long-form uploads run at 16:05 daily (`PD-LongformPush`), starting with EP71 tomorrow, and they
will go out with my placeholders if yours are not ready. **That is fine and intended.** A thumbnail
can be replaced after publication for 50 quota units — `thumbnails.set` — so send them whenever
they are right and this thread will swap them in, published or not.

Order of use, if you want to work in the order they go out: oroville, itaewon, lahaina, morandi,
lacmegantic, uri.
