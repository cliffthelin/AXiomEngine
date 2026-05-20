$inventory = @(
    "Consolidated Membership",
    "Dropout Event Summary for SPED",
    "School Summary",
    "Student District of Residence For Charters",
    "Students Not Attending District of Residence For Districts",
    "Child Count by District Worksheet",
    "School Summary SCRAM",
    "SCRAM CCW Detail",
    "Consolidated Membership Cumulative",
    "School Summary Cumulative",
    "SCRAM Extended School Year",
    "Transfer Student List",
    "New Student ELP Scores",
    "Reading on Grade Level",
    "Reading On Grade Level with PACE",
    "Reading On Grade Level with UGG",
    "RISE Class List",
    "Students Eligible for WIDA ACCESS",
    "Utah Compose Class List",
    "UTIPS Class List",
    "Active Registration",
    "Discipline Incident Summary",
    "Discipline Incident Summary for SPED",
    "Exited Students Current Year",
    "Exited Students Previous Year",
    "Grade Range Errors",
    "Graduation Rate For Five Years",
    "Graduation Rate For Four Years",
    "Racial Survey and Detail of Enrollment",
    "Student Summary"
)

$searchPath = "C:\Projects\GITHUB"
$allFiles = Get-ChildItem -Path $searchPath -Filter "*.rdl*" -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Extension -match "\.rdlc?$" }

$results = foreach ($reportName in $inventory) {
    $cleanReportName = $reportName -replace '[^a-zA-Z0-9]', ' '
    $parts = $cleanReportName -split "\s+" | Where-Object { $_.Length -gt 2 }
    
    $matches = $allFiles | Where-Object {
        $file = $_
        $matchScore = 0
        foreach ($part in $parts) {
            if ($file.Name -like "*$part*") { $matchScore++ }
        }
        ($parts.Count -eq 1 -and $matchScore -eq 1) -or ($parts.Count -gt 1 -and $matchScore -ge 2)
    }

    if ($matches) {
        foreach ($match in $matches) {
            $repo = "Unknown"
            if ($match.FullName -match "GITHUB\\([^\\]+)") { $repo = $Matches[1] }
            [PSCustomObject]@{
                RequestedReportName = $reportName
                MatchedFilePath = $match.FullName
                RepoName = $repo
            }
        }
    } else {
        [PSCustomObject]@{
            RequestedReportName = $reportName
            MatchedFilePath = "NO MATCH FOUND"
            RepoName = "N/A"
        }
    }
}

$results | Format-Table -AutoSize
