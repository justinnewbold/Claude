"""
VAULT 13: Room Model
The Room class representing vault rooms.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from vault13.constants import (
    RoomType, ROOM_CONFIGS, SKILL_LIBRARY
)


@dataclass
class Room:
    """Enhanced room with production and incidents"""
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

    def get_production(self, dwellers_list, adjacency_bonus: float = 0.0,
                      tech_bonuses: Dict[str, float] = None,
                      policy_bonuses: Dict[str, float] = None) -> Dict[str, int]:
        """Calculate production with ALL bonuses"""
        if self.room_type == RoomType.EMPTY or self.under_construction or self.on_fire or self.has_incident:
            return {}

        config = ROOM_CONFIGS.get(self.room_type)
        if not config or not config.production:
            return {}

        production = config.production.copy()
        base_multiplier = self.level
        worker_count = len(self.assigned_dwellers)

        if worker_count > 0 or self.room_type == RoomType.GARDEN:
            # Stat multiplier
            if config.stat_required:
                total_stat = 0
                skill_bonus = 0

                for dweller_name in self.assigned_dwellers:
                    dweller = next((d for d in dwellers_list if d.name == dweller_name), None)
                    if dweller and not dweller.is_child:
                        total_stat += dweller.get_stat(config.stat_required)

                        # Skills
                        resource_type = list(production.keys())[0] if production else None
                        if resource_type == "power" and "power_expert" in dweller.learned_skills:
                            skill_bonus += SKILL_LIBRARY["power_expert"].bonus_value
                        elif resource_type == "water" and "water_purifier" in dweller.learned_skills:
                            skill_bonus += SKILL_LIBRARY["water_purifier"].bonus_value
                        elif resource_type == "food" and "master_chef" in dweller.learned_skills:
                            skill_bonus += SKILL_LIBRARY["master_chef"].bonus_value

                avg_stat = total_stat / worker_count if worker_count > 0 else 5
                stat_multiplier = avg_stat / 5
                skill_multiplier = 1 + skill_bonus
            else:
                stat_multiplier = 1.0
                skill_multiplier = 1.0

            worker_multiplier = 1 + (worker_count * 0.2)
            adjacency_multiplier = 1 + adjacency_bonus

            # Tech bonuses
            tech_mult = 1.0
            if tech_bonuses:
                resource_type = list(production.keys())[0] if production else None
                if resource_type == "power":
                    tech_mult *= tech_bonuses.get("production_power_mult", 1.0)
                elif resource_type == "water":
                    tech_mult *= tech_bonuses.get("production_water_mult", 1.0)
                elif resource_type == "food":
                    tech_mult *= tech_bonuses.get("production_food_mult", 1.0)

            # Policy bonuses
            policy_mult = 1.0
            if policy_bonuses:
                policy_mult *= policy_bonuses.get("production_mult", 1.0)

            for resource in production:
                production[resource] = int(production[resource] * base_multiplier * worker_multiplier *
                                          stat_multiplier * skill_multiplier * adjacency_multiplier *
                                          tech_mult * policy_mult)

        return production

    def can_assign_dweller(self) -> bool:
        """Check if can assign"""
        if self.room_type == RoomType.EMPTY or self.under_construction:
            return False
        config = ROOM_CONFIGS.get(self.room_type)
        return len(self.assigned_dwellers) < config.capacity if config else False

    def get_upgrade_cost(self) -> int:
        """Upgrade cost"""
        if self.level >= 3:
            return 0
        config = ROOM_CONFIGS.get(self.room_type)
        if not config:
            return 0
        return int(config.cost * config.upgrade_cost_multiplier * self.level)

    def can_rush(self) -> bool:
        """Can rush production"""
        return (self.rush_cooldown == 0 and
                not self.under_construction and
                not self.on_fire and
                not self.has_incident and
                len(self.assigned_dwellers) > 0 and
                self.room_type in [RoomType.POWER_GENERATOR, RoomType.WATER_TREATMENT,
                                  RoomType.DINER, RoomType.GARDEN, RoomType.WORKSHOP])

    def get_display_name(self) -> str:
        """Get display name with level"""
        if self.room_type == RoomType.EMPTY:
            return "Empty"
        level_suffix = f" Lv{self.level}" if self.level > 1 else ""
        return f"{self.room_type.value}{level_suffix}"

    def get_status_icon(self) -> str:
        """Get status icon"""
        if self.under_construction:
            return "🚧"
        if self.on_fire:
            return "🔥"
        if self.has_incident:
            return "⚠️"
        if len(self.assigned_dwellers) == 0 and self.room_type != RoomType.EMPTY:
            return "👤"
        return ""

    def is_production_room(self) -> bool:
        """Check if room produces resources"""
        config = ROOM_CONFIGS.get(self.room_type)
        return config is not None and bool(config.production)
