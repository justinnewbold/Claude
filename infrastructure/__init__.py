"""
Vault 67 Game Development Framework
====================================
Core infrastructure for building text-based games.
"""

__version__ = "1.0.0"

# Import key components for easy access
from .base_game import TurnBasedGame, GameMetadata
from .save_system import SaveSystem, get_save_system
from .achievements import AchievementSystem, Achievement
from .config_manager import ConfigManager, get_config
from .validation import get_menu_choice, get_yes_no_input
from .logging_config import get_logger

__all__ = [
    'TurnBasedGame',
    'GameMetadata',
    'SaveSystem',
    'get_save_system',
    'AchievementSystem',
    'Achievement',
    'ConfigManager',
    'get_config',
    'get_menu_choice',
    'get_yes_no_input',
    'get_logger',
]
