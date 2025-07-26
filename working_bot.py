#!/usr/bin/env python3
"""
Working Telegram Bot - Compatible with VS Code environment
"""

import asyncio
import logging
import os
import sys
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
import aiohttp
import subprocess
import tempfile
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = "7563475603:AAH-bhTQky3DLzTAdA-V3MzzbU2p9zRx6eM"
LLAMA_API_URL = "http://127.0.0.1:11500"

# User Information
BOT_OWNER = {
    "first_name": "Chap",
    "last_name": "Arian",
    "username": "@chapariannn",
    "user_id": 7684262149,
    "language": "en",
    "chat_id": 7684262149
}

print(f"🤖 Enhanced Telegram Bot Starting...")
print(f"👤 Owner: {BOT_OWNER['first_name']} {BOT_OWNER['last_name']} ({BOT_OWNER['username']})")

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_msg = f"""🤖 Welcome {user.first_name}!

✨ Enhanced Telegram Bot with AI & Media Processing

🎯 Use /commands to see all available features

🤖 Owner: {BOT_OWNER['first_name']} {BOT_OWNER['last_name']} ({BOT_OWNER['username']})

✅ Bot is fully operational!
"""
    await update.message.reply_text(welcome_msg)
    print(f"📱 /start command from {user.first_name} (@{user.username or 'no_username'})")

async def commands_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_text = """🤖 **ENHANCED BOT COMMANDS**

🤖 **AI FEATURES**
/llama [query] - Llama 3.1:8b AI chat
/test - Test bot functionality

🎵 **MEDIA PROCESSING**  
/ffmpeg_test - Test FFmpeg availability

📱 **BASIC**
/start - Initialize bot
/commands - This help panel
/status - Bot status

🔗 **LINKS**
📸 [Instagram](https://www.instagram.com/am_.shi)
🔗 [LinkedIn](https://www.linkedin.com/in/amir-shirkhodaee)
🔗 [Portfolio](https://amsh23.github.io/my-portfolio/)
"""
    await update.message.reply_text(commands_text, parse_mode="Markdown")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot is working perfectly! All systems operational.")
    print(f"📱 /test command executed for user {update.effective_user.first_name}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status_msg = """📊 **Bot Status Report**

✅ Core functionality: ONLINE
✅ Telegram API: Connected
✅ Command processing: Active
⚙️ FFmpeg: Checking...
🦙 Llama API: Checking...

🔢 Bot Version: Enhanced v2.0
⏰ Uptime: Active
"""
    await update.message.reply_text(status_msg, parse_mode="Markdown")

async def llama_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("❌ Usage: /llama your_question")
        return

    query = " ".join(context.args)
    await update.message.reply_text("🤔 Thinking... (connecting to Llama)")
    
    try:
        payload = {
            "model": "llama3.1:8b",
            "prompt": query,
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{LLAMA_API_URL}/api/generate", 
                              json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    data = await response.json()
                    reply = data.get("response", "⚠️ No response from Llama")
                    
                    # Split long responses
                    if len(reply) > 4096:
                        for i in range(0, len(reply), 4096):
                            await update.message.reply_text(reply[i:i+4096])
                    else:
                        await update.message.reply_text(f"🦙 **Llama:** {reply}")
                else:
                    await update.message.reply_text("❌ Llama API unavailable. Make sure Ollama is running.")
    except asyncio.TimeoutError:
        await update.message.reply_text("⏱️ Llama response timeout. Try again.")
    except Exception as e:
        await update.message.reply_text(f"❌ Llama Error: {str(e)}")

async def ffmpeg_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            await update.message.reply_text(f"✅ FFmpeg available:\n`{version_line}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ FFmpeg not working properly")
    except FileNotFoundError:
        await update.message.reply_text("❌ FFmpeg not installed. Install from https://ffmpeg.org/")
    except Exception as e:
        await update.message.reply_text(f"❌ FFmpeg test error: {str(e)}")

# Main bot function
def main():
    print("🔧 Creating bot application...")
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    print("📝 Adding command handlers...")
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands_help))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("llama", llama_chat))
    application.add_handler(CommandHandler("ffmpeg_test", ffmpeg_test))
    
    print("⚙️ Setting up bot commands...")
    
    # Set bot commands for Telegram UI
    async def setup_commands():
        commands = [
            BotCommand("start", "Initialize bot"),
            BotCommand("commands", "Show all features"),
            BotCommand("test", "Test functionality"),
            BotCommand("status", "Bot status"),
            BotCommand("llama", "Llama AI chat"),
            BotCommand("ffmpeg_test", "Test FFmpeg")
        ]
        await application.bot.set_my_commands(commands)
        print("✅ Bot commands configured")
    
    # Run setup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup_commands())
    
    print("🎯 Bot is ready!")
    print("✅ Send /start or /test in Telegram to verify")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    # Start polling
    try:
        application.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        logger.exception("Bot error")

if __name__ == "__main__":
    main()
