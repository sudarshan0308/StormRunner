# StormRunner Deployment Guide

## Prerequisites

- Unity 2022.3 LTS or later
- Visual Studio 2019/2022 (Windows)
- Xcode 14+ (iOS)
- Android Studio (Android)
- Git for version control

## Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/StormRunner.git
   cd StormRunner
   ```

2. **Open in Unity**
   - Launch Unity Hub
   - Click "Open" and select StormRunner folder
   - Wait for project import

3. **Install Dependencies**
   - Open Package Manager (Window > Package Manager)
   - Install required packages listed in manifest.json

## Platform Deployment

### Windows Deployment

1. **Build Settings**
   - File > Build Settings
   - Platform: Windows
   - Architecture: x86_64
   - Build Type: Release

2. **Player Settings**
   - Company Name: Your Company
   - Product Name: StormRunner
   - Version: 1.0.0

3. **Build**
   - Click "Build"
   - Select output directory
   - Wait for build completion

### Android Deployment

1. **Android Setup**
   - Install Android SDK
   - Configure Unity Android settings
   - Set Keystore for signing

2. **Build Settings**
   - Platform: Android
   - Architecture: ARM64
   - Build Type: Release

3. **Build APK**
   - Click "Build APK"
   - Install on device for testing

### iOS Deployment

1. **iOS Setup**
   - Install Xcode
   - Configure Unity iOS settings
   - Set Bundle Identifier

2. **Build Settings**
   - Platform: iOS
   - Architecture: ARM64
   - Build Type: Release

3. **Build and Archive**
   - Click "Build"
   - Open in Xcode
   - Archive and distribute

## Testing

- **Windows**: Test on various Windows versions
- **Android**: Test on multiple devices and API levels
- **iOS**: Test on different iOS versions and devices

## Distribution

- **Windows**: Steam, Epic Games Store, Direct Download
- **Android**: Google Play Store, Amazon Appstore
- **iOS**: Apple App Store

## Performance Optimization

- Enable GPU Instancing
- Use LOD Groups for distant objects
- Optimize texture compression
- Enable occlusion culling
- Use light probes for lighting

## Troubleshooting

- Check Unity Console for errors
- Verify all dependencies are installed
- Test on target devices early
- Monitor performance metrics
