import {Config} from '@remotion/cli/config';

// Final video is English-only, 1080p (decisions/0002 §4/§5).
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
