#!/bin/bash
set -e

# Simple local build script to properly display debug outputs for troubleshooting issues like empty artifact generation

echo "Checking required dependencies..."
if ! command -v java &> /dev/null; then
    echo "Java not found. Please install Java 17."
    exit 1
fi
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.10+."
    exit 1
fi
if ! command -v pip &> /dev/null; then
    echo "pip not found. Please install pip."
    exit 1
fi

echo "Installing Python dependencies..."
pip install flask requests pytest

echo "Running Python tests..."
cd flask-dashboard
pytest -v
cd ..

echo "Setting up environment and unpacking binaries..."
chmod +x binaries/*.sh
./binaries/unpack_all.sh
chmod +x minecraft-bots/botfury-mod/gradlew

echo "Building Java Mod..."
cd minecraft-bots/botfury-mod
./gradlew clean build --info

# Specifically re-run remapJar with debug info to check what is going on
./gradlew remapJar --debug

echo "Verifying Build Artifact..."
ARTIFACT="build/devlibs/botfury-0.1.0-dev.jar"
if [ ! -f "$ARTIFACT" ]; then
    echo "Build failed: JAR not found at $ARTIFACT"
    exit 1
fi

FILESIZE=$(stat -c%s "$ARTIFACT")
echo "Artifact size: $FILESIZE bytes"

if [ $FILESIZE -lt 1000 ]; then
    echo "Warning: JAR file is unusually small. Checking contents..."
    jar tf "$ARTIFACT"
    echo "Error: The JAR file seems to be empty or corrupted. This indicates a problem with the gradle build/remap process."
    exit 1
fi

echo "Build complete. Artifact is available at minecraft-bots/botfury-mod/$ARTIFACT"
