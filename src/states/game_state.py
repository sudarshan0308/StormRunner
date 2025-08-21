"""
Main game state with 3D-style gameplay
"""

import pygame
import random
import math
from src.states.base_state import BaseState
from src.config import Config

class GameState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.paused = False
        
        # Game entities
        self.player = None
        self.entities = []
        
        # Game systems
        self.weather_system = None
        self.camera_system = None
        
        # Game world
        self.world_objects = []
        self.ground_level = Config.SCREEN_HEIGHT - 100
        
        # UI elements
        self.pause_buttons = []
        self.selected_pause_button = 0
        
    def enter(self):
        """Initialize game state"""
        # Initialize player
        from src.entities.player import Player
        player_data = self.game_manager.get_player_data()
        self.player = Player(Config.SCREEN_WIDTH // 2, self.ground_level - 50, player_data)
        
        # Initialize systems
        from src.systems.weather_system import WeatherSystem
        from src.systems.camera_system import CameraSystem
        
        self.weather_system = WeatherSystem()
        self.camera_system = CameraSystem(self.player)
        
        # Create world objects
        self._create_world()
        
        # Create pause menu
        self._create_pause_menu()
        
    def exit(self):
        """Clean up game state"""
        pass
        
    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                self._toggle_pause()
            elif not self.paused:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_e:
                    self._interact()
                # Weather testing keys
                elif event.key == pygame.K_1:
                    self.weather_system.set_weather("clear")
                elif event.key == pygame.K_2:
                    self.weather_system.set_weather("rain")
                elif event.key == pygame.K_3:
                    self.weather_system.set_weather("storm")
            else:
                # Pause menu navigation
                if event.key == pygame.K_UP:
                    self.selected_pause_button = (self.selected_pause_button - 1) % len(self.pause_buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_pause_button = (self.selected_pause_button + 1) % len(self.pause_buttons)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._handle_pause_button_action(self.pause_buttons[self.selected_pause_button]['action'])
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.pause_buttons):
                    if button['rect'].collidepoint(mouse_pos):
                        self.selected_pause_button = i
                        self._handle_pause_button_action(button['action'])
                        
        elif event.type == pygame.MOUSEMOTION and self.paused:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.pause_buttons):
                if button['rect'].collidepoint(mouse_pos):
                    self.selected_pause_button = i
                    
    def _handle_pause_button_action(self, action):
        """Handle pause menu button actions"""
        from src.game_manager import GameStateType
        
        self.audio_manager.play_sfx("button_click")
        
        if action == 'resume':
            self._toggle_pause()
        elif action == 'main_menu':
            self.game_manager.change_state(GameStateType.MAIN_MENU)
            
    def update(self, dt):
        """Update game state"""
        if not self.paused:
            # Handle continuous input
            keys = pygame.key.get_pressed()
            
            # Player movement
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.move_left(dt)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move_right(dt)
            if keys[pygame.K_LSHIFT]:
                self.player.set_running(True)
            else:
                self.player.set_running(False)
                
            # Update player
            self.player.update(dt, self.ground_level)
            
            # Update systems
            self.weather_system.update(dt)
            self.camera_system.update(dt)
            
            # Update entities
            for entity in self.entities:
                entity.update(dt)
                
    def render(self, screen):
        """Render game state"""
        # Sky background
        sky_color = self.weather_system.get_sky_color()
        screen.fill(sky_color)
        
        # Apply camera offset
        camera_offset = self.camera_system.get_offset()
        
        # Draw world (3D-style perspective)
        self._draw_world(screen, camera_offset)
        
        # Draw entities
        for entity in self.entities:
            entity.render(screen, camera_offset)
            
        # Draw player
        self.player.render(screen, camera_offset)
        
        # Draw weather effects
        self.weather_system.render(screen)
        
        # Draw HUD
        self._draw_hud(screen)
        
        # Draw pause overlay
        if self.paused:
            self._draw_pause_overlay(screen)
            
    def _create_world(self):
        """Create game world objects"""
        # Ground
        self.world_objects.append({
            'type': 'ground',
            'rect': pygame.Rect(0, self.ground_level, Config.SCREEN_WIDTH * 3, 100),
            'color': Config.GREEN
        })
        
        # Buildings (3D-style)
        building_positions = [200, 500, 800, 1200, 1600]
        for i, x in enumerate(building_positions):
            height = random.randint(150, 300)
            self.world_objects.append({
                'type': 'building',
                'rect': pygame.Rect(x, self.ground_level - height, 80, height),
                'color': Config.GRAY,
                'height': height,
                'depth': 40
            })
            
        # Trees
        tree_positions = [150, 350, 650, 950, 1350]
        for x in tree_positions:
            self.world_objects.append({
                'type': 'tree',
                'rect': pygame.Rect(x, self.ground_level - 60, 20, 60),
                'color': Config.GREEN,
                'trunk_color': (139, 69, 19)
            })
            
    def _draw_world(self, screen, camera_offset):
        """Draw world objects with 3D perspective"""
        for obj in self.world_objects:
            if obj['type'] == 'ground':
                # Draw ground
                rect = obj['rect'].copy()
                rect.x += camera_offset[0]
                pygame.draw.rect(screen, obj['color'], rect)
                
                # Ground texture lines
                for i in range(0, rect.width, 50):
                    line_x = rect.x + i
                    if 0 <= line_x <= Config.SCREEN_WIDTH:
                        pygame.draw.line(screen, Config.DARK_GRAY, 
                                       (line_x, rect.y), (line_x, rect.bottom), 2)
                        
            elif obj['type'] == 'building':
                # Draw building with 3D effect
                rect = obj['rect'].copy()
                rect.x += camera_offset[0]
                
                if -100 <= rect.x <= Config.SCREEN_WIDTH + 100:
                    # Main building face
                    pygame.draw.rect(screen, obj['color'], rect)
                    
                    # 3D depth effect
                    depth = obj['depth']
                    # Right face
                    points = [
                        (rect.right, rect.top),
                        (rect.right + depth, rect.top - depth),
                        (rect.right + depth, rect.bottom - depth),
                        (rect.right, rect.bottom)
                    ]
                    darker_color = tuple(max(0, c - 30) for c in obj['color'])
                    pygame.draw.polygon(screen, darker_color, points)
                    
                    # Top face
                    points = [
                        (rect.left, rect.top),
                        (rect.left + depth, rect.top - depth),
                        (rect.right + depth, rect.top - depth),
                        (rect.right, rect.top)
                    ]
                    lighter_color = tuple(min(255, c + 20) for c in obj['color'])
                    pygame.draw.polygon(screen, lighter_color, points)
                    
                    # Windows
                    for row in range(2, obj['height'] // 30):
                        for col in range(1, 3):
                            window_x = rect.x + col * 25
                            window_y = rect.y + row * 30
                            window_rect = pygame.Rect(window_x, window_y, 15, 20)
                            window_color = Config.YELLOW if random.random() > 0.3 else Config.DARK_GRAY
                            pygame.draw.rect(screen, window_color, window_rect)
                            
            elif obj['type'] == 'tree':
                # Draw tree
                rect = obj['rect'].copy()
                rect.x += camera_offset[0]
                
                if -50 <= rect.x <= Config.SCREEN_WIDTH + 50:
                    # Trunk
                    trunk_rect = pygame.Rect(rect.x + 5, rect.y + 40, 10, 20)
                    pygame.draw.rect(screen, obj['trunk_color'], trunk_rect)
                    
                    # Leaves (circular)
                    pygame.draw.circle(screen, obj['color'], 
                                     (rect.centerx, rect.y + 20), 25)
                                     
    def _create_pause_menu(self):
        """Create pause menu buttons"""
        button_width = 200
        button_height = 50
        button_x = Config.SCREEN_WIDTH // 2 - button_width // 2
        
        self.pause_buttons = [
            {'text': 'Resume Game', 'rect': pygame.Rect(button_x, 300, button_width, button_height), 'action': 'resume'},
            {'text': 'Main Menu', 'rect': pygame.Rect(button_x, 370, button_width, button_height), 'action': 'main_menu'}
        ]
        
    def _draw_hud(self, screen):
        """Draw HUD elements"""
        font = pygame.font.Font(None, 24)
        
        # Player name
        player_name = self.game_manager.get_player_data().get('player_name', 'Player')
        name_text = font.render(f"Player: {player_name}", True, Config.WHITE)
        screen.blit(name_text, (10, 10))
        
        # Weather status
        weather_text = font.render(f"Weather: {self.weather_system.current_weather.title()}", True, Config.WHITE)
        screen.blit(weather_text, (10, 35))
        
        # Instructions
        instruction_font = pygame.font.Font(None, 20)
        instructions = [
            "WASD/Arrow Keys: Move | Shift: Run | Space: Jump",
            "E: Interact | 1-3: Weather | ESC: Pause"
        ]
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, Config.WHITE)
            screen.blit(text, (10, Config.SCREEN_HEIGHT - 40 + i * 20))
        
        # FPS counter
        fps = int(self.game_manager.clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, Config.WHITE)
        screen.blit(fps_text, (Config.SCREEN_WIDTH - 80, 10))
        
        # Player position
        pos_text = font.render(f"X: {int(self.player.x)}", True, Config.WHITE)
        screen.blit(pos_text, (Config.SCREEN_WIDTH - 100, 35))
        
    def _toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        
    def _draw_pause_overlay(self, screen):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Config.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause title
        font = pygame.font.Font(None, 72)
        pause_text = font.render("PAUSED", True, Config.WHITE)
        pause_rect = pause_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 200))
        screen.blit(pause_text, pause_rect)
        
        # Draw pause menu buttons
        button_font = pygame.font.Font(None, 48)
        for i, button in enumerate(self.pause_buttons):
            color = Config.WHITE if i == self.selected_pause_button else Config.LIGHT_GRAY
            bg_color = Config.BLUE if i == self.selected_pause_button else Config.DARK_GRAY
            
            pygame.draw.rect(screen, bg_color, button['rect'])
            pygame.draw.rect(screen, color, button['rect'], 2)
            
            text = button_font.render(button['text'], True, color)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
        
    def _interact(self):
        """Handle interaction"""
        # Check for nearby interactive objects
        player_rect = pygame.Rect(self.player.x - 25, self.player.y - 25, 50, 50)
        
        for obj in self.world_objects:
            if obj['type'] in ['building', 'tree']:
                if player_rect.colliderect(obj['rect']):
                    self.audio_manager.play_sfx("interaction")
                    print(f"Interacted with {obj['type']}")
                    break