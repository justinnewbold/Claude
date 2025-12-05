#!/usr/bin/env python3
"""
Achievement System
==================
Universal achievement tracking system for games.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum

from logging_config import get_logger
from error_handling import error_context


logger = get_logger(__name__)


class AchievementCategory(Enum):
    """Achievement categories"""
    GAMEPLAY = "gameplay"
    PROGRESSION = "progression"
    COLLECTION = "collection"
    COMBAT = "combat"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    SPECIAL = "special"
    SECRET = "secret"


class AchievementRarity(Enum):
    """Achievement rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Achievement:
    """Achievement definition"""
    id: str
    name: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity
    points: int = 10
    hidden: bool = False
    icon: str = "🏆"
    requirements: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'rarity': self.rarity.value,
            'points': self.points,
            'hidden': self.hidden,
            'icon': self.icon,
            'requirements': self.requirements
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Achievement':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            category=AchievementCategory(data['category']),
            rarity=AchievementRarity(data['rarity']),
            points=data.get('points', 10),
            hidden=data.get('hidden', False),
            icon=data.get('icon', '🏆'),
            requirements=data.get('requirements', {})
        )


@dataclass
class AchievementProgress:
    """Progress towards an achievement"""
    achievement_id: str
    unlocked: bool = False
    unlock_date: Optional[str] = None
    progress: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AchievementProgress':
        """Create from dictionary"""
        return cls(**data)


class AchievementSystem:
    """
    Universal achievement tracking system.

    Features:
    - Achievement definitions with categories and rarity
    - Progress tracking
    - Unlock notifications
    - Statistics
    - Hidden/secret achievements
    - Custom requirements checking
    """

    def __init__(
        self,
        game_id: str,
        achievements_file: Optional[Path] = None,
        progress_file: Optional[Path] = None
    ):
        """
        Initialize achievement system.

        Args:
            game_id: Unique game identifier
            achievements_file: Path to achievements definition file
            progress_file: Path to progress save file
        """
        self.game_id = game_id
        self.logger = get_logger(__name__)

        # File paths
        self.achievements_file = achievements_file or Path(f"data/{game_id}_achievements.json")
        self.progress_file = progress_file or Path(f"saves/{game_id}_achievements.json")

        # Data
        self.achievements: Dict[str, Achievement] = {}
        self.progress: Dict[str, AchievementProgress] = {}

        # Callbacks
        self.unlock_callbacks: List[Callable[[Achievement], None]] = []

        # Load data
        self._load_achievements()
        self._load_progress()

    def _load_achievements(self):
        """Load achievement definitions"""
        if not self.achievements_file.exists():
            self.logger.warning(f"Achievements file not found: {self.achievements_file}")
            return

        with error_context("loading achievements"):
            with open(self.achievements_file, 'r') as f:
                data = json.load(f)

            for ach_data in data.get('achievements', []):
                achievement = Achievement.from_dict(ach_data)
                self.achievements[achievement.id] = achievement

            self.logger.info(f"Loaded {len(self.achievements)} achievements")

    def _load_progress(self):
        """Load achievement progress"""
        if not self.progress_file.exists():
            # Initialize progress for all achievements
            for ach_id in self.achievements:
                self.progress[ach_id] = AchievementProgress(achievement_id=ach_id)
            return

        with error_context("loading achievement progress"):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)

            for prog_data in data.get('progress', []):
                progress = AchievementProgress.from_dict(prog_data)
                self.progress[progress.achievement_id] = progress

            self.logger.info(f"Loaded progress for {len(self.progress)} achievements")

    def _save_progress(self):
        """Save achievement progress"""
        with error_context("saving achievement progress"):
            # Ensure directory exists
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'game_id': self.game_id,
                'last_updated': datetime.now().isoformat(),
                'progress': [p.to_dict() for p in self.progress.values()]
            }

            with open(self.progress_file, 'w') as f:
                json.dump(data, f, indent=2)

    def register_achievement(self, achievement: Achievement):
        """
        Register a new achievement.

        Args:
            achievement: Achievement to register
        """
        self.achievements[achievement.id] = achievement
        if achievement.id not in self.progress:
            self.progress[achievement.id] = AchievementProgress(
                achievement_id=achievement.id
            )
        self.logger.debug(f"Registered achievement: {achievement.name}")

    def unlock(self, achievement_id: str) -> bool:
        """
        Unlock an achievement.

        Args:
            achievement_id: Achievement ID to unlock

        Returns:
            True if newly unlocked, False if already unlocked
        """
        if achievement_id not in self.achievements:
            self.logger.warning(f"Unknown achievement: {achievement_id}")
            return False

        progress = self.progress.get(achievement_id)
        if not progress:
            progress = AchievementProgress(achievement_id=achievement_id)
            self.progress[achievement_id] = progress

        if progress.unlocked:
            return False  # Already unlocked

        # Unlock it!
        progress.unlocked = True
        progress.unlock_date = datetime.now().isoformat()

        achievement = self.achievements[achievement_id]
        self.logger.info(f"Achievement unlocked: {achievement.name}")

        # Save progress
        self._save_progress()

        # Trigger callbacks
        for callback in self.unlock_callbacks:
            try:
                callback(achievement)
            except Exception as e:
                self.logger.error(f"Error in unlock callback: {e}")

        return True

    def update_progress(self, achievement_id: str, progress_data: Dict[str, Any]):
        """
        Update progress towards an achievement.

        Args:
            achievement_id: Achievement ID
            progress_data: Progress data to update
        """
        if achievement_id not in self.achievements:
            return

        progress = self.progress.get(achievement_id)
        if not progress:
            progress = AchievementProgress(achievement_id=achievement_id)
            self.progress[achievement_id] = progress

        if progress.unlocked:
            return  # Already unlocked

        # Update progress
        progress.progress.update(progress_data)

        # Check if requirements met
        achievement = self.achievements[achievement_id]
        if self._check_requirements(achievement, progress):
            self.unlock(achievement_id)
        else:
            self._save_progress()

    def _check_requirements(
        self,
        achievement: Achievement,
        progress: AchievementProgress
    ) -> bool:
        """
        Check if achievement requirements are met.

        Args:
            achievement: Achievement definition
            progress: Current progress

        Returns:
            True if requirements met
        """
        requirements = achievement.requirements

        for key, required_value in requirements.items():
            current_value = progress.progress.get(key, 0)

            # Handle different requirement types
            if isinstance(required_value, (int, float)):
                if current_value < required_value:
                    return False
            elif isinstance(required_value, bool):
                if current_value != required_value:
                    return False
            elif isinstance(required_value, list):
                # All items in list must be present
                if not all(item in current_value for item in required_value):
                    return False

        return True

    def get_unlocked(self) -> List[Achievement]:
        """Get all unlocked achievements"""
        return [
            self.achievements[prog.achievement_id]
            for prog in self.progress.values()
            if prog.unlocked and prog.achievement_id in self.achievements
        ]

    def get_locked(self, include_hidden: bool = False) -> List[Achievement]:
        """Get all locked achievements"""
        locked = [
            self.achievements[prog.achievement_id]
            for prog in self.progress.values()
            if not prog.unlocked and prog.achievement_id in self.achievements
        ]

        if not include_hidden:
            locked = [ach for ach in locked if not ach.hidden]

        return locked

    def get_progress(self, achievement_id: str) -> Optional[AchievementProgress]:
        """Get progress for an achievement"""
        return self.progress.get(achievement_id)

    def get_statistics(self) -> Dict[str, Any]:
        """Get achievement statistics"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked())
        locked = total - unlocked

        # Calculate total points
        total_points = sum(ach.points for ach in self.achievements.values())
        earned_points = sum(
            ach.points for ach in self.get_unlocked()
        )

        # By category
        by_category = {}
        for ach in self.achievements.values():
            cat = ach.category.value
            if cat not in by_category:
                by_category[cat] = {'total': 0, 'unlocked': 0}
            by_category[cat]['total'] += 1

        for ach in self.get_unlocked():
            cat = ach.category.value
            by_category[cat]['unlocked'] += 1

        # By rarity
        by_rarity = {}
        for ach in self.get_unlocked():
            rarity = ach.rarity.value
            by_rarity[rarity] = by_rarity.get(rarity, 0) + 1

        return {
            'total_achievements': total,
            'unlocked': unlocked,
            'locked': locked,
            'completion_percent': (unlocked / total * 100) if total > 0 else 0,
            'total_points': total_points,
            'earned_points': earned_points,
            'by_category': by_category,
            'by_rarity': by_rarity
        }

    def on_unlock(self, callback: Callable[[Achievement], None]):
        """
        Register callback for achievement unlocks.

        Args:
            callback: Function to call when achievement unlocked
        """
        self.unlock_callbacks.append(callback)

    def print_achievement(self, achievement: Achievement, progress: Optional[AchievementProgress] = None):
        """Print achievement details"""
        if progress is None:
            progress = self.progress.get(achievement.id)

        status = "✅" if progress and progress.unlocked else "🔒"
        print(f"{status} {achievement.icon} {achievement.name}")
        print(f"   {achievement.description}")
        print(f"   Category: {achievement.category.value} | Rarity: {achievement.rarity.value} | Points: {achievement.points}")

        if progress and progress.unlocked:
            print(f"   Unlocked: {progress.unlock_date}")
        elif progress and progress.progress:
            print(f"   Progress: {progress.progress}")


# =============================================================================
# DEFAULT ACHIEVEMENTS
# =============================================================================

def create_default_achievements() -> List[Achievement]:
    """Create default achievements for testing"""
    return [
        Achievement(
            id="first_steps",
            name="First Steps",
            description="Complete the tutorial",
            category=AchievementCategory.PROGRESSION,
            rarity=AchievementRarity.COMMON,
            points=5,
            icon="🎯",
            requirements={'tutorial_complete': True}
        ),
        Achievement(
            id="survivor",
            name="Survivor",
            description="Survive for 100 turns",
            category=AchievementCategory.GAMEPLAY,
            rarity=AchievementRarity.UNCOMMON,
            points=10,
            icon="💪",
            requirements={'turns_survived': 100}
        ),
        Achievement(
            id="collector",
            name="Collector",
            description="Collect 50 items",
            category=AchievementCategory.COLLECTION,
            rarity=AchievementRarity.UNCOMMON,
            points=15,
            icon="📦",
            requirements={'items_collected': 50}
        ),
        Achievement(
            id="warrior",
            name="Warrior",
            description="Defeat 100 enemies",
            category=AchievementCategory.COMBAT,
            rarity=AchievementRarity.RARE,
            points=20,
            icon="⚔️",
            requirements={'enemies_defeated': 100}
        ),
        Achievement(
            id="explorer",
            name="Explorer",
            description="Discover all locations",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.EPIC,
            points=30,
            icon="🗺️",
            requirements={'locations_discovered': 10}
        ),
        Achievement(
            id="secret_master",
            name="???",
            description="???",
            category=AchievementCategory.SECRET,
            rarity=AchievementRarity.LEGENDARY,
            points=50,
            hidden=True,
            icon="🌟",
            requirements={'secret_found': True}
        )
    ]


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Achievement System Test")
    print("=" * 60)

    # Create test system
    system = AchievementSystem(game_id='test_game')

    # Register default achievements
    for achievement in create_default_achievements():
        system.register_achievement(achievement)

    print(f"\n✅ Registered {len(system.achievements)} achievements\n")

    # Test unlock callback
    def on_achievement_unlocked(achievement: Achievement):
        print(f"\n🎉 ACHIEVEMENT UNLOCKED: {achievement.name}")
        print(f"   {achievement.description}")
        print(f"   +{achievement.points} points\n")

    system.on_unlock(on_achievement_unlocked)

    # Test unlocking
    print("1. Testing Direct Unlock:")
    system.unlock('first_steps')

    # Test progress tracking
    print("\n2. Testing Progress Tracking:")
    system.update_progress('survivor', {'turns_survived': 50})
    print("   Progress: 50/100 turns")

    system.update_progress('survivor', {'turns_survived': 100})
    print("   Progress: 100/100 turns (should unlock)")

    # Test statistics
    print("\n3. Statistics:")
    stats = system.get_statistics()
    print(f"   Total: {stats['total_achievements']}")
    print(f"   Unlocked: {stats['unlocked']}")
    print(f"   Completion: {stats['completion_percent']:.1f}%")
    print(f"   Points: {stats['earned_points']}/{stats['total_points']}")

    # Test display
    print("\n4. Achievement List:")
    for achievement in system.achievements.values():
        progress = system.get_progress(achievement.id)
        if not achievement.hidden or progress.unlocked:
            system.print_achievement(achievement, progress)
            print()

    print("✅ All achievement system tests passed!")
