/**
 * Florence — EP37 assembly composition (Florence v. Board of Chosen Freeholders).
 *   Case: a paid fine that a database never cleared → a wrongful arrest → two
 *   jailhouse strip-searches → a 5–4 Supreme Court decision on the Fourth Amendment.
 *
 * BUILD STATUS — DETERMINISTIC 106-CUT ASSEMBLY (04_scenes/assembly_spec.v001.md).
 *   This SUPERSEDES the earlier 36-beat provisional scaffold. Every cut's duration is
 *   locked to the ElevenLabs master (`florence_words.json`, 1510 words @30fps): the
 *   timeline is linear and equals the master audio (0.00 → ~542.93s ≈ 9:03). Cut i runs
 *   for DUR[i] frames (= next cut's word-window start − this cut's start). `FLORENCE_WORDS`
 *   now carries real per-word timings, so `WordBand` renders live word-synced captions.
 *
 * STRUCTURE (owner 2026-07-13): COLD-OPEN HOOK FIRST. The hook (cuts 1-4) plays at video 0;
 *   the canonical BrandOpening sting is OVERLAID right after it (never before), then the body
 *   continues, then BrandEndcard (9s). florenceDuration = 16288 + 270 = 16558f ≈ 9:12.
 *   Narration is 0-based (no lead); runtime_band stays the sole owner APR.
 *
 * ASSET POLICY (all motion is continuous LINEAR velocity so the body clears the
 * animation_density floor; a screen-blend fill light clears the body-luma floor):
 *   - `d(name)` 2.5D parallax from SAM2 fg/bg pairs in _p08sam/ (S01 S03 S05 S06 S08 S11
 *       S12 S13 S14 S16 S19; S08/S11-S14 depth-threshold pairs added 2026-07-13).
 *   - `kb(name)` Ken-Burns a distinct flat still in florence/flat/ (variant sub-cuts).
 *   - `fx(name)` factory B-roll video (florence/factory/, QC'd in 05_visuals/
 *       factory_clip_qc.v001.json) at 14 meaning-matched cuts — real moving footage that
 *       cuts the near-still fraction and satisfies factory_used.
 *   - 3D Room `_set/*.mp4` across 3 distinct Blender passes, each reused ≤4.
 *   - 5 bespoke anims (self-contained 180f); multi-cut spans use `<Span off>` to CONTINUE.
 *   - `<NarrationCaptions/>` burns the film-timed florence_captions.json (caption_integrity).
 *
 * Safety (design §R2): strip-search beats are symbolic / non-graphic; no real-person
 * likeness; factory clips are QC'd for no faces / no overused scales motif.
 *
 * AUDIO: `<Audio narration_master>` is mounted for Studio preview. The FINAL render is
 * produced with `--muted`; the 4-layer mix (narration + ducked BGM + ambience + SFX) is
 * muxed in ffmpeg (scripts/build_florence_audio.py, loudnorm I=-14); narration 0-based (hook-first).
 *
 * 16:9 1920x1080 @30fps (reads from BRAND via Root).
 */
import React from 'react';
import {
  AbsoluteFill, Series, Sequence, Audio, Img, OffthreadVideo, staticFile, interpolate,
  useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {BRAND} from '../brand';
import {
  EvidenceReveal, PenaltyVsProperty, CaseJourney, QuoteUnderExamination,
} from '../components/core5';
import {FilmGrain, VignetteBreath, LightRays} from '../components/motionkit';
import {BrandOpening, BrandEndcard, OPENING_SEC, ENDCARD_SEC} from '../components/Bookends';
import {WarrantScreen} from './florence/WarrantScreen';
import {RecordsDrawer} from './florence/RecordsDrawer';
import {ReceiptStamp} from './florence/ReceiptStamp';
import {VerdictSeam} from './florence/VerdictSeam';
import {BodyLine} from './florence/BodyLine';
import florenceCaptions from '../data/florence_captions.json'; // film-timed cue table (caption_integrity path A)

const FPS = 30;
const LEAD = 0.10; // caption onset-latency correction (s)

// Per-cut frame durations, generated from assembly_spec.v001 word windows (106 cuts).
// Σ = 16288 frames = 542.93s ≈ 9:03 = the master audio length. DO NOT hand-edit;
// regenerate from the spec if the word timings change.
const DUR = [164,101,100,211,126,202,166,165,113,96,154,218,94,151,54,178,229,214,94,160,175,130,99,83,65,140,92,66,154,256,233,150,157,109,244,86,95,122,164,156,93,184,166,106,250,98,203,103,338,160,200,163,71,133,123,172,301,34,68,126,85,119,196,155,136,181,185,124,147,171,253,86,148,159,192,173,196,289,68,65,167,280,136,159,102,319,181,77,325,94,123,227,108,83,96,193,198,99,192,281,112,97,241,160,106,146];

// ── shared leaf renderers ────────────────────────────────────────────────────
const P: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);

/** Continue a self-timed child (bespoke / core5) across a cut boundary without restart. */
const Span: React.FC<{off: number; children: React.ReactNode}> = ({off, children}) => (
  <Sequence from={-off}>{children}</Sequence>
);

/** OffthreadVideo full-frame 3D-room clip, optional dark dim. */
const Room: React.FC<{src: string; dim?: number}> = ({src, dim = 0}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <OffthreadVideo src={staticFile(`_set/${src}.mp4`)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    {dim ? <AbsoluteFill style={{background: `rgba(6,10,18,${dim})`}} /> : null}
  </AbsoluteFill>
);

/** Coordinated dolly-in 2.5D from a SAM2 fg/bg pair. LINEAR velocity (no eased ends)
 *  so the body/center is never near-still — the animation_density floor demands
 *  continuous per-frame motion, not motion that stalls at the cut boundaries. */
const Depth25D: React.FC<{name: string}> = ({name}) => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const bgS = interpolate(p, [0, 1], [1.00, 1.12]);
  const fgS = interpolate(p, [0, 1], [1.02, 1.24]);
  const fgX = interpolate(p, [0, 1], [0, 26]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${bgS})`}}><P src={`florence/_p08sam/${name}_bg.png`} /></AbsoluteFill>
      <AbsoluteFill style={{transform: `translateX(${fgX}px) scale(${fgS})`}}><P src={`florence/_p08sam/${name}_fg.png`} /></AbsoluteFill>
      <LightRays color={BRAND.color.gold} />
    </AbsoluteFill>
  );
};

/** Ken-Burns a distinct flat still. LINEAR constant-velocity zoom+pan (continuous
 *  center motion every frame); seed varies direction so repeats differ. */
const KenBurns: React.FC<{name: string; seed?: number}> = ({name, seed = 0}) => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const dir = seed % 4;
  const s = interpolate(p, [0, 1], [1.06, 1.24]);
  const dx = interpolate(p, [0, 1], [0, dir === 0 ? -36 : dir === 1 ? 36 : dir === 2 ? -18 : 24]);
  const dy = interpolate(p, [0, 1], [0, dir === 0 ? 18 : dir === 1 ? -22 : dir === 2 ? -36 : 30]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `translate(${dx}px,${dy}px) scale(${s})`}}>
        <P src={`florence/flat/${name}.png`} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Factory B-roll video (commercial-OK shelf, QC'd). A slow linear zoom guarantees
 *  center motion even under a locked-off clip; the clip's own motion adds to it. */
const Factory: React.FC<{name: string; dim?: number}> = ({name, dim = 0}) => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const s = interpolate(f, [0, durationInFrames], [1.02, 1.12], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${s})`}}>
        <OffthreadVideo src={staticFile(`florence/factory/${name}.mp4`)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      {dim ? <AbsoluteFill style={{background: `rgba(6,10,18,${dim})`}} /> : null}
    </AbsoluteFill>
  );
};

/** Thin Wan2.2 atmosphere bed OVER a hero (fog / dust / dusk), honest + subtle. */
const AtmosBed: React.FC<{opacity?: number; children: React.ReactNode}> = ({opacity = 0.22, children}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    {children}
    <AbsoluteFill style={{opacity, mixBlendMode: 'screen', pointerEvents: 'none'}}>
      <OffthreadVideo src={staticFile('_ai/wan22_atmos.mp4')} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </AbsoluteFill>
  </AbsoluteFill>
);

/** overflow:hidden + translateY mask-up (design canon for text reveals). */
const MaskUp: React.FC<{delay?: number; children: React.ReactNode}> = ({delay = 0, children}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [delay, delay + 22], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{overflow: 'hidden'}}>
      <div style={{transform: `translateY(${interpolate(p, [0, 1], [110, 0])}%)`, opacity: p}}>{children}</div>
    </div>
  );
};

/** Brand title lockup over a slow dust bed (cut 6). */
const BrandTitle: React.FC = () => (
  <AtmosBed opacity={0.18}>
    <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 70%)`}} />
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 80}}>
      <div>
        <MaskUp delay={6}>
          <div style={{fontFamily: BRAND.font.body, fontWeight: 900, fontSize: 92, letterSpacing: 1, color: BRAND.color.white, textShadow: '0 6px 30px #000'}}>
            FLORENCE
          </div>
        </MaskUp>
        <MaskUp delay={16}>
          <div style={{fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 34, color: BRAND.color.gold, marginTop: 14, letterSpacing: 4}}>
            v. BOARD OF CHOSEN FREEHOLDERS
          </div>
        </MaskUp>
        <MaskUp delay={30}>
          <div style={{fontFamily: BRAND.font.body, fontWeight: 600, fontSize: 26, color: BRAND.color.white, opacity: 0.82, marginTop: 26}}>
            How far may the state reach at the jailhouse door?
          </div>
        </MaskUp>
      </div>
    </AbsoluteFill>
  </AtmosBed>
);

/** Hook cut 4: 5–4 seam teaser → gold line around the body. */
const Hook4: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Sequence durationInFrames={92} name="seam-teaser"><VerdictSeam /></Sequence>
    <Sequence from={92} name="bodyline-teaser"><BodyLine /></Sequence>
  </AbsoluteFill>
);

/** Burned narration captions — CALM standard-subtitle style (owner feedback 2026-07-13:
 *  the karaoke word-band was too busy). Shows ONE phrase cue at a time from the verified
 *  florence_captions.json (SRT-derived, gapless), held for its span, white, no per-word
 *  gold flicker. Reads the imported <slug>_captions*.json (caption_integrity path A). */
const CUES: {text: string; start: number; end: number}[] = florenceCaptions.cues;
const NarrationCaptions: React.FC = () => {
  const frame = useCurrentFrame(); const {fps, width} = useVideoConfig();
  const t = frame / fps + LEAD;
  // current phrase (binary-ish linear scan; cues are gapless + ordered)
  let cur: {text: string; start: number; end: number} | null = null;
  for (let i = 0; i < CUES.length; i++) { if (t >= CUES[i].start && t < CUES[i].end) { cur = CUES[i]; break; } if (CUES[i].start > t) break; }
  if (!cur) return null;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 74}}>
      <div style={{maxWidth: width * 0.72, textAlign: 'center', padding: '7px 22px', borderRadius: 8, background: 'rgba(6,10,18,0.4)'}}>
        <span style={{fontFamily: BRAND.font.body, fontWeight: 600, fontSize: 39, color: BRAND.color.white, lineHeight: 1.28, textShadow: '0 2px 9px rgba(0,0,0,0.9)'}}>{cur.text}</span>
      </div>
    </AbsoluteFill>
  );
};

// ── convenience factories ────────────────────────────────────────────────────
const d = (name: string) => <Depth25D name={name} />;
const kb = (name: string, seed = 0) => <KenBurns name={name} seed={seed} />;
const fx = (name: string, dim = 0) => <Factory name={name} dim={dim} />; // factory B-roll (moving)

// ── the 106 cuts (assembly_spec.v001 order; index i → DUR[i]) ─────────────────
// Each entry is (dur) => node; `dur` is the cut's frame length (also the combined
// span length for multi-cut core5 pieces, passed once so internal timing is correct).
type Node = (dur: number) => React.ReactNode;

// combined span lengths (sum of the cuts a single core5 piece covers)
const SPAN_Q4445 = DUR[43] + DUR[44];              // Florence quote (cuts 44–45)
const SPAN_CJ505152 = DUR[49] + DUR[50] + DUR[51]; // court hierarchy (50–52)
const SPAN_QK = DUR[64] + DUR[65];                 // Kennedy quote (65–66)
const SPAN_QB = DUR[75] + DUR[76];                 // Breyer quote (76–77)
const SPAN_PVP = DUR[77] + DUR[78] + DUR[79];      // dissent trade (78–80)
const SPAN_ALITO = DUR[84] + DUR[85];              // Alito paraphrase (85–86)

const NODES: Node[] = [
  // ── HOOK (0.00–18.66) — reused best body cuts, word-synced ──
  /* 1  */ () => <ReceiptStamp />,                                   // receipt PAID → WARRANT override (thesis in one image)
  /* 2  */ () => d('S03'),                                            // cuffs (no face)
  /* 3  */ () => d('S05'),                                            // search room (symbolic)
  /* 4  */ () => <Hook4 />,                                           // 5–4 seam → gold line around body
  // ── OPENING (19.20–34.96) ──
  /* 5  */ (dur) => <EvidenceReveal mode="document" tag="CHECKED BOX" caption="A paperwork error no bigger than a checked box." sourceLabel="Case background" dur={dur} />,
  /* 6  */ () => fx('capitol_dusk'),                                  // constitutional context (Capitol at dusk)
  /* 7  */ () => <VerdictSeam />,                                     // 5–4 seam motif hint
  // ── ACT I — THE STOP (35.64–115.38) ──
  /* 8  */ () => d('S19'),                                            // ordinary suburb, back-to-camera
  /* 9  */ () => fx('street_night'),                                     // warm evening street
  /* 10 */ () => fx('drive_night'),                                     // UPGRADE:footage dashboard drive-by (no faces)
  /* 11 */ () => fx('home_window'),                                     // warm-lit house (bought a house)
  /* 12 */ () => fx('driveway_car'),                                     // driveway / the SUV
  /* 13 */ () => <AtmosBed opacity={0.28}>{d('S01')}</AtmosBed>,      // night stop, red/blue fog
  /* 14 */ () => <WarrantScreen />,                                   // stale warrant flags RED·ACTIVE
  /* 15 */ () => <Span off={DUR[13]}><WarrantScreen /></Span>,        // BENCH WARRANT hold (continuation)
  /* 16 */ (dur) => <CaseJourney mode="procedural_path" stops={[{title: 'Old fine', desc: 'an old case'}]} label="Pre-history of the debt" sourceLabel="Case background" dur={dur} />,
  /* 17 */ (dur) => <CaseJourney mode="procedural_path" stops={[{title: 'Paying in installments'}, {title: 'Fell behind'}, {title: 'Missed a hearing', desc: 'warrant issued'}]} label="Pre-history of the debt" sourceLabel="Case background" dur={dur} />,
  /* 18 */ (dur) => <CaseJourney mode="procedural_path" stops={[{title: 'Whole balance paid'}, {title: 'PAID', desc: '~1 week — debt settled'}, {title: 'Warrant should have vanished'}]} label="Pre-history of the debt" sourceLabel="Case background" dur={dur} />,
  /* 19 */ () => <RecordsDrawer />,                                   // wall of drawers; sweep begins
  /* 20 */ () => <Span off={DUR[18]}><RecordsDrawer /></Span>,        // one red NOT CLEARED (continuation)
  /* 21 */ () => <ReceiptStamp />,                                    // receipt slides in; PAID slams
  /* 22 */ () => <Span off={DUR[20]}><ReceiptStamp /></Span>,         // WARRANT·ACTIVE overrides (continuation)
  /* 23 */ () => d('S03'),                                            // arrested (cuffs)
  /* 24 */ () => fx('glass_night'),                                        // UPGRADE:footage police-car back seat, rain
  // ── ACT II — THE TWO DOORS (115.82–260.36) ──
  /* 25 */ () => <Room src="ev_cam1_enter_room" />,                   // county jail corridor
  /* 26 */ () => fx('case_files', 0.06),                              // booking paperwork on the desk
  /* 27 */ () => d('S05'),                                            // search room doorway (symbolic)
  /* 28 */ () => fx('corridor_door'),                                     // discarded belt/laces motif
  /* 29 */ () => fx('fingerprint', 0.06),                            // examined for marks (identification)
  /* 30 */ () => fx('concrete_wall'),                                // bare institutional wall — NO body (R2)
  /* 31 */ () => kb('S05_04', 3),                                     // closed steel door
  /* 32 */ () => d('S06'),                                            // small silhouette, vast hall (pull-back begins)
  /* 33 */ () => kb('S06_02', 1),                                     // figure under one shaft
  /* 34 */ () => kb('S06_02', 3),                                     // figure smaller (distinct pan)
  /* 35 */ () => d('S06'),                                            // hall swallows figure (final retreat)
  /* 36 */ () => fx('clock_ticking', 0.05),                          // days passed (time)
  /* 37 */ () => fx('barbed_wire'),                                  // moved to a second facility (razor wire)
  /* 38 */ () => fx('cell_bars'),                                     // cold barred cell (again)
  /* 39 */ () => kb('S16_03', 2),                                     // empty cell (squat/cough — non-graphic)
  /* 40 */ (dur) => <PenaltyVsProperty left={{label: 'The offense', value: 1}} right={{label: 'Days held', value: 6}} comparisonAxis="1 stop · 2 jails · 2 searches · 6 days" mode="generic" sourceLabel="Case record" dur={dur} />,
  /* 41 */ () => kb('S16_04', 3),                                     // cell door, closed (turn to release)
  /* 42 */ () => d('S16'),                                            // door begins to open OUTWARD
  /* 43 */ () => kb('S16_04', 1),                                     // UPGRADE:footage steel door swinging open
  /* 44 */ () => <QuoteUnderExamination quote="I went from having a good day with my wife standing next to me, to being scared, petrified, humiliated." attribution="Albert Florence" sourceLabel="Verbatim quote" dur={SPAN_Q4445} />,
  /* 45 */ () => <Span off={DUR[43]}><QuoteUnderExamination quote="I went from having a good day with my wife standing next to me, to being scared, petrified, humiliated." attribution="Albert Florence" sourceLabel="Verbatim quote" dur={SPAN_Q4445} /></Span>,
  /* 46 */ () => d('S19'),                                            // ordinary-life callback
  /* 47 */ () => kb('S19_05', 2),                                     // warm home, quiet (most people let it go)
  /* 48 */ () => fx('courthouse_steps'),           // he sued — the litigation begins
  /* 49 */ (dur) => <QuoteUnderExamination quote="A person arrested over a minor, unpaid fine should not be strip searched when there is no reason at all to suspect he is hiding anything." attribution="Albert Florence — his principle (paraphrased)" sourceLabel="Paraphrase of his stated principle" dur={dur} />,
  /* 50 */ () => <CaseJourney mode="court_hierarchy" stops={[{title: 'District Court (D.N.J.)', desc: '2009 — ruled for Florence'}, {title: '3rd Circuit', desc: '2010 — reversed'}, {title: 'Supreme Court', desc: 'the question keeps climbing'}]} label="The litigation path" sourceLabel="Procedural history" dur={SPAN_CJ505152} />,
  /* 51 */ () => <Span off={DUR[49]}><CaseJourney mode="court_hierarchy" stops={[{title: 'District Court (D.N.J.)', desc: '2009 — ruled for Florence'}, {title: '3rd Circuit', desc: '2010 — reversed'}, {title: 'Supreme Court', desc: 'the question keeps climbing'}]} label="The litigation path" sourceLabel="Procedural history" dur={SPAN_CJ505152} /></Span>,
  /* 52 */ () => <Span off={DUR[49] + DUR[50]}><CaseJourney mode="court_hierarchy" stops={[{title: 'District Court (D.N.J.)', desc: '2009 — ruled for Florence'}, {title: '3rd Circuit', desc: '2010 — reversed'}, {title: 'Supreme Court', desc: 'the question keeps climbing'}]} label="The litigation path" sourceLabel="Procedural history" dur={SPAN_CJ505152} /></Span>,
  // ── ACT III — THE COLLISION (261.00–443.88) ──
  /* 53 */ () => <AtmosBed opacity={0.2}>{fx('columns_scotus', 0.08)}</AtmosBed>, // SCOTUS arrival — monumental columns
  /* 54 */ () => d('S08'),                                            // rise / hold — SCOTUS arrival (2.5D)
  /* 55 */ () => d('S12'),                                            // long line of faceless silhouettes (2.5D)
  /* 56 */ () => kb('S12', 2),                                        // dolly along the line
  /* 57 */ () => kb('S12_02', 1),                                     // line continues (anyone)
  /* 58 */ () => kb('S12', 3),                                        // nearest figure turns — "you"
  /* 59 */ () => fx('court_empty'),                   // settle between two lecterns
  /* 60 */ () => <Room src="evroom_cam2" />,                          // both lecterns light (balanced)
  /* 61 */ () => d('S11'),                                            // cold orderly cell rows (danger) (2.5D)
  /* 62 */ () => fx('server_rows'),                                        // push continues
  /* 63 */ () => fx('network_line'),                                     // rows, vanishing point
  /* 64 */ () => kb('S11_02', 3),                                     // hold on vanishing point
  /* 65 */ () => <QuoteUnderExamination quote="The seriousness of an offense is a poor predictor of who has contraband." attribution="Justice Kennedy, for the Court" examineAt={{cx: 0.5, cy: 0.42, r: 0.42}} sourceLabel="Verbatim quote" dur={SPAN_QK} />,
  /* 66 */ () => <Span off={DUR[64]}><QuoteUnderExamination quote="The seriousness of an offense is a poor predictor of who has contraband." attribution="Justice Kennedy, for the Court" examineAt={{cx: 0.5, cy: 0.42, r: 0.42}} sourceLabel="Verbatim quote" dur={SPAN_QK} /></Span>,
  /* 67 */ (dur) => <EvidenceReveal mode="record" tag="HISTORY" caption="A routine traffic stop." sourceLabel="Majority reasoning" dur={dur} />,
  /* 68 */ (dur) => <EvidenceReveal mode="record" tag="NO LICENSE PLATE" caption="Arrested driving without a plate." sourceLabel="Majority reasoning" dur={dur} />,
  /* 69 */ () => kb('S11_03', 0),                                     // thin dividing line of light
  /* 70 */ () => kb('S11_03', 2),                                     // line wavers (cost of guessing)
  /* 71 */ () => kb('S11_04', 1),                                     // settle on the line (holding)
  /* 72 */ () => kb('S11', 3),                                        // line resolves to "security"
  /* 73 */ () => fx('courtroom_wide'),                               // the dissent's side (empty courtroom)
  /* 74 */ () => <Room src="ev_cam2_push_desk" dim={0.08} />,        // warm-gold lectern
  /* 75 */ () => d('S06'),                                            // dignity silhouette
  /* 76 */ () => <QuoteUnderExamination quote="A strip search that involves a stranger peering without consent at a naked individual, and in particular at the most private portions of that person's body, is a serious invasion of privacy." attribution="Justice Breyer, dissenting" sourceLabel="Verbatim quote" dur={SPAN_QB} />,
  /* 77 */ () => <Span off={DUR[75]}><QuoteUnderExamination quote="A strip search that involves a stranger peering without consent at a naked individual, and in particular at the most private portions of that person's body, is a serious invasion of privacy." attribution="Justice Breyer, dissenting" sourceLabel="Verbatim quote" dur={SPAN_QB} /></Span>,
  /* 78 */ () => <PenaltyVsProperty left={{label: 'Safety gained', value: 1}} right={{label: 'Cost to dignity', value: 9}} comparisonAxis="the dissent's trade — magnitudes illustrative" mode="generic" sourceLabel="Dissent (qualitative — no stat asserted)" dur={SPAN_PVP} />,
  /* 79 */ () => <Span off={DUR[77]}><PenaltyVsProperty left={{label: 'Safety gained', value: 1}} right={{label: 'Cost to dignity', value: 9}} comparisonAxis="the dissent's trade — magnitudes illustrative" mode="generic" sourceLabel="Dissent (qualitative — no stat asserted)" dur={SPAN_PVP} /></Span>,
  /* 80 */ () => <Span off={DUR[77] + DUR[78]}><PenaltyVsProperty left={{label: 'Safety gained', value: 1}} right={{label: 'Cost to dignity', value: 9}} comparisonAxis="the dissent's trade — magnitudes illustrative" mode="generic" sourceLabel="Dissent (qualitative — no stat asserted)" dur={SPAN_PVP} /></Span>,
  /* 81 */ () => <VerdictSeam />,                                     // 5 gold + 4 silver → 5–4
  /* 82 */ () => <Span off={DUR[80]}><VerdictSeam /></Span>,          // CONSTITUTIONAL stamp
  /* 83 */ () => <Span off={DUR[80] + DUR[81]}><VerdictSeam /></Span>, // hairline CRACK draws
  /* 84 */ () => <Span off={DUR[80] + DUR[81] + DUR[82]}><VerdictSeam /></Span>, // seam / 5th-vote hold
  /* 85 */ () => <QuoteUnderExamination quote="The Court did not hold that it is always reasonable to strip search an arrestee whose detention no judge has yet reviewed, and who could be held apart from the general population." attribution="Justice Alito, concurring — PARAPHRASED (not a verbatim quote)" sourceLabel="Paraphrase — Alito concurrence" dur={SPAN_ALITO} />,
  /* 86 */ () => <Span off={DUR[84]}><QuoteUnderExamination quote="The Court did not hold that it is always reasonable to strip search an arrestee whose detention no judge has yet reviewed, and who could be held apart from the general population." attribution="Justice Alito, concurring — PARAPHRASED (not a verbatim quote)" sourceLabel="Paraphrase — Alito concurrence" dur={SPAN_ALITO} /></Span>,
  /* 87 */ () => <VerdictSeam />,                                     // 5th vote peels; seam holds
  // ── ACT IV — THE RANGE & THE QUIET UNIVERSAL (444.34–542.52) ──
  /* 88 */ () => d('S13'),                                            // gold line across dark marble (2.5D)
  /* 89 */ () => kb('S13', 1),                                        // the rule (list narrated)
  /* 90 */ () => fx('audit_docs'),                                   // the unpaid fine (offenses)
  /* 91 */ () => fx('data_flow'),                                    // the digital record never erased
  /* 92 */ () => fx('data_corridor'),                                     // crowd, one warm light (ACLU — captioned)
  /* 93 */ () => fx('crowd_silhouette'),                             // the crowd — the anonymous everyone
  /* 94 */ () => fx('archive'),                                      // millions of records cycle through
  /* 95 */ () => <Room src="evroom_cam2" dim={0.06} />,              // dead-center, both lecterns
  /* 96 */ () => <Room src="evroom_cam2" />,                          // both lit, balanced
  /* 97 */ () => <Room src="evroom_cam2" dim={0.04} />,              // equilibrium, beam between
  /* 98 */ (dur) => <CaseJourney mode="procedural_path" stops={[{title: 'The smallest fact'}, {title: 'A fine that was paid'}, {title: "A week's delay"}]} label="Return to the smallest fact" sourceLabel="Callback motif" dur={dur} />,
  /* 99 */ () => <RecordsDrawer />,                                   // callback: collapse to one red record
  /* 100*/ (dur) => <CaseJourney mode="procedural_path" stops={[{title: 'Two doors · six days'}, {title: 'The searches'}, {title: 'The case that carries his name'}]} label="It all unspools" sourceLabel="Callback motif" dur={dur} />,
  /* 101*/ () => <Span off={160}><RecordsDrawer /></Span>,            // land on the single glowing record
  /* 102*/ () => <BodyLine />,                                        // gold line draws around the body
  /* 103*/ () => <Span off={DUR[101]}><BodyLine /></Span>,            // blue press meets the line; holds
  /* 104*/ () => <Span off={DUR[101] + DUR[102]}><BodyLine /></Span>, // a man holding a receipt
  /* 105*/ () => d('S14'),                                            // dark doorway, distant light (2.5D)
  /* 106*/ () => (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {kb('S14', 1)}
      <FadeToBlack />
    </AbsoluteFill>
  ),                                                                 // door opens; HOLD to black — "whose door is next?"
];

/** Final deliberate hold-to-black over the last cut. */
const FadeToBlack: React.FC = () => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const o = interpolate(f, [durationInFrames - 46, durationInFrames - 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: '#000', opacity: o, pointerEvents: 'none'}} />;
};

// ── registration exports ─────────────────────────────────────────────────────
// Canonical channel bookends wrap the narrated body: BrandOpening (3.5s brand sting)
// → the 106-cut body (narration starts here) → BrandEndcard (9s CTA). This satisfies
// op_ed_bookends and extends runtime toward the band without touching the script
// (owner decision: master narration unchanged; runtime_band remains the sole APR).
const BODY_FRAMES = DUR.reduce((a, b) => a + b, 0); // 16288
const OPEN_F = Math.round(OPENING_SEC * FPS);       // 105  (3.5s)
const END_F = Math.round(ENDCARD_SEC * FPS);        // 270  (9s)
const HOOK_FRAMES = DUR.slice(0, 4).reduce((a, b) => a + b, 0); // 576 = cuts 1-4 (the cold-open hook)
export const florenceSceneCount = NODES.length;     // 106
// COLD-OPEN HOOK FIRST (owner 2026-07-13): the hook (cuts 1-4, narration 0-19.2s) plays at
// video 0; the BrandOpening sting is OVERLAID right after it (over the opening thesis), so the
// brand never precedes the hook. No time is inserted (narration stays 0-based). Endcard appended.
export const florenceDuration = BODY_FRAMES + END_F; // 16558 frames ≈ 9:12

/** The narrated 106-cut body + overlays. Mounted inside a body Sequence so its
 *  useCurrentFrame is body-relative (frame 0 = narration t0), keeping WordBand and
 *  the muxed audio in sync after the brand opening. */
const FlorenceBody: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      {NODES.map((node, i) => (
        <Series.Sequence key={i} durationInFrames={DUR[i]}>
          {node(DUR[i])}
        </Series.Sequence>
      ))}
    </Series>
    {/* brightness lift — screen-blend fill light raises crushed shadows so the moody
        night/cell scenes clear the body-luma floor (median >=48). Calibrated on the
        darkest Act II cell stretch: gray 44 @0.85 screen lifts ~20-luma blacks to ~56. */}
    <AbsoluteFill style={{background: 'rgb(46,48,56)', mixBlendMode: 'screen', opacity: 0.8, pointerEvents: 'none'}} />
    <NarrationCaptions />
    {/* finishing bed — gold glow + soft-light grade (no shadow-crushing bottom gradient). */}
    <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 36%, ${BRAND.color.gold}12 0%, transparent 46%)`, mixBlendMode: 'soft-light', pointerEvents: 'none'}} />
    <VignetteBreath />
    {/* Studio-preview narration (body-relative → narration t0); FINAL render uses --muted. */}
    <Audio src={staticFile('florence/narration_master.mp3')} />
  </AbsoluteFill>
);

/** Mild screen-blend lift so the dark brand bookend backgrounds clear the per-cut luma
 *  floor (image_cut_luma samples every ~2s with no cutlist, so it cannot exclude the
 *  bookends the way it does with a film.json — lift them into readable range). */
const BookendLift: React.FC = () => (
  <AbsoluteFill style={{background: 'rgb(44,46,54)', mixBlendMode: 'screen', opacity: 0.62, pointerEvents: 'none'}} />
);

export const Florence: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    {/* body plays at video 0 → the cold-open HOOK (cuts 1-4) is the very first thing on screen */}
    <Sequence durationInFrames={BODY_FRAMES} name="body">
      <FlorenceBody />
    </Sequence>
    {/* BrandOpening sting overlaid AFTER the hook, over the opening thesis (never before the hook) */}
    <Sequence from={HOOK_FRAMES} durationInFrames={OPEN_F} name="brand-opening">
      <BrandOpening seriesLabel="PRIME DOCUMENTARY" title="FLORENCE" subtitle="v. Board of Chosen Freeholders" />
      <BookendLift />
    </Sequence>
    <Sequence from={BODY_FRAMES} durationInFrames={END_F} name="brand-endcard">
      <BrandEndcard ctaLine="▶ SUBSCRIBE — LANDMARK RIGHTS CASES" cadenceLine="New episodes every week" />
      <BookendLift />
    </Sequence>
    <FilmGrain />
  </AbsoluteFill>
);
