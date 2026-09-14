# One day's TikTok posting, unattended. Registered with Task Scheduler as PD-TikTokPush.
#
# TikTok has no scheduling API for this account, so this drives TikTok Studio in a real Chrome
# window over CDP. It needs a desktop session; it is not a headless job.
#
# FOUR SEPARATE RUNS OF ONE VIDEO EACH, not one run of four. Measured 2026-08-17: short02 failed
# with COVER_DID_NOT_STICK twice, both times as the second item of a batch, and went through on
# the first attempt when it was the only item in its run. One slot per run costs four browser
# starts and buys a failure mode we do not otherwise know how to avoid.
#
# The date is not "tomorrow". It is the day after the last day already filled, read out of the
# posting ledger, so a day that failed gets picked up instead of skipped forever.
#
# post_day.sh does the two checks that matter before each upload: the browser is up, and TikTok
# Studio is operating the expected account (three videos went to the abandoned account on
# 2026-08-16 because nothing asked). It also refuses if any queued row has lost its cover file.

$ErrorActionPreference = 'Continue'
$repo   = 'C:\Users\aab15\Documents\prime-documentary'
$studio = 'C:\temp\studio_auto'
$log    = Join-Path $studio 'tt_daily_push.log'
$bash   = 'C:\Program Files\Git\bin\bash.exe'

function Log($msg) {
    Add-Content -Path $log -Encoding utf8 -Value ("{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg)
}

Set-Location $repo
Log '--- tiktok push start ---'

# The next day that is not already filled, from the ledger.
$day = & py -3.11 (Join-Path $repo 'scripts\tiktok\next_post_day.py')
$day = ($day | Select-Object -Last 1).Trim()
if ($day -notmatch '^\d{4}-\d{2}-\d{2}$') { Log "FAILED: could not work out the next day (got '$day')"; exit 1 }
Log "filling $day"

# Chrome: launching with the same --user-data-dir joins the existing process rather than
# restarting it, so a degraded instance survives what looks like a restart. Kill first.
try { Stop-Process -Name chrome -Force -ErrorAction Stop } catch {}
Start-Sleep -Seconds 3
& node (Join-Path $repo 'scripts\tiktok\start_chrome.js') | Out-Null

$up = $false
foreach ($i in 1..20) {
    try { Invoke-WebRequest -Uri 'http://127.0.0.1:9222/json/version' -TimeoutSec 3 -UseBasicParsing | Out-Null; $up = $true; break }
    catch { Start-Sleep -Seconds 3 }
}
if (-not $up) { Log 'FAILED: browser never came up on 9222'; exit 1 }

$done = 0
$failStreak = 0
foreach ($slot in 0..3) {
    $out = & $bash 'scripts/tiktok/post_day.sh' $day "$slot" '1' 2>&1 | Out-String
    foreach ($line in ($out -split "`n")) {
        if ($line -match 'SCHEDULED|COVER_|CHECK_LIMIT|REFUSING|ERROR|FAIL') { Log ("slot$slot : " + $line.Trim()) }
    }
    if ($out -match 'SCHEDULED') { $done++; $failStreak = 0 } else { $failStreak++ }

    if ($out -match 'CHECK_LIMIT_REACHED') { Log 'stopping: TikTok daily check limit reached'; break }
    if ($out -match 'REFUSING')            { Log 'stopping: pre-flight refused'; break }

    # Circuit breaker. On 2026-08-16 a broken profile path put the poster into a
    # browser died - rebuilding loop that hammered the login page unattended for
    # minutes. Repeated automated retries against a signed-out account are exactly
    # what botting looks like from the outside. Two failures in a row ends the day.
    if ($failStreak -ge 2) { Log 'stopping: two failures in a row - leaving the account alone until tomorrow'; break }
}

Log "scheduled $done of 4 for $day"
Log '--- tiktok push end ---'
