#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import openai
from openai import OpenAI


def transform_newsletter_to_podcast(newsletter_content: str) -> str:
    """
    Transform the cleaned newsletter text into a podcast script using GPT-4o
    
    Args:
        newsletter_content: Cleaned newsletter text content
    
    Returns:
        Generated podcast script text
    """
    
    # Get OpenAI API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create the prompt for podcast transformation
    prompt = f"""
Transform the following newsletter content into a conversational podcast transcript. Write it as if you're a radio host speaking directly to listeners.

CRITICAL FORMATTING REQUIREMENTS:
- Output ONLY the spoken text - NO stage directions, sound effects, or formatting
- NO "Host:", "[MUSIC]", "[TRANSITION]", or any other labels
- NO brackets, colons, or production notes
- This will be fed directly to a text-to-speech model, so it must be pure spoken content
- Write as continuous flowing speech that a TTS model can read naturally

CONTENT GUIDELINES:
- Write in a natural, conversational radio/podcast style
- Address the audience directly (use "you", "we", "let's")
- Don't mention every single event - select the most interesting ones
- Include the weather information in a natural way
- Highlight the special events and bigger announcements
- Include the main news stories
- Keep it engaging and flowing like spoken conversation
- Make it sound warm and friendly, like a local radio show
- Add natural transitions between topics
- Don't make it too long - aim for a 3-5 minute read
- The newsletter is shared on Monday, Wednesday, Friday, at 7AM, based on the day, tell the user to make sure to check our next newsletter.

NEWSLETTER CONTENT:
{newsletter_content}

Generate a clean podcast transcript with ONLY the spoken words - no formatting or stage directions:
"""
    
    try:
        # Make API call to GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an experienced radio host and podcast producer who specializes in transforming written content into engaging, conversational audio scripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        # Extract the generated script
        podcast_script = response.choices[0].message.content
        
        return podcast_script
        
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")


if __name__ == "__main__":
    try:
        # Example usage with file input for testing
        try:
            with open('newsletter_clean.txt', 'r', encoding='utf-8') as f:
                newsletter_content = f.read()
        except FileNotFoundError:
            print("newsletter_clean.txt not found. This function now works with text content directly.")
            exit(1)
        
        print("Transforming newsletter to podcast transcript...")
        script = transform_newsletter_to_podcast(newsletter_content)
        
        print(f"✅ Podcast transcript generated")
        print(f"📝 Transcript length: {len(script)} characters")
        print("\n" + "="*50)
        print("PODCAST TRANSCRIPT PREVIEW:")
        print("="*50)
        print(script[:500] + "..." if len(script) > 500 else script)
        
    except Exception as e:
        print(f"❌ Error: {e}")