"""
Dynamic weather system with visual effects
"""

import pygame
import random
import math
from src.config import Config

class WeatherSystem:
    def __init__(self):
        self.current_weather = "clear"
        self.weather_timer = 0
        self.weather_change_interval = Config.WEATHER_CHANGE_INTERVAL
        
        # Rain system
        self.rain_particles = []
        self.rain_intensity = 0
        
        # Lightning system
        self.lightning_timer = 0
        self.lightning_active = False
        self.lightning_duration = 0
        
        # Wind system
        self.wind_strength = 0
        self.wind_direction = 1
        
        # Initialize particles
        self._init_rain_particles()
        
    def _init_rain_particles(self):
        """Initialize rain particles"""
        for _ in range(Config.RAIN_PARTICLES):
            particle = {
                'x': random.randint(0, Config.SCREEN_WIDTH),
                'y': random.randint(-Config.SCREEN_HEIGHT, 0),
                'speed': random.uniform(5, 15),
                'length': random.randint(10, 20),
                'alpha': random.randint(100, 255)
            }
            self.rain_particles.append(particle)
            
    def set_weather(self, weather_type):
        """Set weather type"""
        if weather_type in ["clear", "rain", "storm"]:
            self.current_weather = weather_type
            
    def update(self, dt):
        """Update weather system"""
        # Auto weather change
        self.weather_timer += dt
        if self.weather_timer > self.weather_change_interval:
            self._change_weather_randomly()
            self.weather_timer = 0
            
        # Update based on current weather
        if self.current_weather == "clear":
            self.rain_intensity = max(0, self.rain_intensity - dt * 0.001)
            self.wind_strength = max(0, self.wind_strength - dt * 0.0005)
            
        elif self.current_weather == "rain":
            self.rain_intensity = min(0.7, self.rain_intensity + dt * 0.001)
            self.wind_strength = min(0.3, self.wind_strength + dt * 0.0005)
            
        elif self.current_weather == "storm":
            self.rain_intensity = min(1.0, self.rain_intensity + dt * 0.002)
            self.wind_strength = min(1.0, self.wind_strength + dt * 0.001)
            
            # Lightning
            self.lightning_timer += dt
            if self.lightning_timer > random.randint(2000, 8000):
                self._trigger_lightning()
                self.lightning_timer = 0
                
        # Update rain particles
        self._update_rain(dt)
        
        # Update lightning
        if self.lightning_active:
            self.lightning_duration -= dt
            if self.lightning_duration <= 0:
                self.lightning_active = False
                
    def render(self, screen):
        """Render weather effects"""
        # Rain
        if self.rain_intensity > 0:
            self._render_rain(screen)
            
        # Lightning
        if self.lightning_active:
            self._render_lightning(screen)
            
    def get_sky_color(self):
        """Get current sky color based on weather"""
        if self.current_weather == "clear":
            return Config.CLEAR_SKY
        elif self.current_weather == "rain":
            # Interpolate between clear and cloudy
            ratio = self.rain_intensity
            return tuple(
                int(Config.CLEAR_SKY[i] * (1 - ratio) + Config.CLOUDY_SKY[i] * ratio)
                for i in range(3)
            )
        elif self.current_weather == "storm":
            # Interpolate between cloudy and storm
            ratio = min(1.0, self.rain_intensity)
            return tuple(
                int(Config.CLOUDY_SKY[i] * (1 - ratio) + Config.STORM_SKY[i] * ratio)
                for i in range(3)
            )
        return Config.CLEAR_SKY
        
    def _change_weather_randomly(self):
        """Randomly change weather"""
        weather_types = ["clear", "rain", "storm"]
        weights = [0.5, 0.3, 0.2]  # Clear weather more likely
        self.current_weather = random.choices(weather_types, weights=weights)[0]
        
    def _update_rain(self, dt):
        """Update rain particles"""
        if self.rain_intensity > 0:
            for particle in self.rain_particles:
                # Move particle
                particle['y'] += particle['speed'] * dt * 0.1 * self.rain_intensity
                particle['x'] += self.wind_strength * self.wind_direction * dt * 0.05
                
                # Reset particle if off screen
                if particle['y'] > Config.SCREEN_HEIGHT:
                    particle['y'] = random.randint(-50, -10)
                    particle['x'] = random.randint(0, Config.SCREEN_WIDTH)
                    
                if particle['x'] < -10 or particle['x'] > Config.SCREEN_WIDTH + 10:
                    particle['x'] = random.randint(0, Config.SCREEN_WIDTH)
                    
    def _render_rain(self, screen):
        """Render rain particles"""
        for particle in self.rain_particles:
            if 0 <= particle['x'] <= Config.SCREEN_WIDTH and 0 <= particle['y'] <= Config.SCREEN_HEIGHT:
                alpha = int(particle['alpha'] * self.rain_intensity)
                if alpha > 0:
                    # Create rain drop line
                    start_pos = (int(particle['x']), int(particle['y']))
                    end_pos = (int(particle['x'] - self.wind_strength * 5), 
                             int(particle['y'] + particle['length']))
                    
                    # Draw rain line with alpha
                    rain_surface = pygame.Surface((abs(end_pos[0] - start_pos[0]) + 2, 
                                                 abs(end_pos[1] - start_pos[1]) + 2))
                    rain_surface.set_alpha(alpha)
                    rain_surface.fill(Config.RAIN_COLOR)
                    
                    pygame.draw.line(rain_surface, Config.RAIN_COLOR, 
                                   (1, 1), (abs(end_pos[0] - start_pos[0]), 
                                           abs(end_pos[1] - start_pos[1])), 2)
                    
                    screen.blit(rain_surface, (min(start_pos[0], end_pos[0]), 
                                             min(start_pos[1], end_pos[1])))
                    
    def _trigger_lightning(self):
        """Trigger lightning effect"""
        self.lightning_active = True
        self.lightning_duration = Config.LIGHTNING_DURATION
        
    def _render_lightning(self, screen):
        """Render lightning effect"""
        # Flash effect
        lightning_surface = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        lightning_surface.set_alpha(100)
        lightning_surface.fill(Config.LIGHTNING_COLOR)
        screen.blit(lightning_surface, (0, 0))
        
        # Lightning bolt
        if random.random() > 0.7:  # Random lightning bolt appearance
            start_x = random.randint(100, Config.SCREEN_WIDTH - 100)
            points = [(start_x, 0)]
            
            current_x = start_x
            for y in range(0, Config.SCREEN_HEIGHT // 2, 20):
                current_x += random.randint(-30, 30)
                current_x = max(50, min(Config.SCREEN_WIDTH - 50, current_x))
                points.append((current_x, y))
                
            if len(points) > 2:
                pygame.draw.lines(screen, Config.LIGHTNING_COLOR, False, points, 3)