# Upload the next finished long-form, once a day, at 16:05 JST.
#
# WHY THIS EXISTS
# ---------------
# 2026-08-24: EP71 oroville was finished at 05:00 -- master rendered, 61 shipped-frame sheets read
# tile by tile, thumbnail selected, packaging measured at zero unsupported claims, dry run green --
# and it was not uploaded, because the upload was a thing a human had to remember to type at 16:00
# and the Shorts automation spent the day's allowance at 16:20. The 8/25 12:00 slot is empty and
# cannot be filled: an upload costs 1,600 units, the reset is at 16:00 JST, and 12:00 is before it.
#
# So the long-form upload runs on the same clock as everything else, five minutes before the
# Shorts push, and it refuses rather than guesses:
#
#   * it uploads ONE episode, the first in QUEUE below whose dry run passes
#   * a dry run that is not green stops that episode and the script moves on
#   * a slug already scheduled (youtube_schedule_result.v001.json present) is skipped
#   * anything else -- quota, a red gate, a missing master -- ends the run with no upload
#
# It never picks its own publish date: upload_schedule_case_v001.py reads the slot from CONFIG.

$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\aab15\Documents\prime-documentary'
Set-Location $repo

# Publication order. Edit this list; do not edit the schedule inside it -- the slot lives in
# scripts/upload_schedule_case_v001.py CONFIG, which is what the ship gate reads.
$QUEUE = @('oroville', 'itaewon', 'lahaina', 'morandi', 'lacmegantic', 'uri')

$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
$log = Join-Path $repo 'runs\longform_push.log'
function Say($m) { "$stamp  $m" | Tee-Object -FilePath $log -Append }

Say "=== longform push starting"

foreach ($slug in $QUEUE) {
    $done = Get-ChildItem -Path (Join-Path $repo 'episodes') -Recurse -Filter 'youtube_schedule_result.v001.json' `
            -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match "-$slug\\" }
    if ($done) { Say "$slug : already scheduled, skipping"; continue }

    Say "$slug : dry run"
    $dry = & py -3.11 scripts\upload_schedule_case_v001.py --ep $slug --dry-run 2>&1 | Out-String
    if ($dry -notmatch 'DRY_RUN_OK') {
        $why = ($dry -split "`n" | Where-Object { $_ -match 'refus|REFUS|blocking|error|Error' } | Select-Object -First 2) -join ' | '
        Say "$slug : dry run NOT green -- $why"
        continue
    }

    Say "$slug : uploading"
    $out = & py -3.11 scripts\upload_schedule_case_v001.py --ep $slug 2>&1 | Out-String
    $line = ($out -split "`n" | Where-Object { $_ -match 'WATCH|SCHEDULED|RESULT' } | Select-Object -First 2) -join ' | '
    Say "$slug : $line"
    Say "=== one episode per day; stopping here"
    exit 0
}

Say "=== nothing uploaded: no episode in the queue had a green dry run"
exit 1
