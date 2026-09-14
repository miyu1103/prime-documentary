import React from 'react';
import {BRAND} from '../brand';
import hyattFilm from '../data/hyatt_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = hyattFilm as unknown as FilmData;

export const hyattFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const HyattFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="One Rod Becomes Two"
      subtitle="The Kansas City Hyatt Regency walkways and a change that doubled a load."
    />
  );
};
