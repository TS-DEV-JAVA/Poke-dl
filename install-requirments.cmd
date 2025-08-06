@echo off
title Poke-DL-Setup
color 1
echo.
echo     ____  ____  __ __ ______     ____  __        _____ ______________  ______ 
echo    / __ \/ __ \/ //_// ____/    / __ \/ /       / ___// ____/_  __/ / / / __ \
echo   / /_/ / / / / ,-  / __/______/ / / / /  ______\__ \/ __/   / / / / / / /_/ /
echo  / ____/ /_/ / // // /__/_____/ /_/ / /__/_____/__/ / /___  / / / /_/ / ____/ 
echo /_/    \____/_/ /_/_____/    /_____/_____/    /____/_____/ /_/  \____/_/      
echo.
echo [!] INSTALLING NEEDED PYTHON PACKAGES...
pip install requests yt-dlp rich cloudscraper beautifulsoup4
echo [!] INSTALLED NEEDED CLI TOOLS...
setlocal

REM dl folder
set "DEST=%CD%\cli-tools"

REM creat folderr if not their
if not exist "%DEST%" mkdir "%DEST%"

REM urls
set "ARIA2_URL=https://github.com/TS-DEV-JAVA/Poke-dl/releases/download/Aria2/aria2c.exe"
set "FFMPEG_URL=https://github.com/TS-DEV-JAVA/Poke-dl/releases/download/1/ffmpeg.exe"
set "MPV_URL=https://github.com/TS-DEV-JAVA/Poke-dl/releases/download/12/mpv.exe"

REM accualy dl them
echo [*] Downloading aria2c.exe...
curl -L "%ARIA2_URL%" -o "%DEST%\aria2c.exe"

echo [*] Downloading ffmpeg.exe...
curl -L "%FFMPEG_URL%" -o "%DEST%\ffmpeg.exe"

echo [*] Downloading mpv.exe...
curl -L "%MPV_URL%" -o "%DEST%\mpv.exe"

REM add to path
echo [*] Adding cli-tools to system PATH...
powershell -NoProfile -Command ^
  "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'Machine');" ^
  "if ($oldPath -notlike '*%DEST%*') {" ^
  "  [Environment]::SetEnvironmentVariable('Path', $oldPath + ';%DEST%', 'Machine');" ^
  "  Write-Host '[!] cli-tools added to system PATH.'" ^
  "} else { Write-Host '[!] cli-tools already in system PATH.' }"

echo.
title Poke-DL-Setup-Finished
color a
echo     ____  ____  __ __ ______     ____  __         ___________   ___________ __  ____________ 
echo    / __ \/ __ \/ //_// ____/    / __ \/ /        / ____/  _/ / / /  _/ ___// / / / ____/ __ \
echo   / /_/ / / / / ,/  / __/______/ / / / /  ______/ /_   / //  // // / \__ \/ /_/ / __/ / / / /
echo  / ____/ /_/ / // // /__/_____/ /_/ / /__/_____/ __/ _/ // //  // / ___/ / __  / /___/ /_/ / 
echo /_/    \____/_/ /_/_____/    /_____/_____/    /_/   /___/_/ /_/___//____/_/ /_/_____/_____/  
echo.
echo [!] Done. You Can Now Use Poke-DL
pause