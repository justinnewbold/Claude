#!/usr/bin/env python3
"""
Integration Tests - Complete Game Lifecycle
============================================
Test complete game workflows end-to-end.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import time

from base_game import TurnBasedGame, GameMetadata
from save_system import SaveSystem
from achievements import AchievementSystem, Achievement, AchievementCategory, AchievementRarity
from config_manager import ConfigManager
from tutorial_system import TutorialSystem, TutorialBuilder
from mod_loader import ModLoader, ModCreator
from analytics import Analytics, EventType


# =============================================================================
# TEST GAME
# =============================================================================

class TestGame(TurnBasedGame):
    """Simple test game for integration testing"""

    def __init__(self, config_dir=None, save_dir=None):
        super().__init__(GameMetadata(
            name="Test Game",
            version="1.0",
            description="Integration test game"
        ))

        self.config = ConfigManager(config_dir=config_dir) if config_dir else None
        self.save_system = SaveSystem(save_dir=save_dir) if save_dir else None
        self.achievements = AchievementSystem('test_game')
        self.score = 0
        self.level = 1

    def setup(self):
        pass

    def render(self):
        pass

    def handle_input(self, key=None):
        # Simplified for testing
        self.score += 10

    def update(self):
        if self.score >= 100:
            self.level += 1
            self.score = 0

    def cleanup(self):
        pass


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    config_dir = temp_dir / "config"
    save_dir = temp_dir / "saves"
    mods_dir = temp_dir / "mods"
    analytics_dir = temp_dir / "analytics"

    config_dir.mkdir()
    save_dir.mkdir()
    mods_dir.mkdir()
    analytics_dir.mkdir()

    yield {
        'config': config_dir,
        'save': save_dir,
        'mods': mods_dir,
        'analytics': analytics_dir
    }

    shutil.rmtree(temp_dir)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

def test_complete_game_session(temp_dirs):
    """Test complete game session with all features"""
    # Create game
    game = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    # Setup
    game.setup()

    # Play some turns
    for i in range(10):
        game.handle_input()
        game.update()

    assert game.score == 0  # Should have leveled up once (100 points)
    assert game.level == 2

    # Cleanup
    game.cleanup()


def test_save_load_roundtrip(temp_dirs):
    """Test saving and loading preserves game state"""
    # Create and play game
    game1 = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    game1.score = 500
    game1.level = 5
    game1.turn = 42

    # Save
    game1.save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data={
            'score': game1.score,
            'level': game1.level,
            'turn': game1.turn
        },
        save_slot=1
    )

    # Load in new instance
    game2 = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    save_file = game2.save_system.load('test_game', save_slot=1)
    assert save_file is not None

    game2.score = save_file.data['score']
    game2.level = save_file.data['level']
    game2.turn = save_file.data['turn']

    # Verify state preserved
    assert game2.score == 500
    assert game2.level == 5
    assert game2.turn == 42


def test_achievement_unlock_flow(temp_dirs):
    """Test achievement unlock workflow"""
    game = TestGame(config_dir=temp_dirs['config'])

    # Register achievement
    game.achievements.register_achievement(Achievement(
        id="score_100",
        name="Century",
        description="Reach 100 points",
        category=AchievementCategory.PROGRESSION,
        rarity=AchievementRarity.COMMON,
        points=10,
        requirements={'score': 100}
    ))

    # Track progress
    for i in range(10):
        game.score += 10
        game.achievements.update_progress('score_100', {'score': game.score})

    # Verify unlocked
    assert game.achievements.get_progress('score_100').unlocked
    assert 'score_100' in [ach.id for ach in game.achievements.get_unlocked()]


def test_configuration_persistence(temp_dirs):
    """Test configuration saves and loads"""
    from config_manager import Difficulty, TextSpeed

    # Create and modify config
    config1 = ConfigManager(config_dir=temp_dirs['config'])
    config1.gameplay.difficulty = Difficulty.HARD
    config1.display.text_speed = TextSpeed.FAST
    config1.save()

    # Load in new instance
    config2 = ConfigManager(config_dir=temp_dirs['config'])

    assert config2.gameplay.difficulty.value == 'hard'
    assert config2.display.text_speed.value == 0.01


def test_mod_loading_integration(temp_dirs):
    """Test mod loading with game"""
    # Create a test mod
    ModCreator.create_mod_template(
        mod_id='test_mod',
        name='Test Mod',
        author='Test',
        game_id='test_game',
        output_dir=temp_dirs['mods']
    )

    # Load mods
    loader = ModLoader('test_game', mods_dir=temp_dirs['mods'])
    loader.load_all_mods()

    # Verify mod loaded
    assert 'test_mod' in loader.mods
    assert loader.mods['test_mod'].status.value == 'loaded'


def test_analytics_session_tracking(temp_dirs):
    """Test analytics tracks complete session"""
    analytics = Analytics(analytics_dir=temp_dirs['analytics'])
    analytics.enable()

    # Start session
    analytics.start_session('test_game', {'version': '1.0'})

    # Track events
    analytics.track_event(EventType.LEVEL_UP, {'level': 2})
    analytics.track_event(EventType.ACHIEVEMENT_UNLOCK, {'achievement': 'first_win'})

    # Small delay
    time.sleep(0.1)

    # End session
    analytics.end_session()

    # Verify session recorded
    stats = analytics.get_statistics('test_game')
    assert stats['total_sessions'] == 1
    assert stats['total_playtime'] > 0


def test_multiple_save_slots(temp_dirs):
    """Test multiple save slots work independently"""
    save_system = SaveSystem(save_dir=temp_dirs['save'])

    # Save to slot 1
    save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data={'score': 100, 'level': 1},
        save_slot=1
    )

    # Save to slot 2
    save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data={'score': 200, 'level': 2},
        save_slot=2
    )

    # Load both
    save1 = save_system.load('test_game', save_slot=1)
    save2 = save_system.load('test_game', save_slot=2)

    assert save1.data['score'] == 100
    assert save2.data['score'] == 200


def test_achievement_persistence(temp_dirs):
    """Test achievements persist across sessions"""
    # Session 1 - unlock achievement
    achievements1 = AchievementSystem('test_game')
    achievements1.register_achievement(Achievement(
        id="test_ach",
        name="Test",
        description="Test achievement",
        category=AchievementCategory.PROGRESSION,
        rarity=AchievementRarity.COMMON,
        points=10
    ))
    achievements1.unlock('test_ach')

    # Session 2 - verify still unlocked
    achievements2 = AchievementSystem('test_game')
    achievements2.register_achievement(Achievement(
        id="test_ach",
        name="Test",
        description="Test achievement",
        category=AchievementCategory.PROGRESSION,
        rarity=AchievementRarity.COMMON,
        points=10
    ))

    progress = achievements2.get_progress('test_ach')
    assert progress.unlocked


def test_config_with_game(temp_dirs):
    """Test game uses configuration settings"""
    # Set up config
    config = ConfigManager(config_dir=temp_dirs['config'])
    config.gameplay.auto_save = True
    config.gameplay.auto_save_interval = 5
    config.save()

    # Create game
    game = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    # Verify game can access config
    assert game.config.should_auto_save()
    assert game.config.gameplay.auto_save_interval == 5


def test_full_workflow(temp_dirs):
    """Test complete workflow: play, save, load, continue"""
    # Session 1: New game
    game1 = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    # Register achievements
    game1.achievements.register_achievement(Achievement(
        id="level_5",
        name="Level 5",
        description="Reach level 5",
        category=AchievementCategory.PROGRESSION,
        rarity=AchievementRarity.UNCOMMON,
        points=15,
        requirements={'level': 5}
    ))

    # Play
    for i in range(30):
        game1.handle_input()
        game1.update()

    # Save
    game1.save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data={'score': game1.score, 'level': game1.level},
        save_slot=1
    )

    original_level = game1.level

    # Session 2: Load and continue
    game2 = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    save_file = game2.save_system.load('test_game', save_slot=1)
    game2.score = save_file.data['score']
    game2.level = save_file.data['level']

    # Verify loaded correctly
    assert game2.level == original_level

    # Continue playing
    for i in range(20):
        game2.handle_input()
        game2.update()

    # Verify progression continued
    assert game2.level >= original_level


def test_error_recovery(temp_dirs):
    """Test system handles errors gracefully"""
    save_system = SaveSystem(save_dir=temp_dirs['save'])

    # Try to load non-existent save
    save_file = save_system.load('nonexistent_game', save_slot=1)
    assert save_file is None  # Should return None, not crash

    # Try to load with invalid data
    # (System should handle corrupted data gracefully)
    pass  # Add more error cases as needed


def test_concurrent_systems(temp_dirs):
    """Test multiple systems work together"""
    game = TestGame(
        config_dir=temp_dirs['config'],
        save_dir=temp_dirs['save']
    )

    analytics = Analytics(analytics_dir=temp_dirs['analytics'])
    analytics.enable()
    analytics.start_session('test_game')

    # Play with all systems active
    for i in range(10):
        game.handle_input()
        game.update()

        # Track progress
        game.achievements.update_progress('test_ach', {'score': game.score})

        # Track events
        if analytics.is_enabled():
            analytics.track_event(EventType.LEVEL_UP, {'level': game.level})

    # Save
    game.save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data={'score': game.score},
        save_slot=1
    )

    # End analytics
    analytics.end_session()

    # Verify all systems worked
    assert game.score >= 0
    assert game.save_system.load('test_game', save_slot=1) is not None
    assert analytics.get_statistics()['total_sessions'] > 0
