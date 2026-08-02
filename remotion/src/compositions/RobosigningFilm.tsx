import React from 'react';
import {BRAND} from '../brand';
import robosigningFilm from '../data/robosigning_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = robosigningFilm as unknown as FilmData;

export const robosigningFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const RobosigningFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Robo-Signing"
      subtitle="A sworn statement is a person's word. Ten thousand a month said otherwise."
    />
  );
};
