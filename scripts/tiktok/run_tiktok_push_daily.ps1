# One day's TikTok posting, unattended. Registered with Task Scheduler as PD-TikTokPush.
#
# TikTok has no scheduling API for this account, so this drives TikTok Studio in a real Chrome
# window over CDP. That means the task needs a desktop session; it is not a headless job.
#
# The date is not "tomorrow". It is the day after the last day already filled, read out of the
# posting ledger. A run that fails leaves a gap, and asking for "tomorrow" the next day would
# skip that gap forever; asking for last-filled-plus-one closes it.
#
# Chrome is killed first and restarted: launching with the same --user-data-dir merely joins the
# existing process, so a degraded instance survives what looks like a restart.

$ErrorActionPreference = 'Continue'
$repo   = 'C:\Users\aab15\Documents\prime-documentary'
$studio = 'C:\temp\studio_auto'
$log    = Join-Path $studio 'tt_daily_push.log'

function Log($msg) {
    Add-Content -Path $log -Encoding utf8 -Value ("{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg)
}

Set-Location $repo
Log '--- tiktok push start ---'

# next unfilled day, from the ledger
$day = & py -3.11 -c @"
import json, datetime as dt
from pathlib import Path
p = Path(r'C:\temp\studio_auto\tt_clean_result.jsonl')
days = []
if p.exists():
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get('status') == 'SCHEDULED' and r.get('when'):
            days.append(r['when'].split(' ')[0])
base = max(days) if days else dt.date.today().isoformat()
print((dt.date.fromisoformat(base) + dt.timedelta(days=1)).isoformat())
"@
$day = ($day | Select-Object -Last 1).Trim()
if ($day -notmatch '^\d{4}-\d{2}-\d{2}$') { Log "FAILED: could not work out the next day (got '$day')"; exit 1 }
Log "next day to fill: $day"

try { Stop-Process -Name chrome -Force -ErrorAction Stop } catch {}
Start-Sleep -Seconds 3
& node (Join-Path $repo 'scripts\tiktok\start_chrome.js') | Out-Null

$up = $false
foreach ($i in 1..20) {
    try { Invoke-WebRequest -Uri 'http://127.0.0.1:9222/json/version' -TimeoutSec 3 -UseBasicParsing | Out-Null; $up = $true; break }
    catch { Start-Sleep -Seconds 3 }
}
if (-not $up) { Log 'FAILED: browser never came up on 9222'; exit 1 }

$bash = 'C:\Program Files\Git\bin\bash.exe'
$out = & $bash 'scripts/tiktok/post_day.sh' $day '0' '4' 2>&1 | Out-String
foreach ($line in ($out -split "`n")) {
    if ($line -match 'SCHEDULED|ERROR|CHECK_LIMIT|COVER|FAIL|to schedule|queue=') { Log ("push: " + $line.Trim()) }
}

Log '--- tiktok push end ---'
