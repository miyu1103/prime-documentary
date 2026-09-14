import React from 'react';
import {BRAND} from '../brand';
import correaFilm from '../data/correa_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = correaFilm as unknown as FilmData;

export const correaFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const CorreaFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Never Called"
      subtitle="Correa v. Hospital San Francisco and a number left waiting."
    />
  );
};
