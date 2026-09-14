import React from 'react';
import {BRAND} from '../brand';
import marmetFilm from '../data/marmet_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = marmetFilm as unknown as FilmData;

export const marmetFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const MarmetFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Paper You Sign at the Door"
      subtitle="Marmet Health Care Center v. Brown and forced arbitration."
    />
  );
};
