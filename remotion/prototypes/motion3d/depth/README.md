# depth — challenge #1: any-image → 3D parallax

Turn any single still (SDXL or stock) into a moving 3D shot: estimate a depth map,
displace a subdivided plane by it in `@remotion/three`, move the camera → real parallax
(foreground moves more than background). Kills the 紙芝居 problem for every still.

## Pipeline
1. Depth map (ComfyUI venv has torch+transformers; Intel DPT cached in HF hub):
   `C:\Users\aab15\ComfyUI\venv\Scripts\python.exe depth.py <in.jpg> <out_depth.png> Intel/dpt-large`
   - **Use `Intel/dpt-large` (safetensors).** transformers 5.x refuses `.bin` on torch < 2.6
     (CVE-2025-32434), so `dpt-hybrid-midas` (pickle) fails; dpt-large has safetensors.
   - Output: 8-bit grayscale, near = white / far = black, lightly blurred (smooth mesh).
2. `DepthScene.tsx` (`@remotion/three`): `planeGeometry(6,4,360,240)` + `meshStandardMaterial
   {map, displacementMap, displacementScale}` under full `ambientLight`, slow elliptical camera.
   Overscan the plane (scale 1.16) so displaced edges stay off-frame; keep camera moves small
   to limit rubber-sheet stretch at depth discontinuities (single-mesh 2.5D limitation).

Port target: a `MovingImage` variant in `src/components/` so EVERY hero still auto-parallaxes.
