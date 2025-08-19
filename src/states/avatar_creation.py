"""
Avatar creation state with webcam integration
"""

import pygame
import pygame_gui
import cv2
import numpy as np
from src.states.base_state import BaseState
from src.config import Config
from src.game_manager import GameStateType

class AvatarCreationState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.ui_manager = None
        self.camera = None
        self.camera_surface = None
        self.captured_image = None
        self.is_photo_taken = False
        
        # UI elements
        self.take_photo_button = None
        self.retake_button = None
        self.confirm_button = None
        self.back_button = None
        self.name_input = None
        
        # Customization sliders
        self.skin_tone_slider = None
        self.hair_style_slider = None
        self.eye_color_slider = None
        
        # Avatar preview
        self.avatar_surface = None
        
    def enter(self):
        """Initialize avatar creation"""
        self.ui_manager = pygame_gui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.is_photo_taken = False
        
        # Initialize camera
        self._init_camera()
        
        # Create UI elements
        self._create_ui()
        
    def exit(self):
        """Clean up avatar creation"""
        if self.camera:
            self.camera.release()
            
    def _init_camera(self):
        """Initialize webcam"""
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.WEBCAM_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.WEBCAM_HEIGHT)
        except Exception as e:
            print(f"Camera initialization failed: {e}")
            self.camera = None
            
    def _create_ui(self):
        """Create UI elements"""
        # Camera preview area
        self.camera_rect = pygame.Rect(50, 50, 400, 300)
        
        # Buttons
        self.take_photo_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 370, 120, 40),
            text='Take Photo',
            manager=self.ui_manager
        )
        
        self.retake_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(180, 370, 120, 40),
            text='Retake',
            manager=self.ui_manager
        )
        self.retake_button.hide()
        
        self.confirm_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(310, 370, 120, 40),
            text='Confirm',
            manager=self.ui_manager
        )
        self.confirm_button.hide()
        
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 650, 100, 40),
            text='Back',
            manager=self.ui_manager
        )
        
        # Name input
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(500, 100, 200, 30),
            manager=self.ui_manager
        )
        self.name_input.set_text("Player")
        
        # Customization sliders
        self.skin_tone_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(500, 200, 200, 20),
            start_value=0.5,
            value_range=(0.0, 1.0),
            manager=self.ui_manager
        )
        
        self.hair_style_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(500, 250, 200, 20),
            start_value=0.5,
            value_range=(0.0, 1.0),
            manager=self.ui_manager
        )
        
        self.eye_color_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(500, 300, 200, 20),
            start_value=0.5,
            value_range=(0.0, 1.0),
            manager=self.ui_manager
        )
        
    def handle_event(self, event):
        """Handle avatar creation events"""
        self.ui_manager.process_events(event)
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.take_photo_button:
                self._take_photo()
            elif event.ui_element == self.retake_button:
                self._retake_photo()
            elif event.ui_element == self.confirm_button:
                self._confirm_avatar()
            elif event.ui_element == self.back_button:
                self.game_manager.change_state(GameStateType.MAIN_MENU)
                
    def update(self, dt):
        """Update avatar creation"""
        self.ui_manager.update(dt / 1000.0)
        
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
            text = font.render("Camera not available", True, Config.RED)
            text_rect = text.get_rect(center=self.camera_rect.center)
            screen.blit(text, text_rect)
            
        # Labels
        font = pygame.font.Font(None, 24)
        
        # Name label
        name_label = font.render("Player Name:", True, Config.WHITE)
        screen.blit(name_label, (500, 75))
        
        # Customization labels
        skin_label = font.render("Skin Tone:", True, Config.WHITE)
        screen.blit(skin_label, (500, 175))
        
        hair_label = font.render("Hair Style:", True, Config.WHITE)
        screen.blit(hair_label, (500, 225))
        
        eye_label = font.render("Eye Color:", True, Config.WHITE)
        screen.blit(eye_label, (500, 275))
        
        # Avatar preview
        if self.avatar_surface:
            preview_rect = pygame.Rect(500, 350, 200, 200)
            pygame.draw.rect(screen, Config.WHITE, preview_rect, 2)
            screen.blit(self.avatar_surface, preview_rect)
            
        # Instructions
        if not self.is_photo_taken:
            instruction_text = font.render("Position yourself in the camera and take a photo", True, Config.LIGHT_GRAY)
            instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 430))
            screen.blit(instruction_text, instruction_rect)
        else:
            instruction_text = font.render("Customize your avatar and confirm when ready", True, Config.LIGHT_GRAY)
            instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 430))
            screen.blit(instruction_text, instruction_rect)
            
        # Draw UI
        self.ui_manager.draw_ui(screen)
        
    def _update_camera(self):
        """Update camera feed"""
        if not self.camera:
            return
            
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
            
    def _take_photo(self):
        """Take a photo"""
        if not self.camera:
            return
            
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
            
            # Update UI
            self.is_photo_taken = True
            self.take_photo_button.hide()
            self.retake_button.show()
            self.confirm_button.show()
            
            # Play camera sound
            self.audio_manager.play_sfx("camera_shutter")
            
    def _retake_photo(self):
        """Retake photo"""
        self.is_photo_taken = False
        self.captured_image = None
        
        # Update UI
        self.take_photo_button.show()
        self.retake_button.hide()
        self.confirm_button.hide()
        
    def _update_avatar_preview(self):
        """Update avatar preview with customizations"""
        if not self.captured_image is None:
            # Create avatar preview
            avatar_img = cv2.resize(self.captured_image, (200, 200))
            
            # Apply customizations based on slider values
            skin_tone = self.skin_tone_slider.get_current_value()
            hair_style = self.hair_style_slider.get_current_value()
            eye_color = self.eye_color_slider.get_current_value()
            
            # Simple color adjustments (in a real implementation, you'd use more sophisticated image processing)
            if skin_tone != 0.5:
                avatar_img = self._adjust_skin_tone(avatar_img, skin_tone)
                
            # Convert to pygame surface
            avatar_img = np.rot90(avatar_img)
            avatar_img = np.flipud(avatar_img)
            self.avatar_surface = pygame.surfarray.make_surface(avatar_img)
            
    def _adjust_skin_tone(self, image, tone_value):
        """Adjust skin tone of the image"""
        # Simple color adjustment - in practice, you'd use more sophisticated methods
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # Adjust saturation based on tone value
        hsv[:, :, 1] = hsv[:, :, 1] * (0.5 + tone_value)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
    def _confirm_avatar(self):
        """Confirm avatar creation"""
        if not self.captured_image is None:
            # Save avatar data
            player_data = self.game_manager.get_player_data()
            player_data['has_avatar'] = True
            player_data['player_name'] = self.name_input.get_text()
            player_data['skin_tone'] = self.skin_tone_slider.get_current_value()
            player_data['hair_style'] = self.hair_style_slider.get_current_value()
            player_data['eye_color'] = self.eye_color_slider.get_current_value()
            
            # Save avatar image
            import os
            avatar_path = os.path.join(Config.SAVES_DIR, "avatar.png")
            cv2.imwrite(avatar_path, cv2.cvtColor(self.captured_image, cv2.COLOR_RGB2BGR))
            player_data['avatar_path'] = avatar_path
            
            self.game_manager.set_player_data(player_data)
            
            # Go to game
            self.game_manager.change_state(GameStateType.PLAYING)