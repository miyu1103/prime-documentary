import React from 'react';
import {BRAND} from '../brand';
import lejeuneFilm from '../data/lejeune_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = lejeuneFilm as unknown as FilmData;

export const lejeuneFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const LejeuneFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Water at Camp Lejeune"
      subtitle="The base measured its own water, wrote down what it found, and left the taps on."
    />
  );
};
