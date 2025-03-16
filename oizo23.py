# from keep_alive import keep_alive  # Uncomment if keep_alive module is available
import os
import asyncio
import logging
import praw  # Reddit API interaction
import schedule
from dotenv import load_dotenv  # Load environment variables
import nest_asyncio
from gtts import gTTS

nest_asyncio.apply()
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr  # Speech to text conversion using SpeechRecognition
from googletrans import Translator, LANGUAGES  # Text translation
from io import BytesIO
import requests  # For making HTTP requests
import openai  # For OpenAI API

# Logging settings
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Get tokens from .env file
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not TOKEN:
    raise ValueError("❌ Telegram token is not set. Please check the .env file.")

# Reddit settings
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD,
                     user_agent="telegram_reddit_bot")


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This bot is ready to serve.")


# Post to Reddit
def post_to_reddit(subreddit, title, content):
    if not subreddit or not title or not content:
        return "❌ Subreddit, title, and content must not be empty!"
    try:
        sub = reddit.subreddit(subreddit)
        submission = sub.submit(title, selftext=content)
        return f"✅ Post successfully submitted: {submission.url}"
    except Exception as e:
        return f"❌ Error submitting post: {str(e)}"


async def reddit_post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text(
            "❌ Incorrect format! Example: /post subreddit title content")
        return
    subreddit, title, content = args[0], args[1], " ".join(args[2:])
    response = post_to_reddit(subreddit, title, content)
    await update.message.reply_text(response)


# Convert voice to text using SpeechRecognition
async def voice_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.voice:
        await update.message.reply_text("❌ Please send a voice message!")
        return
    file = await update.message.voice.get_file()
    voice_data = BytesIO()
    await file.download(out=voice_data)
    voice_data.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(voice_data) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='en')
        await update.message.reply_text(f"🎤 Converted text: {text}")
    except sr.UnknownValueError:
        await update.message.reply_text("❌ Could not recognize the audio!")
    except sr.RequestError as e:
        await update.message.reply_text(f"❌ Could not request results from Google Speech Recognition service; {e}")


# Convert text to voice
async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Incorrect format! Example: /text_to_voice en text")
        return
    lang, text = args[0], " ".join(args[1:])
    try:
        tts = gTTS(text, lang=lang)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        await update.message.reply_voice(voice=audio_file)
    except Exception as e:
        await update.message.reply_text(f"❌ Error converting text to voice: {str(e)}")


# Chat with OpenAI using GPT-3.5-turbo
async def deepseek_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    if not user_input:
        await update.message.reply_text("❌ Please send a question!")
        return
    if not DEEPSEEK_API_KEY:
        await update.message.reply_text("❌ OpenAI API key is missing!")
        return

    openai.api_key = DEEPSEEK_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": user_input},
            ]
        )
        answer = response.choices[0].message['content']
        await update.message.reply_text(answer)
    except Exception as e:
        logging.error(f"❌ Error calling OpenAI API: {str(e)}")
        await update.message.reply_text(f"❌ Error calling OpenAI API: {str(e)}")


# Translate text
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("❌ Incorrect format! Example: /translate fa en text")
        return
    src_lang, dest_lang, text = args[0], args[1], " ".join(args[2:])
    translator = Translator()
    try:
        translated = await asyncio.to_thread(translator.translate, text, src=src_lang, dest=dest_lang)
        await update.message.reply_text(f"🔄 Translation: {translated.text}")
    except Exception as e:
        logging.error(f"❌ Error in translation: {str(e)}")
        await update.message.reply_text(f"❌ Error in translation: {str(e)}")


# لیست کدهای زبان
language_codes = "\n".join([f"{code} - {name}" for code, name in LANGUAGES.items()])

# پنل دستور دادن
async def command_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = [
        "/start - Start the bot.\nExample: /start",
        "/post - Post to Reddit.\nExample: /post subreddit title content",
        "/voice - Convert voice to text.\nExample: /voice",
        "/deepseek - Chat with DeepSeek.\nExample: /deepseek your_question",
        "/text_to_voice - Convert text to voice.\nExample: /text_to_voice en text",
        "/translate - Translate text.\nExample: /translate fa en text",
        "/languages - Show language codes",
        "/commands - Show commands.\nExample: /commands"
    ]
    await update.message.reply_text("\n".join(commands))

# نمایش کدهای زبان
async def show_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Language codes:\n{language_codes}")

# راه‌اندازی ربات
async def main():
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("post", reddit_post_command))
    application.add_handler(CommandHandler("voice", voice_to_text))
    application.add_handler(CommandHandler("deepseek", deepseek_response))
    application.add_handler(CommandHandler("text_to_voice", text_to_voice))
    application.add_handler(CommandHandler("translate", translate_text))
    application.add_handler(CommandHandler("languages", show_languages))
    application.add_handler(CommandHandler("commands", command_panel))

    # تنظیم منوی دستورات
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("post", "Post to Reddit"),
        BotCommand("voice", "Convert voice to text"),
        BotCommand("deepseek", "Chat with DeepSeek"),
        BotCommand("text_to_voice", "Convert text to voice"),
        BotCommand("translate", "Translate text"),
        BotCommand("languages", "Show language codes"),
        BotCommand("commands", "Show commands")
    ]
    await application.bot.set_my_commands(commands)

    # اجرای ربات
    logging.info("✅ Bot is running...")
    await application.run_polling()

# اجرای برنامه
if __name__ == "__main__":
    loop = asyncio.new_event_loop()  # ایجاد یک حلقه رویداد جدید
    asyncio.set_event_loop(loop)  # تنظیم حلقه رویداد به عنوان حلقه پیش‌فرض
    try:
        loop.run_until_complete(main())  # اجرای تابع main در حلقه رویداد
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()  # بستن حلقه رویداد پس از اتمام کار
