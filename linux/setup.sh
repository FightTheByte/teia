#!/bin/bash

if [ ! "$1" ]; then
  echo "If you need to register for you entitlement key then please follow this link to get a free trial of Watson Text To Speech For Embed and aforementioned key: https://www.ibm.com/account/reg/us-en/signup?formid=urx-51754"
  echo "If you need to find your key or create one, then please follow this link to attain it (sometime you may need to wait for a while before the key becomes active after creating it): https://myibm.ibm.com/products-services/containerlibrary"
  echo "please enter IBM entitlement key as an argument: example 'bash setup.sh Ab459345hbsksdfj4943jwfeksfnadADAadadad '" 
  exit
fi

echo "$1"

echo "${command -v conda}"
# Check if Miniconda is already installed
if [ ! "command -v conda" ]; then

  echo "Miniconda is already installed."
  
else 
  
  echo "Installing Miniconda"

  # Create the Miniconda directory
  mkdir -p ~/miniconda3

  # Download Miniconda installer (no sudo here)
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
  
  # Install Miniconda (no sudo here)
  bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
  
  # Clean up installer
  rm ~/miniconda3/miniconda.sh

  # Update .bashrc to initialize Conda if it's not already there
  if ! grep -Fxq ". \$HOME/miniconda3/etc/profile.d/conda.sh" ~/.bashrc; then
      echo ". $HOME/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
  fi

  # Initialize Conda
  ~/miniconda3/bin/conda init bash
  
  echo "Miniconda installed! :)"

fi

# Update the package list and install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev build-essential libprotobuf-dev protobuf-compiler nvidia-cuda-toolkit curl git

# Add NVIDIA CUDA repository keys
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
echo 'deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /' | sudo tee /etc/apt/sources.list.d/cuda.list

# Install TensorRT dependencies
sudo apt-get install -y libnvinfer8 libnvinfer-dev libnvinfer-plugin-dev libasound2-dev

sudo apt-get update

# Create the Conda environment
~/miniconda3/bin/conda create -n teia python=3.8 -y

# Activate the Conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate teia

# Install packages
pip install setuptools wheel git+https://github.com/huggingface/transformers --verbose

# Install from requirements.txt
pip install -r requirements.txt

if [ ! "command -v docker" ]; then
  echo "docker already installed"
else 

  echo "installing docker"  
  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update

  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  echo "docker installed :)"

fi

docker login cp.icr.io --username cp --password "$1"

cd single-container-tts

docker build . -t tts-standalone

echo "Teia and it's dependencies have been installed, congratulations!"
