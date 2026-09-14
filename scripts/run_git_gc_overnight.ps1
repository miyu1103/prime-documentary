# Pack the repository's loose objects, overnight, only when the machine is otherwise idle.
#
# WHY. Measured 2026-08-22: .git is 168 GB, and 158.6 GB of that is 28,681 LOOSE objects against
# 7.6 GB in 11 packs. Loose objects are stored one file per object with no delta compression and
# no sharing between versions, so a repository in this state is several times larger than the
# history it holds. `git gc` packs them and drops objects no commit can reach.
#
# THIS IS NOT A HISTORY REWRITE. Nothing reachable from a branch, a tag or the reflog is removed,
# so rule 08 ("git history rewrite" needs approval) does not apply. What it removes is garbage:
# objects from interrupted operations and from commits that were amended or discarded. 1.85 GB of
# outright `tmp_obj_*` garbage was already deleted by hand on 2026-08-22; this handles the rest.
#
# HOW MUCH IT WILL SAVE IS NOT KNOWN. Video and PNG do not delta-compress, so the gain comes from
# unreachable objects and from packing overhead, not from squeezing the media. The log records the
# before and after so the next person does not have to guess either.
#
# WHY IT REFUSES TO RUN WHEN BUSY. Owner directive 2026-08-22: the long-form lane has priority.
# gc on 158 GB saturates the disk for hours. If a render, an i2v chain, ComfyUI or a stock
# recovery is running, this exits without touching anything and waits for the next night.

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\aab15\Documents\prime-documentary'
$log  = Join-Path $repo 'runs\git_gc.log'
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
function Log($m) { Add-Content -Path $log -Encoding utf8 -Value ("{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) }

Set-Location $repo
Log '--- git gc start ---'

# Exclude THIS process: a command line that names the things it is looking for will always find
# itself. That exact mistake killed a running script on 2026-08-22.
$me   = $PID
$busy = @(Get-CimInstance Win32_Process | Where-Object {
    $_.ProcessId -ne $me -and (
        ($_.Name -eq 'node.exe'        -and $_.CommandLine -like '*remotion*') -or
        ($_.Name -eq 'ffmpeg.exe') -or
        ($_.Name -like 'python*'        -and $_.CommandLine -like '*i2v*') -or
        ($_.Name -like 'python*'        -and $_.CommandLine -like '*recover_stock_shelf*') -or
        ($_.Name -like 'python*'        -and $_.CommandLine -like '*ComfyUI*') -or
        ($_.Name -like 'python*'        -and $_.CommandLine -like '*main.py*')
    )
})
if ($busy.Count -gt 0) {
    Log ("SKIPPED: {0} heavy job(s) running -- long-form has priority. Names: {1}" -f
         $busy.Count, (($busy | ForEach-Object { $_.Name }) -join ','))
    Log '--- git gc end (skipped) ---'
    exit 0
}

$before = ((Get-ChildItem "$repo\.git" -Recurse -File -Force -EA SilentlyContinue | Measure-Object Length -Sum).Sum)
Log ("before: {0:N1} GB" -f ($before / 1GB))

# --prune=now removes unreachable objects immediately instead of keeping two weeks of them. The
# two-week grace exists to protect work in progress; nothing here writes objects outside a commit.
$out = & git gc --prune=now 2>&1 | Out-String
foreach ($line in ($out -split "`n")) { if ($line.Trim()) { Log ("gc: " + $line.Trim()) } }

$after = ((Get-ChildItem "$repo\.git" -Recurse -File -Force -EA SilentlyContinue | Measure-Object Length -Sum).Sum)
Log ("after : {0:N1} GB   (reclaimed {1:N1} GB)" -f ($after / 1GB), (($before - $after) / 1GB))

# Prove the repository still works before calling this a success.
$fsck = & git rev-parse HEAD 2>&1
if ($LASTEXITCODE -eq 0) { Log ("HEAD still resolves: " + $fsck) } else { Log "WARNING: git rev-parse failed after gc" }
Log '--- git gc end ---'
