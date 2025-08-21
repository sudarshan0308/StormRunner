"""
Main menu state
"""

import pygame
from src.states.base_state import BaseState
from src.config import Config

class MainMenuState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background_color = Config.CLEAR_SKY
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        
        # Button properties
        self.buttons = []
        self.selected_button = 0
        
        # Animation
        self.title_pulse = 0
        self.particle_system = []
        
    def enter(self):
        """Initialize main menu"""
        # Create buttons
        button_width = 300
        button_height = 60
        button_x = Config.SCREEN_WIDTH // 2 - button_width // 2
        start_y = 350
        
        self.buttons = [
            {'text': 'Start Adventure', 'rect': pygame.Rect(button_x, start_y, button_width, button_height), 'action': 'start'},
            {'text': 'Settings', 'rect': pygame.Rect(button_x, start_y + 80, button_width, button_height), 'action': 'settings'},
            {'text': 'Quit Game', 'rect': pygame.Rect(button_x, start_y + 160, button_width, button_height), 'action': 'quit'}
        ]
        
        # Initialize particles
        self._init_particles()
        
    def exit(self):
        """Clean up main menu"""
        pass
        
    def handle_event(self, event):
        """Handle main menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
                self.audio_manager.play_sfx("button_click")
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
                self.audio_manager.play_sfx("button_click")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._handle_button_action(self.buttons[self.selected_button]['action'])
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button['rect'].collidepoint(mouse_pos):
                        self.selected_button = i
                        self._handle_button_action(button['action'])
                        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                if button['rect'].collidepoint(mouse_pos):
                    self.selected_button = i
                    
    def _handle_button_action(self, action):
        """Handle button actions"""
        from src.game_manager import GameStateType
        
        self.audio_manager.play_sfx("button_click")
        
        if action == 'start':
            # Check if player has avatar
            player_data = self.game_manager.get_player_data()
            if player_data.get('has_avatar', False):
                self.game_manager.change_state(GameStateType.PLAYING)
            else:
                self.game_manager.change_state(GameStateType.AVATAR_CREATION)
        elif action == 'settings':
            # TODO: Implement settings menu
            pass
        elif action == 'quit':
            self.game_manager.quit_game()
        
    def update(self, dt):
        """Update main menu"""
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
        import math
        pulse_scale = 1.0 + 0.1 * abs(math.sin(self.title_pulse))
        title_text = self.title_font.render("StormRunner", True, Config.WHITE)
        title_rect = title_text.get_rect()
        
        # Scale title
        scaled_width = int(title_rect.width * pulse_scale)
        scaled_height = int(title_rect.height * pulse_scale)
        scaled_title = pygame.transform.scale(title_text, (scaled_width, scaled_height))
        scaled_rect = scaled_title.get_rect(center=(Config.SCREEN_WIDTH // 2, 150))
        screen.blit(scaled_title, scaled_rect)
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render("3D Adventure Game", True, Config.LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 220))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for i, button in enumerate(self.buttons):
            color = Config.WHITE if i == self.selected_button else Config.LIGHT_GRAY
            bg_color = Config.BLUE if i == self.selected_button else Config.DARK_GRAY
            
            # Draw button background
            pygame.draw.rect(screen, bg_color, button['rect'])
            pygame.draw.rect(screen, color, button['rect'], 2)
            
            # Draw button text
            text = self.button_font.render(button['text'], True, color)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 24)
        instruction_text = instruction_font.render("Use Arrow Keys and Enter, or click with mouse", True, Config.GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
        
        # Draw version info
        version_font = pygame.font.Font(None, 24)
        version_text = version_font.render("v1.0.0 - Python Edition", True, Config.GRAY)
        version_rect = version_text.get_rect(bottomright=(Config.SCREEN_WIDTH - 10, Config.SCREEN_HEIGHT - 10))
        screen.blit(version_text, version_rect)
        
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
                import random
                particle['x'] = random.randint(0, Config.SCREEN_WIDTH)
                
    def _draw_particles(self, screen):
        """Draw background particles"""
        for particle in self.particle_system:
            pygame.draw.circle(screen, Config.WHITE, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])