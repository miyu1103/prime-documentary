import React from 'react';
import {CaseFilm, FilmData} from './CaseFilm';
import data from '../data/forfeiture_film.json';

/**
 * ForfeitureFilm — Sourovelis v. City of Philadelphia (EP28) long-form render.
 * Thin per-episode wrapper around the reusable premium CaseFilm engine. Factory clips staged
 * under remotion/public/forfeiture/factory/ (96, 6 themes) are cut into the timeline alongside
 * the 40 Codex hero stills (upscaled to 4K). Dynamic motion-graphics come from the designed
 * on_screen_text (script.annotated, 28 beats) rendered as kinetic-type; the AmbientMotion
 * overlay + Trail motion blur + mask-reveal typography are the leveled-up premium animation.
 */
export const ForfeitureFilm: React.FC = () => (
  <CaseFilm
    data={data as unknown as FilmData}
    seriesLabel="THEY DID NOTHING WRONG"
    title="They Took the House"
    subtitle="Sourovelis v. City of Philadelphia (2018)"
  />
);
