# Delete files from the prior deployment.
$destination = $OctopusParameters["Octopus.Action.Package.InstallationDirectoryPath"]
Get-ChildItem -Path "${destination}" -File | Remove-Item # Ignore folders; only files.
# The package (currently) doesn't include folders, but it makes and uses them.