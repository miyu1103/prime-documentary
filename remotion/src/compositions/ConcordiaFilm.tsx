import React from 'react';
import {BRAND} from '../brand';
import concordiaFilm from '../data/concordia_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = concordiaFilm as unknown as FilmData;

export const concordiaFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const ConcordiaFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Concordia"
      subtitle="A ship off a Tuscan island, a route flown by hand, and a rule that was written afterwards."
    />
  );
};
