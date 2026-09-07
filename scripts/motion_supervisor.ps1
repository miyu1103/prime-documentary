# Keep ComfyUI alive for the length of a motion build, and keep the build alive across its deaths.
#
# Measured cause, 2026-08-07: ComfyUI does not crash. It finishes a prompt cleanly and is then
# TERMINATED BY WINDOWS -- Application log, Windows Error Reporting, event 1001, bucket type 5,
# RADAR_PRE_LEAK_64. That is the resource-exhaustion detector deciding the process is leaking.
# Commit charge on this machine sits near 87 of 149 GB with the archive ingest jobs also running,
# so it happens every few dozen prompts. Three separate builds lost work to it: 195 clips came back
# "queue failed, connection refused", 94 of them in the marmet section alone.
#
# So restarting is not a workaround for a bug, it is the operating condition. This supervises both
# halves: it brings ComfyUI back whenever the port stops answering, and it restarts the builder,
# which is already resumable because it skips any plate whose mp4 exists.
#
#   powershell -File scripts\motion_supervisor.ps1
#   powershell -File scripts\motion_supervisor.ps1 -MaxHours 10

param(
  [double] $MaxHours = 12.0,
  [string] $Root     = "C:\Users\aab15\Documents\prime-documentary",
  [string] $Comfy    = "C:\Users\aab15\ComfyUI"
)

$ErrorActionPreference = "Continue"
$deadline = (Get-Date).AddHours($MaxHours)
$log = Join-Path $Root "out_supervisor.log"

function Write-Log([string] $m) {
  $line = "{0}  {1}" -f (Get-Date -Format "HH:mm:ss"), $m
  $line | Tee-Object -FilePath $log -Append | Out-Host
}

function Test-Comfy {
  try { Invoke-WebRequest -Uri http://127.0.0.1:8188/system_stats -TimeoutSec 5 -UseBasicParsing | Out-Null; $true }
  catch { $false }
}

function Start-Comfy {
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match 'ComfyUI.*main\.py' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
  Start-Sleep -Seconds 3
  Start-Process -FilePath (Join-Path $Comfy "venv\Scripts\python.exe") `
    -ArgumentList "main.py","--listen","127.0.0.1","--port","8188" `
    -WorkingDirectory $Comfy `
    -RedirectStandardOutput (Join-Path $Root "out_comfy_sv.log") `
    -RedirectStandardError  (Join-Path $Root "out_comfy_sv.err") `
    -WindowStyle Hidden
  $t = (Get-Date).AddMinutes(5)
  while (-not (Test-Comfy) -and (Get-Date) -lt $t) { Start-Sleep -Seconds 5 }
  if (Test-Comfy) { Write-Log "ComfyUI up" } else { Write-Log "ComfyUI FAILED to come up" }
}

function Get-Builder {
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match 'build_motion_from_plates' } | Select-Object -First 1
}

function Start-Builder([string] $slug) {
  Start-Process -FilePath (Join-Path $Root ".venv\Scripts\python.exe") `
    -ArgumentList "scripts\build_motion_from_plates.py","--slug",$slug,"--limit","400" `
    -WorkingDirectory $Root `
    -RedirectStandardOutput (Join-Path $Root "out_motion_$slug.log") `
    -RedirectStandardError  (Join-Path $Root "out_motion_$slug.err") `
    -WindowStyle Hidden
  Write-Log "builder started for $slug"
}

function Remaining([string] $slug) {
  # -match against an ARRAY returns the matching elements and never populates $Matches, so the
  # supervisor read every episode as "nothing left to make" while 60 were outstanding. Join first.
  $out = (& (Join-Path $Root ".venv\Scripts\python.exe") `
             (Join-Path $Root "scripts\build_motion_from_plates.py") --slug $slug --limit 400 --dry-run 2>&1) -join "`n"
  if ($out -match ',\s*(\d+)\s+to make') { [int]$Matches[1] } else { -1 }
}

Write-Log "supervisor start, deadline $deadline"
foreach ($slug in @("correa","memphis","marmet")) {
  while ((Get-Date) -lt $deadline) {
    if (-not (Test-Comfy)) { Write-Log "$slug : ComfyUI not answering, restarting"; Start-Comfy }
    $left = Remaining $slug
    if ($left -le 0) { Write-Log "$slug : nothing left to make"; break }
    Write-Log "$slug : $left to make"
    Start-Builder $slug
    while ((Get-Builder) -and (Get-Date) -lt $deadline) { Start-Sleep -Seconds 20 }
    Write-Log "$slug : builder exited"
  }
}
Write-Log "supervisor done"
