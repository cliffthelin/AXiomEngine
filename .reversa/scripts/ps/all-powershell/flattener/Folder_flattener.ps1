<#
.SYNOPSIS
    Flattens a folder structure into a single directory.

.DESCRIPTION
    Recursively copies files from SourceRoot into DestinationRoot,
    prefixing folder path into filename using "__".

    Example:
        Finance\FY2025\file.txt -> Finance__FY2025__file.txt
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SourceRoot,

    [Parameter(Mandatory=$true)]
    [string]$DestinationRoot
)

$Delimiter = "__"

if (-not (Test-Path $SourceRoot)) {
    throw "SourceRoot does not exist: $SourceRoot"
}

$files = Get-ChildItem -Path $SourceRoot -Recurse -File |
         Where-Object { $_.FullName -notlike "*\_flattened\*" }

if ($files.Count -eq 0) {
    throw "No files found under SourceRoot: $SourceRoot"
}

if (-not (Test-Path $DestinationRoot)) {
    New-Item -ItemType Directory -Path $DestinationRoot | Out-Null
}

Write-Host "Processing $($files.Count) files..."

foreach ($file in $files) {

    $relative = $file.FullName.Substring((Resolve-Path $SourceRoot).Path.Length).TrimStart('\')

    $dirPart = Split-Path $relative -Parent
    $name = Split-Path $relative -Leaf

    if ($dirPart) {
        $prefix = $dirPart -replace '[\\/:*?"<>|]', '_' -replace '\\', $Delimiter
        $newName = "$prefix$Delimiter$name"
    } else {
        $newName = $name
    }

    $outputPath = Join-Path $DestinationRoot $newName
    $counter = 1

    while (Test-Path $outputPath) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($newName)
        $ext  = [System.IO.Path]::GetExtension($newName)
        $outputPath = Join-Path $DestinationRoot ("{0}_{1}{2}" -f $base, $counter, $ext)
        $counter++
    }

    Write-Host "COPY -> $outputPath"
    Copy-Item -Path $file.FullName -Destination $outputPath
}

Write-Host "Flatten complete -> $DestinationRoot"