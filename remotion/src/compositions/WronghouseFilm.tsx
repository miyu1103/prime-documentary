import React from 'react';
import {BRAND} from '../brand';
import wronghouseFilm from '../data/wronghouse_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = wronghouseFilm as unknown as FilmData;

export const wronghouseFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const WronghouseFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Wrong House"
      subtitle="Five o'clock in the morning, an FBI raid, and the address that was never theirs."
    />
  );
};
