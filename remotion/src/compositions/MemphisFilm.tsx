import React from 'react';
import {BRAND} from '../brand';
import memphisFilm from '../data/memphis_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = memphisFilm as unknown as FilmData;

export const memphisFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const MemphisFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Bill in the Wrong Name"
      subtitle="Memphis Light v. Craft and the right to notice."
    />
  );
};
