"""
Save and load game data
"""

import json
import os
from src.config import Config

class SaveManager:
    def __init__(self):
        self.save_file = os.path.join(Config.SAVES_DIR, "player_data.json")
        
    def save_player_data(self, player_data):
        """Save player data to file"""
        try:
            os.makedirs(Config.SAVES_DIR, exist_ok=True)
            with open(self.save_file, 'w') as f:
                json.dump(player_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save player data: {e}")
            
    def load_player_data(self):
        """Load player data from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load player data: {e}")
            
        # Return default player data
        return {
            'player_name': 'Player',
            'has_avatar': False,
            'avatar_path': '',
            'skin_tone': 0.5,
            'hair_style': 0.5,
            'eye_color': 0.5,
            'game_progress': 0,
            'high_score': 0
        }