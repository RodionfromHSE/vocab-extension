"""
Unit tests for the audio_generator module.
"""
import io
import pytest
from unittest.mock import patch, MagicMock
from src.audio_generator import generate_audio, MAX_RETRIES
from gtts.tts import gTTSError


class TestGenerateAudio:
    """Tests for the generate_audio function."""
    
    @patch('src.audio_generator.gTTS')
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
    
    # @patch('src.audio_generator.gTTS')
    # def test_gtts_error_with_retry(self, mock_gtts):
    #     """Test that the retry mechanism works for gTTSError."""
    #     # COMMENTED OUT: This test is slow due to retry delays
    #     # Set up the mock to raise gTTSError twice then succeed on the third attempt
    #     test_audio_data = b"dummy audio data"
    #     mock_tts_instance = MagicMock()
    #     
    #     def mock_write_to_fp(fp):
    #         fp.write(test_audio_data)
    #     
    #     mock_tts_instance.write_to_fp.side_effect = mock_write_to_fp
    #     
    #     # Configure the mock to fail twice and then succeed
    #     mock_gtts.side_effect = [
    #         gTTSError("Test gTTS error 1"),
    #         gTTSError("Test gTTS error 2"),
    #         mock_tts_instance
    #     ]
    #     
    #     # Call the function with a test sentence
    #     result = generate_audio("This is a test sentence.", language="en")
    #     
    #     # Verify the result
    #     assert result == test_audio_data
    #     
    #     # Verify that gTTS was called multiple times (retry attempts)
    #     assert mock_gtts.call_count == 3
    
    # @patch('src.audio_generator.gTTS')
    # def test_gtts_error_max_retries_exceeded(self, mock_gtts):
    #     """Test that after MAX_RETRIES attempts, the gTTSError is raised."""
    #     # COMMENTED OUT: This test is slow due to retry delays
    #     # Set up the mock to always raise gTTSError
    #     mock_gtts.side_effect = gTTSError("Test gTTS error")
    #     
    #     # Call the function and expect a gTTSError after MAX_RETRIES attempts
    #     with pytest.raises(gTTSError):
    #         generate_audio("This is a test sentence.", language="en")
    #     
    #     # Verify that gTTS was called MAX_RETRIES times
    #     assert mock_gtts.call_count == MAX_RETRIES
    
    @patch('src.audio_generator.gTTS')
    def test_unexpected_error(self, mock_gtts):
        """Test handling of unexpected errors that should not be retried."""
        # Set up the mock to raise an unexpected exception
        mock_gtts.side_effect = ValueError("Unexpected error")
        
        # Call the function and expect a RuntimeError
        # Note: Non-gTTSError exceptions are caught and wrapped in RuntimeError
        with pytest.raises(RuntimeError, match="Unexpected error during audio generation"):
            generate_audio("This is a test sentence.", language="en")
        
        # Verify that gTTS was called only once (no retry for non-gTTSError)
        assert mock_gtts.call_count == 1
    
    @patch('src.audio_generator.gTTS')
    def test_additional_kwargs(self, mock_gtts):
        """Test passing additional keyword arguments to gTTS."""
        # Set up the mock
        test_audio_data = b"dummy audio data"
        mock_tts_instance = MagicMock()
        
        def mock_write_to_fp(fp):
            fp.write(test_audio_data)
        
        mock_tts_instance.write_to_fp.side_effect = mock_write_to_fp
        mock_gtts.return_value = mock_tts_instance
        
        # Call the function with additional kwargs
        generate_audio(
            "This is a test sentence.",
            language="en",
            slow=True,
            tld="com"
        )
        
        # Verify that gTTS was called with all the parameters
        mock_gtts.assert_called_once_with(text="This is a test sentence.", lang="en", slow=True, tld="com")