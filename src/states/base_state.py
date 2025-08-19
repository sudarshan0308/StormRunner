"""
Base state class for all game states
"""

import pygame
from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen = game_manager.screen
        self.audio_manager = game_manager.audio_manager
        
    @abstractmethod
    def enter(self):
        """Called when entering this state"""
        pass
        
    @abstractmethod
    def exit(self):
        """Called when exiting this state"""
        pass
        
    @abstractmethod
    def handle_event(self, event):
        """Handle pygame events"""
        pass
        
    @abstractmethod
    def update(self, dt):
        """Update state logic"""
        pass
        
    @abstractmethod
    def render(self, screen):
        """Render state to screen"""
        pass