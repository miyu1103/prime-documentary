import React from 'react';
import {BRAND} from '../brand';
import flowersFilm from '../data/flowers_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = flowersFilm as unknown as FilmData;

export const flowersFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const FlowersFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Six Trials"
      subtitle="One prosecutor, one defendant, and the jury he kept rebuilding."
    />
  );
};
