#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from openai import OpenAI


def generate_newsletter_summary(newsletter_content: str) -> str:
    """
    Generate a short written summary of the newsletter highlighting
    key events and news to tease readers into clicking the full link.

    Args:
        newsletter_content: Cleaned newsletter text content

    Returns:
        Short summary string with a few bullet points
    """

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    prompt = f"""From the following newsletter content, write a very short teaser summary to make people curious and want to read the full newsletter.

REQUIREMENTS:
- Write 3-5 short bullet points (use the bullet character "•")
- Each bullet should be ONE short sentence (max 15 words)
- Mix events and news highlights
- Make them intriguing and curiosity-inducing - tease, don't spoil
- Keep the TOTAL output under 300 characters
- No intro text, no outro, just the bullet points
- Write in English

NEWSLETTER CONTENT:
{newsletter_content}

Write the bullet points:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You write ultra-concise, curiosity-inducing teaser summaries for newsletters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")
