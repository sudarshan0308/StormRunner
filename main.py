#!/usr/bin/env python3
"""
StormRunner - 3D Adventure Game
Main entry point for the game
"""

import pygame
import sys
import os

def main():
    """Main function to start the game"""
    try:
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Import and create game manager
        from src.game_manager import GameManager
        game_manager = GameManager()
        game_manager.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()