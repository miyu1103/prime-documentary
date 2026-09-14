import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/kidsforcash_film.json';

/**
 * KidsForCashFilm — Luzerne County "Kids for Cash" scandal (EP38) long-form render.
 * Thin per-episode wrapper around the reusable premium CaseFilm engine (same as the
 * `Ep38KidsForCash` composition wired in Root.tsx). Unique-sourced factory clips are staged
 * under remotion/public/kidsforcash/factory/ (41, all unique vs other episodes) alongside the
 * 40 hero stills (kfc_S##.png, 4K + depth maps for depth-treated scenes). The 260-cue narration
 * track in data.captions is mounted as burned narration captions by CaseFilm's
 * <Captions cues={data.captions}/> layer; kinetic on-screen figures + AE hero data-cards carry
 * the premium animation. seed timings from kidsforcash_film.json.
 */
export const KidsForCashFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="PRIME DOCUMENTARY"
    title="Kids for Cash"
    subtitle="Two judges. A private jail. Thousands of children."
  />
);
