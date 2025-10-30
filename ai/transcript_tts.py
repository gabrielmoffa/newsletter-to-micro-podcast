#!/usr/bin/env python3

import os
import replicate
from pathlib import Path

def text_to_speech(script_content: str, output_filename: str = "podcast_audio.wav"):
    """Convert podcast script to speech using Replicate Speech-02-turbo model.
    
    Args:
        script_content: The podcast script text to convert
        output_filename: Name of the output audio file
        
    Returns:
        Path to the generated audio file
    """
    
    text = script_content.strip()
    
    # Set up Replicate client
    api_token = os.getenv('REPLICATE_API_TOKEN')
    if not api_token:
        raise ValueError("REPLICATE_API_TOKEN not found in environment variables")
    
    # Configure TTS parameters
    input_params = {
        "text": text,
        "pitch": 0,
        "speed": 1,
        "volume": 1,
        "bitrate": 128000,
        "channel": "mono",
        "voice_id": "Deep_Voice_Man",
        "sample_rate": 32000,
        "language_boost": "English",
        "english_normalization": True
    }
    
    print("Starting text-to-speech conversion...")
    print(f"Text length: {len(text)} characters")
    
    # Run the model
    output = replicate.run(
        "minimax/speech-02-turbo",
        input=input_params
    )
    
    # Save the audio output
    output_path = Path(output_filename)
    
    if hasattr(output, 'read'):
        # If output is a file-like object, read it
        with open(output_path, 'wb') as f:
            f.write(output.read())
    elif isinstance(output, str):
        # If output is a URL, download it
        import requests
        response = requests.get(output)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        # If output is binary data, save directly
        with open(output_path, 'wb') as f:
            f.write(output)
    
    print(f"Audio saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    try:
        # Example usage with file input for testing
        try:
            with open('podcast_script.txt', 'r', encoding='utf-8') as f:
                script_content = f.read()
        except FileNotFoundError:
            print("podcast_script.txt not found. This function now works with script content directly.")
            exit(1)
        
        output_file = text_to_speech(script_content)
        print(f"Successfully converted podcast script to audio: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)