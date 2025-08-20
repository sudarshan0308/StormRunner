#!/bin/bash
echo "========================================"
echo "StormRunner Game - Unix Installer"
echo "========================================"
echo

echo "Installing Python dependencies..."
pip3 install pygame==2.5.2 opencv-python==4.8.1.78 numpy==1.24.3 Pillow==10.0.1 pygame-gui==0.6.9

echo
echo "Installation complete!"
echo
echo "Starting StormRunner..."
python3 main.py