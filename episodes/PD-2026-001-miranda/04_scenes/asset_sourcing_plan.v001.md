# Asset sourcing plan — PD-2026-001-miranda (v001)

Maps each scene to a **real-first** visual/audio source per `decisions/0002` §L (real archival),
§N (channel-survival / rights gate) and invariant 11 (AI stays clearly symbolic).

**Status:** CANDIDATE sources only. Every real asset is UNVERIFIED until `rights-editor` records a
`rights_basis` (`public_domain` | `licensed` | `fair_use`) + `source` + `verified_at` in the rights
manifest. No asset ships without it (decision §N is a hard publish gate). `verified_at` required
because availability/terms are time-sensitive (rule 13).

## Real source pools (public-domain candidates)

- **Oral-argument audio (1966)** — US Supreme Court recording, US-gov work → public domain.
  Prefer the National Archives / Internet Archive copy for monetized use; **avoid Oyez's processed
  version if it carries a CC BY-NC (non-commercial) term.** Verify at download.
  - Internet Archive: `archive.org/details/USSupremeCourtMirandavArizonaOralArgument1966`
- **Opinion text** — *Miranda v. Arizona*, 384 U.S. 436 (1966), official US Reports → public domain.
  - Library of Congress PDF: `tile.loc.gov/storage-services/service/ll/usrep/usrep384/usrep384436/usrep384436.pdf`
- **Era B-roll video** — **Universal Newsreel** (1929–1967), deeded to NARA without copyright
  restrictions → public domain (verify each clip for embedded third-party IP per NARA notice).
  - Internet Archive: `archive.org/details/universal_newsreels` ; **Prelinger Archives**:
    `archive.org/details/prelinger`
- **Stills** — justice official portraits (Warren, Harlan, White; US-gov → PD), US Constitution /
  Bill of Rights (National Archives → PD), SCOTUS building photos (PD/gov).

> The actual interrogation, confession, and retrial were **never filmed/recorded**. Those scenes use
> AI **symbolic reconstruction**, on-screen-labelled, never shown as authentic (invariant 11).

## Per-scene plan

| Scene | Visual mode | Real-first source (candidate) | Real audio underlay | AI symbolic |
|---|---|---|---|---|
| S001 | typography | — (Remotion kinetic) | — | — |
| S002 | typography | Constitution / 5th Amend. still (NARA, PD) | — | — |
| S003 | map | 1960s Phoenix/AZ newsreel B-roll (Universal) + map gfx | — | — |
| S004 | reenactment | generic 1960s police-station exterior B-roll (lead-in) | — | **interrogation room (labelled)** |
| S005 | diagram | — (Remotion) | — | — |
| S006 | typography | — (Remotion) | — | — |
| S007 | archival_illustration | courtroom B-roll (Universal/Prelinger) | — | symbolic courtroom fallback |
| S008 | abstract | opinion PDF page (LoC, PD) | — | — |
| S009 | typography | four case captions (opinion, PD) | **oral-argument clip (short)** | — |
| S010 | diagram | — (Remotion) | — | — |
| S011 | breathing | era atmosphere B-roll (PD) | — | — |
| S012 | timeline | opinion "June 13, 1966" + Warren portrait (PD) | **ruling/oral-argument clip** | — |
| S013 | typography | historical Miranda warning card image (verify) | — | clean card fallback |
| S014 | object | US Constitution / Bill of Rights still (NARA, PD) | — | — |
| S015 | typography | Harlan + White portraits (PD) | — | — |
| S016 | object | police "rights" card photo (verify) | — | card object fallback |
| S017 | diagram | — (Remotion) | — | — |
| S018 | archival_illustration | opinion doc page (PD) | — | **retrial symbolic (labelled)** |
| S019 | diagram | — (Remotion) | — | — |
| S020 | transition_texture | PD light/dust B-roll or Remotion | — | — |
| S021 | typography | — (Remotion) | — | — |
| S022 | abstract | 1960s prison B-roll (Prelinger, verify), stylised | — | **jail-bars light (labelled)** |
| S023 | typography | — (Remotion brand end-card) | — | — |

## Hand-off

- `research-director` + `rights-editor`: acquire the candidates above, verify + record rights basis,
  store under the SSD media tree (`05_visuals/real/`, `06_audio/real/`), and register each asset.
- `visual-director`: update `scene_plan` `required_assets` to reference the chosen real asset IDs
  (real-first), keeping AI-symbolic entries only where no real material exists.
- All AI-symbolic, real-vs-reconstruction labelling, and rights manifest entries are publish-gated
  (decision §N).
