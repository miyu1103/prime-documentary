import React from 'react';
import {BRAND} from '../brand';
import fieldtestFilm from '../data/fieldtest_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = fieldtestFilm as unknown as FilmData;

export const fieldtestFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const FieldtestFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The $2 Test"
      subtitle="A roadside kit turned blue. A laboratory said it was nothing at all."
    />
  );
};
