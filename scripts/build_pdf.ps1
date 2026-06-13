$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$DataDir = Join-Path $Root "data"
$CanonicalPdf = "C:\Users\wangz\Downloads\49.pdf"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

Push-Location $Root
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
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

$status = [ordered]@{
    paper = 49
    decision = "kill/archive"
    canonical_pdf = $CanonicalPdf
    local_pdf_removed = -not (Test-Path $BuiltPdf)
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}
$status | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $DataDir "build_status.json")
