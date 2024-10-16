#!/bin/bash

# Get the current user and home directory
username=$(logname)
home_dir=$(eval echo ~$username)

# Define the paths
install_path="$home_dir/teia"
conda_path="$home_dir/miniconda3"


# Replace placeholders in the service template
service_file="/etc/systemd/system/teia.service"
sed -e "s|{{username}}|$username|g" \
    -e "s|{{install_path}}|$install_path|g" \
    -e "s|{{conda_path}}|$conda_path|g" \
    teia.service.template | sudo tee $service_file

# Reload systemd to apply the new service
sudo systemctl daemon-reload

# Start the service
sudo systemctl start teia.service

# Enable the service to run on startup
sudo systemctl enable teia.service

echo "Teia service has been installed and enabled to run on startup."


