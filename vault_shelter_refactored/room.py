"""
Vault Shelter - Room Module
============================
Room management system extracted from vault_shelter_v6.py
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class RoomType(Enum):
    """Types of rooms in the vault"""
    EMPTY = "empty"
    POWER_GENERATOR = "power_generator"
    WATER_TREATMENT = "water_treatment"
    GARDEN = "garden"
    LIVING_QUARTERS = "living_quarters"
    DINER = "diner"
    STORAGE = "storage"
    MEDBAY = "medbay"
    SCIENCE_LAB = "science_lab"
    WORKSHOP = "workshop"
    TRAINING_ROOM = "training_room"
    ARMORY = "armory"
    RADIO_STATION = "radio_station"
    CLASSROOM = "classroom"
    GYM = "gym"


@dataclass
class RoomConfig:
    """Configuration for a room type"""
    room_type: RoomType
    name: str
    cost: int
    capacity: int
    production: Dict[str, int] = field(default_factory=dict)
    stat_required: Optional[str] = None
    icon: str = "🏢"
    description: str = ""


@dataclass
class Room:
    """
    Enhanced room with production, incidents, and upgrades.

    Extracted from vault_shelter_v6.py as part of modular refactoring.
    """
    room_type: RoomType
    floor: int
    position: int
    level: int = 1
    assigned_dwellers: List[str] = field(default_factory=list)
    under_construction: bool = False
    on_fire: bool = False
    has_incident: bool = False
    incident_strength: int = 0
    rush_cooldown: int = 0

    def get_production(self, dwellers_list: List, room_configs: Dict[RoomType, RoomConfig],
                      adjacency_bonus: float = 0.0, tech_bonuses: Dict[str, float] = None,
                      policy_bonuses: Dict[str, float] = None, skill_library: Dict = None) -> Dict[str, int]:
        """
        Calculate room production with all bonuses.

        Args:
            dwellers_list: List of Dweller objects
            room_configs: Room configuration data
            adjacency_bonus: Bonus from adjacent rooms
            tech_bonuses: Technology bonuses
            policy_bonuses: Policy bonuses
            skill_library: Skill data for worker bonuses

        Returns:
            Dictionary of resource: amount produced
        """
        # Can't produce during problems
        if self.room_type == RoomType.EMPTY or self.under_construction or self.on_fire or self.has_incident:
            return {}

        config = room_configs.get(self.room_type)
        if not config or not config.production:
            return {}

        production = config.production.copy()
        base_multiplier = self.level
        worker_count = len(self.assigned_dwellers)

        # Some rooms work without workers (e.g., Garden)
        if worker_count > 0 or config.room_type == RoomType.GARDEN:
            # Calculate stat multiplier
            if config.stat_required:
                total_stat = 0
                skill_bonus = 0

                for dweller_name in self.assigned_dwellers:
                    dweller = next((d for d in dwellers_list if d.name == dweller_name), None)
                    if dweller and not dweller.is_child:
                        total_stat += dweller.get_stat(config.stat_required)

                        # Skill bonuses
                        if skill_library:
                            resource_type = list(production.keys())[0] if production else None
                            if resource_type == "power" and "power_expert" in dweller.learned_skills:
                                skill_bonus += skill_library.get("power_expert", {}).get("bonus_value", 0)
                            elif resource_type == "water" and "water_purifier" in dweller.learned_skills:
                                skill_bonus += skill_library.get("water_purifier", {}).get("bonus_value", 0)
                            elif resource_type == "food" and "master_chef" in dweller.learned_skills:
                                skill_bonus += skill_library.get("master_chef", {}).get("bonus_value", 0)

                avg_stat = total_stat / worker_count if worker_count > 0 else 5
                stat_multiplier = avg_stat / 5.0 + skill_bonus
            else:
                stat_multiplier = 1.0

            # Apply all multipliers
            for resource, amount in production.items():
                total = amount * base_multiplier * stat_multiplier

                # Adjacency bonus
                if adjacency_bonus > 0:
                    total *= (1 + adjacency_bonus)

                # Technology bonuses
                if tech_bonuses and resource in tech_bonuses:
                    total *= (1 + tech_bonuses[resource])

                # Policy bonuses
                if policy_bonuses and resource in policy_bonuses:
                    total *= (1 + policy_bonuses[resource])

                production[resource] = int(total)

        return production

    def get_capacity(self) -> int:
        """Get room capacity"""
        # Capacity scales with level
        base_capacity = 2  # Default
        return base_capacity + (self.level - 1)

    def can_assign_dweller(self, dweller_name: str) -> bool:
        """Check if dweller can be assigned"""
        if dweller_name in self.assigned_dwellers:
            return False
        if len(self.assigned_dwellers) >= self.get_capacity():
            return False
        if self.room_type == RoomType.EMPTY or self.under_construction:
            return False
        return True

    def assign_dweller(self, dweller_name: str) -> bool:
        """Assign dweller to room"""
        if self.can_assign_dweller(dweller_name):
            self.assigned_dwellers.append(dweller_name)
            return True
        return False

    def unassign_dweller(self, dweller_name: str) -> bool:
        """Remove dweller from room"""
        if dweller_name in self.assigned_dwellers:
            self.assigned_dwellers.remove(dweller_name)
            return True
        return False

    def can_upgrade(self, vault_caps: int, upgrade_cost: int = 100) -> bool:
        """Check if room can be upgraded"""
        if self.level >= 3:  # Max level
            return False
        if self.room_type == RoomType.EMPTY:
            return False
        if vault_caps < upgrade_cost * self.level:
            return False
        return True

    def upgrade(self) -> bool:
        """Upgrade room to next level"""
        if self.level < 3:
            self.level += 1
            return True
        return False

    def start_rush(self) -> Tuple[bool, int]:
        """
        Attempt to rush production.

        Returns:
            Tuple of (success, reward_or_damage)
        """
        import random

        if self.rush_cooldown > 0:
            return False, 0

        # Rush has risk
        success_chance = 0.7 - (self.level * 0.1)  # Harder at higher levels
        success = random.random() < success_chance

        self.rush_cooldown = 10  # 10 turn cooldown

        if success:
            # Successful rush gives bonus resources
            reward = 50 * self.level
            return True, reward
        else:
            # Failed rush causes incident
            self.has_incident = True
            self.incident_strength = random.randint(3, 8)
            damage = 20
            return False, damage

    def resolve_incident(self, combat_power: int) -> bool:
        """
        Resolve room incident with combat.

        Args:
            combat_power: Combined power of dwellers fighting

        Returns:
            True if incident resolved
        """
        if not self.has_incident:
            return True

        if combat_power >= self.incident_strength:
            self.has_incident = False
            self.incident_strength = 0
            return True

        # Reduce incident strength
        self.incident_strength -= 1
        if self.incident_strength <= 0:
            self.has_incident = False
            return True

        return False

    def extinguish_fire(self) -> bool:
        """Extinguish fire in room"""
        if self.on_fire:
            self.on_fire = False
            return True
        return False

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'room_type': self.room_type.value,
            'floor': self.floor,
            'position': self.position,
            'level': self.level,
            'assigned_dwellers': self.assigned_dwellers,
            'under_construction': self.under_construction,
            'on_fire': self.on_fire,
            'has_incident': self.has_incident,
            'incident_strength': self.incident_strength,
            'rush_cooldown': self.rush_cooldown,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Room':
        """Create room from dictionary"""
        data['room_type'] = RoomType(data['room_type'])
        return cls(**data)


# =============================================================================
# ROOM CONFIGURATIONS
# =============================================================================

DEFAULT_ROOM_CONFIGS = {
    RoomType.POWER_GENERATOR: RoomConfig(
        room_type=RoomType.POWER_GENERATOR,
        name="Power Generator",
        cost=150,
        capacity=2,
        production={"power": 5},
        stat_required="strength",
        icon="⚡",
        description="Generates electrical power"
    ),
    RoomType.WATER_TREATMENT: RoomConfig(
        room_type=RoomType.WATER_TREATMENT,
        name="Water Treatment",
        cost=150,
        capacity=2,
        production={"water": 5},
        stat_required="perception",
        icon="💧",
        description="Purifies water"
    ),
    RoomType.GARDEN: RoomConfig(
        room_type=RoomType.GARDEN,
        name="Garden",
        cost=120,
        capacity=2,
        production={"food": 4},
        stat_required="agility",
        icon="🌱",
        description="Grows food"
    ),
    RoomType.LIVING_QUARTERS: RoomConfig(
        room_type=RoomType.LIVING_QUARTERS,
        name="Living Quarters",
        cost=100,
        capacity=4,
        icon="🛏️",
        description="Houses dwellers"
    ),
    RoomType.STORAGE: RoomConfig(
        room_type=RoomType.STORAGE,
        name="Storage Room",
        cost=100,
        capacity=1,
        icon="📦",
        description="Stores resources"
    ),
    RoomType.MEDBAY: RoomConfig(
        room_type=RoomType.MEDBAY,
        name="Med Bay",
        cost=200,
        capacity=2,
        stat_required="intelligence",
        icon="⚕️",
        description="Heals dwellers"
    ),
    RoomType.TRAINING_ROOM: RoomConfig(
        room_type=RoomType.TRAINING_ROOM,
        name="Training Room",
        cost=180,
        capacity=3,
        icon="💪",
        description="Trains dweller stats"
    ),
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def calculate_adjacency_bonus(room: Room, all_rooms: List[Room]) -> float:
    """
    Calculate bonus from adjacent rooms of same type.

    Args:
        room: Room to calculate for
        all_rooms: All rooms in vault

    Returns:
        Bonus multiplier (0.0 - 0.3)
    """
    if room.room_type == RoomType.EMPTY:
        return 0.0

    adjacent_same = 0

    for other in all_rooms:
        if other.room_type == room.room_type and other != room:
            # Check if adjacent (same floor, position ± 1)
            if other.floor == room.floor and abs(other.position - room.position) == 1:
                adjacent_same += 1

    # Up to 30% bonus for 3 adjacent rooms
    return min(adjacent_same * 0.1, 0.3)


def get_room_icon(room_type: RoomType) -> str:
    """Get icon for room type"""
    config = DEFAULT_ROOM_CONFIGS.get(room_type)
    return config.icon if config else "🏢"


def get_room_name(room_type: RoomType) -> str:
    """Get name for room type"""
    config = DEFAULT_ROOM_CONFIGS.get(room_type)
    return config.name if config else room_type.value.replace('_', ' ').title()
