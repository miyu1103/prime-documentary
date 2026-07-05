import React from 'react';
import {Composition, Still} from 'remotion';
import {BRAND} from './brand';
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
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './compositions/CaseFilm';
import kylloFilm from './data/kyllo_film.json';
import katzFilm from './data/katz_film.json';
import rodriguezFilm from './data/rodriguez_film.json';
import cottonFilm from './data/cotton_film.json';
import unlockFilm from './data/unlock_film.json';
import forfeitureFilm from './data/forfeiture_film.json';
import hintonFilm from './data/hinton_film.json';
import {ColdOpen, MIRANDA_HOOK, hookDurationInFrames} from './compositions/ColdOpen';
import {ThumbConcept} from './compositions/ThumbConcept';
import {ThumbnailFrame} from './components/ThumbnailFrame';
import {RoughCut, roughCutDurationInFrames} from './compositions/RoughCut';
import {BumperBrushupPreview, BrandOpeningOriginalPreview, OneCoinBrandOpeningPreview, bumperBrushupDurationInFrames} from './compositions/OpeningBumperBrushup';
import {EndingBrushupPreview, endingBrushupDurationInFrames} from './compositions/EndingBrushup';
import {Short, ShortThumb, shortDurationInFrames} from './compositions/Short';
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
