"""
VAULT 13: Dweller Model
The Dweller class representing vault inhabitants.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from vault13.constants import (
    EQUIPMENT_LIBRARY, SKILL_LIBRARY, TRAIT_LIBRARY, LEGENDARY_ITEMS
)


@dataclass
class Dweller:
    """Enhanced dweller with relationships, skills, and personality"""
    name: str
    # SPECIAL stats
    strength: int = 5
    perception: int = 5
    endurance: int = 5
    charisma: int = 5
    intelligence: int = 5
    agility: int = 5
    luck: int = 5
    # Status
    happiness: int = 50
    health: int = 100
    assigned_room: Optional[Tuple[int, int]] = None
    assigned_room_floor: Optional[int] = None
    assigned_room_pos: Optional[int] = None
    weapon: Optional[str] = None
    outfit: Optional[str] = None
    # AI Personality
    personality_outlook: str = "Pragmatic"
    personality_work_ethic: str = "Hardworking"
    personality_social: str = "Friendly"
    personality_courage: str = "Cautious"
    recent_dialogue: str = ""
    # Progression
    learned_skills: List[str] = field(default_factory=list)
    experience: int = 0
    level: int = 1
    on_expedition: bool = False
    expedition_return_day: int = 0
    # Relationships & Breeding
    age: int = 25
    gender: str = "M"
    parent1: Optional[str] = None
    parent2: Optional[str] = None
    is_child: bool = False
    child_grow_day: Optional[int] = None
    relationships: Dict[str, int] = field(default_factory=dict)
    partner: Optional[str] = None
    pregnant: bool = False
    due_day: Optional[int] = None
    # Traits
    traits: List[str] = field(default_factory=list)

    def get_stat(self, stat_name: str) -> int:
        """Get SPECIAL stat with equipment and trait bonuses"""
        base_stat = getattr(self, stat_name.lower(), 5)
        bonus = 0
        # Equipment bonuses
        if self.outfit and self.outfit in EQUIPMENT_LIBRARY:
            outfit = EQUIPMENT_LIBRARY[self.outfit]
            bonus += outfit.stat_bonus.get(stat_name.lower(), 0)
        # Trait bonuses
        for trait_id in self.traits:
            if trait_id in TRAIT_LIBRARY:
                trait = TRAIT_LIBRARY[trait_id]
                bonus += trait.effects.get(stat_name.lower(), 0)
        return max(1, min(10, base_stat + bonus))

    def get_combat_power(self, legendary_inventory: List[str] = None) -> int:
        """Combat power with skills and legendary bonuses"""
        weapon_damage = 0
        if self.weapon and self.weapon in EQUIPMENT_LIBRARY:
            weapon_damage = EQUIPMENT_LIBRARY[self.weapon].damage

        base_power = self.get_stat("strength") + weapon_damage

        # Skill bonuses
        if "sharp_shooter" in self.learned_skills:
            base_power = int(base_power * (1 + SKILL_LIBRARY["sharp_shooter"].bonus_value))
        if "tank" in self.learned_skills:
            base_power = int(base_power * 1.2)

        # Legendary equipment bonuses
        if legendary_inventory:
            for legendary_id in legendary_inventory:
                if legendary_id in LEGENDARY_ITEMS:
                    legendary = LEGENDARY_ITEMS[legendary_id]
                    if self.weapon == legendary.base_item or self.outfit == legendary.base_item:
                        damage_mult = legendary.power_effect.get("damage_mult", 1.0)
                        base_power = int(base_power * damage_mult)

        # Trait combat bonuses
        for trait_id in self.traits:
            if trait_id in TRAIT_LIBRARY:
                trait = TRAIT_LIBRARY[trait_id]
                combat_mult = trait.effects.get("combat_mult", 1.0)
                base_power = int(base_power * combat_mult)

        return base_power

    def can_learn_skill(self, skill_key: str) -> bool:
        """Check skill requirements"""
        if skill_key in self.learned_skills or self.is_child:
            return False
        skill = SKILL_LIBRARY.get(skill_key)
        if not skill:
            return False
        for stat, required in skill.stat_requirement.items():
            if self.get_stat(stat) < required:
                return False
        return True

    def learn_skill(self, skill_key: str) -> bool:
        """Learn skill"""
        if self.can_learn_skill(skill_key):
            self.learned_skills.append(skill_key)
            return True
        return False

    def add_experience(self, amount: int) -> bool:
        """Add XP and level up"""
        if self.is_child:
            return False
        self.experience += amount
        xp_needed = self.level * 100
        if self.experience >= xp_needed:
            self.level += 1
            self.experience -= xp_needed
            return True
        return False

    def get_personality_summary(self) -> str:
        """Get personality description"""
        return f"{self.personality_outlook}, {self.personality_work_ethic}, {self.personality_social}, {self.personality_courage}"

    def modify_stat(self, stat_name: str, amount: int):
        """Modify SPECIAL stat"""
        if self.is_child:
            return
        current = getattr(self, stat_name.lower(), 5)
        setattr(self, stat_name.lower(), max(1, min(10, current + amount)))

    def modify_happiness(self, amount: int):
        """Modify happiness"""
        self.happiness = max(0, min(100, self.happiness + amount))

    def modify_health(self, amount: int):
        """Modify health"""
        self.health = max(0, min(100, self.health + amount))

    def can_have_children(self) -> bool:
        """Check if can have children"""
        return (not self.is_child and
                not self.pregnant and
                self.partner is not None and
                self.age < 50 and
                self.gender == "F")

    def get_total_stats(self) -> int:
        """Get sum of all SPECIAL stats"""
        return sum([
            self.get_stat("strength"),
            self.get_stat("perception"),
            self.get_stat("endurance"),
            self.get_stat("charisma"),
            self.get_stat("intelligence"),
            self.get_stat("agility"),
            self.get_stat("luck")
        ])

    def is_injured(self) -> bool:
        """Check if dweller needs healing"""
        return self.health < 50

    def is_happy(self) -> bool:
        """Check if dweller is happy"""
        return self.happiness >= 70

    def is_unhappy(self) -> bool:
        """Check if dweller is unhappy"""
        return self.happiness < 30
