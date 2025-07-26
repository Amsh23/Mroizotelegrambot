#!/usr/bin/env python3
"""
Quick test script for the enhanced Telegram bot
"""

import sys
import asyncio
import logging

# Test imports
def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import oizo
        print("✅ Main bot module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import bot: {e}")
        return False
    
    # Test optional dependencies
    optional_deps = {
        'praw': 'Reddit integration',
        'speech_recognition': 'Voice recognition',
        'gtts': 'Text-to-speech',
        'googletrans': 'Translation',
        'argostranslate': 'Offline translation'
    }
    
    for module, description in optional_deps.items():
        try:
            __import__(module)
            print(f"✅ {description} available")
        except ImportError:
            print(f"⚠️ {description} not available (optional)")
    
    return True

def test_ffmpeg():
    """Test FFmpeg availability"""
    print("\n🎬 Testing FFmpeg...")
    import subprocess
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed and working")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found. Install from https://ffmpeg.org/")
        return False

def test_llama_connection():
    """Test Llama API connection"""
    print("\n🦙 Testing Llama API connection...")
    import aiohttp
    
    async def check_llama():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://127.0.0.1:11500/api/tags", 
                                     timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        print("✅ Llama API is running and accessible")
                        return True
                    else:
                        print(f"⚠️ Llama API returned status {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Llama API not accessible: {e}")
            print("   Start with: ollama serve")
            return False
    
    return asyncio.run(check_llama())

def main():
    """Run all tests"""
    print("🤖 Enhanced Telegram Bot - System Check")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Critical import failures detected!")
        sys.exit(1)
    
    # Test FFmpeg
    ffmpeg_ok = test_ffmpeg()
    
    # Test Llama
    llama_ok = test_llama_connection()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print("✅ Core bot functionality: READY")
    print(f"{'✅' if ffmpeg_ok else '❌'} Media processing: {'READY' if ffmpeg_ok else 'NEEDS FFMPEG'}")
    print(f"{'✅' if llama_ok else '⚠️'} Llama AI: {'READY' if llama_ok else 'START OLLAMA'}")
    
    if ffmpeg_ok and llama_ok:
        print("\n🚀 All systems ready! Run: python oizo.py")
    else:
        print("\n⚠️ Some features need setup. See messages above.")

if __name__ == "__main__":
    main()
