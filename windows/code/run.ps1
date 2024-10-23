Write-Host "starting docker"

Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"


   # Function to check if Docker is ready by pinging the Docker API 
   function DockerReady {
       try {
           $response = Invoke-RestMethod -Uri http://localhost:2375/_ping -UseBasicParsing
           return $response -eq "OK"
       } catch {
           return $false
       }
    }
    
    # Wait for Docker to be ready
    do {
        Write-Host "Waiting for Docker to be ready..."
        Start-Sleep -Seconds 3
    } until (DockerReady)
    
# Spin up Watson Container
Start-Process powershell -ArgumentList "-NoExit", "-Command", "docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone"


Write-Host "starting Teia"
conda run --name teia python ./run.py

Write-Host -NoNewLine "Application stopped, press any key to finish..."
$null = $Host.UI.RawUI.ReadKey('NoEcho, IncludeKeyDown')