import React from 'react';
import {BRAND} from '../brand';
import mortonFilm from '../data/morton_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = mortonFilm as unknown as FilmData;

export const mortonFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const MortonFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Twenty-Five Years"
      subtitle="A boy told the truth, and the file that proved him right stayed shut."
    />
  );
};
