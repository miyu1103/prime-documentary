# Daily Shorts publishing. Registered with Windows Task Scheduler as PD-ShortsPush so it survives
# reboots and does not depend on any chat session being open.
#
# Why this exists, measured 2026-08-16: 78 finished Shorts were sitting on disk, the channel's
# scheduled queue had three days of runway left, and `videos.insert` was 0 on 08-12, 08-13, 08-14
# and 08-15. Nothing was broken - the push simply requires a human to remember, daily, for the
# sixteen days the backlog lasts, and four of those days had already been missed.
#
# What it does: scripts/daily_shorts_push.sh, which re-reads the channel (never the local ledger),
# uploads what the quota allows onto free 6/9/18/21 JST slots, and re-reads to report. Every step
# is idempotent; running it twice in a day uploads nothing the second time beyond the quota it has.
#
# --reserve 1650 holds one long-form upload's worth of quota back. The episode chain and this task
# draw from the same 10,000/day, and the episode must never lose to a Short.
#
# Timing: 16:20 JST, twenty minutes after the YouTube quota resets (00:00 Pacific) and twenty
# minutes before PD-ShortsFunnelSync, so the day's uploads exist before the funnel pass looks.

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\aab15\Documents\prime-documentary'
$log  = Join-Path $repo 'runs\shorts_thumbs\daily_push.log'
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null

function Log($msg) {
    $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg
    Add-Content -Path $log -Value $line -Encoding utf8
}

Set-Location $repo
$env:PYTHONIOENCODING = 'utf-8'

Log '--- shorts push start ---'

$bash = 'C:\Program Files\Git\bin\bash.exe'
if (-not (Test-Path $bash)) {
    Log "FAILED: git bash not found at $bash"
    exit 1
}

$out = & $bash 'scripts/daily_shorts_push.sh' '1650' 2>&1 | Out-String
foreach ($line in ($out -split "`n")) {
    if ($line -match 'backlog=|-> \d{2}-\d{2}|scheduled=|per day:|FAIL|failed|out of sync') {
        Log ("push: " + $line.Trim())
    }
}

Log '--- shorts push end ---'
