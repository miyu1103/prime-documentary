# EP70 · THE WRONG HOUSE — IDENTITY NOTE v001

**Written 2026-08-12, the same day the episode was created, so that nobody reading this repository later
reads one episode as two.**

## The episode

| | |
|---|---|
| **Episode id** | `PD-2026-070-wronghouse` |
| **Slug** | `wronghouse` |
| **Topic id** | `TOP-20260812-001` |
| **Subject** | *Martin v. United States* — the FBI raided the wrong house in suburban Atlanta on 18 October 2017; the case is still live in 2026 |
| **Runtime tier** | 45:00 (new tier for this channel) |
| **Score** | 110, FLAGSHIP, `pd_planning_os.v002.json` |

## The renumber

This episode was **created at `PD-2026-071-wronghouse`** and **corrected in place to
`PD-2026-070-wronghouse`** a few hours later, on the same day, before any render, upload or approval.

**Why it was created at 071.** At creation time `episodes/PD-2026-070-oroville/` existed on disk.
`check_final_acceptance.py` takes a bare episode number, so two directories numbered 070 would have
collided in tooling, and `scripts/create_episode.py` refuses to overwrite an existing episode id. 071 was
the next free number.

**Why it was corrected to 070.** The Oroville work migrated to `PD-2026-071-oroville` (now at
`script_verified`, 30 minutes), which freed 070. The owner's assignment is explicit:

> **EP70 = *Martin v. United States*, 45 minutes. EP71 = Oroville, 30 minutes.**

**How it was corrected.** `episode_id` was edited in place in `manifest.json` and
`episode_spec.v001.json`, the directory was moved, and an `EPISODE_RENUMBERED` event was appended to
`events.jsonl`. Nothing was regenerated and no id was minted twice. **There is one episode here.**

## What was renamed, and what deliberately was not

| Artefact | Name now | Renamed? |
|---|---|---|
| Episode directory | `episodes/PD-2026-070-wronghouse/` | yes |
| Machine contract | `episodes/PD-2026-070-wronghouse/episode_spec.v001.json` | id corrected in place |
| Facts ledger | `episodes/_planning/EP70_wronghouse_FACTS_LEDGER.v001.md` | yes |
| Design document | `episodes/_planning/EP70_wronghouse_FILM_BIBLE.v001.md` | yes |
| Script | `episodes/_planning/EP70_wronghouse_script.en.v001.md` | yes |
| Cached sources, normaliser, quotation verifier | `episodes/PD-2026-070-wronghouse/01_research/sources/` | moved with the directory; `SRC-000N` names unchanged, so every offset in `verified_offsets.v001.json` still resolves |
| **Register measurement** | **`episodes/_planning/measurements/EP71_WRONGHOUSE_REGISTER_INVENTORY.v001.json`** | **NO — deliberately kept** |
| **Register measurement generator** | **`episodes/_planning/measurements/EP71_wronghouse_registers.py`** | **NO — deliberately kept** |

**Why those two keep the `EP71_` prefix.** They are a signed measurement and the script that signs it.
The JSON records the run that produced it; the script writes that exact filename and reuses
`EP70_45min_pool.py` unmodified to rebuild the 26,101-clip pool. Renaming them would either break the
regeneration or silently produce a file whose name no longer matches the run recorded inside it. The
repository's own rule for this situation — *a scored or signed artefact keeps its name* — applies, and the
mismatch is documented here rather than tidied away. **`EP71_…REGISTER_INVENTORY` belongs to EP70. It is
not an Oroville file.**

## Two live constraints that outlast this note

1. **The case is not over.** The Eleventh Circuit heard argument on remand on **25 March 2026** and, on
   the record retrieved on 12 August 2026, has not ruled. §9 of the facts ledger is the only part of the
   film that can go stale, and it must be re-verified **before the render** and again **before
   scheduling**. If a ruling lands, ACT_6 and the ending are rewritten, not patched.
2. **Name the actor the record names.** This is a **federal** case about an **FBI** raid. The raiding
   party was a six-member FBI SWAT team led by an FBI special agent; Atlanta Police Department officers
   were staged outside. The defendant is the **United States**, sued under the Federal Tort Claims Act.
   *Police raided*, *Atlanta police raided*, *the state*, *the city*, *Georgia* and *cops* are all
   factually wrong, and they are wrong in the way a viewer who knows the case catches instantly.
   `config/ship_policy.v001.json` puts title and thumbnail text in the **blocking** `factual_support`
   class, so this is not a style preference: every figure, name and outcome on a title or a thumbnail must
   be locatable in the script or the facts ledger with the row cited, and a claim graded uncertain never
   reaches a thumbnail. It is written into `episode_spec.forbidden_claims` as entry 23.
