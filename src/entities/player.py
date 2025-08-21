"""
Player entity with avatar support
"""

import pygame
import os
from src.config import Config

class Player:
    def __init__(self, x, y, player_data):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.player_data = player_data
        
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.speed = Config.PLAYER_SPEED
        self.run_speed = Config.PLAYER_RUN_SPEED
        self.is_running = False
        self.on_ground = False
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        
        # Avatar
        self.avatar_surface = None
        self.load_avatar()
        
        # Audio
        self.footstep_timer = 0
        
    def load_avatar(self):
        """Load player avatar"""
        if self.player_data.get('has_avatar', False):
            avatar_path = self.player_data.get('avatar_path', '')
            if os.path.exists(avatar_path):
                try:
                    # Load avatar image using pygame
                    self.avatar_surface = pygame.image.load(avatar_path)
                    self.avatar_surface = pygame.transform.scale(self.avatar_surface, (self.width, self.height))
                except Exception as e:
                    print(f"Failed to load avatar: {e}")
                    self.create_default_avatar()
            else:
                self.create_default_avatar()
        else:
            self.create_default_avatar()
            
    def create_default_avatar(self):
        """Create default avatar"""
        self.avatar_surface = pygame.Surface((self.width, self.height))
        self.avatar_surface.fill(Config.BLUE)
        
        # Simple character shape
        pygame.draw.circle(self.avatar_surface, Config.LIGHT_GRAY, 
                         (self.width // 2, 12), 8)  # Head
        pygame.draw.rect(self.avatar_surface, Config.RED, 
                        (self.width // 2 - 8, 20, 16, 20))  # Body
        pygame.draw.rect(self.avatar_surface, Config.DARK_GRAY, 
                        (self.width // 2 - 6, 40, 5, 8))  # Left leg
        pygame.draw.rect(self.avatar_surface, Config.DARK_GRAY, 
                        (self.width // 2 + 1, 40, 5, 8))  # Right leg
        
    def move_left(self, dt):
        """Move player left"""
        current_speed = self.run_speed if self.is_running else self.speed
        self.vel_x = -current_speed
        self.facing_right = False
        self._play_footstep(dt)
        
    def move_right(self, dt):
        """Move player right"""
        current_speed = self.run_speed if self.is_running else self.speed
        self.vel_x = current_speed
        self.facing_right = True
        self._play_footstep(dt)
        
    def jump(self):
        """Make player jump"""
        if self.on_ground:
            self.vel_y = -Config.JUMP_STRENGTH
            self.on_ground = False
            
    def set_running(self, running):
        """Set running state"""
        self.is_running = running
        
    def update(self, dt, ground_level):
        """Update player"""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += Config.GRAVITY
            
        # Update position
        self.x += self.vel_x * dt * 0.1
        self.y += self.vel_y * dt * 0.1
        
        # Ground collision
        if self.y >= ground_level - self.height:
            self.y = ground_level - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Screen boundaries
        self.x = max(0, min(self.x, Config.SCREEN_WIDTH * 2 - self.width))
        
        # Friction
        self.vel_x *= 0.8
        
        # Animation
        if abs(self.vel_x) > 0.1:
            self.animation_timer += dt
            if self.animation_timer > 200:  # Animation speed
                self.animation_frame = (self.animation_frame + 1) % 4
                self.animation_timer = 0
        else:
            self.animation_frame = 0
            
    def render(self, screen, camera_offset):
        """Render player"""
        render_x = self.x + camera_offset[0]
        render_y = self.y + camera_offset[1]
        
        # Only render if on screen
        if -50 <= render_x <= Config.SCREEN_WIDTH + 50:
            if self.avatar_surface:
                # Flip sprite if facing left
                if not self.facing_right:
                    flipped_surface = pygame.transform.flip(self.avatar_surface, True, False)
                    screen.blit(flipped_surface, (render_x, render_y))
                else:
                    screen.blit(self.avatar_surface, (render_x, render_y))
            else:
                # Fallback rectangle
                pygame.draw.rect(screen, Config.BLUE, 
                               (render_x, render_y, self.width, self.height))
                               
            # Player name above head
            if self.player_data.get('player_name'):
                font = pygame.font.Font(None, 20)
                name_text = font.render(self.player_data['player_name'], True, Config.WHITE)
                name_rect = name_text.get_rect(center=(render_x + self.width // 2, render_y - 10))
                screen.blit(name_text, name_rect)
                
    def _play_footstep(self, dt):
        """Play footstep sound"""
        if self.on_ground:
            self.footstep_timer += dt
            footstep_interval = 300 if not self.is_running else 200
            
            if self.footstep_timer > footstep_interval:
                self.footstep_timer = 0
                
    def get_rect(self):
        """Get player collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)