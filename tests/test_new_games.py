#!/usr/bin/env python3
"""
Tests for new philosophical games and systems.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSimulationArgument:
    """Tests for Simulation Argument game"""

    def test_import(self):
        """Test that the module can be imported"""
        import simulation_argument
        assert hasattr(simulation_argument, 'SimulationArgumentGame')
        assert hasattr(simulation_argument, 'main')

    def test_game_initialization(self):
        """Test game initializes correctly"""
        from simulation_argument import SimulationArgumentGame, BeliefState
        game = SimulationArgumentGame()
        assert game.state.day == 1
        assert game.state.belief == BeliefState.UNCERTAIN
        assert game.state.evidence_score == 0
        assert game.state.reality_stability == 100

    def test_belief_update(self):
        """Test belief state updates based on evidence"""
        from simulation_argument import SimulationArgumentGame, BeliefState
        game = SimulationArgumentGame()

        # Increase evidence for simulation
        game.state.evidence_score = 20
        game.update_belief()
        assert game.state.belief == BeliefState.CONVINCED_SIM

        # Decrease evidence
        game.state.evidence_score = -20
        game.update_belief()
        assert game.state.belief == BeliefState.CONVINCED_REAL


class TestParadoxOfHeap:
    """Tests for Paradox of the Heap game"""

    def test_import(self):
        """Test that the module can be imported"""
        import paradox_of_heap
        assert hasattr(paradox_of_heap, 'ParadoxOfHeapGame')
        assert hasattr(paradox_of_heap, 'main')

    def test_game_initialization(self):
        """Test game initializes correctly"""
        from paradox_of_heap import ParadoxOfHeapGame
        game = ParadoxOfHeapGame()
        assert game.state.understanding == 0
        assert game.state.frustration == 0
        assert len(game.state.paradoxes_explored) == 0


class TestRokosBasilisk:
    """Tests for Roko's Basilisk game"""

    def test_import(self):
        """Test that the module can be imported"""
        import rokos_basilisk
        assert hasattr(rokos_basilisk, 'RokosBasiliskGame')
        assert hasattr(rokos_basilisk, 'main')

    def test_game_initialization(self):
        """Test game initializes correctly"""
        from rokos_basilisk import RokosBasiliskGame, StanceType
        game = RokosBasiliskGame()
        assert game.state.day == 1
        assert game.state.stance == StanceType.UNAWARE
        assert game.state.fear_level == 50
        assert game.state.rationality == 50

    def test_stance_update(self):
        """Test stance updates correctly"""
        from rokos_basilisk import RokosBasiliskGame, StanceType
        game = RokosBasiliskGame()

        game.state.fear_level = 85
        game.update_stance()
        assert game.state.stance == StanceType.FEARFUL

        game.state.fear_level = 15
        game.state.rationality = 75
        game.update_stance()
        assert game.state.stance == StanceType.RATIONAL


class TestZenosParadoxes:
    """Tests for Zeno's Paradoxes game"""

    def test_import(self):
        """Test that the module can be imported"""
        import zenos_paradoxes
        assert hasattr(zenos_paradoxes, 'ZenosParadoxesGame')
        assert hasattr(zenos_paradoxes, 'main')

    def test_game_initialization(self):
        """Test game initializes correctly"""
        from zenos_paradoxes import ZenosParadoxesGame
        game = ZenosParadoxesGame()
        assert game.state.understanding == 0
        assert game.state.frustration == 0
        assert len(game.state.paradoxes_explored) == 0


class TestKarmaSystem:
    """Tests for the Karma System"""

    def test_import(self):
        """Test that the module can be imported"""
        from vault13.systems.karma import KarmaSystem, DecisionType, KarmaAlignment

    def test_karma_initialization(self):
        """Test karma system initializes correctly"""
        from vault13.systems.karma import KarmaSystem
        karma = KarmaSystem()
        assert karma.profile.total_karma == 0

    def test_karma_recording(self):
        """Test recording decisions affects karma"""
        from vault13.systems.karma import KarmaSystem, DecisionType
        karma = KarmaSystem()

        karma.record_decision(
            "test_game", "test_event",
            "Test decision", 10, DecisionType.VIRTUE
        )
        assert karma.profile.total_karma == 10

        karma.record_decision(
            "test_game", "test_event_2",
            "Bad decision", -15, DecisionType.SELF_INTEREST
        )
        assert karma.profile.total_karma == -5

    def test_alignment(self):
        """Test alignment calculation"""
        from vault13.systems.karma import KarmaSystem, KarmaAlignment, DecisionType
        karma = KarmaSystem()

        # Neutral by default
        assert karma.get_alignment() == KarmaAlignment.NEUTRAL

        # Become good
        karma.record_decision("test", "good", "Good act", 50, DecisionType.VIRTUE)
        assert karma.get_alignment() == KarmaAlignment.GOOD

        # Become very good
        karma.record_decision("test", "better", "Great act", 30, DecisionType.SACRIFICE)
        assert karma.get_alignment() == KarmaAlignment.SAINT


class TestStoryMode:
    """Tests for Story Mode"""

    def test_import(self):
        """Test that the module can be imported"""
        import story_mode
        assert hasattr(story_mode, 'StoryMode')
        assert hasattr(story_mode, 'main')
        assert hasattr(story_mode, 'STORY_CHAPTERS')

    def test_story_initialization(self):
        """Test story mode initializes correctly"""
        from story_mode import StoryMode
        story = StoryMode()
        assert story.progress.current_chapter == 0
        assert len(story.progress.chapters_completed) == 0

    def test_chapter_availability(self):
        """Test chapter availability logic"""
        from story_mode import StoryMode, STORY_CHAPTERS
        story = StoryMode()

        # Prologue should be available
        prologue = story.chapters.get("prologue")
        assert story.is_chapter_available(prologue)

        # Reality chapter should be available (no requirements)
        reality = story.chapters.get("reality")
        assert story.is_chapter_available(reality)

        # Motion should not be available (requires reality)
        motion = story.chapters.get("motion")
        assert not story.is_chapter_available(motion)


class TestAIOpponent:
    """Tests for AI Opponent system"""

    def test_import(self):
        """Test that the module can be imported"""
        from ai_opponent import AIOpponent, Difficulty, Personality

    def test_ai_initialization(self):
        """Test AI opponent initializes correctly"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty, Personality
        config = AIConfig(difficulty=Difficulty.MEDIUM, personality=Personality.BALANCED)
        ai = AIOpponent("test_game", config)
        assert ai.games_played == 0
        assert ai.games_won == 0

    def test_adaptive_difficulty(self):
        """Test adaptive difficulty adjusts correctly"""
        from ai_opponent import AdaptiveDifficulty, Difficulty
        adaptive = AdaptiveDifficulty(base_difficulty=Difficulty.MEDIUM)

        # Player wins 3 times
        for _ in range(3):
            adaptive.adjust_after_game(player_won=True)

        # Should have increased (easier for player)
        assert adaptive.current_adjustment > 0

        # AI wins 3 times
        for _ in range(6):
            adaptive.adjust_after_game(player_won=False)

        # Should have decreased (harder for player)
        assert adaptive.current_adjustment < 0

    def test_player_pattern_tracking(self):
        """Test player pattern tracking"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty
        config = AIConfig(difficulty=Difficulty.MEDIUM, learning_enabled=True)
        ai = AIOpponent("test_game", config)

        # Record some player moves
        ai.record_player_move("move_a", reaction_time=1.5)
        ai.record_player_move("move_b", reaction_time=2.0)
        ai.record_player_move("move_c", reaction_time=1.0)

        # Check average reaction time
        avg_time = ai.get_player_average_reaction_time()
        assert avg_time == pytest.approx(1.5, 0.01)


class TestVault13Models:
    """Tests for vault13 modular models"""

    def test_dweller_model(self):
        """Test Dweller model"""
        from vault13.models.dweller import Dweller
        dweller = Dweller(name="Test Dweller")
        assert dweller.name == "Test Dweller"
        assert dweller.health == 100
        assert dweller.happiness == 50

    def test_dweller_stats(self):
        """Test Dweller stat calculations"""
        from vault13.models.dweller import Dweller
        dweller = Dweller(name="Test", strength=7, intelligence=8)
        assert dweller.get_stat("strength") == 7
        assert dweller.get_stat("intelligence") == 8
        assert dweller.get_total_stats() == 5 * 5 + 7 + 8  # 5 default stats + 2 custom

    def test_room_model(self):
        """Test Room model"""
        from vault13.models.room import Room
        from vault13.constants import RoomType
        room = Room(room_type=RoomType.POWER_GENERATOR, floor=0, position=0)
        assert room.room_type == RoomType.POWER_GENERATOR
        assert room.level == 1
        assert room.can_rush()

    def test_resources_model(self):
        """Test Resources model"""
        from vault13.models.resources import Resources
        resources = Resources()
        assert resources.power == 20
        assert resources.water == 20
        assert resources.food == 20

        resources.add("power", 10)
        assert resources.power == 30  # Capped at max

        resources.remove("caps", 100)
        assert resources.caps == 400


class TestGamesRegistry:
    """Tests for games registry"""

    def test_registry_loads(self):
        """Test that games registry loads correctly"""
        import json
        with open("games_registry.json", "r") as f:
            registry = json.load(f)
        assert "games" in registry
        assert "categories" in registry

    def test_new_games_in_registry(self):
        """Test that new games are in the registry"""
        import json
        with open("games_registry.json", "r") as f:
            registry = json.load(f)

        games = registry["games"]
        assert "simulation_argument" in games
        assert "paradox_of_heap" in games
        assert "rokos_basilisk" in games
        assert "zenos_paradoxes" in games
        assert "story_mode" in games


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
