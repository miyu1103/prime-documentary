export type FlashCrashFactoryAsset = {
  id: string;
  src: string;
  kind: 'image' | 'video';
  layer: 'background' | 'light' | 'texture' | 'vfx';
};

export const FLASHCRASH_FACTORY_ASSETS: FlashCrashFactoryAsset[] = [];
