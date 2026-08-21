# EP76 · MORANDI — FOOTAGE PLAN v001

**Every number in this document was measured against the archive on 2026-08-21 before the query set
was written.** That is what `config/episode_footage_queries.v001.json` demands of itself, and the
reason it demands it is on the record: a previous episode wrote 38 descriptive-phrase queries and
**37 of them returned zero rows**.

Counts are
`py -3.11 scripts/search_archive.py "<term>" --kind video --limit 5000 --paths-only | wc -l`.
Eighty-six terms were probed in round one and forty-eight replacements in round two.
**Nothing was taken on its count alone**: every term below that survived was also read.

---

## 1. THE HEADLINE FINDING IS POSITIVE, AND THAT IS NEW

EP75 lahaina's plan opens by reporting that the shelf could not carry a single one of its subject
registers. **This one is the opposite, and the reason is the subject.** This film is about *the thing
you do without thinking* — driving over a structure somebody else inspects — and about paper. Both
are registers where **place does not matter**, and both are the shelf's strongest holdings.

| register the film needs | measured supply | verdict |
|---|---|---|
| an ordinary car on an ordinary elevated road | `road traffic` 303 · `car traffic` 265 · `highway traffic` 117 · `urban traffic` 102 · `night road` 53 · `tunnel` 68 · `asphalt road` 35 | **the shelf carries it** |
| a working container port | `dock` 46 · `shipping` 34 · `cargo ship` 33 · `shipyard` 23 · `container ship` 9 | **carried.** Genoa is a port, and this is the one *place* register the shelf actually has |
| hands and paper at a desk | `typing` 80 · `office desk` 78 · `writing` 66 · `keyboard` 62 · `notebook` 39 · `hands writing` 37 · `hands typing` 28 · `documents` 12 · `library` 111 | **carried, and clean.** ACT_3 and ACT_4 run on this |
| sky and texture | `timelapse` 906 · `fog` 154 · `particle` 98 · `cloudscape` 79 · `dust` 52 · `rainy` 27 · `grain` 15 · `haze` 12 · `puddle` 10 | carried |
| the valley floor beneath the bridge | `excavator` 45 · `industrial` 20 · `warehouse` 19 · `freight` 15 | thin but real; supplemented by plates |

## 2. WHAT THE SHELF DOES NOT HAVE — the film's own texture

This is the gap `V001`–`V120` was written to fill, and it is total:

| probe | rows |
|---|---|
| `corrosion` · `rebar` · `girder` · `viaduct` · `scaffolding` · `cracked wall` · `guardrail` · `roadworks` | **1 each** |
| `hillside` · `shutters` | **1 each** |
| `rooftops` · `genoa` · `overpass` | 3 each |
| `balcony` | 4 |
| `steel` · `welding` | 6 each |
| `cement` | 8 |
| `rust` · `warehouse` | 19 |
| `concrete` · `industrial` | 20 |

**There is no weathered prestressed concrete on this shelf, and there is no Ligurian street on it
either.** Both were expected and both are commissioned.

## 3. SUBSTRING TRAPS — measured by reading what came back, not by guessing

The config's own `_why` warns that terms are ANDed substring matches. Every one of these looked like
a strong term on its count and is unusable:

| term | rows | what it actually returns |
|---|---|---|
| `port` | 554 | trans**port**ation, **Port**ugal, **port**al, s**port**s. The real port clips are a minority |
| `rain` | 491 | t**rain**ing, t**rain**ers, railway — **and "money raining", which is itself a forbidden subject** |
| `paper` | 914 | news**paper**, and "beautiful wall**paper**" national flags and landscapes. **A legible newspaper is a `fabricated_record`** |
| `hand` / `hands` | 807 / 723 | people eating pizza, dancing, stirring coffee. Not a paperwork register at all |
| `file` | 30 | pro**file**s, "video **file**", "the **filed**" |
| `beam` | 30 | a gymnast's balance beam, sun**beam**s, stage light beams. **Zero structural beams** |
| `stamp` | 12 | passport stamps and rubber stamps **carrying readable text** |
| `toll` | 6 | entirely a**toll** — tropical reef and lagoon |

**The replacements were measured too**, and that is the half that matters: `port` → `dock` 46 /
`shipping` 34 / `cargo ship` 33, all clean; `paper` → `documents` 12 / `office desk` 78, all clean;
`hand` → `hands writing` 37 / `hands typing` 28, all clean.

## 4. THE MOST DANGEROUS TERM IN THIS EPISODE IS `italy`

`italy` returns **84 rows**, and they are **Venice gondolas, Tuscan cypress avenues, the Dolomites
and a piazza fruit stand** — precisely the holiday-Italy register that this episode's `era_setting`
and 59 `forbidden_subjects` exist to bar.

The obvious search term for an Italian film is the one that will wreck it. **`italy` is excluded by
subject, not by count.**

## 5. CONDITIONAL — kept, but never taken on the count alone

| term | rows | why it needs the contact sheet |
|---|---|---|
| `city street` | 230 | Mexico City, Bogotá, Basel. A legible foreign street is the same error class as a US route shield |
| `construction` | 140 | welders and excavators, but also birds and cathedrals. Prefer `excavator` (45) |
| `cloudscape` | 79 | heavy with drone sunsets and golden hour, which this film bars outright |
| `corridor` | 55 | largely sci-fi and horror 3D tunnels. `library` (111) is the better institutional interior |
| `railway` | 52 | Japan, Switzerland, Disneyland, snow |
| `crane` | 43 | port and construction cranes **mixed with crane birds** |

## 6. THE KEPT QUERY SET — 34 terms, measured

Written to `config/episode_footage_queries.v001.json` under `episodes.morandi`.

```
road traffic 303 · car traffic 265 · urban traffic 102 · highway traffic 117 · night road 53
asphalt road 35 · tunnel 68
dock 46 · shipping 34 · cargo ship 33 · shipyard 23 · container ship 9
office desk 78 · typing 80 · writing 66 · keyboard 62 · notebook 39
hands writing 37 · hands typing 28 · documents 12 · library 111
timelapse 906 · fog 154 · haze 12 · particle 98 · dust 52 · grain 15 · rainy 27 · puddle 10
excavator 45 · industrial 20 · warehouse 19 · stairs 20 · city aerial 88
```

**Supply measured: 3,067 rows across 34 queries** (with overlap between them).

- Clip floor for this runtime: `1798.6 s / 45 s` = **40 distinct clips minimum**. Target **60**.
- `episode_spec.distinct_video_assets` = **265**.
- **3,067 ≥ 265 ≥ 60 ≥ 40.** The supply clears every floor with margin.

**A hit count is not a supply count, and this document says so plainly.** These 3,067 rows are
substring matches on human-written titles. What survives the forbidden-subject sweep, the era check
and a person looking at a contact sheet will be a fraction of it. The number proves the shelf is not
empty for these registers; it proves nothing about any individual clip.

## 7. DIVERSITY AND UTILISATION FLOORS — declared

Measured against the projected master (1,789.6 s) and `episode_spec`:

| floor | value | where it comes from |
|---|---|---|
| footage diversity, distinct share | **≥ 0.40** | `check_final_acceptance.footage_diversity` |
| max reuse of any one clip | **≤ 4×** | same |
| generic-symbol clips (scales, gavels, clocks) | **≤ 2** | same |
| footage utilisation | **≥ 1 distinct factory clip per 45 s = 40** | `FACTORY_SECONDS_PER_CLIP` |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| cross-episode | `check_cross_episode_reuse.py` **before** staging | identity is by content, not filename |

**EP68 pinto and EP69 hyatt have already spent this shelf's industrial and engineering registers,
and EP71 oroville its infrastructure ones.** Run the cross-episode check first, not after.

## 8. WHAT MUST HAPPEN BEFORE A CLIP ENTERS A CUT

1. **`check_cross_episode_reuse.py` runs first.** Three siblings have already drawn on the same
   registers.
2. **A person opens a labelled contact sheet** of the road, port, paper and texture registers.
   `footage_review_required` is `true` in the spec and **no gate in this pipeline ever looks at an
   image**. The factory shelf's labels are known to be wrong.
3. **Nothing that shows a legible foreign street, a US route shield, a right-hand-drive vehicle, or
   any of the 59 `forbidden_subjects`** — 12 of which are the holiday-Italy family.
4. **Nothing at golden hour.** The film has three light states and none of them is pretty.
