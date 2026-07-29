from unittest.mock import patch

from main import process_item


@patch("main.io_utils.save_audio_file")
@patch("main.generate_audio", return_value=b"audio")
def test_process_item_uses_configured_filename_prefix(generate_audio, save_audio_file):
    save_audio_file.return_value = {
        "audio_absolute_path": "/tmp/english_custom_audio_7.mp3",
        "audio_relative_path": "english_custom_audio_7.mp3",
    }
    item = {"example": "test phrase"}

    result = process_item(item, 7, "/tmp", "en", "english_custom_")

    generate_audio.assert_called_once_with("test phrase", language="en")
    save_audio_file.assert_called_once_with(
        "/tmp", "english_custom_audio_7.mp3", b"audio"
    )
    assert result["audio_relative_path"] == "english_custom_audio_7.mp3"


@patch("main.io_utils.save_audio_file")
@patch("main.generate_audio", return_value=b"audio")
def test_process_item_defaults_to_no_prefix(generate_audio, save_audio_file):
    save_audio_file.return_value = {
        "audio_absolute_path": "/tmp/audio_7.mp3",
        "audio_relative_path": "audio_7.mp3",
    }

    process_item({"example": "test phrase"}, 7, "/tmp", "en")

    save_audio_file.assert_called_once_with("/tmp", "audio_7.mp3", b"audio")
