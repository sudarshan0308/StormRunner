#!/usr/bin/env python3
"""
Build script for creating distributable versions of StormRunner
"""

import os
import sys
import subprocess
import shutil
import platform

def install_build_tools():
    """Install PyInstaller for building executables"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install PyInstaller: {e}")
        return False

def build_executable():
    """Build executable for current platform"""
    system = platform.system().lower()
    
    # Create builds directory
    os.makedirs("builds", exist_ok=True)
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "StormRunner",
        "--distpath", "builds",
        "--workpath", "build_temp",
        "--specpath", "build_temp",
        "main.py"
    ]
    
    try:
        print(f"Building executable for {system}...")
        subprocess.check_call(cmd)
        
        # Clean up temporary files
        if os.path.exists("build_temp"):
            shutil.rmtree("build_temp")
            
        print(f"Build completed! Executable created in builds/ directory")
        
        # Show final executable name
        if system == "windows":
            exe_name = "StormRunner.exe"
        else:
            exe_name = "StormRunner"
            
        exe_path = os.path.join("builds", exe_name)
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Executable: {exe_path} ({size_mb:.1f} MB)")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_distribution():
    """Create a complete distribution package"""
    system = platform.system().lower()
    
    # Create distribution directory
    dist_dir = f"StormRunner-{system}"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Copy executable
    if system == "windows":
        exe_name = "StormRunner.exe"
    else:
        exe_name = "StormRunner"
        
    exe_source = os.path.join("builds", exe_name)
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, dist_dir)
        
    # Copy documentation
    files_to_copy = ["README.md", "requirements.txt"]
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            
    # Create run script for the distribution
    if system == "windows":
        run_script = os.path.join(dist_dir, "run.bat")
        with open(run_script, 'w') as f:
            f.write("@echo off\n")
            f.write("echo Starting StormRunner...\n")
            f.write("StormRunner.exe\n")
            f.write("pause\n")
    else:
        run_script = os.path.join(dist_dir, "run.sh")
        with open(run_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting StormRunner...'\n")
            f.write("./StormRunner\n")
        os.chmod(run_script, 0o755)
        
    print(f"Distribution package created: {dist_dir}/")
    return True

def main():
    """Main build function"""
    print("StormRunner Build System")
    print("=" * 40)
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("PyInstaller found.")
    except ImportError:
        print("PyInstaller not found. Installing...")
        if not install_build_tools():
            print("Failed to install build tools.")
            return False
            
    # Build executable
    if build_executable():
        print("\nCreating distribution package...")
        create_distribution()
        print("\nBuild process completed successfully!")
        print("\nTo distribute your game:")
        print("1. Share the entire distribution folder")
        print("2. Users can run the game using the executable or run script")
        return True
    else:
        print("Build process failed.")
        return False

if __name__ == "__main__":
    main()