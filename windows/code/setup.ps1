# setup.ps1

$user = [Environment]::UserName

$venv_path = "C:\Users\${user}\miniconda3\envs\teia"

# Get IBM entitlement key

Write-Host "If you haven't registered for Watson embed Text to Speech, please visit the following site to register for a free trial: https://www.ibm.com/account/reg/us-en/signup?formid=urx-51754"

Write-Host "If you have registered for a free Watson Text to Speech Trial, please visit the following site to get your entitlement key: https://myibm.ibm.com/products-services/containerlibrary"

$ENTITLEMENT = Read-Host -Prompt "Please enter IBM entitlement key: "

# Check if Miniconda is installed

if (Get-Command conda -ErrorAction SilentlyContinue){
    Write-Host "Miniconda is already installed."
} else {
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
    Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
    del miniconda.exe
}

# Check if 'teia' virtual environment exists, if not set up teia venv

if (!(Test-Path $venv_path)) { 
    Write-Host "Creating virtual environment 'teia'..."
    conda create --name teia python=3.8 -y

    # Install dependencies
    Write-Host "Installing required dependencies..."
    conda run --name teia pip install --upgrade pip setuptools wheel pip git+https://github.com/huggingface/transformers 
    conda install --name teia cuda -c nvidia/label/cuda-12.1.0
    conda run --name teia pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    conda run --name teia pip install -r requirements_win.txt --extra-index-url https://pypi.ngc.nvidia.com
} else {
    Write-Host "Virtual environment 'teia' already exists."
}

# Check if docker exists, install if not install docker

if (Get-Command docker -ErrorAction SilentlyContinue){
    Write-Host "Docker already installed"
    
    Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"

   # Function to check if Docker is ready by pinging the Docker API 
   function Test-DockerReady {
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
    } until (Test-DockerReady)

    $checkImage = docker images -q tts-standalone
} else {
    wsl --install
    curl "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64" -o docker.exe
    Start-Process '.\docker.exe' -Wait -ArgumentList 'install', '--accept-license'
    del docker.exe
    Write-Host "Docker successfully installed"
}

# Check if watson tts container exists, install if not

if (![String]::IsNullOrEmpty($checkImage)){
    Write-Host "Watson Text to Speech already exists"
} else {
    echo "$ENTITLEMENT" | docker login cp.icr.io --username cp --password-stdin 
    cd ../single-container-tts
    Write-Host "Download Text to speech image (8GB), this may take some time, please wait"
    docker build . --quiet -t tts-standalone
    cd ..
}

echo "Teia has successfully been installed"

Write-Host -NoNewLine "Setup complete. Press any key to finish..."
$null = $Host.UI.RawUI.ReadKey('NoEcho, IncludeKeyDown')
