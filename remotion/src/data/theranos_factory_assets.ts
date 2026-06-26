export type TheranosFactoryAsset = {
  id: string;
  role: 'bg' | 'light' | 'vfx' | 'particle' | 'texture';
  subtype: string;
  kind: string;
  staticPath: string;
  useScenes: string[];
  sha256: string;
};
export const THERANOS_FACTORY_ASSETS: TheranosFactoryAsset[] = [
  {
    "id": "AF-BG-1999",
    "role": "bg",
    "subtype": "laboratory_glassware",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-1999__laboratory_glassware.jpg",
    "useScenes": [
      "SPN-0004",
      "SPN-0008",
      "SPN-0019"
    ],
    "sha256": "sha256:102fad9c1ae442aa24c390cbe8956d931f1d77da913d110449f5d7b3eb7ad7da"
  },
  {
    "id": "AF-BG-25748",
    "role": "bg",
    "subtype": "blood_vials_in_rack",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-25748__blood_vials_in_rack.jpg",
    "useScenes": [
      "SPN-0001",
      "SPN-0004"
    ],
    "sha256": "sha256:e36b14472db175847494563c7e15d6f06f11facdfa06f18c24035968df94cec2"
  },
  {
    "id": "AF-BG-7274",
    "role": "bg",
    "subtype": "microscope_lab",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-7274__microscope_lab.jpg",
    "useScenes": [
      "SPN-0009",
      "SPN-0019"
    ],
    "sha256": "sha256:255d009d5903515565aa72b8d08aa5332bd6df890d5a21467657001d4def24f0"
  },
  {
    "id": "AF-BG-9898",
    "role": "bg",
    "subtype": "balance_scale_brass",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-9898__balance_scale_brass.jpg",
    "useScenes": [
      "SPN-0012",
      "SPN-0018"
    ],
    "sha256": "sha256:447feab86f24fad6f5d76146f881e56aac4aef013ef3104b0f1ede7993869001"
  },
  {
    "id": "AF-BG-0467",
    "role": "bg",
    "subtype": "courtroom_interior",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-0467__courtroom_interior.jpg",
    "useScenes": [
      "SPN-0013",
      "SPN-0014",
      "SPN-0024"
    ],
    "sha256": "sha256:1466a94a30c0779c72cdebe0f5beaa90b5ffee710eb52240ba55bfc101e06f08"
  },
  {
    "id": "AF-BG-10161",
    "role": "bg",
    "subtype": "stacked_legal_documents",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-10161__stacked_legal_documents.jpg",
    "useScenes": [
      "SPN-0007",
      "SPN-0010",
      "SPN-0023"
    ],
    "sha256": "sha256:e06990bd9b501196158df969cca4103cd3d8db9f078608f99831a8bf1bcebda2"
  },
  {
    "id": "AF-BG-12719",
    "role": "bg",
    "subtype": "stock_chart_crashing_red",
    "kind": "image",
    "staticPath": "theranos/factory/backgrounds/AF-BG-12719__stock_chart_crashing_red.jpg",
    "useScenes": [
      "SPN-0005",
      "SPN-0010"
    ],
    "sha256": "sha256:49a7b1f2e8effc740f09cdf6528c580b533146887792d87c74646c1348642e7c"
  },
  {
    "id": "AF-LIGHT-0220",
    "role": "light",
    "subtype": "god_rays_light",
    "kind": "image",
    "staticPath": "theranos/factory/light_assets/AF-LIGHT-0220__god_rays_light.jpg",
    "useScenes": [
      "SPN-0013"
    ],
    "sha256": "sha256:1e1037927904d59aa3b255f05e194874f81c6cee20945538ce400beff0d0a67b"
  },
  {
    "id": "AF-LIGHT-2059",
    "role": "light",
    "subtype": "blue_light_leak",
    "kind": "image",
    "staticPath": "theranos/factory/light_assets/AF-LIGHT-2059__blue_light_leak.jpg",
    "useScenes": [
      "SPN-0001",
      "SPN-0005",
      "SPN-0020"
    ],
    "sha256": "sha256:f7cfcbaae23eea617297a145f17df4bf68f655534c119af083c18819959e0854"
  },
  {
    "id": "AF-VFX-0001",
    "role": "vfx",
    "subtype": "smoke_on_black_background",
    "kind": "image",
    "staticPath": "theranos/factory/vfx_overlays/AF-VFX-0001__smoke_on_black_background.jpg",
    "useScenes": [
      "SPN-0013",
      "SPN-0014"
    ],
    "sha256": "sha256:0dc32348245e00c4e3d788c91e01147849c1cf44b1da395bf5dac32ea3087804"
  },
  {
    "id": "AF-PART-0268",
    "role": "particle",
    "subtype": "floating_dust_in_light_beam",
    "kind": "image",
    "staticPath": "theranos/factory/particle_assets/AF-PART-0268__floating_dust_in_light_beam.jpg",
    "useScenes": [
      "SPN-0007",
      "SPN-0010",
      "SPN-0012",
      "SPN-0013"
    ],
    "sha256": "sha256:6af950f4955966ee20c02147cd8fd2510983489b33d01415043112fd97bd5441"
  },
  {
    "id": "AF-TEX-0027",
    "role": "texture",
    "subtype": "dark_marble_texture",
    "kind": "image",
    "staticPath": "theranos/factory/texture_assets/AF-TEX-0027__dark_marble_texture.jpg",
    "useScenes": [
      "SPN-0011",
      "SPN-0012",
      "SPN-0018",
      "SPN-0020"
    ],
    "sha256": "sha256:92858ef826c51bc6958d20e1c279cad3a14c5dfbe1b526a7b41debc3f34f9b69"
  }
];
