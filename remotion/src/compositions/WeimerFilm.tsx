import React from 'react';
import {BRAND} from '../brand';
import weimerFilm from '../data/weimer_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = weimerFilm as unknown as FilmData;

export const weimerFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const WeimerFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Eleven Springs"
      subtitle="Nobody ever found anything."
    />
  );
};
