# Run one stock-recovery lane detached, so it survives the chat session that started it.
#
# WHY DETACHED. The job is long and a run tied to a shell dies with the shell; the previous copy
# of this work was restarted by hand three times for exactly that reason.
#
# FOUR LANES. (pexels|pixabay) x (video|image), each with its own lock and its own pacing, so all
# four run at once. Measured 2026-08-23 on the degraded line, per lane:
#
#     pexels  video  4 workers  ~1,000/hour   (16 MB each, bandwidth-bound)
#     pixabay video  4 workers  ~1,086/hour
#     pexels  image  8 workers  ~1,220/hour   (0.25 MB each, latency-bound)
#     pixabay image  8 workers  ~2,742/hour
#
# WORKER COUNTS ARE MEASURED, NOT GUESSED. Video: 1 stream 2.93 MB/s, 4 streams 5.09, 8 streams
# 2.97 -- four is the knee and eight congests. Image: 8 workers 2,742/hour, 16 workers 2,618 --
# eight is the knee there too. The defaults below are those two measurements.
#
# WHY PEXELS VIDEO RUNS TWICE. EP76's registers are a subset of the whole pexels video set, and
# an episode that is waiting should not sit behind the general stock. The subset runs first; the
# full pass then skips everything it already fetched, because already_have() reads the disk and
# the ledger, not a list held in memory.
#
#   pwsh -NoProfile -File scripts\run_stock_recovery.ps1 -Source pexels  -Kind video
#   pwsh -NoProfile -File scripts\run_stock_recovery.ps1 -Source pixabay -Kind image
#
# Progress:  Get-Content runs\recover_<source>_<kind>.log -Tail 20
# Stop it:   kill the python process; delete E:\pd-archive\_ledger\<source>_<kind>_recover.lock
#            only if it was killed hard (a clean exit releases it).

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('pexels', 'pixabay')]
    [string]$Source,
    # "both" runs video then image IN ONE LANE. Pexels shares a single API key across kinds,
    # so two lanes at once simply take turns being told no: measured 2026-08-23, 34 rate-limit
    # responses between them and both paces ratcheted to the floor. One lane at a time on that
    # key held ~1,000/hour with none.
    [ValidateSet('video', 'image', 'both')]
    [string]$Kind = 'video',
    [int]$Workers = 0
)

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\aab15\Documents\prime-documentary'
Set-Location $repo
$env:PYTHONIOENCODING = 'utf-8'

if ($Workers -le 0) { $Workers = if ($Kind -eq 'image') { 8 } else { 4 } }

$log = Join-Path $repo ("runs\recover_{0}_{1}.log" -f $Source, $Kind)
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
Add-Content -Path $log -Encoding utf8 -Value ("=== {0} {1} start {2} ({3} workers) ===" -f $Source, $Kind, (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Workers)

if ($Source -eq 'pexels' -and $Kind -ne 'image') {
    & py -3.11 -u scripts\recover_stock_shelf.py --source pexels --kind video --want-ep76 --write --workers $Workers *>&1 |
        Tee-Object -FilePath $log -Append | Out-Null
    Add-Content -Path $log -Encoding utf8 -Value ("--- EP76 subset done {0}; starting the full pass ---" -f (Get-Date -Format 'HH:mm:ss'))
}

$kinds = if ($Kind -eq 'both') { @('video', 'image') } else { @($Kind) }
foreach ($kk in $kinds) {
    # Images were 8, measured as the knee against a HEALTHY line on 2026-08-23. On 2026-08-24
    # the image lane drew 429s steadily at that width while the video lane, four wide, held
    # 260/hour for twelve hours with almost none. The pacer gates the metadata call only, so
    # eight concurrent CDN fetches is eight times the pressure the pacer can see. Four.
    $w = $Workers
    Add-Content -Path $log -Encoding utf8 -Value ("--- {0} {1} pass start {2} ({3} workers) ---" -f $Source, $kk, (Get-Date -Format 'HH:mm:ss'), $w)
    & py -3.11 -u scripts\recover_stock_shelf.py --source $Source --kind $kk --write --workers $w *>&1 |
        Tee-Object -FilePath $log -Append | Out-Null
}

Add-Content -Path $log -Encoding utf8 -Value ("=== {0} {1} end {2} ===" -f $Source, $Kind, (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
