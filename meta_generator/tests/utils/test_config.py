#!/usr/bin/env python3
"""Tests for the configuration utilities."""
import os
import tempfile
import pytest
from omegaconf.dictconfig import DictConfig
from src.utils.config import read_config



def test_read_config_with_custom_path():
    """Test reading config with a custom path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as temp:
        # Write a test config
        temp.write("""
root: "test_root"
api:
  type: "test"
  model: "${root}/test-model"
test_var: "test_value"
        """)
        temp.flush()
        
        # Read the config
        config = read_config(temp.name)
        
        # Check the config was loaded correctly
        assert isinstance(config, DictConfig), f"Expected config to be an OmegaConf object, got {type(config)}"
        assert config.api.type == "test", "Expected api.type to be 'test'"
        assert config.api.model == "test_root/test-model", f"Expected api.model to be 'test_root/test-model', got {config.api.model}"
        assert config.test_var == "test_value"
        
