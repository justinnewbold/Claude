"""
Tests for games_registry.json and related functionality
"""

import json
import pytest
from pathlib import Path


class TestGamesRegistry:
    """Test games registry JSON file"""

    @pytest.fixture
    def registry_path(self):
        """Path to games registry file"""
        return Path(__file__).parent.parent / "games_registry.json"

    @pytest.fixture
    def registry(self, registry_path):
        """Load games registry"""
        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_registry_exists(self, registry_path):
        """Test registry file exists"""
        assert registry_path.exists(), "games_registry.json should exist"

    def test_registry_is_valid_json(self, registry_path):
        """Test registry is valid JSON"""
        with open(registry_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_registry_has_games(self, registry):
        """Test registry contains games"""
        assert 'games' in registry
        assert len(registry['games']) > 0

    def test_registry_has_categories(self, registry):
        """Test registry contains categories"""
        assert 'categories' in registry
        assert len(registry['categories']) > 0

    def test_all_games_have_required_fields(self, registry):
        """Test all games have required fields"""
        required_fields = ['id', 'name', 'description', 'module_path']

        for game_id, game in registry['games'].items():
            for field in required_fields:
                assert field in game, f"Game {game_id} missing field {field}"

    def test_game_module_paths_exist(self, registry, registry_path):
        """Test game module files exist"""
        base_path = registry_path.parent

        for game_id, game in registry['games'].items():
            module_path = base_path / game['module_path']
            assert module_path.exists(), f"Module for {game_id} not found: {game['module_path']}"

    def test_all_games_have_valid_category(self, registry):
        """Test all games have valid category reference"""
        categories = set(registry.get('categories', {}).keys())

        for game_id, game in registry['games'].items():
            if 'category' in game:
                assert game['category'] in categories, \
                    f"Game {game_id} has invalid category: {game['category']}"

    def test_game_ids_match_keys(self, registry):
        """Test game IDs match their keys"""
        for game_id, game in registry['games'].items():
            assert game['id'] == game_id, \
                f"Game key {game_id} doesn't match id {game['id']}"

    def test_no_duplicate_game_names(self, registry):
        """Test no duplicate game names"""
        names = [game['name'] for game in registry['games'].values()]
        assert len(names) == len(set(names)), "Duplicate game names found"

    def test_registry_has_version(self, registry):
        """Test registry has version info"""
        assert 'version' in registry


class TestGameLauncherRegistry:
    """Test GameLauncher using registry"""

    def test_launcher_loads_games(self):
        """Test GameLauncher loads games from registry"""
        from game_launcher import GameLauncher

        launcher = GameLauncher()
        assert len(launcher.games) > 30, "Should load 30+ games"

    def test_launcher_game_info_correct(self):
        """Test GameInfo objects are populated correctly"""
        from game_launcher import GameLauncher

        launcher = GameLauncher()
        vault = launcher.games.get('vault_shelter')

        assert vault is not None
        assert vault.name == "VAULT 13 - Survival Protocol"
        assert vault.module_path == "vault_shelter_v6.py"

    def test_launcher_handles_missing_registry(self, tmp_path, monkeypatch):
        """Test launcher handles missing registry gracefully"""
        from game_launcher import GameLauncher

        # Temporarily change to a path without registry
        monkeypatch.chdir(tmp_path)

        launcher = GameLauncher()
        # Should not crash, just have empty games
        assert isinstance(launcher.games, dict)
