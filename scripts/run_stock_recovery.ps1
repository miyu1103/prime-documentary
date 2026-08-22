# Run the stock-video recovery detached, so it survives the chat session that started it.
#
# WHY DETACHED. The job is long: pexels is ~40 hours at the provider's 200 requests/hour, pixabay
# ~2 hours at 50/minute. A run tied to a shell dies with the shell, and the previous copy of this
# work was restarted by hand three times for exactly that reason.
#
# WHY PEXELS RUNS TWICE. EP76's registers are a 596-clip subset of the 7,924, and an episode that
# is waiting should not sit behind forty hours of general stock. The subset runs first; the full
# pass then skips everything it already fetched, because already_have() reads the disk and the
# ledger, not a list held in memory.
#
#   pwsh -NoProfile -File scripts\run_stock_recovery.ps1 -Source pexels    <- pwsh, not powershell:
#   Windows PowerShell 5.1 has no -Encoding on Tee-Object and writes the log as UTF-16, which
#   reads back as spaced-out gibberish. pwsh 7 defaults to UTF-8.
#   pwsh -NoProfile -File scripts\run_stock_recovery.ps1 -Source pixabay
#
# Progress:  Get-Content runs\recover_<source>.log -Tail 20
# Stop it:   the recover script releases its lock on exit; kill the python process and delete
#            E:\pd-archive\_ledger\<source>_recover.lock only if it was killed hard.

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('pexels', 'pixabay')]
    [string]$Source
)

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\aab15\Documents\prime-documentary'
Set-Location $repo
$env:PYTHONIOENCODING = 'utf-8'

$log = Join-Path $repo "runs\recover_$Source.log"
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
Add-Content -Path $log -Encoding utf8 -Value ("=== {0} recovery start {1} ===" -f $Source, (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))

if ($Source -eq 'pexels') {
    & py -3.11 -u scripts\recover_stock_shelf.py --source pexels --want-ep76 --write *>&1 |
        Tee-Object -FilePath $log -Append | Out-Null
    Add-Content -Path $log -Encoding utf8 -Value ("--- EP76 subset done {0}; starting the full pass ---" -f (Get-Date -Format 'HH:mm:ss'))
}

& py -3.11 -u scripts\recover_stock_shelf.py --source $Source --write *>&1 |
    Tee-Object -FilePath $log -Append | Out-Null

Add-Content -Path $log -Encoding utf8 -Value ("=== {0} recovery end {1} ===" -f $Source, (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
