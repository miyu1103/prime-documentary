import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/rodriguez_film.json';

/**
 * RodriguezFilm — Rodriguez v. United States (EP27) long-form render.
 * Thin per-episode wrapper around the reusable CaseFilm engine. Factory clips staged under
 * remotion/public/rodriguez/factory/ are cut into the timeline (build_case_film_assets.py),
 * so the factory footage is actually used alongside the Codex hero stills. Dynamic
 * motion-graphics come from the designed on_screen_text rendered as kinetic-type beats.
 */
export const RodriguezFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="LANDMARK RIGHTS"
    title="How Long Can the Police Keep You at a Traffic Stop?"
    subtitle="Rodriguez v. United States (2015)"
  />
);
