"""
Tests for config module
========================
"""

import pytest
from pathlib import Path
from config import (
    Paths,
    GameSettings,
    GameBalance,
    Config,
    get_games_by_category,
    get_all_categories,
    GAME_REGISTRY
)


class TestPaths:
    """Test path management"""

    def test_paths_singleton(self):
        """Test that Paths is a singleton"""
        paths1 = Paths()
        paths2 = Paths()
        assert paths1 is paths2

    def test_paths_create_directories(self):
        """Test that necessary directories are created"""
        paths = Paths()
        assert paths.app_data.exists()
        assert paths.config_dir.exists()
        assert paths.save_dir.exists()

    def test_get_save_file(self):
        """Test save file path generation"""
        paths = Paths()
        save_file = paths.get_save_file(0)
        assert save_file.name == 'vault_save.json'

        save_file_2 = paths.get_save_file(2)
        assert save_file_2.name == 'vault_save_2.json'


class TestGameSettings:
    """Test game settings"""

    def test_default_settings(self):
        """Test default settings are sensible"""
        settings = GameSettings()
        assert settings.color_enabled is True
        assert settings.difficulty == "normal"
        assert settings.autosave_enabled is True

    def test_settings_validation(self):
        """Test settings post-init validation"""
        # This would test platform-specific adjustments
        settings = GameSettings()
        # Should always be bool
        assert isinstance(settings.color_enabled, bool)
        assert isinstance(settings.unicode_enabled, bool)


class TestGameRegistry:
    """Test game registry"""

    def test_game_registry_not_empty(self):
        """Test that game registry has entries"""
        assert len(GAME_REGISTRY) > 0

    def test_all_games_have_required_fields(self):
        """Test all registered games have required info"""
        for game_id, game_info in GAME_REGISTRY.items():
            assert game_info.id
            assert game_info.name
            assert game_info.file
            assert game_info.category
            assert isinstance(game_info.playable, bool)

    def test_get_games_by_category(self):
        """Test filtering games by category"""
        main_games = get_games_by_category('main')
        assert len(main_games) > 0
        assert all(g.category == 'main' for g in main_games)

        quantum_games = get_games_by_category('quantum')
        assert all(g.category == 'quantum' for g in quantum_games)

    def test_get_all_categories(self):
        """Test getting all categories"""
        categories = get_all_categories()
        assert 'main' in categories
        assert 'quantum' in categories
        assert 'computation' in categories

    def test_no_duplicate_game_ids(self):
        """Test that all game IDs are unique"""
        game_ids = [g.id for g in GAME_REGISTRY.values()]
        assert len(game_ids) == len(set(game_ids))


class TestConfig:
    """Test config management"""

    def test_config_singleton(self):
        """Test that Config is a singleton"""
        config1 = Config()
        config2 = Config()
        assert config1 is config2

    def test_difficulty_multipliers(self):
        """Test getting difficulty multipliers"""
        config = Config()
        config.settings.difficulty = 'easy'
        multipliers = config.get_difficulty_multipliers()

        assert 'resource_production' in multipliers
        assert 'resource_consumption' in multipliers
        assert multipliers['resource_production'] > 1.0  # Easy bonus

    def test_difficulty_multipliers_invalid(self):
        """Test invalid difficulty defaults to normal"""
        config = Config()
        config.settings.difficulty = 'invalid'
        multipliers = config.get_difficulty_multipliers()

        # Should default to normal (all 1.0)
        assert multipliers['resource_production'] == 1.0
        assert multipliers['resource_consumption'] == 1.0
