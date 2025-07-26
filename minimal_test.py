#!/usr/bin/env python3
"""
Minimal bot test to identify the issue
"""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("🔍 Starting minimal bot test...")

try:
    print("1. Testing basic imports...")
    import asyncio
    print("   ✅ asyncio imported")
    
    import os
    print("   ✅ os imported")
    
    from telegram import Update, BotCommand
    from telegram.ext import Application, CommandHandler, ContextTypes
    print("   ✅ telegram imports successful")
    
    print("2. Testing bot token...")
    TOKEN = "7563475603:AAH-bhTQky3DLzTAdA-V3MzzbU2p9zRx6eM"
    print(f"   ✅ Token available: {TOKEN[:20]}...")
    
    print("3. Creating minimal bot...")
    
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("🤖 Minimal bot is working!")
    
    async def test_main():
        print("   📱 Initializing bot application...")
        application = Application.builder().token(TOKEN).build()
        
        print("   🔧 Adding command handler...")
        application.add_handler(CommandHandler("start", start_command))
        
        print("   🚀 Starting bot polling...")
        print("   ✅ Bot is running! Send /start in Telegram to test.")
        print("   Press Ctrl+C to stop.")
        
        await application.run_polling()
    
    if __name__ == "__main__":
        asyncio.run(test_main())
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
