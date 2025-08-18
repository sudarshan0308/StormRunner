# StormRunner Build Instructions

## Prerequisites

Before building StormRunner, ensure you have the following installed:

### Unity Requirements
- Unity 2022.3 LTS or later
- Universal Render Pipeline (URP) package
- Input System package
- Cinemachine package
- Post Processing package
- TextMeshPro package

### Platform-Specific Requirements

#### Windows Build
- Visual Studio 2019/2022 with C++ build tools
- Windows 10 SDK

#### Android Build
- Android SDK (API Level 24 minimum, 33 target)
- Android NDK
- Java Development Kit (JDK) 8 or later
- Android Studio (recommended)

#### iOS Build
- Xcode 14 or later
- iOS 12.0 minimum deployment target
- Apple Developer Account (for device deployment)

## Build Process

### 1. Project Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/StormRunner.git
   cd StormRunner
   ```

2. **Open in Unity**
   - Launch Unity Hub
   - Click "Open" and select the StormRunner folder
   - Wait for Unity to import all assets and packages

3. **Verify Package Installation**
   - Open Package Manager (Window > Package Manager)
   - Ensure all required packages are installed:
     - Universal Render Pipeline
     - Input System
     - Cinemachine
     - Post Processing
     - TextMeshPro

### 2. Configure Build Settings

1. **Open Build Settings**
   - Go to File > Build Settings
   - Verify that all scenes are added:
     - MainMenu
     - AvatarCreation
     - GameScene

2. **Configure Player Settings**
   - Click "Player Settings" in Build Settings
   - Set Company Name: "StormRunner Studios"
   - Set Product Name: "StormRunner"
   - Set Version: "1.0.0"

### 3. Platform-Specific Builds

#### Windows Build

1. **Select Platform**
   - In Build Settings, select "PC, Mac & Linux Standalone"
   - Set Target Platform to "Windows"
   - Set Architecture to "x86_64"

2. **Configure Settings**
   - Player Settings > PC, Mac & Linux Settings
   - Set Fullscreen Mode: "Fullscreen Window"
   - Set Default Screen Width: 1920
   - Set Default Screen Height: 1080

3. **Build**
   - Click "Build" in Build Settings
   - Choose output directory (e.g., Builds/Windows/)
   - Wait for build completion

#### Android Build

1. **Select Platform**
   - In Build Settings, select "Android"
   - Click "Switch Platform"

2. **Configure Android Settings**
   - Player Settings > Android Settings
   - Set Package Name: "com.stormrunnerstudios.stormrunner"
   - Set Minimum API Level: 24 (Android 7.0)
   - Set Target API Level: 33 (Android 13)
   - Set Scripting Backend: IL2CPP
   - Set Target Architectures: ARM64

3. **Keystore Setup** (for release builds)
   - Publishing Settings > Keystore Manager
   - Create new keystore or use existing
   - Set keystore password and key alias

4. **Build**
   - Click "Build" for APK or "Build App Bundle" for AAB
   - Choose output directory (e.g., Builds/Android/)
   - Wait for build completion

#### iOS Build

1. **Select Platform**
   - In Build Settings, select "iOS"
   - Click "Switch Platform"

2. **Configure iOS Settings**
   - Player Settings > iOS Settings
   - Set Bundle Identifier: "com.stormrunnerstudios.stormrunner"
   - Set Target minimum iOS Version: 12.0
   - Set Target Device: iPhone & iPad
   - Set Architecture: ARM64

3. **Build**
   - Click "Build" in Build Settings
   - Choose output directory (e.g., Builds/iOS/)
   - Wait for build completion

4. **Xcode Configuration**
   - Open generated Xcode project
   - Set Development Team
   - Configure signing certificates
   - Build and archive for distribution

### 4. Automated Building

You can use the built-in BuildManager for automated builds:

1. **Using Menu Commands**
   - StormRunner > Build All Platforms
   - StormRunner > Build Windows
   - StormRunner > Build Android

2. **Command Line Building**
   ```bash
   # Windows
   "C:\Program Files\Unity\Hub\Editor\2022.3.19f1\Editor\Unity.exe" -batchmode -quit -projectPath . -executeMethod BuildManager.BuildWindows

   # macOS
   /Applications/Unity/Hub/Editor/2022.3.19f1/Unity.app/Contents/MacOS/Unity -batchmode -quit -projectPath . -executeMethod BuildManager.BuildWindows
   ```

## Testing Builds

### Windows Testing
1. Navigate to build directory
2. Run StormRunner.exe
3. Test all game features:
   - Main menu navigation
   - Avatar creation (webcam functionality)
   - Player movement and controls
   - Weather system
   - Audio system

### Android Testing
1. Enable Developer Options on Android device
2. Enable USB Debugging
3. Install APK: `adb install StormRunner.apk`
4. Test on device with touch controls

### iOS Testing
1. Connect iOS device to Mac
2. Open Xcode project
3. Select connected device
4. Build and run on device
5. Test touch controls and performance

## Performance Optimization

### Build Optimization
- Enable "Strip Engine Code" in Player Settings
- Set Managed Stripping Level to "High"
- Enable "Optimize Mesh Data" in Player Settings
- Use texture compression appropriate for platform

### Runtime Optimization
- The PerformanceManager automatically adjusts quality settings
- Monitor frame rate and adjust settings as needed
- Use the TestingManager (F1 key) for performance testing

## Troubleshooting

### Common Issues

1. **Missing Packages**
   - Solution: Install required packages via Package Manager

2. **Build Errors**
   - Check Unity Console for specific errors
   - Verify all scripts compile without errors
   - Ensure all required assets are present

3. **Android Build Issues**
   - Verify Android SDK and NDK paths in Unity preferences
   - Check minimum API level compatibility
   - Ensure keystore is properly configured

4. **iOS Build Issues**
   - Verify Xcode version compatibility
   - Check iOS deployment target
   - Ensure proper signing certificates

### Performance Issues
- Use the built-in PerformanceManager for dynamic quality adjustment
- Monitor frame rate using the TestingManager
- Adjust quality settings based on target device capabilities

## Distribution

### Windows
- Create installer using tools like Inno Setup or NSIS
- Distribute via Steam, Epic Games Store, or direct download

### Android
- Upload to Google Play Console
- Follow Google Play policies and guidelines
- Test on various Android devices

### iOS
- Submit to App Store via App Store Connect
- Follow Apple's App Store Review Guidelines
- Test on various iOS devices

## Support

For build issues or questions:
1. Check Unity Console for error messages
2. Verify all prerequisites are installed
3. Test on clean Unity installation
4. Contact development team with specific error details