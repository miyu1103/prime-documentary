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
import {RobosigningFilm, robosigningFilmDurationInFrames} from './compositions/RobosigningFilm';
import {LejeuneFilm, lejeuneFilmDurationInFrames} from './compositions/LejeuneFilm';
import {SurfsideFilm, surfsideFilmDurationInFrames} from './compositions/SurfsideFilm';
import {WeimerFilm, weimerFilmDurationInFrames} from './compositions/WeimerFilm';
import {FieldtestFilm, fieldtestFilmDurationInFrames} from './compositions/FieldtestFilm';
import {GreeneFilm, greeneFilmDurationInFrames} from './compositions/GreeneFilm';
import {CorreaFilm, correaFilmDurationInFrames} from './compositions/CorreaFilm';
import {MemphisFilm, memphisFilmDurationInFrames} from './compositions/MemphisFilm';
import {MarmetFilm, marmetFilmDurationInFrames} from './compositions/MarmetFilm';
import {PintoFilm, pintoFilmDurationInFrames} from './compositions/PintoFilm';
import {OpenfieldsFilm, openfieldsFilmDurationInFrames} from './compositions/OpenfieldsFilm';
import {HyattFilm, hyattFilmDurationInFrames} from './compositions/HyattFilm';
import {WronghouseFilm, wronghouseFilmDurationInFrames} from './compositions/WronghouseFilm';
import {OrovilleFilm, orovilleFilmDurationInFrames} from './compositions/OrovilleFilm';
import {ItaewonFilm, itaewonFilmDurationInFrames} from './compositions/ItaewonFilm';
import {LahainaFilm, lahainaFilmDurationInFrames} from './compositions/LahainaFilm';
import {MorandiFilm, morandiFilmDurationInFrames} from './compositions/MorandiFilm';
import {KeyBridgeFilm, keybridgeFilmDurationInFrames} from './compositions/KeyBridgeFilm';
import {ConcordiaFilm, concordiaFilmDurationInFrames} from './compositions/ConcordiaFilm';
import {StationFilm, stationFilmDurationInFrames} from './compositions/StationFilm';
import {RamirezFilm, ramirezFilmDurationInFrames} from './compositions/RamirezFilm';
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
import lacmeganticFilm from './data/lacmegantic_film.json';
import uriFilm from './data/uri_film.json';
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
import {SHORT82} from './data/short82';
import {SHORT86} from './data/short86';
import {SHORT87} from './data/short87';
import {SHORT88} from './data/short88';
import {SHORT89} from './data/short89';
import {SHORT90} from './data/short90';
import {SHORT91} from './data/short91';
import {SHORT92} from './data/short92';
import {SHORT93} from './data/short93';
import {SHORT94} from './data/short94';
import {SHORT95} from './data/short95';
import {SHORT96} from './data/short96';
import {SHORT97} from './data/short97';
import {SHORT98} from './data/short98';
import {SHORT99} from './data/short99';
import {SHORT01} from './data/short01';
import {SHORT02} from './data/short02';
import {SHORT03} from './data/short03';
import {SHORT04} from './data/short04';
import {SHORT05} from './data/short05';
import {SHORT100} from './data/short100';
import {SHORT101} from './data/short101';
import {SHORT102} from './data/short102';
import {SHORT103} from './data/short103';
import {SHORT104} from './data/short104';
import {SHORT105} from './data/short105';
import {SHORT106} from './data/short106';
import {SHORT107} from './data/short107';
import {SHORT108} from './data/short108';
import {SHORT109} from './data/short109';
import {SHORT110} from './data/short110';
import {SHORT111} from './data/short111';
import {SHORT112} from './data/short112';
import {SHORT113} from './data/short113';
import {SHORT114} from './data/short114';
import {SHORT115} from './data/short115';
import {SHORT116} from './data/short116';
import {SHORT117} from './data/short117';
import {SHORT118} from './data/short118';
import {SHORT119} from './data/short119';
import {SHORT120} from './data/short120';
import {SHORT132} from './data/short132';
import {SHORT133} from './data/short133';
import {SHORT134} from './data/short134';
import {SHORT121} from './data/short121';
import {SHORT122} from './data/short122';
import {SHORT130} from './data/short130';
import {SHORT131} from './data/short131';
import {SHORT135} from './data/short135';
import {SHORT136} from './data/short136';
import {SHORT137} from './data/short137';
import {SHORT138} from './data/short138';
import {SHORT139} from './data/short139';
import {SHORT140} from './data/short140';
import {SHORT141} from './data/short141';
import {SHORT142} from './data/short142';
import {SHORT143} from './data/short143';
import {SHORT144} from './data/short144';
import {SHORT145} from './data/short145';
import {SHORT150} from './data/short150';
import {SHORT151} from './data/short151';
import {SHORT152} from './data/short152';
import {SHORT153} from './data/short153';
import {SHORT154} from './data/short154';
import {SHORT155} from './data/short155';
import {SHORT156} from './data/short156';
import {SHORT157} from './data/short157';
import {SHORT158} from './data/short158';
import {SHORT159} from './data/short159';
import {SHORT160} from './data/short160';
import {SHORT161} from './data/short161';
import {SHORT162} from './data/short162';
import {SHORT163} from './data/short163';
import {SHORT164} from './data/short164';
import {SHORT165} from './data/short165';
import {SHORT170} from './data/short170';
import {SHORT171} from './data/short171';
import {SHORT172} from './data/short172';
import {SHORT173} from './data/short173';
import {SHORT174} from './data/short174';
import {SHORT175} from './data/short175';
import {SHORT176} from './data/short176';
import {SHORT177} from './data/short177';
import {SHORT178} from './data/short178';
import {SHORT179} from './data/short179';
import {SHORT180} from './data/short180';
import {SHORT181} from './data/short181';
import {MAHANOY_ROUGHCUT} from './data/mahanoy_roughcut';
import {TIMBS_ROUGHCUT} from './data/timbs_roughcut';
import {KELO_ROUGHCUT} from './data/kelo_roughcut';
import {ARBITRATION_ROUGHCUT} from './data/arbitration_roughcut';
import {KING_ROUGHCUT} from './data/king_roughcut';
import {LANGE_ROUGHCUT} from './data/lange_roughcut';
import {THERANOS_ROUGHCUT} from './data/theranos_roughcut';
import {TITAN_ROUGHCUT} from './data/titan_roughcut';
import {ONECOIN_ROUGHCUT} from './data/onecoin_roughcut';
import {SHORT182} from './data/short182';
import {SHORT183} from './data/short183';
import {SHORT184} from './data/short184';
import {SHORT185} from './data/short185';
import {SHORT186} from './data/short186';
import {SHORT187} from './data/short187';
import {SHORT188} from './data/short188';
import {SHORT189} from './data/short189';
import {SHORT190} from './data/short190';
import {SHORT191} from './data/short191';
import {SHORT192} from './data/short192';
import {SHORT193} from './data/short193';
import {SHORT194} from './data/short194';
import {SHORT195} from './data/short195';
import {SHORT196} from './data/short196';
import {SHORT197} from './data/short197';
import {SHORT200} from './data/short200';
import {SHORT201} from './data/short201';
import {SHORT202} from './data/short202';
import {SHORT203} from './data/short203';
import {SHORT204} from './data/short204';
import {SHORT205} from './data/short205';
import {SHORT250} from './data/short250';
import {SHORT251} from './data/short251';
import {SHORT252} from './data/short252';
import {SHORT253} from './data/short253';
import {SHORT254} from './data/short254';
import {SHORT255} from './data/short255';
import {SHORT256} from './data/short256';
import {SHORT257} from './data/short257';
import {SHORT258} from './data/short258';
import {SHORT259} from './data/short259';
import {SHORT260} from './data/short260';
import {SHORT261} from './data/short261';
import {SHORT262} from './data/short262';
import {SHORT263} from './data/short263';
import {SHORT264} from './data/short264';
import {SHORT265} from './data/short265';
import {SHORT266} from './data/short266';
import {SHORT267} from './data/short267';
import {SHORT268} from './data/short268';
import {SHORT269} from './data/short269';
import {SHORT270} from './data/short270';
import {SHORT271} from './data/short271';
import {SHORT272} from './data/short272';
import {SHORT273} from './data/short273';
import {SHORT274} from './data/short274';
import {SHORT275} from './data/short275';
import {SHORT276} from './data/short276';
import {SHORT277} from './data/short277';
import {SHORT278} from './data/short278';
import {SHORT279} from './data/short279';
import {SHORT280} from './data/short280';
import {SHORT281} from './data/short281';
import {SHORT282} from './data/short282';
import {SHORT289} from './data/short289';
import {SHORT290} from './data/short290';
import {SHORT291} from './data/short291';
import {SHORT292} from './data/short292';
import {SHORT293} from './data/short293';
import {SHORT294} from './data/short294';
import {SHORT295} from './data/short295';
import {SHORT296} from './data/short296';
import {SHORT297} from './data/short297';
import {SHORT298} from './data/short298';
import {SHORT299} from './data/short299';
import {SHORT300} from './data/short300';
import {SHORT301} from './data/short301';
import {SHORT302} from './data/short302';
import {SHORT303} from './data/short303';
import {SHORT304} from './data/short304';
import {SHORT305} from './data/short305';
import {SHORT306} from './data/short306';
import {SHORT307} from './data/short307';
import {SHORT308} from './data/short308';
import {SHORT309} from './data/short309';
import {SHORT310} from './data/short310';
import {SHORT311} from './data/short311';
import {SHORT312} from './data/short312';
import {SHORT313} from './data/short313';
import {SHORT314} from './data/short314';
import {SHORT315} from './data/short315';
import {SHORT316} from './data/short316';
import {SHORT317} from './data/short317';
import {SHORT318} from './data/short318';
import {SHORT319} from './data/short319';
import {SHORT320} from './data/short320';
import {SHORT321} from './data/short321';
import {SHORT322} from './data/short322';
import {SHORT323} from './data/short323';
import {SHORT324} from './data/short324';
import {SHORT325} from './data/short325';
import {SHORT326} from './data/short326';
import {SHORT327} from './data/short327';
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
      {/* EP72 Lac-Megantic. 29:44 with bookends. The bible's first warning binds this film:
          three men were charged with criminal negligence and a jury acquitted all three in
          January 2018, so nothing in the cut may read as an accusation against the engineer. */}
      <Composition
        id="Ep72Lacmegantic"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(lacmeganticFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: lacmeganticFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'Seven Hand Brakes Held a 10,000-Ton Train. It Needed Seventeen.',
          subtitle: 'Lac-Megantic, 6 July 2013 - eighteen contributing factors, and no one person to blame.',
        }}
      />
      {/* EP73 Winter Storm Uri. 30:02 with bookends. Quarantine: the grid did NOT collapse,
          no single fuel type is blamed, winterization was recommended and not required, and
          246 is the only death figure stated as fact. */}
      <Composition
        id="Ep73Uri"
        component={CaseFilm}
        durationInFrames={caseFilmDurationInFrames(uriFilm as unknown as FilmData, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          data: uriFilm as unknown as FilmData,
          seriesLabel: 'PRIME DOCUMENTARY',
          title: 'Texas Cut Power to Save the Grid. It Cut Off the Gas That Ran the Grid.',
          subtitle: 'Winter Storm Uri: a fix was written down in 2011 and never made a rule.',
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
      <Composition
        id="Ep61Weimer"
        component={WeimerFilm}
        durationInFrames={weimerFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep62Greene"
        component={GreeneFilm}
        durationInFrames={greeneFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep63Correa"
        component={CorreaFilm}
        durationInFrames={correaFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep64Memphis"
        component={MemphisFilm}
        durationInFrames={memphisFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep66Openfields"
        component={OpenfieldsFilm}
        durationInFrames={openfieldsFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep65Marmet"
        component={MarmetFilm}
        durationInFrames={marmetFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep68Pinto"
        component={PintoFilm}
        durationInFrames={pintoFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep69Hyatt"
        component={HyattFilm}
        durationInFrames={hyattFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep70Wronghouse"
        component={WronghouseFilm}
        durationInFrames={wronghouseFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep71Oroville"
        component={OrovilleFilm}
        durationInFrames={orovilleFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep74Itaewon"
        component={ItaewonFilm}
        durationInFrames={itaewonFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep75Lahaina"
        component={LahainaFilm}
        durationInFrames={lahainaFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep76Morandi"
        component={MorandiFilm}
        durationInFrames={morandiFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep81Station"
        component={StationFilm}
        durationInFrames={stationFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep80Concordia"
        component={ConcordiaFilm}
        durationInFrames={concordiaFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep77KeyBridge"
        component={KeyBridgeFilm}
        durationInFrames={keybridgeFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep67Ramirez"
        component={RamirezFilm}
        durationInFrames={ramirezFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep60Surfside"
        component={SurfsideFilm}
        durationInFrames={surfsideFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep59Robosigning"
        component={RobosigningFilm}
        durationInFrames={robosigningFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep58Lejeune"
        component={LejeuneFilm}
        durationInFrames={lejeuneFilmDurationInFrames}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="Ep57Fieldtest"
        component={FieldtestFilm}
        durationInFrames={fieldtestFilmDurationInFrames}
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
      {/* ---- SHORT #82 Miranda (he won at the Supreme Court and went to prison anyway) — EP01 ----
           Second angle on EP01: short01 already took "why police read you your rights". This one
           takes the ACT IV twist short01 never touches. Numbered 82 because short60-81 are
           reserved by SHORTS_SLATE_EP53-56 / EP57-59. */}
      <Composition id="Short-short82-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT82, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT82, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short82-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT82, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT82, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short82" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT82, headline: 'HE WON.\nHE WENT\nTO PRISON.', badge: '5-4', backgroundSrc: 'shorts/short82/short82_04.png'}} />
      {/* ---- SHORT #86 Titan (the letter three dozen professionals signed) — EP16 ---- */}
      <Composition id="Short-short86-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT86, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT86, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short86-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT86, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT86, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short86" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT86, headline: 'THEY WARNED\nHIM IN 2018', badge: '36 SIGNED', backgroundSrc: 'shorts/short86/short86_01.png'}} />
      {/* ---- SHORT #87 Titan (the seam between everyone's rules and no one's) — EP16 ---- */}
      <Composition id="Short-short87-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT87, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT87, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short87-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT87, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT87, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short87" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT87, headline: 'NO RULES\nOUT THERE', badge: 'NO FLAG', backgroundSrc: 'shorts/short87/short87_01.png'}} />
      {/* ---- SHORT #88 — Terry — a frisk is not a search ---- */}
      <Composition id="Short-short88-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT88, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT88, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short88-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT88, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT88, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short88" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT88, headline: 'A FRISK IS NOT\nA SEARCH', badge: 'TERRY', backgroundSrc: 'shorts/short88/short88_01.png'}} />
      {/* ---- SHORT #89 — Terry — the argument that won ---- */}
      <Composition id="Short-short89-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT89, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT89, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short89-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT89, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT89, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short89" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT89, headline: 'IT WAS NEVER\nABOUT YOU', badge: '8–1', backgroundSrc: 'shorts/short89/short89_01.png'}} />
      {/* ---- SHORT #90 — Florence — he was the passenger ---- */}
      <Composition id="Short-short90-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT90, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT90, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short90-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT90, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT90, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short90" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT90, headline: 'HE WASN’T\nEVEN DRIVING', badge: 'STRIP SEARCH', backgroundSrc: 'shorts/short90/short90_01.png'}} />
      {/* ---- SHORT #91 — Florence — scared, petrified, humiliated ---- */}
      <Composition id="Short-short91-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT91, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT91, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short91-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT91, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT91, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short91" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT91, headline: 'SCARED.\nHUMILIATED.', badge: '5–4', backgroundSrc: 'shorts/short91/short91_01.png'}} />
      {/* ---- SHORT #92 — Cooper — the name was never his ---- */}
      <Composition id="Short-short92-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT92, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT92, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short92-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT92, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT92, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short92" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT92, headline: 'THAT WAS NEVER\nHIS NAME', badge: 'UNSOLVED', backgroundSrc: 'shorts/short92/short92_01.png'}} />
      {/* ---- SHORT #93 — Cooper — the door in the tail ---- */}
      <Composition id="Short-short93-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT93, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT93, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short93-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT93, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT93, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short93" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT93, headline: 'HE PICKED THAT\nPLANE', badge: 'A DOOR IN THE TAIL', backgroundSrc: 'shorts/short93/short93_01.png'}} />
      {/* ---- SHORT #94 — Madoff — nobody ran the warnings down ---- */}
      <Composition id="Short-short94-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT94, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT94, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short94-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT94, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT94, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short94" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT94, headline: 'HE DID THE MATH\nIN 2000', badge: 'NOBODY CHECKED', backgroundSrc: 'shorts/short94/short94_01.png'}} />
      {/* ---- SHORT #95 — Madoff — one big lie ---- */}
      <Composition id="Short-short95-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT95, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT95, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short95-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT95, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT95, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short95" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT95, headline: 'HE TOLD HIS\nOWN SONS', badge: 'ONE BIG LIE', backgroundSrc: 'shorts/short95/short95_01.png'}} />
      {/* ---- SHORT #96 — Hinton — the test nobody ran ---- */}
      <Composition id="Short-short96-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT96, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT96, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short96-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT96, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT96, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short96" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT96, headline: 'NOBODY TESTED\nTHE BULLETS', badge: '30 YEARS', backgroundSrc: 'shorts/short96/short96_01.png'}} />
      {/* ---- SHORT #97 — Hinton — never solved ---- */}
      <Composition id="Short-short97-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT97, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT97, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short97-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT97, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT97, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short97" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT97, headline: 'HE WALKED OUT\nIN 2015', badge: 'STILL UNSOLVED', backgroundSrc: 'shorts/short97/short97_01.png'}} />
      {/* ---- SHORT #98 — Lange — not never, just not automatically ---- */}
      <Composition id="Short-short98-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT98, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT98, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short98-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT98, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT98, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short98" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT98, headline: 'THERE IS NO\nAUTOMATIC YES', badge: 'LANGE', backgroundSrc: 'shorts/short98/short98_01.png'}} />
      {/* ---- SHORT #99 — Lange — the baseline nobody states ---- */}
      <Composition id="Short-short99-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT99, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT99, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short99-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT99, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT99, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short99" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT99, headline: 'YOUR DOOR\nSTAYS SHUT', badge: 'BASELINE', backgroundSrc: 'shorts/short99/short99_01.png'}} />
      {/* ---- SHORT #100 ---- */}
      <Composition id="Short-short100-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT100, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT100, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short100-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT100, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT100, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short100" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT100, headline: '14 YEARS ON\nDEATH ROW', badge: '5–4', backgroundSrc: 'shorts/short100/short100_01.png'}} />
      {/* ---- SHORT #101 ---- */}
      <Composition id="Short-short101-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT101, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT101, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short101-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT101, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT101, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short101" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT101, headline: 'THE LAB RESULT\nTHEY BURIED', badge: 'TYPE B', backgroundSrc: 'shorts/short101/short101_01.png'}} />
      {/* ---- SHORT #102 ---- */}
      <Composition id="Short-short102-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT102, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT102, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short102-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT102, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT102, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short102" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT102, headline: 'NO WARRANT.\nNO CRIME.', badge: 'GUNS TAKEN', backgroundSrc: 'shorts/short102/short102_01.png'}} />
      {/* ---- SHORT #103 ---- */}
      <Composition id="Short-short103-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT103, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT103, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short103-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT103, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT103, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short103" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT103, headline: 'A HOUSE IS NOT\nA CAR', badge: '9–0', backgroundSrc: 'shorts/short103/short103_01.png'}} />
      {/* ---- SHORT #104 ---- */}
      <Composition id="Short-short104-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT104, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT104, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short104-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT104, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT104, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short104" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT104, headline: 'THE WARNING\nWAS DELETED', badge: 'ONECOIN', backgroundSrc: 'shorts/short104/short104_01.png'}} />
      {/* ---- SHORT #105 ---- */}
      <Composition id="Short-short105-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT105, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT105, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short105-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT105, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT105, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short105" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT105, headline: 'THE COIN\nNEVER EXISTED', badge: '$4 BILLION', backgroundSrc: 'shorts/short105/short105_01.png'}} />
      {/* ---- SHORT #106 ---- */}
      <Composition id="Short-short106-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT106, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT106, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short106-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT106, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT106, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short106" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT106, headline: 'SHE WAS SURE.\nSHE WAS WRONG.', badge: '11 YEARS', backgroundSrc: 'shorts/short106/short106_01.png'}} />
      {/* ---- SHORT #107 ---- */}
      <Composition id="Short-short107-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT107, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT107, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short107-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT107, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT107, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short107" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT107, headline: 'CERTAINTY WAS\nTHE PROBLEM', badge: 'MEMORY', backgroundSrc: 'shorts/short107/short107_01.png'}} />
      {/* ---- SHORT #108 ---- */}
      <Composition id="Short-short108-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT108, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT108, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short108-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT108, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT108, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short108" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT108, headline: 'THE BILL THAT\nALMOST PASSED', badge: 'SOPA', backgroundSrc: 'shorts/short108/short108_01.png'}} />
      {/* ---- SHORT #109 ---- */}
      <Composition id="Short-short109-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT109, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT109, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short109-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT109, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT109, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short109" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT109, headline: 'NO LOCK\nWAS BROKEN', badge: '4.8M FILES', backgroundSrc: 'shorts/short109/short109_01.png'}} />
      {/* ---- SHORT #110 ---- */}
      <Composition id="Short-short110-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT110, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT110, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short110-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT110, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT110, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short110" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT110, headline: 'HE WAS NEVER\nTOLD', badge: '5–4', backgroundSrc: 'shorts/short110/short110_01.png'}} />
      {/* ---- SHORT #111 ---- */}
      <Composition id="Short-short111-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT111, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT111, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short111-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT111, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT111, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short111" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT111, headline: 'A RIGHT WITH NO\nREMEDY', badge: 'MAPP', backgroundSrc: 'shorts/short111/short111_01.png'}} />
      {/* ---- SHORT #112 ---- */}
      <Composition id="Short-short112-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT112, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT112, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short112-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT112, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT112, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short112" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT112, headline: 'GET A\nWARRANT', badge: '9–0', backgroundSrc: 'shorts/short112/short112_01.png'}} />
      {/* ---- SHORT #113 ---- */}
      <Composition id="Short-short113-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT113, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT113, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short113-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT113, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT113, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short113" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT113, headline: 'YOUR PHONE KEPT\nTHE RECORD', badge: '127 DAYS', backgroundSrc: 'shorts/short113/short113_01.png'}} />
      {/* ---- SHORT #114 ---- */}
      <Composition id="Short-short114-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT114, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT114, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short114-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT114, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT114, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short114" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT114, headline: 'A BLURRY LINE,\nRIGHTLY DRAWN', badge: '5–4', backgroundSrc: 'shorts/short114/short114_01.png'}} />
      {/* ---- SHORT #115 ---- */}
      <Composition id="Short-short115-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT115, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT115, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short115-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT115, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT115, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short115" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT115, headline: 'A $42,000 CAR\nFOR $385', badge: '9–0', backgroundSrc: 'shorts/short115/short115_01.png'}} />
      {/* ---- SHORT #116 ---- */}
      <Composition id="Short-short116-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT116, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT116, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short116-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT116, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT116, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short116" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT116, headline: 'THE CLAUSE THAT\nDIDN’T APPLY', badge: 'UNTIL 2019', backgroundSrc: 'shorts/short116/short116_01.png'}} />
      {/* ---- SHORT #117 ---- */}
      <Composition id="Short-short117-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT117, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT117, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short117-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT117, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT117, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short117" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT117, headline: 'HER HOME FOR A\nDEVELOPER', badge: '5–4', backgroundSrc: 'shorts/short117/short117_01.png'}} />
      {/* ---- SHORT #118 ---- */}
      <Composition id="Short-short118-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT118, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT118, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short118-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT118, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT118, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short118" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT118, headline: 'THEY BULLDOZED\nIT FOR NOTHING', badge: 'STILL EMPTY', backgroundSrc: 'shorts/short118/short118_01.png'}} />
      {/* ---- SHORT #119 ---- */}
      <Composition id="Short-short119-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT119, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT119, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short119-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT119, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT119, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short119" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT119, headline: 'ONE POST.\nONE YEAR OUT.', badge: '8–1', backgroundSrc: 'shorts/short119/short119_01.png'}} />
      {/* ---- SHORT #120 ---- */}
      <Composition id="Short-short120-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT120, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT120, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short120-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT120, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT120, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short120" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT120, headline: 'SCHOOL STOPS AT\nTHE GATE', badge: 'MAHANOY', backgroundSrc: 'shorts/short120/short120_01.png'}} />
      {/* ---- SHORT #132 ---- */}
      <Composition id="Short-short132-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT132, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT132, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short132-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT132, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT132, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short132" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT132, headline: 'THE RULE HAS\nAN EXPIRY DATE', badge: 'KYLLO', backgroundSrc: 'shorts/short132/short132_01.png'}} />
      {/* ---- SHORT #133 ---- */}
      <Composition id="Short-short133-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT133, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT133, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short133-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT133, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT133, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short133" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT133, headline: 'IT NEVER BANNED\nTHE SCAN', badge: 'NARROW', backgroundSrc: 'shorts/short133/short133_01.png'}} />
      {/* ---- SHORT #134 ---- */}
      <Composition id="Short-short134-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT134, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT134, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short134-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT134, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT134, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short134" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT134, headline: 'HE SAID YOU\nCANNOT SEIZE IT', badge: '1 DISSENT', backgroundSrc: 'shorts/short134/short134_01.png'}} />
      {/* ---- SHORT #121 ---- */}
      <Composition id="Short-short121-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT121, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT121, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short121-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT121, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT121, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short121" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT121, headline: 'ONE AT A TIME\nMEANS NO ONE', badge: '5–4', backgroundSrc: 'shorts/short121/short121_01.png'}} />
      {/* ---- SHORT #122 ---- */}
      <Composition id="Short-short122-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT122, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT122, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short122-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT122, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT122, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short122" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT122, headline: 'YOU NEVER\nSIGNED IT', badge: 'FINE PRINT', backgroundSrc: 'shorts/short122/short122_01.png'}} />
      {/* ---- SHORT #130 ---- */}
      <Composition id="Short-short130-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT130, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT130, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short130-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT130, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT130, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short130" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT130, headline: 'ONE WORD DID\nALL THE WORK', badge: '‘IDENTIFICATION’', backgroundSrc: 'shorts/short130/short130_01.png'}} />
      {/* ---- SHORT #131 ---- */}
      <Composition id="Short-short131-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT131, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT131, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short131-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT131, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT131, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short131" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT131, headline: 'A PATTERN\nOR A BLUEPRINT', badge: 'DNA AT ARREST', backgroundSrc: 'shorts/short131/short131_01.png'}} />
      {/* ---- SHORT #135 ---- */}
      <Composition id="Short-short135-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT135, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT135, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short135-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT135, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT135, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short135" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT135, headline: 'PLACES, OR\nPEOPLE', badge: 'KATZ', backgroundSrc: 'shorts/short135/short135_01.png'}} />
      {/* ---- SHORT #136 ---- */}
      <Composition id="Short-short136-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT136, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT136, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short136-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT136, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT136, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short136" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT136, headline: 'THE STOP WAS\nALREADY OVER', badge: '9–0', backgroundSrc: 'shorts/short136/short136_01.png'}} />
      {/* ---- SHORT #137 ---- */}
      <Composition id="Short-short137-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT137, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT137, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short137-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT137, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT137, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short137" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT137, headline: 'THEN THE DOG\nARRIVED', badge: '7 MINUTES', backgroundSrc: 'shorts/short137/short137_01.png'}} />
      {/* ---- SHORT #138 ---- */}
      <Composition id="Short-short138-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT138, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT138, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short138-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT138, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT138, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short138" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT138, headline: 'AT THE BORDER,\nA DIFFERENT RULE', badge: 'YOUR PHONE', backgroundSrc: 'shorts/short138/short138_01.png'}} />
      {/* ---- SHORT #139 ---- */}
      <Composition id="Short-short139-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT139, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT139, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short139-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT139, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT139, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short139" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT139, headline: 'YOUR THUMB.\nNOT YOUR MIND.', badge: 'SPLIT', backgroundSrc: 'shorts/short139/short139_01.png'}} />
      {/* ---- SHORT #140 ---- */}
      <Composition id="Short-short140-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT140, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT140, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short140-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT140, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT140, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short140" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT140, headline: 'NO WARNING.\nNO LAWSUIT.', badge: '6–3', backgroundSrc: 'shorts/short140/short140_01.png'}} />
      {/* ---- SHORT #141 ---- */}
      <Composition id="Short-short141-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT141, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT141, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short141-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT141, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT141, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short141" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT141, headline: 'A RIGHT WITH\nNO DOOR', badge: 'DISSENT', backgroundSrc: 'shorts/short141/short141_01.png'}} />
      {/* ---- SHORT #142 ---- */}
      <Composition id="Short-short142-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT142, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT142, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short142-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT142, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT142, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short142" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT142, headline: 'HE NEVER SAW\nTHE DRIVER', badge: '8–1', backgroundSrc: 'shorts/short142/short142_01.png'}} />
      {/* ---- SHORT #143 ---- */}
      <Composition id="Short-short143-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT143, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT143, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short143-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT143, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT143, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short143" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT143, headline: 'A NAME ON\nA PLATE', badge: 'REVOKED', backgroundSrc: 'shorts/short143/short143_01.png'}} />
      {/* ---- SHORT #144 ---- */}
      <Composition id="Short-short144-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT144, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT144, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short144-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT144, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT144, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short144" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT144, headline: 'THE STOP WAS\nILLEGAL', badge: 'EVIDENCE KEPT', backgroundSrc: 'shorts/short144/short144_01.png'}} />
      {/* ---- SHORT #145 ---- */}
      <Composition id="Short-short145-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT145, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT145, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short145-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT145, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT145, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short145" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT145, headline: 'A WARRANT\nERASED IT', badge: 'DISSENT', backgroundSrc: 'shorts/short145/short145_01.png'}} />
      {/* ---- SHORT #150 ---- */}
      <Composition id="Short-short150-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT150, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT150, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short150-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT150, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT150, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short150" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT150, headline: 'HE WROTE IN\nPENCIL', badge: '9–0', backgroundSrc: 'shorts/short150/short150_01.png'}} />
      {/* ---- SHORT #151 ---- */}
      <Composition id="Short-short151-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT151, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT151, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short151-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT151, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT151, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short151" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT151, headline: 'A LAWYER IS NOT\nA LUXURY', badge: 'GIDEON', backgroundSrc: 'shorts/short151/short151_01.png'}} />
      {/* ---- SHORT #152 ---- */}
      <Composition id="Short-short152-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT152, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT152, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short152-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT152, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT152, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short152" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT152, headline: 'THE WITHDRAWAL\nNEVER CAME', badge: 'FTX', backgroundSrc: 'shorts/short152/short152_01.png'}} />
      {/* ---- SHORT #153 ---- */}
      <Composition id="Short-short153-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT153, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT153, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short153-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT153, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT153, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short153" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT153, headline: 'THE BALANCE\nWAS A NUMBER', badge: '$8 BILLION', backgroundSrc: 'shorts/short153/short153_01.png'}} />
      {/* ---- SHORT #154 ---- */}
      <Composition id="Short-short154-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT154, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT154, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short154-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT154, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT154, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short154" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT154, headline: 'THE TEST NEVER\nWORKED', badge: 'THERANOS', backgroundSrc: 'shorts/short154/short154_01.png'}} />
      {/* ---- SHORT #155 ---- */}
      <Composition id="Short-short155-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT155, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT155, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short155-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT155, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT155, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short155" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT155, headline: 'ONE DROP\nOF BLOOD', badge: 'A PROMISE', backgroundSrc: 'shorts/short155/short155_01.png'}} />
      {/* ---- SHORT #156 ---- */}
      <Composition id="Short-short156-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT156, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT156, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short156-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT156, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT156, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short156" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT156, headline: '36 MINUTES.\n$1 TRILLION.', badge: 'FLASH CRASH', backgroundSrc: 'shorts/short156/short156_01.png'}} />
      {/* ---- SHORT #157 ---- */}
      <Composition id="Short-short157-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT157, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT157, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short157-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT157, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT157, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short157" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT157, headline: 'HE TRADED FROM\nHIS BEDROOM', badge: 'SARAO', backgroundSrc: 'shorts/short157/short157_01.png'}} />
      {/* ---- SHORT #158 ---- */}
      <Composition id="Short-short158-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT158, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT158, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short158-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT158, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT158, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short158" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT158, headline: 'THEY WROTE IT\nOFF ON TAX', badge: '$10M BACK', backgroundSrc: 'shorts/short158/short158_01.png'}} />
      {/* ---- SHORT #159 ---- */}
      <Composition id="Short-short159-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT159, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT159, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short159-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT159, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT159, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short159" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT159, headline: 'SOMEBODY GOT\nTHE THIN LETTER', badge: 'SIDE DOOR', backgroundSrc: 'shorts/short159/short159_01.png'}} />
      {/* ---- SHORT #160 ---- */}
      <Composition id="Short-short160-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT160, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT160, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short160-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT160, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT160, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short160" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT160, headline: 'NONE OF IT\nCAN BE SOLD', badge: 'STILL MISSING', backgroundSrc: 'shorts/short160/short160_01.png'}} />
      {/* ---- SHORT #161 ---- */}
      <Composition id="Short-short161-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT161, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT161, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short161-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT161, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT161, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short161" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT161, headline: 'PSYCHICS.\nBILLBOARDS.', badge: '35 YEARS', backgroundSrc: 'shorts/short161/short161_01.png'}} />
      {/* ---- SHORT #162 ---- */}
      <Composition id="Short-short162-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT162, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT162, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short162-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT162, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT162, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short162" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT162, headline: 'A LETTER THAT\nMOVED BILLIONS', badge: 'MILKEN', backgroundSrc: 'shorts/short162/short162_01.png'}} />
      {/* ---- SHORT #163 ---- */}
      <Composition id="Short-short163-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT163, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT163, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short163-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT163, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT163, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short163" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT163, headline: 'THE ROAD RAN\nTHROUGH ONE MAN', badge: 'JUNK BONDS', backgroundSrc: 'shorts/short163/short163_01.png'}} />
      {/* ---- SHORT #164 ---- */}
      <Composition id="Short-short164-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT164, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT164, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short164-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT164, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT164, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short164" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT164, headline: 'THE CALL WAS\nBEING RECORDED', badge: 'WIRETAP', backgroundSrc: 'shorts/short164/short164_01.png'}} />
      {/* ---- SHORT #165 ---- */}
      <Composition id="Short-short165-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT165, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT165, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short165-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT165, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT165, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short165" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT165, headline: 'YOUR PENSION\nWAS ON THE OTHER SIDE', badge: 'INSIDER', backgroundSrc: 'shorts/short165/short165_01.png'}} />
      {/* ---- SHORT #170 ---- */}
      <Composition id="Short-short170-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT170, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT170, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short170-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT170, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT170, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short170" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT170, headline: 'COURTROOM 478\nHAD NO JURY', badge: 'FORFEITURE', backgroundSrc: 'shorts/short170/short170_01.png'}} />
      {/* ---- SHORT #171 ---- */}
      <Composition id="Short-short171-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT171, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT171, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short171-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT171, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT171, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short171" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT171, headline: 'THEY PAINTED\nHOUSES', badge: 'NO CONVICTION', backgroundSrc: 'shorts/short171/short171_01.png'}} />
      {/* ---- SHORT #172 ---- */}
      <Composition id="Short-short172-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT172, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT172, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short172-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT172, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT172, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short172" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT172, headline: 'YOUR FACE IS A\nPASSWORD', badge: 'YOU CAN’T CHANGE', backgroundSrc: 'shorts/short172/short172_01.png'}} />
      {/* ---- SHORT #173 ---- */}
      <Composition id="Short-short173-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT173, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT173, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short173-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT173, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT173, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short173" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT173, headline: 'ONE RULE.\nONE CITY.', badge: 'SETTLEMENT', backgroundSrc: 'shorts/short173/short173_01.png'}} />
      {/* ---- SHORT #174 ---- */}
      <Composition id="Short-short174-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT174, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT174, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short174-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT174, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT174, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short174" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT174, headline: 'A FEW THOUSAND\nDOLLARS A HEAD', badge: 'KIDS FOR CASH', backgroundSrc: 'shorts/short174/short174_01.png'}} />
      {/* ---- SHORT #175 ---- */}
      <Composition id="Short-short175-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT175, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT175, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short175-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT175, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT175, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short175" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT175, headline: 'POLICE ARE\nALLOWED TO LIE', badge: 'FRAZIER', backgroundSrc: 'shorts/short175/short175_01.png'}} />
      {/* ---- SHORT #176 ---- */}
      <Composition id="Short-short176-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT176, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT176, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short176-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT176, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT176, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short176" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT176, headline: 'A CHILD IS NOT\nAN ADULT', badge: '4,102 YEARS', backgroundSrc: 'shorts/short176/short176_01.png'}} />
      {/* ---- SHORT #177 ---- */}
      <Composition id="Short-short177-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT177, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT177, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short177-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT177, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT177, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short177" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT177, headline: 'THEY WRECKED IT.\nTHEY OWED NOTHING.', badge: 'LECH', backgroundSrc: 'shorts/short177/short177_01.png'}} />
      {/* ---- SHORT #178 ---- */}
      <Composition id="Short-short178-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT178, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT178, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short178-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT178, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT178, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short178" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT178, headline: 'THE STATEMENT\nCARRIED NO WEIGHT', badge: 'SPLIT', backgroundSrc: 'shorts/short178/short178_01.png'}} />
      {/* ---- SHORT #179 ---- */}
      <Composition id="Short-short179-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT179, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT179, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short179-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT179, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT179, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short179" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT179, headline: 'THE REASONS HAD\nONLY FOUR VOTES', badge: 'HUDSON', backgroundSrc: 'shorts/short179/short179_01.png'}} />
      {/* ---- SHORT #180 ---- */}
      <Composition id="Short-short180-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT180, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT180, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short180-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT180, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT180, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short180" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT180, headline: 'RUIN AS\nREVENUE', badge: 'FINES & FEES', backgroundSrc: 'shorts/short180/short180_01.png'}} />
      {/* ---- SHORT #181 ---- */}
      <Composition id="Short-short181-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT181, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT181, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short181-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT181, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT181, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short181" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT181, headline: 'TOO POOR\nTO PAY', badge: 'BEARDEN', backgroundSrc: 'shorts/short181/short181_01.png'}} />
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
          {/* ---- SHORT #182 ---- */}
      <Composition id="Short-short182-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT182, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT182, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short182-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT182, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT182, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short182" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT182, headline: 'HOW FAR\nIS TOO FAR', badge: 'TLO', backgroundSrc: 'shorts/short182/short182_01.png'}} />
      {/* ---- SHORT #183 ---- */}
      <Composition id="Short-short183-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT183, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT183, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short183-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT183, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT183, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short183" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT183, headline: 'THREE JUSTICES\nSAID NO', badge: 'TLO', backgroundSrc: 'shorts/short183/short183_01.png'}} />
      {/* ---- SHORT #184 ---- */}
      <Composition id="Short-short184-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT184, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT184, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short184-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT184, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT184, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short184" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT184, headline: 'AN HOUR\nIN A CELL', badge: 'ATWATER', backgroundSrc: 'shorts/short184/short184_01.png'}} />
      {/* ---- SHORT #185 ---- */}
      <Composition id="Short-short185-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT185, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT185, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short185-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT185, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT185, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short185" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT185, headline: 'ADMINISTRATIVE\nEASE', badge: 'ATWATER', backgroundSrc: 'shorts/short185/short185_01.png'}} />
      {/* ---- SHORT #186 ---- */}
      <Composition id="Short-short186-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT186, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT186, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short186-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT186, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT186, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short186" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT186, headline: 'FLASHOVER', badge: 'WILLINGHAM', backgroundSrc: 'shorts/short186/short186_01.png'}} />
      {/* ---- SHORT #187 ---- */}
      <Composition id="Short-short187-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT187, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT187, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short187-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT187, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT187, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short187" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT187, headline: 'MYSTICS\nOR PSYCHICS', badge: 'WILLINGHAM', backgroundSrc: 'shorts/short187/short187_01.png'}} />
      {/* ---- SHORT #188 ---- */}
      <Composition id="Short-short188-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT188, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT188, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short188-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT188, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT188, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short188" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT188, headline: 'JUNK\nSCIENCE', badge: 'MORTON', backgroundSrc: 'shorts/short188/short188_01.png'}} />
      {/* ---- SHORT #189 ---- */}
      <Composition id="Short-short189-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT189, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT189, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short189-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT189, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT189, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short189" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT189, headline: 'ONE TEST\nALMOST FREE', badge: 'MORTON', backgroundSrc: 'shorts/short189/short189_01.png'}} />
      {/* ---- SHORT #190 ---- */}
      <Composition id="Short-short190-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT190, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT190, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short190-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT190, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT190, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short190" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT190, headline: 'A CAR\nCAN DRIVE OFF', badge: 'CARSEARCH', backgroundSrc: 'shorts/short190/short190_01.png'}} />
      {/* ---- SHORT #191 ---- */}
      <Composition id="Short-short191-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT191, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT191, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short191-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT191, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT191, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short191" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT191, headline: 'THE SMELL\nWAS ENOUGH', badge: 'CARSEARCH', backgroundSrc: 'shorts/short191/short191_01.png'}} />
      {/* ---- SHORT #192 ---- */}
      <Composition id="Short-short192-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT192, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT192, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short192-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT192, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT192, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short192" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT192, headline: '1215\nEVEN THE KING', badge: 'TYLER', backgroundSrc: 'shorts/short192/short192_01.png'}} />
      {/* ---- SHORT #193 ---- */}
      <Composition id="Short-short193-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT193, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT193, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short193-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT193, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT193, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short193" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT193, headline: '$2,300 BECAME\n$15,000', badge: 'TYLER', backgroundSrc: 'shorts/short193/short193_01.png'}} />
      {/* ---- SHORT #194 ---- */}
      <Composition id="Short-short194-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT194, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT194, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short194-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT194, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT194, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short194" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT194, headline: 'MORE LIKELY\nTHAN NOT', badge: 'ROLIN', backgroundSrc: 'shorts/short194/short194_01.png'}} />
      {/* ---- SHORT #195 ---- */}
      <Composition id="Short-short195-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT195, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT195, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short195-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT195, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT195, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short195" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT195, headline: '$209 MILLION\n5,000 TRAVELERS', badge: 'ROLIN', backgroundSrc: 'shorts/short195/short195_01.png'}} />
      {/* ---- SHORT #196 ---- */}
      <Composition id="Short-short196-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT196, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT196, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short196-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT196, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT196, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short196" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT196, headline: '$107,702\n301 DEPOSITS', badge: 'HINDERS', backgroundSrc: 'shorts/short196/short196_01.png'}} />
      {/* ---- SHORT #197 ---- */}
      <Composition id="Short-short197-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT197, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT197, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short197-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT197, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT197, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short197" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT197, headline: '9 IN 10\nNO CRIME', badge: 'HINDERS', backgroundSrc: 'shorts/short197/short197_01.png'}} />
      {/* ---- SHORT #200 ---- */}
      <Composition id="Short-short200-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT200, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT200, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short200-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT200, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT200, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short200" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT200, headline: 'ALL SEVEN\nEXCLUDED', badge: 'NORFOLK', backgroundSrc: 'shorts/short200/short200_01.png'}} />
      {/* ---- SHORT #201 ---- */}
      <Composition id="Short-short201-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT201, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT201, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short201-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT201, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT201, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short201" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT201, headline: '6,700 JURORS\n225 TRIALS', badge: 'FLOWERS', backgroundSrc: 'shorts/short201/short201_01.png'}} />
      {/* ---- SHORT #202 ---- */}
      <Composition id="Short-short202-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT202, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT202, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short202-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT202, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT202, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short202" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT202, headline: '148 CLAIMS\nHALF BELIEVED', badge: 'BURGE', backgroundSrc: 'shorts/short202/short202_01.png'}} />
      {/* ---- SHORT #203 ---- */}
      <Composition id="Short-short203-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT203, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT203, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short203-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT203, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT203, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short203" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT203, headline: 'THE LIE\nTHAT HELD IT UP', badge: 'POSTOFFICE', backgroundSrc: 'shorts/short203/short203_01.png'}} />
      {/* ---- SHORT #204 ---- */}
      <Composition id="Short-short204-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT204, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT204, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short204-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT204, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT204, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short204" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT204, headline: 'ABOUT ONE\nEVERY WEEK', badge: 'POSTOFFICE', backgroundSrc: 'shorts/short204/short204_01.png'}} />
      {/* ---- SHORT #205 ---- */}
      <Composition id="Short-short205-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT205, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT205, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short205-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT205, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT205, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short205" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT205, headline: 'PREGNANT\nAND IMPRISONED', badge: 'POSTOFFICE', backgroundSrc: 'shorts/short205/short205_01.png'}} />
      {/* ---- SHORT #250 ---- */}
      <Composition id="Short-short250-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT250, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT250, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short250-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT250, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT250, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short250" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT250, headline: '80+ COMPOUNDS\nTURN IT BLUE', badge: 'FIELDTEST', backgroundSrc: 'shorts/short250/short250_01.png'}} />
      {/* ---- SHORT #251 ---- */}
      <Composition id="Short-short251-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT251, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT251, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short251-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT251, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT251, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short251" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT251, headline: '58%\nPLEADED GUILTY', badge: 'FIELDTEST', backgroundSrc: 'shorts/short251/short251_01.png'}} />
      {/* ---- SHORT #252 ---- */}
      <Composition id="Short-short252-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT252, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT252, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short252-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT252, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT252, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short252" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT252, headline: '251 CASES\nNO DRUGS', badge: 'FIELDTEST', backgroundSrc: 'shorts/short252/short252_01.png'}} />
      {/* ---- SHORT #253 ---- */}
      <Composition id="Short-short253-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT253, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT253, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short253-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT253, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT253, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short253" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT253, headline: 'NOTHING\nHAPPENED', badge: 'LEJEUNE', backgroundSrc: 'shorts/short253/short253_01.png'}} />
      {/* ---- SHORT #254 ---- */}
      <Composition id="Short-short254-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT254, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT254, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short254-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT254, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT254, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short254" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT254, headline: 'NO LAWYER\nNO SCIENTIST', badge: 'LEJEUNE', backgroundSrc: 'shorts/short254/short254_01.png'}} />
      {/* ---- SHORT #255 ---- */}
      <Composition id="Short-short255-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT255, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT255, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short255-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT255, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT255, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short255" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT255, headline: 'FIFTY-FIFTY\nIS ENOUGH', badge: 'LEJEUNE', backgroundSrc: 'shorts/short255/short255_01.png'}} />
      {/* ---- SHORT #256 ---- */}
      <Composition id="Short-short256-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT256, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT256, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short256-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT256, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT256, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short256" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT256, headline: 'NOBODY\nCALLED BACK', badge: 'ROBOSIGNING', backgroundSrc: 'shorts/short256/short256_01.png'}} />
      {/* ---- SHORT #257 ---- */}
      <Composition id="Short-short257-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT257, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT257, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short257-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT257, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT257, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short257" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT257, headline: '10,000\nA MONTH', badge: 'ROBOSIGNING', backgroundSrc: 'shorts/short257/short257_01.png'}} />
      {/* ---- SHORT #258 ---- */}
      <Composition id="Short-short258-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT258, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT258, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short258-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT258, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT258, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short258" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT258, headline: '$10 AN HOUR\n350 SIGNATURES', badge: 'ROBOSIGNING', backgroundSrc: 'shorts/short258/short258_01.png'}} />
      {/* ---- SHORT #259 ---- */}
      <Composition id="Short-short259-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT259, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT259, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short259-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT259, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT259, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short259" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT259, headline: 'UNDER OATH', badge: 'GREENE', backgroundSrc: 'shorts/short259/short259_01.png'}} />
      {/* ---- SHORT #260 ---- */}
      <Composition id="Short-short260-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT260, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT260, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short260-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT260, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT260, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short260" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT260, headline: 'ONE ATTEMPT', badge: 'GREENE', backgroundSrc: 'shorts/short260/short260_01.png'}} />
      {/* ---- SHORT #261 ---- */}
      <Composition id="Short-short261-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT261, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT261, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short261-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT261, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT261, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short261" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT261, headline: 'AT LEAST 11\nSTATES', badge: 'GREENE', backgroundSrc: 'shorts/short261/short261_01.png'}} />
      {/* ---- SHORT #262 ---- */}
      <Composition id="Short-short262-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT262, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT262, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short262-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT262, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT262, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short262" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT262, headline: 'AGE 65', badge: 'CORREA', backgroundSrc: 'shorts/short262/short262_01.png'}} />
      {/* ---- SHORT #263 ---- */}
      <Composition id="Short-short263-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT263, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT263, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short263-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT263, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT263, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short263" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT263, headline: 'EVEN-HANDEDLY', badge: 'CORREA', backgroundSrc: 'shorts/short263/short263_01.png'}} />
      {/* ---- SHORT #264 ---- */}
      <Composition id="Short-short264-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT264, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT264, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short264-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT264, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT264, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short264" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT264, headline: '$200,000', badge: 'CORREA', backgroundSrc: 'shorts/short264/short264_01.png'}} />
      {/* ---- SHORT #265 ---- */}
      <Composition id="Short-short265-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT265, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT265, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short265-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT265, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT265, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short265" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT265, headline: 'FIVE TIMES', badge: 'MEMPHIS', backgroundSrc: 'shorts/short265/short265_01.png'}} />
      {/* ---- SHORT #266 ---- */}
      <Composition id="Short-short266-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT266, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT266, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short266-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT266, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT266, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short266" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT266, headline: 'WHERE\nWHAT HOURS\nBEFORE WHOM', badge: 'MEMPHIS', backgroundSrc: 'shorts/short266/short266_01.png'}} />
      {/* ---- SHORT #267 ---- */}
      <Composition id="Short-short267-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT267, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT267, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short267-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT267, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT267, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short267" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT267, headline: 'ABOUT 2,000 A\nMONTH', badge: 'MEMPHIS', backgroundSrc: 'shorts/short267/short267_01.png'}} />
      {/* ---- SHORT #268 ---- */}
      <Composition id="Short-short268-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT268, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT268, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short268-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT268, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT268, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short268" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT268, headline: 'ONE EXCEPTION', badge: 'MARMET', backgroundSrc: 'shorts/short268/short268_01.png'}} />
      {/* ---- SHORT #269 ---- */}
      <Composition id="Short-short269-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT269, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT269, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short269-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT269, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT269, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short269" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT269, headline: 'ONE POINT\nOVERRULED', badge: 'MARMET', backgroundSrc: 'shorts/short269/short269_01.png'}} />
      {/* ---- SHORT #270 ---- */}
      <Composition id="Short-short270-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT270, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT270, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short270-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT270, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT270, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short270" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT270, headline: 'PER CURIAM', badge: 'MARMET', backgroundSrc: 'shorts/short270/short270_01.png'}} />
      {/* ---- SHORT #271 ---- */}
      <Composition id="Short-short271-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT271, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT271, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short271-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT271, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT271, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short271" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT271, headline: 'THEY CUT\nA BRANCH', badge: '93 ACRES', backgroundSrc: 'shorts/short271/short271_01.png'}} />
      {/* ---- SHORT #272 ---- */}
      <Composition id="Short-short272-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT272, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT272, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short272-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT272, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT272, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short272" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT272, headline: 'ONE EXTRA\nNOUN', badge: '3 TIMES', backgroundSrc: 'shorts/short272/short272_01.png'}} />
      {/* ---- SHORT #273 ---- */}
      <Composition id="Short-short273-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT273, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT273, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short273-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT273, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT273, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short273" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT273, headline: 'LAWFUL, AND\nUNLAWFUL', badge: '3-0', backgroundSrc: 'shorts/short273/short273_01.png'}} />
      {/* ---- SHORT #274 ---- */}
      <Composition id="Short-short274-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT274, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT274, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short274-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT274, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT274, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short274" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT274, headline: 'ON A\nTERRORIST LIST', badge: '2011', backgroundSrc: 'shorts/short274/short274_01.png'}} />
      {/* ---- SHORT #275 ---- */}
      <Composition id="Short-short275-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT275, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT275, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short275-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT275, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT275, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short275" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT275, headline: 'NAME\nONLY', badge: '27 YEARS', backgroundSrc: 'shorts/short275/short275_01.png'}} />
      {/* ---- SHORT #276 ---- */}
      <Composition id="Short-short276-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT276, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT276, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short276-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT276, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT276, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short276" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT276, headline: 'NO HARM,\nNO COURT', badge: '5-4', backgroundSrc: 'shorts/short276/short276_01.png'}} />
      {/* ---- SHORT #277 ---- */}
      <Composition id="Short-short277-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT277, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT277, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short277-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT277, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT277, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short277" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT277, headline: 'IT COUNTS\nTHE DEAD', badge: '1973', backgroundSrc: 'shorts/short277/short277_01.png'}} />
      {/* ---- SHORT #278 ---- */}
      <Composition id="Short-short278-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT278, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT278, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short278-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT278, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT278, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short278" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT278, headline: 'NOT THE\nFUEL TANK', badge: '1972', backgroundSrc: 'shorts/short278/short278_01.png'}} />
      {/* ---- SHORT #279 ---- */}
      <Composition id="Short-short279-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT279, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT279, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short279-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT279, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT279, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short279" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT279, headline: 'THE COMPANY\nINDICTED', badge: '$36,000', backgroundSrc: 'shorts/short279/short279_01.png'}} />
      {/* ---- SHORT #280 ---- */}
      <Composition id="Short-short280-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT280, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT280, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short280-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT280, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT280, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short280" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT280, headline: 'ONE ROD\nBECAME TWO', badge: '4 INCHES', backgroundSrc: 'shorts/short280/short280_01.png'}} />
      {/* ---- SHORT #281 ---- */}
      <Composition id="Short-short281-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT281, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT281, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short281-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT281, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT281, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short281" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT281, headline: 'LOOK, DO\nNOT TOUCH', badge: 'COURT ORDER', backgroundSrc: 'shorts/short281/short281_01.png'}} />
      {/* ---- SHORT #282 ---- */}
      <Composition id="Short-short282-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT282, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT282, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short282-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT282, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT282, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short282" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT282, headline: 'NOBODY\nCHARGED', badge: '$78M', backgroundSrc: 'shorts/short282/short282_01.png'}} />
      {/* ---- SHORT #289 ---- */}
      <Composition id="Short-short289-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT289, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT289, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short289-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT289, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT289, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short289" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT289, headline: 'NOBODY\nBROKE A RULE', badge: 'FULL CASE', backgroundSrc: 'shorts/short289/short289_01.png'}} />
      {/* ---- SHORT #290 ---- */}
      <Composition id="Short-short290-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT290, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT290, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short290-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT290, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT290, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short290" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT290, headline: 'HIS OWN\nGPS', badge: 'FULL CASE', backgroundSrc: 'shorts/short290/short290_01.png'}} />
      {/* ---- SHORT #291 ---- */}
      <Composition id="Short-short291-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT291, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT291, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short291-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT291, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT291, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short291" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT291, headline: '223 ENTRIES', badge: 'FULL CASE', backgroundSrc: 'shorts/short291/short291_01.png'}} />
      {/* ---- SHORT #292 ---- */}
      <Composition id="Short-short292-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT292, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT292, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short292-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT292, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT292, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short292" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT292, headline: 'NEVER\nA ZONE', badge: 'FULL CASE', backgroundSrc: 'shorts/short292/short292_01.png'}} />
      {/* ---- SHORT #293 ---- */}
      <Composition id="Short-short293-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT293, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT293, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short293-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT293, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT293, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short293" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT293, headline: 'NO DELIVERY\nRECEIPT', badge: 'FULL CASE', backgroundSrc: 'shorts/short293/short293_01.png'}} />
      {/* ---- SHORT #294 ---- */}
      <Composition id="Short-short294-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT294, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT294, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short294-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT294, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT294, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short294" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT294, headline: 'EXPENSES,\nTWO DAYS', badge: 'FULL CASE', backgroundSrc: 'shorts/short294/short294_01.png'}} />
      {/* ---- SHORT #295 ---- */}
      <Composition id="Short-short295-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT295, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT295, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short295-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT295, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT295, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short295" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT295, headline: 'ELEVEN\nREPORTS', badge: 'FULL CASE', backgroundSrc: 'shorts/short295/short295_01.png'}} />
      {/* ---- SHORT #296 ---- */}
      <Composition id="Short-short296-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT296, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT296, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short296-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT296, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT296, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short296" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT296, headline: 'NINE PEOPLE\nON A DOORMAT', badge: 'FULL CASE', backgroundSrc: 'shorts/short296/short296_01.png'}} />
      {/* ---- SHORT #297 ---- */}
      <Composition id="Short-short297-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT297, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT297, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short297-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT297, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT297, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short297" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT297, headline: 'NOT\nINSUFFICIENT EVIDENCE', badge: 'FULL CASE', backgroundSrc: 'shorts/short297/short297_01.png'}} />
      {/* ---- SHORT #298 ---- */}
      <Composition id="Short-short298-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT298, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT298, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short298-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT298, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT298, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short298" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT298, headline: 'ONE\nOPERABLE', badge: 'FULL CASE', backgroundSrc: 'shorts/short298/short298_01.png'}} />
      {/* ---- SHORT #299 ---- */}
      <Composition id="Short-short299-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT299, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT299, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short299-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT299, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT299, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short299" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT299, headline: 'ALREADY\nCLOSED', badge: 'FULL CASE', backgroundSrc: 'shorts/short299/short299_01.png'}} />
      {/* ---- SHORT #300 ---- */}
      <Composition id="Short-short300-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT300, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT300, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short300-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT300, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT300, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short300" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT300, headline: 'UNINTERRUPTED\nPOWER', badge: 'FULL CASE', backgroundSrc: 'shorts/short300/short300_01.png'}} />
      {/* ---- SHORT #301 ---- */}
      <Composition id="Short-short301-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT301, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT301, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short301-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT301, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT301, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short301" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT301, headline: 'SEVENTY\nCLOSE THE ROAD', badge: 'FULL CASE', backgroundSrc: 'shorts/short301/short301_01.png'}} />
      {/* ---- SHORT #302 ---- */}
      <Composition id="Short-short302-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT302, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT302, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short302-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT302, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT302, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short302" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT302, headline: 'CARRIED\nOUT', badge: '2013', backgroundSrc: 'shorts/short302/short302_01.png'}} />
      {/* ---- SHORT #303 ---- */}
      <Composition id="Short-short303-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT303, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT303, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short303-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT303, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT303, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short303" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT303, headline: 'TWO\nPER CENT', badge: '1999', backgroundSrc: 'shorts/short303/short303_01.png'}} />
      {/* ---- SHORT #304 ---- */}
      <Composition id="Short-short304-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT304, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT304, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short304-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT304, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT304, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short304" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT304, headline: 'NOT THE THING\nBEING TESTED', badge: 'FULL CASE', backgroundSrc: 'shorts/short304/short304_01.png'}} />
      {/* ---- SHORT #305 ---- */}
      <Composition id="Short-short305-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT305, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT305, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short305-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT305, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT305, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short305" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT305, headline: 'NINETY-FOUR\nPER CENT', badge: 'FULL CASE', backgroundSrc: 'shorts/short305/short305_01.png'}} />
      {/* ---- SHORT #306 ---- */}
      <Composition id="Short-short306-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT306, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT306, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short306-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT306, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT306, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short306" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT306, headline: 'NO\nDECISION', badge: 'FULL CASE', backgroundSrc: 'shorts/short306/short306_01.png'}} />
      {/* ---- SHORT #307 ---- */}
      <Composition id="Short-short307-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT307, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT307, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short307-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT307, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT307, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short307" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT307, headline: 'DECLINED\nTO ACT', badge: '2011', backgroundSrc: 'shorts/short307/short307_01.png'}} />
      {/* ---- SHORT #308 ---- */}
      <Composition id="Short-short308-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT308, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT308, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short308-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT308, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT308, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short308" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT308, headline: 'FOUR MINUTES\nTWENTY-THREE SECONDS', badge: 'FULL CASE', backgroundSrc: 'shorts/short308/short308_01.png'}} />
      {/* ---- SHORT #309 ---- */}
      <Composition id="Short-short309-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT309, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT309, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short309-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT309, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT309, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short309" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT309, headline: 'NOT IDENTIFIED\nAS CRITICAL', badge: 'FULL CASE', backgroundSrc: 'shorts/short309/short309_01.png'}} />

      <Composition id="Short-short310-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT310, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT310, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short310-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT310, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT310, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short310" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT310, headline: 'SIXTY-SEVEN\nSECONDS', badge: '2024', backgroundSrc: 'shorts/short310/short310_01.png'}} />

      <Composition id="Short-short311-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT311, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT311, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short311-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT311, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT311, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short311" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT311, headline: 'A LOOSE\nWIRE', badge: 'NTSB', backgroundSrc: 'shorts/short311/short311_01.png'}} />

      <Composition id="Short-short312-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT312, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT312, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short312-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT312, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT312, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short312" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT312, headline: 'SIXTY-EIGHT\nBRIDGES', badge: 'FULL CASE', backgroundSrc: 'shorts/short312/short312_01.png'}} />

      <Composition id="Short-short313-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT313, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT313, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short313-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT313, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT313, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short313" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT313, headline: 'EIGHTEEN\nSECONDS', badge: '2009', backgroundSrc: 'shorts/short313/short313_01.png'}} />

      <Composition id="Short-short314-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT314, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT314, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short314-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT314, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT314, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short314" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT314, headline: 'ENTIRELY\nOPT-IN', badge: 'FULL CASE', backgroundSrc: 'shorts/short314/short314_01.png'}} />

      <Composition id="Short-short315-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT315, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT315, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short315-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT315, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT315, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short315" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT315, headline: 'TRUE.\nNOT COMPLETE', badge: 'NTSB', backgroundSrc: 'shorts/short315/short315_01.png'}} />

      <Composition id="Short-short316-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT316, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT316, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short316-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT316, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT316, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short316" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT316, headline: 'THE ENTIRE\nSAFETY NET', badge: '2000', backgroundSrc: 'shorts/short316/short316_01.png'}} />

      <Composition id="Short-short317-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT317, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT317, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short317-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT317, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT317, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short317" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT317, headline: 'IT WAS\nCIRCULATED', badge: 'FULL CASE', backgroundSrc: 'shorts/short317/short317_01.png'}} />

      <Composition id="Short-short318-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT318, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT318, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short318-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT318, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT318, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short318" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT318, headline: 'FOUR HUNDRED\nPER CENT', badge: 'NTSB', backgroundSrc: 'shorts/short318/short318_01.png'}} />

      <Composition id="Short-short319-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT319, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT319, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short319-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT319, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT319, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short319" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT319, headline: 'EVERYBODY\nCOULD HAVE GOT OFF', badge: '2012', backgroundSrc: 'shorts/short319/short319_01.png'}} />

      <Composition id="Short-short320-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT320, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT320, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short320-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT320, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT320, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short320" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT320, headline: 'NEVER ONCE\nWALKED IT', badge: 'FULL CASE', backgroundSrc: 'shorts/short320/short320_01.png'}} />

      <Composition id="Short-short321-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT321, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT321, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short321-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT321, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT321, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short321" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT321, headline: 'NOT ONE\nHUMAN', badge: 'FULL CASE', backgroundSrc: 'shorts/short321/short321_01.png'}} />

      <Composition id="Short-short322-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT322, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT322, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short322-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT322, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT322, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short322" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT322, headline: 'NINETY\nSECONDS', badge: '2003', backgroundSrc: 'shorts/short322/short322_01.png'}} />

      <Composition id="Short-short323-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT323, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT323, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short323-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT323, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT323, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short323" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT323, headline: 'IT DID NOT\nIGNITE AT ALL', badge: 'NIST', backgroundSrc: 'shorts/short323/short323_01.png'}} />

      <Composition id="Short-short324-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT324, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT324, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short324-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT324, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT324, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short324" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT324, headline: 'IT IS\nTHE DOOR', badge: 'FULL CASE', backgroundSrc: 'shorts/short324/short324_01.png'}} />

      <Composition id="Short-short325-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT325, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT325, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short325-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT325, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT325, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short325" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT325, headline: 'THE SAME\nNUMBER OF PEOPLE', badge: '1989', backgroundSrc: 'shorts/short325/short325_01.png'}} />

      <Composition id="Short-short326-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT326, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT326, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short326-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT326, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT326, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short326" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT326, headline: 'THE FIRST THING\nTAKEN AWAY', badge: 'FULL CASE', backgroundSrc: 'shorts/short326/short326_01.png'}} />

      <Composition id="Short-short327-yt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT327, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT327, platform: 'yt' as const, depth: true, method: true}} />
      <Composition id="Short-short327-tt" component={Short}
        durationInFrames={shortDurationInFrames(SHORT327, BRAND.video.fps)}
        fps={BRAND.video.fps} width={1080} height={1920}
        defaultProps={{data: SHORT327, platform: 'tiktok' as const, depth: true, method: true}} />
      <Still id="ShortThumb-short327" component={ShortThumb} width={1080} height={1920}
        defaultProps={{data: SHORT327, headline: 'FORESEEABLE.', badge: 'NTSB', backgroundSrc: 'shorts/short327/short327_01.png'}} />
</>
  );
};
