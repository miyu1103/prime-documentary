# Real PD asset sourcing — PD-2026-002-gideon (v001)

Per brief §"Real PD assets first" + 0004 §D/§E2 (floor: **8–12 distinct real inserts where real
material exists**) + invariant 11 (AI only for the never-recorded, labelled). Every entry is
public-domain (US federal works) or an explicit no-known-restrictions archive record; each is
rights-logged in `09_package/rights_manifest` on acquisition (content_hash + rights_basis +
verified_at). Verified via web research 2026-06-17.

## Hero + primary real assets (verified sources)

| # | Asset | Source / ID | Rights basis | Direct URL / acquisition | Use (scene) |
|---|---|---|---|---|---|
| R1 | **Gideon's cert petition** (handwritten pencil, prison stationery) — HERO | National Archives, **NAID 597554** ("Petition for Writ of Certiorari, Gideon v. Cochran", 1/5/1962) | US federal court record — public domain, no restrictions | catalog.archives.gov/id/597554 (digital object JPG/PDF via NARA catalog/API) | S001 hook push-in; S009–S010 |
| R2 | **Gideon's 1961 habeas petition** (alt document) | Florida Memory **item 339319** (State Archives of Florida) | State archive, no known copyright restriction | floridamemory.com/items/show/339319 | S008–S010 document layer |
| R3 | **Oral-argument audio, 1963-01-15** (Abe Fortas for Gideon, ~53 min, 2 parts) | Oyez / NARA SCOTUS recording, case 1962/155 | US Supreme Court recording — public domain (federal gov work) | s3.amazonaws.com/oyez.case-media.mp3/case_data/1962/155/19630115a_155_part1.delivery.mp3 (+ part2) | S013–S015 (the Court hears it); authentic VO texture |
| R4 | **Opinion 372 U.S. 335** (full text, for on-screen quote) | Library of Congress, U.S. Reports vol. 372 | US federal court opinion — public domain | tile.loc.gov US Reports (usrep372335) — verify exact PDF URL | S016 (6th Amendment reasoning quote) |
| R5 | **Hugo Black portrait** | LoC Prints & Photographs **item 2006687493** (Harris & Ewing), repro LC-USZ62-46836 | "No known restrictions on publication" — public domain | loc.gov/pictures/item/2006687493/ (download highest-res TIFF/JPG) | S015 (opinion author) |
| R6 | **1960s Florida / courthouse / prison / pool-hall B-roll** (3–5 clips) | Prelinger Archives / Universal Newsreel on archive.org | Prelinger PD / US gov newsreel PD | archive.org — select specific item IDs (search "1960s Florida courtroom", "prison 1960s", "pool hall") | S002, S004, S007, S020–S024 texture |

> R1–R5 are specific verified records. R6 needs item-ID selection on archive.org (multiple clips →
> several distinct inserts, helping clear the 8–12 floor). Petition pages + portrait + opinion-quote +
> audio segments each count as distinct real moments.

## Acquisition status (2026-06-17) — floor 8–12 MET (8 acquired)
ACQUIRED to `05_visuals/real/` + rights-logged (rights_manifest AST-0200..0221, all hashes verified):
- **R1 petition** — 5 pages (`gideon_petition_cert_p1..p5.jpg`); p1 = the iconic pencil/prison-stationery
  hero ("No. 890 Misc. OCT TERM 1961, To: Earl Warren"). Via Wikimedia Commons (NARA NAID 597554).
- **R3 oral-argument audio** — `..._part1.mp3` (12.4 MB) + `..._part2.mp3` (28.9 MB). Oyez/NARA, PD.
- **R5 Hugo Black portrait** — `hugo_black_portrait_loc.jpg` (LoC LCCN 2014718460, PD). *Note: a
  younger Black; consider swapping for a Justice-era PD portrait later (cosmetic).*

REMAINING (recommended, floor already met):
- **R6 B-roll** — select 3–5 archive.org Prelinger / Universal-Newsreel PD clips (1960s FL courthouse /
  prison / pool hall). Needs clip viewing (editorial) → owner inbox or curated download.
- **R4 opinion 372 U.S. 335 PDF** — LoC US Reports (LoC blocks headless; owner download or Justia text
  for the on-screen quote — the quote text is already in claims).
- NARA/LoC headless note: their sites resist scripted download (SPA / 403); the reliable path is
  Wikimedia Commons direct file URLs (used here) or the owner download-to-inbox workflow.

## Rights protocol (0004 §N)
On acquisition, each real asset gets a rights_manifest entry: `producer` (NARA/LoC/Oyez/Florida
Memory/Prelinger), `license` = the PD/no-restriction basis above, `content_hash` (sha256 of the
downloaded file), `needs_verification: false`, `source_url`. Real assets are genuine evidence (not
synthetic) — no "reconstruction" label needed; they strengthen credibility per §D.
