# Recreate the H: alias at logon.
#
# WHY. The real H: (a Samsung T7) died. What answers to H: today is `subst H: E:\` -- an alias
# that lives in the logon session and DISAPPEARS on reboot. Measured 2026-08-22: 339 scripts in
# this repo still hard-code `H:\pd-media`. After a reboot they all fail at once, and the failure
# has no obvious cause: the path simply is not there.
#
# WHY A LOGON TASK AND NOT THE REGISTRY. The robust fix is
# HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\DOS Devices, which needs administrator
# rights this account does not have (measured: IsInRole(Administrator) = False). A subst is
# per-logon-session, and every PD scheduled task runs with LogonType = Interactive (measured on
# all 13 of them), so a task that runs at logon puts H: in the same session those tasks use.
#
# WHAT IT REFUSES TO DO. It will not map H: to a drive that is not the archive. If E:\pd-archive
# is absent -- E: swapped, unplugged, or a different disk -- it exits 1 and maps nothing, because
# a wrong H: is worse than no H:: the scripts would run and write to the wrong place.
#
# THIS IS THE BANDAGE, NOT THE CURE. The cure is removing `H:\pd-media` from those scripts -- scripts/fix_h_paths.py did 385 of
# them on 2026-08-22; this task still covers the .json records and anything added since.

$ErrorActionPreference = 'Continue'
$repo   = 'C:\Users\aab15\Documents\prime-documentary'
$log    = Join-Path $repo 'runs\ensure_h_drive.log'
$anchor = 'E:\pd-archive'   # must exist before H: is allowed to point at E:\

New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
function Log($msg) {
    Add-Content -Path $log -Encoding utf8 -Value ("{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg)
}

if (Test-Path 'H:\') {
    Log 'H: already present -- nothing to do'
    exit 0
}

if (-not (Test-Path $anchor)) {
    Log "REFUSING: $anchor is not there, so E:\ is not the archive. H: left unmapped on purpose."
    exit 1
}

& subst H: E:\ 2>&1 | ForEach-Object { Log "subst: $_" }
Start-Sleep -Milliseconds 300

if (Test-Path 'H:\pd-archive') {
    Log 'H: recreated -> E:\  (verified H:\pd-archive is readable)'
    exit 0
}

Log 'FAILED: subst ran but H:\pd-archive is not readable'
exit 1
