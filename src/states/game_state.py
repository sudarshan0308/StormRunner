"""
Main game state with 3D-style gameplay
"""

import pygame
import pygame_gui
import random
import math
from src.states.base_state import BaseState
from src.config import Config
from src.game_manager import GameStateType
from src.entities.player import Player
from src.systems.weather_system import WeatherSystem
from src.systems.camera_system import CameraSystem

class GameState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.ui_manager = None
        self.paused = False
        
        # Game entities
        self.player = None
        self.entities = []
        
        # Game systems
        self.weather_system = None
        self.camera_system = None
        
        # UI elements
        self.pause_menu = None
        self.hud_elements = {}
        
        # Game world
        self.world_objects = []
        self.ground_level = Config.SCREEN_HEIGHT - 100
        
    def enter(self):
        """Initialize game state"""
        self.ui_manager = pygame_gui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        
        # Initialize player
        player_data = self.game_manager.get_player_data()
        self.player = Player(Config.SCREEN_WIDTH // 2, self.ground_level - 50, player_data)
        
        # Initialize systems
        self.weather_system = WeatherSystem()
        self.camera_system = CameraSystem(self.player)
        
        # Create world objects
        self._create_world()
        
        # Create HUD
        self._create_hud()
        
        # Start game music
        self.audio_manager.play_music("game_music")
        
    def exit(self):
        """Clean up game state"""
        pass
        
    def handle_event(self, event):
        """Handle game events"""
        if not self.paused:
            self.ui_manager.process_events(event)
            
            # Player input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                    self._toggle_pause()
                elif event.key == pygame.K_SPACE:
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
            # Pause menu events
            self.ui_manager.process_events(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                    self._toggle_pause()
                    
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if hasattr(self, 'resume_button') and event.ui_element == self.resume_button:
                    self._toggle_pause()
                elif hasattr(self, 'main_menu_button') and event.ui_element == self.main_menu_button:
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
                
            # Update HUD
            self._update_hud()
            
        self.ui_manager.update(dt / 1000.0)
        
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
        
        # Draw UI
        self.ui_manager.draw_ui(screen)
        
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
                    pygame.draw.polygon(screen, tuple(max(0, c - 30) for c in obj['color']), points)
                    
                    # Top face
                    points = [
                        (rect.left, rect.top),
                        (rect.left + depth, rect.top - depth),
                        (rect.right + depth, rect.top - depth),
                        (rect.right, rect.top)
                    ]
                    pygame.draw.polygon(screen, tuple(min(255, c + 20) for c in obj['color']), points)
                    
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
                                     
    def _create_hud(self):
        """Create HUD elements"""
        # Player name
        self.hud_elements['name_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 200, 30),
            text=f"Player: {self.game_manager.get_player_data().get('player_name', 'Player')}",
            manager=self.ui_manager
        )
        
        # Weather status
        self.hud_elements['weather_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 50, 200, 30),
            text="Weather: Clear",
            manager=self.ui_manager
        )
        
        # Instructions
        self.hud_elements['instructions'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, Config.SCREEN_HEIGHT - 100, 400, 80),
            text="WASD/Arrow Keys: Move | Shift: Run | Space: Jump | E: Interact | 1-3: Weather | ESC: Pause",
            manager=self.ui_manager
        )
        
    def _update_hud(self):
        """Update HUD elements"""
        if 'weather_label' in self.hud_elements:
            weather_text = f"Weather: {self.weather_system.current_weather.title()}"
            self.hud_elements['weather_label'].set_text(weather_text)
            
    def _draw_hud(self, screen):
        """Draw additional HUD elements"""
        # FPS counter
        fps = int(pygame.time.Clock().get_fps()) if hasattr(pygame.time.Clock(), 'get_fps') else 60
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {fps}", True, Config.WHITE)
        screen.blit(fps_text, (Config.SCREEN_WIDTH - 80, 10))
        
        # Player position
        pos_text = font.render(f"X: {int(self.player.x)}", True, Config.WHITE)
        screen.blit(pos_text, (Config.SCREEN_WIDTH - 100, 35))
        
    def _toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        
        if self.paused:
            self._create_pause_menu()
            self.audio_manager.pause_music()
        else:
            self._destroy_pause_menu()
            self.audio_manager.resume_music()
            
    def _create_pause_menu(self):
        """Create pause menu"""
        # Resume button
        self.resume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(Config.SCREEN_WIDTH // 2 - 100, 300, 200, 50),
            text='Resume Game',
            manager=self.ui_manager
        )
        
        # Main menu button
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(Config.SCREEN_WIDTH // 2 - 100, 370, 200, 50),
            text='Main Menu',
            manager=self.ui_manager
        )
        
    def _destroy_pause_menu(self):
        """Destroy pause menu"""
        if hasattr(self, 'resume_button'):
            self.resume_button.kill()
        if hasattr(self, 'main_menu_button'):
            self.main_menu_button.kill()
            
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