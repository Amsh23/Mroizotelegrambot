#!/usr/bin/env python3
"""
Quick test version with immediate output
"""

import asyncio
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

TOKEN = "7563475603:AAH-bhTQky3DLzTAdA-V3MzzbU2p9zRx6eM"

print("🚀 Starting Enhanced Telegram Bot...")
print(f"🔑 Using token: {TOKEN[:20]}...")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_msg = f"""🤖 Welcome {user.first_name}!

✨ Enhanced Telegram Bot with AI & Media Processing

🎯 Use /commands to see all available features

🤖 Owner: Chap Arian (@chapariannn)
"""
    await update.message.reply_text(welcome_msg)
    print(f"📱 Responded to /start from {user.first_name} (@{user.username})")

async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_text = """🤖 **ENHANCED BOT COMMANDS**

🤖 **AI FEATURES**
/llama [query] - Llama 3.1:8b AI chat
/test - Test bot functionality

📱 **BASIC**
/start - Initialize bot
/commands - This help panel
"""
    await update.message.reply_text(commands_text, parse_mode="Markdown")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot is working perfectly! All systems operational.")

async def main():
    print("🔧 Creating application...")
    application = Application.builder().token(TOKEN).build()
    
    print("📝 Adding command handlers...")
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("commands", commands_command))
    application.add_handler(CommandHandler("test", test_command))
    
    # Set bot commands
    commands = [
        BotCommand("start", "Initialize bot"),
        BotCommand("commands", "Show all features"),
        BotCommand("test", "Test bot functionality")
    ]
    
    print("⚙️ Configuring bot commands...")
    await application.bot.set_my_commands(commands)
    
    print("🎯 Bot is ready!")
    print("✅ Send /start or /test in Telegram to verify functionality")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
