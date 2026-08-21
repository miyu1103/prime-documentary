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

# 2026-08-20: this used to keep only lines matching a regex. The push failed that day and the
# ONE thing the log did not contain was why: the child's stderr did not match the filter and was
# discarded. A summary log that drops the error is worse than no log. Everything now goes to a
# full transcript; the summary keeps the lines a human scans for.
# THE UPLOAD MUST NOT RUN WITH TWO LIVE DEFAULT ROUTES. Measured 2026-08-20: this machine had
# Wi-Fi (10.40.210.161) and Ethernet (192.168.210.1) both Up on different subnets. When the route
# flips mid-transfer the established TCP connection dies, and YouTube accepts the metadata FIRST --
# so short151 sat in Studio looking scheduled for 2026-08-24 21:00 while its body was never
# received, and would have published as an empty video. EP69 hyatt aborted the same way at
# 1,334 MB of 1,645 MB after twelve retries. Uploads run clean with one route: five Shorts went
# through on 2026-08-21 with zero drops, all five processed/succeeded.
#
# Count routes on LIVE adapters ONLY. A disconnected Wi-Fi leaves its row in the route table, so
# counting rows makes this guard refuse a machine that is actually fine -- that false refusal
# already stopped one upload run.
$liveRoutes = @(Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue |
    Where-Object { (Get-NetAdapter -InterfaceIndex $_.ifIndex -ErrorAction SilentlyContinue).Status -eq 'Up' }).Count
if ($liveRoutes -ne 1) {
    Log ("REFUSING TO UPLOAD: {0} live default route(s), expected 1. Turn Wi-Fi off from the taskbar (the wired link stays up); no admin rights needed. Nothing was uploaded and nothing is broken -- the backlog simply waits for the next run." -f $liveRoutes)
    Log '--- shorts push end (refused) ---'
    exit 1
}
Log 'network: 1 live default route -- safe to upload'

$stamp = Get-Date -Format 'yyyyMMdd_HHmm'
$full  = Join-Path $repo ("runs\shorts_thumbs\push_{0}.transcript.log" -f $stamp)

$out = & $bash 'scripts/daily_shorts_push.sh' '1650' 2>&1 | Out-String
Set-Content -Path $full -Value $out -Encoding utf8
Log ("push: full transcript -> " + $full)

foreach ($line in ($out -split "`n")) {
    if ($line -match 'backlog=|-> \d{2}-\d{2}|scheduled=|per day:|FAIL|failed|out of sync|\|') {
        Log ("push: " + $line.Trim())
    }
}

Log '--- shorts push end ---'
