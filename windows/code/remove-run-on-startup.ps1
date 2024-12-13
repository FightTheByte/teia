$user = [Environment]::UserName
$path = "C:\Users\${user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

Remove-Item -Path "$path\run-on-startup.exe"

Write-Host -NoNewLine "Removed startup service: Press any key to finish..."
$null = $Host.UI.RawUI.ReadKey('NoEcho, IncludeKeyDown')