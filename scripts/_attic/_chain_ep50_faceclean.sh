#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
echo "[chain] batch1 people (P01-36 skin-clean)..."
py -3.11 scripts/gen_centralpark_people_sdxl.py >> out_ep50_people_reclean1.log 2>&1
echo "[chain] batch2 people (P37-76 skin-clean)..."
py -3.11 scripts/gen_centralpark_people2_sdxl.py >> out_ep50_people_reclean2.log 2>&1
echo "[chain] deleting old people i2v (cp_P) to force re-i2v..."
rm -rf /c/Users/aab15/ae-demo/wan_frames_cp_P* 2>/dev/null
rm -f /c/Users/aab15/ComfyUI/output/wanout/cp_P* 2>/dev/null
echo "[chain] re-i2v people (skin-clean); scenes cp_V skipped..."
py -3.11 scripts/i2v_centralpark_batch.py >> out_i2v_reclean.log 2>&1
echo "[chain] assembling re-i2v people..."
py -3.11 scripts/assemble_centralpark_i2v.py >> out_i2v_reclean.log 2>&1
echo "[chain] EP50 face-clean assets DONE"
