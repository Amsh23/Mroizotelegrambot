@echo off
title Enhanced Telegram Bot - Starting...

echo.
echo 🤖 Enhanced Telegram Bot
echo ========================
echo.

echo 🔍 Running system check...
python test_bot.py

echo.
echo 🚀 Starting the bot...
echo Press Ctrl+C to stop
echo.

python oizo.py
