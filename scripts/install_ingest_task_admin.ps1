# Register the shelf ingest as a Windows scheduled task so it survives closing the chat,
# and a reboot. MUST BE RUN FROM AN ADMINISTRATOR PowerShell -- registering a task in the
# root task folder is denied to a normal user, which is why the chat could not do it.
#
#   1. Press the Windows key, type "powershell"
#   2. Right-click "Windows PowerShell" -> "Run as administrator"
#   3. Paste this one line and press Enter:
#
#      & "C:\Users\aab15\Documents\prime-documentary\scripts\install_ingest_task_admin.ps1"
#
# The old PD-Ingest-IA task pointed at H:\pd-media\...\ingest_run1.log. H: is a subst alias
# for E:\ that disappears on reboot, so the task failed with result 1 every time it fired --
# most recently 2026-08-27 19:06. This replaces it rather than adding a second one.

$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\aab15\Documents\prime-documentary'

if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
        ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This window is NOT running as administrator. Close it and reopen PowerShell with" -ForegroundColor Red
    Write-Host "'Run as administrator', then paste the same line again." -ForegroundColor Red
    exit 1
}

$cmd = '/c cd /d "' + $repo + '" && py -3.11 -u scripts\ingest_archive_sources.py ' +
       '--source ia,nasa,coverr,mixkit --theme all --limit 200 --passes 20 ' +
       '>> runs\ingest_scheduled.log 2>&1'

$action = New-ScheduledTaskAction -Execute 'cmd' -Argument $cmd -WorkingDirectory $repo

# AtStartup so a reboot restarts it; daily as a safety net if it ever exits early.
# IgnoreNew is the important one: the ingest has no lock of its own, and two copies appending
# to the same ledger is how the ledger was corrupted before.
$triggers = @(
    (New-ScheduledTaskTrigger -AtStartup),
    (New-ScheduledTaskTrigger -Daily -At 03:07)
)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable `
    -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Limited

Register-ScheduledTask -TaskName 'PD-Ingest-IA' -Action $action -Trigger $triggers `
    -Settings $settings -Principal $principal -Force | Out-Null

Write-Host "PD-Ingest-IA registered." -ForegroundColor Green
Get-ScheduledTask -TaskName 'PD-Ingest-IA' | Select-Object TaskName, State | Format-Table -AutoSize

Write-Host ""
Write-Host "Before starting it, close the chat session's own copy or it will be a second writer:"
Write-Host "  Get-CimInstance Win32_Process -Filter \"Name like '%python%'\" |"
Write-Host "    Where-Object { `$_.CommandLine -like '*ingest_archive_sources*' } |"
Write-Host "    ForEach-Object { Stop-Process -Id `$_.ProcessId -Force }"
Write-Host ""
Write-Host "Then:  Start-ScheduledTask -TaskName 'PD-Ingest-IA'"
Write-Host "Check: Get-Content '$repo\runs\ingest_scheduled.log' -Tail 5"
