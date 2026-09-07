import React from 'react';
import {BRAND} from '../brand';
import greeneFilm from '../data/greene_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = greeneFilm as unknown as FilmData;

export const greeneFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const GreeneFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="A Paper on the Door"
      subtitle="Greene v. Lindsey and the notice that vanished."
    />
  );
};
