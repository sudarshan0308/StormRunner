#!/usr/bin/env python3
"""
StormRunner - 3D Adventure Game
Main entry point for the game
"""

import pygame
import sys
import os
from src.game_manager import GameManager
from src.config import Config

def main():
    """Main function to start the game"""
    try:
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Create game manager and run
        game_manager = GameManager()
        game_manager.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()