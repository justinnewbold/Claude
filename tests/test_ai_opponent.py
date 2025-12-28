"""
Tests for ai_opponent module
=============================
"""

import pytest
from unittest.mock import Mock, patch


class TestDifficulty:
    """Test Difficulty enum"""

    def test_difficulty_levels(self):
        """Test all difficulty levels exist"""
        from ai_opponent import Difficulty

        assert Difficulty.EASY.value == "easy"
        assert Difficulty.MEDIUM.value == "medium"
        assert Difficulty.HARD.value == "hard"
        assert Difficulty.NIGHTMARE.value == "nightmare"


class TestPersonality:
    """Test Personality enum"""

    def test_personality_types(self):
        """Test all personality types exist"""
        from ai_opponent import Personality

        assert Personality.AGGRESSIVE.value == "aggressive"
        assert Personality.DEFENSIVE.value == "defensive"
        assert Personality.BALANCED.value == "balanced"
        assert Personality.CHAOTIC.value == "chaotic"
        assert Personality.ANALYTICAL.value == "analytical"
        assert Personality.TRICKY.value == "tricky"


class TestAIConfig:
    """Test AIConfig dataclass"""

    def test_default_values(self):
        """Test default AIConfig values"""
        from ai_opponent import AIConfig, Difficulty, Personality

        config = AIConfig()

        assert config.difficulty == Difficulty.MEDIUM
        assert config.personality == Personality.BALANCED
        assert config.think_time_seconds == 1.0
        assert config.mistake_chance == 0.0
        assert config.learning_enabled is True
        assert config.taunt_enabled is False

    def test_custom_values(self):
        """Test AIConfig with custom values"""
        from ai_opponent import AIConfig, Difficulty, Personality

        config = AIConfig(
            difficulty=Difficulty.HARD,
            personality=Personality.AGGRESSIVE,
            taunt_enabled=True
        )

        assert config.difficulty == Difficulty.HARD
        assert config.personality == Personality.AGGRESSIVE
        assert config.taunt_enabled is True


class TestPlayerPattern:
    """Test PlayerPattern dataclass"""

    def test_default_values(self):
        """Test default PlayerPattern values"""
        from ai_opponent import PlayerPattern

        pattern = PlayerPattern()

        assert pattern.opening_moves == []
        assert pattern.common_responses == {}
        assert pattern.preferred_strategies == {}
        assert pattern.games_analyzed == 0


class TestRandomStrategy:
    """Test RandomStrategy class"""

    def test_creation(self):
        """Test creating a RandomStrategy"""
        from ai_opponent import RandomStrategy

        get_moves = lambda s: [1, 2, 3]
        strategy = RandomStrategy(get_moves)

        moves = strategy.get_possible_moves({})
        assert moves == [1, 2, 3]

    def test_with_all_callbacks(self):
        """Test RandomStrategy with all callbacks"""
        from ai_opponent import RandomStrategy

        get_moves = lambda s: ["a", "b"]
        evaluate = lambda s: 0.5
        apply = lambda s, m: f"{s}_{m}"
        is_terminal = lambda s: len(s) > 5

        strategy = RandomStrategy(get_moves, evaluate, apply, is_terminal)

        assert strategy.evaluate_state("test") == 0.5
        assert strategy.apply_move("state", "m") == "state_m"
        assert strategy.is_terminal("short") is False
        assert strategy.is_terminal("toolong") is True


class TestAIOpponent:
    """Test AIOpponent class"""

    def test_creation(self):
        """Test creating an AIOpponent"""
        from ai_opponent import AIOpponent

        ai = AIOpponent("test_game")

        assert ai.game_id == "test_game"
        assert ai.games_played == 0
        assert ai.games_won == 0
        assert ai.win_rate == 0.0

    def test_difficulty_setup(self):
        """Test difficulty affects mistake_chance"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty

        easy_config = AIConfig(difficulty=Difficulty.EASY)
        easy_ai = AIOpponent("test", easy_config)

        hard_config = AIConfig(difficulty=Difficulty.HARD)
        hard_ai = AIOpponent("test", hard_config)

        # Easy AI should make more mistakes
        assert easy_ai.config.mistake_chance > hard_ai.config.mistake_chance

    def test_get_move_with_possible_moves(self):
        """Test getting a move with provided moves"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty

        config = AIConfig(
            difficulty=Difficulty.EASY,
            think_time_seconds=0.01  # Fast for testing
        )
        ai = AIOpponent("test", config)

        move = ai.get_move(None, possible_moves=[1, 2, 3])

        assert move in [1, 2, 3]

    def test_get_move_requires_moves_or_strategy(self):
        """Test get_move raises error without moves or strategy"""
        from ai_opponent import AIOpponent

        ai = AIOpponent("test")

        with pytest.raises(ValueError):
            ai.get_move({})

    def test_record_result(self):
        """Test recording game results"""
        from ai_opponent import AIOpponent

        ai = AIOpponent("test")

        ai.record_result(won=True)
        assert ai.games_played == 1
        assert ai.games_won == 1
        assert ai.win_rate == 1.0

        ai.record_result(won=False)
        assert ai.games_played == 2
        assert ai.games_won == 1
        assert ai.win_rate == 0.5

    def test_get_taunt_disabled(self):
        """Test taunts disabled by default"""
        from ai_opponent import AIOpponent

        ai = AIOpponent("test")
        taunt = ai.get_taunt()

        assert taunt is None

    def test_get_taunt_enabled(self):
        """Test taunts when enabled"""
        from ai_opponent import AIOpponent, AIConfig

        config = AIConfig(taunt_enabled=True)
        ai = AIOpponent("test", config)

        taunt = ai.get_taunt("general")

        assert taunt is not None
        assert isinstance(taunt, str)


class TestMinimax:
    """Test minimax algorithm"""

    def test_minimax_basic(self):
        """Test basic minimax functionality"""
        from ai_opponent import minimax, RandomStrategy

        # Simple number comparison game
        get_moves = lambda s: [s + 1, s + 2] if s < 5 else []
        evaluate = lambda s: s  # Higher is better
        apply = lambda s, m: m
        is_terminal = lambda s: s >= 5

        strategy = RandomStrategy(get_moves, evaluate, apply, is_terminal)

        score, move = minimax(strategy, 0, depth=3, maximizing=True)

        assert move is not None
        assert score >= 0


class TestMonteCarloSearch:
    """Test Monte Carlo search"""

    def test_monte_carlo_basic(self):
        """Test basic Monte Carlo search"""
        from ai_opponent import monte_carlo_search, RandomStrategy

        get_moves = lambda s: ["good", "bad"]
        evaluate = lambda s: 1.0 if s == "good" else 0.0
        apply = lambda s, m: m
        is_terminal = lambda s: s in ["good", "bad"]

        strategy = RandomStrategy(get_moves, evaluate, apply, is_terminal)

        move = monte_carlo_search(strategy, "start", simulations=10)

        assert move in ["good", "bad"]


class TestFactoryFunctions:
    """Test factory functions"""

    def test_create_opponent(self):
        """Test create_opponent function"""
        from ai_opponent import create_opponent, Difficulty, Personality

        ai = create_opponent("test", "hard", "aggressive")

        assert ai.game_id == "test"
        assert ai.config.difficulty == Difficulty.HARD
        assert ai.config.personality == Personality.AGGRESSIVE

    def test_create_easy_opponent(self):
        """Test create_easy_opponent function"""
        from ai_opponent import create_easy_opponent, Difficulty

        ai = create_easy_opponent("test")

        assert ai.config.difficulty == Difficulty.EASY

    def test_create_hard_opponent(self):
        """Test create_hard_opponent function"""
        from ai_opponent import create_hard_opponent, Difficulty

        ai = create_hard_opponent("test")

        assert ai.config.difficulty == Difficulty.HARD
