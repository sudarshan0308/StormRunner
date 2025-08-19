"""
Main menu state
"""

import pygame
import pygame_gui
from src.states.base_state import BaseState
from src.config import Config
from src.game_manager import GameStateType

class MainMenuState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.ui_manager = pygame_gui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.background_color = Config.CLEAR_SKY
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 36)
        
        # UI elements
        self.play_button = None
        self.settings_button = None
        self.quit_button = None
        
        # Animation
        self.title_pulse = 0
        self.particle_system = []
        
    def enter(self):
        """Initialize main menu UI"""
        self.ui_manager = pygame_gui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = Config.SCREEN_WIDTH // 2 - button_width // 2
        
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x, 350, button_width, button_height),
            text='Start Adventure',
            manager=self.ui_manager
        )
        
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x, 420, button_width, button_height),
            text='Settings',
            manager=self.ui_manager
        )
        
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x, 490, button_width, button_height),
            text='Quit Game',
            manager=self.ui_manager
        )
        
        # Start background music
        self.audio_manager.play_music("menu_music")
        
        # Initialize particles
        self._init_particles()
        
    def exit(self):
        """Clean up main menu"""
        pass
        
    def handle_event(self, event):
        """Handle main menu events"""
        self.ui_manager.process_events(event)
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.audio_manager.play_sfx("button_click")
                # Check if player has avatar
                player_data = self.game_manager.get_player_data()
                if player_data.get('has_avatar', False):
                    self.game_manager.change_state(GameStateType.PLAYING)
                else:
                    self.game_manager.change_state(GameStateType.AVATAR_CREATION)
                    
            elif event.ui_element == self.settings_button:
                self.audio_manager.play_sfx("button_click")
                # TODO: Implement settings menu
                
            elif event.ui_element == self.quit_button:
                self.audio_manager.play_sfx("button_click")
                self.game_manager.quit_game()
                
    def update(self, dt):
        """Update main menu"""
        self.ui_manager.update(dt / 1000.0)
        
        # Update title animation
        self.title_pulse += dt * 0.003
        
        # Update particles
        self._update_particles(dt)
        
    def render(self, screen):
        """Render main menu"""
        # Background gradient
        self._draw_gradient_background(screen)
        
        # Draw particles
        self._draw_particles(screen)
        
        # Draw title with pulse effect
        pulse_scale = 1.0 + 0.1 * abs(pygame.math.Vector2(1, 0).rotate(self.title_pulse * 180).x)
        title_text = self.title_font.render("StormRunner", True, Config.WHITE)
        title_rect = title_text.get_rect()
        
        # Scale title
        scaled_title = pygame.transform.scale(title_text, 
                                            (int(title_rect.width * pulse_scale), 
                                             int(title_rect.height * pulse_scale)))
        scaled_rect = scaled_title.get_rect(center=(Config.SCREEN_WIDTH // 2, 150))
        screen.blit(scaled_title, scaled_rect)
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render("3D Adventure Game", True, Config.LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 220))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw version info
        version_font = pygame.font.Font(None, 24)
        version_text = version_font.render("v1.0.0 - Python Edition", True, Config.GRAY)
        version_rect = version_text.get_rect(bottomright=(Config.SCREEN_WIDTH - 10, Config.SCREEN_HEIGHT - 10))
        screen.blit(version_text, version_rect)
        
        # Draw UI
        self.ui_manager.draw_ui(screen)
        
    def _draw_gradient_background(self, screen):
        """Draw gradient background"""
        for y in range(Config.SCREEN_HEIGHT):
            ratio = y / Config.SCREEN_HEIGHT
            color = [
                int(Config.CLEAR_SKY[i] * (1 - ratio) + Config.DARK_GRAY[i] * ratio)
                for i in range(3)
            ]
            pygame.draw.line(screen, color, (0, y), (Config.SCREEN_WIDTH, y))
            
    def _init_particles(self):
        """Initialize background particles"""
        import random
        self.particle_system = []
        for _ in range(50):
            particle = {
                'x': random.randint(0, Config.SCREEN_WIDTH),
                'y': random.randint(0, Config.SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150)
            }
            self.particle_system.append(particle)
            
    def _update_particles(self, dt):
        """Update background particles"""
        for particle in self.particle_system:
            particle['y'] += particle['speed'] * dt * 0.1
            if particle['y'] > Config.SCREEN_HEIGHT:
                particle['y'] = -10
                particle['x'] = pygame.math.Vector2(particle['x'], 0).rotate(0.1).x % Config.SCREEN_WIDTH
                
    def _draw_particles(self, screen):
        """Draw background particles"""
        for particle in self.particle_system:
            color = (*Config.WHITE, particle['alpha'])
            pygame.draw.circle(screen, Config.WHITE, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])