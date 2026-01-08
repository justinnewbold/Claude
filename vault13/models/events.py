"""
VAULT 13: Event Models
Data structures for game events, challenges, and systems.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple


@dataclass
class RushAttempt:
    """Rush production attempt"""
    room_floor: int
    room_pos: int
    dwellers_assigned: int
    success_chance: float
    bonus_production: int
    risk_damage: int
    turns_remaining: int = 3
    completed: bool = False
    succeeded: bool = False


@dataclass
class EventChain:
    """Multi-turn story event"""
    chain_id: str
    title: str
    current_stage: int = 0
    stages: List[Dict[str, Any]] = field(default_factory=list)
    completed: bool = False
    player_choices: List[str] = field(default_factory=list)

    def get_current_stage(self) -> Optional[Dict[str, Any]]:
        """Get current stage data"""
        if self.current_stage < len(self.stages):
            return self.stages[self.current_stage]
        return None

    def advance(self, choice: str = None):
        """Advance to next stage"""
        if choice:
            self.player_choices.append(choice)
        self.current_stage += 1
        if self.current_stage >= len(self.stages):
            self.completed = True


@dataclass
class DailyChallenge:
    """Daily/weekly challenge"""
    challenge_id: str
    title: str
    description: str
    challenge_type: str  # "daily", "weekly"
    objective: str  # "build_rooms", "earn_caps", "complete_quests", etc.
    target: int
    progress: int = 0
    reward_caps: int = 0
    reward_research: int = 0
    expires_day: int = 0
    completed: bool = False

    def check_completion(self) -> bool:
        """Check if challenge is completed"""
        if self.progress >= self.target:
            self.completed = True
        return self.completed

    def get_progress_percentage(self) -> float:
        """Get progress as percentage"""
        return min(100, (self.progress / self.target) * 100) if self.target > 0 else 0


@dataclass
class Pet:
    """Vault pet companion"""
    pet_id: str
    name: str
    species: str  # "dog", "cat", "parrot", "rad_scorpion", "molerat"
    rarity: str  # "common", "rare", "legendary"
    bonus_type: str  # "luck", "happiness", "exploration", "combat", "production"
    bonus_value: int
    assigned_dweller: Optional[str] = None
    happiness: int = 100
    emoji: str = "🐕"

    def get_bonus_description(self) -> str:
        """Get human-readable bonus description"""
        return f"+{self.bonus_value} {self.bonus_type}"


@dataclass
class MentalHealth:
    """Dweller mental health tracking"""
    dweller_id: str
    stress_level: int = 0  # 0-100
    trauma_events: List[str] = field(default_factory=list)
    therapy_sessions: int = 0
    medications: List[str] = field(default_factory=list)
    breakdown_risk: int = 0  # 0-100
    last_breakdown_day: int = 0
    resilience: int = 50  # How well they cope with stress

    def add_stress(self, amount: int):
        """Add stress, capped at 100"""
        self.stress_level = min(100, self.stress_level + amount)
        self._update_breakdown_risk()

    def reduce_stress(self, amount: int):
        """Reduce stress, minimum 0"""
        self.stress_level = max(0, self.stress_level - amount)
        self._update_breakdown_risk()

    def _update_breakdown_risk(self):
        """Update breakdown risk based on stress and resilience"""
        # Higher stress + lower resilience = higher risk
        self.breakdown_risk = max(0, min(100,
            self.stress_level - (self.resilience // 2)
        ))

    def is_at_risk(self) -> bool:
        """Check if at risk of breakdown"""
        return self.breakdown_risk > 70


@dataclass
class Disease:
    """Disease that can afflict dwellers"""
    disease_id: str
    name: str
    severity: int  # 1-5
    contagious: bool
    transmission_rate: float  # 0.0-1.0
    symptoms: List[str] = field(default_factory=list)
    cure_research_required: int = 0
    duration_days: int = 5
    effects: Dict[str, int] = field(default_factory=dict)


@dataclass
class Infection:
    """Active infection on a dweller"""
    dweller_id: str
    disease: Disease
    day_infected: int
    days_remaining: int
    quarantined: bool = False
    treated: bool = False

    def is_recovered(self) -> bool:
        """Check if infection has run its course"""
        return self.days_remaining <= 0


@dataclass
class CombatEncounter:
    """Tactical combat encounter"""
    encounter_id: str
    encounter_type: str  # "raider_attack", "mutant_assault", "robot_malfunction"
    turn: int = 0
    enemy_count: int = 0
    enemy_health: List[int] = field(default_factory=list)
    enemy_positions: List[Tuple[int, int]] = field(default_factory=list)
    defender_positions: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    cover_map: List[List[str]] = field(default_factory=list)
    active: bool = True
    victory: bool = False

    def get_remaining_enemies(self) -> int:
        """Count remaining enemies"""
        return sum(1 for hp in self.enemy_health if hp > 0)

    def is_over(self) -> bool:
        """Check if combat is over"""
        return not self.active or self.get_remaining_enemies() == 0


@dataclass
class DefenseWave:
    """Raider attack wave"""
    wave_number: int
    raiders_count: int
    raider_strength: int
    rewards: Dict[str, int] = field(default_factory=dict)
    completed: bool = False


@dataclass
class HallOfFameEntry:
    """Record of legendary moments"""
    entry_type: str  # "best_dweller", "record", "memorable_death", "greatest_vault"
    title: str
    description: str
    day_achieved: int
    stats: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Disaster:
    """Major vault disaster"""
    disaster_type: str
    severity: int  # 1-10
    start_day: int
    duration: int
    effects: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False

    def get_days_remaining(self, current_day: int) -> int:
        """Get days until disaster ends"""
        return max(0, (self.start_day + self.duration) - current_day)


@dataclass
class TradeOffer:
    """Merchant trade offer"""
    item_id: str
    item_name: str
    price: int
    quantity: int = 1
    is_buying: bool = False  # True = merchant buys from you


@dataclass
class Relationship:
    """Relationship between two dwellers"""
    dweller1_id: str
    dweller2_id: str
    relationship_type: str  # "friend", "rival", "mentor", "enemy"
    strength: int = 50  # 0-100
    history: List[str] = field(default_factory=list)
    days_known: int = 0

    def improve(self, amount: int):
        """Improve relationship"""
        self.strength = min(100, self.strength + amount)

    def degrade(self, amount: int):
        """Degrade relationship"""
        self.strength = max(-100, self.strength - amount)
