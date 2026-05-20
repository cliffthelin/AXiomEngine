# Description: Remove the old task (if applicable) and create a new one.
# OctopusDeploy will automatically execute this during deployment.

# Remove the old instance/version of the task.
Get-ScheduledTask -TaskName "Import" -TaskPath "\Acadience\" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# Dynamically determine gMSA.
$suffix = $OctopusParameters["Octopus.Environment.Name"].Substring(0, 1)
$gMSA = "USOE\DBLS_TASK_${suffix}$"
Write-Host "gMSA: ${gMSA}" # For troubleshooting.

# Set up details about the task.
$packagePath = $OctopusParameters["Octopus.Action.Package.InstallationDirectoryPath"]
$principal = New-ScheduledTaskPrincipal -UserId $gMSA -LogonType Password
$settings = New-ScheduledTaskSettingsSet -Compatibility Win8 -AllowStartIfOnBatteries # Default 3 days execution time limit.
$trigger = New-ScheduledTaskTrigger -Daily -At 2:30:00
$action = New-ScheduledTaskAction `
	-Execute "${packagePath}\UtahPublicEd.Acadience.Import.exe" `
	-WorkingDirectory "${packagePath}"

# Create the new instance/version of the task.
$task = Register-ScheduledTask "Acadience\Import" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description @"
Temporary solution maintained by the UTREx team to feed data to Acadience (ALO) system. 
Project repository: https://bitbucket.org/usbe-it/acadience-file-import
"@