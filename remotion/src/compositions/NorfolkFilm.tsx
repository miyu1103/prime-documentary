import React from 'react';
import {BRAND} from '../brand';
import norfolkFilm from '../data/norfolk_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = norfolkFilm as unknown as FilmData;

export const norfolkFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const NorfolkFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Norfolk Four"
      subtitle="Four sailors, four confessions, and one man's DNA."
    />
  );
};
