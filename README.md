# StormRunner - 3D Adventure Game (Python Edition)

A thrilling 3D-style adventure game built with Python and Pygame, featuring avatar customization with webcam integration, dynamic weather effects, and immersive gameplay.

## Features

- **Avatar Customization**: Take a selfie using your webcam to create your personalized avatar
- **Dynamic Weather System**: Experience realistic weather changes including clear skies, rain, and thunderstorms
- **3D-Style Graphics**: Pseudo-3D rendering with depth effects and perspective
- **Immersive Audio**: Dynamic sound effects and background music
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Easy Deployment**: Simple Python setup with minimal dependencies

## Quick Start

### Option 1: Quick Run (Recommended)
```bash
python run.py
```
This will automatically install dependencies and start the game.

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Requirements

- Python 3.7 or higher
- Webcam (for avatar creation)
- Audio output device

## Dependencies

All dependencies are automatically installed when using `run.py`:

- `pygame` - Game engine and graphics
- `opencv-python` - Webcam and image processing
- `numpy` - Numerical operations
- `Pillow` - Image manipulation
- `pygame-gui` - User interface elements

## Game Controls

- **WASD / Arrow Keys**: Move character
- **Shift**: Run/Sprint
- **Space**: Jump
- **E**: Interact with objects
- **1-3**: Change weather (Clear/Rain/Storm)
- **ESC/Tab**: Pause menu

## Game Features

### Avatar Creation
1. Launch the game and click "Start Adventure"
2. If no avatar exists, you'll be taken to avatar creation
3. Allow camera access when prompted
4. Position yourself in the camera view and click "Take Photo"
5. Customize your avatar with sliders for skin tone, hair, and eyes
6. Enter your player name and click "Confirm"

### Weather System
- **Clear Weather**: Bright blue skies with good visibility
- **Rain**: Animated rain particles with cloudy skies
- **Storm**: Heavy rain with lightning effects and camera shake

### 3D-Style World
- Pseudo-3D buildings with depth and perspective
- Parallax scrolling for immersive movement
- Dynamic camera system that follows the player

## File Structure

```
StormRunner/
├── main.py                 # Main game entry point
├── run.py                  # Quick start script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── config.py          # Game configuration
│   ├── game_manager.py    # Main game manager
│   ├── audio_manager.py   # Audio system
│   ├── save_manager.py    # Save/load system
│   ├── states/            # Game states
│   │   ├── main_menu.py   # Main menu
│   │   ├── avatar_creation.py # Avatar creation
│   │   └── game_state.py  # Main gameplay
│   ├── entities/          # Game entities
│   │   └── player.py      # Player character
│   └── systems/           # Game systems
│       ├── weather_system.py # Weather effects
│       └── camera_system.py  # Camera control
├── assets/                # Game assets (auto-created)
├── saves/                 # Save files (auto-created)
└── builds/                # Distribution builds
```

## Building for Distribution

### Windows Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Cross-Platform
The game runs natively on:
- **Windows** 7/8/10/11
- **macOS** 10.12+
- **Linux** (Ubuntu, Debian, Fedora, etc.)

## Troubleshooting

### Camera Issues
- Ensure your webcam is not being used by another application
- Grant camera permissions when prompted
- If camera fails, the game will still work with a default avatar

### Performance Issues
- Close other applications to free up system resources
- The game automatically adjusts quality based on performance
- Reduce screen resolution if needed

### Audio Issues
- Ensure audio drivers are up to date
- Check system volume settings
- The game creates placeholder sounds if audio files are missing

## Development

### Adding New Features
1. Create new modules in the appropriate `src/` subdirectory
2. Follow the existing code structure and patterns
3. Update configuration in `src/config.py` as needed

### Custom Assets
- Place audio files in `assets/audio/` (OGG format recommended)
- Place images in `assets/images/` (PNG format recommended)
- The game will automatically use custom assets if available

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your Python version is 3.7 or higher

## Version History

- **v1.0.0** - Initial Python release with full feature set
  - Avatar creation with webcam
  - Dynamic weather system
  - 3D-style graphics
  - Cross-platform support
  - Complete audio system

Enjoy your adventure in StormRunner!