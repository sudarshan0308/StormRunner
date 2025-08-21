"""
Camera system for following the player
"""

import pygame
import random
from src.config import Config

class CameraSystem:
    def __init__(self, target):
        self.target = target
        self.x = 0
        self.y = 0
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_timer = 0
        
        # Camera settings
        self.follow_speed = 0.1
        self.dead_zone_width = 200
        self.dead_zone_height = 100
        
    def update(self, dt):
        """Update camera position"""
        if self.target:
            # Calculate target position
            target_x = self.target.x - Config.SCREEN_WIDTH // 2
            target_y = self.target.y - Config.SCREEN_HEIGHT // 2
            
            # Dead zone following
            camera_center_x = -self.x + Config.SCREEN_WIDTH // 2
            camera_center_y = -self.y + Config.SCREEN_HEIGHT // 2
            
            # Horizontal following
            if self.target.x < camera_center_x - self.dead_zone_width // 2:
                self.x = -(self.target.x - Config.SCREEN_WIDTH // 2 + self.dead_zone_width // 2)
            elif self.target.x > camera_center_x + self.dead_zone_width // 2:
                self.x = -(self.target.x - Config.SCREEN_WIDTH // 2 - self.dead_zone_width // 2)
                
            # Vertical following (less aggressive)
            if self.target.y < camera_center_y - self.dead_zone_height // 2:
                self.y = -(self.target.y - Config.SCREEN_HEIGHT // 2 + self.dead_zone_height // 2)
            elif self.target.y > camera_center_y + self.dead_zone_height // 2:
                self.y = -(self.target.y - Config.SCREEN_HEIGHT // 2 - self.dead_zone_height // 2)
                
            # Smooth camera movement
            self.x = self.x * (1 - self.follow_speed) + target_x * self.follow_speed
            
            # Limit camera bounds
            self.x = max(-Config.SCREEN_WIDTH, min(0, self.x))
            self.y = max(-200, min(0, self.y))
            
        # Update camera shake
        if self.shake_duration > 0:
            self.shake_timer += dt
            self.shake_duration -= dt
            
            if self.shake_duration <= 0:
                self.shake_intensity = 0
                
    def get_offset(self):
        """Get camera offset with shake"""
        offset_x = self.x
        offset_y = self.y
        
        # Add shake effect
        if self.shake_intensity > 0:
            shake_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            shake_y = random.uniform(-self.shake_intensity, self.shake_intensity)
            offset_x += shake_x
            offset_y += shake_y
            
        return (offset_x, offset_y)
        
    def shake(self, intensity, duration):
        """Start camera shake"""
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = 0