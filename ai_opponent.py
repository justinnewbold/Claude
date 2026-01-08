#!/usr/bin/env python3
"""
AI Opponent System
==================
Provides configurable AI opponents for single-player games.

Features:
- Multiple difficulty levels
- Pluggable strategy system
- Learning from player patterns
- Personality-based behavior
- Common game AI algorithms (minimax, Monte Carlo, etc.)

Usage:
    from ai_opponent import AIOpponent, Difficulty

    # Create an AI opponent
    ai = AIOpponent("chess", difficulty=Difficulty.MEDIUM)

    # Get AI's move
    move = ai.get_move(game_state)

    # Record result for learning
    ai.record_result(won=False)
"""

import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List, Callable, TypeVar, Generic
from logging_config import get_logger

logger = get_logger(__name__)

# Type variable for game state
GameState = TypeVar('GameState')
Move = TypeVar('Move')


class Difficulty(Enum):
    """AI difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    NIGHTMARE = "nightmare"


class Personality(Enum):
    """AI personality types affecting play style"""
    AGGRESSIVE = "aggressive"      # Prefers attacking moves
    DEFENSIVE = "defensive"        # Prefers safe moves
    BALANCED = "balanced"          # Mix of strategies
    CHAOTIC = "chaotic"           # Unpredictable
    ANALYTICAL = "analytical"      # Optimal play
    TRICKY = "tricky"             # Sets traps


@dataclass
class AIConfig:
    """Configuration for AI behavior"""
    difficulty: Difficulty = Difficulty.MEDIUM
    personality: Personality = Personality.BALANCED
    think_time_seconds: float = 1.0  # Simulated thinking time
    mistake_chance: float = 0.0      # Chance of suboptimal move
    learning_enabled: bool = True    # Learn from games
    taunt_enabled: bool = False      # Say things during play


@dataclass
class PlayerPattern:
    """Tracks patterns in player behavior"""
    opening_moves: List[Any] = field(default_factory=list)
    common_responses: Dict[str, List[Any]] = field(default_factory=dict)
    preferred_strategies: Dict[str, int] = field(default_factory=dict)
    games_analyzed: int = 0
    move_sequences: List[List[Any]] = field(default_factory=list)
    reaction_times: List[float] = field(default_factory=list)
    risk_tolerance: float = 0.5  # 0=conservative, 1=aggressive


@dataclass
class AdaptiveDifficulty:
    """Tracks adaptive difficulty settings"""
    base_difficulty: Difficulty = Difficulty.MEDIUM
    current_adjustment: float = 0.0  # -1 to 1 adjustment
    player_win_streak: int = 0
    ai_win_streak: int = 0
    games_for_adjustment: int = 3

    def adjust_after_game(self, player_won: bool):
        """Adjust difficulty based on results"""
        if player_won:
            self.player_win_streak += 1
            self.ai_win_streak = 0
            if self.player_win_streak >= self.games_for_adjustment:
                self.current_adjustment = min(1.0, self.current_adjustment + 0.2)
        else:
            self.ai_win_streak += 1
            self.player_win_streak = 0
            if self.ai_win_streak >= self.games_for_adjustment:
                self.current_adjustment = max(-1.0, self.current_adjustment - 0.2)

    def get_effective_mistake_chance(self, base_chance: float) -> float:
        """Get adjusted mistake chance"""
        # Negative adjustment = harder (fewer mistakes)
        # Positive adjustment = easier (more mistakes)
        adjustment = self.current_adjustment * 0.2
        return max(0, min(1, base_chance + adjustment))


class Strategy(ABC, Generic[GameState, Move]):
    """
    Base class for AI strategies.

    Implement this to create game-specific AI logic.
    """

    @abstractmethod
    def get_possible_moves(self, state: GameState) -> List[Move]:
        """Get all possible moves from current state"""
        pass

    @abstractmethod
    def evaluate_state(self, state: GameState) -> float:
        """Evaluate how good a state is for the AI (higher = better)"""
        pass

    @abstractmethod
    def apply_move(self, state: GameState, move: Move) -> GameState:
        """Apply a move to get new state"""
        pass

    @abstractmethod
    def is_terminal(self, state: GameState) -> bool:
        """Check if game is over"""
        pass

    def score_move(self, state: GameState, move: Move) -> float:
        """Score a move (default: evaluate resulting state)"""
        new_state = self.apply_move(state, move)
        return self.evaluate_state(new_state)


class RandomStrategy(Strategy[GameState, Move]):
    """Strategy that picks random moves"""

    def __init__(self, get_moves: Callable, evaluate: Callable = None,
                 apply: Callable = None, is_terminal: Callable = None):
        self._get_moves = get_moves
        self._evaluate = evaluate or (lambda s: 0.0)
        self._apply = apply or (lambda s, m: s)
        self._is_terminal = is_terminal or (lambda s: False)

    def get_possible_moves(self, state: GameState) -> List[Move]:
        return self._get_moves(state)

    def evaluate_state(self, state: GameState) -> float:
        return self._evaluate(state)

    def apply_move(self, state: GameState, move: Move) -> GameState:
        return self._apply(state, move)

    def is_terminal(self, state: GameState) -> bool:
        return self._is_terminal(state)


class AIOpponent:
    """
    Configurable AI opponent for games.

    Works with any game that provides a Strategy implementation.
    """

    def __init__(self, game_id: str, config: Optional[AIConfig] = None,
                 strategy: Optional[Strategy] = None):
        self.game_id = game_id
        self.config = config or AIConfig()
        self.strategy = strategy

        self.games_played = 0
        self.games_won = 0
        self.player_patterns = PlayerPattern()
        self.adaptive_difficulty = AdaptiveDifficulty(base_difficulty=self.config.difficulty)

        self._last_move_time = 0.0
        self._move_history: List[Any] = []
        self._player_move_history: List[Any] = []
        self._last_player_move_time = 0.0

        # Adjust mistake chance based on difficulty
        self._setup_difficulty()

        logger.info(f"AI Opponent created for {game_id} ({self.config.difficulty.value})")

    def _setup_difficulty(self):
        """Configure AI based on difficulty level"""
        difficulty_settings = {
            Difficulty.EASY: {"mistake_chance": 0.4, "think_time": 0.5},
            Difficulty.MEDIUM: {"mistake_chance": 0.15, "think_time": 1.0},
            Difficulty.HARD: {"mistake_chance": 0.05, "think_time": 1.5},
            Difficulty.NIGHTMARE: {"mistake_chance": 0.0, "think_time": 2.0},
        }
        settings = difficulty_settings.get(self.config.difficulty, {})
        self.config.mistake_chance = settings.get("mistake_chance", 0.15)
        self.config.think_time_seconds = settings.get("think_time", 1.0)

    def get_move(self, game_state: Any, possible_moves: Optional[List[Any]] = None) -> Any:
        """
        Get the AI's move for the current game state.

        Args:
            game_state: Current state of the game
            possible_moves: Optional list of valid moves (if strategy not set)

        Returns:
            The chosen move
        """
        start_time = time.time()

        # Get possible moves
        if possible_moves is None:
            if self.strategy:
                possible_moves = self.strategy.get_possible_moves(game_state)
            else:
                raise ValueError("Either provide possible_moves or set a strategy")

        if not possible_moves:
            return None

        # Choose move based on strategy
        if self.strategy and random.random() > self.config.mistake_chance:
            move = self._choose_strategic_move(game_state, possible_moves)
        else:
            move = self._choose_fallback_move(possible_moves)

        # Apply personality adjustments
        move = self._apply_personality(game_state, possible_moves, move)

        # Simulate thinking time
        elapsed = time.time() - start_time
        if elapsed < self.config.think_time_seconds:
            time.sleep(self.config.think_time_seconds - elapsed)

        self._move_history.append(move)
        self._last_move_time = time.time()

        return move

    def _choose_strategic_move(self, state: Any, moves: List[Any]) -> Any:
        """Choose move using strategy"""
        scored_moves = []

        for move in moves:
            score = self.strategy.score_move(state, move)
            scored_moves.append((move, score))

        # Sort by score (best first)
        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # Pick from top moves based on difficulty
        if self.config.difficulty == Difficulty.NIGHTMARE:
            return scored_moves[0][0]  # Always best
        elif self.config.difficulty == Difficulty.HARD:
            # Pick from top 2
            top_n = min(2, len(scored_moves))
            return random.choice(scored_moves[:top_n])[0]
        elif self.config.difficulty == Difficulty.MEDIUM:
            # Pick from top 3
            top_n = min(3, len(scored_moves))
            return random.choice(scored_moves[:top_n])[0]
        else:
            # Pick from top half
            top_n = max(1, len(scored_moves) // 2)
            return random.choice(scored_moves[:top_n])[0]

    def _choose_fallback_move(self, moves: List[Any]) -> Any:
        """Choose a random move (used when making mistakes)"""
        return random.choice(moves)

    def _apply_personality(self, state: Any, moves: List[Any],
                          current_choice: Any) -> Any:
        """Adjust move based on AI personality"""
        if self.config.personality == Personality.CHAOTIC:
            # 30% chance to pick random move instead
            if random.random() < 0.3:
                return random.choice(moves)

        # Other personalities would need game-specific logic
        # to identify "aggressive" vs "defensive" moves

        return current_choice

    def record_result(self, won: bool, game_data: Optional[Dict[str, Any]] = None):
        """
        Record the result of a game for learning.

        Args:
            won: Whether the AI won
            game_data: Optional additional game data
        """
        self.games_played += 1
        if won:
            self.games_won += 1

        if self.config.learning_enabled and game_data:
            self._learn_from_game(game_data)

        logger.info(f"Game recorded: {'Win' if won else 'Loss'} "
                   f"({self.games_won}/{self.games_played})")

    def _learn_from_game(self, game_data: Dict[str, Any]):
        """Learn patterns from game data"""
        self.player_patterns.games_analyzed += 1

        # Track opening moves
        if "player_moves" in game_data:
            moves = game_data["player_moves"]
            if moves:
                self.player_patterns.opening_moves.append(moves[0])
                # Store full sequence for pattern analysis
                self.player_patterns.move_sequences.append(moves)
                # Keep only last 50 games
                if len(self.player_patterns.move_sequences) > 50:
                    self.player_patterns.move_sequences.pop(0)

        # Track strategies
        if "player_strategy" in game_data:
            strategy = game_data["player_strategy"]
            self.player_patterns.preferred_strategies[strategy] = \
                self.player_patterns.preferred_strategies.get(strategy, 0) + 1

        # Track risk tolerance from aggressive/conservative plays
        if "risky_moves" in game_data and "safe_moves" in game_data:
            risky = game_data["risky_moves"]
            safe = game_data["safe_moves"]
            total = risky + safe
            if total > 0:
                new_tolerance = risky / total
                # Exponential moving average
                alpha = 0.3
                self.player_patterns.risk_tolerance = (
                    alpha * new_tolerance +
                    (1 - alpha) * self.player_patterns.risk_tolerance
                )

    def predict_player_move(self, current_state: Any,
                           context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """
        Predict what move the player is likely to make based on patterns.

        Args:
            current_state: Current game state
            context: Additional context (turn number, game phase, etc.)

        Returns:
            Predicted move or None if not enough data
        """
        if self.player_patterns.games_analyzed < 3:
            return None  # Not enough data

        predictions = {}

        # Check if this matches an opening pattern
        turn = context.get("turn", 0) if context else 0
        if turn < 3:
            # Look for common opening moves
            for seq in self.player_patterns.move_sequences:
                if turn < len(seq):
                    move = seq[turn]
                    predictions[str(move)] = predictions.get(str(move), 0) + 1

        # Weight by risk tolerance if move categories are known
        if context and "risky_moves" in context and "safe_moves" in context:
            risk = self.player_patterns.risk_tolerance
            if risk > 0.6:  # Player is aggressive
                # Weight risky moves higher
                for move in context["risky_moves"]:
                    predictions[str(move)] = predictions.get(str(move), 0) + 2
            elif risk < 0.4:  # Player is conservative
                for move in context["safe_moves"]:
                    predictions[str(move)] = predictions.get(str(move), 0) + 2

        if not predictions:
            return None

        # Return most likely move
        return max(predictions.keys(), key=lambda m: predictions[m])

    def record_player_move(self, move: Any, reaction_time: Optional[float] = None):
        """Record a player's move for pattern learning"""
        self._player_move_history.append(move)

        if reaction_time is not None:
            self.player_patterns.reaction_times.append(reaction_time)
            # Keep only recent times
            if len(self.player_patterns.reaction_times) > 100:
                self.player_patterns.reaction_times.pop(0)

    def get_player_average_reaction_time(self) -> Optional[float]:
        """Get player's average reaction time"""
        times = self.player_patterns.reaction_times
        if not times:
            return None
        return sum(times) / len(times)

    def get_taunt(self, situation: str = "general") -> Optional[str]:
        """Get a taunt message for the current situation"""
        if not self.config.taunt_enabled:
            return None

        taunts = {
            "general": [
                "Interesting move...",
                "Let me think about this.",
                "Hmm, I see what you're doing.",
            ],
            "winning": [
                "I believe I have the advantage.",
                "This is going well for me.",
                "Your defeat approaches.",
            ],
            "losing": [
                "A minor setback.",
                "You're better than I expected.",
                "I must reconsider my approach.",
            ],
            "player_mistake": [
                "Are you sure about that?",
                "Interesting choice...",
                "That could be problematic for you.",
            ],
        }

        messages = taunts.get(situation, taunts["general"])
        return random.choice(messages)

    @property
    def win_rate(self) -> float:
        """Get AI's win rate"""
        if self.games_played == 0:
            return 0.0
        return self.games_won / self.games_played


# === Common AI Algorithms ===

def minimax(strategy: Strategy, state: Any, depth: int,
            maximizing: bool, alpha: float = float('-inf'),
            beta: float = float('inf')) -> tuple:
    """
    Minimax algorithm with alpha-beta pruning.

    Args:
        strategy: Game strategy implementation
        state: Current game state
        depth: Search depth
        maximizing: True if maximizing player's turn
        alpha: Alpha value for pruning
        beta: Beta value for pruning

    Returns:
        Tuple of (best_score, best_move)
    """
    if depth == 0 or strategy.is_terminal(state):
        return strategy.evaluate_state(state), None

    moves = strategy.get_possible_moves(state)
    if not moves:
        return strategy.evaluate_state(state), None

    best_move = moves[0]

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_state = strategy.apply_move(state, move)
            eval_score, _ = minimax(strategy, new_state, depth - 1,
                                   False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_state = strategy.apply_move(state, move)
            eval_score, _ = minimax(strategy, new_state, depth - 1,
                                   True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def monte_carlo_search(strategy: Strategy, state: Any,
                       simulations: int = 100) -> Any:
    """
    Monte Carlo Tree Search for move selection.

    Args:
        strategy: Game strategy implementation
        state: Current game state
        simulations: Number of random simulations per move

    Returns:
        Best move based on simulation results
    """
    moves = strategy.get_possible_moves(state)
    if not moves:
        return None

    move_scores = {}

    for move in moves:
        scores = []
        for _ in range(simulations):
            sim_state = strategy.apply_move(state, move)

            # Random playout
            while not strategy.is_terminal(sim_state):
                sim_moves = strategy.get_possible_moves(sim_state)
                if not sim_moves:
                    break
                sim_state = strategy.apply_move(sim_state,
                                                random.choice(sim_moves))

            scores.append(strategy.evaluate_state(sim_state))

        move_scores[move] = sum(scores) / len(scores) if scores else 0

    # Return move with highest average score
    return max(move_scores.keys(), key=lambda m: move_scores[m])


# === Factory Functions ===

def create_opponent(game_id: str, difficulty: str = "medium",
                   personality: str = "balanced") -> AIOpponent:
    """
    Create an AI opponent with specified settings.

    Args:
        game_id: Identifier for the game
        difficulty: easy/medium/hard/nightmare
        personality: aggressive/defensive/balanced/chaotic/analytical/tricky

    Returns:
        Configured AIOpponent instance
    """
    config = AIConfig(
        difficulty=Difficulty(difficulty),
        personality=Personality(personality)
    )
    return AIOpponent(game_id, config)


def create_easy_opponent(game_id: str) -> AIOpponent:
    """Create an easy AI opponent"""
    return create_opponent(game_id, "easy", "balanced")


def create_hard_opponent(game_id: str) -> AIOpponent:
    """Create a hard AI opponent"""
    return create_opponent(game_id, "hard", "analytical")


if __name__ == '__main__':
    print("AI Opponent Demo")
    print("=" * 40)

    # Demo with simple number guessing
    class NumberStrategy(Strategy):
        def __init__(self, target: int, range_max: int = 100):
            self.target = target
            self.range_max = range_max
            self.low = 1
            self.high = range_max

        def get_possible_moves(self, state):
            return list(range(self.low, self.high + 1))

        def evaluate_state(self, state):
            # Closer to target is better (negative distance)
            return -abs(state - self.target)

        def apply_move(self, state, move):
            return move

        def is_terminal(self, state):
            return state == self.target

    target = random.randint(1, 100)
    print(f"Secret target: {target}")

    ai = AIOpponent("number_guess", AIConfig(difficulty=Difficulty.HARD))
    ai.strategy = NumberStrategy(target)

    for turn in range(1, 8):
        guess = ai.get_move(None)
        print(f"Turn {turn}: AI guesses {guess}", end=" ")

        if guess == target:
            print("- Correct!")
            break
        elif guess < target:
            print("- Too low")
            ai.strategy.low = guess + 1
        else:
            print("- Too high")
            ai.strategy.high = guess - 1
    else:
        print("AI failed to guess in time!")

    ai.record_result(won=(guess == target))
    print(f"\nAI Win Rate: {ai.win_rate * 100:.1f}%")
