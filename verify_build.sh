#!/bin/sh
set -e

echo "Unpacking binaries..."
./binaries/unpack_all.sh

echo "Setting permissions..."
chmod +x minecraft-bots/botfury-mod/gradlew

echo "Building mod..."
cd minecraft-bots/botfury-mod
./gradlew build

if [ -f "build/devlibs/botfury-0.1.0-dev.jar" ]; then
    echo "SUCCESS: Mod compiled successfully."
else
    echo "FAILURE: JAR not found."
    exit 1
fi
