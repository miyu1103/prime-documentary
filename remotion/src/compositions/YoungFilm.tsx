import React from 'react';
import {BRAND} from '../brand';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';
import youngFilm from '../data/young_film.json';

const data = youngFilm as unknown as FilmData;

export const youngFilmDurationInFrames = (fps = BRAND.video.fps) => caseFilmDurationInFrames(data, fps);

export const YoungFilm: React.FC = () => (
  <CaseFilm
    data={data}
    seriesLabel="PRIME DOCUMENTARY"
    title="Police Raided the Wrong House"
    subtitle="What does the law owe you? Almost nothing it has to."
  />
);
