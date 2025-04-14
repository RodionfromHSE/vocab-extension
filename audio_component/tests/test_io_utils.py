"""
Unit tests for the io_utils module.
"""
import os
import json
import tempfile
import pytest
from pathlib import Path
from io_utils import (
    read_input_json,
    create_target_directory,
    save_audio_file,
    write_output_json
)

class TestReadInputJson:
    """Tests for the read_input_json function."""
    
    def test_valid_json_with_sentences(self):
        """Test reading a valid JSON file with sentences."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump([
                {"sentence": "Hello, world!"},
                {"sentence": "This is a test."}
            ], f)
            temp_file = f.name
        
        try:
            result = read_input_json(temp_file)
            assert len(result) == 2
            assert result[0]["sentence"] == "Hello, world!"
            assert result[1]["sentence"] == "This is a test."
        finally:
            os.unlink(temp_file)
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_input_json("non_existent_file.json")
    
    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("This is not valid JSON")
            temp_file = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                read_input_json(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_missing_sentence_field(self):
        """Test handling of JSON objects missing the 'sentence' field."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump([
                {"text": "Hello, world!"},  # Missing 'sentence' field
                {"sentence": "This is a test."}
            ], f)
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError, match="missing the 'sentence' field"):
                read_input_json(temp_file)
        finally:
            os.unlink(temp_file)

class TestCreateTargetDirectory:
    """Tests for the create_target_directory function."""
    
    def test_directory_creation(self):
        """Test that the target directory is created successfully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = temp_dir
            media_subdir = "test_media"
            
            target_dir = create_target_directory(save_dir, media_subdir)
            
            assert os.path.exists(target_dir)
            assert os.path.isdir(target_dir)
            assert os.path.basename(target_dir) == media_subdir
    
    def test_existing_directory(self):
        """Test handling of an existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = temp_dir
            media_subdir = "test_media"
            
            # Create the directory first
            os.makedirs(os.path.join(save_dir, media_subdir), exist_ok=True)
            
            # Should not raise an error
            target_dir = create_target_directory(save_dir, media_subdir)
            
            assert os.path.exists(target_dir)
            assert os.path.isdir(target_dir)

class TestSaveAudioFile:
    """Tests for the save_audio_file function."""
    
    def test_save_audio_file(self):
        """Test saving an audio file and getting paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = "test_audio"
            audio_data = b"dummy audio data"
            
            result = save_audio_file(temp_dir, file_name, audio_data)
            
            # Check that the file was saved
            expected_path = os.path.join(temp_dir, file_name + ".mp3")
            assert os.path.exists(expected_path)
            
            # Check the returned paths
            assert result["audio_absolute_path"] == expected_path
            assert result["audio_relative_path"] == os.path.join(
                os.path.basename(temp_dir), file_name + ".mp3"
            )
            
            # Check the file contents
            with open(expected_path, "rb") as f:
                saved_data = f.read()
                assert saved_data == audio_data
    
    def test_file_name_with_extension(self):
        """Test saving a file with an extension already included."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = "test_audio.mp3"
            audio_data = b"dummy audio data"
            
            result = save_audio_file(temp_dir, file_name, audio_data)
            
            # Check that the file was saved without adding another extension
            expected_path = os.path.join(temp_dir, file_name)
            assert os.path.exists(expected_path)
            assert result["audio_absolute_path"] == expected_path

class TestWriteOutputJson:
    """Tests for the write_output_json function."""
    
    def test_write_output_json(self):
        """Test writing data to an output JSON file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "output.json")
            data = [
                {"sentence": "Hello", "audio_absolute_path": "/path/to/hello.mp3"},
                {"sentence": "World", "audio_absolute_path": "/path/to/world.mp3"}
            ]
            
            write_output_json(data, output_file)
            
            # Check that the file was created
            assert os.path.exists(output_file)
            
            # Check the file contents
            with open(output_file, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
                assert saved_data == data
    
    def test_write_output_json_nested_directory(self):
        """Test writing to a file in a nested directory that doesn't exist yet."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = os.path.join(temp_dir, "nested", "dir")
            output_file = os.path.join(nested_dir, "output.json")
            data = [{"sentence": "Test"}]
            
            write_output_json(data, output_file)
            
            # Check that the directories and file were created
            assert os.path.exists(nested_dir)
            assert os.path.exists(output_file)