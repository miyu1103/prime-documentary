import React from 'react';
import {BRAND} from '../brand';
import burgeFilm from '../data/burge_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = burgeFilm as unknown as FilmData;

export const burgeFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const BurgeFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Midnight Crew"
      subtitle="A Chicago station, two decades, and the crime nobody would name."
    />
  );
};
