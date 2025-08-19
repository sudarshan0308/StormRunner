#!/usr/bin/env python3
"""
StormRunner - Quick run script
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False
    return True

def run_game():
    """Run the game"""
    try:
        import main
        main.main()
    except ImportError as e:
        print(f"Missing dependencies: {e}")
        print("Installing requirements...")
        if install_requirements():
            print("Please run the game again.")
        return False
    except Exception as e:
        print(f"Error running game: {e}")
        return False
    return True

if __name__ == "__main__":
    print("StormRunner - 3D Adventure Game")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import pygame
        import cv2
        import numpy
        import PIL
        import pygame_gui
        print("All dependencies found. Starting game...")
        run_game()
    except ImportError:
        print("Installing required dependencies...")
        if install_requirements():
            print("Dependencies installed. Starting game...")
            run_game()
        else:
            print("Failed to install dependencies. Please install manually:")
            print("pip install -r requirements.txt")