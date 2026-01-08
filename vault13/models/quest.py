"""
VAULT 13: Quest and Expedition Models
Quest, expedition, and objective data structures.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from vault13.constants import QuestStatus, ObjectiveType, FactionType


@dataclass
class QuestStep:
    """Individual step in a quest"""
    description: str
    requirements: Dict[str, Any] = field(default_factory=dict)
    completed: bool = False


@dataclass
class Quest:
    """Procedural quest with branching paths"""
    quest_id: str
    title: str
    description: str
    quest_type: str  # "resource", "dweller", "exploration", "faction", "research"
    steps: List[QuestStep] = field(default_factory=list)
    rewards: Dict[str, int] = field(default_factory=dict)
    current_step: int = 0
    turns_remaining: int = 20
    completed: bool = False
    failed: bool = False
    branch_choice: Optional[str] = None
    created_day: int = 1
    faction: Optional[FactionType] = None

    def get_current_step_text(self) -> str:
        """Get current step description"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step].description
        return "Quest completed!"

    def advance_step(self):
        """Move to next step"""
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.completed = True

    def is_expired(self) -> bool:
        """Check if quest has expired"""
        return self.turns_remaining <= 0 and not self.completed


@dataclass
class ExpeditionEncounter:
    """Event during expedition"""
    encounter_type: str  # "combat", "loot", "choice", "trap", "discovery"
    description: str
    choices: List[str] = field(default_factory=list)
    outcomes: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class Expedition:
    """Basic wasteland expedition"""
    dweller_name: str
    destination: str
    duration: int
    return_day: int
    difficulty: int
    potential_loot: List[str] = field(default_factory=list)

    def is_complete(self, current_day: int) -> bool:
        """Check if expedition is complete"""
        return current_day >= self.return_day


@dataclass
class ActiveExpedition:
    """Full expedition with encounters"""
    expedition_id: str
    dweller_id: str
    location: str
    distance: int
    current_progress: int = 0
    encounters: List[ExpeditionEncounter] = field(default_factory=list)
    current_encounter: Optional[ExpeditionEncounter] = None
    loot_found: List[str] = field(default_factory=list)
    damage_taken: int = 0
    returning: bool = False

    def get_progress_percentage(self) -> float:
        """Get expedition progress as percentage"""
        if self.distance == 0:
            return 100.0
        return (self.current_progress / self.distance) * 100

    def is_complete(self) -> bool:
        """Check if expedition is complete"""
        return self.returning and self.current_progress <= 0


@dataclass
class VaultObjective:
    """Victory objective"""
    objective_type: ObjectiveType
    description: str
    requirements: Dict[str, Any] = field(default_factory=dict)
    progress: Dict[str, Any] = field(default_factory=dict)
    completed: bool = False

    def check_completion(self, game) -> bool:
        """Check if objective is completed"""
        if self.objective_type == ObjectiveType.UTOPIA:
            adults = [d for d in game.dwellers if not d.is_child]
            return all(d.happiness >= 90 for d in adults) and len(adults) >= 10
        elif self.objective_type == ObjectiveType.ECONOMIC:
            return game.resources.caps >= self.requirements.get("caps", 10000)
        elif self.objective_type == ObjectiveType.SURVIVAL:
            return game.day >= self.requirements.get("days", 100)
        elif self.objective_type == ObjectiveType.MILITARY:
            armed = sum(1 for d in game.dwellers if d.weapon and not d.is_child)
            return armed >= 15 and len(game.dwellers) >= 15
        elif self.objective_type == ObjectiveType.EXODUS:
            return self.progress.get("expeditions_completed", 0) >= 10
        elif self.objective_type == ObjectiveType.RESEARCH:
            return game.resources.research >= 5000
        return False

    def get_progress_text(self, game) -> str:
        """Get human-readable progress text"""
        if self.objective_type == ObjectiveType.SURVIVAL:
            return f"Day {game.day} / {self.requirements.get('days', 100)}"
        elif self.objective_type == ObjectiveType.ECONOMIC:
            return f"{game.resources.caps} / {self.requirements.get('caps', 10000)} caps"
        elif self.objective_type == ObjectiveType.RESEARCH:
            return f"{game.resources.research} / 5000 research"
        elif self.objective_type == ObjectiveType.UTOPIA:
            adults = [d for d in game.dwellers if not d.is_child]
            happy_count = sum(1 for d in adults if d.happiness >= 90)
            return f"{happy_count} / {len(adults)} happy dwellers"
        return "In progress..."
