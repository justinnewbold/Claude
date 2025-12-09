"""
Vault Shelter - Dweller Module
===============================
Dweller management system extracted from vault_shelter_v6.py

This represents the refactoring of the monolithic 6,983-line file.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class Dweller:
    """
    Enhanced dweller with full SPECIAL stats, relationships, and breeding.

    Extracted from vault_shelter_v6.py as part of modular refactoring.
    """
    # Identity
    name: str
    age: int = 25
    gender: str = "M"  # M or F

    # SPECIAL stats (Fallout-style)
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
    parent1: Optional[str] = None
    parent2: Optional[str] = None
    is_child: bool = False
    child_grow_day: Optional[int] = None
    relationships: Dict[str, int] = field(default_factory=dict)  # name: affection (0-100)
    partner: Optional[str] = None
    pregnant: bool = False
    due_day: Optional[int] = None

    # Traits
    traits: List[str] = field(default_factory=list)

    def get_stat(self, stat_name: str, equipment_library: Dict = None, trait_library: Dict = None) -> int:
        """
        Get SPECIAL stat with equipment and trait bonuses.

        Args:
            stat_name: Name of SPECIAL stat (strength, perception, etc.)
            equipment_library: Equipment data (optional)
            trait_library: Trait data (optional)

        Returns:
            Modified stat value (1-10)
        """
        base_stat = getattr(self, stat_name.lower(), 5)
        bonus = 0

        # Equipment bonuses
        if equipment_library and self.outfit and self.outfit in equipment_library:
            outfit = equipment_library[self.outfit]
            bonus += outfit.get('stat_bonus', {}).get(stat_name.lower(), 0)

        # Trait bonuses
        if trait_library:
            for trait_id in self.traits:
                if trait_id in trait_library:
                    trait = trait_library[trait_id]
                    bonus += trait.get('effects', {}).get(stat_name.lower(), 0)

        return max(1, min(10, base_stat + bonus))

    def get_combat_power(self, equipment_library: Dict = None, skill_library: Dict = None,
                        legendary_items: Dict = None) -> int:
        """
        Calculate combat power with all bonuses.

        Args:
            equipment_library: Equipment data
            skill_library: Skill data
            legendary_items: Legendary equipment data

        Returns:
            Total combat power
        """
        weapon_damage = 0

        if equipment_library and self.weapon and self.weapon in equipment_library:
            weapon_damage = equipment_library[self.weapon].get('damage', 0)

        base_power = self.get_stat("strength", equipment_library) + weapon_damage

        # Skill bonuses
        if skill_library:
            if "sharp_shooter" in self.learned_skills:
                bonus = skill_library.get("sharp_shooter", {}).get("bonus_value", 0)
                base_power = int(base_power * (1 + bonus))
            if "tank" in self.learned_skills:
                base_power = int(base_power * 1.2)

        # Legendary equipment bonuses
        if legendary_items:
            for legendary_id in legendary_items:
                legendary = legendary_items[legendary_id]
                if self.weapon == legendary.get('base_item') or self.outfit == legendary.get('base_item'):
                    damage_mult = legendary.get('power_effect', {}).get('damage_mult', 1.0)
                    base_power = int(base_power * damage_mult)

        return base_power

    def can_learn_skill(self, skill_key: str, skill_library: Dict = None) -> bool:
        """
        Check if dweller can learn a skill.

        Args:
            skill_key: Skill identifier
            skill_library: Skill data

        Returns:
            True if requirements met
        """
        if skill_key in self.learned_skills or self.is_child:
            return False

        if not skill_library or skill_key not in skill_library:
            return False

        skill = skill_library[skill_key]
        requirements = skill.get('stat_requirement', {})

        for stat, required in requirements.items():
            if self.get_stat(stat) < required:
                return False

        return True

    def learn_skill(self, skill_key: str, skill_library: Dict = None) -> bool:
        """Learn a skill if requirements met"""
        if self.can_learn_skill(skill_key, skill_library):
            self.learned_skills.append(skill_key)
            return True
        return False

    def add_experience(self, amount: int) -> bool:
        """
        Add experience and level up if threshold reached.

        Args:
            amount: XP to add

        Returns:
            True if leveled up
        """
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
        """
        Modify a SPECIAL stat.

        Args:
            stat_name: Stat to modify
            amount: Amount to add/subtract
        """
        if self.is_child:
            return

        current = getattr(self, stat_name.lower(), 5)
        setattr(self, stat_name.lower(), max(1, min(10, current + amount)))

    def modify_happiness(self, amount: int):
        """Modify happiness (0-100)"""
        self.happiness = max(0, min(100, self.happiness + amount))

    def modify_health(self, amount: int):
        """Modify health (0-100)"""
        self.health = max(0, min(100, self.health + amount))

    def can_have_children(self) -> bool:
        """Check if dweller can have children"""
        return (not self.is_child and
                not self.pregnant and
                self.partner is not None and
                self.age < 50 and
                self.gender == "F")

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'strength': self.strength,
            'perception': self.perception,
            'endurance': self.endurance,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'agility': self.agility,
            'luck': self.luck,
            'happiness': self.happiness,
            'health': self.health,
            'assigned_room': self.assigned_room,
            'weapon': self.weapon,
            'outfit': self.outfit,
            'learned_skills': self.learned_skills,
            'experience': self.experience,
            'level': self.level,
            'traits': self.traits,
            'relationships': self.relationships,
            'partner': self.partner,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Dweller':
        """Create dweller from dictionary"""
        return cls(**data)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_random_dweller(name: str) -> Dweller:
    """
    Create a dweller with random stats.

    Args:
        name: Dweller name

    Returns:
        New Dweller instance
    """
    import random

    return Dweller(
        name=name,
        strength=random.randint(3, 8),
        perception=random.randint(3, 8),
        endurance=random.randint(3, 8),
        charisma=random.randint(3, 8),
        intelligence=random.randint(3, 8),
        agility=random.randint(3, 8),
        luck=random.randint(3, 8),
        age=random.randint(18, 40),
        gender=random.choice(["M", "F"]),
        personality_outlook=random.choice(["Optimistic", "Pragmatic", "Pessimistic"]),
        personality_work_ethic=random.choice(["Hardworking", "Average", "Lazy"]),
        personality_social=random.choice(["Friendly", "Neutral", "Antisocial"]),
        personality_courage=random.choice(["Brave", "Cautious", "Cowardly"]),
    )


def calculate_child_stats(parent1: Dweller, parent2: Dweller) -> Dict[str, int]:
    """
    Calculate child stats from parents.

    Args:
        parent1: First parent
        parent2: Second parent

    Returns:
        Dictionary of SPECIAL stats
    """
    import random

    stats = {}
    stat_names = ['strength', 'perception', 'endurance', 'charisma', 'intelligence', 'agility', 'luck']

    for stat in stat_names:
        parent1_stat = getattr(parent1, stat, 5)
        parent2_stat = getattr(parent2, stat, 5)

        # Average with some randomness
        avg = (parent1_stat + parent2_stat) // 2
        variation = random.randint(-1, 1)
        stats[stat] = max(1, min(10, avg + variation))

    return stats


def get_relationship_status(affection: int) -> str:
    """
    Get relationship status from affection level.

    Args:
        affection: Affection level (0-100)

    Returns:
        Status string
    """
    if affection >= 80:
        return "❤️ Soulmates"
    elif affection >= 60:
        return "💕 In Love"
    elif affection >= 40:
        return "😊 Friends"
    elif affection >= 20:
        return "🤝 Acquaintances"
    else:
        return "😐 Strangers"
