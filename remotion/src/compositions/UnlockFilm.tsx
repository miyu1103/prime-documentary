import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/unlock_film.json';

/**
 * UnlockFilm — "Can the Police Force Your Phone Open?" (EP31) long-form render.
 *
 * Thin per-episode wrapper around the reusable CaseFilm engine. The decoration layer
 * is the downloaded commercial factory shelf: dozens of factory clips staged under
 * remotion/public/unlock/factory/ (airport_terminal, smartphone_in_dark, surveillance_camera,
 * supreme_court_building, police_car_lights, us_constitution, courtroom, city night, documents…)
 * are cut into the timeline (see build_case_film_assets.py), so the factory footage is
 * actually used (~1 distinct clip per <45s), alongside the 42 Codex hero stills. Data
 * (cuts / captions / hook) is built deterministically from the narration + forced-aligned
 * captions. OP/ED = canonical components/Bookends via CaseFilm.
 */
export const UnlockFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="YOUR RIGHTS"
    title="Can the Police Force Your Phone Open?"
    subtitle="Your face, your thumb, your mind"
  />
);
