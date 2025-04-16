#!/usr/bin/env python3
"""Configuration utilities for the meta generator."""
import os
from typing import Dict, Any
from omegaconf import OmegaConf

def read_config(config_path: str) -> OmegaConf:
    """
    Load configuration with OmegaConf with resolution.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        OmegaConf: Configuration object with resolved values
    """
    config_path = os.path.abspath(config_path)
    cfg = OmegaConf.load(config_path)
    
    # Resolve all variables in the config
    cfg = OmegaConf.create(OmegaConf.to_yaml(cfg, resolve=True))
    return cfg

