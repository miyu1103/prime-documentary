# map — challenge #3: animated documentary map

US map where states draw in + highlight, city pins ripple, and money-trail arcs
draw with a traveling light dot. Accurate geography (real data), broadcast look.

## Data
- Source: `us-atlas@3/states-10m.json` (US Census TIGER → **public domain**).
- `convert_map.mjs` (needs devDeps `d3-geo topojson-client`): projects with
  `geoAlbersUsa().fitExtent(...)` to 1920×1080, emits `us_map.json`
  `{W,H,states:[{name,d}],pins:[{name,x,y}]}`. City lat/long → pixel via the same projection.
  Run: `node convert_map.mjs states-10m.json src/us_map.json`
- `MapScene.tsx` imports the JSON (no d3 at runtime): stroke draw-in (strokeDashoffset)
  staggered L→R, highlight fills, pins with repeating ripples, quadratic-bezier arcs with a
  dot via `qbez()`. Props `{accent,title,highlight[]}`.

Port target: a `CaseMap` component; per-episode data (states/pins/routes) from the shotlist.
