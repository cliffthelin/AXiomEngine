Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# -----------------------------
# FORM
# -----------------------------
$form = New-Object System.Windows.Forms.Form
$form.Text = "Folder Flatten Tool"
$form.Size = New-Object System.Drawing.Size(900,650)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(30,30,30)

# -----------------------------
# BUTTONS
# -----------------------------

$btnSelect = New-Object System.Windows.Forms.Button
$btnSelect.Text = "Select Folder"
$btnSelect.Size = New-Object System.Drawing.Size(140,35)
$btnSelect.Location = New-Object System.Drawing.Point(20,20)
$btnSelect.BackColor = [System.Drawing.Color]::FromArgb(45,45,45)
$btnSelect.ForeColor = "White"

$btnPreview = New-Object System.Windows.Forms.Button
$btnPreview.Text = "Preview"
$btnPreview.Size = New-Object System.Drawing.Size(140,35)
$btnPreview.Location = New-Object System.Drawing.Point(180,20)
$btnPreview.BackColor = [System.Drawing.Color]::FromArgb(45,45,45)
$btnPreview.ForeColor = "White"

$btnRun = New-Object System.Windows.Forms.Button
$btnRun.Text = "Run Flatten"
$btnRun.Size = New-Object System.Drawing.Size(160,35)
$btnRun.Location = New-Object System.Drawing.Point(340,20)
$btnRun.BackColor = [System.Drawing.Color]::FromArgb(70,70,70)
$btnRun.ForeColor = "White"

# -----------------------------
# STATUS
# -----------------------------

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = "Select a folder..."
$statusLabel.Size = New-Object System.Drawing.Size(800,20)
$statusLabel.Location = New-Object System.Drawing.Point(20,65)
$statusLabel.ForeColor = "LightGray"

# -----------------------------
# TEXTBOX
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
# FOLDER DIALOG
# -----------------------------

$folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog
$script:SelectedPath = ""

# -----------------------------
# SELECT EVENT (FIXED)
# -----------------------------

$btnSelect.Add_Click({
    if ($folderDialog.ShowDialog() -eq "OK") {
        $script:SelectedPath = $folderDialog.SelectedPath
        $statusLabel.Text = "Selected: $script:SelectedPath"
        $textBox.Clear()
    }
})

# -----------------------------
# PREVIEW EVENT (FIXED)
# -----------------------------

$btnPreview.Add_Click({

    if (-not $script:SelectedPath) {
        $statusLabel.Text = "ERROR: No folder selected."
        return
    }

    $files = Get-ChildItem -Path $script:SelectedPath -Recurse -File |
             Where-Object { $_.FullName -notlike "*\_flattened\*" }

    if ($files.Count -eq 0) {
        $statusLabel.Text = "No files found."
        return
    }

    $textBox.Clear()
    $statusLabel.Text = "Previewing $($files.Count) files..."

    $Delimiter = "__"

    foreach ($file in $files | Sort-Object FullName) {

        $relative = $file.FullName.Substring($script:SelectedPath.Length).TrimStart('\')

        $dirPart = Split-Path $relative -Parent
        $name = Split-Path $relative -Leaf

        if ($dirPart) {
            $prefix = $dirPart -replace '[\\/:*?"<>|]', '_' -replace '\\', $Delimiter
            $newName = "$prefix$Delimiter$name"
        } else {
            $newName = $name
        }

        $textBox.AppendText($newName + "`r`n")
    }

    $statusLabel.Text = "Preview complete."
})

# -----------------------------
# RUN EVENT (NEW + WORKING)
# -----------------------------

$btnRun.Add_Click({

    if (-not $script:SelectedPath) {
        $statusLabel.Text = "ERROR: No folder selected."
        return
    }

    $destination = Join-Path $script:SelectedPath "_flattened"

    $statusLabel.Text = "Running flatten..."
    $textBox.Clear()

    & "$PSScriptRoot\folder_flattener.ps1" `
        -SourceRoot $script:SelectedPath `
        -DestinationRoot $destination 2>&1 |
        ForEach-Object { $textBox.AppendText($_ + "`r`n") }

    $statusLabel.Text = "DONE → $destination"
})

# -----------------------------
# ADD CONTROLS
# -----------------------------

$form.Controls.Add($btnSelect)
$form.Controls.Add($btnPreview)
$form.Controls.Add($btnRun)
$form.Controls.Add($textBox)
$form.Controls.Add($statusLabel)

# -----------------------------
# RUN GUI
# -----------------------------

$form.ShowDialog()