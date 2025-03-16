.
# Telegram Bot 🤖

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green)
![License](https://img.shields.io/badge/License-MIT-orange)

This is a **Telegram Bot** designed to provide various functionalities such as posting to Reddit, converting voice to text, translating text, and interacting with AI models like DeepSeek. The bot is built using Python and leverages popular libraries like `python-telegram-bot`, `praw`, `gTTS`, and `googletrans`.

---

## ✨ Features

The bot supports the following commands and functionalities:

### 1. **Post to Reddit**
   - Post content to a specified subreddit.
   - Command: `/post <subreddit> <title> <content>`
   - Example: `/post test_bot "My First Post" "This is a test post from the bot."`

### 2. **Voice to Text**
   - Convert voice messages to text using Google Speech Recognition.
   - Command: `/voice`
   - Example: Send a voice message, and the bot will reply with the transcribed text.

### 3. **Text to Voice**
   - Convert text to voice messages using Google Text-to-Speech (gTTS).
   - Command: `/text_to_voice <language_code> <text>`
   - Example: `/text_to_voice en "Hello, how are you?"`

### 4. **AI-Powered Chat (DeepSeek)**
   - Interact with the DeepSeek AI model to get answers to questions.
   - Command: `/deepseek <your_question>`
   - Example: `/deepseek What is the capital of France?`

### 5. **Text Translation**
   - Translate text between different languages using Google Translate.
   - Command: `/translate <source_language_code> <target_language_code> <text>`
   - Example: `/translate fa en "سلام"` (Translates "Hello" from Persian to English).

### 6. **Show Language Codes**
   - Display a list of supported language codes for translation and text-to-voice.
   - Command: `/languages`

### 7. **Command Panel**
   - Display all available commands and their usage.
   - Command: `/commands`

---

## 🚀 Setup Instructions

### 1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/telegram-bot.git
   cd telegram-bot
   ```

### 2. **Install Dependencies**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Configure Environment Variables**
   Create a `.env` file in the project root and add the following variables:
   ```plaintext
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

   - **TELEGRAM_BOT_TOKEN**: Obtain this from [BotFather](https://core.telegram.org/bots#botfather).
   - **DEEPSEEK_API_KEY**: Required if you want to use the AI-powered chat feature.

### 4. **Run the Bot**
   Start the bot by running:
   ```bash
   python oizo23.py
   ```

---

## 🛠️ Usage

Once the bot is running, you can interact with it in Telegram using the commands listed above. Here are some examples:

1. **Post to Reddit**:
   ```
   /post test_bot "My First Post" "This is a test post from the bot."
   ```

2. **Convert Voice to Text**:
   Send a voice message, and the bot will reply with the transcribed text.

3. **Translate Text**:
   ```
   /translate fa en "سلام"
   ```
   Output: `🔄 Translation: Hello`

4. **Ask DeepSeek AI**:
   ```
   /deepseek What is the capital of France?
   ```

5. **Show Commands**:
   ```
   /commands
   ```

---

## 🤝 Contributing

We welcome contributions! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and ensure tests pass.
4. Submit a pull request with a detailed description of your changes.

For more information, see our [Contributing Guidelines](CONTRIBUTING.md).

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Thanks to the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library for making Telegram bot development easier.
- Special thanks to [DeepSeek](https://deepseek.com) for providing the AI-powered chat functionality.

---
