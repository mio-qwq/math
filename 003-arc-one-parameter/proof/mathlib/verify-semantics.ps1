param(
    [string]$LakeExecutable = "lake",
    [switch]$FetchCache,
    [switch]$UseExistingStd
)

$ErrorActionPreference = "Stop"
$packageDirectory = $PSScriptRoot
$proofDirectory = Split-Path -Parent $packageDirectory
$previousLeanPath = $env:LEAN_PATH
$stdModules = @("FiniteCore", "FiniteCoreT", "CochainData")
$semanticModules = @(
    "BitPolynomial", "BytePacking", "TermSemantics", "ScalarEvaluation",
    "TableBasisSemantics", "FiniteBilinear", "FiniteBilinearUnit",
    "FiniteBilinearLaws", "FiniteTableContraction", "TwentyDimAssociativity",
    "TwentyDimUnit", "TracePairSemantics", "TraceInvariance", "TwentyDimAlgebra"
)

function Invoke-LeanModule([string]$Directory, [string]$Module) {
    $source = Join-Path $Directory "$Module.lean"
    $object = Join-Path $Directory "$Module.olean"
    Write-Output "Checking $Module.lean"
    & $LakeExecutable env lean "--root=$Directory" -o $object $source
    if ($LASTEXITCODE -ne 0) {
        throw "Lean rejected $Module.lean (exit $LASTEXITCODE)."
    }
}

Push-Location $packageDirectory
try {
    $env:LEAN_PATH = $packageDirectory + [IO.Path]::PathSeparator + $proofDirectory
    if ($FetchCache) {
        $imports = foreach ($module in $semanticModules) {
            foreach ($line in Get-Content (Join-Path $packageDirectory "$module.lean")) {
                if ($line -match '^import (Mathlib\.[A-Za-z0-9_.]+)$') {
                    $Matches[1].Replace('.', '/') + '.lean'
                }
            }
        }
        $imports = @($imports | Sort-Object -Unique)
        & $LakeExecutable exe cache get @imports
        if ($LASTEXITCODE -ne 0) { throw "Mathlib cache retrieval failed." }
    }

    foreach ($module in $stdModules) {
        if ($UseExistingStd) {
            if (-not (Test-Path -LiteralPath (Join-Path $proofDirectory "$module.olean"))) {
                throw "Missing $module.olean; run without -UseExistingStd."
            }
            Write-Output "Using existing $module.olean; its source is not rechecked in this run."
        } else {
            Invoke-LeanModule $proofDirectory $module
        }
    }
    foreach ($module in $semanticModules) {
        Invoke-LeanModule $packageDirectory $module
    }
    Write-Output "PASS: all $($semanticModules.Count) semantic modules compiled."
    if (-not $UseExistingStd) {
        Write-Output "The $($stdModules.Count) required Std source modules were also recompiled."
    }
    Write-Output "This replay does not include the separate large cochain closure blocks or prove the complete ARC realization."
} finally {
    $env:LEAN_PATH = $previousLeanPath
    Pop-Location
}
