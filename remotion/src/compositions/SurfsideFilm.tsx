import React from 'react';
import {BRAND} from '../brand';
import surfsideFilm from '../data/surfside_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = surfsideFilm as unknown as FilmData;

export const surfsideFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const SurfsideFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Surfside"
      subtitle="Everything that mattered was written down before it happened."
    />
  );
};
