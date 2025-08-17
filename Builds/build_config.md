# StormRunner Build Configuration

## Platform-Specific Build Settings

### Windows Build
- Target Platform: Windows
- Architecture: x86_64
- Graphics API: DirectX 11/12
- Compression: LZ4HC
- Build Type: Development/Release

### Android Build
- Target Platform: Android
- Minimum API Level: 24 (Android 7.0)
- Target API Level: 33 (Android 13)
- Architecture: ARM64
- Graphics API: OpenGL ES 3.1, Vulkan
- Compression: LZ4HC

### iOS Build
- Target Platform: iOS
- Minimum iOS Version: 12.0
- Architecture: ARM64
- Graphics API: Metal
- Compression: LZ4HC

## Build Steps

1. **Open Unity Project**
2. **File > Build Settings**
3. **Select Target Platform**
4. **Configure Player Settings**
5. **Build and Run**

## Required Dependencies

- Unity 2022.3 LTS
- Universal Render Pipeline
- Input System Package
- Cinemachine Package
- Post Processing Package

## Performance Optimization

- Enable GPU Instancing
- Use LOD Groups
- Optimize Texture Compression
- Enable Occlusion Culling
- Use Light Probes
