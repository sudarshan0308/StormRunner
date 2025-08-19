"""
Game configuration settings
"""

import pygame
import os

class Config:
    # Screen settings
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    TITLE = "StormRunner - 3D Adventure Game"
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 100, 200)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    
    # Weather colors
    CLEAR_SKY = (135, 206, 235)
    CLOUDY_SKY = (105, 105, 105)
    STORM_SKY = (47, 79, 79)
    RAIN_COLOR = (173, 216, 230)
    LIGHTNING_COLOR = (255, 255, 255)
    
    # Game settings
    PLAYER_SPEED = 5
    PLAYER_RUN_SPEED = 8
    JUMP_STRENGTH = 15
    GRAVITY = 0.8
    
    # Audio settings
    MASTER_VOLUME = 0.7
    MUSIC_VOLUME = 0.5
    SFX_VOLUME = 0.8
    
    # Paths
    ASSETS_DIR = "assets"
    AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
    IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
    FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
    SAVES_DIR = "saves"
    
    # Avatar settings
    AVATAR_SIZE = (64, 64)
    WEBCAM_WIDTH = 640
    WEBCAM_HEIGHT = 480
    
    # Weather settings
    WEATHER_CHANGE_INTERVAL = 30000  # 30 seconds
    RAIN_PARTICLES = 200
    LIGHTNING_DURATION = 100  # milliseconds
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        directories = [cls.ASSETS_DIR, cls.AUDIO_DIR, cls.IMAGES_DIR, 
                      cls.FONTS_DIR, cls.SAVES_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)