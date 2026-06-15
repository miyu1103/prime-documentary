/**
 * Maps sceneId -> path relative to remotion/public/.
 * Scenes not listed here fall back to coded animated art.
 * Prefer approved/ over mj/ when both exist for the same scene.
 */
export const SCENE_IMG: Record<string, string> = {
  S002: 'approved/s002_s014_constitution_fifth_amendment_01_primary.png',
  S003: 'mj/s003_phoenix_arrest.png',
  S004: 'approved/s004_interrogation_room_01_primary.png',
  S005: 'mj/s005_interrogation_imbalance.png',
  S006: 'pd/miranda_fingerprints_1963.jpg',
  S007: 'approved/s007_courtroom_1960s_01_primary.png',
  S008: 'mj/s008_scotus_exterior.png',
  S009: 'pd/miranda_portrait_1967.jpg',
  S010: 'pd/earl_warren_chief_justice.jpg',
  S011: 'mj/s008_scotus_exterior.png',
  S012: 'mj/s012_scotus_chamber.png',
  S013: 'mj/s013_miranda_rights_card.png',
  S014: 'approved/s002_s014_constitution_fifth_amendment_01_primary.png',
  S015: 'pd/earl_warren_chief_justice.jpg',
  S016: 'approved/s016_miranda_warning_card_01_primary.png',
  S017: 'mj/s017_miranda_warning_reading.png',
  S018: 'approved/s018_retrial_symbolic_01_primary.png',
};
