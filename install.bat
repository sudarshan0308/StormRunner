@echo off
echo ========================================
echo StormRunner Game - Windows Installer
echo ========================================
echo.

echo Installing Python dependencies...
pip install pygame==2.5.2 opencv-python==4.8.1.78 numpy==1.24.3 Pillow==10.0.1 pygame-gui==0.6.9

echo.
echo Installation complete!
echo.
echo Starting StormRunner...
python main.py

pause