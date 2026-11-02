import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/kyllo_film.json';

/**
 * KylloFilm — the Kyllo v. United States (EP25) long-form render.
 *
 * Thin per-episode wrapper around the reusable CaseFilm engine. The decoration layer
 * is the downloaded commercial factory shelf: dozens of factory clips staged under
 * remotion/public/kyllo/factory/ are cut into the timeline (see build_kyllo_film_assets.py),
 * so the factory footage is actually used (~1 distinct clip per <45s), alongside the
 * Codex hero stills. Data (cuts / captions / hook) is built deterministically from the
 * narration + forced-aligned captions.
 */
export const KylloFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="LANDMARK RIGHTS"
    title="They Scanned His Home From the Street"
    subtitle="Kyllo v. United States (2001)"
  />
);
