# Daily funnel maintenance. Registered with Windows Task Scheduler as PD-ShortsFunnelSync so it
# survives reboots and does not depend on any chat session being open.
#
# Why this exists: on 2026-08-02 every one of 46 published Shorts pointed nowhere, and 4,391 views
# dead-ended. Long-forms publish one a day, so a different Short becomes linkable every single day.
# Doing that by hand means remembering, daily, forever - and the first day it is forgotten is the
# day a Short goes out with no way back to the case it is about.
#
# What it does, in order:
#   1. attach the long-form link to any Short whose destination has just gone public
#   2. post the channel's own comment carrying the unanswered question and the link
#   3. write a receipt so a later run can be checked rather than trusted
#
# Both steps are idempotent and both refuse rather than guess: a Short whose destination is not
# public is skipped silently and retried tomorrow.

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\aab15\Documents\prime-documentary'
$log  = Join-Path $repo 'runs\short_funnel\daily_sync.log'
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null

function Log($msg) {
    $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg
    Add-Content -Path $log -Value $line -Encoding utf8
}

Set-Location $repo
$env:PYTHONIOENCODING = 'utf-8'

Log '--- funnel sync start ---'

# 1. description line one
$out = & py -3.11 'scripts\daily_funnel_sync.py' '--apply' 2>&1 | Out-String
Log ("daily_funnel_sync: " + (($out -split "`n" | Where-Object { $_ -match 'link out|linked|FAILED' }) -join ' | '))

# 2. the pinned-style comment. Costs 50 units each; skipped automatically if a Short already has
#    one, so a repeat run is cheap.
$out = & py -3.11 'scripts\post_short_funnel_comment.py' '--apply' 2>&1 | Out-String
Log ("funnel_comment: " + (($out -split "`n" | Where-Object { $_ -match 'need a funnel|posted|FAILED' }) -join ' | '))

# 3. state of the funnel after the run, so drift is visible in the log without opening anything
$out = & py -3.11 'scripts\short_funnel_gate.py' 2>&1 | Out-String
Log ("gate: " + (($out -split "`n" | Where-Object { $_ -match 'PASS|FAIL|link' }) -join ' | '))

Log '--- funnel sync end ---'
