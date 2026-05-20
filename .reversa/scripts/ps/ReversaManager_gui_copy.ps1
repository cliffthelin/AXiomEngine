Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName Microsoft.VisualBasic

$ErrorActionPreference = 'Stop'

$script:DefaultAgents = @(
    'reversa',
    'reversa-scout',

    $tabPage = New-Object System.Windows.Forms.TabPage
    $tabPage.Text = $Instance.Name
    $tabPage.BackColor = $script:Theme.PanelBack
    $tabPage.ForeColor = $script:Theme.Text

    $catalog = @(Get-MarkdownCatalog -Instance $Instance)
    Save-MarkdownCatalog -Instance $Instance -Catalog $catalog | Out-Null
    $catalogByPath = @{}
    foreach ($entry in $catalog) {
        $catalogByPath[$entry.FullPath] = $entry
    }

    $taskList = @(Get-PlanTasks -PlanPath $Instance.PlanPath)
    $completedTaskCount = @($taskList | Where-Object { $_.Done }).Count

            $tabPage = New-Object System.Windows.Forms.TabPage
            $tabPage.Text = $Instance.Name
            $tabPage.BackColor = $script:Theme.PanelBack
            $tabPage.ForeColor = $script:Theme.Text

            $catalog = @(Get-MarkdownCatalog -Instance $Instance)
            Save-MarkdownCatalog -Instance $Instance -Catalog $catalog | Out-Null
            $catalogByPath = @{}
            foreach ($entry in $catalog) { $catalogByPath[$entry.FullPath] = $entry }
            $taskList = @(Get-PlanTasks -PlanPath $Instance.PlanPath)
            $completedTaskCount = @($taskList | Where-Object { $_.Done }).Count
            $records = @(Get-StatementProvenanceRecords -Instance $Instance)
            $ruleCatalog = @(Get-RuleCatalog -Instance $Instance -Records $records)
            $ruleConflicts = @(Get-RuleConflicts -RuleCatalog $ruleCatalog)
            $provenanceStatus = Get-ProvenanceValidation -Instance $Instance -Catalog $catalog
            $databaseGroundingStatus = Get-DatabaseGroundingValidation -Instance $Instance
            $databaseGroundingPaths = Get-DatabaseGroundingPaths -Instance $Instance
            $traceabilityPaths = Get-TraceabilityPaths -Instance $Instance

            $tabPage.Tag = [pscustomobject]@{
                Instance = $Instance
                Catalog = $catalog
                Provenance = $provenanceStatus
                DatabaseGrounding = $databaseGroundingStatus
                Rules = $ruleCatalog
                Conflicts = $ruleConflicts
            }

            $splitMain = New-Object System.Windows.Forms.SplitContainer
            $splitMain.Dock = 'Fill'
            $splitMain.SplitterDistance = 420
            $splitMain.Panel1.BackColor = $script:Theme.PanelBack
            $splitMain.Panel2.BackColor = $script:Theme.PanelAlt

            $summaryTabs = New-Object System.Windows.Forms.TabControl
            $summaryTabs.Dock = 'Fill'
            $summaryTabs.BackColor = $script:Theme.PanelBack
            $summaryTabs.ForeColor = $script:Theme.Text
            $splitMain.Panel1.Controls.Add($summaryTabs)

            $summaryTab = New-Object System.Windows.Forms.TabPage
            $summaryTab.Text = 'Summary'
            $summaryTab.BackColor = $script:Theme.PanelBack
            $summaryTabs.TabPages.Add($summaryTab)

            $workflowTab = New-Object System.Windows.Forms.TabPage
            $workflowTab.Text = 'Workflow'
            $workflowTab.BackColor = $script:Theme.PanelBack
            $summaryTabs.TabPages.Add($workflowTab)

            $agentsTab = New-Object System.Windows.Forms.TabPage
            $agentsTab.Text = 'Agents'
            $agentsTab.BackColor = $script:Theme.PanelBack
            $summaryTabs.TabPages.Add($agentsTab)

            $summaryLabel = New-Object System.Windows.Forms.Label
            $summaryLabel.Dock = 'Top'
            $summaryLabel.Height = 180
            $summaryLabel.Padding = New-Object System.Windows.Forms.Padding(12)
            $summaryLabel.Font = New-Object System.Drawing.Font('Segoe UI', 10)
            $summaryLabel.ForeColor = $script:Theme.Text
            $summaryTab.Controls.Add($summaryLabel)

            $actionBox = New-Object System.Windows.Forms.GroupBox
            $actionBox.Text = 'Quick Actions'
            $actionBox.Dock = 'Top'
            $actionBox.Height = 118
            $actionBox.ForeColor = $script:Theme.Text
            $actionBox.BackColor = $script:Theme.PanelBack
            $summaryTab.Controls.Add($actionBox)

            $snapshotList = New-Object System.Windows.Forms.ListView
            $snapshotList.Dock = 'Fill'
            $snapshotList.View = 'Details'
            $snapshotList.FullRowSelect = $true
            $snapshotList.HeaderStyle = 'Clickable'
            $snapshotList.BackColor = $script:Theme.Surface
            $snapshotList.ForeColor = $script:Theme.Text
            [void]$snapshotList.Columns.Add('Area', 150)
            [void]$snapshotList.Columns.Add('Value', 90)
            [void]$snapshotList.Columns.Add('Detail', 170)
            Enable-ListViewSorting -ListView $snapshotList
            $summaryTab.Controls.Add($snapshotList)

            $btnOpenProject = New-Object System.Windows.Forms.Button
            $btnOpenProject.Text = 'Open Project'
            $btnOpenProject.Location = New-Object System.Drawing.Point(12, 28)
            $btnOpenProject.Size = New-Object System.Drawing.Size(110, 30)
            $btnOpenProject.BackColor = $script:Theme.PanelAlt
            $btnOpenProject.ForeColor = $script:Theme.Text
            $actionBox.Controls.Add($btnOpenProject)

            $btnOpenOutput = New-Object System.Windows.Forms.Button
            $btnOpenOutput.Text = 'Open Output'
            $btnOpenOutput.Location = New-Object System.Drawing.Point(132, 28)
            $btnOpenOutput.Size = New-Object System.Drawing.Size(110, 30)
            $btnOpenOutput.BackColor = $script:Theme.PanelAlt
            $btnOpenOutput.ForeColor = $script:Theme.Text
            $actionBox.Controls.Add($btnOpenOutput)

            $btnOpenTraceability = New-Object System.Windows.Forms.Button
            $btnOpenTraceability.Text = 'Open Traceability'
            $btnOpenTraceability.Location = New-Object System.Drawing.Point(252, 28)
            $btnOpenTraceability.Size = New-Object System.Drawing.Size(120, 30)
            $btnOpenTraceability.BackColor = $script:Theme.PanelAlt
            $btnOpenTraceability.ForeColor = $script:Theme.Text
            $actionBox.Controls.Add($btnOpenTraceability)

            $btnOpenPlan = New-Object System.Windows.Forms.Button
            $btnOpenPlan.Text = 'Open Plan'
            $btnOpenPlan.Location = New-Object System.Drawing.Point(12, 68)
            $btnOpenPlan.Size = New-Object System.Drawing.Size(110, 30)
            $btnOpenPlan.BackColor = $script:Theme.PanelAlt
            $btnOpenPlan.ForeColor = $script:Theme.Text
            $actionBox.Controls.Add($btnOpenPlan)

            $btnOpenReports = New-Object System.Windows.Forms.Button
            $btnOpenReports.Text = 'Open Reports'
            $btnOpenReports.Location = New-Object System.Drawing.Point(132, 68)
            $btnOpenReports.Size = New-Object System.Drawing.Size(110, 30)
            $btnOpenReports.BackColor = $script:Theme.PanelAlt
            $btnOpenReports.ForeColor = $script:Theme.Text
            $actionBox.Controls.Add($btnOpenReports)

            $btnTabRefresh = New-Object System.Windows.Forms.Button
            $btnTabRefresh.Text = 'Refresh Health'
            $btnTabRefresh.Location = New-Object System.Drawing.Point(252, 68)
            $btnTabRefresh.Size = New-Object System.Drawing.Size(120, 30)
            $btnTabRefresh.BackColor = $script:Theme.AccentSoft
            $btnTabRefresh.ForeColor = $script:Theme.Text
            $actionBox.Controls.Add($btnTabRefresh)

            $workflowSplit = New-Object System.Windows.Forms.SplitContainer
            $workflowSplit.Dock = 'Fill'
            $workflowSplit.Orientation = 'Horizontal'
            $workflowSplit.SplitterDistance = 220
            $workflowTab.Controls.Add($workflowSplit)

            $phaseView = New-Object System.Windows.Forms.ListView
            $phaseView.Dock = 'Fill'
            $phaseView.View = 'Details'
            $phaseView.FullRowSelect = $true
            $phaseView.HeaderStyle = 'Clickable'
            $phaseView.BackColor = $script:Theme.Surface
            $phaseView.ForeColor = $script:Theme.Text
            [void]$phaseView.Columns.Add('Status', 80)
            [void]$phaseView.Columns.Add('Phase', 170)
            [void]$phaseView.Columns.Add('Detail', 130)
            Enable-ListViewSorting -ListView $phaseView
            $workflowSplit.Panel1.Controls.Add($phaseView)

            $taskView = New-Object System.Windows.Forms.ListView
            $taskView.Dock = 'Fill'
            $taskView.View = 'Details'
            $taskView.FullRowSelect = $true
            $taskView.HeaderStyle = 'Clickable'
            $taskView.BackColor = $script:Theme.Surface
            $taskView.ForeColor = $script:Theme.Text
            [void]$taskView.Columns.Add('Done', 60)
            [void]$taskView.Columns.Add('Task', 520)
            Enable-ListViewSorting -ListView $taskView
            $workflowSplit.Panel2.Controls.Add($taskView)

            $agentView = New-Object System.Windows.Forms.ListView
            $agentView.Dock = 'Fill'
            $agentView.View = 'Details'
            $agentView.FullRowSelect = $true
            $agentView.HeaderStyle = 'Clickable'
            $agentView.BackColor = $script:Theme.Surface
            $agentView.ForeColor = $script:Theme.Text
            [void]$agentView.Columns.Add('Agent', 180)
            [void]$agentView.Columns.Add('Statements', 90)
            [void]$agentView.Columns.Add('Artifacts', 80)
            [void]$agentView.Columns.Add('Rules', 70)
            Enable-ListViewSorting -ListView $agentView
            $agentsTab.Controls.Add($agentView)

            $splitRight = New-Object System.Windows.Forms.SplitContainer
            $splitRight.Dock = 'Fill'
            $splitRight.Orientation = 'Vertical'
            $splitRight.SplitterDistance = 520
            $splitMain.Panel2.Controls.Add($splitRight)

            $navTabs = New-Object System.Windows.Forms.TabControl
            $navTabs.Dock = 'Fill'
            $navTabs.BackColor = $script:Theme.PanelAlt
            $navTabs.ForeColor = $script:Theme.Text
            $splitRight.Panel1.Controls.Add($navTabs)

            $documentsTab = New-Object System.Windows.Forms.TabPage
            $documentsTab.Text = 'Documents'
            $documentsTab.BackColor = $script:Theme.PanelAlt
            $navTabs.TabPages.Add($documentsTab)

            $rulesTab = New-Object System.Windows.Forms.TabPage
            $rulesTab.Text = 'Rules'
            $rulesTab.BackColor = $script:Theme.PanelAlt
            $navTabs.TabPages.Add($rulesTab)

            $conflictsTab = New-Object System.Windows.Forms.TabPage
            $conflictsTab.Text = 'Conflicts'
            $conflictsTab.BackColor = $script:Theme.PanelAlt
            $navTabs.TabPages.Add($conflictsTab)

            $filesTab = New-Object System.Windows.Forms.TabPage
            $filesTab.Text = 'Files'
            $filesTab.BackColor = $script:Theme.PanelAlt
            $navTabs.TabPages.Add($filesTab)

            $databaseTab = New-Object System.Windows.Forms.TabPage
            $databaseTab.Text = 'Database'
            $databaseTab.BackColor = $script:Theme.PanelAlt
            $navTabs.TabPages.Add($databaseTab)

            $documentsPanel = New-Object System.Windows.Forms.Panel
            $documentsPanel.Dock = 'Fill'
            $documentsTab.Controls.Add($documentsPanel)

            $documentsFilterPanel = New-Object System.Windows.Forms.Panel
            $documentsFilterPanel.Dock = 'Top'
            $documentsFilterPanel.Height = 52
            $documentsPanel.Controls.Add($documentsFilterPanel)

            $txtDocumentFilter = New-Object System.Windows.Forms.TextBox
            $txtDocumentFilter.Location = New-Object System.Drawing.Point(10, 14)
            $txtDocumentFilter.Size = New-Object System.Drawing.Size(220, 24)
            $txtDocumentFilter.BackColor = $script:Theme.Surface
            $txtDocumentFilter.ForeColor = $script:Theme.Text
            $documentsFilterPanel.Controls.Add($txtDocumentFilter)

            $cmbDocumentCategory = New-Object System.Windows.Forms.ComboBox
            $cmbDocumentCategory.Location = New-Object System.Drawing.Point(240, 14)
            $cmbDocumentCategory.Size = New-Object System.Drawing.Size(180, 24)
            $cmbDocumentCategory.DropDownStyle = 'DropDownList'
            $cmbDocumentCategory.BackColor = $script:Theme.Surface
            $cmbDocumentCategory.ForeColor = $script:Theme.Text
            [void]$cmbDocumentCategory.Items.Add('All Categories')
            foreach ($category in @($catalog | ForEach-Object { $_.Category } | Sort-Object -Unique)) { if ($category) { [void]$cmbDocumentCategory.Items.Add([string]$category) } }
            $cmbDocumentCategory.SelectedIndex = 0
            $documentsFilterPanel.Controls.Add($cmbDocumentCategory)

            $documentView = New-Object System.Windows.Forms.ListView
            $documentView.Dock = 'Fill'
            $documentView.View = 'Details'
            $documentView.FullRowSelect = $true
            $documentView.HeaderStyle = 'Clickable'
            $documentView.MultiSelect = $false
            $documentView.BackColor = $script:Theme.Surface
            $documentView.ForeColor = $script:Theme.Text
            [void]$documentView.Columns.Add('Category', 110)
            [void]$documentView.Columns.Add('Title', 170)
            [void]$documentView.Columns.Add('Relative Path', 220)
            [void]$documentView.Columns.Add('Sources', 70)
            Enable-ListViewSorting -ListView $documentView
            $documentsPanel.Controls.Add($documentView)

            $rulesPanel = New-Object System.Windows.Forms.Panel
            $rulesPanel.Dock = 'Fill'
            $rulesTab.Controls.Add($rulesPanel)

            $rulesFilterPanel = New-Object System.Windows.Forms.Panel
            $rulesFilterPanel.Dock = 'Top'
            $rulesFilterPanel.Height = 52
            $rulesPanel.Controls.Add($rulesFilterPanel)

            $txtRuleFilter = New-Object System.Windows.Forms.TextBox
            $txtRuleFilter.Location = New-Object System.Drawing.Point(10, 14)
            $txtRuleFilter.Size = New-Object System.Drawing.Size(220, 24)
            $txtRuleFilter.BackColor = $script:Theme.Surface
            $txtRuleFilter.ForeColor = $script:Theme.Text
            $rulesFilterPanel.Controls.Add($txtRuleFilter)

            $cmbRuleConfidence = New-Object System.Windows.Forms.ComboBox
            $cmbRuleConfidence.Location = New-Object System.Drawing.Point(240, 14)
            $cmbRuleConfidence.Size = New-Object System.Drawing.Size(180, 24)
            $cmbRuleConfidence.DropDownStyle = 'DropDownList'
            $cmbRuleConfidence.BackColor = $script:Theme.Surface
            $cmbRuleConfidence.ForeColor = $script:Theme.Text
            [void]$cmbRuleConfidence.Items.Add('All Confidence')
            foreach ($confidence in @($ruleCatalog | ForEach-Object { $_.Confidence } | Sort-Object -Unique)) { if ($confidence) { [void]$cmbRuleConfidence.Items.Add([string]$confidence) } }
            $cmbRuleConfidence.SelectedIndex = 0
            $rulesFilterPanel.Controls.Add($cmbRuleConfidence)

            $ruleView = New-Object System.Windows.Forms.ListView
            $ruleView.Dock = 'Fill'
            $ruleView.View = 'Details'
            $ruleView.FullRowSelect = $true
            $ruleView.HeaderStyle = 'Clickable'
            $ruleView.MultiSelect = $false
            $ruleView.BackColor = $script:Theme.Surface
            $ruleView.ForeColor = $script:Theme.Text
            [void]$ruleView.Columns.Add('Rule ID', 110)
            [void]$ruleView.Columns.Add('Confidence', 90)
            [void]$ruleView.Columns.Add('Agent', 110)
            [void]$ruleView.Columns.Add('Artifact', 150)
            [void]$ruleView.Columns.Add('Document', 160)
            [void]$ruleView.Columns.Add('Statement', 260)
            Enable-ListViewSorting -ListView $ruleView
            $rulesPanel.Controls.Add($ruleView)

            $conflictSplit = New-Object System.Windows.Forms.SplitContainer
            $conflictSplit.Dock = 'Fill'
            $conflictSplit.Orientation = 'Horizontal'
            $conflictSplit.SplitterDistance = 210
            $conflictsTab.Controls.Add($conflictSplit)

            $conflictView = New-Object System.Windows.Forms.ListView
            $conflictView.Dock = 'Fill'
            $conflictView.View = 'Details'
            $conflictView.FullRowSelect = $true
            $conflictView.HeaderStyle = 'Clickable'
            $conflictView.MultiSelect = $false
            $conflictView.BackColor = $script:Theme.Surface
            $conflictView.ForeColor = $script:Theme.Text
            [void]$conflictView.Columns.Add('Rule ID', 110)
            [void]$conflictView.Columns.Add('Entries', 60)
            [void]$conflictView.Columns.Add('Confidence', 130)
            [void]$conflictView.Columns.Add('Documents', 170)
            [void]$conflictView.Columns.Add('Summary', 300)
            Enable-ListViewSorting -ListView $conflictView
            $conflictSplit.Panel1.Controls.Add($conflictView)

            $conflictDetailPanel = New-Object System.Windows.Forms.Panel
            $conflictDetailPanel.Dock = 'Fill'
            $conflictSplit.Panel2.Controls.Add($conflictDetailPanel)

            $btnCopyConflictPrompt = New-Object System.Windows.Forms.Button
            $btnCopyConflictPrompt.Text = 'Copy Prompt'
            $btnCopyConflictPrompt.Location = New-Object System.Drawing.Point(10, 8)
            $btnCopyConflictPrompt.Size = New-Object System.Drawing.Size(110, 28)
            $btnCopyConflictPrompt.BackColor = $script:Theme.AccentSoft
            $btnCopyConflictPrompt.ForeColor = $script:Theme.Text
            $btnCopyConflictPrompt.Enabled = $false
            $conflictDetailPanel.Controls.Add($btnCopyConflictPrompt)

            $conflictPromptBox = New-Object System.Windows.Forms.TextBox
            $conflictPromptBox.Location = New-Object System.Drawing.Point(10, 42)
            $conflictPromptBox.Size = New-Object System.Drawing.Size(490, 120)
            $conflictPromptBox.Multiline = $true
            $conflictPromptBox.ReadOnly = $true
            $conflictPromptBox.ScrollBars = 'Both'
            $conflictPromptBox.WordWrap = $false
            $conflictPromptBox.BackColor = $script:Theme.Surface
            $conflictPromptBox.ForeColor = $script:Theme.Text
            $conflictPromptBox.Font = New-Object System.Drawing.Font('Consolas', 9)
            $conflictDetailPanel.Controls.Add($conflictPromptBox)

            $tree = New-Object System.Windows.Forms.TreeView
            $tree.Dock = 'Fill'
            $tree.HideSelection = $false
            $tree.BackColor = $script:Theme.Surface
            $tree.ForeColor = $script:Theme.Text
            $tree.BorderStyle = 'None'
            $filesTab.Controls.Add($tree)

            $dbActionBox = New-Object System.Windows.Forms.GroupBox
            $dbActionBox.Text = 'DB Grounding Actions'
            $dbActionBox.Dock = 'Fill'
            $dbActionBox.ForeColor = $script:Theme.Text
            $dbActionBox.BackColor = $script:Theme.PanelBack
            $databaseTab.Controls.Add($dbActionBox)

            $dbServerLabel = New-Object System.Windows.Forms.Label
            $dbServerLabel.Text = 'Server'
            $dbServerLabel.Location = New-Object System.Drawing.Point(12, 28)
            $dbServerLabel.AutoSize = $true
            $dbActionBox.Controls.Add($dbServerLabel)

            $dbServerBox = New-Object System.Windows.Forms.TextBox
            $dbServerBox.Location = New-Object System.Drawing.Point(12, 48)
            $dbServerBox.Size = New-Object System.Drawing.Size(220, 24)
            $dbServerBox.ReadOnly = $true
            $dbServerBox.BackColor = $script:Theme.Surface
            $dbServerBox.ForeColor = $script:Theme.Text
            $dbActionBox.Controls.Add($dbServerBox)

            $dbNameLabel = New-Object System.Windows.Forms.Label
            $dbNameLabel.Text = 'Database'
            $dbNameLabel.Location = New-Object System.Drawing.Point(244, 28)
            $dbNameLabel.AutoSize = $true
            $dbActionBox.Controls.Add($dbNameLabel)

            $dbNameBox = New-Object System.Windows.Forms.TextBox
            $dbNameBox.Location = New-Object System.Drawing.Point(244, 48)
            $dbNameBox.Size = New-Object System.Drawing.Size(220, 24)
            $dbNameBox.ReadOnly = $true
            $dbNameBox.BackColor = $script:Theme.Surface
            $dbNameBox.ForeColor = $script:Theme.Text
            $dbActionBox.Controls.Add($dbNameBox)

            $dbEngineLabel = New-Object System.Windows.Forms.Label
            $dbEngineLabel.Text = 'Engine'
            $dbEngineLabel.Location = New-Object System.Drawing.Point(12, 78)
            $dbEngineLabel.AutoSize = $true
            $dbActionBox.Controls.Add($dbEngineLabel)

            $dbEngineBox = New-Object System.Windows.Forms.TextBox
            $dbEngineBox.Location = New-Object System.Drawing.Point(12, 98)
            $dbEngineBox.Size = New-Object System.Drawing.Size(120, 24)
            $dbEngineBox.ReadOnly = $true
            $dbEngineBox.BackColor = $script:Theme.Surface
            $dbEngineBox.ForeColor = $script:Theme.Text
            $dbActionBox.Controls.Add($dbEngineBox)

            $dbApprovalLabel = New-Object System.Windows.Forms.Label
            $dbApprovalLabel.Text = 'Approval'
            $dbApprovalLabel.Location = New-Object System.Drawing.Point(144, 78)
            $dbApprovalLabel.AutoSize = $true
            $dbActionBox.Controls.Add($dbApprovalLabel)

            $dbApprovalBox = New-Object System.Windows.Forms.TextBox
            $dbApprovalBox.Location = New-Object System.Drawing.Point(144, 98)
            $dbApprovalBox.Size = New-Object System.Drawing.Size(160, 24)
            $dbApprovalBox.ReadOnly = $true
            $dbApprovalBox.BackColor = $script:Theme.Surface
            $dbApprovalBox.ForeColor = $script:Theme.Text
            $dbActionBox.Controls.Add($dbApprovalBox)

            $dbPilotLabel = New-Object System.Windows.Forms.Label
            $dbPilotLabel.Text = 'Pilot table'
            $dbPilotLabel.Location = New-Object System.Drawing.Point(316, 78)
            $dbPilotLabel.AutoSize = $true
            $dbActionBox.Controls.Add($dbPilotLabel)

            $dbPilotBox = New-Object System.Windows.Forms.TextBox
            $dbPilotBox.Location = New-Object System.Drawing.Point(316, 98)
            $dbPilotBox.Size = New-Object System.Drawing.Size(148, 24)
            $dbPilotBox.ReadOnly = $true
            $dbPilotBox.BackColor = $script:Theme.Surface
            $dbPilotBox.ForeColor = $script:Theme.Text
            $dbActionBox.Controls.Add($dbPilotBox)

            $dbAccessLabel = New-Object System.Windows.Forms.Label
            $dbAccessLabel.Text = 'Access reference'
            $dbAccessLabel.Location = New-Object System.Drawing.Point(12, 128)
            $dbAccessLabel.AutoSize = $true
            $dbActionBox.Controls.Add($dbAccessLabel)

            $dbAccessBox = New-Object System.Windows.Forms.TextBox
            $dbAccessBox.Location = New-Object System.Drawing.Point(12, 148)
            $dbAccessBox.Size = New-Object System.Drawing.Size(452, 24)
            $dbAccessBox.ReadOnly = $true
            $dbAccessBox.BackColor = $script:Theme.Surface
            $dbAccessBox.ForeColor = $script:Theme.Text
            $dbActionBox.Controls.Add($dbAccessBox)

            $queryList = New-Object System.Windows.Forms.ListView
            $queryList.Location = New-Object System.Drawing.Point(12, 182)
            $queryList.Size = New-Object System.Drawing.Size(250, 180)
            $queryList.View = 'Details'
            $queryList.FullRowSelect = $true
            $queryList.HeaderStyle = 'Clickable'
            $queryList.MultiSelect = $false
            $queryList.BackColor = $script:Theme.Surface
            $queryList.ForeColor = $script:Theme.Text
            [void]$queryList.Columns.Add('Query ID', 120)
            [void]$queryList.Columns.Add('Phase', 70)
            [void]$queryList.Columns.Add('Run', 40)
            Enable-ListViewSorting -ListView $queryList
            $dbActionBox.Controls.Add($queryList)

            $queryDetailsBox = New-Object System.Windows.Forms.TextBox
            $queryDetailsBox.Location = New-Object System.Drawing.Point(274, 182)
            $queryDetailsBox.Size = New-Object System.Drawing.Size(190, 180)
            $queryDetailsBox.Multiline = $true
            $queryDetailsBox.ReadOnly = $true
            $queryDetailsBox.ScrollBars = 'Vertical'
            $queryDetailsBox.BackColor = $script:Theme.Surface
            $queryDetailsBox.ForeColor = $script:Theme.Text
            $queryDetailsBox.Font = New-Object System.Drawing.Font('Consolas', 9)
            $dbActionBox.Controls.Add($queryDetailsBox)

            $btnCopyQueryId = New-Object System.Windows.Forms.Button
            $btnCopyQueryId.Text = 'Copy Query ID'
            $btnCopyQueryId.Location = New-Object System.Drawing.Point(274, 144)
            $btnCopyQueryId.Size = New-Object System.Drawing.Size(90, 28)
            $btnCopyQueryId.BackColor = $script:Theme.PanelAlt
            $btnCopyQueryId.ForeColor = $script:Theme.Text
            $btnCopyQueryId.Enabled = $false
            $dbActionBox.Controls.Add($btnCopyQueryId)

            $btnCopyCancel = New-Object System.Windows.Forms.Button
            $btnCopyCancel.Text = 'Copy Cancel'
            $btnCopyCancel.Location = New-Object System.Drawing.Point(374, 144)
            $btnCopyCancel.Size = New-Object System.Drawing.Size(90, 28)
            $btnCopyCancel.BackColor = $script:Theme.PanelAlt
            $btnCopyCancel.ForeColor = $script:Theme.Text
            $btnCopyCancel.Enabled = $false
            $dbActionBox.Controls.Add($btnCopyCancel)

            $previewPanel = New-Object System.Windows.Forms.Panel
            $previewPanel.Dock = 'Fill'
            $splitRight.Panel2.Controls.Add($previewPanel)

            $previewToolbar = New-Object System.Windows.Forms.Panel
            $previewToolbar.Dock = 'Top'
            $previewToolbar.Height = 62
            $previewToolbar.BackColor = $script:Theme.PanelBack
            $previewPanel.Controls.Add($previewToolbar)

            $currentFileLabel = New-Object System.Windows.Forms.Label
            $currentFileLabel.Text = 'Selected file: -'
            $currentFileLabel.Location = New-Object System.Drawing.Point(10, 10)
            $currentFileLabel.AutoSize = $true
            $previewToolbar.Controls.Add($currentFileLabel)

            $metaLabel = New-Object System.Windows.Forms.Label
            $metaLabel.Text = 'Category: - | Sources: -'
            $metaLabel.Location = New-Object System.Drawing.Point(10, 34)
            $metaLabel.AutoSize = $true
            $metaLabel.ForeColor = $script:Theme.Muted
            $previewToolbar.Controls.Add($metaLabel)

            $cmbReferenceOpenMode = New-Object System.Windows.Forms.ComboBox
            $cmbReferenceOpenMode.Location = New-Object System.Drawing.Point(520, 8)
            $cmbReferenceOpenMode.Size = New-Object System.Drawing.Size(110, 24)
            $cmbReferenceOpenMode.DropDownStyle = 'DropDownList'
            $cmbReferenceOpenMode.BackColor = $script:Theme.Surface
            $cmbReferenceOpenMode.ForeColor = $script:Theme.Text
            [void]$cmbReferenceOpenMode.Items.AddRange(@('VS Code', 'OS Default'))
            $cmbReferenceOpenMode.SelectedIndex = 0
            $previewToolbar.Controls.Add($cmbReferenceOpenMode)

            $btnOpenCurrent = New-Object System.Windows.Forms.Button
            $btnOpenCurrent.Text = 'Open Current'
            $btnOpenCurrent.Location = New-Object System.Drawing.Point(640, 7)
            $btnOpenCurrent.Size = New-Object System.Drawing.Size(100, 28)
            $btnOpenCurrent.BackColor = $script:Theme.PanelAlt
            $btnOpenCurrent.ForeColor = $script:Theme.Text
            $previewToolbar.Controls.Add($btnOpenCurrent)

            $btnSaveFile = New-Object System.Windows.Forms.Button
            $btnSaveFile.Text = 'Save'
            $btnSaveFile.Location = New-Object System.Drawing.Point(750, 7)
            $btnSaveFile.Size = New-Object System.Drawing.Size(80, 28)
            $btnSaveFile.BackColor = $script:Theme.AccentSoft
            $btnSaveFile.ForeColor = $script:Theme.Text
            $previewToolbar.Controls.Add($btnSaveFile)

            $btnRefreshPreview = New-Object System.Windows.Forms.Button
            $btnRefreshPreview.Text = 'Refresh Preview'
            $btnRefreshPreview.Location = New-Object System.Drawing.Point(840, 7)
            $btnRefreshPreview.Size = New-Object System.Drawing.Size(120, 28)
            $btnRefreshPreview.BackColor = $script:Theme.PanelAlt
            $btnRefreshPreview.ForeColor = $script:Theme.Text
            $previewToolbar.Controls.Add($btnRefreshPreview)

            $btnFocusPreview = New-Object System.Windows.Forms.Button
            $btnFocusPreview.Text = 'Focus Preview'
            $btnFocusPreview.Location = New-Object System.Drawing.Point(970, 7)
            $btnFocusPreview.Size = New-Object System.Drawing.Size(110, 28)
            $btnFocusPreview.BackColor = $script:Theme.PanelAlt
            $btnFocusPreview.ForeColor = $script:Theme.Text
            $previewToolbar.Controls.Add($btnFocusPreview)

            $btnRefreshStatus = New-Object System.Windows.Forms.Button
            $btnRefreshStatus.Text = 'Refresh Status'
            $btnRefreshStatus.Location = New-Object System.Drawing.Point(1090, 7)
            $btnRefreshStatus.Size = New-Object System.Drawing.Size(110, 28)
            $btnRefreshStatus.BackColor = $script:Theme.PanelAlt
            $btnRefreshStatus.ForeColor = $script:Theme.Text
            $previewToolbar.Controls.Add($btnRefreshStatus)

            $previewSplit = New-Object System.Windows.Forms.SplitContainer
            $previewSplit.Dock = 'Fill'
            $previewSplit.Orientation = 'Horizontal'
            $previewSplit.SplitterDistance = 520
            $previewPanel.Controls.Add($previewSplit)

            $previewTabs = New-Object System.Windows.Forms.TabControl
            $previewTabs.Dock = 'Fill'
            $previewSplit.Panel1.Controls.Add($previewTabs)

            $renderTab = New-Object System.Windows.Forms.TabPage
            $renderTab.Text = 'HTML'
            $previewTabs.TabPages.Add($renderTab)

            $browser = New-Object System.Windows.Forms.WebBrowser
            $browser.Dock = 'Fill'
            $browser.IsWebBrowserContextMenuEnabled = $false
            $browser.WebBrowserShortcutsEnabled = $false
            $browser.ScriptErrorsSuppressed = $true
            $renderTab.Controls.Add($browser)

            $rawTab = New-Object System.Windows.Forms.TabPage
            $rawTab.Text = 'Markdown/Text'
            $previewTabs.TabPages.Add($rawTab)

            $rawBox = New-Object System.Windows.Forms.TextBox
            $rawBox.Dock = 'Fill'
            $rawBox.Multiline = $true
            $rawBox.ReadOnly = $false
            $rawBox.ScrollBars = 'Both'
            $rawBox.WordWrap = $false
            $rawBox.BackColor = $script:Theme.Surface
            $rawBox.ForeColor = $script:Theme.Text
            $rawBox.Font = New-Object System.Drawing.Font('Consolas', 10)
            $rawTab.Controls.Add($rawBox)

            $statusTab = New-Object System.Windows.Forms.TabPage
            $statusTab.Text = 'Grounding'
            $previewTabs.TabPages.Add($statusTab)

            $statusBrowser = New-Object System.Windows.Forms.WebBrowser
            $statusBrowser.Dock = 'Fill'
            $statusBrowser.IsWebBrowserContextMenuEnabled = $false
            $statusBrowser.WebBrowserShortcutsEnabled = $false
            $statusBrowser.ScriptErrorsSuppressed = $true
            $statusTab.Controls.Add($statusBrowser)

            $referenceTabs = New-Object System.Windows.Forms.TabControl
            $referenceTabs.Dock = 'Fill'
            $previewSplit.Panel2.Controls.Add($referenceTabs)

            $referencesTab = New-Object System.Windows.Forms.TabPage
            $referencesTab.Text = 'References'
            $referenceTabs.TabPages.Add($referencesTab)

            $referenceView = New-Object System.Windows.Forms.ListView
            $referenceView.Dock = 'Fill'
            $referenceView.View = 'Details'
            $referenceView.FullRowSelect = $true
            $referenceView.HeaderStyle = 'Clickable'
            $referenceView.MultiSelect = $false
            $referenceView.BackColor = $script:Theme.Surface
            $referenceView.ForeColor = $script:Theme.Text
            [void]$referenceView.Columns.Add('Path', 320)
            [void]$referenceView.Columns.Add('Lines', 70)
            [void]$referenceView.Columns.Add('Kind', 90)
            [void]$referenceView.Columns.Add('Confidence', 90)
            Enable-ListViewSorting -ListView $referenceView
            $referencesTab.Controls.Add($referenceView)

            $detailsTab = New-Object System.Windows.Forms.TabPage
            $detailsTab.Text = 'Selection Details'
            $referenceTabs.TabPages.Add($detailsTab)

            $detailBox = New-Object System.Windows.Forms.TextBox
            $detailBox.Dock = 'Fill'
            $detailBox.Multiline = $true
            $detailBox.ReadOnly = $true
            $detailBox.ScrollBars = 'Both'
            $detailBox.WordWrap = $false
            $detailBox.BackColor = $script:Theme.Surface
            $detailBox.ForeColor = $script:Theme.Text
            $detailBox.Font = New-Object System.Drawing.Font('Consolas', 9)
            $detailsTab.Controls.Add($detailBox)

            $phaseItems = New-Object System.Collections.Generic.List[object]
            foreach ($phaseName in @($Instance.State.completed)) { $phaseItems.Add([pscustomobject]@{ Status = 'Done'; Phase = [string]$phaseName; Detail = 'Completed phase' }) }
            if ($Instance.State.phase) { $phaseItems.Add([pscustomobject]@{ Status = 'Current'; Phase = [string]$Instance.State.phase; Detail = 'Current phase' }) }
            $agentSummary = @($records | Group-Object Agent | Sort-Object Name | ForEach-Object {
                [pscustomobject]@{
                    Agent = if ([string]::IsNullOrWhiteSpace([string]$_.Name)) { '(unknown)' } else { [string]$_.Name }
                    Statements = $_.Count
                    Artifacts = @($_.Group | ForEach-Object { $_.Artifact } | Where-Object { $_ } | Sort-Object -Unique).Count
                    Rules = @($_.Group | ForEach-Object { $_.BusinessRules } | ForEach-Object { $_ }).Count
                }
            })
            $currentSelection = [pscustomobject]@{ Path = $null; Rule = $null; Conflict = $null }
            $selectedDbQuery = [pscustomobject]@{ Value = $null }
            $selectedReference = [pscustomobject]@{ Value = $null }

            $setSourceReferences = {
                param([object[]]$Sources, [string]$DetailText)
                $referenceView.Items.Clear()
                foreach ($source in @($Sources)) {
                    $resolvedPath = if ($source.PSObject.Properties['path']) { Get-ResolvedInstancePath -Instance $Instance -Path ([string]$source.path) } else { $null }
                    $lineStart = if ($source.PSObject.Properties['line_start']) { [int]$source.line_start } else { 0 }
                    $lineEnd = if ($source.PSObject.Properties['line_end']) { [int]$source.line_end } else { 0 }
                    $lineText = if ($lineStart -gt 0 -and $lineEnd -ge $lineStart) { '{0}-{1}' -f $lineStart, $lineEnd } elseif ($lineStart -gt 0) { [string]$lineStart } else { '' }
                    $displayPath = if ($resolvedPath) { $resolvedPath } elseif ($source.PSObject.Properties['path']) { [string]$source.path } else { '' }
                    $item = New-Object System.Windows.Forms.ListViewItem($displayPath)
                    [void]$item.SubItems.Add($lineText)
                    [void]$item.SubItems.Add((if ($source.PSObject.Properties['kind']) { [string]$source.kind } else { '' }))
                    [void]$item.SubItems.Add((if ($source.PSObject.Properties['confidence']) { [string]$source.confidence } else { '' }))
                    $item.Tag = [pscustomobject]@{ Path = $resolvedPath; Line = $lineStart; Source = $source }
                    [void]$referenceView.Items.Add($item)
                }
                $detailBox.Text = $DetailText
                if ($referenceView.Items.Count -gt 0) { $selectedReference.Value = $referenceView.Items[0].Tag } else { $selectedReference.Value = $null }
            }

            $showSelection = {
                param([string]$SelectionPath)
                $currentSelection.Path = $SelectionPath
                $currentSelection.Rule = $null
                $currentSelection.Conflict = $null
                $currentFileLabel.Text = if ($SelectionPath) { "Selected file: $SelectionPath" } else { 'Selected file: -' }
                $metadata = if ($SelectionPath -and $catalogByPath.ContainsKey($SelectionPath)) { $catalogByPath[$SelectionPath] } else { $null }
                if ($metadata) {
                    $metaLabel.Text = "Category: $($metadata.Category) | Sources: $($metadata.Sources.Count)"
                    & $setSourceReferences @($metadata.Sources) (@(
                        "Title: $($metadata.Title)",
                        "Category: $($metadata.Category)",
                        "Relative: $($metadata.RelativePath)",
                        "Sources: $($metadata.Sources.Count)",
                        "Source summary: $(Get-SourceSummaryText -Sources $metadata.Sources)"
                    ) -join [Environment]::NewLine)
                } else {
                    $metaLabel.Text = 'Category: - | Sources: -'
                    & $setSourceReferences @() ("Path: $SelectionPath")
                }
                if ($script:PreviewMode -eq 'Open Externally' -and $SelectionPath) {
                    Open-PathIfExists -Path $SelectionPath
                    $rawBox.Text = "Opened externally:`r`n$SelectionPath"
                    $browser.DocumentText = Convert-MarkdownToHtml -Markdown ("# External Preview`n`nOpened through the OS:`n`n- {0}" -f $SelectionPath) -Title 'External Preview'
                    return
                }
                if ($metadata) {
                    $content = Get-FileContent -Path $SelectionPath
                    $rawBox.Text = $content
                    $title = Split-Path -Leaf $SelectionPath
                    if ([System.IO.Path]::GetExtension($SelectionPath).ToLowerInvariant() -eq '.md') {
                        $browser.DocumentText = Convert-MarkdownToHtml -Markdown $content -Title $title -Metadata $metadata
                    } else {
                        Update-MarkdownPreview -Browser $browser -RawBox $rawBox -Path $SelectionPath
                    }
                } else {
                    Update-MarkdownPreview -Browser $browser -RawBox $rawBox -Path $SelectionPath
                }
            }

            $showRuleSelection = {
                param([object]$RuleRow)
                if (-not $RuleRow) { return }
                $currentSelection.Rule = $RuleRow
                $currentSelection.Conflict = $null
                $targetPath = if ($RuleRow.SourceDocumentPath -and (Test-Path -LiteralPath $RuleRow.SourceDocumentPath)) { $RuleRow.SourceDocumentPath } elseif ($RuleRow.Artifact) { Get-ResolvedInstancePath -Instance $Instance -Path $RuleRow.Artifact } else { $null }
                if ($targetPath -and (Test-Path -LiteralPath $targetPath)) { & $showSelection $targetPath } else {
                    $currentFileLabel.Text = 'Selected file: -'
                    $metaLabel.Text = "Rule: $($RuleRow.RuleId) | Sources: $(@($RuleRow.Sources).Count)"
                    $browser.DocumentText = Convert-MarkdownToHtml -Markdown ("# Rule $($RuleRow.RuleId)`n`nNo document file could be resolved for this rule.") -Title $RuleRow.RuleId
                    $rawBox.Text = $RuleRow.Statement
                }
                & $setSourceReferences @($RuleRow.Sources) (@(
                    "Rule ID: $($RuleRow.RuleId)",
                    "Agent: $($RuleRow.Agent)",
                    "Artifact: $($RuleRow.Artifact)",
                    "Confidence: $($RuleRow.Confidence)",
                    "Source document: $($RuleRow.SourceDocument)",
                    "Rationale: $($RuleRow.Rationale)",
                    "Statement: $($RuleRow.Statement)",
                    "Block: $($RuleRow.BlockId)"
                ) -join [Environment]::NewLine)
            }

            $showConflictSelection = {
                param([object]$ConflictRow)
                $currentSelection.Conflict = $ConflictRow
                if (-not $ConflictRow) { $conflictPromptBox.Text = ''; $btnCopyConflictPrompt.Enabled = $false; return }
                $conflictPromptBox.Text = $ConflictRow.ResolutionPrompt
                $btnCopyConflictPrompt.Enabled = $true
                $allSources = @($ConflictRow.Entries | ForEach-Object { $_.Sources } | ForEach-Object { $_ })
                & $setSourceReferences $allSources (@(
                    "Rule ID: $($ConflictRow.RuleId)",
                    "Entries: $($ConflictRow.EntryCount)",
                    "Confidence set: $($ConflictRow.ConfidenceSet)",
                    "Documents: $($ConflictRow.DocumentSet)",
                    '',
                    $ConflictRow.ResolutionPrompt
                ) -join [Environment]::NewLine)
                $browser.DocumentText = Convert-MarkdownToHtml -Markdown ("# Conflict $($ConflictRow.RuleId)`n`n````text`n$($ConflictRow.ResolutionPrompt)`n````") -Title $ConflictRow.RuleId
                $rawBox.Text = $ConflictRow.ResolutionPrompt
            }

            $setDatabaseQueryDetails = {
                param([object]$QueryItem)
                $selectedDbQuery.Value = $QueryItem
                if (-not $QueryItem) { $queryDetailsBox.Text = 'No query selected.'; $btnCopyQueryId.Enabled = $false; $btnCopyCancel.Enabled = $false; return }
                $query = $QueryItem.Query
                $queryDetailsBox.Text = @(
                    "Bundle: $($QueryItem.BundleId)",
                    "Query ID: $([string]$query.query_id)",
                    "Phase: $([string]$query.phase)",
                    "Session ID: $([string]$query.session_id)",
                    "Executed: $([string]$query.executed)",
                    "Cancel: $([string]$query.cancel_command)",
                    "Explain: $([string]$query.explain_summary)"
                ) -join [Environment]::NewLine
                $btnCopyQueryId.Enabled = -not [string]::IsNullOrWhiteSpace([string]$query.query_id)
                $btnCopyCancel.Enabled = -not [string]::IsNullOrWhiteSpace([string]$query.cancel_command)
            }

            $refreshDatabaseGroundingPanel = {
                $schemaGrounding = Read-JsonSafe -Path $databaseGroundingPaths.SchemaGroundingPath
                $queryGrounding = Read-JsonSafe -Path $databaseGroundingPaths.QueryGroundingPath
                $dbServerBox.Text = if ($queryGrounding -and $queryGrounding.server_alias) { [string]$queryGrounding.server_alias } elseif ($schemaGrounding -and $schemaGrounding.server_alias) { [string]$schemaGrounding.server_alias } else { '-' }
                $dbNameBox.Text = if ($queryGrounding -and $queryGrounding.database_name) { [string]$queryGrounding.database_name } elseif ($schemaGrounding -and $schemaGrounding.database_name) { [string]$schemaGrounding.database_name } else { '-' }
                $dbEngineBox.Text = if ($queryGrounding -and $queryGrounding.engine) { [string]$queryGrounding.engine } elseif ($schemaGrounding -and $schemaGrounding.engine) { [string]$schemaGrounding.engine } else { '-' }
                $dbApprovalBox.Text = if ($queryGrounding -and $queryGrounding.approval_status) { [string]$queryGrounding.approval_status } else { '-' }
                $dbPilotBox.Text = if ($queryGrounding -and $queryGrounding.pilot_table) { ((@([string]$queryGrounding.pilot_table.schema, [string]$queryGrounding.pilot_table.table) | Where-Object { $_ }) -join '.') } else { '-' }
                $dbAccessBox.Text = if ($queryGrounding -and $queryGrounding.access_source) { [string]$queryGrounding.access_source } elseif ($schemaGrounding -and $schemaGrounding.safe_connection_reference) { [string]$schemaGrounding.safe_connection_reference } else { '-' }
                $queryList.Items.Clear()
                foreach ($bundle in @($queryGrounding.bundles)) {
                    foreach ($query in @($bundle.queries)) {
                        $item = New-Object System.Windows.Forms.ListViewItem([string]$query.query_id)
                        [void]$item.SubItems.Add([string]$query.phase)
                        [void]$item.SubItems.Add((if ($query.executed) { 'Yes' } else { 'No' }))
                        $item.Tag = [pscustomobject]@{ BundleId = [string]$bundle.bundle_id; Query = $query }
                        [void]$queryList.Items.Add($item)
                    }
                }
                if ($queryList.Items.Count -gt 0) { & $setDatabaseQueryDetails $queryList.Items[0].Tag } else { & $setDatabaseQueryDetails $null }
            }

            $bindDocumentList = {
                $filter = $txtDocumentFilter.Text.Trim()
                $categoryFilter = [string]$cmbDocumentCategory.SelectedItem
                $documentView.Items.Clear()
                foreach ($doc in @($catalog | Where-Object {
                    ([string]::IsNullOrWhiteSpace($filter) -or $_.Title -like "*$filter*" -or $_.RelativePath -like "*$filter*") -and (($categoryFilter -eq 'All Categories') -or ([string]$_.Category -eq $categoryFilter))
                })) {
                    $item = New-Object System.Windows.Forms.ListViewItem([string]$doc.Category)
                    [void]$item.SubItems.Add([string]$doc.Title)
                    [void]$item.SubItems.Add([string]$doc.RelativePath)
                    [void]$item.SubItems.Add([string]@($doc.Sources).Count)
                    $item.Tag = $doc
                    [void]$documentView.Items.Add($item)
                }
            }

            $bindRuleList = {
                $filter = $txtRuleFilter.Text.Trim()
                $confidenceFilter = [string]$cmbRuleConfidence.SelectedItem
                $ruleView.Items.Clear()
                foreach ($rule in @($ruleCatalog | Where-Object {
                    ([string]::IsNullOrWhiteSpace($filter) -or $_.RuleId -like "*$filter*" -or $_.Statement -like "*$filter*" -or $_.SourceDocument -like "*$filter*" -or $_.Artifact -like "*$filter*") -and (($confidenceFilter -eq 'All Confidence') -or ([string]$_.Confidence -eq $confidenceFilter))
                })) {
                    $item = New-Object System.Windows.Forms.ListViewItem([string]$rule.RuleId)
                    [void]$item.SubItems.Add([string]$rule.Confidence)
                    [void]$item.SubItems.Add([string]$rule.Agent)
                    [void]$item.SubItems.Add([string]$rule.Artifact)
                    [void]$item.SubItems.Add([string]$rule.SourceDocument)
                    [void]$item.SubItems.Add([string]$rule.Statement)
                    $item.Tag = $rule
                    [void]$ruleView.Items.Add($item)
                }
            }

            $bindConflictList = {
                $conflictView.Items.Clear()
                foreach ($conflict in @($ruleConflicts)) {
                    $item = New-Object System.Windows.Forms.ListViewItem([string]$conflict.RuleId)
                    [void]$item.SubItems.Add([string]$conflict.EntryCount)
                    [void]$item.SubItems.Add([string]$conflict.ConfidenceSet)
                    [void]$item.SubItems.Add([string]$conflict.DocumentSet)
                    [void]$item.SubItems.Add([string]$conflict.Summary)
                    $item.Tag = $conflict
                    [void]$conflictView.Items.Add($item)
                }
            }

            $refreshSummary = {
                $scriptStatus = Get-ProvenanceValidation -Instance $Instance -Catalog $catalog
                $databaseStatus = Get-DatabaseGroundingValidation -Instance $Instance
                $summaryLabel.Text = @(
                    "Project root: $($Instance.Root)",
                    "Current phase: $($Instance.State.phase)",
                    "Output folder: $($Instance.OutputFolder)",
                    "Completed phases: $((@($Instance.State.completed) -join ', '))",
                    "Tasks complete: $completedTaskCount / $($taskList.Count)",
                    "Documents in gallery: $($catalog.Count)",
                    "Provenance records: $($scriptStatus.RecordCount) | Rules: $($ruleCatalog.Count) | Conflicts: $($ruleConflicts.Count)",
                    "DB grounding: $($databaseStatus.Level) | Active tables: $($databaseStatus.ActiveTables) | Query approval: $($databaseStatus.ApprovalStatus)"
                ) -join [Environment]::NewLine
                $snapshotList.Items.Clear()
                foreach ($row in @(
                    [pscustomobject]@{ Area = 'Documents'; Value = $catalog.Count; Detail = 'Cataloged markdown and reports' },
                    [pscustomobject]@{ Area = 'Rules'; Value = $ruleCatalog.Count; Detail = 'Every provenance-linked business rule' },
                    [pscustomobject]@{ Area = 'Conflicts'; Value = $ruleConflicts.Count; Detail = 'Rules with conflicting statements' },
                    [pscustomobject]@{ Area = 'Agents'; Value = $agentSummary.Count; Detail = 'Agents observed in provenance' },
                    [pscustomobject]@{ Area = 'Tracked files'; Value = @((Get-TrackedFiles -State $Instance.State)).Count; Detail = 'Checkpoint and tracked files' },
                    [pscustomobject]@{ Area = 'DB queries'; Value = $databaseStatus.BundleCount; Detail = 'Grounding query bundles' }
                )) {
                    $item = New-Object System.Windows.Forms.ListViewItem([string]$row.Area)
                    [void]$item.SubItems.Add([string]$row.Value)
                    [void]$item.SubItems.Add([string]$row.Detail)
                    [void]$snapshotList.Items.Add($item)
                }
                $phaseView.Items.Clear()
                foreach ($phase in @($phaseItems)) {
                    $item = New-Object System.Windows.Forms.ListViewItem([string]$phase.Status)
                    [void]$item.SubItems.Add([string]$phase.Phase)
                    [void]$item.SubItems.Add([string]$phase.Detail)
                    [void]$phaseView.Items.Add($item)
                }
                $taskView.Items.Clear()
                foreach ($task in @($taskList)) {
                    $item = New-Object System.Windows.Forms.ListViewItem((if ($task.Done) { 'Yes' } else { 'No' }))
                    [void]$item.SubItems.Add((if ($null -ne $task.Text) { [string]$task.Text } else { '' }))
                    if ($task.Done) { $item.ForeColor = $script:Theme.Success }
                    [void]$taskView.Items.Add($item)
                }
                $agentView.Items.Clear()
                foreach ($agent in @($agentSummary)) {
                    $item = New-Object System.Windows.Forms.ListViewItem([string]$agent.Agent)
                    [void]$item.SubItems.Add([string]$agent.Statements)
                    [void]$item.SubItems.Add([string]$agent.Artifacts)
                    [void]$item.SubItems.Add([string]$agent.Rules)
                    [void]$agentView.Items.Add($item)
                }
                $statusBrowser.DocumentText = Convert-MarkdownToHtml -Markdown (Convert-GroundingStatusToMarkdown -Provenance $scriptStatus -DatabaseGrounding $databaseStatus) -Title 'Grounding Status'
                & $refreshDatabaseGroundingPanel
                & $bindDocumentList
                & $bindRuleList
                & $bindConflictList
            }

            $tree.Nodes.Clear()
            $reversaRoot = Join-Path $Instance.Root '.reversa'
            if (Test-Path -LiteralPath $reversaRoot) { $rootNode = New-TreeNode -Text '.reversa' -Path $reversaRoot; Add-DirectoryToTree -ParentNode $rootNode -DirectoryPath $reversaRoot; [void]$tree.Nodes.Add($rootNode) }
            if (Test-Path -LiteralPath $Instance.OutputPath) { $outputNode = New-TreeNode -Text $Instance.OutputFolder -Path $Instance.OutputPath; Add-DirectoryToTree -ParentNode $outputNode -DirectoryPath $Instance.OutputPath; [void]$tree.Nodes.Add($outputNode) }
            foreach ($relativeFile in @(Get-TrackedFiles -State $Instance.State)) {
                if (-not $trackedNode) { $trackedNode = New-TreeNode -Text 'Checkpoint Files' -Path '' }
                $fullPath = Join-Path $Instance.Root ($relativeFile -replace '/', '\')
                [void]$trackedNode.Nodes.Add((New-TreeNode -Text "$(Split-Path -Leaf $relativeFile)  [$relativeFile]" -Path $fullPath -IsFile $true))
            }
            if ($trackedNode -and $trackedNode.Nodes.Count -gt 0) { [void]$tree.Nodes.Add($trackedNode) }
            foreach ($pathItem in @(
                [pscustomobject]@{ Label = 'PDD Short'; Path = $traceabilityPaths.PddPath },
                [pscustomobject]@{ Label = 'PDD Extended'; Path = $traceabilityPaths.ExtendedPddPath },
                [pscustomobject]@{ Label = 'Provenance Settings'; Path = $traceabilityPaths.SettingsPath },
                [pscustomobject]@{ Label = 'Statement Provenance'; Path = $traceabilityPaths.StatementPath },
                [pscustomobject]@{ Label = 'Business Rules Index'; Path = $traceabilityPaths.BusinessIndexPath }
            )) { if (Test-Path -LiteralPath $pathItem.Path) { if (-not $traceNode) { $traceNode = New-TreeNode -Text 'Provenance Artifacts' -Path '' }; [void]$traceNode.Nodes.Add((New-TreeNode -Text $pathItem.Label -Path $pathItem.Path -IsFile $true)) } }
            if ($traceNode -and $traceNode.Nodes.Count -gt 0) { [void]$tree.Nodes.Add($traceNode) }
            foreach ($pathItem in @(
                [pscustomobject]@{ Label = 'Schema Grounding JSON'; Path = $databaseGroundingPaths.SchemaGroundingPath },
                [pscustomobject]@{ Label = 'Schema Grounding Schema'; Path = $databaseGroundingPaths.SchemaGroundingSchemaPath },
                [pscustomobject]@{ Label = 'Schema Grounding Example'; Path = $databaseGroundingPaths.SchemaGroundingExamplePath },
                [pscustomobject]@{ Label = 'Query Grounding JSON'; Path = $databaseGroundingPaths.QueryGroundingPath },
                [pscustomobject]@{ Label = 'Query Grounding Schema'; Path = $databaseGroundingPaths.QueryGroundingSchemaPath },
                [pscustomobject]@{ Label = 'Query Grounding Example'; Path = $databaseGroundingPaths.QueryGroundingExamplePath },
                [pscustomobject]@{ Label = 'Schema Layer'; Path = $databaseGroundingPaths.SchemaLayerPath },
                [pscustomobject]@{ Label = 'Table Activity'; Path = $databaseGroundingPaths.TableActivityPath },
                [pscustomobject]@{ Label = 'Inactive Schema'; Path = $databaseGroundingPaths.InactiveSchemaPath },
                [pscustomobject]@{ Label = 'Query Approval'; Path = $databaseGroundingPaths.QueryApprovalPath }
            )) { if (Test-Path -LiteralPath $pathItem.Path) { if (-not $dbNode) { $dbNode = New-TreeNode -Text 'Database Grounding Artifacts' -Path '' }; [void]$dbNode.Nodes.Add((New-TreeNode -Text $pathItem.Label -Path $pathItem.Path -IsFile $true)) } }
            if ($dbNode -and $dbNode.Nodes.Count -gt 0) { [void]$tree.Nodes.Add($dbNode) }
            $tree.ExpandAll()

            $btnOpenProject.Add_Click({ Open-PathIfExists -Path $Instance.Root })
            $btnOpenOutput.Add_Click({ Open-PathIfExists -Path $Instance.OutputPath })
            $btnOpenTraceability.Add_Click({ Open-PathIfExists -Path (Join-Path $Instance.OutputPath 'traceability') })
            $btnOpenPlan.Add_Click({ Open-PathIfExists -Path $Instance.PlanPath })
            $btnOpenReports.Add_Click({ Open-PathIfExists -Path (Join-Path (Join-Path $Instance.OutputPath 'traceability') 'versions\reports') })
            $btnTabRefresh.Add_Click({ & $refreshSummary })
            $btnRefreshStatus.Add_Click({ & $refreshSummary })
            $cmbReferenceOpenMode.Add_SelectedIndexChanged({ $script:ReferenceOpenMode = [string]$cmbReferenceOpenMode.SelectedItem })
            $btnOpenCurrent.Add_Click({ if ($currentSelection.Path) { Open-ReferenceTarget -Path $currentSelection.Path -Mode $script:ReferenceOpenMode } })
            $btnFocusPreview.Add_Click({ $splitRight.Panel1Collapsed = -not $splitRight.Panel1Collapsed; $btnFocusPreview.Text = if ($splitRight.Panel1Collapsed) { 'Show Navigator' } else { 'Focus Preview' } })
            $tree.Add_AfterSelect({ if ($this.SelectedNode -and $this.SelectedNode.Tag -and $this.SelectedNode.Tag.IsFile) { & $showSelection $this.SelectedNode.Tag.Path } })
            $documentView.Add_SelectedIndexChanged({ if ($this.SelectedItems.Count -gt 0 -and $this.SelectedItems[0].Tag) { & $showSelection $this.SelectedItems[0].Tag.FullPath } })
            $ruleView.Add_SelectedIndexChanged({ if ($this.SelectedItems.Count -gt 0) { & $showRuleSelection $this.SelectedItems[0].Tag } })
            $conflictView.Add_SelectedIndexChanged({ if ($this.SelectedItems.Count -gt 0) { & $showConflictSelection $this.SelectedItems[0].Tag } })
            $referenceView.Add_SelectedIndexChanged({ if ($this.SelectedItems.Count -gt 0) { $selectedReference.Value = $this.SelectedItems[0].Tag } })
            $referenceView.Add_DoubleClick({ if ($selectedReference.Value -and $selectedReference.Value.Path) { Open-ReferenceTarget -Path $selectedReference.Value.Path -Line ([int]$selectedReference.Value.Line) -Mode $script:ReferenceOpenMode } })
            $btnCopyConflictPrompt.Add_Click({ if ($currentSelection.Conflict) { [System.Windows.Forms.Clipboard]::SetText([string]$currentSelection.Conflict.ResolutionPrompt) } })
            $queryList.Add_SelectedIndexChanged({ if ($this.SelectedItems.Count -gt 0) { & $setDatabaseQueryDetails $this.SelectedItems[0].Tag } })
            $btnCopyQueryId.Add_Click({ if ($selectedDbQuery.Value -and $selectedDbQuery.Value.Query -and $selectedDbQuery.Value.Query.query_id) { [System.Windows.Forms.Clipboard]::SetText([string]$selectedDbQuery.Value.Query.query_id) } })
            $btnCopyCancel.Add_Click({ if ($selectedDbQuery.Value -and $selectedDbQuery.Value.Query -and $selectedDbQuery.Value.Query.cancel_command) { [System.Windows.Forms.Clipboard]::SetText([string]$selectedDbQuery.Value.Query.cancel_command) } })
            $txtDocumentFilter.Add_TextChanged({ & $bindDocumentList })
            $cmbDocumentCategory.Add_SelectedIndexChanged({ & $bindDocumentList })
            $txtRuleFilter.Add_TextChanged({ & $bindRuleList })
            $cmbRuleConfidence.Add_SelectedIndexChanged({ & $bindRuleList })
            $btnSaveFile.Add_Click({
                if (-not $currentSelection.Path) { [System.Windows.Forms.MessageBox]::Show('Select a text or markdown file before saving.', 'No File Selected', 'OK', 'Information') | Out-Null; return }
                try {
                    Set-Content -LiteralPath $currentSelection.Path -Value $rawBox.Text -Encoding UTF8
                    if ($catalogByPath.ContainsKey($currentSelection.Path)) {
                        $updatedContent = Get-FileContent -Path $currentSelection.Path
                        $updatedEntry = $catalogByPath[$currentSelection.Path]
                        $updatedEntry.Sources = @(Get-MarkdownSources -Instance $Instance -RelativePath $updatedEntry.RelativePath -Content $updatedContent)
                        $updatedEntry.Title = ((($updatedContent -split "`r?`n") | Where-Object { $_ -match '^#' } | Select-Object -First 1) -replace '^#+\s*', '').Trim()
                        if (-not $updatedEntry.Title) { $updatedEntry.Title = [System.IO.Path]::GetFileNameWithoutExtension($currentSelection.Path) }
                        Save-MarkdownCatalog -Instance $Instance -Catalog $catalog | Out-Null
                    }
                    & $refreshSummary
                    & $showSelection $currentSelection.Path
                } catch {
                    [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Save Failed', 'OK', 'Error') | Out-Null
                }
            })
            $btnRefreshPreview.Add_Click({ if ($currentSelection.Conflict) { & $showConflictSelection $currentSelection.Conflict } elseif ($currentSelection.Rule) { & $showRuleSelection $currentSelection.Rule } else { & $showSelection $currentSelection.Path } })

            $script:ReferenceOpenMode = 'VS Code'
            & $refreshSummary
            if ($documentView.Items.Count -gt 0) { & $showSelection $documentView.Items[0].Tag.FullPath } elseif ($tree.Nodes.Count -gt 0) { foreach ($rootNode in $tree.Nodes) { foreach ($child in $rootNode.Nodes) { if ($child.Tag -and $child.Tag.IsFile) { & $showSelection $child.Tag.Path; break } } } } else { $browser.DocumentText = Convert-MarkdownToHtml -Markdown "# $($Instance.Name)`n`nSelect a document, rule, conflict, or file to preview it." -Title $Instance.Name; $rawBox.Text = '' }
            $ActiveLabel.Text = "Active instance: $($Instance.Name)"
            return $tabPage
    $state.traceability | Add-Member -NotePropertyName statement_provenance_file -NotePropertyValue '.reversa/_config/statement-provenance.jsonl' -Force
    $state.traceability | Add-Member -NotePropertyName statement_provenance_schema_file -NotePropertyValue '.reversa/_config/statement-provenance.schema.json' -Force
    $state.traceability | Add-Member -NotePropertyName statement_provenance_example_file -NotePropertyValue '.reversa/_config/statement-provenance.example.jsonl' -Force
    $state.traceability | Add-Member -NotePropertyName business_rules_index_file -NotePropertyValue "$outputFolder/traceability/business-rules-index.md" -Force
    Set-Content -LiteralPath $statePath -Value ($state | ConvertTo-Json -Depth 20) -Encoding UTF8

    $settingsPath = Join-Path $TargetFolder '.reversa\_config\provenance-settings.json'
    if (Test-Path -LiteralPath $settingsPath) {
        $settings = Read-JsonSafe -Path $settingsPath
        if ($settings) {
            $settings | Add-Member -NotePropertyName enabled -NotePropertyValue $Enabled -Force
            $settings | Add-Member -NotePropertyName instruction_file -NotePropertyValue '.reversa/context/pdd_short.md' -Force
            $settings | Add-Member -NotePropertyName extended_instruction_file -NotePropertyValue '.reversa/context/pdd_instructions.md' -Force
            $settings | Add-Member -NotePropertyName statement_provenance_file -NotePropertyValue '.reversa/_config/statement-provenance.jsonl' -Force
            $settings | Add-Member -NotePropertyName statement_provenance_schema_file -NotePropertyValue '.reversa/_config/statement-provenance.schema.json' -Force
            $settings | Add-Member -NotePropertyName statement_provenance_example_file -NotePropertyValue '.reversa/_config/statement-provenance.example.jsonl' -Force
            $settings | Add-Member -NotePropertyName business_rules_index_file -NotePropertyValue "$outputFolder/traceability/business-rules-index.md" -Force
            $settings | Add-Member -NotePropertyName confidence_scale -NotePropertyValue @(
                [pscustomobject]@{ id = 'confirmed'; label = '🟢 CONFIRMED'; aliases = @('🟢', 'confirmed', 'green', 'high'); requires_sources = $true },
                [pscustomobject]@{ id = 'inferred'; label = '🟡 INFERRED'; aliases = @('🟡', 'inferred', 'supported', 'yellow', 'medium'); requires_sources = $false },
                [pscustomobject]@{ id = 'gap'; label = '🔴 GAP'; aliases = @('🔴', 'gap', 'speculative', 'red', 'low'); requires_sources = $false }
            ) -Force
            Set-Content -LiteralPath $settingsPath -Value ($settings | ConvertTo-Json -Depth 20) -Encoding UTF8
        }
    }

    $configPath = Join-Path $TargetFolder '.reversa\config.toml'
    if (Test-Path -LiteralPath $configPath) {
        $content = Get-Content -LiteralPath $configPath -Raw
        $traceabilitySection = @(
            '[traceability]',
            "enable_provenance_indexing = $($Enabled.ToString().ToLowerInvariant())",
            'business_rules_instruction = ".reversa/context/pdd_short.md"',
            'extended_business_rules_instruction = ".reversa/context/pdd_instructions.md"',
            'statement_provenance_file = ".reversa/_config/statement-provenance.jsonl"',
            'statement_provenance_schema_file = ".reversa/_config/statement-provenance.schema.json"',
            'statement_provenance_example_file = ".reversa/_config/statement-provenance.example.jsonl"',
            "business_rules_index_file = `"$outputFolder/traceability/business-rules-index.md`""
        ) -join "`r`n"

        if ($content -match '(?ms)^\[traceability\].*?(?=^\[[^\]]+\]|\z)') {
            $content = [regex]::Replace($content, '(?ms)^\[traceability\].*?(?=^\[[^\]]+\]|\z)', $traceabilitySection)
        } else {
            $content = $content.TrimEnd() + "`r`n`r`n" + $traceabilitySection + "`r`n"
        }

        Set-Content -LiteralPath $configPath -Value $content -Encoding UTF8
    }
}

function Get-PowerShellExecutable {
    $currentProcessPath = (Get-Process -Id $PID -ErrorAction SilentlyContinue).Path
    if ($currentProcessPath -and (Test-Path -LiteralPath $currentProcessPath)) {
        return $currentProcessPath
    }

    foreach ($candidate in @(
        (Join-Path $PSHOME 'pwsh.exe'),
        (Join-Path $PSHOME 'powershell.exe')
    )) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    return 'pwsh'
}

function Get-TraceabilityToolkitDefaultSource {
    $candidates = @(
        (Join-Path $PSScriptRoot 'UTREx_SIF_VRF-develop\_reversa_sdd\traceability'),
        (Join-Path $PSScriptRoot 'UTRExSubmissionQueue-develop\_reversa_sdd\traceability')
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    return ''
}

function Get-TraceabilityToolkitTargetFolder {
    param([string]$TargetFolder)

    if ([string]::IsNullOrWhiteSpace($TargetFolder)) {
        return ''
    }

    $defaults = Get-TargetDefaults -TargetFolder $TargetFolder
    $outputFolder = if ($defaults -and $defaults.OutputFolder) { [string]$defaults.OutputFolder } else { '_reversa_sdd' }
    return Join-Path (Join-Path $TargetFolder ($outputFolder -replace '/', '\')) 'traceability'
}

function Get-TraceabilityToolkitPackageItems {
    param([string]$SourceFolder)

    if (-not (Test-Path -LiteralPath $SourceFolder)) {
        return @()
    }

    $includeNames = @(
        'TRACEABILITY-RERUN-PLAYBOOK.md',
        'TRACEABILITY-STARTER-KIT.md',
        'README-SCHEMA-ARTIFACTS.md'
    )

    return @(
        Get-ChildItem -LiteralPath $SourceFolder -File -ErrorAction SilentlyContinue |
            Where-Object {
                $_.Extension -eq '.ps1' -or $includeNames -contains $_.Name
            } |
            Sort-Object Name
    )
}

function Install-TraceabilityToolkit {
    param(
        [string]$SourceFolder,
        [string]$TargetFolder
    )

    if (-not (Test-Path -LiteralPath $SourceFolder)) {
        throw 'Select a valid traceability toolkit source folder.'
    }

    if (-not (Test-Path -LiteralPath $TargetFolder)) {
        throw 'Select a valid target repository folder.'
    }

    $destinationFolder = Get-TraceabilityToolkitTargetFolder -TargetFolder $TargetFolder
    if ([string]::IsNullOrWhiteSpace($destinationFolder)) {
        throw 'Unable to resolve the target traceability folder.'
    }

    $packageItems = @(Get-TraceabilityToolkitPackageItems -SourceFolder $SourceFolder)
    if ($packageItems.Count -eq 0) {
        throw 'No toolkit files were found in the selected source folder.'
    }

    if (-not (Test-Path -LiteralPath $destinationFolder)) {
        New-Item -ItemType Directory -Path $destinationFolder -Force | Out-Null
    }

    $backupFolder = Join-Path $destinationFolder ('.gui-backups\traceability-toolkit\' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    $overwritten = 0
    foreach ($item in $packageItems) {
        $destinationPath = Join-Path $destinationFolder $item.Name
        if (Test-Path -LiteralPath $destinationPath) {
            if (-not (Test-Path -LiteralPath $backupFolder)) {
                New-Item -ItemType Directory -Path $backupFolder -Force | Out-Null
            }

            Copy-Item -LiteralPath $destinationPath -Destination (Join-Path $backupFolder $item.Name) -Force
            $overwritten++
        }

        Copy-Item -LiteralPath $item.FullName -Destination $destinationPath -Force
    }

    return [pscustomobject]@{
        DestinationFolder = $destinationFolder
        InstalledCount = $packageItems.Count
        OverwrittenCount = $overwritten
        BackupFolder = if ($overwritten -gt 0) { $backupFolder } else { '' }
        InstalledFiles = @($packageItems | ForEach-Object { $_.Name })
    }
}

function Invoke-TraceabilityToolkitAction {
    param(
        [string]$TargetFolder,
        [string]$Action
    )

    $traceabilityFolder = Get-TraceabilityToolkitTargetFolder -TargetFolder $TargetFolder
    if (-not (Test-Path -LiteralPath $traceabilityFolder)) {
        throw 'Install the traceability toolkit before running toolkit actions.'
    }

    $actionMap = @{
        'Audit Provenance Setup' = @{
            Script = 'Audit-TraceabilityProvenanceSetup.ps1'
            Arguments = '-TraceabilityFolder "{0}"' -f $traceabilityFolder
        }
        'Build Versions Index' = @{
            Script = 'Build-TraceabilityVersionsIndex.ps1'
            Arguments = ''
        }
    }

    if (-not $actionMap.ContainsKey($Action)) {
        throw "Unsupported toolkit action: $Action"
    }

    $selectedAction = $actionMap[$Action]
    $scriptPath = Join-Path $traceabilityFolder $selectedAction.Script
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        throw "Toolkit script not found: $($selectedAction.Script)"
    }

    $arguments = @(
        '-NoProfile',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        ('"{0}"' -f $scriptPath)
    )
    if (-not [string]::IsNullOrWhiteSpace([string]$selectedAction.Arguments)) {
        $arguments += [string]$selectedAction.Arguments
    }

    return Invoke-ProcessCapture -FilePath (Get-PowerShellExecutable) -Arguments ($arguments -join ' ') -WorkingDirectory $traceabilityFolder
}

function Open-PathIfExists {
    param([string]$Path)

    if (-not [string]::IsNullOrWhiteSpace($Path) -and (Test-Path -LiteralPath $Path)) {
        Start-Process -FilePath $Path | Out-Null
    }

    function Open-PathInVSCode {
        param(
            [string]$Path,
            [int]$Line = 0
        )

        if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) {
            return
        }

        $target = if ($Line -gt 0) { '{0}:{1}' -f $Path, $Line } else { $Path }
        Invoke-ProcessCapture -FilePath 'cmd.exe' -Arguments ('/c start "" code -r -g "{0}"' -f $target) -WorkingDirectory (Split-Path -Parent $Path) | Out-Null
    }

    function Open-ReferenceTarget {
        param(
            [string]$Path,
            [int]$Line = 0,
            [string]$Mode = 'VS Code'
        )

        if ([string]::IsNullOrWhiteSpace($Path)) {
            return
        }

        if ($Mode -eq 'OS Default') {
            Open-PathIfExists -Path $Path
            return
        }

        Open-PathInVSCode -Path $Path -Line $Line
    }

    function Get-ResolvedInstancePath {
        param(
            [object]$Instance,
            [string]$Path
        )

        if ([string]::IsNullOrWhiteSpace($Path)) {
            return $null
        }

        if ([System.IO.Path]::IsPathRooted($Path)) {
            return $Path
        }

        return Join-Path $Instance.Root ($Path -replace '/', '\')
    }

    function Get-SourceSummaryText {
        param([object[]]$Sources)

        $parts = New-Object System.Collections.Generic.List[string]
        foreach ($source in @($Sources)) {
            $path = if ($source.PSObject.Properties['path']) { [string]$source.path } else { '' }
            $lineStart = if ($source.PSObject.Properties['line_start']) { [int]$source.line_start } else { 0 }
            $kind = if ($source.PSObject.Properties['kind']) { [string]$source.kind } else { '' }
            $label = $path
            if ($lineStart -gt 0) {
                $label = '{0}:{1}' -f $label, $lineStart
            }
            if ($kind) {
                $label = '{0} [{1}]' -f $label, $kind
            }
            if ($label) {
                $parts.Add($label)
            }
        }

        return ($parts -join '; ')
    }

    function Get-StatementProvenanceRecords {
        param([object]$Instance)

        $paths = Get-TraceabilityPaths -Instance $Instance
        $records = New-Object System.Collections.Generic.List[object]
        if (-not (Test-Path -LiteralPath $paths.StatementPath)) {
            return @()
        }

        foreach ($line in (Get-Content -LiteralPath $paths.StatementPath -ErrorAction SilentlyContinue)) {
            if ([string]::IsNullOrWhiteSpace($line)) {
                continue
            }

            try {
                $record = $line | ConvertFrom-Json
                $records.Add([pscustomobject]@{
                    BlockId = [string]$record.block_id
                    Agent = [string]$record.agent
                    Artifact = [string]$record.artifact
                    StatementSummary = [string]$record.statement_summary
                    Confidence = [string]$record.confidence
                    Sources = @($record.sources)
                    BusinessRules = @($record.business_rules)
                    Raw = $record
                })
            } catch {
            }
        }

        return @($records)
    }

    function Get-RuleCatalog {
        param(
            [object]$Instance,
            [object[]]$Records
        )

        $rows = New-Object System.Collections.Generic.List[object]
        foreach ($record in @($Records)) {
            foreach ($rule in @($record.BusinessRules)) {
                $sourceDocument = if ($rule.PSObject.Properties['source_document']) { [string]$rule.source_document } else { '' }
                $rows.Add([pscustomobject]@{
                    RuleId = if ($rule.PSObject.Properties['rule_id']) { [string]$rule.rule_id } else { '' }
                    Statement = $record.StatementSummary
                    Artifact = $record.Artifact
                    Agent = $record.Agent
                    Confidence = $record.Confidence
                    SourceDocument = $sourceDocument
                    SourceDocumentPath = Get-ResolvedInstancePath -Instance $Instance -Path $sourceDocument
                    Rationale = if ($rule.PSObject.Properties['rationale']) { [string]$rule.rationale } else { '' }
                    Sources = @($record.Sources)
                    BlockId = $record.BlockId
                    RawRecord = $record
                    RawRule = $rule
                })
            }
        }

        return @($rows | Sort-Object RuleId, Artifact, BlockId)
    }

    function Get-RuleConflicts {
        param([object[]]$RuleCatalog)

        $conflicts = New-Object System.Collections.Generic.List[object]
        foreach ($group in @($RuleCatalog | Group-Object RuleId)) {
            if ([string]::IsNullOrWhiteSpace([string]$group.Name)) {
                continue
            }

            $entries = @($group.Group)
            if ($entries.Count -lt 2) {
                continue
            }

            $rationales = @($entries | ForEach-Object { $_.Rationale } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
            $statements = @($entries | ForEach-Object { $_.Statement } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
            $confidences = @($entries | ForEach-Object { $_.Confidence } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
            $documents = @($entries | ForEach-Object { $_.SourceDocument } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
            $hasConflict = ($rationales.Count -gt 1) -or ($statements.Count -gt 1) -or ($confidences.Count -gt 1)
            if (-not $hasConflict) {
                continue
            }

            $conflicts.Add([pscustomobject]@{
                RuleId = [string]$group.Name
                EntryCount = $entries.Count
                ConfidenceSet = ($confidences -join ', ')
                DocumentSet = ($documents -join ', ')
                Summary = ($statements | Select-Object -First 2) -join ' || '
                ResolutionPrompt = @(
                    "Analyze the conflicting business rule entries for rule ID: $($group.Name).",
                    'Determine the root cause of the conflict, identify which statement should be kept, merged, or split, and propose the exact remediation in the provenance records and source documents.',
                    '',
                    'Conflicting entries:',
                    ($entries | ForEach-Object {
                        '- Block {0} | Agent {1} | Artifact {2} | Confidence {3} | Document {4} | Rationale {5} | Statement {6}' -f $_.BlockId, $_.Agent, $_.Artifact, $_.Confidence, $_.SourceDocument, $_.Rationale, $_.Statement
                    })
                ) -join [Environment]::NewLine
                Entries = $entries
            })
        }

        return @($conflicts | Sort-Object RuleId)
    }

    function Enable-ListViewSorting {
        param([System.Windows.Forms.ListView]$ListView)

        $sortState = [pscustomobject]@{ Column = 0; Ascending = $true }
        $ListView.ListViewItemSorter = New-Object System.Collections.CaseInsensitiveComparer
        $ListView.Add_ColumnClick({
            param($sender, $eventArgs)

            $columnIndex = [int]$eventArgs.Column
            if ($sortState.Column -eq $columnIndex) {
                $sortState.Ascending = -not $sortState.Ascending
            } else {
                $sortState.Column = $columnIndex
                $sortState.Ascending = $true
            }

            $items = @($sender.Items | ForEach-Object { $_ })
            $sender.BeginUpdate()
            $sender.Items.Clear()
            foreach ($item in @($items | Sort-Object -Property @{ Expression = {
                if ($_.SubItems.Count -gt $columnIndex) { [string]$_.SubItems[$columnIndex].Text } else { '' }
            }; Descending = (-not $sortState.Ascending) })) {
                [void]$sender.Items.Add($item)
            }
            $sender.EndUpdate()
        })
    }
}

function Launch-VSCodeWorkspace {
    param([string]$TargetFolder)

    if ([string]::IsNullOrWhiteSpace($TargetFolder) -or -not (Test-Path -LiteralPath $TargetFolder)) {
        throw 'Select a valid target folder before launching VS Code.'
    }

    return Invoke-ProcessCapture -FilePath 'cmd.exe' -Arguments ('/c start "" code -r "{0}"' -f $TargetFolder) -WorkingDirectory $TargetFolder
}

function Get-SelectedEngineIds {
    param([string]$Selection)

    switch ($Selection) {
        'GitHub Copilot' { return @('github-copilot') }
        'Claude Code' { return @('claude-code') }
        default { return @('claude-code', 'github-copilot') }
    }
}

function Get-TraceabilityAuditReportPath {
    param([string]$TargetFolder)

    return Join-Path (Get-TraceabilityToolkitTargetFolder -TargetFolder $TargetFolder) 'audit\traceability-provenance-audit.md'
}

function Read-DelimitedList {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return @()
    }

    return @(
        $Value -split ';' |
            ForEach-Object { $_.Trim() } |
            Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    )
}

function Prompt-ForTraceabilitySnapshotOptions {
    $buildMethod = [Microsoft.VisualBasic.Interaction]::InputBox(
        'Build method: module, feature, combined, or unspecified',
        'Create Traceability Snapshot',
        'unspecified'
    )

    if ([string]::IsNullOrWhiteSpace($buildMethod)) {
        return $null
    }

    $normalizedBuildMethod = $buildMethod.Trim().ToLowerInvariant()
    if ($normalizedBuildMethod -notin @('module', 'feature', 'combined', 'unspecified')) {
        throw 'Build method must be one of: module, feature, combined, unspecified.'
    }

    $buildScope = [Microsoft.VisualBasic.Interaction]::InputBox(
        'Build scope label (optional)',
        'Create Traceability Snapshot',
        ''
    )
    $sourceInputs = [Microsoft.VisualBasic.Interaction]::InputBox(
        'Additional source inputs separated by semicolons (optional)',
        'Create Traceability Snapshot',
        ''
    )
    $supportingSnapshots = [Microsoft.VisualBasic.Interaction]::InputBox(
        'Supporting snapshot paths separated by semicolons (optional)',
        'Create Traceability Snapshot',
        ''
    )
    $changeSummary = [Microsoft.VisualBasic.Interaction]::InputBox(
        'Change summary (optional)',
        'Create Traceability Snapshot',
        ''
    )

    return [pscustomobject]@{
        BuildMethod = $normalizedBuildMethod
        BuildScope = if ($null -eq $buildScope) { '' } else { $buildScope.Trim() }
        SourceInputs = @(Read-DelimitedList -Value $sourceInputs)
        SupportingSnapshots = @(Read-DelimitedList -Value $supportingSnapshots)
        ChangeSummary = if ($null -eq $changeSummary) { '' } else { $changeSummary.Trim() }
    }
}

function Select-FolderWithPrompt {
    param(
        [string]$Description,
        [string]$InitialPath = ''
    )

    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = $Description
    if (-not [string]::IsNullOrWhiteSpace($InitialPath) -and (Test-Path -LiteralPath $InitialPath)) {
        $dialog.SelectedPath = $InitialPath
    }

    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        return $dialog.SelectedPath
    }

    return ''
}

function Invoke-TraceabilitySnapshotCreate {
    param(
        [string]$TargetFolder,
        [string]$BuildMethod,
        [string]$BuildScope,
        [string[]]$SourceInputs = @(),
        [string[]]$SupportingSnapshots = @(),
        [string]$ChangeSummary = ''
    )

    $traceabilityFolder = Get-TraceabilityToolkitTargetFolder -TargetFolder $TargetFolder
    $scriptPath = Join-Path $traceabilityFolder 'New-TraceabilitySnapshot.ps1'
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        throw 'Snapshot helper not found. Install the traceability toolkit first.'
    }

    $arguments = New-Object System.Collections.Generic.List[string]
    $arguments.Add('-NoProfile') | Out-Null
    $arguments.Add('-ExecutionPolicy') | Out-Null
    $arguments.Add('Bypass') | Out-Null
    $arguments.Add('-File') | Out-Null
    $arguments.Add(('"{0}"' -f $scriptPath)) | Out-Null
    $arguments.Add('-TracingFolder') | Out-Null
    $arguments.Add(('"{0}"' -f $traceabilityFolder)) | Out-Null
    $arguments.Add('-BuildMethod') | Out-Null
    $arguments.Add($BuildMethod) | Out-Null

    if (-not [string]::IsNullOrWhiteSpace($BuildScope)) {
        $arguments.Add('-BuildScope') | Out-Null
        $arguments.Add(('"{0}"' -f $BuildScope.Replace('"', '\"'))) | Out-Null
    }
    if (-not [string]::IsNullOrWhiteSpace($ChangeSummary)) {
        $arguments.Add('-ChangeSummary') | Out-Null
        $arguments.Add(('"{0}"' -f $ChangeSummary.Replace('"', '\"'))) | Out-Null
    }
    foreach ($sourceInput in @($SourceInputs)) {
        $arguments.Add('-SourceInputs') | Out-Null
        $arguments.Add(('"{0}"' -f $sourceInput.Replace('"', '\"'))) | Out-Null
    }
    foreach ($supportingSnapshot in @($SupportingSnapshots)) {
        $arguments.Add('-SupportingSnapshots') | Out-Null
        $arguments.Add(('"{0}"' -f $supportingSnapshot.Replace('"', '\"'))) | Out-Null
    }

    $result = Invoke-ProcessCapture -FilePath (Get-PowerShellExecutable) -Arguments ($arguments -join ' ') -WorkingDirectory $traceabilityFolder
    $combined = (($result.StdOut + [Environment]::NewLine + $result.StdErr) -split "`r?`n")
    $snapshotPath = ''
    foreach ($line in $combined) {
        if ($line -match '^Snapshot created:\s*(.+)$') {
            $snapshotPath = $Matches[1].Trim()
            break
        }
    }

    return [pscustomobject]@{
        ExitCode = $result.ExitCode
        StdOut = $result.StdOut
        StdErr = $result.StdErr
        SnapshotPath = $snapshotPath
    }
}

function Invoke-TraceabilitySnapshotCompare {
    param(
        [string]$TargetFolder,
        [string]$LeftSnapshotPath,
        [string]$RightSnapshotPath
    )

    $traceabilityFolder = Get-TraceabilityToolkitTargetFolder -TargetFolder $TargetFolder
    $scriptPath = Join-Path $traceabilityFolder 'Compare-TraceabilitySnapshots.ps1'
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        throw 'Compare helper not found. Install the traceability toolkit first.'
    }

    $arguments = @(
        '-NoProfile',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        ('"{0}"' -f $scriptPath),
        '-LeftSnapshotPath',
        ('"{0}"' -f $LeftSnapshotPath),
        '-RightSnapshotPath',
        ('"{0}"' -f $RightSnapshotPath)
    )

    $result = Invoke-ProcessCapture -FilePath (Get-PowerShellExecutable) -Arguments ($arguments -join ' ') -WorkingDirectory $traceabilityFolder
    $combined = (($result.StdOut + [Environment]::NewLine + $result.StdErr) -split "`r?`n")
    $markdownReportPath = ''
    foreach ($line in $combined) {
        if ($line -match '^Report created:\s*(.+\.md)$') {
            $markdownReportPath = $Matches[1].Trim()
            break
        }
    }

    return [pscustomobject]@{
        ExitCode = $result.ExitCode
        StdOut = $result.StdOut
        StdErr = $result.StdErr
        ReportPath = $markdownReportPath
    }
}

function Install-AuditOpenTraceabilityToolkit {
    param(
        [string]$SourceFolder,
        [string]$TargetFolder
    )

    $installResult = Install-TraceabilityToolkit -SourceFolder $SourceFolder -TargetFolder $TargetFolder
    $auditResult = Invoke-TraceabilityToolkitAction -TargetFolder $TargetFolder -Action 'Audit Provenance Setup'
    $reportPath = Get-TraceabilityAuditReportPath -TargetFolder $TargetFolder
    if ($auditResult.ExitCode -eq 0) {
        Open-PathIfExists -Path $reportPath
    }

    return [pscustomobject]@{
        Install = $installResult
        Audit = $auditResult
        ReportPath = $reportPath
    }
}

function New-TreeNode {
    param(
        [string]$Text,
        [string]$Path,
        [bool]$IsFile = $false
    )

    $node = New-Object System.Windows.Forms.TreeNode($Text)
    $node.Tag = [pscustomobject]@{
        Path = $Path
        IsFile = $IsFile
    }
    return $node
}

function Add-DirectoryToTree {
    param(
        [System.Windows.Forms.TreeNode]$ParentNode,
        [string]$DirectoryPath
    )

    Get-ChildItem -LiteralPath $DirectoryPath -Force -ErrorAction SilentlyContinue |
        Sort-Object @{ Expression = { -not $_.PSIsContainer } }, Name |
        ForEach-Object {
            $childNode = New-TreeNode -Text $_.Name -Path $_.FullName -IsFile (-not $_.PSIsContainer)
            [void]$ParentNode.Nodes.Add($childNode)
            if ($_.PSIsContainer) {
                Add-DirectoryToTree -ParentNode $childNode -DirectoryPath $_.FullName
            }
        }
}

function Get-FileContent {
    param([string]$Path)

    $extension = [System.IO.Path]::GetExtension($Path).ToLowerInvariant()
    $textExtensions = @('.md', '.txt', '.json', '.toml', '.yaml', '.yml', '.ps1', '.js', '.mjs', '.cs', '.xml', '.sql', '.config', '.props', '.targets', '.bat', '.cmd')
    if ($textExtensions -notcontains $extension) {
        return "Preview not available for $extension files.`r`n`r`n$Path"
    }

    try {
        return Get-Content -LiteralPath $Path -Raw
    } catch {
        return "Failed to read file:`r`n$Path`r`n`r`n$($_.Exception.Message)"
    }
}

function Convert-InlineMarkdown {
    param([string]$Text)

    $encoded = [System.Net.WebUtility]::HtmlEncode($Text)
    $encoded = [regex]::Replace($encoded, '\*\*(.+?)\*\*', '<strong>$1</strong>')
    $encoded = [regex]::Replace($encoded, '`([^`]+)`', '<code>$1</code>')
    $encoded = [regex]::Replace($encoded, '\[(.+?)\]\((.+?)\)', '<a href="$2">$1</a>')
    return $encoded
}

function Convert-MarkdownToHtml {
    param(
        [string]$Markdown,
        [string]$Title = 'Preview',
        [object]$Metadata = $null
    )

    $lines = ($Markdown -replace "`r", '') -split "`n"
    $builder = New-Object System.Text.StringBuilder
    $null = $builder.AppendLine('<html><head><meta charset="utf-8">')
    $null = $builder.AppendLine('<style>body{font-family:Segoe UI,Arial,sans-serif;background:#121214;color:#e6e6eb;margin:0;padding:20px;}h1,h2,h3,h4,h5,h6{color:#ffa203;}code{background:#1f1f25;color:#ffd18c;padding:2px 4px;border-radius:4px;}pre{background:#1b1b1f;color:#f0f0f0;padding:14px;border-radius:8px;overflow:auto;border:1px solid #3e3e46;}blockquote{border-left:4px solid #ffa203;margin:12px 0;padding:6px 14px;color:#c7c7d0;background:#1b1b1f;}ul,ol{margin:8px 0 8px 24px;}p{line-height:1.55;}a{color:#7eb6ff;}hr{border:none;border-top:1px solid #3e3e46;margin:16px 0;}.table{white-space:pre-wrap;background:#1b1b1f;padding:12px;border-radius:8px;border:1px solid #3e3e46;}.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:0 0 20px 0;}.meta-card{background:#1b1b1f;border:1px solid #3e3e46;border-radius:10px;padding:12px 14px;}.meta-card h3{margin:0 0 8px 0;font-size:14px;color:#ffa203;text-transform:uppercase;letter-spacing:.06em;}.meta-card ul{margin:0 0 0 18px;padding:0;}.meta-card li{margin:4px 0;}</style></head><body>')
    $null = $builder.AppendLine("<div style='font-size:24px;font-weight:600;margin-bottom:18px;'>$([System.Net.WebUtility]::HtmlEncode($Title))</div>")
    if ($Metadata) {
        $null = $builder.AppendLine('<div class="meta">')
        $null = $builder.AppendLine("<div class='meta-card'><h3>Category</h3><div>$([System.Net.WebUtility]::HtmlEncode($Metadata.Category))</div></div>")
        $null = $builder.AppendLine("<div class='meta-card'><h3>Markdown Source</h3><div>$([System.Net.WebUtility]::HtmlEncode($Metadata.RelativePath))</div></div>")
        $sourceItems = if ($Metadata.Sources -and $Metadata.Sources.Count -gt 0) {
            '<ul>' + (($Metadata.Sources | ForEach-Object { '<li><strong>{0}</strong>: {1}{2}</li>' -f ([System.Net.WebUtility]::HtmlEncode($_.Type)), ([System.Net.WebUtility]::HtmlEncode($_.Value)), (if ($_.Detail) { ' <span style="color:#b4b4be;">(' + [System.Net.WebUtility]::HtmlEncode($_.Detail) + ')</span>' } else { '' }) }) -join '') + '</ul>'
        } else {
            '<div>No associated sources detected.</div>'
        }
        $null = $builder.AppendLine("<div class='meta-card'><h3>Associated Sources</h3>$sourceItems</div>")
        $null = $builder.AppendLine('</div>')
    }

    $inCode = $false
    $inUl = $false
    $inOl = $false
    $paragraph = New-Object System.Collections.Generic.List[string]

    function Close-Paragraph([System.Text.StringBuilder]$HtmlBuilder, [System.Collections.Generic.List[string]]$ParagraphLines) {
        if ($ParagraphLines.Count -gt 0) {
            $content = ($ParagraphLines | ForEach-Object { Convert-InlineMarkdown $_ }) -join '<br/>'
            $null = $HtmlBuilder.AppendLine("<p>$content</p>")
            $ParagraphLines.Clear()
        }
    }

    function Close-Lists([System.Text.StringBuilder]$HtmlBuilder, [ref]$Ul, [ref]$Ol) {
        if ($Ul.Value) {
            $null = $HtmlBuilder.AppendLine('</ul>')
            $Ul.Value = $false
        }
        if ($Ol.Value) {
            $null = $HtmlBuilder.AppendLine('</ol>')
            $Ol.Value = $false
        }
    }

    foreach ($line in $lines) {
        if ($line -match '^```') {
            Close-Paragraph $builder $paragraph
            $ulRef = [ref]$inUl
            $olRef = [ref]$inOl
            Close-Lists $builder $ulRef $olRef
            if (-not $inCode) {
                $null = $builder.AppendLine('<pre><code>')
                $inCode = $true
            } else {
                $null = $builder.AppendLine('</code></pre>')
                $inCode = $false
            }
            continue
        }

        if ($inCode) {
            $null = $builder.AppendLine([System.Net.WebUtility]::HtmlEncode($line))
            continue
        }

        if ([string]::IsNullOrWhiteSpace($line)) {
            Close-Paragraph $builder $paragraph
            $ulRef = [ref]$inUl
            $olRef = [ref]$inOl
            Close-Lists $builder $ulRef $olRef
            continue
        }

        if ($line -match '^#{1,6}\s+(.+)$') {
            Close-Paragraph $builder $paragraph
            $ulRef = [ref]$inUl
            $olRef = [ref]$inOl
            Close-Lists $builder $ulRef $olRef
            $level = ($line -split ' ')[0].Length
            $content = Convert-InlineMarkdown $Matches[1]
            $null = $builder.AppendLine("<h$level>$content</h$level>")
            continue
        }

        if ($line -match '^[-*]\s+(.+)$') {
            Close-Paragraph $builder $paragraph
            if (-not $inUl) {
                if ($inOl) { $null = $builder.AppendLine('</ol>'); $inOl = $false }
                $null = $builder.AppendLine('<ul>')
                $inUl = $true
            }
            $null = $builder.AppendLine("<li>$(Convert-InlineMarkdown $Matches[1])</li>")
            continue
        }

        if ($line -match '^\d+\.\s+(.+)$') {
            Close-Paragraph $builder $paragraph
            if (-not $inOl) {
                if ($inUl) { $null = $builder.AppendLine('</ul>'); $inUl = $false }
                $null = $builder.AppendLine('<ol>')
                $inOl = $true
            }
            $null = $builder.AppendLine("<li>$(Convert-InlineMarkdown $Matches[1])</li>")
            continue
        }

        if ($line -match '^>\s+(.+)$') {
            Close-Paragraph $builder $paragraph
            $ulRef = [ref]$inUl
            $olRef = [ref]$inOl
            Close-Lists $builder $ulRef $olRef
            $null = $builder.AppendLine("<blockquote>$(Convert-InlineMarkdown $Matches[1])</blockquote>")
            continue
        }

        if ($line -match '^---+$') {
            Close-Paragraph $builder $paragraph
            $ulRef = [ref]$inUl
            $olRef = [ref]$inOl
            Close-Lists $builder $ulRef $olRef
            $null = $builder.AppendLine('<hr/>')
            continue
        }

        if ($line.Contains('|')) {
            Close-Paragraph $builder $paragraph
            $ulRef = [ref]$inUl
            $olRef = [ref]$inOl
            Close-Lists $builder $ulRef $olRef
            $null = $builder.AppendLine("<div class='table'>$([System.Net.WebUtility]::HtmlEncode($line))</div>")
            continue
        }

        $paragraph.Add($line)
    }

    Close-Paragraph $builder $paragraph
    $ulRef = [ref]$inUl
    $olRef = [ref]$inOl
    Close-Lists $builder $ulRef $olRef

    if ($inCode) {
        $null = $builder.AppendLine('</code></pre>')
    }

    $null = $builder.AppendLine('</body></html>')
    return $builder.ToString()
}

function Export-MarkdownCatalogToHtml {
    param([object]$Instance)

    $catalog = Get-MarkdownCatalog -Instance $Instance
    $catalogPath = Save-MarkdownCatalog -Instance $Instance -Catalog $catalog
    $htmlRoot = Join-Path $Instance.Root '.reversa\_html'
    New-Item -ItemType Directory -Path $htmlRoot -Force | Out-Null

    foreach ($entry in $catalog) {
        $htmlPath = Join-Path $htmlRoot (($entry.RelativePath -replace '/', '\\') -replace '\.md$', '.html')
        $htmlDir = Split-Path -Parent $htmlPath
        if (-not (Test-Path -LiteralPath $htmlDir)) {
            New-Item -ItemType Directory -Path $htmlDir -Force | Out-Null
        }
        $markdown = Get-FileContent -Path $entry.FullPath
        $html = Convert-MarkdownToHtml -Markdown $markdown -Title $entry.Title -Metadata $entry
        Set-Content -LiteralPath $htmlPath -Value $html -Encoding UTF8
    }

    $grouped = $catalog | Group-Object Category | Sort-Object Name
    $indexBuilder = New-Object System.Text.StringBuilder
    $null = $indexBuilder.AppendLine('# Markdown HTML Export')
    $null = $indexBuilder.AppendLine('')
    $null = $indexBuilder.AppendLine("Instance: $($Instance.Name)")
    $null = $indexBuilder.AppendLine("")
    $null = $indexBuilder.AppendLine("Catalog source: .reversa/_config/markdown-catalog.json")
    foreach ($group in $grouped) {
        $null = $indexBuilder.AppendLine("")
        $null = $indexBuilder.AppendLine("## $($group.Name)")
        foreach ($entry in ($group.Group | Sort-Object RelativePath)) {
            $htmlRelative = ($entry.RelativePath -replace '\.md$', '.html')
            $null = $indexBuilder.AppendLine(("- [{0}]({1})" -f $entry.Title, $htmlRelative))
            $null = $indexBuilder.AppendLine(("  Source markdown: {0}" -f $entry.RelativePath))
            if ($entry.Sources.Count -gt 0) {
                foreach ($source in $entry.Sources) {
                    $null = $indexBuilder.AppendLine(("  Assoc: {0} -> {1}" -f $source.Type, $source.Value))
                }
            }
        }
    }

    $indexMarkdown = $indexBuilder.ToString()
    $indexPath = Join-Path $htmlRoot 'index.html'
    Set-Content -LiteralPath $indexPath -Value (Convert-MarkdownToHtml -Markdown $indexMarkdown -Title 'Markdown HTML Export Index') -Encoding UTF8

    return [pscustomobject]@{
        HtmlRoot = $htmlRoot
        CatalogPath = $catalogPath
        MarkdownCount = $catalog.Count
    }
}

function Invoke-ProcessCapture {
    param(
        [string]$FilePath,
        [string]$Arguments,
        [string]$WorkingDirectory,
        [string]$StandardInput = ''
    )

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $FilePath
    $psi.Arguments = $Arguments
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    [void]$process.Start()

    if ($StandardInput) {
        $process.StandardInput.WriteLine($StandardInput)
    }
    $process.StandardInput.Close()

    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    return [pscustomobject]@{
        ExitCode = $process.ExitCode
        StdOut = $stdout
        StdErr = $stderr
    }
}

function Invoke-ReversaUpdate {
    param(
        [string]$BaseRepo,
        [string]$TargetFolder
    )

    $version = Get-ReversaBaseVersion -BaseRepoPath $BaseRepo
    if (-not $version) {
        throw 'Unable to determine the Reversa version from the base repository.'
    }

    $command = '/c cd /d "{0}" && (echo y| npx -y reversa@{1} update)' -f $TargetFolder, $version
    return Invoke-ProcessCapture -FilePath 'cmd.exe' -Arguments $command -WorkingDirectory $TargetFolder
}

function Invoke-ReversaInstall {
    param(
        [string]$BaseRepo,
        [string]$TargetFolder,
        [hashtable]$Answers
    )

    $version = Get-ReversaBaseVersion -BaseRepoPath $BaseRepo
    if (-not $version) {
        throw 'Unable to determine the Reversa version from the base repository.'
    }

    $answers.version = $version
    $answersFile = Join-Path $env:TEMP ('reversa-install-{0}.json' -f ([guid]::NewGuid().ToString('N')))
    $scriptFile = Join-Path $env:TEMP ('reversa-install-{0}.mjs' -f ([guid]::NewGuid().ToString('N')))
    Set-Content -LiteralPath $answersFile -Value ($Answers | ConvertTo-Json -Depth 10) -Encoding UTF8

    $nodeScript = @'
import { existsSync } from 'fs';
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';
import { pathToFileURL } from 'url';

const [,, baseRepo, targetFolder, answersFile] = process.argv;
const answers = JSON.parse(await readFile(answersFile, 'utf8'));

const writerModule = await import(pathToFileURL(join(baseRepo, 'lib', 'installer', 'writer.js')).href);
const manifestModule = await import(pathToFileURL(join(baseRepo, 'lib', 'installer', 'manifest.js')).href);
const detectorModule = await import(pathToFileURL(join(baseRepo, 'lib', 'installer', 'detector.js')).href);

const { Writer } = writerModule;
const { buildManifest, saveManifest, loadManifest } = manifestModule;
const { ENGINES } = detectorModule;

const writer = new Writer(targetFolder);
const selectedEngines = ENGINES.filter(engine => answers.engines.includes(engine.id));
const skippedEntryFiles = [];

for (const agent of answers.agents) {
  for (const engine of selectedEngines) {
    await writer.installSkill(agent, engine.skillsDir);
    if (engine.universalSkillsDir && engine.universalSkillsDir !== engine.skillsDir) {
      await writer.installSkill(agent, engine.universalSkillsDir);
    }
  }
}

const seenEntryFiles = new Set();
for (const engine of selectedEngines) {
  if (!engine.entryFile || seenEntryFiles.has(engine.entryFile)) {
    continue;
  }
  seenEntryFiles.add(engine.entryFile);
  const destination = join(targetFolder, engine.entryFile);
  if (existsSync(destination)) {
    skippedEntryFiles.push(engine.entryFile);
    continue;
  }
  await writer.installEntryFile(engine);
}

writer.createReversaDir(answers, answers.version);
if (answers.git_strategy === 'gitignore') {
  writer.updateGitignore(answers.output_folder);
}
writer.saveCreatedFiles();

const existingManifest = existsSync(join(targetFolder, '.reversa', '_config', 'files-manifest.json'))
  ? loadManifest(targetFolder)
  : {};
const newManifest = buildManifest(targetFolder, writer.manifestPaths);
saveManifest(targetFolder, { ...existingManifest, ...newManifest });

await writeFile(join(targetFolder, '.reversa', 'version'), answers.version, 'utf8');

console.log(JSON.stringify({
  installed: true,
  version: answers.version,
  targetFolder,
  skippedEntryFiles,
  engines: answers.engines,
  agents: answers.agents.length
}, null, 2));
'@

    Set-Content -LiteralPath $scriptFile -Value $nodeScript -Encoding UTF8

    try {
        $arguments = '"{0}" "{1}" "{2}"' -f $scriptFile, $BaseRepo, $answersFile
        return Invoke-ProcessCapture -FilePath 'node' -Arguments $arguments -WorkingDirectory $TargetFolder
    } finally {
        Remove-Item -LiteralPath $answersFile -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $scriptFile -Force -ErrorAction SilentlyContinue
    }
}

function Update-MarkdownPreview {
    param(
        [System.Windows.Forms.WebBrowser]$Browser,
        [System.Windows.Forms.TextBox]$RawBox,
        [string]$Path
    )

    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) {
        $RawBox.Text = ''
        $Browser.DocumentText = Convert-MarkdownToHtml -Markdown 'No file selected.' -Title 'Preview'
        return
    }

    $content = Get-FileContent -Path $Path
    $RawBox.Text = $content
    $title = Split-Path -Leaf $Path
    if ([System.IO.Path]::GetExtension($Path).ToLowerInvariant() -eq '.md') {
        $Browser.DocumentText = Convert-MarkdownToHtml -Markdown $content -Title $title
    } else {
        $escaped = [System.Net.WebUtility]::HtmlEncode($content)
        $Browser.DocumentText = "<html><body style='margin:0;background:#121214;color:#e6e6eb;font-family:Consolas,monospace;'><pre style='padding:16px;white-space:pre-wrap;'>$escaped</pre></body></html>"
    }
}

function Build-InstanceTab {
    param(
        [object]$Instance,
        [System.Windows.Forms.Label]$ActiveLabel
    )

    $tabPage = New-Object System.Windows.Forms.TabPage
    $tabPage.Text = $Instance.Name
    $tabPage.BackColor = $script:Theme.PanelBack
    $tabPage.ForeColor = $script:Theme.Text
    $catalog = Get-MarkdownCatalog -Instance $Instance
    Save-MarkdownCatalog -Instance $Instance -Catalog $catalog | Out-Null
    $catalogByPath = @{}
    foreach ($entry in $catalog) {
        $catalogByPath[$entry.FullPath] = $entry
    }
    $provenanceStatus = Get-ProvenanceValidation -Instance $Instance -Catalog $catalog
    $databaseGroundingStatus = Get-DatabaseGroundingValidation -Instance $Instance
    $databaseGroundingPaths = Get-DatabaseGroundingPaths -Instance $Instance

    $tabPage.Tag = [pscustomobject]@{
        Instance = $Instance
        Catalog = $catalog
        Provenance = $provenanceStatus
        DatabaseGrounding = $databaseGroundingStatus
    }

    $splitMain = New-Object System.Windows.Forms.SplitContainer
    $splitMain.Dock = 'Fill'
    $splitMain.BackColor = $script:Theme.FormBack
    $splitMain.SplitterDistance = 380
    $splitMain.Panel1.BackColor = $script:Theme.PanelBack
    $splitMain.Panel2.BackColor = $script:Theme.PanelAlt

    $summaryBox = New-Object System.Windows.Forms.GroupBox
    $summaryBox.Text = 'Instance Summary'
    $summaryBox.Dock = 'Top'
    $summaryBox.Height = 130
    $summaryBox.ForeColor = $script:Theme.Text
    $summaryBox.BackColor = $script:Theme.PanelBack

    $summaryLabel = New-Object System.Windows.Forms.Label
    $summaryLabel.Dock = 'Fill'
    $summaryLabel.Padding = New-Object System.Windows.Forms.Padding(12)
    $summaryLabel.ForeColor = $script:Theme.Text
    $summaryLabel.BackColor = $script:Theme.PanelBack
    $summaryLabel.Font = New-Object System.Drawing.Font('Segoe UI', 10)
    $taskList = Get-PlanTasks -PlanPath $Instance.PlanPath
    $completedTaskCount = @($taskList | Where-Object { $_.Done }).Count
    $summaryLabel.Text = @(
        "Root: $($Instance.Root)",
        "Phase: $($Instance.State.phase)",
        "Output: $($Instance.OutputFolder)",
        "Completed phases: $((@($Instance.State.completed) -join ', '))",
        "Task progress: $completedTaskCount / $($taskList.Count)",
        "Provenance: $($provenanceStatus.Level) | Records: $($provenanceStatus.RecordCount) | Rule links: $($provenanceStatus.BusinessRuleLinks)",
        "DB grounding: $($databaseGroundingStatus.Level) | Active tables: $($databaseGroundingStatus.ActiveTables) | Query approval: $($databaseGroundingStatus.ApprovalStatus)"
    ) -join [Environment]::NewLine
    $summaryBox.Controls.Add($summaryLabel)

    $actionBox = New-Object System.Windows.Forms.GroupBox
    $actionBox.Text = 'Quick Actions'
    $actionBox.Dock = 'Top'
    $actionBox.Height = 118
    $actionBox.ForeColor = $script:Theme.Text
    $actionBox.BackColor = $script:Theme.PanelBack

    $btnOpenProject = New-Object System.Windows.Forms.Button
    $btnOpenProject.Text = 'Open Project'
    $btnOpenProject.Location = New-Object System.Drawing.Point(12, 28)
    $btnOpenProject.Size = New-Object System.Drawing.Size(110, 30)
    $btnOpenProject.BackColor = $script:Theme.PanelAlt
    $btnOpenProject.ForeColor = $script:Theme.Text
    $actionBox.Controls.Add($btnOpenProject)

    $btnOpenOutput = New-Object System.Windows.Forms.Button
    $btnOpenOutput.Text = 'Open Output'
    $btnOpenOutput.Location = New-Object System.Drawing.Point(132, 28)
    $btnOpenOutput.Size = New-Object System.Drawing.Size(110, 30)
    $btnOpenOutput.BackColor = $script:Theme.PanelAlt
    $btnOpenOutput.ForeColor = $script:Theme.Text
    $actionBox.Controls.Add($btnOpenOutput)

    $btnOpenTraceability = New-Object System.Windows.Forms.Button
    $btnOpenTraceability.Text = 'Open Traceability'
    $btnOpenTraceability.Location = New-Object System.Drawing.Point(252, 28)
    $btnOpenTraceability.Size = New-Object System.Drawing.Size(120, 30)
    $btnOpenTraceability.BackColor = $script:Theme.PanelAlt
    $btnOpenTraceability.ForeColor = $script:Theme.Text
    $actionBox.Controls.Add($btnOpenTraceability)

    $btnOpenPlan = New-Object System.Windows.Forms.Button
    $btnOpenPlan.Text = 'Open Plan'
    $btnOpenPlan.Location = New-Object System.Drawing.Point(12, 68)
    $btnOpenPlan.Size = New-Object System.Drawing.Size(110, 30)
    $btnOpenPlan.BackColor = $script:Theme.PanelAlt
    $btnOpenPlan.ForeColor = $script:Theme.Text
    $actionBox.Controls.Add($btnOpenPlan)

    $btnOpenReports = New-Object System.Windows.Forms.Button
    $btnOpenReports.Text = 'Open Reports'
    $btnOpenReports.Location = New-Object System.Drawing.Point(132, 68)
    $btnOpenReports.Size = New-Object System.Drawing.Size(110, 30)
    $btnOpenReports.BackColor = $script:Theme.PanelAlt
    $btnOpenReports.ForeColor = $script:Theme.Text
    $actionBox.Controls.Add($btnOpenReports)

    $btnTabRefresh = New-Object System.Windows.Forms.Button
    $btnTabRefresh.Text = 'Refresh Health'
    $btnTabRefresh.Location = New-Object System.Drawing.Point(252, 68)
    $btnTabRefresh.Size = New-Object System.Drawing.Size(120, 30)
    $btnTabRefresh.BackColor = $script:Theme.AccentSoft
    $btnTabRefresh.ForeColor = $script:Theme.Text
    $actionBox.Controls.Add($btnTabRefresh)

    $taskBox = New-Object System.Windows.Forms.GroupBox
    $taskBox.Text = 'Task Completion'
    $taskBox.Dock = 'Fill'
    $taskBox.ForeColor = $script:Theme.Text
    $taskBox.BackColor = $script:Theme.PanelBack

    $taskView = New-Object System.Windows.Forms.ListView
    $taskView.Dock = 'Fill'
    $taskView.View = 'Details'
    $taskView.FullRowSelect = $true
    $taskView.GridLines = $false
    $taskView.HeaderStyle = 'Nonclickable'
    $taskView.BackColor = $script:Theme.Surface
    $taskView.ForeColor = $script:Theme.Text
    [void]$taskView.Columns.Add('Done', 60)
    [void]$taskView.Columns.Add('Task', 520)
    foreach ($task in $taskList) {
        $doneText = if ($task.Done) { 'Yes' } else { 'No' }
        $item = New-Object System.Windows.Forms.ListViewItem($doneText)
        $taskText = if ($null -ne $task.Text) { [string]$task.Text } else { '' }
        [void]$item.SubItems.Add($taskText)
        if ($task.Done) {
            $item.ForeColor = $script:Theme.Success
        }
        [void]$taskView.Items.Add($item)
    }
    $taskBox.Controls.Add($taskView)

    $dbActionBox = New-Object System.Windows.Forms.GroupBox
    $dbActionBox.Text = 'DB Grounding Actions'
    $dbActionBox.Dock = 'Top'
    $dbActionBox.Height = 270
    $dbActionBox.ForeColor = $script:Theme.Text
    $dbActionBox.BackColor = $script:Theme.PanelBack

    $dbServerLabel = New-Object System.Windows.Forms.Label
    $dbServerLabel.Text = 'Server'
    $dbServerLabel.Location = New-Object System.Drawing.Point(12, 28)
    $dbServerLabel.AutoSize = $true
    $dbServerLabel.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbServerLabel)

    $dbServerBox = New-Object System.Windows.Forms.TextBox
    $dbServerBox.Location = New-Object System.Drawing.Point(12, 48)
    $dbServerBox.Size = New-Object System.Drawing.Size(168, 24)
    $dbServerBox.ReadOnly = $true
    $dbServerBox.BackColor = $script:Theme.Surface
    $dbServerBox.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbServerBox)

    $dbNameLabel = New-Object System.Windows.Forms.Label
    $dbNameLabel.Text = 'Database'
    $dbNameLabel.Location = New-Object System.Drawing.Point(192, 28)
    $dbNameLabel.AutoSize = $true
    $dbNameLabel.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbNameLabel)

    $dbNameBox = New-Object System.Windows.Forms.TextBox
    $dbNameBox.Location = New-Object System.Drawing.Point(192, 48)
    $dbNameBox.Size = New-Object System.Drawing.Size(168, 24)
    $dbNameBox.ReadOnly = $true
    $dbNameBox.BackColor = $script:Theme.Surface
    $dbNameBox.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbNameBox)

    $dbEngineLabel = New-Object System.Windows.Forms.Label
    $dbEngineLabel.Text = 'Engine'
    $dbEngineLabel.Location = New-Object System.Drawing.Point(12, 78)
    $dbEngineLabel.AutoSize = $true
    $dbEngineLabel.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbEngineLabel)

    $dbEngineBox = New-Object System.Windows.Forms.TextBox
    $dbEngineBox.Location = New-Object System.Drawing.Point(12, 98)
    $dbEngineBox.Size = New-Object System.Drawing.Size(100, 24)
    $dbEngineBox.ReadOnly = $true
    $dbEngineBox.BackColor = $script:Theme.Surface
    $dbEngineBox.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbEngineBox)

    $dbApprovalLabel = New-Object System.Windows.Forms.Label
    $dbApprovalLabel.Text = 'Approval'
    $dbApprovalLabel.Location = New-Object System.Drawing.Point(124, 78)
    $dbApprovalLabel.AutoSize = $true
    $dbApprovalLabel.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbApprovalLabel)

    $dbApprovalBox = New-Object System.Windows.Forms.TextBox
    $dbApprovalBox.Location = New-Object System.Drawing.Point(124, 98)
    $dbApprovalBox.Size = New-Object System.Drawing.Size(116, 24)
    $dbApprovalBox.ReadOnly = $true
    $dbApprovalBox.BackColor = $script:Theme.Surface
    $dbApprovalBox.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbApprovalBox)

    $dbPilotLabel = New-Object System.Windows.Forms.Label
    $dbPilotLabel.Text = 'Pilot table'
    $dbPilotLabel.Location = New-Object System.Drawing.Point(252, 78)
    $dbPilotLabel.AutoSize = $true
    $dbPilotLabel.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbPilotLabel)

    $dbPilotBox = New-Object System.Windows.Forms.TextBox
    $dbPilotBox.Location = New-Object System.Drawing.Point(252, 98)
    $dbPilotBox.Size = New-Object System.Drawing.Size(108, 24)
    $dbPilotBox.ReadOnly = $true
    $dbPilotBox.BackColor = $script:Theme.Surface
    $dbPilotBox.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbPilotBox)

    $dbAccessLabel = New-Object System.Windows.Forms.Label
    $dbAccessLabel.Text = 'Access reference'
    $dbAccessLabel.Location = New-Object System.Drawing.Point(12, 128)
    $dbAccessLabel.AutoSize = $true
    $dbAccessLabel.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbAccessLabel)

    $dbAccessBox = New-Object System.Windows.Forms.TextBox
    $dbAccessBox.Location = New-Object System.Drawing.Point(12, 148)
    $dbAccessBox.Size = New-Object System.Drawing.Size(348, 24)
    $dbAccessBox.ReadOnly = $true
    $dbAccessBox.BackColor = $script:Theme.Surface
    $dbAccessBox.ForeColor = $script:Theme.Text
    $dbActionBox.Controls.Add($dbAccessBox)

    $queryList = New-Object System.Windows.Forms.ListView
    $queryList.Location = New-Object System.Drawing.Point(12, 178)
    $queryList.Size = New-Object System.Drawing.Size(180, 78)
    $queryList.View = 'Details'
    $queryList.FullRowSelect = $true
    $queryList.HeaderStyle = 'Nonclickable'
    $queryList.MultiSelect = $false
    $queryList.BackColor = $script:Theme.Surface
    $queryList.ForeColor = $script:Theme.Text
    [void]$queryList.Columns.Add('Query ID', 100)
    [void]$queryList.Columns.Add('Phase', 55)
    [void]$queryList.Columns.Add('Run', 35)
    $dbActionBox.Controls.Add($queryList)

    $queryDetailsBox = New-Object System.Windows.Forms.TextBox
    $queryDetailsBox.Location = New-Object System.Drawing.Point(200, 178)
    $queryDetailsBox.Size = New-Object System.Drawing.Size(160, 78)
    $queryDetailsBox.Multiline = $true
    $queryDetailsBox.ReadOnly = $true
    $queryDetailsBox.ScrollBars = 'Vertical'
    $queryDetailsBox.BackColor = $script:Theme.Surface
    $queryDetailsBox.ForeColor = $script:Theme.Text
    $queryDetailsBox.Font = New-Object System.Drawing.Font('Consolas', 9)
    $dbActionBox.Controls.Add($queryDetailsBox)

    $btnCopyQueryId = New-Object System.Windows.Forms.Button
    $btnCopyQueryId.Text = 'Copy Query ID'
    $btnCopyQueryId.Location = New-Object System.Drawing.Point(200, 132)
    $btnCopyQueryId.Size = New-Object System.Drawing.Size(78, 28)
    $btnCopyQueryId.BackColor = $script:Theme.PanelAlt
    $btnCopyQueryId.ForeColor = $script:Theme.Text
    $btnCopyQueryId.Enabled = $false
    $dbActionBox.Controls.Add($btnCopyQueryId)

    $btnCopyCancel = New-Object System.Windows.Forms.Button
    $btnCopyCancel.Text = 'Copy Cancel'
    $btnCopyCancel.Location = New-Object System.Drawing.Point(282, 132)
    $btnCopyCancel.Size = New-Object System.Drawing.Size(78, 28)
    $btnCopyCancel.BackColor = $script:Theme.PanelAlt
    $btnCopyCancel.ForeColor = $script:Theme.Text
    $btnCopyCancel.Enabled = $false
    $dbActionBox.Controls.Add($btnCopyCancel)

    $selectedDbQuery = [pscustomobject]@{ Value = $null }

    [scriptblock]$setDatabaseQueryDetails = {
        param([object]$QueryItem)

        $selectedDbQuery.Value = $QueryItem
        if (-not $QueryItem) {
            $queryDetailsBox.Text = 'No query selected.'
            $btnCopyQueryId.Enabled = $false
            $btnCopyCancel.Enabled = $false
            return
        }

        $query = $QueryItem.Query
        $queryDetailsBox.Text = @(
            "Bundle: $($QueryItem.BundleId)",
            "Query ID: $([string]$query.query_id)",
            "Phase: $([string]$query.phase)",
            "Session ID: $([string]$query.session_id)",
            "Executed: $([string]$query.executed)",
            "Cancel: $([string]$query.cancel_command)",
            "Explain: $([string]$query.explain_summary)"
        ) -join [Environment]::NewLine
        $btnCopyQueryId.Enabled = -not [string]::IsNullOrWhiteSpace([string]$query.query_id)
        $btnCopyCancel.Enabled = -not [string]::IsNullOrWhiteSpace([string]$query.cancel_command)
    }

    [scriptblock]$refreshDatabaseGroundingPanel = {
        $schemaGrounding = Read-JsonSafe -Path $databaseGroundingPaths.SchemaGroundingPath
        $queryGrounding = Read-JsonSafe -Path $databaseGroundingPaths.QueryGroundingPath

        $serverValue = if ($queryGrounding -and $queryGrounding.server_alias) { [string]$queryGrounding.server_alias } elseif ($schemaGrounding -and $schemaGrounding.server_alias) { [string]$schemaGrounding.server_alias } else { '-' }
        $databaseValue = if ($queryGrounding -and $queryGrounding.database_name) { [string]$queryGrounding.database_name } elseif ($schemaGrounding -and $schemaGrounding.database_name) { [string]$schemaGrounding.database_name } else { '-' }
        $engineValue = if ($queryGrounding -and $queryGrounding.engine) { [string]$queryGrounding.engine } elseif ($schemaGrounding -and $schemaGrounding.engine) { [string]$schemaGrounding.engine } else { '-' }
        $approvalValue = if ($queryGrounding -and $queryGrounding.approval_status) { [string]$queryGrounding.approval_status } else { '-' }
        $pilotValue = if ($queryGrounding -and $queryGrounding.pilot_table) {
            $pilotSchema = if ($queryGrounding.pilot_table.schema) { [string]$queryGrounding.pilot_table.schema } else { '' }
            $pilotTable = if ($queryGrounding.pilot_table.table) { [string]$queryGrounding.pilot_table.table } else { '' }
            (($pilotSchema, $pilotTable) | Where-Object { $_ }) -join '.'
        } else {
            '-'
        }
        $accessValue = if ($queryGrounding -and $queryGrounding.access_source) { [string]$queryGrounding.access_source } elseif ($schemaGrounding -and $schemaGrounding.safe_connection_reference) { [string]$schemaGrounding.safe_connection_reference } else { '-' }

        $dbServerBox.Text = $serverValue
        $dbNameBox.Text = $databaseValue
        $dbEngineBox.Text = $engineValue
        $dbApprovalBox.Text = $approvalValue
        $dbPilotBox.Text = if ([string]::IsNullOrWhiteSpace($pilotValue)) { '-' } else { $pilotValue }
        $dbAccessBox.Text = $accessValue

        $queryList.Items.Clear()
        foreach ($bundle in @($queryGrounding.bundles)) {
            foreach ($query in @($bundle.queries)) {
                $item = New-Object System.Windows.Forms.ListViewItem([string]$query.query_id)
                [void]$item.SubItems.Add([string]$query.phase)
                $executedText = if ($query.executed) { 'Yes' } else { 'No' }
                [void]$item.SubItems.Add($executedText)
                $item.Tag = [pscustomobject]@{
                    BundleId = [string]$bundle.bundle_id
                    Query = $query
                }
                [void]$queryList.Items.Add($item)
            }
        }

        if ($queryList.Items.Count -gt 0) {
            $queryList.Items[0].Selected = $true
            $null = $setDatabaseQueryDetails.Invoke($queryList.Items[0].Tag)
        } else {
            $null = $setDatabaseQueryDetails.Invoke($null)
        }
    }

    $queryList.Add_SelectedIndexChanged({
        if ($this.SelectedItems.Count -gt 0) {
            $null = $setDatabaseQueryDetails.Invoke($this.SelectedItems[0].Tag)
        }
    })

    $btnCopyQueryId.Add_Click({
        if ($selectedDbQuery.Value -and $selectedDbQuery.Value.Query -and $selectedDbQuery.Value.Query.query_id) {
            [System.Windows.Forms.Clipboard]::SetText([string]$selectedDbQuery.Value.Query.query_id)
            Write-Log "Copied query ID: $([string]$selectedDbQuery.Value.Query.query_id)"
        }
    })

    $btnCopyCancel.Add_Click({
        if ($selectedDbQuery.Value -and $selectedDbQuery.Value.Query -and $selectedDbQuery.Value.Query.cancel_command) {
            [System.Windows.Forms.Clipboard]::SetText([string]$selectedDbQuery.Value.Query.cancel_command)
            Write-Log "Copied cancel command for query ID: $([string]$selectedDbQuery.Value.Query.query_id)"
        }
    })

    $splitMain.Panel1.Controls.Add($taskBox)
    $splitMain.Panel1.Controls.Add($actionBox)
    $splitMain.Panel1.Controls.Add($summaryBox)

    $splitRight = New-Object System.Windows.Forms.SplitContainer
    $splitRight.Dock = 'Fill'
    $splitRight.Orientation = 'Vertical'
    $splitRight.SplitterDistance = 360
    $splitRight.Panel1.BackColor = $script:Theme.PanelAlt
    $splitRight.Panel2.BackColor = $script:Theme.PanelAlt

    $treeBox = New-Object System.Windows.Forms.GroupBox
    $treeBox.Text = 'Generated Files'
    $treeBox.Dock = 'Fill'
    $treeBox.ForeColor = $script:Theme.Text
    $treeBox.BackColor = $script:Theme.PanelAlt

    $tree = New-Object System.Windows.Forms.TreeView
    $tree.Dock = 'Fill'
    $tree.HideSelection = $false
    $tree.BackColor = $script:Theme.Surface
    $tree.ForeColor = $script:Theme.Text
    $tree.BorderStyle = 'None'

    $tree.Nodes.Clear()
    $reversaRoot = Join-Path $Instance.Root '.reversa'
    if (Test-Path -LiteralPath $reversaRoot) {
        $reversaNode = New-TreeNode -Text '.reversa' -Path $reversaRoot
        Add-DirectoryToTree -ParentNode $reversaNode -DirectoryPath $reversaRoot
        [void]$tree.Nodes.Add($reversaNode)
    }

    if (Test-Path -LiteralPath $Instance.OutputPath) {
        $outputNode = New-TreeNode -Text $Instance.OutputFolder -Path $Instance.OutputPath
        Add-DirectoryToTree -ParentNode $outputNode -DirectoryPath $Instance.OutputPath
        [void]$tree.Nodes.Add($outputNode)
    }

    $trackedFiles = Get-TrackedFiles -State $Instance.State
    if ($trackedFiles.Count -gt 0) {
        $trackedNode = New-TreeNode -Text 'Checkpoint Files' -Path ''
        foreach ($relativeFile in $trackedFiles) {
            $fullPath = Join-Path $Instance.Root ($relativeFile -replace '/', '\\')
            $leaf = Split-Path -Leaf $relativeFile
            $fileNode = New-TreeNode -Text "$leaf  [$relativeFile]" -Path $fullPath -IsFile $true
            [void]$trackedNode.Nodes.Add($fileNode)
        }
        [void]$tree.Nodes.Add($trackedNode)
    }

    $traceabilityPaths = Get-TraceabilityPaths -Instance $Instance
    $traceabilityNode = New-TreeNode -Text 'Provenance Artifacts' -Path ''
    foreach ($pathItem in @(
        [pscustomobject]@{ Label = 'PDD Short'; Path = $traceabilityPaths.PddPath },
        [pscustomobject]@{ Label = 'PDD Extended'; Path = $traceabilityPaths.ExtendedPddPath },
        [pscustomobject]@{ Label = 'Provenance Settings'; Path = $traceabilityPaths.SettingsPath },
        [pscustomobject]@{ Label = 'Statement Provenance'; Path = $traceabilityPaths.StatementPath },
        [pscustomobject]@{ Label = 'Business Rules Index'; Path = $traceabilityPaths.BusinessIndexPath }
    )) {
        if (Test-Path -LiteralPath $pathItem.Path) {
            $node = New-TreeNode -Text $pathItem.Label -Path $pathItem.Path -IsFile $true
            [void]$traceabilityNode.Nodes.Add($node)
        }
    }
    if ($traceabilityNode.Nodes.Count -gt 0) {
        [void]$tree.Nodes.Add($traceabilityNode)
    }

    $databaseGroundingNode = New-TreeNode -Text 'Database Grounding Artifacts' -Path ''
    foreach ($pathItem in @(
        [pscustomobject]@{ Label = 'Schema Grounding JSON'; Path = $databaseGroundingPaths.SchemaGroundingPath },
        [pscustomobject]@{ Label = 'Schema Grounding Schema'; Path = $databaseGroundingPaths.SchemaGroundingSchemaPath },
        [pscustomobject]@{ Label = 'Schema Grounding Example'; Path = $databaseGroundingPaths.SchemaGroundingExamplePath },
        [pscustomobject]@{ Label = 'Query Grounding JSON'; Path = $databaseGroundingPaths.QueryGroundingPath },
        [pscustomobject]@{ Label = 'Query Grounding Schema'; Path = $databaseGroundingPaths.QueryGroundingSchemaPath },
        [pscustomobject]@{ Label = 'Query Grounding Example'; Path = $databaseGroundingPaths.QueryGroundingExamplePath },
        [pscustomobject]@{ Label = 'Schema Layer'; Path = $databaseGroundingPaths.SchemaLayerPath },
        [pscustomobject]@{ Label = 'Table Activity'; Path = $databaseGroundingPaths.TableActivityPath },
        [pscustomobject]@{ Label = 'Inactive Schema'; Path = $databaseGroundingPaths.InactiveSchemaPath },
        [pscustomobject]@{ Label = 'Query Approval'; Path = $databaseGroundingPaths.QueryApprovalPath }
    )) {
        if (Test-Path -LiteralPath $pathItem.Path) {
            $node = New-TreeNode -Text $pathItem.Label -Path $pathItem.Path -IsFile $true
            [void]$databaseGroundingNode.Nodes.Add($node)
        }
    }
    if ($databaseGroundingNode.Nodes.Count -gt 0) {
        [void]$tree.Nodes.Add($databaseGroundingNode)
    }

    $tree.ExpandAll()
    $treeBox.Controls.Add($tree)

    $previewPanel = New-Object System.Windows.Forms.Panel
    $previewPanel.Dock = 'Fill'
    $previewPanel.BackColor = $script:Theme.PanelAlt

    $previewToolbar = New-Object System.Windows.Forms.Panel
    $previewToolbar.Dock = 'Top'
    $previewToolbar.Height = 60
    $previewToolbar.BackColor = $script:Theme.PanelBack

    $currentFileLabel = New-Object System.Windows.Forms.Label
    $currentFileLabel.Text = 'Selected file: -'
    $currentFileLabel.Location = New-Object System.Drawing.Point(10, 12)
    $currentFileLabel.AutoSize = $true
    $currentFileLabel.ForeColor = $script:Theme.Text
    $previewToolbar.Controls.Add($currentFileLabel)

    $metaLabel = New-Object System.Windows.Forms.Label
    $metaLabel.Text = 'Category: - | Sources: -'
    $metaLabel.Location = New-Object System.Drawing.Point(10, 34)
    $metaLabel.AutoSize = $true
    $metaLabel.ForeColor = $script:Theme.Muted
    $previewToolbar.Controls.Add($metaLabel)

    $btnSaveFile = New-Object System.Windows.Forms.Button
    $btnSaveFile.Text = 'Save'
    $btnSaveFile.Size = New-Object System.Drawing.Size(90, 28)
    $btnSaveFile.Location = New-Object System.Drawing.Point(620, 7)
    $btnSaveFile.BackColor = $script:Theme.AccentSoft
    $btnSaveFile.ForeColor = $script:Theme.Text
    $previewToolbar.Controls.Add($btnSaveFile)

    $btnRefreshPreview = New-Object System.Windows.Forms.Button
    $btnRefreshPreview.Text = 'Refresh Preview'
    $btnRefreshPreview.Size = New-Object System.Drawing.Size(120, 28)
    $btnRefreshPreview.Location = New-Object System.Drawing.Point(720, 7)
    $btnRefreshPreview.BackColor = $script:Theme.PanelAlt
    $btnRefreshPreview.ForeColor = $script:Theme.Text
    $previewToolbar.Controls.Add($btnRefreshPreview)

    $btnRefreshStatus = New-Object System.Windows.Forms.Button
    $btnRefreshStatus.Text = 'Refresh Status'
    $btnRefreshStatus.Size = New-Object System.Drawing.Size(110, 28)
    $btnRefreshStatus.Location = New-Object System.Drawing.Point(850, 7)
    $btnRefreshStatus.BackColor = $script:Theme.PanelAlt
    $btnRefreshStatus.ForeColor = $script:Theme.Text
    $previewToolbar.Controls.Add($btnRefreshStatus)

    $previewTabs = New-Object System.Windows.Forms.TabControl
    $previewTabs.Dock = 'Fill'
    $previewTabs.BackColor = $script:Theme.PanelAlt
    $previewTabs.ForeColor = $script:Theme.Text

    $renderTab = New-Object System.Windows.Forms.TabPage
    $renderTab.Text = 'Rendered'
    $renderTab.BackColor = $script:Theme.PanelAlt

    $browser = New-Object System.Windows.Forms.WebBrowser
    $browser.Dock = 'Fill'
    $browser.IsWebBrowserContextMenuEnabled = $false
    $browser.WebBrowserShortcutsEnabled = $false
    $browser.ScriptErrorsSuppressed = $true
    $renderTab.Controls.Add($browser)

    $rawTab = New-Object System.Windows.Forms.TabPage
    $rawTab.Text = 'Raw'
    $rawTab.BackColor = $script:Theme.PanelAlt

    $rawBox = New-Object System.Windows.Forms.TextBox
    $rawBox.Dock = 'Fill'
    $rawBox.Multiline = $true
    $rawBox.ReadOnly = $false
    $rawBox.ScrollBars = 'Both'
    $rawBox.WordWrap = $false
    $rawBox.BackColor = $script:Theme.Surface
    $rawBox.ForeColor = $script:Theme.Text
    $rawBox.Font = New-Object System.Drawing.Font('Consolas', 10)
    $rawTab.Controls.Add($rawBox)

    $statusTab = New-Object System.Windows.Forms.TabPage
    $statusTab.Text = 'Grounding'
    $statusTab.BackColor = $script:Theme.PanelAlt

    $statusBrowser = New-Object System.Windows.Forms.WebBrowser
    $statusBrowser.Dock = 'Fill'
    $statusBrowser.IsWebBrowserContextMenuEnabled = $false
    $statusBrowser.WebBrowserShortcutsEnabled = $false
    $statusBrowser.ScriptErrorsSuppressed = $true
    $statusTab.Controls.Add($statusBrowser)

    [void]$previewTabs.TabPages.Add($renderTab)
    [void]$previewTabs.TabPages.Add($rawTab)
    [void]$previewTabs.TabPages.Add($statusTab)

    $previewPanel.Controls.Add($previewTabs)
    $previewPanel.Controls.Add($previewToolbar)

    $currentSelection = [pscustomobject]@{ Path = $null }

    [scriptblock]$refreshProvenanceStatus = {
        $scriptStatus = Get-ProvenanceValidation -Instance $Instance -Catalog $catalog
        $databaseStatus = Get-DatabaseGroundingValidation -Instance $Instance
        $summaryLabel.Text = @(
            "Root: $($Instance.Root)",
            "Phase: $($Instance.State.phase)",
            "Output: $($Instance.OutputFolder)",
            "Completed phases: $((@($Instance.State.completed) -join ', '))",
            "Task progress: $completedTaskCount / $($taskList.Count)",
            "Provenance: $($scriptStatus.Level) | Records: $($scriptStatus.RecordCount) | Rule links: $($scriptStatus.BusinessRuleLinks)",
            "DB grounding: $($databaseStatus.Level) | Active tables: $($databaseStatus.ActiveTables) | Query approval: $($databaseStatus.ApprovalStatus)"
        ) -join [Environment]::NewLine
        $statusBrowser.DocumentText = Convert-MarkdownToHtml -Markdown (Convert-GroundingStatusToMarkdown -Provenance $scriptStatus -DatabaseGrounding $databaseStatus) -Title 'Grounding Status'
        $null = $refreshDatabaseGroundingPanel.Invoke()
    }

    [scriptblock]$showSelection = {
        param([string]$SelectionPath)

        $currentSelection.Path = $SelectionPath
        $currentFileLabel.Text = if ($SelectionPath) {
            "Selected file: $SelectionPath"
        } else {
            'Selected file: -'
        }
        $metadata = if ($SelectionPath -and $catalogByPath.ContainsKey($SelectionPath)) { $catalogByPath[$SelectionPath] } else { $null }
        if ($metadata) {
            $metaLabel.Text = "Category: $($metadata.Category) | Sources: $($metadata.Sources.Count)"
        } else {
            $metaLabel.Text = 'Category: - | Sources: -'
        }

        if ($script:PreviewMode -eq 'Open Externally' -and -not [string]::IsNullOrWhiteSpace($SelectionPath)) {
            Open-PathIfExists -Path $SelectionPath
            $rawBox.Text = "Opened externally:`r`n$SelectionPath"
            $browser.DocumentText = Convert-MarkdownToHtml -Markdown ("# External Preview`n`nOpened through the OS:`n`n- {0}" -f $SelectionPath) -Title 'External Preview'
            return
        }

        if ($metadata) {
            $content = Get-FileContent -Path $SelectionPath
            $rawBox.Text = $content
            $title = Split-Path -Leaf $SelectionPath
            if ([System.IO.Path]::GetExtension($SelectionPath).ToLowerInvariant() -eq '.md') {
                $browser.DocumentText = Convert-MarkdownToHtml -Markdown $content -Title $title -Metadata $metadata
            } else {
                Update-MarkdownPreview -Browser $browser -RawBox $rawBox -Path $SelectionPath
            }
        } else {
            Update-MarkdownPreview -Browser $browser -RawBox $rawBox -Path $SelectionPath
        }
    }

    $btnOpenProject.Add_Click({ Open-PathIfExists -Path $Instance.Root })
    $btnOpenOutput.Add_Click({ Open-PathIfExists -Path $Instance.OutputPath })
    $btnOpenTraceability.Add_Click({ Open-PathIfExists -Path (Join-Path $Instance.OutputPath 'traceability') })
    $btnOpenPlan.Add_Click({ Open-PathIfExists -Path $Instance.PlanPath })
    $btnOpenReports.Add_Click({ Open-PathIfExists -Path (Join-Path (Join-Path $Instance.OutputPath 'traceability') 'versions\reports') })
    $btnTabRefresh.Add_Click({ $null = $refreshProvenanceStatus.Invoke() })

    $tree.Add_AfterSelect({
        if ($this.SelectedNode -and $this.SelectedNode.Tag -and $this.SelectedNode.Tag.IsFile) {
            $null = $showSelection.Invoke($this.SelectedNode.Tag.Path)
        }
    })

    $btnSaveFile.Add_Click({
        if (-not $currentSelection.Path) {
            [System.Windows.Forms.MessageBox]::Show('Select a text or markdown file before saving.', 'No File Selected', 'OK', 'Information') | Out-Null
            return
        }

        try {
            Set-Content -LiteralPath $currentSelection.Path -Value $rawBox.Text -Encoding UTF8
            if ($catalogByPath.ContainsKey($currentSelection.Path)) {
                $updatedContent = Get-FileContent -Path $currentSelection.Path
                $updatedEntry = $catalogByPath[$currentSelection.Path]
                $updatedEntry.Sources = @(Get-MarkdownSources -Instance $Instance -RelativePath $updatedEntry.RelativePath -Content $updatedContent)
                $updatedEntry.Title = ((($updatedContent -split "`r?`n") | Where-Object { $_ -match '^#' } | Select-Object -First 1) -replace '^#+\s*', '').Trim()
                if (-not $updatedEntry.Title) { $updatedEntry.Title = [System.IO.Path]::GetFileNameWithoutExtension($currentSelection.Path) }
                Save-MarkdownCatalog -Instance $Instance -Catalog $catalog | Out-Null
            }
            $null = $refreshProvenanceStatus.Invoke()
            $null = $showSelection.Invoke($currentSelection.Path)
        } catch {
            [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Save Failed', 'OK', 'Error') | Out-Null
        }
    })

    $btnRefreshPreview.Add_Click({
        $null = $showSelection.Invoke($currentSelection.Path)
    })

    $btnRefreshStatus.Add_Click({
        $null = $refreshProvenanceStatus.Invoke()
    })

    $splitRight.Panel1.Controls.Add($treeBox)
    $splitRight.Panel2.Controls.Add($previewPanel)
    $splitMain.Panel2.Controls.Add($splitRight)
    $tabPage.Controls.Add($splitMain)

    if ($tree.Nodes.Count -gt 0) {
        $nodeQueue = New-Object System.Collections.Queue
        foreach ($rootNode in $tree.Nodes) {
            $nodeQueue.Enqueue($rootNode)
        }

        $firstFileNode = $null
        while ($nodeQueue.Count -gt 0 -and $null -eq $firstFileNode) {
            $candidateNode = [System.Windows.Forms.TreeNode]$nodeQueue.Dequeue()
            if ($candidateNode.Tag -and $candidateNode.Tag.IsFile) {
                $firstFileNode = $candidateNode
                break
            }

            foreach ($childNode in $candidateNode.Nodes) {
                $nodeQueue.Enqueue($childNode)
            }
        }

        if ($firstFileNode) {
            $tree.SelectedNode = $firstFileNode
            $null = $showSelection.Invoke($firstFileNode.Tag.Path)
        } else {
            $browser.DocumentText = Convert-MarkdownToHtml -Markdown "# $($Instance.Name)`n`nSelect a file from the Files tree to preview it." -Title $Instance.Name
            $rawBox.Text = ''
        }
    }

    $null = $refreshProvenanceStatus.Invoke()

    $ActiveLabel.Text = "Active instance: $($Instance.Name)"
    return $tabPage
}

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Reversa Manager'
$form.Size = New-Object System.Drawing.Size(1540, 980)
$form.MinimumSize = New-Object System.Drawing.Size(1280, 800)
$form.StartPosition = 'CenterScreen'
$form.BackColor = $script:Theme.FormBack
$form.ForeColor = $script:Theme.Text

$topPanel = New-Object System.Windows.Forms.Panel
$topPanel.Dock = 'Top'
$topPanel.Height = 430
$topPanel.BackColor = $script:Theme.PanelBack
$form.Controls.Add($topPanel)

$contentTabs = New-Object System.Windows.Forms.TabControl
$contentTabs.Dock = 'Fill'
$contentTabs.BackColor = $script:Theme.PanelAlt
$contentTabs.ForeColor = $script:Theme.Text
$form.Controls.Add($contentTabs)

$logBox = New-Object System.Windows.Forms.TextBox
$logBox.Dock = 'Bottom'
$logBox.Height = 130
$logBox.Multiline = $true
$logBox.ReadOnly = $true
$logBox.ScrollBars = 'Vertical'
$logBox.BackColor = $script:Theme.Surface
$logBox.ForeColor = $script:Theme.Text
$logBox.Font = New-Object System.Drawing.Font('Consolas', 10)
$form.Controls.Add($logBox)

function Write-Log {
    param([string]$Message)

    $timestamp = Get-Date -Format 'HH:mm:ss'
    $logBox.AppendText("[$timestamp] $Message`r`n")
}

$labelFont = New-Object System.Drawing.Font('Segoe UI', 9.5, [System.Drawing.FontStyle]::Bold)
$valueFont = New-Object System.Drawing.Font('Segoe UI', 10)

$lblBase = New-Object System.Windows.Forms.Label
$lblBase.Text = 'Base Reversa repo'
$lblBase.Location = New-Object System.Drawing.Point(18, 18)
$lblBase.AutoSize = $true
$lblBase.ForeColor = $script:Theme.Text
$lblBase.Font = $labelFont
$topPanel.Controls.Add($lblBase)

$txtBase = New-Object System.Windows.Forms.TextBox
$txtBase.Location = New-Object System.Drawing.Point(18, 42)
$txtBase.Size = New-Object System.Drawing.Size(760, 28)
$txtBase.BackColor = $script:Theme.Surface
$txtBase.ForeColor = $script:Theme.Text
$txtBase.Font = $valueFont
$txtBase.Text = 'C:\Projects\Reversa'
$topPanel.Controls.Add($txtBase)

$btnBaseBrowse = New-Object System.Windows.Forms.Button
$btnBaseBrowse.Text = 'Browse'
$btnBaseBrowse.Location = New-Object System.Drawing.Point(792, 40)
$btnBaseBrowse.Size = New-Object System.Drawing.Size(96, 32)
$btnBaseBrowse.BackColor = $script:Theme.PanelAlt
$btnBaseBrowse.ForeColor = $script:Theme.Text
$topPanel.Controls.Add($btnBaseBrowse)

$actionGroup = New-Object System.Windows.Forms.GroupBox
$actionGroup.Text = 'Primary Actions'
$actionGroup.Location = New-Object System.Drawing.Point(904, 12)
$actionGroup.Size = New-Object System.Drawing.Size(600, 72)
$actionGroup.ForeColor = $script:Theme.Text
$actionGroup.BackColor = $script:Theme.PanelBack
$topPanel.Controls.Add($actionGroup)

$lblVersion = New-Object System.Windows.Forms.Label
$lblVersion.Text = 'Base version: -'
$lblVersion.Location = New-Object System.Drawing.Point(12, 31)
$lblVersion.AutoSize = $true
$lblVersion.ForeColor = $script:Theme.Accent
$lblVersion.Font = $labelFont
$actionGroup.Controls.Add($lblVersion)

$lblTarget = New-Object System.Windows.Forms.Label
$lblTarget.Text = 'Target folder'
$lblTarget.Location = New-Object System.Drawing.Point(18, 84)
$lblTarget.AutoSize = $true
$lblTarget.ForeColor = $script:Theme.Text
$lblTarget.Font = $labelFont
$topPanel.Controls.Add($lblTarget)

$txtTarget = New-Object System.Windows.Forms.TextBox
$txtTarget.Location = New-Object System.Drawing.Point(18, 108)
$txtTarget.Size = New-Object System.Drawing.Size(760, 28)
$txtTarget.BackColor = $script:Theme.Surface
$txtTarget.ForeColor = $script:Theme.Text
$txtTarget.Font = $valueFont
$txtTarget.Text = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop'
$topPanel.Controls.Add($txtTarget)

$btnTargetBrowse = New-Object System.Windows.Forms.Button
$btnTargetBrowse.Text = 'Browse'
$btnTargetBrowse.Location = New-Object System.Drawing.Point(792, 106)
$btnTargetBrowse.Size = New-Object System.Drawing.Size(96, 32)
$btnTargetBrowse.BackColor = $script:Theme.PanelAlt
$btnTargetBrowse.ForeColor = $script:Theme.Text
$topPanel.Controls.Add($btnTargetBrowse)

$btnRefresh = New-Object System.Windows.Forms.Button
$btnRefresh.Text = 'Refresh Instances'
$btnRefresh.Location = New-Object System.Drawing.Point(164, 24)
$btnRefresh.Size = New-Object System.Drawing.Size(128, 32)
$btnRefresh.BackColor = $script:Theme.AccentSoft
$btnRefresh.ForeColor = $script:Theme.Text
$actionGroup.Controls.Add($btnRefresh)

$btnInstall = New-Object System.Windows.Forms.Button
$btnInstall.Text = 'Install Reversa'
$btnInstall.Location = New-Object System.Drawing.Point(304, 24)
$btnInstall.Size = New-Object System.Drawing.Size(128, 32)
$btnInstall.BackColor = $script:Theme.PanelAlt
$btnInstall.ForeColor = $script:Theme.Text
$actionGroup.Controls.Add($btnInstall)

$btnUpdate = New-Object System.Windows.Forms.Button
$btnUpdate.Text = 'Update Reversa'
$btnUpdate.Location = New-Object System.Drawing.Point(444, 24)
$btnUpdate.Size = New-Object System.Drawing.Size(128, 32)
$btnUpdate.BackColor = $script:Theme.PanelAlt
$btnUpdate.ForeColor = $script:Theme.Text
$actionGroup.Controls.Add($btnUpdate)

$btnHtmlExport = New-Object System.Windows.Forms.Button
$btnHtmlExport.Text = 'Bulk MD -> HTML'
$btnHtmlExport.Location = New-Object System.Drawing.Point(12, 224)
$btnHtmlExport.Size = New-Object System.Drawing.Size(136, 32)
$btnHtmlExport.BackColor = $script:Theme.PanelAlt
$btnHtmlExport.ForeColor = $script:Theme.Text
$topPanel.Controls.Add($btnHtmlExport)

$lblToolkitSource = New-Object System.Windows.Forms.Label
$lblToolkitSource.Text = 'Traceability toolkit source'
$lblToolkitSource.Location = New-Object System.Drawing.Point(18, 150)
$lblToolkitSource.AutoSize = $true
$lblToolkitSource.ForeColor = $script:Theme.Text
$lblToolkitSource.Font = $labelFont
$topPanel.Controls.Add($lblToolkitSource)

$txtToolkitSource = New-Object System.Windows.Forms.TextBox
$txtToolkitSource.Location = New-Object System.Drawing.Point(18, 174)
$txtToolkitSource.Size = New-Object System.Drawing.Size(760, 28)
$txtToolkitSource.BackColor = $script:Theme.Surface
$txtToolkitSource.ForeColor = $script:Theme.Text
$txtToolkitSource.Font = $valueFont
$txtToolkitSource.Text = Get-TraceabilityToolkitDefaultSource
$topPanel.Controls.Add($txtToolkitSource)

$btnToolkitSourceBrowse = New-Object System.Windows.Forms.Button
$btnToolkitSourceBrowse.Text = 'Browse'
$btnToolkitSourceBrowse.Location = New-Object System.Drawing.Point(792, 172)
$btnToolkitSourceBrowse.Size = New-Object System.Drawing.Size(96, 32)
$btnToolkitSourceBrowse.BackColor = $script:Theme.PanelAlt
$btnToolkitSourceBrowse.ForeColor = $script:Theme.Text
$topPanel.Controls.Add($btnToolkitSourceBrowse)

$toolkitGroup = New-Object System.Windows.Forms.GroupBox
$toolkitGroup.Text = 'Traceability Toolkit'
$toolkitGroup.Location = New-Object System.Drawing.Point(904, 194)
$toolkitGroup.Size = New-Object System.Drawing.Size(600, 144)
$toolkitGroup.ForeColor = $script:Theme.Text
$toolkitGroup.BackColor = $script:Theme.PanelBack
$topPanel.Controls.Add($toolkitGroup)

$lblToolkitTarget = New-Object System.Windows.Forms.Label
$lblToolkitTarget.Text = 'Resolved target traceability folder'
$lblToolkitTarget.Location = New-Object System.Drawing.Point(12, 24)
$lblToolkitTarget.AutoSize = $true
$lblToolkitTarget.ForeColor = $script:Theme.Text
$toolkitGroup.Controls.Add($lblToolkitTarget)

$txtToolkitTarget = New-Object System.Windows.Forms.TextBox
$txtToolkitTarget.Location = New-Object System.Drawing.Point(12, 44)
$txtToolkitTarget.Size = New-Object System.Drawing.Size(420, 26)
$txtToolkitTarget.ReadOnly = $true
$txtToolkitTarget.BackColor = $script:Theme.Surface
$txtToolkitTarget.ForeColor = $script:Theme.Text
$txtToolkitTarget.Font = $valueFont
$toolkitGroup.Controls.Add($txtToolkitTarget)

$cmbToolkitAction = New-Object System.Windows.Forms.ComboBox
$cmbToolkitAction.Location = New-Object System.Drawing.Point(12, 76)
$cmbToolkitAction.Size = New-Object System.Drawing.Size(420, 26)
$cmbToolkitAction.DropDownStyle = 'DropDownList'
$cmbToolkitAction.BackColor = $script:Theme.Surface
$cmbToolkitAction.ForeColor = $script:Theme.Text
[void]$cmbToolkitAction.Items.AddRange(@('Audit Provenance Setup', 'Build Versions Index', 'Create Snapshot', 'Compare Snapshots'))
$cmbToolkitAction.SelectedIndex = 0
$toolkitGroup.Controls.Add($cmbToolkitAction)

$btnToolkitInstall = New-Object System.Windows.Forms.Button
$btnToolkitInstall.Text = 'Install Toolkit'
$btnToolkitInstall.Location = New-Object System.Drawing.Point(446, 40)
$btnToolkitInstall.Size = New-Object System.Drawing.Size(138, 28)
$btnToolkitInstall.BackColor = $script:Theme.AccentSoft
$btnToolkitInstall.ForeColor = $script:Theme.Text
$toolkitGroup.Controls.Add($btnToolkitInstall)

$btnToolkitRun = New-Object System.Windows.Forms.Button
$btnToolkitRun.Text = 'Run Action'
$btnToolkitRun.Location = New-Object System.Drawing.Point(446, 74)
$btnToolkitRun.Size = New-Object System.Drawing.Size(138, 28)
$btnToolkitRun.BackColor = $script:Theme.PanelAlt
$btnToolkitRun.ForeColor = $script:Theme.Text
$toolkitGroup.Controls.Add($btnToolkitRun)

$btnToolkitInstallAuditOpen = New-Object System.Windows.Forms.Button
$btnToolkitInstallAuditOpen.Text = 'Install + Audit + Open'
$btnToolkitInstallAuditOpen.Location = New-Object System.Drawing.Point(446, 106)
$btnToolkitInstallAuditOpen.Size = New-Object System.Drawing.Size(138, 28)
$btnToolkitInstallAuditOpen.BackColor = $script:Theme.PanelAlt
$btnToolkitInstallAuditOpen.ForeColor = $script:Theme.Text
$toolkitGroup.Controls.Add($btnToolkitInstallAuditOpen)

$projectFlowGroup = New-Object System.Windows.Forms.GroupBox
$projectFlowGroup.Text = 'Project Start Flow'
$projectFlowGroup.Location = New-Object System.Drawing.Point(18, 214)
$projectFlowGroup.Size = New-Object System.Drawing.Size(870, 140)
$projectFlowGroup.ForeColor = $script:Theme.Text
$projectFlowGroup.BackColor = $script:Theme.PanelBack
$topPanel.Controls.Add($projectFlowGroup)

$lblProjectMode = New-Object System.Windows.Forms.Label
$lblProjectMode.Text = 'Project mode'
$lblProjectMode.Location = New-Object System.Drawing.Point(12, 28)
$lblProjectMode.AutoSize = $true
$lblProjectMode.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($lblProjectMode)

$cmbProjectMode = New-Object System.Windows.Forms.ComboBox
$cmbProjectMode.Location = New-Object System.Drawing.Point(12, 48)
$cmbProjectMode.Size = New-Object System.Drawing.Size(146, 26)
$cmbProjectMode.DropDownStyle = 'DropDownList'
$cmbProjectMode.BackColor = $script:Theme.Surface
$cmbProjectMode.ForeColor = $script:Theme.Text
[void]$cmbProjectMode.Items.AddRange(@('Existing Project', 'New Project'))
$cmbProjectMode.SelectedIndex = 0
$projectFlowGroup.Controls.Add($cmbProjectMode)

$lblExistingProject = New-Object System.Windows.Forms.Label
$lblExistingProject.Text = 'Existing project'
$lblExistingProject.Location = New-Object System.Drawing.Point(172, 28)
$lblExistingProject.AutoSize = $true
$lblExistingProject.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($lblExistingProject)

$cmbExistingProject = New-Object System.Windows.Forms.ComboBox
$cmbExistingProject.Location = New-Object System.Drawing.Point(172, 48)
$cmbExistingProject.Size = New-Object System.Drawing.Size(280, 26)
$cmbExistingProject.DropDownStyle = 'DropDownList'
$cmbExistingProject.BackColor = $script:Theme.Surface
$cmbExistingProject.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($cmbExistingProject)

$lblEngineChoice = New-Object System.Windows.Forms.Label
$lblEngineChoice.Text = 'Agentic system'
$lblEngineChoice.Location = New-Object System.Drawing.Point(468, 28)
$lblEngineChoice.AutoSize = $true
$lblEngineChoice.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($lblEngineChoice)

$cmbEngineChoice = New-Object System.Windows.Forms.ComboBox
$cmbEngineChoice.Location = New-Object System.Drawing.Point(468, 48)
$cmbEngineChoice.Size = New-Object System.Drawing.Size(146, 26)
$cmbEngineChoice.DropDownStyle = 'DropDownList'
$cmbEngineChoice.BackColor = $script:Theme.Surface
$cmbEngineChoice.ForeColor = $script:Theme.Text
[void]$cmbEngineChoice.Items.AddRange(@('Both', 'GitHub Copilot', 'Claude Code'))
$cmbEngineChoice.SelectedIndex = 0
$projectFlowGroup.Controls.Add($cmbEngineChoice)

$lblPreviewMode = New-Object System.Windows.Forms.Label
$lblPreviewMode.Text = 'Preview mode'
$lblPreviewMode.Location = New-Object System.Drawing.Point(628, 28)
$lblPreviewMode.AutoSize = $true
$lblPreviewMode.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($lblPreviewMode)

$cmbPreviewMode = New-Object System.Windows.Forms.ComboBox
$cmbPreviewMode.Location = New-Object System.Drawing.Point(628, 48)
$cmbPreviewMode.Size = New-Object System.Drawing.Size(146, 26)
$cmbPreviewMode.DropDownStyle = 'DropDownList'
$cmbPreviewMode.BackColor = $script:Theme.Surface
$cmbPreviewMode.ForeColor = $script:Theme.Text
[void]$cmbPreviewMode.Items.AddRange(@('In GUI', 'Open Externally'))
$cmbPreviewMode.SelectedIndex = 0
$projectFlowGroup.Controls.Add($cmbPreviewMode)

$btnStartWorkflow = New-Object System.Windows.Forms.Button
$btnStartWorkflow.Text = 'Start Workflow'
$btnStartWorkflow.Location = New-Object System.Drawing.Point(780, 44)
$btnStartWorkflow.Size = New-Object System.Drawing.Size(78, 32)
$btnStartWorkflow.BackColor = $script:Theme.AccentSoft
$btnStartWorkflow.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($btnStartWorkflow)

$chkInstallToolkitOnStart = New-Object System.Windows.Forms.CheckBox
$chkInstallToolkitOnStart.Location = New-Object System.Drawing.Point(12, 92)
$chkInstallToolkitOnStart.Size = New-Object System.Drawing.Size(220, 24)
$chkInstallToolkitOnStart.Text = 'Install traceability toolkit on start'
$chkInstallToolkitOnStart.Checked = $true
$chkInstallToolkitOnStart.ForeColor = $script:Theme.Text
$chkInstallToolkitOnStart.BackColor = $script:Theme.PanelBack
$projectFlowGroup.Controls.Add($chkInstallToolkitOnStart)

$chkAuditAfterInstall = New-Object System.Windows.Forms.CheckBox
$chkAuditAfterInstall.Location = New-Object System.Drawing.Point(246, 92)
$chkAuditAfterInstall.Size = New-Object System.Drawing.Size(200, 24)
$chkAuditAfterInstall.Text = 'Run audit after toolkit install'
$chkAuditAfterInstall.Checked = $true
$chkAuditAfterInstall.ForeColor = $script:Theme.Text
$chkAuditAfterInstall.BackColor = $script:Theme.PanelBack
$projectFlowGroup.Controls.Add($chkAuditAfterInstall)

$chkAutoRefresh = New-Object System.Windows.Forms.CheckBox
$chkAutoRefresh.Location = New-Object System.Drawing.Point(468, 92)
$chkAutoRefresh.Size = New-Object System.Drawing.Size(180, 24)
$chkAutoRefresh.Text = 'Auto-refresh results view'
$chkAutoRefresh.Checked = $false
$chkAutoRefresh.ForeColor = $script:Theme.Text
$chkAutoRefresh.BackColor = $script:Theme.PanelBack
$projectFlowGroup.Controls.Add($chkAutoRefresh)

$btnOpenVSCode = New-Object System.Windows.Forms.Button
$btnOpenVSCode.Text = 'Open In VS Code'
$btnOpenVSCode.Location = New-Object System.Drawing.Point(654, 88)
$btnOpenVSCode.Size = New-Object System.Drawing.Size(120, 30)
$btnOpenVSCode.BackColor = $script:Theme.PanelAlt
$btnOpenVSCode.ForeColor = $script:Theme.Text
$projectFlowGroup.Controls.Add($btnOpenVSCode)

$activeInstanceLabel = New-Object System.Windows.Forms.Label
$activeInstanceLabel.Text = 'Active instance: -'
$activeInstanceLabel.Location = New-Object System.Drawing.Point(18, 458)
$activeInstanceLabel.AutoSize = $true
$activeInstanceLabel.ForeColor = $script:Theme.Accent
$activeInstanceLabel.Font = $labelFont
$topPanel.Controls.Add($activeInstanceLabel)

$installGroup = New-Object System.Windows.Forms.GroupBox
$installGroup.Text = 'Install Defaults'
$installGroup.Location = New-Object System.Drawing.Point(904, 92)
$installGroup.Size = New-Object System.Drawing.Size(600, 102)
$installGroup.ForeColor = $script:Theme.Text
$installGroup.BackColor = $script:Theme.PanelBack
$topPanel.Controls.Add($installGroup)

$workflowGroup = New-Object System.Windows.Forms.GroupBox
$workflowGroup.Text = 'Recommended Workflow'
$workflowGroup.Location = New-Object System.Drawing.Point(18, 360)
$workflowGroup.Size = New-Object System.Drawing.Size(1486, 90)
$workflowGroup.ForeColor = $script:Theme.Text
$workflowGroup.BackColor = $script:Theme.PanelBack
$topPanel.Controls.Add($workflowGroup)

$workflowLabel = New-Object System.Windows.Forms.Label
$workflowLabel.Location = New-Object System.Drawing.Point(12, 24)
$workflowLabel.Size = New-Object System.Drawing.Size(1458, 60)
$workflowLabel.ForeColor = $script:Theme.Text
$workflowLabel.BackColor = $script:Theme.PanelBack
$workflowLabel.Font = New-Object System.Drawing.Font('Segoe UI', 9)
$workflowLabel.Text = @(
    '1. Select an existing project or switch to New Project, then choose the agentic system and preview mode.',
    '2. Start Workflow installs Reversa when needed, optionally adds the traceability toolkit + audit, refreshes the GUI, and opens the folder in VS Code.',
    '3. Use the instance tabs below for live review. Quick Actions give direct control over the project, output, traceability, plan, and reports.'
) -join [Environment]::NewLine
$workflowGroup.Controls.Add($workflowLabel)

$txtProjectName = New-Object System.Windows.Forms.TextBox
$txtProjectName.Location = New-Object System.Drawing.Point(12, 32)
$txtProjectName.Size = New-Object System.Drawing.Size(170, 26)
$txtProjectName.BackColor = $script:Theme.Surface
$txtProjectName.ForeColor = $script:Theme.Text
$txtProjectName.Font = $valueFont
$installGroup.Controls.Add($txtProjectName)

$txtUserName = New-Object System.Windows.Forms.TextBox
$txtUserName.Location = New-Object System.Drawing.Point(194, 32)
$txtUserName.Size = New-Object System.Drawing.Size(120, 26)
$txtUserName.BackColor = $script:Theme.Surface
$txtUserName.ForeColor = $script:Theme.Text
$txtUserName.Font = $valueFont
$installGroup.Controls.Add($txtUserName)

$txtOutputFolder = New-Object System.Windows.Forms.TextBox
$txtOutputFolder.Location = New-Object System.Drawing.Point(326, 32)
$txtOutputFolder.Size = New-Object System.Drawing.Size(140, 26)
$txtOutputFolder.BackColor = $script:Theme.Surface
$txtOutputFolder.ForeColor = $script:Theme.Text
$txtOutputFolder.Font = $valueFont
$installGroup.Controls.Add($txtOutputFolder)

$cmbAnswerMode = New-Object System.Windows.Forms.ComboBox
$cmbAnswerMode.Location = New-Object System.Drawing.Point(478, 32)
$cmbAnswerMode.Size = New-Object System.Drawing.Size(108, 26)
$cmbAnswerMode.DropDownStyle = 'DropDownList'
$cmbAnswerMode.BackColor = $script:Theme.Surface
$cmbAnswerMode.ForeColor = $script:Theme.Text
[void]$cmbAnswerMode.Items.AddRange(@('chat', 'file'))
$installGroup.Controls.Add($cmbAnswerMode)

$chkProvenanceIndexing = New-Object System.Windows.Forms.CheckBox
$chkProvenanceIndexing.Location = New-Object System.Drawing.Point(12, 66)
$chkProvenanceIndexing.Size = New-Object System.Drawing.Size(400, 24)
$chkProvenanceIndexing.Text = 'Enable PDD provenance + business-rule indexing'
$chkProvenanceIndexing.Checked = $true
$chkProvenanceIndexing.ForeColor = $script:Theme.Text
$chkProvenanceIndexing.BackColor = $script:Theme.PanelBack
$installGroup.Controls.Add($chkProvenanceIndexing)

$folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog
$autoRefreshTimer = New-Object System.Windows.Forms.Timer
$autoRefreshTimer.Interval = 15000
$script:PreviewMode = 'In GUI'
$script:ProjectPicker = @{}

function Refresh-ProjectPicker {
    $rootFolder = ''
    $target = $txtTarget.Text.Trim()
    if ($target -and (Test-Path -LiteralPath $target)) {
        $rootFolder = Split-Path -Parent $target
    }
    if (-not $rootFolder) {
        $rootFolder = Get-DefaultWorkspaceRoot
    }

    $script:ProjectPicker = @{}
    $cmbExistingProject.Items.Clear()
    foreach ($project in @(Get-ProjectCandidates -RootFolder $rootFolder)) {
        $label = if ($project.Installed) { '{0}  [installed]' -f $project.Name } else { $project.Name }
        $script:ProjectPicker[$label] = $project.Path
        [void]$cmbExistingProject.Items.Add($label)
    }

    if ($cmbExistingProject.Items.Count -gt 0 -and $cmbExistingProject.SelectedIndex -lt 0) {
        $cmbExistingProject.SelectedIndex = 0
    }
}

function Update-ProjectModeState {
    $isExistingProject = ([string]$cmbProjectMode.SelectedItem) -eq 'Existing Project'
    $cmbExistingProject.Enabled = $isExistingProject
    $btnTargetBrowse.Enabled = -not $isExistingProject
}

function Start-Workflow {
    $isExistingProject = ([string]$cmbProjectMode.SelectedItem) -eq 'Existing Project'
    $target = $txtTarget.Text.Trim()

    if ($isExistingProject) {
        $selectedLabel = [string]$cmbExistingProject.SelectedItem
        if (-not [string]::IsNullOrWhiteSpace($selectedLabel) -and $script:ProjectPicker.ContainsKey($selectedLabel)) {
            $target = [string]$script:ProjectPicker[$selectedLabel]
            $txtTarget.Text = $target
        }
    }

    if ([string]::IsNullOrWhiteSpace($target)) {
        throw 'Select or enter a target project folder before starting the workflow.'
    }

    if (-not (Test-Path -LiteralPath $target)) {
        if ($isExistingProject) {
            throw 'The selected existing project folder was not found.'
        }

        $null = New-Item -ItemType Directory -Path $target -Force
        Write-Log "Created project folder: $target"
    }

    $baseRepo = $txtBase.Text.Trim()
    if (-not (Test-Path -LiteralPath $baseRepo)) {
        throw 'Select a valid base Reversa repository before starting the workflow.'
    }

    $engines = @(Get-SelectedEngineIds -Selection ([string]$cmbEngineChoice.SelectedItem))
    $statePath = Join-Path $target '.reversa\state.json'
    if (-not (Test-Path -LiteralPath $statePath)) {
        $answers = [ordered]@{
            project_name = $txtProjectName.Text.Trim()
            user_name = $txtUserName.Text.Trim()
            chat_language = 'English'
            doc_language = 'English'
            output_folder = $txtOutputFolder.Text.Trim()
            answer_mode = [string]$cmbAnswerMode.SelectedItem
            enable_provenance_indexing = [bool]$chkProvenanceIndexing.Checked
            git_strategy = 'gitignore'
            engines = $engines
            agents = $script:DefaultAgents
        }

        if ([string]::IsNullOrWhiteSpace([string]$answers.project_name)) {
            $answers.project_name = Split-Path -Leaf $target
        }
        if ([string]::IsNullOrWhiteSpace([string]$answers.user_name)) {
            $answers.user_name = $env:USERNAME
        }
        if ([string]::IsNullOrWhiteSpace([string]$answers.output_folder)) {
            $answers.output_folder = '_reversa_sdd'
        }
        if ([string]::IsNullOrWhiteSpace([string]$answers.answer_mode)) {
            $answers.answer_mode = 'chat'
        }

        Write-Log "Installing Reversa into $target"
        $installResult = Invoke-ReversaInstall -BaseRepo $baseRepo -TargetFolder $target -Answers $answers
        $combinedInstall = ($installResult.StdOut + [Environment]::NewLine + $installResult.StdErr).Trim()
        if ($combinedInstall) { Write-Log $combinedInstall }
        if ($installResult.ExitCode -ne 0) {
            throw "Install failed with exit code $($installResult.ExitCode)."
        }
    }
    else {
        Set-TraceabilityPreference -TargetFolder $target -Enabled ([bool]$chkProvenanceIndexing.Checked)
    }

    if ([bool]$chkInstallToolkitOnStart.Checked) {
        $source = $txtToolkitSource.Text.Trim()
        if (-not (Test-Path -LiteralPath $source)) {
            throw 'Select a valid traceability toolkit source folder before starting the workflow.'
        }

        if ([bool]$chkAuditAfterInstall.Checked) {
            $toolkitResult = Install-AuditOpenTraceabilityToolkit -SourceFolder $source -TargetFolder $target
            $combinedAudit = ($toolkitResult.Audit.StdOut + [Environment]::NewLine + $toolkitResult.Audit.StdErr).Trim()
            if ($combinedAudit) { Write-Log $combinedAudit }
            if ($toolkitResult.Audit.ExitCode -ne 0) {
                throw "Toolkit audit failed with exit code $($toolkitResult.Audit.ExitCode)."
            }
        }
        else {
            $toolkitInstall = Install-TraceabilityToolkit -SourceFolder $source -TargetFolder $target
            Write-Log ("Toolkit installed: {0} files -> {1}" -f $toolkitInstall.InstalledCount, $toolkitInstall.DestinationFolder)
        }
    }

    Refresh-DefaultsFromTarget
    Refresh-ProjectPicker
    Refresh-InstancesView

    $launchResult = Launch-VSCodeWorkspace -TargetFolder $target
    $combinedLaunch = ($launchResult.StdOut + [Environment]::NewLine + $launchResult.StdErr).Trim()
    if ($combinedLaunch) { Write-Log $combinedLaunch }
    Write-Log ("Workflow started for {0} using {1}" -f $target, ([string]$cmbEngineChoice.SelectedItem))
}

function Refresh-DefaultsFromTarget {
    $target = $txtTarget.Text.Trim()
    if (-not $target -or -not (Test-Path -LiteralPath $target)) {
        $txtToolkitTarget.Text = ''
        return
    }

    $defaults = Get-TargetDefaults -TargetFolder $target
    $txtProjectName.Text = $defaults.ProjectName
    $txtUserName.Text = $defaults.UserName
    $txtOutputFolder.Text = $defaults.OutputFolder
    $cmbAnswerMode.SelectedItem = $defaults.AnswerMode
    $chkProvenanceIndexing.Checked = $defaults.EnableProvenanceIndexing
    if (@($defaults.Engines).Count -eq 1) {
        if ($defaults.Engines[0] -eq 'github-copilot') { $cmbEngineChoice.SelectedItem = 'GitHub Copilot' }
        elseif ($defaults.Engines[0] -eq 'claude-code') { $cmbEngineChoice.SelectedItem = 'Claude Code' }
        else { $cmbEngineChoice.SelectedItem = 'Both' }
    } else {
        $cmbEngineChoice.SelectedItem = 'Both'
    }
    $txtToolkitTarget.Text = Get-TraceabilityToolkitTargetFolder -TargetFolder $target
}

function Refresh-BaseVersion {
    $version = Get-ReversaBaseVersion -BaseRepoPath $txtBase.Text.Trim()
    if ($version) {
        $lblVersion.Text = "Base version: $version"
    } else {
        $lblVersion.Text = 'Base version: unavailable'
    }
}

function Refresh-InstancesView {
    $contentTabs.TabPages.Clear()
    $activeInstanceLabel.Text = 'Active instance: -'
    $target = $txtTarget.Text.Trim()
    if (-not $target -or -not (Test-Path -LiteralPath $target)) {
        Write-Log 'Target folder does not exist.'
        return
    }

    $instances = Get-ReversaInstances -TargetFolder $target
    if (-not $instances -or $instances.Count -eq 0) {
        Write-Log 'No Reversa instances found for the selected target.'
        return
    }

    foreach ($instance in $instances) {
        [void]$contentTabs.TabPages.Add((Build-InstanceTab -Instance $instance -ActiveLabel $activeInstanceLabel))
    }

    if ($contentTabs.TabPages.Count -gt 0) {
        $contentTabs.SelectedIndex = 0
        $activeInstanceLabel.Text = "Active instance: $($contentTabs.SelectedTab.Text)"
    }

    Write-Log ("Loaded {0} instance(s) for {1}." -f $instances.Count, $target)
}

$contentTabs.Add_SelectedIndexChanged({
    if ($contentTabs.SelectedTab) {
        $activeInstanceLabel.Text = "Active instance: $($contentTabs.SelectedTab.Text)"
    }
})

$btnBaseBrowse.Add_Click({
    if ($folderDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $txtBase.Text = $folderDialog.SelectedPath
        Refresh-BaseVersion
    }
})

$btnTargetBrowse.Add_Click({
    if ($folderDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $txtTarget.Text = $folderDialog.SelectedPath
        Refresh-DefaultsFromTarget
        Refresh-ProjectPicker
        Refresh-InstancesView
    }
})

$cmbProjectMode.Add_SelectedIndexChanged({
    Update-ProjectModeState
})

$cmbExistingProject.Add_SelectedIndexChanged({
    $selectedLabel = [string]$cmbExistingProject.SelectedItem
    if ($selectedLabel -and $script:ProjectPicker.ContainsKey($selectedLabel)) {
        $txtTarget.Text = [string]$script:ProjectPicker[$selectedLabel]
        Refresh-DefaultsFromTarget
        Refresh-InstancesView
    }
})

$cmbPreviewMode.Add_SelectedIndexChanged({
    $script:PreviewMode = [string]$cmbPreviewMode.SelectedItem
})

$btnOpenVSCode.Add_Click({
    try {
        $target = $txtTarget.Text.Trim()
        if (-not (Test-Path -LiteralPath $target)) {
            throw 'Select a valid target folder before opening VS Code.'
        }

        $result = Launch-VSCodeWorkspace -TargetFolder $target
        $combined = ($result.StdOut + [Environment]::NewLine + $result.StdErr).Trim()
        if ($combined) { Write-Log $combined }
        Write-Log ("Opened VS Code for {0}" -f $target)
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Open VS Code Failed', 'OK', 'Error') | Out-Null
    }
})

$btnStartWorkflow.Add_Click({
    try {
        Start-Workflow
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Start Workflow Failed', 'OK', 'Error') | Out-Null
    }
})

$autoRefreshTimer.Add_Tick({
    if ([bool]$chkAutoRefresh.Checked) {
        Refresh-InstancesView
    }
})
$autoRefreshTimer.Start()

$btnToolkitSourceBrowse.Add_Click({
    if ($folderDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $txtToolkitSource.Text = $folderDialog.SelectedPath
    }
})

$btnRefresh.Add_Click({
    Refresh-BaseVersion
    Refresh-DefaultsFromTarget
    Refresh-ProjectPicker
    Refresh-InstancesView
})

$btnToolkitInstall.Add_Click({
    try {
        $target = $txtTarget.Text.Trim()
        $source = $txtToolkitSource.Text.Trim()
        if (-not (Test-Path -LiteralPath $target)) {
            throw 'Select a valid target folder before installing the traceability toolkit.'
        }
        if (-not (Test-Path -LiteralPath $source)) {
            throw 'Select a valid traceability toolkit source folder before installing.'
        }

        Write-Log "Installing traceability toolkit into $target"
        $installResult = Install-TraceabilityToolkit -SourceFolder $source -TargetFolder $target
        Write-Log ("Toolkit installed: {0} files -> {1}" -f $installResult.InstalledCount, $installResult.DestinationFolder)
        if ($installResult.OverwrittenCount -gt 0) {
            Write-Log ("Backed up {0} overwritten file(s) to {1}" -f $installResult.OverwrittenCount, $installResult.BackupFolder)
        }

        $txtToolkitTarget.Text = $installResult.DestinationFolder
        Refresh-InstancesView
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Toolkit Install Failed', 'OK', 'Error') | Out-Null
    }
})

$btnToolkitRun.Add_Click({
    try {
        $target = $txtTarget.Text.Trim()
        if (-not (Test-Path -LiteralPath $target)) {
            throw 'Select a valid target folder before running a toolkit action.'
        }

        $action = [string]$cmbToolkitAction.SelectedItem
        if ([string]::IsNullOrWhiteSpace($action)) {
            throw 'Select a toolkit action to run.'
        }

        Write-Log ("Running traceability toolkit action: {0}" -f $action)
        switch ($action) {
            'Create Snapshot' {
                $snapshotOptions = Prompt-ForTraceabilitySnapshotOptions
                if ($null -eq $snapshotOptions) {
                    Write-Log 'Create Snapshot canceled.'
                    return
                }

                $result = Invoke-TraceabilitySnapshotCreate -TargetFolder $target -BuildMethod $snapshotOptions.BuildMethod -BuildScope $snapshotOptions.BuildScope -SourceInputs $snapshotOptions.SourceInputs -SupportingSnapshots $snapshotOptions.SupportingSnapshots -ChangeSummary $snapshotOptions.ChangeSummary
                $combined = ($result.StdOut + [Environment]::NewLine + $result.StdErr).Trim()
                if ($combined) { Write-Log $combined }
                if ($result.ExitCode -ne 0) {
                    throw "Create Snapshot failed with exit code $($result.ExitCode)."
                }
                if (-not [string]::IsNullOrWhiteSpace($result.SnapshotPath)) {
                    Write-Log ("Snapshot path: {0}" -f $result.SnapshotPath)
                    Open-PathIfExists -Path $result.SnapshotPath
                }
            }
            'Compare Snapshots' {
                $versionsRoot = Join-Path (Get-TraceabilityToolkitTargetFolder -TargetFolder $target) 'versions'
                $leftSnapshot = Select-FolderWithPrompt -Description 'Select the left snapshot folder' -InitialPath $versionsRoot
                if ([string]::IsNullOrWhiteSpace($leftSnapshot)) {
                    Write-Log 'Compare Snapshots canceled before selecting the left snapshot.'
                    return
                }
                $rightSnapshot = Select-FolderWithPrompt -Description 'Select the right snapshot folder' -InitialPath $versionsRoot
                if ([string]::IsNullOrWhiteSpace($rightSnapshot)) {
                    Write-Log 'Compare Snapshots canceled before selecting the right snapshot.'
                    return
                }

                $result = Invoke-TraceabilitySnapshotCompare -TargetFolder $target -LeftSnapshotPath $leftSnapshot -RightSnapshotPath $rightSnapshot
                $combined = ($result.StdOut + [Environment]::NewLine + $result.StdErr).Trim()
                if ($combined) { Write-Log $combined }
                if ($result.ExitCode -ne 0) {
                    throw "Compare Snapshots failed with exit code $($result.ExitCode)."
                }
                if (-not [string]::IsNullOrWhiteSpace($result.ReportPath)) {
                    Write-Log ("Compare report: {0}" -f $result.ReportPath)
                    Open-PathIfExists -Path $result.ReportPath
                }
            }
            default {
                $result = Invoke-TraceabilityToolkitAction -TargetFolder $target -Action $action
                $combined = ($result.StdOut + [Environment]::NewLine + $result.StdErr).Trim()
                if ($combined) { Write-Log $combined }
                if ($result.ExitCode -ne 0) {
                    throw "Toolkit action failed with exit code $($result.ExitCode)."
                }
            }
        }

        Refresh-InstancesView
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Toolkit Action Failed', 'OK', 'Error') | Out-Null
    }
})

$btnToolkitInstallAuditOpen.Add_Click({
    try {
        $target = $txtTarget.Text.Trim()
        $source = $txtToolkitSource.Text.Trim()
        if (-not (Test-Path -LiteralPath $target)) {
            throw 'Select a valid target folder before running Install + Audit + Open.'
        }
        if (-not (Test-Path -LiteralPath $source)) {
            throw 'Select a valid traceability toolkit source folder before running Install + Audit + Open.'
        }

        Write-Log ("Running Install + Audit + Open for {0}" -f $target)
        $result = Install-AuditOpenTraceabilityToolkit -SourceFolder $source -TargetFolder $target
        $txtToolkitTarget.Text = $result.Install.DestinationFolder
        Write-Log ("Toolkit installed: {0} files -> {1}" -f $result.Install.InstalledCount, $result.Install.DestinationFolder)

        $combined = ($result.Audit.StdOut + [Environment]::NewLine + $result.Audit.StdErr).Trim()
        if ($combined) { Write-Log $combined }
        if ($result.Audit.ExitCode -ne 0) {
            throw "Audit failed with exit code $($result.Audit.ExitCode)."
        }

        if (Test-Path -LiteralPath $result.ReportPath) {
            Write-Log ("Opened audit report: {0}" -f $result.ReportPath)
        }

        Refresh-InstancesView
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Install + Audit + Open Failed', 'OK', 'Error') | Out-Null
    }
})

$btnInstall.Add_Click({
    try {
        $target = $txtTarget.Text.Trim()
        $baseRepo = $txtBase.Text.Trim()
        if (-not (Test-Path -LiteralPath $target)) {
            throw 'Select a valid target folder before installing.'
        }
        if (-not (Test-Path -LiteralPath $baseRepo)) {
            throw 'Select a valid base Reversa repository before installing.'
        }
        if (Test-Path -LiteralPath (Join-Path $target '.reversa\state.json')) {
            [System.Windows.Forms.MessageBox]::Show('Reversa is already installed in this target. Use Update Reversa instead.', 'Already Installed', 'OK', 'Information') | Out-Null
            return
        }

        $answers = [ordered]@{
            project_name = $txtProjectName.Text.Trim()
            user_name = $txtUserName.Text.Trim()
            chat_language = 'English'
            doc_language = 'English'
            output_folder = $txtOutputFolder.Text.Trim()
            answer_mode = [string]$cmbAnswerMode.SelectedItem
            enable_provenance_indexing = [bool]$chkProvenanceIndexing.Checked
            git_strategy = 'gitignore'
            engines = @(Get-SelectedEngineIds -Selection ([string]$cmbEngineChoice.SelectedItem))
            agents = $script:DefaultAgents
        }

        Write-Log "Installing Reversa into $target"
        $result = Invoke-ReversaInstall -BaseRepo $baseRepo -TargetFolder $target -Answers $answers
        $combined = ($result.StdOut + [Environment]::NewLine + $result.StdErr).Trim()
        if ($combined) { Write-Log $combined }
        if ($result.ExitCode -ne 0) {
            throw "Install failed with exit code $($result.ExitCode)."
        }
        Refresh-InstancesView
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Install Failed', 'OK', 'Error') | Out-Null
    }
})

$btnUpdate.Add_Click({
    try {
        $target = $txtTarget.Text.Trim()
        $baseRepo = $txtBase.Text.Trim()
        if (-not (Test-Path -LiteralPath $target)) {
            throw 'Select a valid target folder before updating.'
        }
        if (-not (Test-Path -LiteralPath $baseRepo)) {
            throw 'Select a valid base Reversa repository before updating.'
        }
        if (-not (Test-Path -LiteralPath (Join-Path $target '.reversa\state.json'))) {
            throw 'Reversa is not installed in the selected target.'
        }

        Write-Log "Updating Reversa in $target"
        $result = Invoke-ReversaUpdate -BaseRepo $baseRepo -TargetFolder $target
        $combined = ($result.StdOut + [Environment]::NewLine + $result.StdErr).Trim()
        if ($combined) { Write-Log $combined }
        if ($result.ExitCode -ne 0) {
            throw "Update failed with exit code $($result.ExitCode)."
        }
        Set-TraceabilityPreference -TargetFolder $target -Enabled ([bool]$chkProvenanceIndexing.Checked)
        Refresh-InstancesView
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Update Failed', 'OK', 'Error') | Out-Null
    }
})

$btnHtmlExport.Add_Click({
    try {
        if (-not $contentTabs.SelectedTab -or -not $contentTabs.SelectedTab.Tag) {
            throw 'Select an instance tab before running the bulk markdown export.'
        }

        $instance = $contentTabs.SelectedTab.Tag.Instance
        $result = Export-MarkdownCatalogToHtml -Instance $instance
        Write-Log ("Exported {0} markdown file(s) to HTML under {1}. Catalog: {2}" -f $result.MarkdownCount, $result.HtmlRoot, $result.CatalogPath)
        Refresh-InstancesView
    } catch {
        Write-Log $_.Exception.Message
        [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Bulk Export Failed', 'OK', 'Error') | Out-Null
    }
})

Refresh-BaseVersion
Refresh-DefaultsFromTarget
Refresh-ProjectPicker
Update-ProjectModeState
Refresh-InstancesView
Write-Log 'Reversa Manager started.'

[void]$form.ShowDialog()