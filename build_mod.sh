#!/bin/bash
set -e

echo "========================================="
echo "🌀 Building BotFury Mod for Minecraft 🌀"
echo "========================================="

echo "1/3 Unpacking dependencies..."
chmod +x binaries/*.sh
./binaries/unpack_all.sh

echo "2/3 Building the Fabric mod..."
cd minecraft-bots/botfury-mod
chmod +x gradlew
./gradlew build

echo "3/3 Build complete!"
cd ../..

ARTIFACT="minecraft-bots/botfury-mod/build/libs/botfury-0.1.0.jar"
if [ -f "$ARTIFACT" ]; then
    echo "========================================="
    echo "✅ SUCCESS! The BotFury mod has been built."
    echo "You can find your mod JAR file at:"
    echo "-> $ARTIFACT"
    echo "Copy this file to your Minecraft 'mods' folder to play!"
    echo "========================================="
else
    echo "❌ FAILURE: The JAR file was not found. Please check the build logs above for errors."
    exit 1
fi
