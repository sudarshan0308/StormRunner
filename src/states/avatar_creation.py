"""
Avatar creation state with webcam integration
"""

import pygame
import os
from src.states.base_state import BaseState
from src.config import Config

class AvatarCreationState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.camera = None
        self.camera_surface = None
        self.captured_image = None
        self.is_photo_taken = False
        
        # UI elements
        self.buttons = []
        self.selected_button = 0
        self.sliders = {}
        self.player_name = "Player"
        self.name_input_active = False
        
        # Avatar preview
        self.avatar_surface = None
        
    def enter(self):
        """Initialize avatar creation"""
        self.is_photo_taken = False
        
        # Initialize camera
        self._init_camera()
        
        # Create UI elements
        self._create_ui()
        
    def exit(self):
        """Clean up avatar creation"""
        if self.camera:
            try:
                self.camera.release()
            except:
                pass
            
    def _init_camera(self):
        """Initialize webcam"""
        try:
            import cv2
            self.camera = cv2.VideoCapture(0)
            if self.camera.isOpened():
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.WEBCAM_WIDTH)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.WEBCAM_HEIGHT)
                print("Camera initialized successfully")
            else:
                print("Camera not available")
                self.camera = None
        except Exception as e:
            print(f"Camera initialization failed: {e}")
            self.camera = None
            
    def _create_ui(self):
        """Create UI elements"""
        # Camera preview area
        self.camera_rect = pygame.Rect(50, 50, 400, 300)
        
        # Buttons
        button_width = 120
        button_height = 40
        
        if not self.is_photo_taken:
            self.buttons = [
                {'text': 'Take Photo', 'rect': pygame.Rect(50, 370, button_width, button_height), 'action': 'take_photo'},
                {'text': 'Back', 'rect': pygame.Rect(50, 650, 100, button_height), 'action': 'back'}
            ]
        else:
            self.buttons = [
                {'text': 'Retake', 'rect': pygame.Rect(50, 370, button_width, button_height), 'action': 'retake'},
                {'text': 'Confirm', 'rect': pygame.Rect(180, 370, button_width, button_height), 'action': 'confirm'},
                {'text': 'Back', 'rect': pygame.Rect(50, 650, 100, button_height), 'action': 'back'}
            ]
        
        # Sliders for customization
        self.sliders = {
            'skin_tone': {'value': 0.5, 'rect': pygame.Rect(500, 200, 200, 20), 'label': 'Skin Tone'},
            'hair_style': {'value': 0.5, 'rect': pygame.Rect(500, 250, 200, 20), 'label': 'Hair Style'},
            'eye_color': {'value': 0.5, 'rect': pygame.Rect(500, 300, 200, 20), 'label': 'Eye Color'}
        }
        
        # Name input area
        self.name_input_rect = pygame.Rect(500, 100, 200, 30)
        
    def handle_event(self, event):
        """Handle avatar creation events"""
        if event.type == pygame.KEYDOWN:
            if self.name_input_active:
                if event.key == pygame.K_RETURN:
                    self.name_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 20:
                        self.player_name += event.unicode
            else:
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._handle_button_action(self.buttons[self.selected_button]['action'])
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check button clicks
                for i, button in enumerate(self.buttons):
                    if button['rect'].collidepoint(mouse_pos):
                        self.selected_button = i
                        self._handle_button_action(button['action'])
                        return
                
                # Check name input click
                if self.name_input_rect.collidepoint(mouse_pos):
                    self.name_input_active = True
                else:
                    self.name_input_active = False
                
                # Check slider clicks
                for slider_name, slider in self.sliders.items():
                    if slider['rect'].collidepoint(mouse_pos):
                        relative_x = mouse_pos[0] - slider['rect'].x
                        slider['value'] = max(0, min(1, relative_x / slider['rect'].width))
                        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                if button['rect'].collidepoint(mouse_pos):
                    self.selected_button = i
                    
    def _handle_button_action(self, action):
        """Handle button actions"""
        from src.game_manager import GameStateType
        
        self.audio_manager.play_sfx("button_click")
        
        if action == 'take_photo':
            self._take_photo()
        elif action == 'retake':
            self._retake_photo()
        elif action == 'confirm':
            self._confirm_avatar()
        elif action == 'back':
            self.game_manager.change_state(GameStateType.MAIN_MENU)
                
    def update(self, dt):
        """Update avatar creation"""
        # Update camera feed
        if self.camera and not self.is_photo_taken:
            self._update_camera()
            
        # Update avatar preview
        if self.is_photo_taken:
            self._update_avatar_preview()
            
    def render(self, screen):
        """Render avatar creation"""
        # Background
        screen.fill(Config.DARK_GRAY)
        
        # Title
        font = pygame.font.Font(None, 48)
        title_text = font.render("Create Your Avatar", True, Config.WHITE)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 30))
        screen.blit(title_text, title_rect)
        
        # Camera preview border
        pygame.draw.rect(screen, Config.WHITE, self.camera_rect, 2)
        
        # Camera feed or captured photo
        if self.camera_surface:
            screen.blit(self.camera_surface, self.camera_rect)
        else:
            # No camera available message
            font = pygame.font.Font(None, 24)
            text = font.render("Camera not available - using default avatar", True, Config.RED)
            text_rect = text.get_rect(center=self.camera_rect.center)
            screen.blit(text, text_rect)
            
        # Draw buttons
        button_font = pygame.font.Font(None, 32)
        for i, button in enumerate(self.buttons):
            color = Config.WHITE if i == self.selected_button else Config.LIGHT_GRAY
            bg_color = Config.BLUE if i == self.selected_button else Config.DARK_GRAY
            
            pygame.draw.rect(screen, bg_color, button['rect'])
            pygame.draw.rect(screen, color, button['rect'], 2)
            
            text = button_font.render(button['text'], True, color)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
        
        # Draw customization UI if photo taken
        if self.is_photo_taken:
            self._draw_customization_ui(screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        if not self.is_photo_taken:
            instruction_text = font.render("Position yourself in the camera and take a photo", True, Config.LIGHT_GRAY)
        else:
            instruction_text = font.render("Customize your avatar and confirm when ready", True, Config.LIGHT_GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 430))
        screen.blit(instruction_text, instruction_rect)
        
    def _draw_customization_ui(self, screen):
        """Draw customization interface"""
        font = pygame.font.Font(None, 24)
        
        # Name input
        name_label = font.render("Player Name:", True, Config.WHITE)
        screen.blit(name_label, (500, 75))
        
        # Name input box
        input_color = Config.WHITE if self.name_input_active else Config.LIGHT_GRAY
        pygame.draw.rect(screen, Config.DARK_GRAY, self.name_input_rect)
        pygame.draw.rect(screen, input_color, self.name_input_rect, 2)
        
        name_text = font.render(self.player_name, True, Config.WHITE)
        screen.blit(name_text, (self.name_input_rect.x + 5, self.name_input_rect.y + 5))
        
        # Sliders
        for slider_name, slider in self.sliders.items():
            # Label
            label_text = font.render(slider['label'] + ":", True, Config.WHITE)
            screen.blit(label_text, (slider['rect'].x, slider['rect'].y - 25))
            
            # Slider track
            pygame.draw.rect(screen, Config.GRAY, slider['rect'])
            
            # Slider handle
            handle_x = slider['rect'].x + int(slider['value'] * slider['rect'].width)
            handle_rect = pygame.Rect(handle_x - 5, slider['rect'].y - 5, 10, slider['rect'].height + 10)
            pygame.draw.rect(screen, Config.WHITE, handle_rect)
        
        # Avatar preview
        if self.avatar_surface:
            preview_rect = pygame.Rect(500, 350, 200, 200)
            pygame.draw.rect(screen, Config.WHITE, preview_rect, 2)
            scaled_avatar = pygame.transform.scale(self.avatar_surface, (200, 200))
            screen.blit(scaled_avatar, preview_rect)
            
    def _update_camera(self):
        """Update camera feed"""
        if not self.camera:
            return
            
        try:
            import cv2
            import numpy as np
            
            ret, frame = self.camera.read()
            if ret:
                # Flip horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize to fit preview area
                frame = cv2.resize(frame, (self.camera_rect.width, self.camera_rect.height))
                
                # Convert to pygame surface
                frame = np.rot90(frame)
                frame = np.flipud(frame)
                self.camera_surface = pygame.surfarray.make_surface(frame)
        except Exception as e:
            print(f"Camera update error: {e}")
            
    def _take_photo(self):
        """Take a photo"""
        if not self.camera:
            # Create default avatar if no camera
            self._create_default_avatar()
            self.is_photo_taken = True
            self._create_ui()
            self.audio_manager.play_sfx("camera_shutter")
            return
            
        try:
            import cv2
            import numpy as np
            
            ret, frame = self.camera.read()
            if ret:
                # Process the captured frame
                frame = cv2.flip(frame, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.camera_rect.width, self.camera_rect.height))
                
                # Store captured image
                self.captured_image = frame.copy()
                
                # Convert to pygame surface
                frame = np.rot90(frame)
                frame = np.flipud(frame)
                self.camera_surface = pygame.surfarray.make_surface(frame)
                
                # Update state
                self.is_photo_taken = True
                self._create_ui()
                
                # Play camera sound
                self.audio_manager.play_sfx("camera_shutter")
        except Exception as e:
            print(f"Photo capture error: {e}")
            self._create_default_avatar()
            self.is_photo_taken = True
            self._create_ui()
            
    def _create_default_avatar(self):
        """Create default avatar"""
        import numpy as np
        
        # Create a simple default avatar
        width, height = 200, 200
        avatar_array = np.zeros((width, height, 3), dtype=np.uint8)
        
        # Fill with a gradient
        for y in range(height):
            for x in range(width):
                avatar_array[x, y] = [100 + x // 3, 150 + y // 3, 200]
        
        self.captured_image = avatar_array
        self.camera_surface = pygame.surfarray.make_surface(avatar_array)
            
    def _retake_photo(self):
        """Retake photo"""
        self.is_photo_taken = False
        self.captured_image = None
        self._create_ui()
        
    def _update_avatar_preview(self):
        """Update avatar preview with customizations"""
        if self.captured_image is None:
            return
            
        try:
            import cv2
            import numpy as np
            
            # Create avatar preview
            avatar_img = cv2.resize(self.captured_image, (200, 200))
            
            # Apply customizations based on slider values
            skin_tone = self.sliders['skin_tone']['value']
            
            # Simple color adjustments
            if skin_tone != 0.5:
                avatar_img = self._adjust_skin_tone(avatar_img, skin_tone)
                
            # Convert to pygame surface
            avatar_img = np.rot90(avatar_img)
            avatar_img = np.flipud(avatar_img)
            self.avatar_surface = pygame.surfarray.make_surface(avatar_img)
        except Exception as e:
            print(f"Avatar preview error: {e}")
            
    def _adjust_skin_tone(self, image, tone_value):
        """Adjust skin tone of the image"""
        try:
            import cv2
            import numpy as np
            
            # Simple color adjustment
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Adjust saturation based on tone value
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (0.5 + tone_value), 0, 255)
            
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        except:
            return image
        
    def _confirm_avatar(self):
        """Confirm avatar creation"""
        # Save avatar data
        player_data = self.game_manager.get_player_data()
        player_data['has_avatar'] = True
        player_data['player_name'] = self.player_name
        player_data['skin_tone'] = self.sliders['skin_tone']['value']
        player_data['hair_style'] = self.sliders['hair_style']['value']
        player_data['eye_color'] = self.sliders['eye_color']['value']
        
        # Save avatar image if available
        if self.captured_image is not None:
            try:
                import cv2
                avatar_path = os.path.join(Config.SAVES_DIR, "avatar.png")
                cv2.imwrite(avatar_path, cv2.cvtColor(self.captured_image, cv2.COLOR_RGB2BGR))
                player_data['avatar_path'] = avatar_path
            except Exception as e:
                print(f"Failed to save avatar image: {e}")
                player_data['avatar_path'] = ''
        
        self.game_manager.set_player_data(player_data)
        
        # Go to game
        from src.game_manager import GameStateType
        self.game_manager.change_state(GameStateType.PLAYING)