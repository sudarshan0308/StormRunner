#!/usr/bin/env python3
"""
StormRunner - One-Click Game Launcher
This script handles everything automatically
"""

import subprocess
import sys
import os
import platform

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required!")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    requirements = [
        "pygame==2.5.2",
        "opencv-python==4.8.1.78", 
        "numpy==1.24.3",
        "Pillow==10.0.1",
        "pygame-gui==0.6.9"
    ]
    
    print("🔄 Installing game dependencies...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req, "--quiet"])
            print(f"✅ Installed {req.split('==')[0]}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req}")
            return False
    return True

def run_game():
    """Launch the game"""
    try:
        print("🎮 Starting StormRunner...")
        print("=" * 50)
        import main
        main.main()
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ Game error: {e}")
        return False
    return True

def main():
    """Main launcher function"""
    print("🌟 StormRunner Game Launcher")
    print("=" * 50)
    
    # Check Python version
    check_python()
    
    # Try to run game first
    try:
        import pygame, cv2, numpy, PIL, pygame_gui
        print("✅ All dependencies found")
        run_game()
    except ImportError:
        print("📦 Installing missing dependencies...")
        if install_requirements():
            print("✅ Installation complete!")
            run_game()
        else:
            print("❌ Installation failed!")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()