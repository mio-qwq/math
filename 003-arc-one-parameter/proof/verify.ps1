param([string]$LeanExecutable = "lean")

$ErrorActionPreference = "Stop"
$proofDirectory = $PSScriptRoot
$previousLeanPath = $env:LEAN_PATH
$certificates = @(
    "FiniteCore", "FiniteCoreT", "CochainData", "CochainBoundary",
    "CochainClosure0", "CochainClosure1", "CochainClosure2", "CochainClosure"
)

try {
    $env:LEAN_PATH = $proofDirectory
    foreach ($certificate in $certificates) {
        $source = Join-Path $proofDirectory "$certificate.lean"
        $object = Join-Path $proofDirectory "$certificate.olean"
        Write-Output "Checking $certificate.lean with the Lean kernel"
        & $LeanExecutable -o $object $source
        if ($LASTEXITCODE -ne 0) {
            throw "Lean rejected $certificate.lean (exit $LASTEXITCODE)."
        }
    }
} finally {
    $env:LEAN_PATH = $previousLeanPath
}
