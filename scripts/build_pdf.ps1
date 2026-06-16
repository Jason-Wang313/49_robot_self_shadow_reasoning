$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$DataDir = Join-Path $Root "data"
$CanonicalPdf = "C:\Users\wangz\Downloads\49.pdf"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Program,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $Program @Arguments | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "$Program failed with exit code $LASTEXITCODE. Check main.log for details."
    }
}

Push-Location $Root
try {
    Invoke-Checked pdflatex -interaction=nonstopmode -halt-on-error main.tex
    Invoke-Checked bibtex main
    Invoke-Checked pdflatex -interaction=nonstopmode -halt-on-error main.tex
    Invoke-Checked pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

$BuiltPdf = Join-Path $Root "main.pdf"
if (-not (Test-Path $BuiltPdf)) {
    throw "Expected PDF was not produced: $BuiltPdf"
}

Copy-Item -Force -Path $BuiltPdf -Destination $CanonicalPdf
Remove-Item -Force -LiteralPath $BuiltPdf

$hash = Get-FileHash -Path $CanonicalPdf -Algorithm SHA256
$status = [ordered]@{
    paper = 49
    status = "final_v3_full_scale"
    canonical_pdf = $CanonicalPdf
    canonical_sha256 = $hash.Hash
    local_pdf_removed = -not (Test-Path $BuiltPdf)
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}
$status | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $DataDir "build_status.json")
