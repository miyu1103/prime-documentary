import React from 'react';
import {Composition, Still} from 'remotion';
import './load-fonts'; // register brand premium fonts (Oswald/Anton/Archivo) for the render
import {BRAND} from './brand';
import {PDCore5Preview, core5PreviewDuration} from './components/core5/preview';
import {TimbsB1, timbsB1DurationInFrames} from './compositions/TimbsB1';
import {TimbsB2, timbsB2DurationInFrames} from './compositions/TimbsB2';
import {TimbsDepthTest, timbsDepthTestDuration} from './compositions/TimbsDepthTest';
import {TimbsParallax, timbsParallaxDuration} from './compositions/TimbsParallax';
import {TimbsC3, timbsC3DurationInFrames} from './compositions/TimbsC3';
import {PDTest60, pdTest60Duration} from './compositions/PDTest60';
import {PDNewLook, pdNewLookDuration} from './compositions/PDNewLook';
import {PD3DShowcase, pd3DShowcaseDuration} from './compositions/PD3DShowcase';
import {PDAllTools, pdAllToolsDuration} from './compositions/PDAllTools';
import {PDForfeiture60, pdForfeiture60Duration} from './compositions/PDForfeiture60';
import {PDDepthFixed, pdDepthFixedDuration} from './compositions/PDDepthFixed';
import {PDReel, pdReelDuration} from './compositions/PDReel';
import {PDOriginal, pdOriginalDuration} from './compositions/PDOriginal';
import {WarrantScreen, warrantScreenDuration} from './compositions/florence/WarrantScreen';
import {RecordsDrawer, recordsDrawerDuration} from './compositions/florence/RecordsDrawer';
import {ReceiptStamp, receiptStampDuration} from './compositions/florence/ReceiptStamp';
import {VerdictSeam, verdictSeamDuration} from './compositions/florence/VerdictSeam';
import {BodyLine, bodyLineDuration} from './compositions/florence/BodyLine';
import {Florence, florenceDuration} from './compositions/Florence';
import {PDAIHero, pdAIHeroDuration} from './compositions/PDAIHero';
import {Opening} from './compositions/Opening';
import {Episode, TEMPLATE_12MIN} from './compositions/Episode';
import {StyleTest} from './compositions/StyleTest';
import {Animatic, animaticDurationInFrames, durationInFramesFor} from './compositions/Animatic';
import {GIDEON_ANIMATIC, GIDEON_SCENE_IMG} from './data/gideon_animatic';
import {GideonPremium, gideonPremiumDurationInFrames} from './compositions/GideonPremium';
import {MirandaPremium, mirandaPremiumDurationInFrames} from './compositions/MirandaPremium';
import {MappPremium, mappPremiumDurationInFrames} from './compositions/MappPremium';
import {MadoffPremium, madoffPremiumDurationInFrames} from './compositions/MadoffPremium';
import {TimbsPremium, timbsPremiumDurationInFrames} from './compositions/TimbsPremium';
import {KeloPremium, keloPremiumDurationInFrames} from './compositions/KeloPremium';
import {KeloThumbnailFrame} from './compositions/KeloThumbnailFrame';
import {TylerThumbnailFrame} from './compositions/TylerThumbnailFrame';
import {MahanoyPremium, mahanoyPremiumDurationInFrames} from './compositions/MahanoyPremium';
import {ArbitrationPremium, arbitrationPremiumDurationInFrames} from './compositions/ArbitrationPremium';
import {KingPremium, kingPremiumDurationInFrames} from './compositions/KingPremium';
import {LangePremium, langePremiumDurationInFrames} from './compositions/LangePremium';
import {TheranosPremium, theranosPremiumDurationInFrames} from './compositions/TheranosPremium';
import {TitanPremium, titanPremiumDurationInFrames} from './compositions/TitanPremium';
import {OneCoinPremium, oneCoinPremiumDurationInFrames} from './compositions/OneCoinPremium';
import {FlashCrashPremium, flashCrashPremiumDurationInFrames} from './compositions/FlashCrashPremium';
import {VarsityBluesPremium, varsityBluesPremiumDurationInFrames} from './compositions/VarsityBluesPremium';
import {GardnerPremium, gardnerPremiumDurationInFrames} from './compositions/GardnerPremium';
import {SwartzPremium, swartzPremiumDurationInFrames} from './compositions/SwartzPremium';
import {RajaratnamPremium, rajaratnamPremiumDurationInFrames} from './compositions/RajaratnamPremium';
import {OneCoinThumbnailFrame} from './compositions/OneCoinThumbnailFrame';
import {KingThumbnailFrame} from './compositions/KingThumbnailFrame';
import {MirandaThumbnailFrame} from './compositions/MirandaThumbnailFrame';
import {ClipProof} from './compositions/ClipProof';
import {DepthTest} from './compositions/DepthTest';
import {MotionSample, motionSampleDurationInFrames} from './compositions/MotionSample';
import {TylerFigures, tylerFiguresDurationInFrames} from './compositions/TylerFigures';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './compositions/CaseFilm';
import {OpeningLech, openingLechDurationInFrames} from './compositions/OpeningLech';
import {LechThumbnail, LECH_THUMBS} from './compositions/LechThumbnails';
import {OpeningYoung, openingYoungDurationInFrames} from './compositions/OpeningYoung';
import {YoungFilm, youngFilmDurationInFrames} from './compositions/YoungFilm';
import {YoungThumbnail, YOUNG_THUMBS} from './compositions/YoungThumbnails';
import {OpeningCaniglia, openingCanigliaDurationInFrames} from './compositions/OpeningCaniglia';
import {CanigliaThumbnail, CANIGLIA_THUMBS} from './compositions/CanigliaThumbnails';
import {OpeningTekoh, openingTekohDurationInFrames} from './compositions/OpeningTekoh';
import {TekohThumbnail, TEKOH_THUMBS} from './compositions/TekohThumbnails';
import {OpeningCleveland, openingClevelandDurationInFrames} from './compositions/OpeningCleveland';
import {ClevelandThumbnail, CLEV_THUMBS} from './compositions/ClevelandThumbnails';
import {TloThumbnail, TLO_THUMBS} from './compositions/TloThumbnails';
import {AtwaterThumbnail, ATWATER_THUMBS} from './compositions/AtwaterThumbnails';
import {OpeningGlover, openingGloverDurationInFrames} from './compositions/OpeningGlover';
import {GloverThumbnail, GLOVER_THUMBS} from './compositions/GloverThumbnails';
import {OpeningStrieff, openingStrieffDurationInFrames} from './compositions/OpeningStrieff';
import {StrieffThumbnail, STRIEFF_THUMBS} from './compositions/StrieffThumbnails';
import {OpeningCentralpark, openingCentralparkDurationInFrames} from './compositions/OpeningCentralpark';
import {CentralparkFilm, centralparkFilmDurationInFrames} from './compositions/CentralparkFilm';
import {FlowersFilm, flowersFilmDurationInFrames} from './compositions/FlowersFilm';
import {WillinghamFilm, willinghamFilmDurationInFrames} from './compositions/WillinghamFilm';
import {MortonFilm, mortonFilmDurationInFrames} from './compositions/MortonFilm';
import {NorfolkFilm, norfolkFilmDurationInFrames} from './compositions/NorfolkFilm';
import {BurgeFilm, burgeFilmDurationInFrames} from './compositions/BurgeFilm';
import {PostofficeFilm, postofficeFilmDurationInFrames} from './compositions/PostofficeFilm';
import {CentralparkThumbnail, CENTRALPARK_THUMBS} from './compositions/CentralparkThumbnails';
import {Frazier39Opening, frazier39OpeningDurationInFrames} from './compositions/Frazier39Opening';
import {FrazierThumbnail, FRAZIER_THUMBS} from './compositions/FrazierThumbnails';
import {WilliamsFilm, williamsFilmDurationInFrames} from './compositions/WilliamsFilm';
import {AircashFigTest, AIRCASH_FIG_TEST_FRAMES} from './compositions/AircashFigTest';
import {HindersFigTest, HINDERS_FIG_TEST_FRAMES} from './compositions/HindersFigTest';
import kylloFilm from './data/kyllo_film.json';
import tylerFilm from './data/tyler_film.json';
import katzFilm from './data/katz_film.json';
import rodriguezFilm from './data/rodriguez_film.json';
import cottonFilm from './data/cotton_film.json';
import unlockFilm from './data/unlock_film.json';
import forfeitureFilm from './data/forfeiture_film.json';
import hindersFilm from './data/hinders_film.json';
import kidsforcashFilm from './data/kidsforcash_film.json';
import lechFilm from './data/lech_film.json';
import thompsonFilm from './data/thompson_film.json';
import canigliaFilm from './data/caniglia_film.json';
import tekohFilm from './data/tekoh_film.json';
import clevelandFilm from './data/cleveland_film.json';
import tloFilm from './data/tlo_film.json';
import atwaterFilm from './data/atwater_film.json';
import gloverFilm from './data/glover_film.json';
import strieffFilm from './data/strieff_film.json';
import frazierFilm from './data/frazier_film.json';
import hintonFilm from './data/hinton_film.json';
import carsearchFilm from './data/carsearch_film.json';
import rolinFilm from './data/rolin_film.json';
import williamsFilm from './data/williams_film.json';
import {CarsearchThumbnail, CARSEARCH_THUMBS} from './compositions/CarsearchThumbnails';
import {RolinThumbnail, ROLIN_THUMBS} from './compositions/RolinThumbnails';
import {KidsForCashThumbnail, KIDSFORCASH_THUMBS} from './compositions/KidsForCashThumbnails';
import {ColdOpen, MIRANDA_HOOK, hookDurationInFrames} from './compositions/ColdOpen';
import {ThumbConcept} from './compositions/ThumbConcept';
import {ThumbnailFrame} from './components/ThumbnailFrame';
import {NumberTicker} from './components/motionkit/NumberTicker';
import {RoughCut, roughCutDurationInFrames} from './compositions/RoughCut';
import {BumperBrushupPreview, BrandOpeningOriginalPreview, OneCoinBrandOpeningPreview, bumperBrushupDurationInFrames} from './compositions/OpeningBumperBrushup';
import {EndingBrushupPreview, endingBrushupDurationInFrames} from './compositions/EndingBrushup';
import {Short, ShortThumb, shortDurationInFrames} from './compositions/Short';
import {ShortThumbYT} from './compositions/ShortThumbYT';
import {SHORT06} from './data/short06';
import {SHORT07} from './data/short07';
import {SHORT08} from './data/short08';
import {SHORT09} from './data/short09';
import {SHORT10} from './data/short10';
import {SHORT11} from './data/short11';
import {SHORT12} from './data/short12';
import {SHORT13} from './data/short13';
import {SHORT14} from './data/short14';
import {SHORT15} from './data/short15';
import {SHORT16} from './data/short16';
import {SHORT17} from './data/short17';
import {SHORT18} from './data/short18';
import {SHORT19} from './data/short19';
import {SHORT20} from './data/short20';
import {SHORT21} from './data/short21';
import {SHORT22} from './data/short22';
import {SHORT24} from './data/short24';
import {SHORT25} from './data/short25';
import {SHORT26} from './data/short26';
import {SHORT27} from './data/short27';
import {SHORT23} from './data/short23';
import {SHORT28} from './data/short28';
import {SHORT29} from './data/short29';
import {SHORT30} from './data/short30';
import {SHORT31} from './data/short31';
import {SHORT32} from './data/short32';
import {SHORT33} from './data/short33';
import {SHORT34} from './data/short34';
import {SHORT35} from './data/short35';
import {SHORT36} from './data/short36';
import {SHORT37} from './data/short37';
import {SHORT38} from './data/short38';
import {SHORT39} from './data/short39';
import {SHORT40} from './data/short40';
import {SHORT40M} from './data/short40m';
import {SHORT41} from './data/short41';
import {SHORT42} from './data/short42';
import {SHORT43} from './data/short43';
import {SHORT46} from './data/short46';
import {SHORT47} from './data/short47';
import {SHORT48} from './data/short48';
import {SHORT49} from './data/short49';
import {SHORT50} from './data/short50';
import {SHORT51} from './data/short51';
import {SHORT52} from './data/short52';
import {SHORT53} from './data/short53';
import {SHORT54} from './data/short54';
import {SHORT55} from './data/short55';
import {SHORT56} from './data/short56';
import {SHORT57} from './data/short57';
import {SHORT58} from './data/short58';
import {SHORT59} from './data/short59';
import {SHORT60} from './data/short60';
import {SHORT63} from './data/short63';
import {SHORT66} from './data/short66';
import {SHORT01} from './data/short01';
import {SHORT02} from './data/short02';
import {SHORT03} from './data/short03';
import {SHORT04} from './data/short04';
import {SHORT05} from './data/short05';
import {MAHANOY_ROUGHCUT} from './data/mahanoy_roughcut';
import {TIMBS_ROUGHCUT} from './data/timbs_roughcut';
import {KELO_ROUGHCUT} from './data/kelo_roughcut';
import {ARBITRATION_ROUGHCUT} from './data/arbitration_roughcut';
import {KING_ROUGHCUT} from './data/king_roughcut';
import {LANGE_ROUGHCUT} from './data/lange_roughcut';
import {THERANOS_ROUGHCUT} from './data/theranos_roughcut';
import {TITAN_ROUGHCUT} from './data/titan_roughcut';
import {ONECOIN_ROUGHCUT} from './data/onecoin_roughcut';
import lechOpeningProps from '../props/lech.json';
import youngOpeningProps from '../props/young.json';
import canigliaOpeningProps from '../props/caniglia.json';
import tekohOpeningProps from '../props/tekoh.json';

const ROUGHCUTS = [
  ['RoughCut-timbs', TIMBS_ROUGHCUT],
  ['RoughCut-kelo', KELO_ROUGHCUT],
  ['RoughCut-arbitration', ARBITRATION_ROUGHCUT],
  ['RoughCut-king', KING_ROUGHCUT],
  ['RoughCut-lange', LANGE_ROUGHCUT],
  ['RoughCut-theranos', THERANOS_ROUGHCUT],
  ['RoughCut-titan', TITAN_ROUGHCUT],
  ['RoughCut-onecoin', ONECOIN_ROUGHCUT],
] as const;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* dev harness: CaseFilm `depth` treatment（実DPT深度パララックス）の目視確認 */}
      <Composition
        id="DepthTest"
        component={DepthTest}
        durationInFrames={90}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {/* dev harness: EP34 rolin aircash 7図の smoke 検証（各6s・全図フルフレーム） */}
      <Composition
        id="AircashFigTest"
        component={AircashFigTest}
        durationInFrames={AIRCASH_FIG_TEST_FRAMES}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {/* dev harness: EP35 hinders 27図の smoke 検証（各4s・全図フルフレーム） */}
      <Composition
        id="HindersFigTest"
        component={HindersFigTest}
        durationInFrames={HINDERS_FIG_TEST_FRAMES}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {/* プレビュー専用: ブランドオープニング磨き上げ版(アフター・未採用) */}
      <Composition
        id="BumperBrushupPreview"
        component={BumperBrushupPreview}
        durationInFrames={bumperBrushupDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {/* プレビュー専用: 既存BrandOpening(ビフォー・比較用) */}
      <Composition
        id="BrandOpeningOriginalPreview"
        component={BrandOpeningOriginalPreview}
        durationInFrames={bumperBrushupDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="OneCoinBrandOpeningPreview"
        component={OneCoinBrandOpeningPreview}
        durationInFrames={bumperBrushupDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {/* プレビュー専用: 派手版エンディング(アフター・未採用) */}
      <Composition
        id="EndingBrushupPreview"
        component={EndingBrushupPreview}
        durationInFrames={endingBrushupDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="RoughCut-mahanoy"
        component={RoughCut}
        durationInFrames={roughCutDurationInFrames(MAHANOY_ROUGHCUT)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{data: MAHANOY_ROUGHCUT}}
      />
      {ROUGHCUTS.map(([id, data]) => (
        <Composition
          key={id}
          id={id}
          component={RoughCut}
          durationInFrames={roughCutDurationInFrames(data)}
          fps={BRAND.video.fps}
          width={BRAND.video.width}
          height={BRAND.video.height}
          defaultProps={{data}}
        />
      ))}
      {/* Vertical 9:16 Shorts — same footage exported for YouTube (yt) and TikTok (tt); only the CTA differs. */}
      <Composition
        id="Short-short06-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT06, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT06, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short06-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT06, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT06, platform: 'tiktok' as const}}
      />
      <Composition
        id="Ep39Frazier"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(frazierFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: frazierFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'They Can Lie',
          subtitle: 'Frazier v. Cupp and police deception',
        }}
      />
      <Composition
        id="Frazier39Opening"
        component={Frazier39Opening}
        durationInFrames={frazier39OpeningDurationInFrames(60)}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'THEY CAN LIE',
          subtitle: 'FRAZIER V. CUPP - 1969',
          accent: '#E5B53A',
          hasLogo: true,
        }}
      />
      {FRAZIER_THUMBS.map((concept) => (
        <Still
          key={concept.id}
          id={`Thumb-frazier-${concept.id}`}
          component={FrazierThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      <Still
        id="Thumb-frazier-selected"
        component={FrazierThumbnail}
        width={1280}
        height={720}
        defaultProps={{concept: FRAZIER_THUMBS[0]}}
      />
      <Composition
        id="Ep40Lech"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(lechFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: lechFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'They Destroyed Their House',
          subtitle: 'A stranger ran inside. The family paid for it.',
        }}
      />
      <Composition
        id="Ep41Thompson"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(thompsonFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: thompsonFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'The Paper That Could Not Save Him',
          subtitle: 'Connick v. Thompson and the price of a buried page',
        }}
      />
      <Composition
        id="Ep42Young"
        component={YoungFilm}
        durationInFrames={youngFilmDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep43Caniglia"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(canigliaFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: canigliaFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'Police Came for a Welfare Check. They Left With His Guns.',
          subtitle: 'Caniglia v. Strom and the line at the door.',
        }}
      />
      <Composition
        id="Ep44Tekoh"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(tekohFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: tekohFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'They Never Read Him His Rights. Then the Court Closed One Door.',
          subtitle: 'Vega v. Tekoh and the difference between a right and a remedy.',
        }}
      />
      <Composition
        id="Ep45Cleveland"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(clevelandFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: clevelandFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: "Jailed for Being Too Poor to Pay a Fine. It's Unconstitutional.",
          subtitle: "Bearden v. Georgia and the debtors' prison that never ended.",
        }}
      />
      <Composition
        id="Ep46Tlo"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(tloFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: tloFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'A Teacher Searched Her Purse. The Supreme Court Said It Was Fine.',
          subtitle: 'The Fourth Amendment applies at school - but the bar is reasonable suspicion, not probable cause. 6-3, 1985.',
        }}
      />

      {/* EP46 fix: corrected numberticker for the decision-year figure. The baked base
          render shows the YEAR as "1,985" (NumberTicker always comma-grouped). This standalone
          composition re-renders the SAME figure with group disabled -> "1985", to be overlaid on
          just that figure's window on the final (identical component/props/dur/fps -> seamless).
          174 frames = 5.8s * 30fps, matching FigureBeats dur for the tlo numberticker (497.11-502.91). */}
      <Composition
        id="TloTickerFix"
        component={NumberTicker}
        durationInFrames={174}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          value: 1985,
          topLabel: 'BY THE NUMBERS',
          label: 'decided January 15, 1985',
          decimals: 0,
          group: false,
          dur: 174,
        }}
      />
      <Composition
        id="Ep47Atwater"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(atwaterFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: atwaterFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'A Teacher Searched Her Purse. The Supreme Court Said It Was Fine.',
          subtitle: 'The Fourth Amendment applies at school - but the bar is reasonable suspicion, not probable cause. 6-3, 1985.',
        }}
      />
      <Composition
        id="Ep48Glover"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(gloverFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: gloverFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'A Cop Ran Your Plate and Pulled You Over. He Never Saw You Break a Law.',
          subtitle: 'Kansas v. Glover: the stop stood, but the rule stayed narrow.',
        }}
      />
      <Composition
        id="Ep49Strieff"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(strieffFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: strieffFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'The Stop Was Illegal. The Evidence Still Stayed.',
          subtitle: 'Utah v. Strieff: attenuation, warrants, and the narrowed exclusionary rule.',
        }}
      />
      <Composition
        id="OpeningStrieff"
        component={OpeningStrieff}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingStrieffDurationInFrames(60)}
        defaultProps={{
          title: 'THE WARRANT',
          subtitle: 'UTAH v. STRIEFF - 2016',
          accent: '#9C6BAA',
          hasLogo: true,
        }}
      />
      <Composition
        id="Ep50Centralpark"
        component={CentralparkFilm}
        durationInFrames={centralparkFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep54Flowers"
        component={FlowersFilm}
        durationInFrames={flowersFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep51Willingham"
        component={WillinghamFilm}
        durationInFrames={willinghamFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep52Morton"
        component={MortonFilm}
        durationInFrames={mortonFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep53Norfolk"
        component={NorfolkFilm}
        durationInFrames={norfolkFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep55Burge"
        component={BurgeFilm}
        durationInFrames={burgeFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep56Postoffice"
        component={PostofficeFilm}
        durationInFrames={postofficeFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />

      {/* EP47 fix: corrected numberticker for the decision-year figure. The baked base render
          shows the YEAR as "2,001" (NumberTicker comma-grouped). This standalone composition
          re-renders the SAME figure with group disabled -> "2001", region-overlaid on just that
          figure's window on the final (identical component/props/dur/fps -> seamless). 174 frames
          = 5.8s * 30fps, matching FigureBeats dur for the atwater numberticker (524.326-530.126).
          topLabel/label/decimals match the atwater_film.json figure exactly. */}
      <Composition
        id="AtwaterTickerFix"
        component={NumberTicker}
        durationInFrames={174}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          value: 2001,
          topLabel: 'BY THE NUMBERS',
          label: 'decided - the Supreme Court',
          decimals: 0,
          group: false,
          dur: 174,
        }}
      />
      <Composition
        id="OpeningLech"
        component={OpeningLech}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingLechDurationInFrames(60)}
        defaultProps={lechOpeningProps}
      />
      <Composition
        id="OpeningYoung"
        component={OpeningYoung}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingYoungDurationInFrames(60)}
        defaultProps={youngOpeningProps}
      />
      <Composition
        id="OpeningCaniglia"
        component={OpeningCaniglia}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingCanigliaDurationInFrames(60)}
        defaultProps={canigliaOpeningProps}
      />
      <Composition
        id="OpeningTekoh"
        component={OpeningTekoh}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingTekohDurationInFrames(60)}
        defaultProps={tekohOpeningProps}
      />
      <Composition
        id="OpeningCleveland"
        component={OpeningCleveland}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingClevelandDurationInFrames(60)}
        defaultProps={{
          title: 'POVERTY TO PRISON',
          subtitle: 'BEARDEN V. GEORGIA - 1983',
          accent: '#B43A3A',
          hasLogo: true,
        }}
      />
      <Composition
        id="OpeningGlover"
        component={OpeningGlover}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingGloverDurationInFrames(60)}
        defaultProps={{
          title: 'THE NAME ON THE PLATE',
          subtitle: 'KANSAS v. GLOVER',
          accent: '#5B8DB8',
          hasLogo: true,
        }}
      />
      <Composition
        id="OpeningCentralpark"
        component={OpeningCentralpark}
        width={1920}
        height={1080}
        fps={60}
        durationInFrames={openingCentralparkDurationInFrames(60)}
        defaultProps={{
          title: 'THE EXONERATED FIVE',
          subtitle: 'CENTRAL PARK - 1989 TO 2002',
          accent: '#2F9FC4',
          hasLogo: true,
        }}
      />
      {CLEV_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-cleveland-0${index + 1}`}
          component={ClevelandThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {GLOVER_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-glover-0${index + 1}`}
          component={GloverThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {STRIEFF_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-strieff-0${index + 1}`}
          component={StrieffThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {CENTRALPARK_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-centralpark-0${index + 1}`}
          component={CentralparkThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {TEKOH_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-tekoh-0${index + 1}`}
          component={TekohThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {TLO_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-tlo-0${index + 1}`}
          component={TloThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {ATWATER_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-atwater-0${index + 1}`}
          component={AtwaterThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {CANIGLIA_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-caniglia-0${index + 1}`}
          component={CanigliaThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {YOUNG_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-young-0${index + 1}`}
          component={YoungThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      {LECH_THUMBS.map((concept, index) => (
        <Still
          key={concept.id}
          id={`Thumb-lech-0${index + 1}`}
          component={LechThumbnail}
          width={1280}
          height={720}
          defaultProps={{concept}}
        />
      ))}
      <Still
        id="ShortThumb-short06"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT06,
          headline: 'STOPPED &\nFRISKED?',
          badge: '8-1',
          backgroundSrc: 'shorts/short06/short06_thumb.png',
        }}
      />
      {/* 16:9 CTR thumbnail for a Short's dedicated YouTube custom thumbnail.
          Render per-short via --props JSON (runs/shorts_thumbs/props/<short>.json). */}
      <Still
        id="ShortThumbYT"
        component={ShortThumbYT}
        width={1280}
        height={720}
        defaultProps={{
          headline: 'STILL\nUNSOLVED',
          subhead: 'THE GARDNER HEIST - 1990',
          heroImage: 'shorts/short20/short20_01.png',
          accent: '#E5B53A',
          badge: 'UNSOLVED',
          focusY: 26,
        }}
      />
      <Still id="Thumb-carsearch-01" component={CarsearchThumbnail} width={1280} height={720} defaultProps={{concept: CARSEARCH_THUMBS[0]}} />
      <Still id="Thumb-carsearch-02" component={CarsearchThumbnail} width={1280} height={720} defaultProps={{concept: CARSEARCH_THUMBS[1]}} />
      <Still id="Thumb-carsearch-03" component={CarsearchThumbnail} width={1280} height={720} defaultProps={{concept: CARSEARCH_THUMBS[2]}} />
      <Still id="Thumb-rolin-01" component={RolinThumbnail} width={1280} height={720} defaultProps={{concept: ROLIN_THUMBS[0]}} />
      <Still id="Thumb-rolin-02" component={RolinThumbnail} width={1280} height={720} defaultProps={{concept: ROLIN_THUMBS[1]}} />
      <Still id="Thumb-rolin-03" component={RolinThumbnail} width={1280} height={720} defaultProps={{concept: ROLIN_THUMBS[2]}} />
      <Still id="Thumb-kidsforcash-01" component={KidsForCashThumbnail} width={1280} height={720} defaultProps={{concept: KIDSFORCASH_THUMBS[0]}} />
      <Still id="Thumb-kidsforcash-02" component={KidsForCashThumbnail} width={1280} height={720} defaultProps={{concept: KIDSFORCASH_THUMBS[1]}} />
      <Still id="Thumb-kidsforcash-03" component={KidsForCashThumbnail} width={1280} height={720} defaultProps={{concept: KIDSFORCASH_THUMBS[2]}} />
      <Composition
        id="Short-short07-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT07, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT07, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short07-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT07, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT07, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short07"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT07,
          headline: 'NO WARRANT?\nNO PHONE SEARCH',
          badge: '9-0',
          backgroundSrc: 'shorts/short07/short07_thumb.png',
        }}
      />
      <Composition
        id="Short-short08-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT08, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT08, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short08-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT08, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT08, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short08"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT08,
          headline: '127 DAYS\nNO WARRANT?',
          badge: '5-4',
          backgroundSrc: 'shorts/short08/short08_thumb.png',
        }}
      />
      <Composition
        id="Short-short09-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT09, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT09, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short09-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT09, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT09, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short09"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT09,
          headline: 'SEIZED\nNO CONVICTION?',
          badge: '9-0',
          backgroundSrc: 'shorts/short09/short09_thumb.png',
        }}
      />
      <Composition
        id="Short-short10-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT10, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT10, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short10-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT10, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT10, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short10"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT10,
          headline: 'THEY TOOK\nHER HOME',
          badge: '5-4',
          backgroundSrc: 'shorts/short10/short10_thumb.png',
        }}
      />
      <Composition
        id="Short-short11-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT11, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT11, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short11-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT11, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT11, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short11"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT11,
          headline: 'PUNISHED\nFOR A POST?',
          badge: '8-1',
          backgroundSrc: 'shorts/short11/short11_thumb.png',
        }}
      />
      <Composition
        id="Short-short12-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT12, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT12, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short12-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT12, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT12, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short12"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT12,
          headline: "YOU CAN'T\nSUE THEM",
          badge: '5-4',
          backgroundSrc: 'shorts/short12/short12_thumb.png',
        }}
      />
      <Composition
        id="Short-short13-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT13, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT13, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short13-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT13, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT13, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short13"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT13,
          headline: 'ARRESTED?\nDNA TAKEN',
          badge: '5-4',
          backgroundSrc: 'shorts/short13/short13_thumb.png',
        }}
      />
      <Composition
        id="Short-short14-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT14, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT14, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short14-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT14, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT14, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short14"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT14,
          headline: 'CHASED INTO\nYOUR HOME?',
          badge: '9-0',
          backgroundSrc: 'shorts/short14/short14_thumb.png',
        }}
      />
      <Composition
        id="Short-short15-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT15, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT15, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short15-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT15, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT15, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short15"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT15,
          headline: '$9 BILLION\nLIE?',
          badge: 'FRAUD',
          backgroundSrc: 'shorts/short15/short15_thumb.png',
        }}
      />
      <Composition
        id="Short-short16-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT16, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT16, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short16-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT16, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT16, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short16"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT16,
          headline: 'ALREADY\nGONE',
          badge: 'DAY 1',
          backgroundSrc: 'shorts/short16/short16_thumb.png',
        }}
      />
      <Composition
        id="Short-short17-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT17, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT17, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short17-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT17, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT17, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short17"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT17,
          headline: 'SHE SOLD\nNOTHING',
          badge: 'MISSING',
          backgroundSrc: 'shorts/short17/short17_thumb.png',
        }}
      />
      <Composition
        id="Short-short18-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT18, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT18, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short18-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT18, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT18, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short18"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT18,
          headline: '$1 TRILLION\nGONE',
          badge: '36 MIN',
          backgroundSrc: 'shorts/short18/short18_thumb.png',
        }}
      />
      <Composition
        id="Short-short19-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT19, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT19, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short19-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT19, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT19, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short19"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT19,
          headline: 'THE SIDE\nDOOR',
          badge: '$25M',
          backgroundSrc: 'shorts/short19/short19_thumb.png',
        }}
      />
      <Composition
        id="Short-short20-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT20, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT20, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short20-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT20, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT20, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short20"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT20,
          headline: 'STILL\nMISSING',
          badge: '$500M',
          backgroundSrc: 'shorts/short20/short20_thumb.png',
        }}
      />
      <Composition
        id="Short-short21-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT21, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT21, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short21-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT21, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT21, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short21"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT21,
          headline: 'HE\nVANISHED',
          badge: '$200K',
          backgroundSrc: 'shorts/short21/short21_thumb.png',
        }}
      />
      <Composition
        id="Short-short22-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT22, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT22, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short22-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT22, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT22, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short22"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT22,
          headline: '98 CHARGES\n6 PLEAS',
          badge: 'PARDONED',
          backgroundSrc: 'shorts/short22/short22_thumb.png',
        }}
      />
      <Composition
        id="Short-short24-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT24, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT24, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short24-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT24, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT24, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short24"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT24,
          headline: 'HIS OWN\nVOICE',
          badge: '11 YEARS',
          backgroundSrc: 'shorts/short24/short24_thumb.png',
        }}
      />
      <Composition
        id="Short-short25-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT25, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT25, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short25-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT25, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT25, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short25"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT25,
          headline: 'NEVER\nWENT IN',
          badge: '5–4',
          backgroundSrc: 'shorts/short25/short25_thumb.png',
        }}
      />
      <Composition
        id="Short-short26-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT26, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT26, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short26-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT26, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT26, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short26"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT26,
          headline: 'STILL A\nSEARCH',
          badge: '1967',
          backgroundSrc: 'shorts/short26/short26_thumb.png',
        }}
      />
      <Composition
        id="Short-short27-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT27, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT27, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short27-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT27, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT27, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short27"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT27,
          headline: 'STOP WAS\nOVER',
          badge: '6–3 · 2015',
          backgroundSrc: 'shorts/short27/short27_thumb.png',
        }}
      />
      {/* Alternate thumbnail options (variant B) — different headline angle for A/B choice */}
      <Still id="ShortThumb-short19-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT19, headline: 'BOUGHT\nA SPOT', badge: '$25M', backgroundSrc: 'shorts/short19/short19_thumb.png'}} />
      <Still id="ShortThumb-short20-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT20, headline: '13 GONE\nNONE FOUND', badge: '$500M', backgroundSrc: 'shorts/short20/short20_thumb.png'}} />
      <Still id="ShortThumb-short21-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT21, headline: 'JUMPED &\nGONE', badge: '$200K', backgroundSrc: 'shorts/short21/short21_thumb.png'}} />
      <Still id="ShortThumb-short22-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT22, headline: 'PARDON ≠\nINNOCENT', badge: '98 → 6', backgroundSrc: 'shorts/short22/short22_thumb.png'}} />
      <Still id="ShortThumb-short24-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT24, headline: 'CAUGHT ON\nWIRETAP', badge: '11 YEARS', backgroundSrc: 'shorts/short24/short24_thumb.png'}} />
      <Still id="ShortThumb-short25-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT25, headline: 'SCANNED\nYOUR HOME', badge: '5–4', backgroundSrc: 'shorts/short25/short25_thumb.png'}} />
      <Still id="ShortThumb-short26-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT26, headline: 'PEOPLE,\nNOT PLACES', badge: '1967', backgroundSrc: 'shorts/short26/short26_thumb.png'}} />
      <Still id="ShortThumb-short27-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT27, headline: '7 MIN\nTOO LONG', badge: '6–3', backgroundSrc: 'shorts/short27/short27_thumb.png'}} />
      <Composition
        id="Short-short23-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT23, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT23, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short23-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT23, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT23, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short23"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT23,
          headline: 'THE VICTIM\nSAID NO',
          badge: '13 CHARGES',
          backgroundSrc: 'shorts/short23/short23_thumb.png',
        }}
      />
      <Composition
        id="Short-short28-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT28, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT28, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short28-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT28, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT28, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short28"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT28,
          headline: 'THE HOUSE\nON TRIAL',
          badge: '$40',
          backgroundSrc: 'shorts/short28/short28_thumb.png',
        }}
      />
      {/* ---- SHORT #29 Hinton (30 years, one bullet) ---- */}
      <Composition
        id="Short-short29-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT29, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT29, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short29-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT29, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT29, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short29"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT29,
          headline: 'INNOCENT —\n30 YEARS',
          badge: '9–0',
          backgroundSrc: 'shorts/short29/short29_thumb.png',
        }}
      />
      <Still id="ShortThumb-short29-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT29, headline: 'A BULLET\nMATCHED NOTHING', badge: 'DEATH ROW', backgroundSrc: 'shorts/short29/short29_thumb.png'}} />
      {/* ---- SHORT #30 Cotton (sure but wrong) ---- */}
      <Composition
        id="Short-short30-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT30, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT30, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short30-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT30, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT30, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short30"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT30,
          headline: 'SURE —\nBUT WRONG',
          badge: 'DNA',
          backgroundSrc: 'shorts/short30/short30_thumb.png',
        }}
      />
      <Still id="ShortThumb-short30-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT30, headline: 'SHE CHOSE\nHIM TWICE', badge: 'WRONG MAN', backgroundSrc: 'shorts/short30/short30_thumb.png'}} />
      {/* ---- SHORT #31 Unlock (thumb vs passcode) ---- */}
      <Composition
        id="Short-short31-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT31, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT31, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short31-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT31, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT31, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short31"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT31,
          headline: 'YOUR THUMB\nOR YOUR MIND?',
          badge: '5TH AMEND.',
          backgroundSrc: 'shorts/short31/short31_thumb.png',
        }}
      />
      <Still id="ShortThumb-short31-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT31, headline: 'THEY CAN\nFORCE YOUR FACE', badge: 'PHONE', backgroundSrc: 'shorts/short31/short31_thumb.png'}} />
      {/* ---- SHORT #32 Car search (Carroll 1925 / Collins 2018 curtilage) ---- */}
      <Composition
        id="Short-short32-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT32, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT32, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short32-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT32, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT32, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short32"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT32,
          headline: 'SEARCH YOUR CAR?\nNOT HERE',
          badge: '8–1',
          backgroundSrc: 'shorts/short32/short32_thumb.png',
        }}
      />
      <Still id="ShortThumb-short32-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT32, headline: 'NO WARRANT\nNEEDED', badge: 'YOUR CAR', backgroundSrc: 'shorts/short32/short32_thumb.png'}} />
      {/* Real DPT depth-map parallax on every still (motion3d slice-1 ported to shorts). EP32 ships depth. */}
      <Composition
        id="Short-short32-depth"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT32, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT32, platform: 'yt' as const, depth: true}}
      />
      <Composition
        id="Short-short32-depth-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT32, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT32, platform: 'tiktok' as const, depth: true}}
      />
      {/* ---- SHORT #33 Tyler v. Hennepin County — PREMIUM (depth + motionkit money/vote/quote scenes) ---- */}
      <Composition
        id="Short-short33-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT33, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT33, platform: 'yt' as const, depth: true}}
      />
      <Composition
        id="Short-short33-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT33, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT33, platform: 'tiktok' as const, depth: true}}
      />
      <Still
        id="ShortThumb-short33"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT33,
          headline: 'THEY KEPT\n$25,000',
          badge: '9–0',
          backgroundSrc: 'shorts/short33/short33_thumb.png',
        }}
      />
      <Still id="ShortThumb-short33-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT33, headline: 'A $15K DEBT.\nA $40K HOME.', badge: 'TAKEN', backgroundSrc: 'shorts/short33/short33_thumb.png'}} />
      {/* ---- SHORT #34 Rolin (airport cash forfeiture) — PREMIUM ---- */}
      <Composition
        id="Short-short34-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT34, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT34, platform: 'yt' as const, depth: true}}
      />
      <Composition
        id="Short-short34-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT34, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT34, platform: 'tiktok' as const, depth: true}}
      />
      <Still
        id="ShortThumb-short34"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT34,
          headline: 'CASH IS\nLEGAL',
          badge: 'SEIZED',
          backgroundSrc: 'shorts/short34/short34_thumb.png',
        }}
      />
      <Still id="ShortThumb-short34-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT34, headline: 'NO CRIME.\nNO CASH BACK.', badge: 'AIRPORT', backgroundSrc: 'shorts/short34/short34_thumb.png'}} />
      {/* ---- SHORT #35 Hinders (IRS structuring seizure) — PREMIUM ---- */}
      <Composition
        id="Short-short35-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT35, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT35, platform: 'yt' as const, depth: true}}
      />
      <Composition
        id="Short-short35-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT35, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT35, platform: 'tiktok' as const, depth: true}}
      />
      <Still
        id="ShortThumb-short35"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT35,
          headline: 'HER ACCOUNT\nSEIZED',
          badge: 'NO CRIME',
          backgroundSrc: 'shorts/short35/short35_thumb.png',
        }}
      />
      <Still id="ShortThumb-short35-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT35, headline: 'UNDER $10K\n= SUSPICIOUS?', badge: 'IRS', backgroundSrc: 'shorts/short35/short35_thumb.png'}} />

      {/* ---- SHORT #36 Riley (phone search at arrest) — loop-designed ---- */}
      <Composition id="Short-short36-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT36, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT36, platform: 'yt' as const, depth: true}} />
      <Composition id="Short-short36-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT36, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT36, platform: 'tiktok' as const, depth: true}} />
      <Still id="ShortThumb-short36" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT36, headline: 'YOUR PHONE?', badge: 'NO WARRANT', backgroundSrc: 'shorts/short36/short36_01.png'}} />

      {/* ---- SHORT #37 Mapp (illegal search, evidence excluded) — loop-designed ---- */}
      <Composition id="Short-short37-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT37, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT37, platform: 'yt' as const, depth: true}} />
      <Composition id="Short-short37-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT37, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT37, platform: 'tiktok' as const, depth: true}} />
      <Still id="ShortThumb-short37" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT37, headline: 'FAKE\nWARRANT', badge: 'MAPP v. OHIO', backgroundSrc: 'shorts/short37/short37_01.png'}} />
      {/* ---- SHORT #38 Williams (facial-recognition wrongful arrest) — PREMIUM (new-shorts batch) ---- */}
      <Composition id="Short-short38-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT38, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT38, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short38-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT38, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT38, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short38" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT38, headline: 'WRONG\nFACE', badge: 'A.I. MATCH', backgroundSrc: 'shorts/short38/short38_01.png'}} />
      {/* ---- SHORT #39 Florence (strip-search after a minor offense) — PREMIUM (new-shorts batch) ---- */}
      <Composition id="Short-short39-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT39, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT39, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short39-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT39, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT39, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short39" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT39, headline: 'STRIPPED\nOVER A FINE', badge: '5–4', backgroundSrc: 'shorts/short39/short39_01.png'}} />
      {/* ---- SHORT #40 Kids for Cash (judges paid to jail children) — PREMIUM (new-shorts batch) ---- */}
      <Composition id="Short-short40-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT40, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT40, platform: 'yt' as const, depth: true}} />
      <Composition id="Short-short40-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT40, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT40, platform: 'tiktok' as const, depth: true}} />
      <Still id="ShortThumb-short40" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT40, headline: 'KIDS FOR\nCASH', badge: '28 YEARS', backgroundSrc: 'shorts/short40/short40_01.png'}} />
      {/* ---- SHORT #40m Kids for Cash — SHORTS_METHOD v001 REFERENCE (does NOT touch scheduled short40) ---- */}
      <Composition id="Short-short40m-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT40M, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT40M, platform: 'yt' as const, depth: false, method: true}} />
      <Composition id="Short-short40m-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT40M, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT40M, platform: 'tiktok' as const, depth: false, method: true}} />
      <Still id="ShortThumb-short40m" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT40M, headline: 'KIDS FOR\nCASH', badge: '28 YEARS', backgroundSrc: 'shorts/short40m/short40m_judge.png'}} />
      {/* ---- SHORT #41 Frazier (police deception, false confession) — PREMIUM (new-shorts batch) ---- */}
      <Composition id="Short-short41-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT41, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT41, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short41-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT41, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT41, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short41" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT41, headline: 'THE PRINTS\nWERE FAKE', badge: '16 YEARS', backgroundSrc: 'shorts/short41/short41_01.png'}} />
      {/* ---- SHORT #42 Lech (police destroyed a family's house) — PREMIUM (new-shorts batch) ---- */}
      <Composition id="Short-short42-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT42, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT42, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short42-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT42, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT42, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short42" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT42, headline: 'POLICE BROKE\nHIS HOUSE', badge: 'NOTHING OWED', backgroundSrc: 'shorts/short42/short42_01.png'}} />
      {/* ---- SHORT #43 Thompson (Connick v. Thompson, hidden blood evidence) — PREMIUM (new-shorts batch) ---- */}
      <Composition id="Short-short43-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT43, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT43, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short43-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT43, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT43, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short43" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT43, headline: '14 YEARS\nON A LIE', badge: '5–4', backgroundSrc: 'shorts/short43/short43_01.png'}} />
      {/* ---- SHORT #46 Tekoh (Vega v. Tekoh, a Miranda warning never read) — PREMIUM (EP44) ---- */}
      <Composition id="Short-short46-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT46, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT46, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short46-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT46, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT46, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short46" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT46, headline: 'NO WARNING\nNO PAYOUT', badge: '6–3', backgroundSrc: 'shorts/short46/short46_03.png'}} />
      {/* ---- SHORT #47 Cleveland (Bearden v. Georgia, jailed for being too poor) — PREMIUM (EP45) ---- */}
      <Composition id="Short-short47-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT47, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT47, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short47-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT47, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT47, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short47" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT47, headline: 'JAILED FOR\nBEING POOR', badge: '1983', backgroundSrc: 'shorts/short47/short47_04.png'}} />
      {/* ---- SHORT #48 T.L.O. (New Jersey v. T.L.O., the schoolhouse 4th Amendment) — PREMIUM (EP46) ---- */}
      <Composition id="Short-short48-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT48, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT48, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short48-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT48, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT48, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short48" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT48, headline: 'SEARCHED\nAT SCHOOL', badge: '6–3', backgroundSrc: 'shorts/short48/short48_01.png'}} />
      <Still id="ShortThumb-short48-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT48, headline: 'A LOWER\nBAR', badge: '6–3', backgroundSrc: 'shorts/short48/short48_01.png'}} />
      {/* ---- SHORT #49 Atwater (Atwater v. Lago Vista, arrest for a fine-only offense) — PREMIUM (EP47) ---- */}
      <Composition id="Short-short49-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT49, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT49, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short49-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT49, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT49, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short49" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT49, headline: 'JAILED OVER\nA SEATBELT', badge: '5–4', backgroundSrc: 'shorts/short49/short49_01.png'}} />
      <Still id="ShortThumb-short49-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT49, headline: 'A $50\nARREST', badge: '5–4', backgroundSrc: 'shorts/short49/short49_01.png'}} />
      {/* ---- SHORT #50 Glover (Kansas v. Glover, plate-check traffic stop) — PREMIUM (EP48) ---- */}
      <Composition id="Short-short50-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT50, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT50, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short50-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT50, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT50, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short50" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT50, headline: 'A NAME ON\nA PLATE', badge: '8–1', backgroundSrc: 'shorts/short50/short50_01.png'}} />
      <Still id="ShortThumb-short50-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT50, headline: 'STOPPED\nON A GUESS', badge: '8–1', backgroundSrc: 'shorts/short50/short50_04.png'}} />
      {/* ---- SHORT #51 Strieff (Utah v. Strieff, illegal stop + attenuation) — PREMIUM (EP49) ---- */}
      <Composition id="Short-short51-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT51, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT51, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short51-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT51, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT51, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short51" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT51, headline: 'AN ILLEGAL\nSTOP. LEGAL.', badge: '5–3', backgroundSrc: 'shorts/short51/short51_01.png'}} />
      <Still id="ShortThumb-short51-B" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT51, headline: 'THE WARRANT\nIN YOUR POCKET', badge: '5–3', backgroundSrc: 'shorts/short51/short51_04.png'}} />
      {/* ---- SHORT #52 Young (wrong-house raid) — PREMIUM (EP42) ---- */}
      <Composition id="Short-short52-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT52, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT52, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short52-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT52, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT52, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short52" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT52, headline: 'WRONG\nHOUSE?', badge: '$2.9M', backgroundSrc: 'shorts/short52/short52_02.png'}} />
      {/* ---- SHORT #53 Caniglia (community caretaking, 9-0) — PREMIUM (EP43) ---- */}
      <Composition id="Short-short53-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT53, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT53, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short53-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT53, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT53, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short53" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT53, headline: 'JUST TO\nHELP?', badge: '9–0', backgroundSrc: 'shorts/short53/short53_01.png'}} />
      {/* ---- SHORT #54 Central Park Five (false confessions) — PREMIUM (EP50) ---- */}
      <Composition id="Short-short54-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT54, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT54, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short54-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT54, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT54, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short54" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT54, headline: 'THEY ALL\nCONFESSED', badge: 'VACATED', backgroundSrc: 'shorts/short54/short54_02.png'}} />
      {/* ---- SHORT #55 Willingham (arson science) — PREMIUM (EP51) ---- */}
      <Composition id="Short-short55-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT55, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT55, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short55-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT55, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT55, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short55" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT55, headline: 'NO\nCRIME?', badge: '2004', backgroundSrc: 'shorts/short55/short55_01.png'}} />
      {/* ---- SHORT #56 Morton (Brady violation) — PREMIUM (EP52) ---- */}
      <Composition id="Short-short56-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT56, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT56, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short56-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT56, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT56, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short56" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT56, headline: 'THE MONSTER\nWAS REAL', badge: 'EXONERATED', backgroundSrc: 'shorts/short56/short56_01.png'}} />
      {/* ---- SHORT #57 Norfolk Four (serial false confessions) — PREMIUM (EP53) ---- */}
      <Composition id="Short-short57-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT57, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT57, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short57-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT57, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT57, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short57" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT57, headline: '4 CONFESSIONS.\n0 KILLERS.', badge: 'INNOCENT', backgroundSrc: 'shorts/short57/short57_02.png'}} />
      {/* ---- SHORT #58 Flowers (tried six times, 7-2) — PREMIUM (EP54) ---- */}
      <Composition id="Short-short58-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT58, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT58, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short58-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT58, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT58, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short58" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT58, headline: 'TRIED\n6 TIMES', badge: '7–2', backgroundSrc: 'shorts/short58/short58_01.png'}} />
      {/* ---- SHORT #59 Burge (the Midnight Crew) — PREMIUM (EP55) ---- */}
      <Composition id="Short-short59-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT59, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT59, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short59-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT59, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT59, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short59" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT59, headline: 'TAUGHT IN\nSCHOOLS', badge: 'REPARATIONS', backgroundSrc: 'shorts/short59/short59_03.png'}} />
      {/* ---- SHORT #60 Norfolk Four (they fixed the confession) — PREMIUM (EP53) ---- */}
      <Composition id="Short-short60-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT60, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT60, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short60-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT60, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT60, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short60" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT60, headline: 'THEY FIXED\nTHE CONFESSION', badge: 'INNOCENT', backgroundSrc: 'shorts/short60/short60_10.png'}} />
      {/* ---- SHORT #63 Flowers (the juror who voted not guilty) — PREMIUM (EP54) ---- */}
      <Composition id="Short-short63-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT63, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT63, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short63-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT63, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT63, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short63" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT63, headline: 'HE VOTED\nNOT GUILTY', badge: 'HANDCUFFED', backgroundSrc: 'shorts/short63/short63_09.png'}} />
      {/* ---- SHORT #66 Burge (the letter that was buried) — PREMIUM (EP55) ---- */}
      <Composition id="Short-short66-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT66, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT66, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short66-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT66, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT66, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short66" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT66, headline: 'THEY BURIED\nTHE LETTER', badge: '1982', backgroundSrc: 'shorts/short66/short66_04.png'}} />
      <Composition
        id="Short-short01-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT01, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT01, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short01-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT01, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT01, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short01"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT01,
          headline: 'WHY READ\nYOUR RIGHTS?',
          badge: '1966',
          backgroundSrc: 'shorts/short01/short01_thumb.png',
        }}
      />
      <Composition
        id="Short-short02-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT02, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT02, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short02-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT02, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT02, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short02"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT02,
          headline: "CAN'T AFFORD\nA LAWYER?",
          badge: '9-0',
          backgroundSrc: 'shorts/short02/short02_thumb.png',
        }}
      />
      <Composition
        id="Short-short03-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT03, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT03, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short03-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT03, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT03, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short03"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT03,
          headline: 'ILLEGAL SEARCH?\nEVIDENCE OUT',
          badge: '1961',
          backgroundSrc: 'shorts/short03/short03_thumb.png',
        }}
      />
      <Composition
        id="Short-short04-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT04, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT04, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short04-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT04, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT04, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short04"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT04,
          headline: '$8 BILLION\nGONE?',
          badge: 'FRAUD',
          backgroundSrc: 'shorts/short04/short04_thumb.png',
        }}
      />
      <Composition
        id="Short-short05-yt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT05, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT05, platform: 'yt' as const}}
      />
      <Composition
        id="Short-short05-tt"
        component={Short}
        durationInFrames={shortDurationInFrames(SHORT05, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={1080}
        height={1920}
        defaultProps={{data: SHORT05, platform: 'tiktok' as const}}
      />
      <Still
        id="ShortThumb-short05"
        component={ShortThumb}
        width={1080}
        height={1920}
        defaultProps={{
          data: SHORT05,
          headline: 'STEADY RETURNS\nZERO TRADES',
          badge: 'PONZI',
          backgroundSrc: 'shorts/short05/short05_thumb.png',
        }}
      />
      <Composition
        id="Opening"
        component={Opening}
        durationInFrames={Math.round(BRAND.video.fps * 2.5)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{channelName: 'Prime Documentary'}}
      />
      <Composition
        id="MirandaEpisode"
        component={Episode}
        durationInFrames={Math.round(BRAND.video.fps * 12 * 60)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          title: 'Why Do Police Read You Your Rights?',
          channelName: 'Prime Documentary',
          sections: TEMPLATE_12MIN,
        }}
      />
      <Composition
        id="GideonAnimatic"
        component={Animatic}
        durationInFrames={durationInFramesFor(GIDEON_ANIMATIC, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          bgmSrc: null as string | null,
          scenes: GIDEON_ANIMATIC,
          sceneImg: GIDEON_SCENE_IMG,
        }}
      />
      <Composition
        id="GideonPremium"
        component={GideonPremium}
        durationInFrames={gideonPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="MirandaPremium"
        component={MirandaPremium}
        durationInFrames={mirandaPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="MappPremium"
        component={MappPremium}
        durationInFrames={mappPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="MadoffPremium"
        component={MadoffPremium}
        durationInFrames={madoffPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TimbsPremium"
        component={TimbsPremium}
        durationInFrames={timbsPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDCore5"
        component={PDCore5Preview}
        durationInFrames={core5PreviewDuration(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TimbsB1"
        component={TimbsB1}
        durationInFrames={timbsB1DurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TimbsB2"
        component={TimbsB2}
        durationInFrames={timbsB2DurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TimbsC3"
        component={TimbsC3}
        durationInFrames={timbsC3DurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDTest60"
        component={PDTest60}
        durationInFrames={pdTest60Duration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDNewLook"
        component={PDNewLook}
        durationInFrames={pdNewLookDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PD3DShowcase"
        component={PD3DShowcase}
        durationInFrames={pd3DShowcaseDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDAllTools"
        component={PDAllTools}
        durationInFrames={pdAllToolsDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDForfeiture60"
        component={PDForfeiture60}
        durationInFrames={pdForfeiture60Duration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDDepthFixed"
        component={PDDepthFixed}
        durationInFrames={pdDepthFixedDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDReel"
        component={PDReel}
        durationInFrames={pdReelDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="PDOriginal"
        component={PDOriginal}
        durationInFrames={pdOriginalDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="FlorenceWarrantScreen"
        component={WarrantScreen}
        durationInFrames={warrantScreenDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition id="FlorenceRecordsDrawer" component={RecordsDrawer} durationInFrames={recordsDrawerDuration} fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height} />
      <Composition id="FlorenceReceiptStamp" component={ReceiptStamp} durationInFrames={receiptStampDuration} fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height} />
      <Composition id="FlorenceVerdictSeam" component={VerdictSeam} durationInFrames={verdictSeamDuration} fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height} />
      <Composition id="FlorenceBodyLine" component={BodyLine} durationInFrames={bodyLineDuration} fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height} />
      <Composition
        id="PDAIHero"
        component={PDAIHero}
        durationInFrames={pdAIHeroDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {/* EP37 Florence — DETERMINISTIC 106-cut assembly (04_scenes/assembly_spec.v001.md).
          Cut durations are locked to the ElevenLabs master via florence_words.json
          (Σ=16288f=542.93s≈9:03). WordBand captions are live. FINAL render uses --muted;
          the narration + SFX + per-act BGM bed is muxed in ffmpeg (06_audio/mix_plan.v001.md). */}
      <Composition
        id="Florence"
        component={Florence}
        durationInFrames={florenceDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TimbsDepthTest"
        component={TimbsDepthTest}
        durationInFrames={timbsDepthTestDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TimbsParallax"
        component={TimbsParallax}
        durationInFrames={timbsParallaxDuration}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="KeloPremium"
        component={KeloPremium}
        durationInFrames={keloPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="MahanoyPremium"
        component={MahanoyPremium}
        durationInFrames={mahanoyPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="ArbitrationPremium"
        component={ArbitrationPremium}
        durationInFrames={arbitrationPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="KingPremium"
        component={KingPremium}
        durationInFrames={kingPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="LangePremium"
        component={LangePremium}
        durationInFrames={langePremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TheranosPremium"
        component={TheranosPremium}
        durationInFrames={theranosPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TitanPremium"
        component={TitanPremium}
        durationInFrames={titanPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="OneCoinPremium"
        component={OneCoinPremium}
        durationInFrames={oneCoinPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="FlashCrashPremium"
        component={FlashCrashPremium}
        durationInFrames={flashCrashPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="VarsityBluesPremium"
        component={VarsityBluesPremium}
        durationInFrames={varsityBluesPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="GardnerPremium"
        component={GardnerPremium}
        durationInFrames={gardnerPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="SwartzPremium"
        component={SwartzPremium}
        durationInFrames={swartzPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="RajaratnamPremium"
        component={RajaratnamPremium}
        durationInFrames={rajaratnamPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      {([
        ['cold_open', 'cold-open'],
        ['the_promise', 'the-promise'],
        ['the_crack', 'the-crack'],
        ['the_void', 'the-void'],
        ['coda', 'coda'],
      ] as const).map(([chapterId, chapterSlug]) => (
        <Composition
          key={`OneCoinPremium-${chapterSlug}`}
          id={`OneCoinPremium-${chapterSlug}`}
          component={OneCoinPremium}
          durationInFrames={oneCoinPremiumDurationInFrames(BRAND.video.fps, chapterId)}
          fps={BRAND.video.fps}
          width={BRAND.video.width}
          height={BRAND.video.height}
          defaultProps={{chapterId}}
        />
      ))}
      {(['A', 'B', 'C'] as const).map((option) => (
        <Still
          key={`OneCoinThumb-${option}`}
          id={`OneCoinThumb-${option}`}
          component={OneCoinThumbnailFrame}
          width={1280}
          height={720}
          defaultProps={{option}}
        />
      ))}
      {/* EP35 hinders — assembled from scene_plan (figures/heroes wired). Placeholder timing
          until the audio thread's narration lands; re-run build_hinders_film.py to stamp seconds. */}
      {/* EP38 kids-for-cash — canonical CaseFilm (Bookends + 8s highlight hook + depth
          parallax + kinetic type + AmbientMotion + no-repeat footage). */}
      <Composition
        id="Ep38KidsForCash"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(kidsforcashFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: kidsforcashFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'Kids for Cash',
          subtitle: 'Two judges. A private jail. Thousands of children.',
        }}
      />
      <Composition
        id="Ep35Hinders"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(hindersFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: hindersFilm as unknown as FilmData,
          seriesLabel: 'THEY FOLLOWED THE RULES',
          title: 'Following the Rule',
          subtitle: 'United States v. $32,820.56 (civil forfeiture / IRS structuring)',
        }}
      />
      <Composition
        id="CaseFilm-forfeiture"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(forfeitureFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: forfeitureFilm as unknown as FilmData,
          seriesLabel: 'THEY DID NOTHING WRONG',
          title: 'They Took the House',
          subtitle: 'Sourovelis v. City of Philadelphia (2018)',
        }}
      />
      <Composition
        id="CaseFilm-carsearch"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(carsearchFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: carsearchFilm as unknown as FilmData,
          seriesLabel: 'KNOW YOUR RIGHTS',
          title: 'Can the Police Search Your Car?',
          subtitle: 'Carroll (1925) · Collins v. Virginia (2018)',
        }}
      />
      {/* EP34 rolin — airport civil forfeiture. 60fps super-heavy (data.fps=60; CaseFilm reads
          useVideoConfig().fps). Blender heroes composite via data.heroCuts. */}
      <Composition
        id="CaseFilm-rolin"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(rolinFilm as unknown as FilmData, 60)}
        fps={60}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: rolinFilm as unknown as FilmData,
          seriesLabel: 'KNOW YOUR RIGHTS',
          title: 'They Took His Cash at the Airport',
          subtitle: 'Civil Forfeiture · No Charge · No Crime',
        }}
      />
      <Composition
        id="CaseFilm-hinton"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(hintonFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: hintonFilm as unknown as FilmData,
          seriesLabel: 'THEY DID NOTHING WRONG',
          title: 'Thirty Years in the Dark',
          subtitle: 'Hinton v. Alabama (2014)',
        }}
      />
      {/* EP29 thumbnails (1280x720). backgroundSrc = Codex bespoke art staged to
          remotion/public/hinton/thumb/bg{1,2,3}.png (see 10_thumbnail/CODEX_BACKGROUNDS.md).
          Render + select via scripts/build_hinton_thumbnails.py once the art lands. */}
      <Still
        id="Thumb-hinton-A"
        component={ThumbnailFrame}
        width={1280}
        height={720}
        defaultProps={{title: '30 YEARS. INNOCENT.', backgroundSrc: 'hinton/thumb/bg1.png', variant: 'left'}}
      />
      <Still
        id="Thumb-hinton-B"
        component={ThumbnailFrame}
        width={1280}
        height={720}
        defaultProps={{title: 'THE BULLETS LIED', backgroundSrc: 'hinton/thumb/bg2.png', variant: 'left'}}
      />
      <Still
        id="Thumb-hinton-C"
        component={ThumbnailFrame}
        width={1280}
        height={720}
        defaultProps={{title: 'THEY WANTED HIM DEAD', backgroundSrc: 'hinton/thumb/bg3.png', variant: 'center'}}
      />
      <Composition
        id="CaseFilm-kyllo"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(kylloFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: kylloFilm as unknown as FilmData,
          seriesLabel: 'LANDMARK RIGHTS',
          title: 'They Scanned His Home From the Street',
          subtitle: 'Kyllo v. United States (2001)',
        }}
      />
      <Composition
        id="CaseFilm-tyler"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(tylerFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: tylerFilm as unknown as FilmData,
          seriesLabel: 'THEY DID NOTHING WRONG',
          title: 'The $2,300 That Took a House',
          subtitle: 'Tyler v. Hennepin County (2023)',
        }}
      />
      {/* EP36 williams — first known US wrongful arrest from facial-recognition misidentification.
          SKELETON timing (estimated seconds); hero stills under williams/img/ are generated
          separately and are intentionally absent until the image+factory step lands. */}
      <Composition
        id="CaseFilm-williams"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(williamsFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: williamsFilm as unknown as FilmData,
          seriesLabel: 'THEY DID NOTHING WRONG',
          title: 'Arrested by an Algorithm',
          subtitle: 'Williams v. City of Detroit (facial-recognition wrongful arrest)',
        }}
      />
      {/* EP36 williams — PREMIUM ANIMATION cut (beatsheet-driven; replaces the still-heavy
          CaseFilm-williams). 128 beats @30fps, ~11.89min. Duration read from the beatsheet meta. */}
      <Composition
        id="WilliamsFilm"
        component={WilliamsFilm}
        durationInFrames={williamsFilmDurationInFrames()}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="CaseFilm-katz"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(katzFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: katzFilm as unknown as FilmData,
          seriesLabel: 'LANDMARK RIGHTS',
          title: 'The FBI Recorded His Calls — and Never Touched the Booth',
          subtitle: 'Katz v. United States (1967)',
        }}
      />
      <Composition
        id="CaseFilm-rodriguez"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(rodriguezFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: rodriguezFilm as unknown as FilmData,
          seriesLabel: 'LANDMARK RIGHTS',
          title: 'How Long Can the Police Keep You at a Traffic Stop?',
          subtitle: 'Rodriguez v. United States (2015)',
        }}
      />
      <Composition
        id="CaseFilm-cotton"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(cottonFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: cottonFilm as unknown as FilmData,
          seriesLabel: 'TRUE CRIME JUSTICE',
          title: 'The Face She Was Sure Of',
          subtitle: 'Ronald Cotton and Jennifer Thompson',
        }}
      />
      <Composition
        id="CaseFilm-unlock"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(unlockFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: unlockFilm as unknown as FilmData,
          seriesLabel: 'YOUR RIGHTS',
          title: 'Can the Police Force Your Phone Open?',
          subtitle: 'Your face, your thumb, your mind',
        }}
      />
      <Composition
        id="MotionSample"
        component={MotionSample}
        durationInFrames={motionSampleDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="TylerFigures"
        component={TylerFigures}
        durationInFrames={tylerFiguresDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="StyleTest"
        component={StyleTest}
        durationInFrames={BRAND.video.fps * 60}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{bgmSrc: 'bgm_placeholder.wav' as string | null}}
      />
      <Composition
        id="Animatic"
        component={Animatic}
        durationInFrames={animaticDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{bgmSrc: 'bgm_placeholder.wav' as string | null}}
      />
      <Composition
        id="ClipProof"
        component={ClipProof}
        durationInFrames={Math.round(BRAND.video.fps * 5)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          src: 'proof_clip.mp4',
          hook: 'You have the right to remain silent.',
          citation: 'Miranda v. Arizona, 384 U.S. 436 (1966)',
          reconstruction: true,
        }}
      />
      <Composition
        id="ColdOpen"
        component={ColdOpen}
        durationInFrames={hookDurationInFrames(MIRANDA_HOOK)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{beats: MIRANDA_HOOK}}
      />
      <Still
        id="ThumbConcept"
        component={ThumbConcept}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          kicker: 'MIRANDA v. ARIZONA',
          line1: 'Won.',
          line2: 'Still jailed.',
          sub: 'How 4 words rewrote every U.S. arrest',
          symbol: 'bars' as const,
        }}
      />
      <Still
        id="ThumbnailFrame"
        component={ThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          title: 'Why Do Police Read You Your Rights?',
          backgroundSrc: null,
          variant: 'left' as const,
        }}
      />
      <Still
        id="MirandaThumbnailA"
        component={ThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          title: 'The 4 Sentences That Rewrote Every U.S. Arrest',
          backgroundSrc: 'miranda/thumbs/THUMB-01.png',
          variant: 'left' as const,
        }}
      />
      <Still
        id="MirandaThumbnailB"
        component={ThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          title: 'He Won at the Supreme Court — and Still Went to Prison',
          backgroundSrc: 'miranda/thumbs/THUMB-01.png',
          variant: 'left' as const,
        }}
      />
      <Still
        id="MirandaThumbnailC"
        component={ThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          title: 'Why Police MUST Read You Your Rights',
          backgroundSrc: 'miranda/thumbs/THUMB-01.png',
          variant: 'left' as const,
        }}
      />
      <Still
        id="MirandaThumbnailA2"
        component={MirandaThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          backgroundSrc: 'miranda/thumbs/THUMB-05.png',
          line1: 'READ RIGHTS',
          line2: "OR IT'S OUT",
          badge: 'The warning police must say',
          variant: 'red_alert' as const,
        }}
      />
      <Still
        id="MirandaThumbnailB2"
        component={MirandaThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          backgroundSrc: 'miranda/thumbs/THUMB-01.png',
          line1: 'HE WON',
          line2: 'STILL GUILTY',
          badge: 'The twist behind Miranda rights',
          variant: 'gold_verdict' as const,
        }}
      />
      <Still
        id="MirandaThumbnailC2"
        component={MirandaThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          backgroundSrc: 'miranda/thumbs/THUMB-05.png',
          line1: 'POLICE',
          line2: 'MUST SAY THIS',
          badge: 'Miranda rights explained',
          variant: 'blue_rights' as const,
        }}
      />
      <Still
        id="KeloThumbnailFrame"
        component={KeloThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          backgroundSrc: 'kelo/thumbs/THUMB-02.png',
          headlineTop: 'YOUR HOME',
          headlineBottom: 'TAKEN?',
          badge: 'FOR A DEVELOPER',
          variant: 'taken' as const,
        }}
      />
      <Still
        id="TylerThumbnail-A-disproportion"
        component={TylerThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{variant: 'disproportion' as const}}
      />
      <Still
        id="TylerThumbnail-B-surplus"
        component={TylerThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{variant: 'surplus' as const}}
      />
      <Still
        id="TylerThumbnail-C-legal"
        component={TylerThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{variant: 'legal' as const}}
      />
      <Still
        id="KingThumbnailFrame"
        component={KingThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          backgroundSrc: 'king/SPN-0004.png',
          line1: 'DNA AT',
          line2: 'ARREST?',
          badge: 'MARYLAND v. KING',
          variant: 'left' as const,
        }}
      />
    </>
  );
};
