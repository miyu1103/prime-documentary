import React from 'react';
import {BRAND} from '../brand';
import centralparkFilm from '../data/centralpark_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = centralparkFilm as unknown as FilmData;

export const centralparkFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const CentralparkFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Exonerated Five"
      subtitle="A room, a promise, and the hours the camera missed."
    />
  );
};
