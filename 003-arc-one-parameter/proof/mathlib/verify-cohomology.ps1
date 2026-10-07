param(
    [string[]]$Targets = @("TwentyDimHochschildClass"),
    [string]$LakeExecutable = "lake",
    [switch]$FetchCache,
    [switch]$UseExistingStd,
    [switch]$PlanOnly
)

$ErrorActionPreference = "Stop"
$packageDirectory = $PSScriptRoot
$proofDirectory = Split-Path -Parent $packageDirectory
$previousLeanPath = $env:LEAN_PATH
$taskVisited = @{}
$taskPlan = [Collections.Generic.List[object]]::new()
$taskMathlibImports = [Collections.Generic.HashSet[string]]::new()

function Add-LocalModule([string]$Module) {
    if ($taskVisited[$Module] -eq "done") { return }
    if ($taskVisited[$Module] -eq "visiting") { throw "Local import cycle at $Module." }
    $taskPath = Join-Path $packageDirectory "$Module.lean"
    $taskStd = $false
    if (-not (Test-Path -LiteralPath $taskPath)) {
        $taskPath = Join-Path $proofDirectory "$Module.lean"
        $taskStd = $true
    }
    if (-not (Test-Path -LiteralPath $taskPath)) { throw "Missing local module $Module." }
    $taskVisited[$Module] = "visiting"
    foreach ($taskLine in Get-Content -LiteralPath $taskPath) {
        if ($taskLine -match '^import\s+(.+)$') {
            foreach ($taskImport in ($Matches[1] -split '\s+')) {
                if ($taskImport -eq '--') { break }
                if ($taskImport -like 'Mathlib.*') {
                    [void]$taskMathlibImports.Add($taskImport.Replace('.', '/') + '.lean')
                } elseif ($taskImport -ne 'Std') {
                    Add-LocalModule $taskImport
                }
            }
        }
    }
    $taskVisited[$Module] = "done"
    $taskPlan.Add([pscustomobject]@{ Module = $Module; Source = $taskPath; Std = $taskStd })
}

foreach ($taskTarget in $Targets) { Add-LocalModule $taskTarget }
if ($PlanOnly) {
    $taskPlan | ForEach-Object { "$(if ($_.Std) { 'Std' } else { 'Mathlib package' }): $($_.Module).lean" }
    Write-Output "Plan only: no source compiled and no cache fetched."
    return
}

Push-Location $packageDirectory
try {
    $env:LEAN_PATH = $packageDirectory + [IO.Path]::PathSeparator + $proofDirectory
    if ($FetchCache) {
        $taskImports = @($taskMathlibImports | Sort-Object)
        & $LakeExecutable exe cache get @taskImports
        if ($LASTEXITCODE -ne 0) { throw "Mathlib cache retrieval failed." }
    }
    $taskCompiled = 0
    $taskReused = 0
    foreach ($taskModule in $taskPlan) {
        $taskObject = [IO.Path]::ChangeExtension($taskModule.Source, '.olean')
        if ($UseExistingStd -and $taskModule.Std) {
            if (-not (Test-Path -LiteralPath $taskObject)) {
                throw "Missing $($taskModule.Module).olean; run without -UseExistingStd."
            }
            Write-Output "Using existing $($taskModule.Module).olean; its source is not rechecked in this run."
            $taskReused++
            continue
        }
        $taskRoot = Split-Path -Parent $taskModule.Source
        Write-Output "Checking $($taskModule.Module).lean"
        & $LakeExecutable env lean "--root=$taskRoot" -o $taskObject $taskModule.Source
        if ($LASTEXITCODE -ne 0) {
            throw "Lean rejected $($taskModule.Module).lean (exit $LASTEXITCODE)."
        }
        $taskCompiled++
    }
    Write-Output "PASS: $taskCompiled source modules compiled, $taskReused Std artifacts explicitly reused."
    Write-Output "Targets: $($Targets -join ', '). No Ext comparison or complete ARC realization is claimed."
} finally {
    $env:LEAN_PATH = $previousLeanPath
    Pop-Location
}
