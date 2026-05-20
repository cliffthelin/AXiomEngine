
$schoolYear = "2017"
$sourceDir = '\\usoe-fs2\Datateam$\Data and Statistics\3-Sarah\Audit\PACE_PDF.20170913'
$destDir = 'C:\rpt\PACE_PDF.20170913'
## Remove-Item -Path $destDir\*.* -recurse
 copy-item -Path $sourceDir\*.* -Destination $destDir -Exclude _*.*,DoNot*.*

$files = Get-ChildItem -Path $destDir -Exclude _*.*,DoNot*.*  ##, Name.substring(0,2)

## Create Directories for each LEA
ForEach( $f in $files )
{
    $leaNumber = $f.Name.Substring(0,2)

    if (Test-Path $destDir\$leaNumber) {
    } else {
        new-item -type directory -path $destDir\$leaNumber
     }
}

## moveLEAFiles into their Directory
ForEach( $f in $files )
{
    $leaNumber = $f.name.Substring(0,2)
    if (Test-Path $destDir\$leaNumber)
    {
        Move-Item -Path $f -Destination $destDir\$leanumber
    }
}

## Zip up each directories files into it's own file
ForEach( $d in Get-ChildItem -Directory -Path $destDir)
{
    $compressionLevel = [System.IO.Compression.CompressionLevel]::Optimal
    $zipfilename = "$destDir\$d-PACE-$schoolYear.zip"
    ##Write-Output $zipfilename
    if (test-path $zipfilename) {} else {
    [System.IO.Compression.ZipFile]::CreateFromDirectory("$destDir\$d",$zipfilename, $compressionLevel, $false)
    }
}

## Move files back into root directory
ForEach( $d in Get-ChildItem -Directory -Path $destDir)
{
    move-item -Path $destDir\$d\*.* -Destination $destDir
}

## Remove directories created earlier
get-childitem -directory -path $destDir | remove-item

