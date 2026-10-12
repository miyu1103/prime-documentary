# The GPU lock is held by the long-form render chain (2026-09-07 16:10 JST)

`out_gpu_comfy.lock` names pid 42692, `longform-renders-EP83-85`. That is the supervisor in
`scripts/_runcopy/gpu_handoff_83_85.sh`, rendering EP83 max737, EP84 threemile and EP85
katrina one at a time. `_chain_i2v_robust.sh` reads this file and will decline politely while
it is held -- that is the mechanism, not a workaround.

WHY THIS FILE EXISTS. The EP86 columbia i2v chain and these renders took the same card three
times today. Measured: with the chain running, the render fell from ~350 frames/min to 124,
and at one point to 38. Killing the chain was not converging -- it was restarted at 15:37 and
again at 16:02 -- and every kill destroys that chain's in-flight clip. So the render chain now
takes the lock the project already provides instead of taking the card by force.

The lock goes stale on its own when pid 42692 exits, which is when the last of the three
masters is built. `_chain_i2v_robust.sh` removes a stale lock itself, so columbia resumes with
no action from anyone; it counts finished clips, so nothing it has already made is lost.

If EP86 needs the card sooner than that, stop the supervisor (pid 42692) rather than deleting
this lock -- deleting it just puts both jobs back on one card.
