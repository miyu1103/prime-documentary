import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/cotton_film.json';

/**
 * CottonFilm — the Ronald Cotton / Jennifer Thompson (EP30) long-form render.
 *
 * Thin per-episode wrapper around the reusable CaseFilm engine (same pattern as
 * KylloFilm / KatzFilm). The decoration layer is the downloaded commercial factory
 * shelf: 96 themed factory clips staged under remotion/public/cotton/factory/ are cut
 * into the timeline (see build_case_film_assets.py) — 124 of the 207 cuts are factory
 * footage (~4:6 image:footage, distinct-fraction 0.66, max reuse 3), alongside the 40
 * Codex hero stills. Data (cuts / captions / hook / graphics) is built deterministically
 * from the narration + forced-aligned captions. Canonical BrandOpening / BrandEndcard
 * bookends come from CaseFilm.
 */
export const CottonFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="Prime Documentary"
    title="She Was Sure. She Was Wrong."
    subtitle="Ronald Cotton · eyewitness misidentification"
  />
);
