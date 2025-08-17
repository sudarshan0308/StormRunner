# StormRunner - 3D Adventure Game

A thrilling 3D adventure game where players become their own avatar in a dynamic city environment with realistic weather effects.

## Features

- **Avatar Customization**: Take a selfie to generate your personalized avatar
- **Realistic Weather**: Dynamic thunderstorms, lightning, rain, and storm effects
- **Immersive Gameplay**: Third-person camera following your character
- **Cross-Platform**: Runs on Windows, iOS, and Android
- **Dolby Sound**: High-quality audio experience
- **Beautiful Graphics**: Modern, colorful city environment

## Project Structure

```
StormRunner/
├── Assets/
│   ├── Scripts/           # C# game scripts
│   ├── Prefabs/           # Reusable game objects
│   ├── Materials/          # 3D materials and shaders
│   ├── Textures/           # 2D textures and images
│   ├── Models/             # 3D models and meshes
│   ├── Audio/              # Sound effects and music
│   ├── Scenes/             # Game scenes
│   └── UI/                 # User interface elements
├── ProjectSettings/         # Unity project configuration
├── Packages/               # Unity packages and dependencies
└── Builds/                 # Platform-specific builds
```

## Requirements

- Unity 2022.3 LTS or later
- Visual Studio 2019/2022 or Visual Studio Code
- Git for version control

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/StormRunner.git
   cd StormRunner
   ```

2. **Open in Unity**
   - Launch Unity Hub
   - Click "Open" and select the StormRunner folder
   - Wait for Unity to import the project

3. **Install Required Packages**
   - Open Package Manager (Window > Package Manager)
   - Install the following packages:
     - Universal Render Pipeline (URP)
     - Input System
     - Cinemachine
     - Post Processing

4. **Build for Different Platforms**
   - Windows: File > Build Settings > Windows
   - Android: File > Build Settings > Android
   - iOS: File > Build Settings > iOS

## Game Controls

- **WASD**: Move character
- **Mouse**: Look around
- **Space**: Jump
- **Shift**: Sprint
- **E**: Interact
- **Tab**: Open menu

## Development Roadmap

- [x] Project structure setup
- [x] Basic character controller
- [x] Weather system foundation
- [x] Camera system
- [ ] Avatar customization system
- [ ] Weather effects implementation
- [ ] Sound system integration
- [ ] UI development
- [ ] Level design
- [ ] Testing and optimization
- [ ] Platform-specific builds

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the development team.
