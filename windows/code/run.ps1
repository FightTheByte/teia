Write-Host "starting docker"

Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"

$END_TIME = (Get-Date).AddSeconds(20)

   # Function to check if Docker backend is ready by checking Docker server version 
   function DockerReady{
       try{
           $RES = docker info --format '{{json .ServerVersion}}'
           if ($RES -eq '""' -or $RES -eq $null){
               echo "docker API not initialised"
               return $false
           } else{
               return $true
           }
        } catch {
            return $false
        }
   }
    
    # Wait for Docker to be ready
   do{
        if((Get-Date).CompareTo($END_TIME) -eq 1){
            $Prompt = Read-Host 'Unable to start Docker, please manually start Docker and try again. Press and Key to exit'
            Switch($Prompt){
                $Prompt {Exit}
            }
        }
        Write-Host "Waiting for Docker to be ready..."
        Start-Sleep -Seconds 3
   } until (DockerReady)
    
# Spin up Watson Container
Start-Process powershell -ArgumentList "-NoExit", "-Command", "docker run --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone"


Write-Host "starting Teia"
conda run --name teia python ../common/run.py

Write-Host -NoNewLine "Application stopped, press any key to finish..."
$null = $Host.UI.RawUI.ReadKey('NoEcho, IncludeKeyDown')
