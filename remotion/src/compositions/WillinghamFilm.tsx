import React from 'react';
import {BRAND} from '../brand';
import willinghamFilm from '../data/willingham_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = willinghamFilm as unknown as FilmData;

export const willinghamFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const WillinghamFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Fire That Wasn't"
      subtitle="Texas executed him for an arson that the science undid."
    />
  );
};
