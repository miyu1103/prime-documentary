import React from 'react';
import {BRAND} from '../brand';
import keybridgeFilm from '../data/keybridge_film.json';
import {CaseFilm, caseFilmDurationInFrames, FilmData} from './CaseFilm';

const data = keybridgeFilm as unknown as FilmData;

export const keybridgeFilmDurationInFrames = caseFilmDurationInFrames(data, BRAND.video.fps);

export const KeyBridgeFilm: React.FC = () => {
  return (
    <CaseFilm
      data={data}
      seriesLabel="PRIME DOCUMENTARY"
      title="Key Bridge"
      subtitle="A blackout at one twenty-five, an order to stop the traffic, and an indictment that is only an accusation."
    />
  );
};
