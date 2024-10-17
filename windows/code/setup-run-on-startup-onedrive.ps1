$user = [Environment]::UserName
$path = "C:\Users\${user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

Copy-Item -Path ".\run-on-startup-onedrive.exe" -Destination "$path"

Write-Host -NoNewLine "Created startup service: Press any key to finish..."
$null = $Host.UI.RawUI.ReadKey('NoEcho, IncludeKeyDown')