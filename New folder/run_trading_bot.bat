@echo off
title Trading Bot
color 0A

echo ========================================
echo    Trading Bot Launcher
echo ========================================
echo.
echo 1. Run Original CLI (Single Order)
echo 2. Run Interactive Mode
echo 3. Run Enhanced CLI (Menu System)
echo 4. Run Quick Test
echo 5. Exit
echo.

set /p choice="Select option (1-5): "

if "%choice%"=="1" goto single
if "%choice%"=="2" goto interactive
if "%choice%"=="3" goto enhanced
if "%choice%"=="4" goto test
if "%choice%"=="5" goto exit

:single
echo.
echo Example: python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python cli.py
goto exit

:interactive
python cli.py --interactive
goto exit

:enhanced
python enhanced_cli.py
goto exit

:test
python quick_test.py
goto exit

:exit
echo.
echo Goodbye!
pause