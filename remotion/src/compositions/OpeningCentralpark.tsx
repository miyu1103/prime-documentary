import React from 'react';
import {OpeningCleveland, openingClevelandDurationInFrames, OpeningClevelandProps} from './OpeningCleveland';

export type OpeningCentralparkProps = OpeningClevelandProps;

export const openingCentralparkDurationInFrames = openingClevelandDurationInFrames;

export const OpeningCentralpark: React.FC<OpeningCentralparkProps> = (props) => {
  return <OpeningCleveland {...props} />;
};
