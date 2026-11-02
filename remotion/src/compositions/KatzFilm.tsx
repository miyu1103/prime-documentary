import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/katz_film.json';

/**
 * KatzFilm — Katz v. United States (EP26) long-form render.
 * Thin per-episode wrapper around the reusable CaseFilm engine. The decoration layer is the
 * downloaded commercial factory shelf: dozens of factory clips staged under
 * remotion/public/katz/factory/ are cut into the timeline (build_case_film_assets.py), so the
 * factory footage is actually used alongside the Codex hero stills. Dynamic motion-graphics
 * come from the designed on_screen_text (script.annotated) rendered as kinetic-type beats.
 */
export const KatzFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="LANDMARK RIGHTS"
    title="The FBI Recorded His Calls — and Never Touched the Booth"
    subtitle="Katz v. United States (1967)"
  />
);
