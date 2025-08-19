"""
Main game manager that handles all game states and systems
"""

import pygame
import sys
from enum import Enum
from src.config import Config
from src.states.main_menu import MainMenuState
from src.states.avatar_creation import AvatarCreationState
from src.states.game_state import GameState
from src.audio_manager import AudioManager
from src.save_manager import SaveManager

class GameStateType(Enum):
    MAIN_MENU = "main_menu"
    AVATAR_CREATION = "avatar_creation"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class GameManager:
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption(Config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create necessary directories
        Config.create_directories()
        
        # Initialize managers
        self.audio_manager = AudioManager()
        self.save_manager = SaveManager()
        
        # Game states
        self.states = {}
        self.current_state = None
        self.current_state_type = GameStateType.MAIN_MENU
        
        # Initialize states
        self._initialize_states()
        
        # Player data
        self.player_data = self.save_manager.load_player_data()
        
    def _initialize_states(self):
        """Initialize all game states"""
        self.states[GameStateType.MAIN_MENU] = MainMenuState(self)
        self.states[GameStateType.AVATAR_CREATION] = AvatarCreationState(self)
        self.states[GameStateType.PLAYING] = GameState(self)
        
        # Set initial state
        self.current_state = self.states[GameStateType.MAIN_MENU]
        
    def change_state(self, new_state_type):
        """Change to a new game state"""
        if new_state_type in self.states:
            if self.current_state:
                self.current_state.exit()
            
            self.current_state_type = new_state_type
            self.current_state = self.states[new_state_type]
            self.current_state.enter()
            
    def run(self):
        """Main game loop"""
        self.current_state.enter()
        
        while self.running:
            dt = self.clock.tick(Config.FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                else:
                    self.current_state.handle_event(event)
            
            # Update current state
            self.current_state.update(dt)
            
            # Render current state
            self.screen.fill(Config.BLACK)
            self.current_state.render(self.screen)
            
            # Update display
            pygame.display.flip()
            
    def quit_game(self):
        """Quit the game"""
        self.save_manager.save_player_data(self.player_data)
        self.running = False
        
    def get_player_data(self):
        """Get current player data"""
        return self.player_data
        
    def set_player_data(self, data):
        """Set player data"""
        self.player_data = data
        self.save_manager.save_player_data(data)