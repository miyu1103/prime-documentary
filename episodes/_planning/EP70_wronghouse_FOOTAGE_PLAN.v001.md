# EP70 wronghouse — FOOTAGE PLAN v001

*Martin v. United States.* Atlanta, Fulton County, Georgia. 1973–2026. Written 2026-08-20,
after the H: archive drive failed and took the shelf this plan would normally have been
measured against.

**Read §3 before writing any query for any episode.** It is the expensive part of this
document and it is not about EP70.

---

## 1. What the episode needs

`episode_spec.v001.json` declares `distinct_video_assets: 300` and 209 `forbidden_subjects`.

The register splits, and the split matters more than the range:

- **96% is 2017–2026 and contemporary.** The spec says so in terms: "a 2020s suburban front
  door, a 2020s patrol light, a 2020s courthouse corridor are all in period." Modern American
  stock is the CORRECT dressing here, not a compromise.
- **ACT_4 alone is April 1973 – 1974** (Collinsville, Illinois; the Senate Committee on
  Government Operations; the FTCA amendment). Nothing contemporary may appear in it: no mobile
  phone, no flat screen, no modern vehicle, no LED, no modern signage, no laptop, no bodycam.

Registers, in the order the film needs them:

| # | register | what it dresses |
|---|---|---|
| R1 | suburban house exterior — porch, lawn, fence, mailbox, driveway, roof | the two houses three doors apart |
| R2 | door and entry — doorway, handle, threshold, gate | the raid itself, told without depicting it |
| R3 | domestic interior — hallway, room, bedroom, kitchen, window, curtain, stairs | the inside of an ordinary house |
| R4 | street and neighbourhood — road, sidewalk, driving, car, truck, night, dusk, rain | Atlanta suburbia, and the drive to it |
| R5 | legal and government — courthouse, court, government, marble, office, desk, paper, document, file | the Eleventh Circuit and the Supreme Court |
| R6 | enforcement — police, patrol | the agents, without a real-person likeness |
| R7 | Georgia landscape — forest, pine, trees, field | establishing |
| R8 | 1973 period — vintage, retro, telephone, radio, television, typewriter | ACT_4 only |

## 2. What the shelf held on 2026-08-20

Measured with `scripts/measure_shelf_for_episode.py` against the rebuilt ledger
(`E:\pd-archive\_ledger`), counting only rows whose `license_decision` is `pd`, and
subtracting any hit whose FILENAME carries one of the 209 forbidden words — because
`check_spec_satisfied` matches those against the staged filename, so such a clip is an
automatic build failure however good it looks.

**14,453 video rows, 13,116 with a clear commercial licence.** Word counts, high to low:
road 646, forest 516, walking 316, street 313, trees 304, computer 276, car 270, night 265,
office 189, vehicle 151, hands 142, house 140, rain 118, driving 115, desk 96, home 78,
fence 72, door 69, corridor 47, window 44, police 43, truck 43, vintage 38, retro 25,
typewriter 17, stairs 16, court 16, sidewalk 15, government 15, hallway 12, kitchen 12,
patrol 10, bedroom 9, judge 9, curtain 8, porch 5, lawn 5, lawyer 5, garage 4, courthouse 4,
marble 4, suburb 3, mailbox 3, neighborhood 3, telephone 3.

Below the floor and therefore absent from the query set: driveway, doorway, doorbell,
residential, streetlight, blinds, carpet, columns, badge, siren, folder, lock, hinge,
threshold, staircase, van.

Those counts are real. **They are also almost entirely useless, and §3 is why.**

## 3. THE LESSON. A hit count is not a supply count, and I proved it the expensive way.

A query set was built from the counts above — 72 terms, 6,297 net candidates — and run through
`prestage_footage_review.py`: 554 candidates in, 208 dropped mechanically, **346 presented for
a content verdict across 121 contact sheets.**

Five sheets were sampled from across the range. **All five were a total loss:**

| sheet | what was actually in it |
|---|---|
| 1 | a red semi on a Mexican desert highway; aerial of a green Latin-American mountain valley |
| 2 | sunset road lined with cactus; a blonde woman's face filling a car interior |
| 40 | **Copenhagen** — the lakes, the harbour, the red-tiled roofs, twice |
| 80 | **3D CGI office renders with green and blue chroma-key screens** |
| 110 | **a Japanese pagoda at sunset; a tropical ferry; the Black Forest** |

So: `road 646` is the count of the WORD in the titles of international scenic stock.
`office 189` is chroma-key CGI. `forest 516` is the Black Forest. `sky` and `clouds` are a
ferry in the tropics.

`EP69_hyatt_FOOTAGE_PLAN.v001.md` warns about exactly this, and this plan quoted the warning
into `config/episode_footage_queries.v001.json` **while committing the error in the same
breath.** Reading a rule is not the same as obeying it.

**Why the old shelf worked and this one does not.** The lost `asset_manifest.v001.json` —
88,850 entries — was organised by SUBTYPE: `front_door_house` 328, `courthouse_steps` 313,
`long_shadow_of_a_person` 313, ~300 items per subject. The subject was the unit of storage.
What survived the drive failure is filed by download THEME with free-text titles, so a word
query retrieves whatever happens to contain that word. The structure is what was lost, not
just the files.

**What to do instead.** `ingest_modern_web.py`'s themes carry SUBJECT PHRASES, not words:
`"suburban street driving"`, `"porch of old house"`, `"mailbox rural road"`,
`"federal building entrance"`, `"government office corridor"`, `"eviction notice posted door"`,
`"police car night lights"`. Those go to the Pixabay/Pexels APIs as phrases. Fetch the register
rather than filtering for it.

That download was started 2026-08-20 11:00 across `small_town`, `government_buildings`,
`courtroom_justice`, `household_loss`, `police_modern`. **It is not clean either** — inside
the first 65 items it returned `mosque-masjid-islamic-dome` for a government-landmark phrase.
Phrase search raises the hit rate; it does not remove the need to look.

## 4. The query set

`config/episode_footage_queries.v001.json` → `episodes.wronghouse`, 72 terms, every one
measured, none colliding with a forbidden word. **It is retained but it is not sufficient**,
for the reason in §3. It selects candidates; the contact sheets decide.

Deliberately dropped despite having counts: `archive` (3) — every row lives under
`D:\pd-archive`, and an earlier pass matched the folder name 1,928 times, so the word cannot
be trusted here; `stack` and `uniform` — too generic to mean anything in this register.

## 5. Where this stands

- i2v started 2026-08-20 10:58 on EP70's 160 plates, target 60 motion clips. This raises the
  video pool from the episode's own purpose-made material and needs no shelf at all.
- With `factory=0` and `motion=100`, `solve_totals` gives 260 cuts over 2,389.7 s — a 9.2 s
  mean, which is the slow, static feel the channel is trying to leave behind. With
  `factory=131, motion=60` it gives 351 cuts at 6.8 s. **The staged pool is what buys pace**,
  which is why the download matters and why a thin, wrong pool is worse than a smaller right one.
- Nothing has been staged into `remotion/public/wronghouse/factory`. The 121 sheets from the
  word-query run should be discarded rather than reviewed: re-run `prestage_footage_review.py`
  after the download lands, and read the sheets it builds then.
