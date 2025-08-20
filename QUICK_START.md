# 🎮 StormRunner - QUICK START GUIDE

## ⚡ INSTANT PLAY (30 seconds)

### Step 1: Download & Extract
Download the game files and extract to any folder.

### Step 2: Run the Game
**Windows:**
```cmd
python run.py
```

**macOS/Linux:**
```bash
python3 run.py
```

**That's it!** The game will automatically:
- Install all required dependencies
- Start the game
- Open the main menu

## 🎯 FIRST TIME PLAYING

1. **Main Menu** → Click "Start Adventure"
2. **Avatar Creation** → Allow camera access → Take photo → Customize → Confirm
3. **Game World** → Use WASD to move, Space to jump, E to interact

## 🚀 CREATE EXECUTABLE (For Distribution)

```bash
python build.py
```

Creates a standalone executable in `builds/` folder that runs without Python installed!

## 📱 CONTROLS

| Key | Action |
|-----|--------|
| WASD/Arrows | Move |
| Shift | Run |
| Space | Jump |
| E | Interact |
| 1-3 | Change Weather |
| ESC | Pause Menu |

## 🌟 FEATURES TO TEST

- ✅ **Avatar Creation** - Take selfie with webcam
- ✅ **Weather System** - Press 1, 2, 3 for different weather
- ✅ **3D World** - Explore buildings and trees
- ✅ **Interactions** - Press E near objects
- ✅ **Audio** - Background music and sound effects

## 🔧 IF SOMETHING GOES WRONG

**Camera not working?** → Game will use default avatar
**No sound?** → Game creates placeholder audio
**Slow performance?** → Game auto-adjusts quality

## 📦 SHARE YOUR GAME

1. Run `python build.py`
2. Share the `builds/StormRunner-[platform]/` folder
3. Users can run the executable directly!

**Need help?** Check `DEPLOYMENT_COMPLETE.md` for detailed instructions.

---
**Ready to play in under 1 minute!** 🎉