#!/usr/bin/env python3
"""
Cross-Game State Persistence
=============================
Unified state management for tracking progress, high scores, achievements,
and play time across all games in the collection.

Features:
- High scores for all games
- Play time tracking
- Achievement unlocks
- Game-specific settings
- Auto-save on exit
"""

import json
import atexit
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, field, asdict
from platform_utils import get_app_data_dir
from logging_config import get_logger

logger = get_logger(__name__)

# State file location
STATE_FILE = get_app_data_dir("vault13") / "game_state.json"


@dataclass
class GameStats:
    """Statistics for a single game"""
    play_count: int = 0
    total_play_time_seconds: float = 0.0
    high_score: int = 0
    best_time_seconds: Optional[float] = None
    last_played: Optional[str] = None
    wins: int = 0
    losses: int = 0
    achievements: List[str] = field(default_factory=list)
    custom_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Achievement:
    """An unlockable achievement"""
    id: str
    name: str
    description: str
    game_id: str
    unlocked: bool = False
    unlocked_at: Optional[str] = None
    icon: str = "🏆"


class GameStateManager:
    """
    Manages persistent game state across all games.

    Usage:
        state = GameStateManager()

        # Record a game session
        state.start_session("echo_chambers")
        # ... play game ...
        state.end_session("echo_chambers", score=1500, won=True)

        # Get high score
        high = state.get_high_score("echo_chambers")

        # Unlock achievement
        state.unlock_achievement("echo_chambers", "first_timeline", "First Timeline", "Created your first timeline")
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern - only one state manager exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.game_stats: Dict[str, GameStats] = {}
        self.global_achievements: List[Achievement] = []
        self.total_play_time_seconds: float = 0.0
        self.first_played: Optional[str] = None
        self.last_played: Optional[str] = None
        self._current_sessions: Dict[str, datetime] = {}

        self._load_state()

        # Register auto-save on exit
        atexit.register(self._save_state)

        logger.info("GameStateManager initialized")

    def _load_state(self):
        """Load state from file"""
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Load game stats
                for game_id, stats_data in data.get('game_stats', {}).items():
                    self.game_stats[game_id] = GameStats(**stats_data)

                # Load global data
                self.total_play_time_seconds = data.get('total_play_time_seconds', 0.0)
                self.first_played = data.get('first_played')
                self.last_played = data.get('last_played')

                # Load achievements
                for ach_data in data.get('global_achievements', []):
                    self.global_achievements.append(Achievement(**ach_data))

                logger.info(f"Loaded state: {len(self.game_stats)} games, {len(self.global_achievements)} achievements")
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted state file, starting fresh: {e}")
        except Exception as e:
            logger.warning(f"Could not load state: {e}")

    def _save_state(self):
        """Save state to file"""
        try:
            # Ensure directory exists
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'game_stats': {
                    game_id: asdict(stats)
                    for game_id, stats in self.game_stats.items()
                },
                'global_achievements': [asdict(ach) for ach in self.global_achievements],
                'total_play_time_seconds': self.total_play_time_seconds,
                'first_played': self.first_played,
                'last_played': self.last_played,
            }

            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            logger.info("State saved successfully")
        except Exception as e:
            logger.error(f"Could not save state: {e}")

    def _get_or_create_stats(self, game_id: str) -> GameStats:
        """Get stats for a game, creating if necessary"""
        if game_id not in self.game_stats:
            self.game_stats[game_id] = GameStats()
        return self.game_stats[game_id]

    # === Session Management ===

    def start_session(self, game_id: str):
        """Start tracking a game session"""
        self._current_sessions[game_id] = datetime.now()

        stats = self._get_or_create_stats(game_id)
        stats.play_count += 1
        stats.last_played = datetime.now().isoformat()

        if not self.first_played:
            self.first_played = datetime.now().isoformat()
        self.last_played = datetime.now().isoformat()

        logger.info(f"Started session for {game_id}")

    def end_session(self, game_id: str, score: Optional[int] = None,
                   won: Optional[bool] = None, time_seconds: Optional[float] = None):
        """End a game session and record stats"""
        stats = self._get_or_create_stats(game_id)

        # Calculate play time from session
        if game_id in self._current_sessions:
            session_start = self._current_sessions.pop(game_id)
            duration = (datetime.now() - session_start).total_seconds()
            stats.total_play_time_seconds += duration
            self.total_play_time_seconds += duration
        elif time_seconds is not None:
            stats.total_play_time_seconds += time_seconds
            self.total_play_time_seconds += time_seconds

        # Record score
        if score is not None and score > stats.high_score:
            stats.high_score = score
            logger.info(f"New high score for {game_id}: {score}")

        # Record win/loss
        if won is not None:
            if won:
                stats.wins += 1
            else:
                stats.losses += 1

        # Record best time
        if time_seconds is not None:
            if stats.best_time_seconds is None or time_seconds < stats.best_time_seconds:
                stats.best_time_seconds = time_seconds

        self._save_state()
        logger.info(f"Ended session for {game_id}")

    # === Score Management ===

    def get_high_score(self, game_id: str) -> int:
        """Get high score for a game"""
        return self._get_or_create_stats(game_id).high_score

    def set_high_score(self, game_id: str, score: int) -> bool:
        """Set high score if it's higher than current. Returns True if new record."""
        stats = self._get_or_create_stats(game_id)
        if score > stats.high_score:
            stats.high_score = score
            self._save_state()
            return True
        return False

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top games by high score"""
        games = [
            {'game_id': game_id, 'high_score': stats.high_score, 'play_count': stats.play_count}
            for game_id, stats in self.game_stats.items()
            if stats.high_score > 0
        ]
        return sorted(games, key=lambda x: x['high_score'], reverse=True)[:limit]

    # === Time Tracking ===

    def get_play_time(self, game_id: str) -> timedelta:
        """Get total play time for a game"""
        seconds = self._get_or_create_stats(game_id).total_play_time_seconds
        return timedelta(seconds=seconds)

    def get_total_play_time(self) -> timedelta:
        """Get total play time across all games"""
        return timedelta(seconds=self.total_play_time_seconds)

    def format_play_time(self, td: timedelta) -> str:
        """Format a timedelta as human-readable string"""
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    # === Achievement Management ===

    def unlock_achievement(self, game_id: str, ach_id: str, name: str,
                          description: str, icon: str = "🏆") -> bool:
        """Unlock an achievement. Returns True if newly unlocked."""
        stats = self._get_or_create_stats(game_id)

        full_id = f"{game_id}:{ach_id}"

        # Check if already unlocked
        if full_id in stats.achievements:
            return False

        # Add to game stats
        stats.achievements.append(full_id)

        # Add to global achievements
        self.global_achievements.append(Achievement(
            id=full_id,
            name=name,
            description=description,
            game_id=game_id,
            unlocked=True,
            unlocked_at=datetime.now().isoformat(),
            icon=icon
        ))

        self._save_state()
        logger.info(f"Achievement unlocked: {name} ({full_id})")
        return True

    def has_achievement(self, game_id: str, ach_id: str) -> bool:
        """Check if an achievement is unlocked"""
        stats = self._get_or_create_stats(game_id)
        return f"{game_id}:{ach_id}" in stats.achievements

    def get_achievements(self, game_id: Optional[str] = None) -> List[Achievement]:
        """Get achievements, optionally filtered by game"""
        if game_id:
            return [a for a in self.global_achievements if a.game_id == game_id]
        return self.global_achievements

    # === Custom Data ===

    def set_custom_data(self, game_id: str, key: str, value: Any):
        """Store custom game-specific data"""
        stats = self._get_or_create_stats(game_id)
        stats.custom_data[key] = value
        self._save_state()

    def get_custom_data(self, game_id: str, key: str, default: Any = None) -> Any:
        """Get custom game-specific data"""
        stats = self._get_or_create_stats(game_id)
        return stats.custom_data.get(key, default)

    # === Statistics ===

    def get_stats_summary(self) -> Dict[str, Any]:
        """Get summary statistics across all games"""
        total_plays = sum(s.play_count for s in self.game_stats.values())
        total_wins = sum(s.wins for s in self.game_stats.values())
        total_losses = sum(s.losses for s in self.game_stats.values())

        return {
            'total_games_played': len(self.game_stats),
            'total_sessions': total_plays,
            'total_play_time': self.format_play_time(self.get_total_play_time()),
            'total_wins': total_wins,
            'total_losses': total_losses,
            'win_rate': total_wins / (total_wins + total_losses) if (total_wins + total_losses) > 0 else 0,
            'total_achievements': len(self.global_achievements),
            'first_played': self.first_played,
            'last_played': self.last_played,
        }


# Global state manager instance
_state_manager: Optional[GameStateManager] = None


def get_state_manager() -> GameStateManager:
    """Get the global state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = GameStateManager()
    return _state_manager


# Convenience functions
def start_game_session(game_id: str):
    """Start tracking a game session"""
    get_state_manager().start_session(game_id)


def end_game_session(game_id: str, **kwargs):
    """End a game session"""
    get_state_manager().end_session(game_id, **kwargs)


def record_high_score(game_id: str, score: int) -> bool:
    """Record a high score"""
    return get_state_manager().set_high_score(game_id, score)


def unlock_achievement(game_id: str, ach_id: str, name: str, description: str, icon: str = "🏆") -> bool:
    """Unlock an achievement"""
    return get_state_manager().unlock_achievement(game_id, ach_id, name, description, icon)


if __name__ == '__main__':
    # Demo/test
    print("Game State Manager Demo")
    print("=" * 40)

    state = get_state_manager()

    # Simulate some game sessions
    state.start_session("demo_game")
    state.end_session("demo_game", score=1500, won=True)

    state.start_session("demo_game")
    state.end_session("demo_game", score=2000, won=True)

    # Unlock an achievement
    state.unlock_achievement("demo_game", "first_win", "First Victory", "Win your first game")

    # Show stats
    print("\nStats Summary:")
    for key, value in state.get_stats_summary().items():
        print(f"  {key}: {value}")

    print(f"\nHigh Score: {state.get_high_score('demo_game')}")
    print(f"Play Time: {state.format_play_time(state.get_play_time('demo_game'))}")
    print(f"Achievements: {len(state.get_achievements('demo_game'))}")
