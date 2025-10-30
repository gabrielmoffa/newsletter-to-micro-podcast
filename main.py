#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from substack.substack_pull_data import get_latest_newsletter_html
from substack.substack_clean_up import clean_newsletter_html
from ai.newsletter_to_podcast_transcript import transform_newsletter_to_podcast
from ai.transcript_tts import text_to_speech
from telegram.telegram_bot import TelegramBot


def run_newsletter_to_podcast_pipeline(newsletter_url: str = "https://giadafromgamma.substack.com", 
                                     channel_id: str = "-1003291063219"):
    """
    Complete pipeline: Newsletter -> Clean Text -> Podcast Script -> Audio -> Telegram
    
    Args:
        newsletter_url: Substack newsletter URL
        channel_id: Telegram channel ID (e.g., '@channelname' or '-1001234567890')
    """
    
    print("🚀 Starting Newsletter to Podcast Pipeline")
    print("=" * 50)
    
    try:
        # Step 1: Pull latest newsletter data
        print("📰 Step 1: Fetching latest newsletter...")
        html_content, latest_post_url = get_latest_newsletter_html(newsletter_url)
        print(f"✅ Newsletter fetched ({len(html_content)} characters)")
        print(f"📄 Latest post URL: {latest_post_url}")
        
        # Step 2: Clean up HTML to text
        print("\n🧹 Step 2: Cleaning newsletter HTML...")
        clean_text = clean_newsletter_html(html_content)
        print(f"✅ Newsletter cleaned ({len(clean_text)} characters)")
        
        # Step 3: Transform to podcast script
        print("\n🎙️ Step 3: Generating podcast transcript...")
        podcast_script = transform_newsletter_to_podcast(clean_text)
        print(f"✅ Podcast script generated ({len(podcast_script)} characters)")
        
        # Step 4: Convert to audio
        print("\n🔊 Step 4: Converting to audio...")
        audio_path = text_to_speech(podcast_script)
        print(f"✅ Audio generated: {audio_path}")
        
        # Step 5: Send to Telegram
        print(f"\n📱 Step 5: Sending to Telegram channel {channel_id}...")
        bot = TelegramBot()
        
        # Create episode title with date
        today = datetime.now().strftime("%B %d, %Y")
        episode_title = f"Daily Newsletter Podcast - {today}"
        
        # Send the audio file with newsletter link in caption
        response = bot.send_podcast_episode(channel_id, str(audio_path), episode_title, latest_post_url)
        
        if response.get('ok'):
            print("✅ Successfully sent podcast with newsletter link to Telegram!")
            print(f"Message ID: {response['result']['message_id']}")
        else:
            print(f"❌ Telegram error: {response.get('description', 'Unknown error')}")
        
        print("\n🎉 Pipeline completed successfully!")
        print("=" * 50)
        
        # Summary
        print("\n📋 Process summary:")
        print(f"   📰 Newsletter content: {len(html_content)} characters")
        print(f"   📝 Cleaned text: {len(clean_text)} characters")
        print(f"   🎭 Podcast script: {len(podcast_script)} characters")
        print(f"   🎵 Audio file: {audio_path}")
        print(f"   🔗 Newsletter URL: {latest_post_url}")
        
        # Clean up the temporary audio file after successful upload
        try:
            os.remove(audio_path)
            print(f"   🗑️  Temporary audio file cleaned up")
        except Exception as cleanup_error:
            print(f"   ⚠️  Could not clean up audio file: {cleanup_error}")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        raise



if __name__ == "__main__":
    # Configuration
    NEWSLETTER_URL = "https://giadafromgamma.substack.com"
    
    # Telegram channel ID
    CHANNEL_ID = "-1003291063219"
    
    print("Newsletter to Podcast Automation")
    print("================================")
    
    run_newsletter_to_podcast_pipeline(NEWSLETTER_URL, CHANNEL_ID)