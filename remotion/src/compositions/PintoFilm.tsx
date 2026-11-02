import React from 'react';
import {BRAND} from '../brand';
import pintoFilm from '../data/pinto_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = pintoFilm as unknown as FilmData;

export const pintoFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const PintoFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Report Everyone Quotes"
      subtitle="Grimshaw v. Ford Motor Co. and a document the jury never saw."
    />
  );
};
