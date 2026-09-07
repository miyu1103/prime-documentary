import React from 'react';
import {BRAND} from '../brand';
import orovilleFilm from '../data/oroville_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = orovilleFilm as unknown as FilmData;

export const orovilleFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const OrovilleFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Oroville"
      subtitle="An evacuation order, a closing shop, and the only court that ever looked at it."
    />
  );
};
