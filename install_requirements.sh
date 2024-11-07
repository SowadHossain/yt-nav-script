#!/bin/bash

# Update and install Python package installer
echo "Updating package lists and installing pip..."
sudo apt update -y && sudo apt install python3-pip -y

# Install Selenium for Python
echo "Installing Selenium..."
pip3 install selenium

# Install necessary additional libraries if not already installed
echo "Installing additional Python libraries (numpy, opencv-python, pyautogui, pyaudio)..."
pip3 install numpy opencv-python pyautogui pyaudio

echo "All libraries installed."

# Download ChromeDriver if not already available
echo "Checking for ChromeDriver installation..."
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip -o ~/chromedriver_linux64.zip -d ~/
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
rm ~/chromedriver_linux64.zip

echo "ChromeDriver installed."

# Final message
echo "Environment setup is complete. You are ready to run the Selenium script."

