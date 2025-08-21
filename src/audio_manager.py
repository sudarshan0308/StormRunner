"""
Audio manager for music and sound effects
"""

import pygame
import numpy as np
from src.config import Config

class AudioManager:
    def __init__(self):
        self.music_volume = Config.MUSIC_VOLUME
        self.sfx_volume = Config.SFX_VOLUME
        self.master_volume = Config.MASTER_VOLUME
        
        # Sound effects dictionary
        self.sfx = {}
        
        # Load audio files
        self._load_audio()
        
    def _load_audio(self):
        """Load audio files"""
        # Create placeholder sounds if audio files don't exist
        self._create_placeholder_sounds()
        
    def _create_placeholder_sounds(self):
        """Create placeholder sound effects"""
        # Create simple beep sounds for different actions
        try:
            # Button click sound
            self.sfx['button_click'] = self._create_beep(440, 0.1)
            
            # Camera shutter sound
            self.sfx['camera_shutter'] = self._create_beep(800, 0.2)
            
            # Interaction sound
            self.sfx['interaction'] = self._create_beep(600, 0.15)
            
            # Footstep sound
            self.sfx['footstep'] = self._create_beep(200, 0.05)
            
        except Exception as e:
            print(f"Failed to create placeholder sounds: {e}")
            
    def _create_beep(self, frequency, duration):
        """Create a simple beep sound"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                wave = 4096 * np.sin(frequency * 2 * np.pi * time)
                arr.append([int(wave), int(wave)])
                
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            return sound
        except Exception as e:
            print(f"Failed to create beep sound: {e}")
            return None
        
    def play_music(self, music_name):
        """Play background music"""
        try:
            # For now, just print that music would play
            print(f"Playing music: {music_name}")
        except Exception as e:
            print(f"Failed to play music: {e}")
            
    def play_sfx(self, sfx_name, volume=1.0):
        """Play sound effect"""
        try:
            if sfx_name in self.sfx and self.sfx[sfx_name]:
                sound = self.sfx[sfx_name]
                sound.set_volume(self.sfx_volume * self.master_volume * volume)
                sound.play()
        except Exception as e:
            print(f"Failed to play sound effect {sfx_name}: {e}")
            
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        
    def pause_music(self):
        """Pause background music"""
        pygame.mixer.music.pause()
        
    def resume_music(self):
        """Resume background music"""
        pygame.mixer.music.unpause()
        
    def set_master_volume(self, volume):
        """Set master volume"""
        self.master_volume = max(0.0, min(1.0, volume))
        
    def set_music_volume(self, volume):
        """Set music volume"""
        self.music_volume = max(0.0, min(1.0, volume))
        
    def set_sfx_volume(self, volume):
        """Set sound effects volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))