# 🎮 StormRunner - Testing Guide

## ⚡ INSTANT TESTING (30 Seconds)

### **Step 1: Launch the Game**
```bash
python run_game.py
```
**OR** double-click:
- **Windows**: `START_GAME.bat`
- **Mac/Linux**: `START_GAME.sh`

### **Step 2: Test All Features**

#### **🎯 Main Menu Testing**
- ✅ Use **Arrow Keys** + **Enter** to navigate
- ✅ Use **Mouse** to click buttons
- ✅ Click "Start Adventure"

#### **📸 Avatar Creation Testing**
1. **Camera Test**: Allow camera access when prompted
2. **Photo Test**: Click "Take Photo" or press Enter
3. **Customization Test**: 
   - Move sliders to adjust appearance
   - Click in name field and type your name
4. **Confirm Test**: Click "Confirm" to proceed

#### **🎮 Gameplay Testing**
- **Movement**: `WASD` or `Arrow Keys`
- **Running**: Hold `Shift` while moving
- **Jumping**: Press `Space`
- **Interaction**: Press `E` near buildings/trees
- **Weather Control**: Press `1`, `2`, `3` for different weather
- **Pause**: Press `ESC` to pause/unpause

#### **🌦️ Weather System Testing**
- **Press 1**: Clear sunny weather
- **Press 2**: Rain with particles
- **Press 3**: Storm with lightning and camera shake

#### **🎵 Audio Testing**
- ✅ Button click sounds
- ✅ Camera shutter sound
- ✅ Interaction sounds
- ✅ Weather audio changes

## 🔧 WHERE TO TEST

### **Local Testing**
```bash
# In your project directory
python run_game.py
```

### **Distribution Testing**
1. **Create portable version**:
   ```bash
   python create_installer.py
   ```
2. **Test the ZIP file**:
   - Extract `StormRunner-Portable-[platform].zip`
   - Run `START_GAME` script
   - Verify it works without Python installed

### **Cross-Platform Testing**
- **Windows**: Test on Windows 10/11
- **macOS**: Test on macOS 10.12+
- **Linux**: Test on Ubuntu/Debian/Fedora

## ✅ TESTING CHECKLIST

### **Core Functionality**
- [ ] Game launches without errors
- [ ] Main menu navigation works
- [ ] Avatar creation completes successfully
- [ ] Player movement is smooth
- [ ] Weather effects display correctly
- [ ] Audio plays without issues
- [ ] Game can be paused and resumed
- [ ] All controls respond properly

### **Error Handling**
- [ ] Camera not available → Uses default avatar
- [ ] Missing dependencies → Auto-installs
- [ ] Audio issues → Creates placeholder sounds
- [ ] Performance problems → Game still playable

### **User Experience**
- [ ] Instructions are clear
- [ ] Controls are intuitive
- [ ] Visual feedback is immediate
- [ ] Game feels responsive
- [ ] No crashes or freezes

## 🚨 TROUBLESHOOTING

### **Camera Issues**
```bash
# If camera doesn't work:
# 1. Check if camera is being used by another app
# 2. Grant camera permissions
# 3. Game will use default avatar automatically
```

### **Performance Issues**
```bash
# If game runs slowly:
# 1. Close other applications
# 2. Game auto-adjusts quality
# 3. Try lower screen resolution
```

### **Audio Issues**
```bash
# If no sound:
# 1. Check system volume
# 2. Game creates placeholder sounds
# 3. Update audio drivers if needed
```

## 🎯 EXPECTED RESULTS

### **Successful Test Results**
- ✅ Game launches in under 10 seconds
- ✅ All features work as described
- ✅ Smooth 60 FPS gameplay
- ✅ Responsive controls
- ✅ Clear visual and audio feedback
- ✅ Professional user experience

### **Performance Targets**
- **Startup Time**: < 10 seconds
- **Frame Rate**: 60 FPS (or 30+ on older hardware)
- **Memory Usage**: < 200 MB
- **File Size**: < 50 MB for distribution

## 🏆 DEPLOYMENT READY

If all tests pass, your game is **100% ready for deployment**!

### **Next Steps**
1. **Create distribution packages**
2. **Upload to your preferred platform**
3. **Share with users**
4. **Collect feedback**

**Your StormRunner game is production-ready!** 🎉