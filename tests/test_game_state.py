"""
Tests for game_state module
=============================
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch


class TestGameStats:
    """Test GameStats dataclass"""

    def test_default_values(self):
        """Test default GameStats values"""
        from game_state import GameStats
        stats = GameStats()
        assert stats.play_count == 0
        assert stats.total_play_time_seconds == 0.0
        assert stats.high_score == 0
        assert stats.best_time_seconds is None
        assert stats.wins == 0
        assert stats.losses == 0
        assert stats.achievements == []

    def test_custom_values(self):
        """Test GameStats with custom values"""
        from game_state import GameStats
        stats = GameStats(
            play_count=10,
            high_score=5000,
            wins=7,
            losses=3
        )
        assert stats.play_count == 10
        assert stats.high_score == 5000
        assert stats.wins == 7
        assert stats.losses == 3


class TestGameStateManager:
    """Test GameStateManager functionality"""

    def test_singleton_pattern(self):
        """Test that GameStateManager is a singleton"""
        from game_state import GameStateManager
        manager1 = GameStateManager()
        manager2 = GameStateManager()
        assert manager1 is manager2

    def test_get_or_create_stats(self):
        """Test getting or creating game stats"""
        from game_state import get_state_manager
        manager = get_state_manager()

        # Should create new stats for unknown game
        stats = manager._get_or_create_stats("test_game_xyz")
        assert stats.play_count == 0

    def test_high_score_tracking(self):
        """Test high score tracking"""
        from game_state import get_state_manager
        manager = get_state_manager()

        game_id = "test_high_score_game"

        # First score should be recorded
        result = manager.set_high_score(game_id, 1000)
        assert result is True
        assert manager.get_high_score(game_id) == 1000

        # Lower score should not replace
        result = manager.set_high_score(game_id, 500)
        assert result is False
        assert manager.get_high_score(game_id) == 1000

        # Higher score should replace
        result = manager.set_high_score(game_id, 2000)
        assert result is True
        assert manager.get_high_score(game_id) == 2000

    def test_achievement_unlock(self):
        """Test achievement unlocking"""
        from game_state import get_state_manager
        manager = get_state_manager()

        game_id = "test_achievement_game"

        # First unlock should succeed
        result = manager.unlock_achievement(
            game_id, "test_ach", "Test Achievement", "A test"
        )
        assert result is True
        assert manager.has_achievement(game_id, "test_ach")

        # Second unlock should return False (already unlocked)
        result = manager.unlock_achievement(
            game_id, "test_ach", "Test Achievement", "A test"
        )
        assert result is False

    def test_play_time_formatting(self):
        """Test play time formatting"""
        from game_state import get_state_manager
        from datetime import timedelta

        manager = get_state_manager()

        # Test seconds
        assert manager.format_play_time(timedelta(seconds=45)) == "45s"

        # Test minutes
        assert manager.format_play_time(timedelta(minutes=5, seconds=30)) == "5m 30s"

        # Test hours
        assert manager.format_play_time(timedelta(hours=2, minutes=30)) == "2h 30m"


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_start_and_end_session(self):
        """Test session tracking convenience functions"""
        from game_state import start_game_session, end_game_session, get_state_manager

        game_id = "test_session_game"

        start_game_session(game_id)
        end_game_session(game_id, score=100, won=True)

        manager = get_state_manager()
        stats = manager._get_or_create_stats(game_id)
        assert stats.play_count >= 1
        assert stats.wins >= 1

    def test_record_high_score(self):
        """Test record_high_score convenience function"""
        from game_state import record_high_score, get_state_manager

        game_id = "test_record_score_game"

        result = record_high_score(game_id, 999)
        manager = get_state_manager()
        assert manager.get_high_score(game_id) == 999
