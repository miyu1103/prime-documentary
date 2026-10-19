param(
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$ReviewHtml = Join-Path $Repo "episodes\_planning\pd_014_015_owner_review.html"
$ActionSheet = Join-Path $Repo "episodes\_planning\pd_014_015_owner_action_required.v001.md"
$ReadinessMd = Join-Path $Repo "episodes\_planning\pd_009_015_readiness_check.latest.md"
$ReadinessJson = Join-Path $Repo "episodes\_planning\pd_009_015_readiness_check.latest.json"

Set-Location $Repo

Write-Host "Prime Documentary 14/15 owner review" -ForegroundColor Cyan
Write-Host "Repo: $Repo"
Write-Host ""

Write-Host "Running readiness check..." -ForegroundColor Yellow
python scripts\check_pd_009_015_readiness.py | Write-Host

if (-not (Test-Path -LiteralPath $ReadinessJson)) {
    throw "Missing readiness output: $ReadinessJson"
}

$Readiness = Get-Content -LiteralPath $ReadinessJson -Raw -Encoding UTF8 | ConvertFrom-Json
Write-Host ""
Write-Host ("Readiness: {0}" -f $Readiness.summary.status) -ForegroundColor Yellow

Write-Host ""
Write-Host "Review files:" -ForegroundColor Cyan
Write-Host "  Dashboard:    $ReviewHtml"
Write-Host "  Action sheet: $ActionSheet"
Write-Host "  Status:       $ReadinessMd"
Write-Host ""
Write-Host "Current expected state:" -ForegroundColor Cyan
Write-Host "  9-13: scheduled"
Write-Host "  14/15: edit_review, blocked until exact owner approvals are recorded"
Write-Host ""
Write-Host "No upload, schedule, publish, paid API call, or APR creation is performed by this launcher." -ForegroundColor DarkYellow

if (-not $NoBrowser) {
    if (-not (Test-Path -LiteralPath $ReviewHtml)) {
        throw "Missing review dashboard: $ReviewHtml"
    }
    Start-Process -FilePath $ReviewHtml
}
