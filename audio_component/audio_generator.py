"""
Audio generator module for the Audio Companion Component.

This module provides functions for converting text to speech using
Google Text-to-Speech (gTTS) and handles errors gracefully.
"""
import io
from typing import Dict, Optional, Any
from gtts import gTTS
from gtts.tts import gTTSError


def generate_audio(sentence: str, **kwargs) -> bytes:
    """
    Converts the given sentence to an MP3 file using gTTS.
    
    Args:
        sentence: The text to convert to speech.
        **kwargs: Additional keyword arguments for gTTS. 
            Should include 'language' which will be mapped to 'lang' for gTTS.
            See gTTS documentation for all available options.
    
    Returns:
        Binary data representing the MP3 file.
    
    Raises:
        ValueError: If the sentence is empty or if required arguments are missing.
        RuntimeError: If there's an error during audio generation.
    """
    # Validate input
    if not sentence or not sentence.strip():
        raise ValueError("Sentence cannot be empty")
    
    # Ensure language is provided
    if 'language' not in kwargs:
        raise ValueError("Language must be provided")
    
    # Prepare gTTS parameters - map 'language' to 'lang'
    gtts_params = {
        'text': sentence,
        **kwargs
    }
    gtts_params['lang'] = gtts_params.pop('language')
    
    try:
        # Create an in-memory file-like object to store the audio data
        mp3_fp = io.BytesIO()
        
        # Generate the audio using gTTS
        tts = gTTS(**gtts_params)
        tts.write_to_fp(mp3_fp)
        
        # Get the audio data
        mp3_fp.seek(0)
        audio_data = mp3_fp.read()
        
        return audio_data
    
    except gTTSError as e:
        # Handle gTTS-specific errors
        error_message = f"Error generating audio with gTTS: {str(e)}"
        raise RuntimeError(error_message) from e
    
    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"Unexpected error during audio generation: {str(e)}"
        raise RuntimeError(error_message) from e