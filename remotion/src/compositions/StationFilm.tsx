import React from 'react';
import {BRAND} from '../brand';
import stationFilm from '../data/station_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = stationFilm as unknown as FilmData;

export const stationFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const StationFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="The Station"
      subtitle="Two doors on the outside, one door on the inside, and about ninety seconds."
    />
  );
};
