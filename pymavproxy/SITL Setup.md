# Setup Git
sudo apt-get update
sudo apt-get install git
sudo apt-get install gitk git-gui

# Clone ArduPilot
mkdir MavProxy
cd MavProxy
git clone https://github.com/ArduPilot/ardupilot.git

# Install required packages
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y