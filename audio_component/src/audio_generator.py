"""
Audio generator module for the Audio Companion Component.

This module provides functions for converting text to speech using
Google Text-to-Speech (gTTS) and handles errors gracefully.
"""
import io
import os
from typing import Dict
from gtts import gTTS
from gtts.tts import gTTSError
from retry import retry

# Global retry configuration
MAX_RETRIES = 3
# Use a very small delay during tests to speed up test execution
RETRY_DELAY = 0.01 if os.environ.get('PYTEST_CURRENT_TEST') else 10  # seconds
RETRY_BACKOFF = 2  # exponential backoff multiplier

def _validate_tts_params(sentence: str, kwargs: Dict) -> Dict:
    """Validate input parameters for TTS and prepare gTTS parameters."""
    if not sentence or not sentence.strip():
        raise ValueError("Sentence cannot be empty")
    
    if 'language' not in kwargs:
        raise ValueError("Language must be provided")
    
    # Prepare gTTS parameters - map 'language' to 'lang'
    gtts_params = {**kwargs, 'text': sentence}
    gtts_params['lang'] = gtts_params.pop('language')
    
    return gtts_params

@retry(exceptions=gTTSError, tries=MAX_RETRIES, delay=RETRY_DELAY, backoff=RETRY_BACKOFF, logger=None)
def generate_audio(sentence: str, **kwargs) -> bytes:
    """
    Convert the given sentence to an MP3 file using gTTS with retry capability.
    
    Args:
        sentence: The text to convert to speech.
        **kwargs: Additional keyword arguments for gTTS, including 'language'.
    
    Returns:
        Binary data representing the MP3 file.
    
    Raises:
        ValueError: If the sentence is empty or if required arguments are missing.
        RuntimeError: If there's an error during audio generation after MAX_RETRIES attempts.
        gTTSError: If there's a gTTS-specific error that persists after retries.
    """
    # Validate and prepare parameters
    gtts_params = _validate_tts_params(sentence, kwargs)
    
    try:
        # Create an in-memory file-like object to store the audio data
        mp3_fp = io.BytesIO()
        
        # Generate the audio using gTTS
        tts = gTTS(**gtts_params)
        tts.write_to_fp(mp3_fp)
        
        # Get the audio data
        mp3_fp.seek(0)
        return mp3_fp.read()
        
    except gTTSError:
        # This will be caught by the retry decorator
        raise
    
    except Exception as e:
        # Handle any other unexpected errors (not retried)
        raise RuntimeError(f"Unexpected error during audio generation: {str(e)}") from e