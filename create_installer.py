#!/usr/bin/env python3
"""
Create installer packages for StormRunner
"""

import os
import sys
import shutil
import zipfile
import platform
from pathlib import Path

def create_portable_package():
    """Create portable game package"""
    system = platform.system().lower()
    
    # Create package directory
    package_name = f"StormRunner-Portable-{system}"
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copy game files
    game_files = [
        "main.py", "run.py", "requirements.txt", "README.md", 
        "LICENSE", "QUICK_START.md", "run_game.py"
    ]
    
    for file in game_files:
        if os.path.exists(file):
            shutil.copy2(file, package_name)
    
    # Copy source directory
    if os.path.exists("src"):
        shutil.copytree("src", os.path.join(package_name, "src"))
    
    # Create launcher scripts
    if system == "windows":
        with open(os.path.join(package_name, "START_GAME.bat"), "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting StormRunner...\n")
            f.write("python run_game.py\n")
            f.write("pause\n")
    else:
        with open(os.path.join(package_name, "START_GAME.sh"), "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting StormRunner...'\n")
            f.write("python3 run_game.py\n")
        os.chmod(os.path.join(package_name, "START_GAME.sh"), 0o755)
    
    # Create README for package
    with open(os.path.join(package_name, "HOW_TO_PLAY.txt"), "w") as f:
        f.write("STORMRUNNER - HOW TO PLAY\n")
        f.write("=" * 30 + "\n\n")
        f.write("QUICK START:\n")
        if system == "windows":
            f.write("1. Double-click START_GAME.bat\n")
        else:
            f.write("1. Run ./START_GAME.sh\n")
        f.write("2. Wait for automatic setup\n")
        f.write("3. Enjoy the game!\n\n")
        f.write("CONTROLS:\n")
        f.write("- WASD/Arrow Keys: Move\n")
        f.write("- Shift: Run\n")
        f.write("- Space: Jump\n")
        f.write("- E: Interact\n")
        f.write("- 1-3: Change Weather\n")
        f.write("- ESC: Pause\n\n")
        f.write("REQUIREMENTS:\n")
        f.write("- Python 3.7+\n")
        f.write("- Webcam (optional)\n")
        f.write("- Audio device\n")
    
    # Create ZIP archive
    zip_name = f"{package_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Created portable package: {zip_name}")
    print(f"📁 Package size: {os.path.getsize(zip_name) / 1024 / 1024:.1f} MB")
    
    return zip_name

def create_web_package():
    """Create web-ready package"""
    web_dir = "StormRunner-Web"
    if os.path.exists(web_dir):
        shutil.rmtree(web_dir)
    os.makedirs(web_dir)
    
    # Create index.html
    with open(os.path.join(web_dir, "index.html"), "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>StormRunner - Download</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .download-btn { background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
        .screenshot { max-width: 100%; height: auto; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>🌟 StormRunner - 3D Adventure Game</h1>
    <p>Experience thrilling 3D adventure with dynamic weather, avatar customization, and immersive gameplay!</p>
    
    <h2>🎮 Features</h2>
    <ul>
        <li>✅ Avatar Creation with Webcam</li>
        <li>✅ Dynamic Weather System</li>
        <li>✅ 3D-Style Graphics</li>
        <li>✅ Immersive Audio</li>
        <li>✅ Cross-Platform Support</li>
    </ul>
    
    <h2>📥 Download</h2>
    <a href="StormRunner-Portable-windows.zip" class="download-btn">Download for Windows</a>
    <a href="StormRunner-Portable-darwin.zip" class="download-btn">Download for macOS</a>
    <a href="StormRunner-Portable-linux.zip" class="download-btn">Download for Linux</a>
    
    <h2>🚀 How to Play</h2>
    <ol>
        <li>Download and extract the game</li>
        <li>Run START_GAME script</li>
        <li>Allow camera access for avatar creation</li>
        <li>Enjoy the adventure!</li>
    </ol>
    
    <h2>🎯 System Requirements</h2>
    <ul>
        <li>Python 3.7+ (auto-installed)</li>
        <li>4GB RAM</li>
        <li>Webcam (optional)</li>
        <li>Audio device</li>
    </ul>
</body>
</html>""")
    
    print(f"✅ Created web package: {web_dir}/")

def main():
    """Create all installer packages"""
    print("🏗️  Creating StormRunner Installer Packages")
    print("=" * 50)
    
    # Create portable package
    zip_file = create_portable_package()
    
    # Create web package
    create_web_package()
    
    print("\n🎉 All packages created successfully!")
    print("\nDistribution files:")
    print(f"📦 Portable: {zip_file}")
    print(f"🌐 Web: StormRunner-Web/")
    print("\nReady for distribution! 🚀")

if __name__ == "__main__":
    main()