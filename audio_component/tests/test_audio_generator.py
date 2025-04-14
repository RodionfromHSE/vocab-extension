"""
Unit tests for the audio_generator module.
"""
import io
import pytest
from unittest.mock import patch, MagicMock
from audio_generator import generate_audio
from gtts.tts import gTTSError


class TestGenerateAudio:
    """Tests for the generate_audio function."""
    
    @patch('audio_generator.gTTS')
    def test_successful_audio_generation(self, mock_gtts):
        """Test successful generation of audio from text."""
        # Set up the mock to return a known binary response
        test_audio_data = b"dummy audio data"
        mock_tts_instance = MagicMock()
        
        def mock_write_to_fp(fp):
            fp.write(test_audio_data)
        
        mock_tts_instance.write_to_fp.side_effect = mock_write_to_fp
        mock_gtts.return_value = mock_tts_instance
        
        # Call the function with a test sentence
        result = generate_audio("This is a test sentence.", language="en")
        
        # Verify the result
        assert result == test_audio_data
        
        # Verify that gTTS was called with the correct parameters
        mock_gtts.assert_called_once_with(text="This is a test sentence.", lang="en")
    
    def test_empty_sentence(self):
        """Test handling of an empty sentence."""
        with pytest.raises(ValueError, match="Sentence cannot be empty"):
            generate_audio("", language="en")
        
        with pytest.raises(ValueError, match="Sentence cannot be empty"):
            generate_audio("   ", language="en")
    
    def test_missing_language(self):
        """Test handling of missing language parameter."""
        with pytest.raises(ValueError, match="Language must be provided"):
            generate_audio("This is a test.")
    
    @patch('audio_generator.gTTS')
    def test_gtts_error(self, mock_gtts):
        """Test handling of gTTS errors."""
        # Set up the mock to raise a gTTSError
        mock_gtts.side_effect = gTTSError("Test gTTS error")
        
        # Call the function and expect a RuntimeError
        with pytest.raises(RuntimeError, match="Error generating audio with gTTS"):
            generate_audio("This is a test sentence.", language="en")
    
    @patch('audio_generator.gTTS')
    def test_unexpected_error(self, mock_gtts):
        """Test handling of unexpected errors."""
        # Set up the mock to raise an unexpected exception
        mock_gtts.side_effect = Exception("Unexpected error")
        
        # Call the function and expect a RuntimeError
        with pytest.raises(RuntimeError, match="Unexpected error during audio generation"):
            generate_audio("This is a test sentence.", language="en")
    
    @patch('audio_generator.gTTS')
    def test_additional_kwargs(self, mock_gtts):
        """Test passing additional keyword arguments to gTTS."""
        # Set up the mock
        mock_tts_instance = MagicMock()
        mock_gtts.return_value = mock_tts_instance
        
        # Call the function with additional kwargs
        generate_audio(
            "This is a test sentence.",
            language="en",
            slow=True,
            tld="com"
        )
        
        # Verify that gTTS was called with all the provided parameters
        mock_gtts.assert_called_once_with(
            text="This is a test sentence.",
            lang="en",
            slow=True,
            tld="com"
        )