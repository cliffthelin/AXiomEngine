Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# -----------------------------
# FORM SETUP (DARK MODE)
# -----------------------------

$form = New-Object System.Windows.Forms.Form
$form.Text = "Folder Flatten Preview (Standalone)"
$form.Size = New-Object System.Drawing.Size(900,650)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(30,30,30)

# -----------------------------
# SELECT FOLDER BUTTON
# -----------------------------

$btnSelect = New-Object System.Windows.Forms.Button
$btnSelect.Text = "Select Folder"
$btnSelect.Size = New-Object System.Drawing.Size(140,35)
$btnSelect.Location = New-Object System.Drawing.Point(20,20)
$btnSelect.BackColor = [System.Drawing.Color]::FromArgb(45,45,45)
$btnSelect.ForeColor = "White"

# -----------------------------
# PREVIEW BUTTON
# -----------------------------

$btnPreview = New-Object System.Windows.Forms.Button
$btnPreview.Text = "Preview Flatten"
$btnPreview.Size = New-Object System.Drawing.Size(160,35)
$btnPreview.Location = New-Object System.Drawing.Point(180,20)
$btnPreview.BackColor = [System.Drawing.Color]::FromArgb(45,45,45)
$btnPreview.ForeColor = "White"

# -----------------------------
# STATUS LABEL (IMPORTANT)
# -----------------------------

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = "Select a folder to begin..."
$statusLabel.Size = New-Object System.Drawing.Size(800,20)
$statusLabel.Location = New-Object System.Drawing.Point(20,65)
$statusLabel.ForeColor = "LightGray"

# -----------------------------
# TEXT DISPLAY BOX
# -----------------------------

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Multiline = $true
$textBox.ScrollBars = "Vertical"
$textBox.Size = New-Object System.Drawing.Size(840,480)
$textBox.Location = New-Object System.Drawing.Point(20,90)
$textBox.BackColor = [System.Drawing.Color]::FromArgb(20,20,20)
$textBox.ForeColor = "White"
$textBox.Font = New-Object System.Drawing.Font("Consolas",10)

# -----------------------------
# FOLDER BROWSER
# -----------------------------

$folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog
$SelectedPath = ""

# -----------------------------
# EVENT: SELECT FOLDER
# -----------------------------

$btnSelect.Add_Click({
    if ($folderDialog.ShowDialog() -eq "OK") {
        $SelectedPath = $folderDialog.SelectedPath
        $statusLabel.Text = "Selected: $SelectedPath"
        $textBox.Clear()
    }
})

# -----------------------------
# EVENT: PREVIEW
# -----------------------------

$btnPreview.Add_Click({

    if (-not $SelectedPath) {
        $statusLabel.Text = "ERROR: No folder selected."
        return
    }

    $textBox.Clear()
    $Delimiter = "__"

    $files = Get-ChildItem -Path $SelectedPath -Recurse -File

    if ($files.Count -eq 0) {
        $statusLabel.Text = "No files found in selected folder."
        return
    }

    $statusLabel.Text = "Processing $($files.Count) files..."

    $previewList = @()

    foreach ($file in $files) {

        # Relative path
        $relative = $file.FullName.Substring($SelectedPath.Length).TrimStart('\')

        $dirPart = Split-Path $relative -Parent
        $name = Split-Path $relative -Leaf

        if ($dirPart) {
            $prefix = $dirPart -replace '[\\/:*?"<>|]', '_' -replace '\\', $Delimiter
            $newName = "$prefix$Delimiter$name"
        } else {
            $newName = $name
        }

        $previewList += $newName
    }

    # Sort for readability
    $previewList = $previewList | Sort-Object

    # Output
    foreach ($item in $previewList) {
        $textBox.AppendText($item + "`r`n")
    }

    $statusLabel.Text = "Preview complete: $($previewList.Count) files shown."
})

# -----------------------------
# ADD CONTROLS
# -----------------------------

$form.Controls.Add($btnSelect)
$form.Controls.Add($btnPreview)
$form.Controls.Add($textBox)
$form.Controls.Add($statusLabel)

# -----------------------------
# RUN
# -----------------------------

$form.ShowDialog()