import React from 'react';
import {BRAND} from '../brand';
import openfieldsFilm from '../data/openfields_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = openfieldsFilm as unknown as FilmData;

export const openfieldsFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const OpenfieldsFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Nobody Has To"
      subtitle="Rainwaters v. TWRA and the land the Fourth Amendment leaves out."
    />
  );
};
