@echo off
setlocal

echo =========================================
echo 🌀 Building BotFury Mod for Minecraft 🌀
echo =========================================

echo 1/3 Unpacking dependencies...
call binaries\unpack_all.bat

echo 2/3 Building the Fabric mod...
cd minecraft-bots\botfury-mod
call gradlew.bat build

echo 3/3 Build complete!
cd ..\..

set ARTIFACT=minecraft-bots\botfury-mod\build\libs\botfury-0.1.0.jar
if exist "%ARTIFACT%" (
    echo =========================================
    echo ✅ SUCCESS! The BotFury mod has been built.
    echo You can find your mod JAR file at:
    echo -^> %ARTIFACT%
    echo Copy this file to your Minecraft 'mods' folder to play!
    echo =========================================
) else (
    echo ❌ FAILURE: The JAR file was not found. Please check the build logs above for errors.
    exit /b 1
)
