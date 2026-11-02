# Notice when the stock-recovery lanes stop fetching, and restart them.
#
# WHY. 2026-08-24, measured from the ledger afterwards:
#
#     08時   452 items      lane healthy
#     09時    18            first stall
#     10時   358            restarted by hand
#     11時    57            degraded again
#     12-16時  0            five hours, nothing at all
#     17時    49            noticed, and only because somebody asked
#     18時   325            after the real fix
#
# Six hours of a machine doing nothing while the process sat there looking alive. The lane
# cannot detect this itself: the failure mode is a connection pool full of sockets the far end
# closed, so every request fails, and the adaptive pacer only speeds up after a SUCCESS -- it
# had no way back. A supervisor has to be outside the thing it supervises.
#
# WHY NOT pd_watchdog.py. That one watches the i2v and render chain, belongs to the long-form
# lane, and RECORDS a stall rather than acting on it. What was needed here was a restart: every
# time this was fixed by hand, the fix was "kill it and start it again".
#
# WHAT COUNTS AS A STALL. The newest row in the source's ledger is older than STALL_MINUTES
# while a lane process for that source is alive. A lane that has finished its work exits and
# owns no lock, so "no process" is not a stall -- it is done.
#
#   pwsh -NoProfile -File scripts\watch_stock_recovery.ps1            # one check
#   pwsh -NoProfile -File scripts\watch_stock_recovery.ps1 -Install   # every 15 minutes

param([switch]$Install, [int]$StallMinutes = 25)

$repo = 'C:\Users\aab15\Documents\prime-documentary'
$log  = Join-Path $repo 'runs\watch_stock_recovery.log'

if ($Install) {
    $a = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument `
        "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$repo\scripts\watch_stock_recovery.ps1`""
    $t = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) `
        -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 3650)
    $p = New-ScheduledTaskPrincipal -UserId 'aab15' -LogonType Interactive -RunLevel Limited
    $s = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -MultipleInstances IgnoreNew
    Register-ScheduledTask -TaskName 'PD-WatchStockRecovery' -Action $a -Trigger $t -Principal $p `
        -Settings $s -Description 'Restart a stock-recovery lane that has stopped fetching.' -Force | Out-Null
    "registered PD-WatchStockRecovery, every 15 minutes"
    exit 0
}

$ErrorActionPreference = 'Continue'
Set-Location $repo
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
function Log($m) { Add-Content -Path $log -Encoding utf8 -Value ("{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) }

$me = $PID
foreach ($src in @('pexels', 'pixabay')) {
    # Exclude this process. A command line that names what it is looking for finds itself, and
    # that mistake killed a running script on 2026-08-22.
    $live = @(Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -ne $me -and $_.Name -eq 'python3.11.exe' -and
        $_.CommandLine -like '*recover_stock_shelf*' -and $_.CommandLine -like "*--source $src*"
    })
    if ($live.Count -eq 0) { continue }          # not running is not stalled

    $ledger = "E:\pd-archive\_ledger\$src.jsonl"
    if (-not (Test-Path $ledger)) { continue }
    $age = ((Get-Date) - (Get-Item $ledger).LastWriteTime).TotalMinutes
    if ($age -lt $StallMinutes) { continue }

    Log ("STALLED: {0} has {1} live process(es) and has not written a row for {2:N0} minutes" -f $src, $live.Count, $age)
    $live | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false -EA SilentlyContinue }
    Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -ne $me -and $_.CommandLine -like '*run_stock_recovery*' -and $_.CommandLine -like "*$src*"
    } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false -EA SilentlyContinue }
    Start-Sleep -Seconds 4
    Get-ChildItem "E:\pd-archive\_ledger\${src}_*_recover.lock" -EA SilentlyContinue |
        Remove-Item -Force -Confirm:$false -EA SilentlyContinue

    Start-Process powershell.exe -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass',
        '-WindowStyle', 'Hidden', '-File', "$repo\scripts\run_stock_recovery.ps1",
        '-Source', $src, '-Kind', 'both') -WindowStyle Hidden
    Log ("restarted $src")
}
