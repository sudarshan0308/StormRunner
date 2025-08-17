# StormRunner Project Structure

## Overview
StormRunner is a 3D adventure game built with Unity, featuring realistic weather effects, avatar customization, and cross-platform support.

## Directory Structure

```
StormRunner/
├── Assets/
│   ├── Scripts/                    # C# game scripts
│   │   ├── GameManager.cs         # Main game controller
│   │   ├── PlayerController.cs    # Player movement and interaction
│   │   ├── CameraController.cs    # Third-person camera system
│   │   ├── WeatherSystem.cs       # Dynamic weather effects
│   │   ├── AvatarCreationSystem.cs # Selfie-based avatar creation
│   │   ├── MainMenuUI.cs          # Main menu interface
│   │   ├── AudioManager.cs        # Dolby audio system
│   │   └── InputActions.inputactions # Input system configuration
│   ├── Prefabs/                   # Reusable game objects
│   ├── Materials/                  # 3D materials and shaders
│   ├── Textures/                   # 2D textures and images
│   ├── Models/                     # 3D models and meshes
│   ├── Audio/                      # Sound effects and music
│   ├── Scenes/                     # Game scenes
│   └── UI/                         # User interface elements
├── ProjectSettings/                 # Unity project configuration
├── Packages/                       # Unity packages and dependencies
├── Builds/                         # Platform-specific builds
├── README.md                       # Project overview
├── DEPLOYMENT.md                   # Deployment instructions
├── PROJECT_STRUCTURE.md            # This file
└── LICENSE                         # Project license
```

## Core Systems

### 1. Game Management
- **GameManager.cs**: Central game state management
- Handles scene transitions, game state, and player data
- Singleton pattern for global access

### 2. Player System
- **PlayerController.cs**: Character movement and physics
- WASD movement, jumping, running, interaction
- Input system integration for cross-platform support

### 3. Camera System
- **CameraController.cs**: Third-person camera following
- Cinemachine integration for smooth camera movement
- Collision detection and camera shake effects

### 4. Weather System
- **WeatherSystem.cs**: Dynamic weather simulation
- Rain, thunder, lightning, storm effects
- Particle systems and audio integration

### 5. Avatar Creation
- **AvatarCreationSystem.cs**: Selfie-based avatar generation
- Webcam integration for photo capture
- Real-time avatar customization

### 6. Audio System
- **AudioManager.cs**: High-quality audio management
- Dolby audio support
- Dynamic audio mixing based on weather

### 7. User Interface
- **MainMenuUI.cs**: Main menu and settings
- Responsive UI with animations
- Settings persistence

## Key Features

- **Cross-Platform**: Windows, iOS, Android support
- **Realistic Weather**: Dynamic storm effects with particles
- **Avatar Customization**: Selfie-based character creation
- **Dolby Audio**: High-quality spatial audio
- **Modern Graphics**: URP rendering pipeline
- **Responsive Controls**: Input system for all platforms

## Dependencies

- Unity 2022.3 LTS
- Universal Render Pipeline (URP)
- Input System Package
- Cinemachine Package
- Post Processing Package
- TextMeshPro

## Build Targets

- **Windows**: x86_64, DirectX 11/12
- **Android**: ARM64, OpenGL ES 3.1, Vulkan
- **iOS**: ARM64, Metal

## Development Workflow

1. Open project in Unity
2. Install required packages
3. Configure platform-specific settings
4. Test in editor
5. Build for target platform
6. Deploy and test on device

## Performance Considerations

- GPU instancing for repeated objects
- LOD groups for distant objects
- Texture compression optimization
- Occlusion culling
- Light probe usage
