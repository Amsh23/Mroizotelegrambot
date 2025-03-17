import os
import asyncio
import logging
import praw
from dotenv import load_dotenv
import nest_asyncio
from gtts import gTTS
from telegram import Update, BotCommand, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
import aiohttp
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from io import BytesIO
import requests

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

# Load environment variables from .env file
load_dotenv()

# Retrieve tokens and credentials from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Check if the Telegram token is set
if not TOKEN:
    raise ValueError("Telegram token is not set. Please check the .env file and ensure TELEGRAM_BOT_TOKEN is defined.")

# Check if Reddit credentials are set
if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]):
    raise ValueError("Reddit credentials are not set. Please check the .env file and ensure all Reddit credentials are defined.")

# Initialize Reddit instance
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD,
                     user_agent=os.getenv("REDDIT_USER_AGENT", "telegram_reddit_bot"))

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command. Sends a welcome message to the user.
    Args:
        update (Update): Incoming update from Telegram.
    """
    await update.message.reply_text("Hello! I'm your bot!")

# Function to post content to Reddit
def post_to_reddit(subreddit, title, content):
    """
    Post content to a specified subreddit.
    Args:
        subreddit (str): The subreddit to post to.
        title (str): The title of the post.
        content (str): The content of the post.
    Returns:
        str: The result of the post attempt.
    """
    if not subreddit or not title or not content:
        return "Subreddit, title, and content must not be empty!"
    try:
        sub = reddit.subreddit(subreddit)
        submission = sub.submit(title, selftext=content)
        return f"Post successfully submitted: {submission.url}"
    except praw.exceptions.APIException as e:
        return f"Reddit API error: {e.message}"
    except praw.exceptions.ClientException as e:
        return f"Client error: {e.message}"
    except praw.exceptions.PRAWException as e:
        return f"PRAW error: {e.message}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Command handler for /post
async def post_reddit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /post command. Posts content to Reddit.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
    await update.message.reply_text("Posting to Reddit...")

# Command handler for /voice
async def voice_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /voice command. Converts voice message to text.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
    if not update.message.voice:
        await update.message.reply_text("Please send a voice message!")
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
        await update.message.reply_text(f"Converted text: {text}")
    except sr.UnknownValueError:
        await update.message.reply_text("Could not recognize the audio!")
    except sr.RequestError as e:
        await update.message.reply_text(f"Could not request results from Google Speech Recognition service; {e}")

# Command handler for /text_to_voice
async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /text_to_voice command. Converts text to voice message.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Incorrect format! Example: /text_to_voice en text")
        return
    lang, text = args[0], " ".join(args[1:])
    try:
        tts = gTTS(text, lang=lang)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        await update.message.reply_voice(voice=audio_file)
    except Exception as e:
        await update.message.reply_text(f"Error converting text to voice: {str(e)}")

# Command handler for /deepseek
async def deepseek_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /deepseek command. Sends a question to DeepSeek API and returns the response.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
    user_input = " ".join(context.args)
    if not user_input:
        await update.message.reply_text("Please send a question!")
        return
    if not DEEPSEEK_API_KEY:
        await update.message.reply_text("DeepSeek API key is missing!")
        return
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "question": user_input
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.deepseek.com/v1/ask", headers=headers, json=data) as response:
                if response.status != 200:
                    await update.message.reply_text(f"Error calling DeepSeek API: {response.status}")
                    return
                result = await response.json()
                answer = result.get("answer", "No answer found!")
                await update.message.reply_text(answer)
    except Exception as e:
        logging.error(f"Error calling DeepSeek API: {str(e)}")
        await update.message.reply_text(f"Error calling DeepSeek API: {str(e)}")

# Command handler for /translate
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /translate command. Translates text from one language to another.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Incorrect format! Example: /translate fa en text")
        return
    src_lang, dest_lang, text = args[0], args[1], " ".join(args[2:])
    translator = Translator()
    try:
        translated = await asyncio.to_thread(translator.translate, text, src=src_lang, dest=dest_lang)
        await update.message.reply_text(f"Translation: {translated.text}")
    except Exception as e:
        logging.error(f"Error in translation: {str(e)}")
        await update.message.reply_text(f"Error in translation: {str(e)}")

# Command handler for /languages
async def show_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /languages command. Shows available language codes.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
    language_codes = "\n".join([f"{code} - {name}" for code, name in LANGUAGES.items()])
    await update.message.reply_text(f"Language codes:\n{language_codes}")

# Command handler for /commands
async def command_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /commands command. Shows available commands.
    Args:
        update (Update): Incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): Context for the command.
    """
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

# Main function to start the bot
async def main():
    """
    Main function to start the bot.
    """
    # Create the application instance with the bot token
    application = Application.builder().token(TOKEN).build()

    # Initialize the application
    await application.initialize()

    # Add command handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("post", post_reddit))
    application.add_handler(CommandHandler("voice", voice_to_text))
    application.add_handler(CommandHandler("deepseek", deepseek_response))
    application.add_handler(CommandHandler("text_to_voice", text_to_voice))
    application.add_handler(CommandHandler("translate", translate_text))
    application.add_handler(CommandHandler("languages", show_languages))
    application.add_handler(CommandHandler("commands", command_panel))

    # Define the bot commands for the Telegram interface
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

    # Set the bot commands
    await application.bot.set_my_commands(commands)

    # Log that the bot is running
    logging.info("Bot is running...")

    # Start the bot
    try:
        await application.run_polling()
    except RuntimeError as e:
        logging.error(f"RuntimeError: {e}")

# Call the main function to start the bot
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
