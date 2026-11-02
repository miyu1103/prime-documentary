#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
# ensure webui VRAM stays freed
curl -s -m 15 -X POST http://127.0.0.1:7860/sdapi/v1/unload-checkpoint >/dev/null 2>&1
echo "[chain2] re-i2v people (skin-clean stills)..."
py -3.11 scripts/i2v_centralpark_batch.py >> out_i2v_reclean2.log 2>&1
echo "[chain2] assembling..."
py -3.11 scripts/assemble_centralpark_i2v.py >> out_i2v_reclean2.log 2>&1
echo "[chain2] EP50 face-clean i2v DONE"
