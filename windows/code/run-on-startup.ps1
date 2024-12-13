Write-Host "starting docker"

$user = [Environment]::UserName

Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"

$file_path = "C:\Users\${user}\Desktop\teia\windows"


   # Check if Docker is ready
   function DockerReady {
       try {
           $response = Invoke-RestMethod -Uri http://localhost:2375/_ping -UseBasicParsing
           return $response -eq "OK"
       } catch {
           return $false
       }
    }
     
    # Wait for Docker
    do {
        Write-Host "Waiting for Docker to be ready..."
        Start-Sleep -Seconds 3
    } until (DockerReady)

Start-Process powershell -ArgumentList "-NoExit", "-Command", "docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone"


Start-Sleep -Second 80


Write-Host "Starting Teia"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "conda run --name teia python '$file_path\run-on-startup.py' '$file_path'"


Write-Host -NoNewLine "Application initialised, press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho, IncludeKeyDown')