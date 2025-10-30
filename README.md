# Newsletter to Micro Podcast

Automatically converts Substack newsletters into audio podcasts and publishes them to Telegram channels.

## Overview

This automation pipeline:
1. 📰 Fetches the latest newsletter from a Substack publication
2. 🧹 Cleans and extracts text content from HTML
3. 🎙️ Transforms the text into a conversational podcast script using GPT-4
4. 🔊 Converts the script to audio using AI text-to-speech
5. 📱 Posts the audio podcast with newsletter link to a Telegram channel

Perfect for creating daily audio summaries of newsletters for your community!

## Features

- **Fully automated pipeline** - Run once to process latest newsletter
- **AI-powered script generation** - GPT-4 creates engaging podcast-style content
- **High-quality audio** - Uses Replicate's Speech-02-turbo model
- **Telegram integration** - Automatically posts to your channel
- **Memory-efficient** - Works entirely in-memory (ideal for GitHub Actions)
- **Configurable** - Easy to adapt for different newsletters and channels

## Prerequisites

### API Keys Required
1. **OpenAI API Key** - For GPT-4 newsletter transformation
2. **Replicate API Token** - For text-to-speech conversion
3. **Telegram Bot Token** - For posting to Telegram channels

### Telegram Setup
1. Create a Telegram bot via [@BotFather](https://t.me/BotFather)
2. Add your bot to your target channel as an admin
3. Give the bot "Post messages" permission
4. Get your channel ID (numeric format like `-1001234567890`)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd newsletter-to-micro-podcast
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export REPLICATE_API_TOKEN="your-replicate-token"
export TELEGRAM_API_BOT="your-telegram-bot-token"
```

## Configuration

Edit `main.py` to configure your newsletter and channel:

```python
# Newsletter URL (Substack publication)
NEWSLETTER_URL = "https://giadafromgamma.substack.com"

# Telegram channel ID
CHANNEL_ID = "-1003291063219"
```

## Usage

Simply run the pipeline:
```bash
python main.py
```

The script will automatically process the latest newsletter and post it to your configured Telegram channel.

## Project Structure

```
newsletter-to-micro-podcast/
├── main.py                    # Main pipeline orchestrator
├── requirements.txt           # Python dependencies
├── substack/
│   ├── substack_pull_data.py  # Fetch newsletter content
│   └── substack_clean_up.py   # HTML to text conversion
├── ai/
│   ├── newsletter_to_podcast_transcript.py  # GPT-4 script generation
│   └── transcript_tts.py      # Text-to-speech conversion
└── telegram/
    └── telegram_bot.py        # Telegram posting functionality
```

## How It Works

### Step 1: Newsletter Fetching
- Uses `substack-api` to get the latest newsletter post
- Returns both HTML content and the specific post URL

### Step 2: Content Cleaning
- Parses HTML with BeautifulSoup
- Removes navigation, ads, and formatting
- Extracts clean, readable text content

### Step 3: Podcast Script Generation
- Sends cleaned text to GPT-4 with specialized prompt
- Transforms newsletter into conversational podcast format
- Optimized for text-to-speech conversion

### Step 4: Audio Generation
- Uses Replicate's Speech-02-turbo model
- Configured for podcast-quality audio (mono, 32kHz)
- Male voice optimized for newsletter content

### Step 5: Telegram Publishing
- Posts audio file with embedded caption
- Includes episode title, description, and newsletter link
- Automatically cleans up temporary files

## GitHub Actions Integration

This project is designed to work seamlessly with GitHub Actions for automated daily publishing:

- **Memory-efficient**: No intermediate files created
- **Stateless**: Each run is independent
- **Error handling**: Comprehensive logging and error reporting
- **Cleanup**: Automatic temporary file removal

Example workflow runs:
- Daily at 8 AM (after newsletter publication)
- On-demand via workflow dispatch
- Triggered by newsletter publication webhooks

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `REPLICATE_API_TOKEN` | Replicate API token for TTS | Yes |
| `TELEGRAM_API_BOT` | Telegram bot token | Yes |

## Dependencies

- `openai==2.6.1` - GPT-4 integration
- `replicate==1.0.7` - Text-to-speech conversion
- `beautifulsoup4==4.14.2` - HTML parsing
- `requests==2.32.5` - HTTP requests
- `substack-api==1.1.1` - Newsletter fetching

## Troubleshooting

### Common Issues

**Telegram "Chat not found" error:**
- Ensure bot is added to the channel as admin
- Verify channel ID format (should start with `-100`)
- Check bot has "Post messages" permission

**OpenAI API errors:**
- Verify API key is valid and has credits
- Check if GPT-4 access is enabled on your account

**Audio generation fails:**
- Ensure Replicate API token is valid
- Check if text content is within size limits

**Newsletter not found:**
- Verify Substack URL is accessible
- Check if newsletter has published posts

## License

MIT License - Feel free to use and modify for your projects!