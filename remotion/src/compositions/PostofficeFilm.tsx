import React from 'react';
import {BRAND} from '../brand';
import postofficeFilm from '../data/postoffice_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = postofficeFilm as unknown as FilmData;

export const postofficeFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const PostofficeFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Horizon Scandal"
      subtitle="The computer said the money was missing. Britain believed the computer."
    />
  );
};
