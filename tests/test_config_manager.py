#!/usr/bin/env python3
"""
Tests for Configuration Manager
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from config_manager import ConfigManager, TextSpeed, Difficulty, ColorScheme


@pytest.fixture
def temp_config_dir():
    """Create temporary config directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_config_creation(temp_config_dir):
    """Test configuration manager creation"""
    config = ConfigManager(config_dir=temp_config_dir)
    assert config.config_dir == temp_config_dir
    assert config.display.text_speed == TextSpeed.NORMAL
    assert config.gameplay.difficulty == Difficulty.NORMAL


def test_config_save_load(temp_config_dir):
    """Test saving and loading configuration"""
    config1 = ConfigManager(config_dir=temp_config_dir)
    config1.gameplay.difficulty = Difficulty.HARD
    config1.display.text_speed = TextSpeed.FAST
    config1.save()

    # Load in new instance
    config2 = ConfigManager(config_dir=temp_config_dir)
    assert config2.gameplay.difficulty == Difficulty.HARD
    assert config2.display.text_speed == TextSpeed.FAST


def test_game_specific_config(temp_config_dir):
    """Test game-specific configuration"""
    config = ConfigManager(config_dir=temp_config_dir)

    game_settings = {'custom_setting': 'value'}
    config.save_game_config('test_game', game_settings)

    loaded = config.load_game_config('test_game')
    assert loaded['custom_setting'] == 'value'


def test_reset_to_defaults(temp_config_dir):
    """Test resetting to defaults"""
    config = ConfigManager(config_dir=temp_config_dir)
    config.gameplay.difficulty = Difficulty.EXTREME
    config.reset_to_defaults()

    assert config.gameplay.difficulty == Difficulty.NORMAL
    assert config.display.text_speed == TextSpeed.NORMAL
