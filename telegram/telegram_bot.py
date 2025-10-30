#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from pathlib import Path
from typing import Optional


class TelegramBot:
    def __init__(self, bot_token: Optional[str] = None):
        """
        Initialize Telegram bot with token from environment or parameter
        
        Args:
            bot_token: Optional bot token, if not provided will use TELEGRAM_API_BOT env var
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_API_BOT')
        if not self.bot_token:
            raise ValueError("Bot token not found. Set TELEGRAM_API_BOT environment variable or pass bot_token parameter")
        
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = "HTML") -> dict:
        """
        Send a text message to a channel or chat
        
        Args:
            chat_id: Channel ID or username (e.g., '@channelname' or '-1001234567890')
            text: Message text to send
            parse_mode: Text formatting mode (HTML, Markdown, or None)
        
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        response = requests.post(url, data=data)
        return response.json()
    
    def send_audio(self, chat_id: str, audio_path: str, caption: str = "", title: str = "Podcast Episode") -> dict:
        """
        Send an audio file to a channel or chat
        
        Args:
            chat_id: Channel ID or username
            audio_path: Path to the audio file
            caption: Optional caption for the audio
            title: Title for the audio file
        
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/sendAudio"
        
        audio_file = Path(audio_path)
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        with open(audio_file, 'rb') as audio:
            files = {'audio': audio}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'title': title,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, files=files, data=data)
            return response.json()
    
    def send_podcast_episode(self, chat_id: str, audio_path: str, episode_title: str = "Daily Newsletter Podcast", newsletter_url: str = None) -> dict:
        """
        Send a complete podcast episode with formatted message
        
        Args:
            chat_id: Channel ID or username
            audio_path: Path to the podcast audio file
            episode_title: Title for the episode
            newsletter_url: URL to the specific newsletter post
        
        Returns:
            API response as dictionary
        """
        # Create a nice caption for the podcast
        caption = f"""🎧 <b>{episode_title}</b>

📰 Your daily newsletter transformed into an audio experience!

🔔 Don't forget to check our next newsletter - we publish Monday, Wednesday, and Friday at 7AM."""
        
        # Add newsletter link if provided
        if newsletter_url:
            caption += f"\n\n📖 <b>Read the full newsletter:</b>\n{newsletter_url}"
        
        caption += "\n\n#Podcast #Newsletter #DailyUpdate"
        
        return self.send_audio(chat_id, audio_path, caption, episode_title)
    
    def get_chat_info(self, chat_id: str) -> dict:
        """
        Get information about a chat/channel
        
        Args:
            chat_id: Channel ID or username
        
        Returns:
            API response with chat information
        """
        url = f"{self.base_url}/getChat"
        data = {"chat_id": chat_id}
        
        response = requests.post(url, data=data)
        return response.json()


