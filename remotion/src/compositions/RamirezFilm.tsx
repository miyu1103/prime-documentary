import React from 'react';
import {BRAND} from '../brand';
import ramirezFilm from '../data/ramirez_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = ramirezFilm as unknown as FilmData;

export const ramirezFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const RamirezFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="A Letter in the Drawer"
      subtitle="TransUnion LLC v. Ramirez and the harm the law would not see."
    />
  );
};
