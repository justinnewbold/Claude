"""
VAULT 13: Constants and Enumerations
All game constants, enums, and configuration data.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


# =============================================================================
# ENUMS
# =============================================================================

class RoomType(Enum):
    """All room types in the vault"""
    EMPTY = "Empty"
    # Production
    POWER_GENERATOR = "Power Generator"
    WATER_TREATMENT = "Water Treatment"
    DINER = "Diner"
    # Utility
    LIVING_QUARTERS = "Living Quarters"
    STORAGE_ROOM = "Storage Room"
    MEDBAY = "Medbay"
    # Advanced
    TRAINING_ROOM = "Training Room"
    SCIENCE_LAB = "Science Lab"
    # v5.0 Rooms
    RADIO_ROOM = "Radio Room"
    WORKSHOP = "Workshop"
    ARMORY = "Armory"
    GARDEN = "Garden"
    GYM = "Gym"
    ARCHIVES = "Archives"


class EquipmentType(Enum):
    """Equipment types"""
    WEAPON = "Weapon"
    OUTFIT = "Outfit"


class QuestStatus(Enum):
    """Quest status"""
    ACTIVE = "Active"
    COMPLETED = "Completed"
    FAILED = "Failed"


class ObjectiveType(Enum):
    """Victory objectives"""
    UTOPIA = "Utopia"
    ECONOMIC = "Economic"
    RESEARCH = "Research"
    MILITARY = "Military"
    EXODUS = "Exodus"
    SURVIVAL = "Survival"


class Season(Enum):
    """Four seasons"""
    SPRING = "Spring"
    SUMMER = "Summer"
    FALL = "Fall"
    WINTER = "Winter"


class GovernmentType(Enum):
    """Vault government types"""
    DEMOCRACY = "Democracy"
    AUTOCRACY = "Autocracy"
    TECHNOCRACY = "Technocracy"


class FactionType(Enum):
    """Wasteland factions"""
    RAIDERS = "Raiders"
    BROTHERHOOD = "Brotherhood of Steel"
    MERCHANTS = "Merchant Guild"
    SETTLERS = "Settler Alliance"
    OUTCASTS = "Outcast Survivors"


class RelationshipType(Enum):
    """Dweller relationships"""
    STRANGER = "Stranger"
    ACQUAINTANCE = "Acquaintance"
    FRIEND = "Friend"
    BEST_FRIEND = "Best Friend"
    RIVAL = "Rival"
    ENEMY = "Enemy"
    ROMANTIC = "Romantic Interest"
    PARTNER = "Partner"
    MARRIED = "Married"


class DisasterType(Enum):
    """Major disasters"""
    FLOOD = "Flood"
    PLAGUE = "Plague"
    MELTDOWN = "Reactor Meltdown"
    INVASION = "Raider Invasion"
    FAMINE = "Famine"


class TraitType(Enum):
    """Dweller trait types"""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    MUTATION = "Mutation"


# =============================================================================
# PERSONALITY TRAITS
# =============================================================================

PERSONALITY_TRAITS = {
    "outlook": ["Optimistic", "Pessimistic", "Pragmatic", "Cynical"],
    "work_ethic": ["Hardworking", "Lazy", "Ambitious", "Laid-back"],
    "social": ["Friendly", "Reserved", "Charismatic", "Awkward"],
    "courage": ["Brave", "Cautious", "Reckless", "Cowardly"]
}


# =============================================================================
# SKILL DATA
# =============================================================================

@dataclass
class Skill:
    """Learnable dweller skill"""
    name: str
    description: str
    stat_requirement: Dict[str, int]
    bonus_type: str
    bonus_value: float
    icon: str = "⭐"


SKILL_LIBRARY = {
    # Production Skills
    "power_expert": Skill("Power Expert", "+30% power production", {"strength": 6, "intelligence": 5}, "production_power", 0.3, "⚡"),
    "water_purifier": Skill("Water Purifier", "+30% water production", {"perception": 6, "intelligence": 5}, "production_water", 0.3, "💧"),
    "master_chef": Skill("Master Chef", "+30% food production", {"agility": 6, "charisma": 5}, "production_food", 0.3, "🍖"),
    # Combat Skills
    "sharp_shooter": Skill("Sharp Shooter", "+50% weapon damage", {"perception": 7, "agility": 6}, "combat_damage", 0.5, "🎯"),
    "tank": Skill("Tank", "-30% damage taken", {"strength": 7, "endurance": 7}, "combat_defense", 0.3, "🛡️"),
    # Exploration Skills
    "wasteland_survivor": Skill("Wasteland Survivor", "-25% expedition time", {"endurance": 6, "luck": 6}, "exploration_speed", 0.25, "🏜️"),
    "scavenger": Skill("Scavenger", "+50% loot found", {"perception": 6, "luck": 7}, "exploration_loot", 0.5, "🔍"),
    # Utility Skills
    "leader": Skill("Leader", "+10% happiness aura", {"charisma": 8, "intelligence": 6}, "happiness_aura", 0.1, "👑"),
    "medic": Skill("Medic", "Heal faster, treat others", {"intelligence": 7, "charisma": 5}, "healing", 0.3, "⚕️"),
}


# =============================================================================
# EQUIPMENT DATA
# =============================================================================

@dataclass
class Equipment:
    """Dweller equipment"""
    name: str
    equipment_type: EquipmentType
    stat_bonus: Dict[str, int] = field(default_factory=dict)
    damage: int = 0
    defense: int = 0
    icon: str = "⚔️"
    crafting_recipe: Optional[Dict[str, int]] = None

    def get_description(self) -> str:
        if self.equipment_type == EquipmentType.WEAPON:
            return f"Damage: {self.damage}" + (f", Defense: {self.defense}" if self.defense > 0 else "")
        else:
            bonuses = ", ".join([f"+{v} {k.upper()[0]}" for k, v in self.stat_bonus.items()])
            return f"Bonuses: {bonuses}"


EQUIPMENT_LIBRARY = {
    # Weapons
    "rusty_pistol": Equipment("Rusty Pistol", EquipmentType.WEAPON, damage=5, icon="🔫"),
    "laser_rifle": Equipment("Laser Rifle", EquipmentType.WEAPON, damage=15, icon="⚡"),
    "plasma_gun": Equipment("Plasma Gun", EquipmentType.WEAPON, damage=25, icon="💚"),
    "combat_rifle": Equipment("Combat Rifle", EquipmentType.WEAPON, damage=20, icon="🔫",
                             crafting_recipe={"metal": 3, "electronics": 2}),
    "sniper_rifle": Equipment("Sniper Rifle", EquipmentType.WEAPON, damage=30, icon="🎯",
                             crafting_recipe={"metal": 5, "electronics": 3}),
    # Outfits
    "vault_suit": Equipment("Vault Suit", EquipmentType.OUTFIT, stat_bonus={"endurance": 1}, icon="👔"),
    "scientist_coat": Equipment("Scientist Coat", EquipmentType.OUTFIT, stat_bonus={"intelligence": 2}, icon="🥼"),
    "power_armor": Equipment("Power Armor", EquipmentType.OUTFIT, stat_bonus={"strength": 3, "endurance": 2}, icon="🛡️"),
    "reinforced_armor": Equipment("Reinforced Armor", EquipmentType.OUTFIT, stat_bonus={"endurance": 3}, defense=10, icon="🛡️",
                                 crafting_recipe={"metal": 4, "cloth": 2}),
}


# =============================================================================
# ROOM CONFIGURATION
# =============================================================================

@dataclass
class RoomStats:
    """Room configuration"""
    cost: int
    production: Dict[str, int]
    capacity: int
    stat_required: Optional[str] = None
    description: str = ""
    upgrade_cost_multiplier: float = 1.5
    requires_tech: Optional[str] = None


ROOM_CONFIGS = {
    RoomType.POWER_GENERATOR: RoomStats(150, {"power": 5}, 2, "strength", "Generates electrical power"),
    RoomType.WATER_TREATMENT: RoomStats(120, {"water": 5}, 2, "perception", "Purifies water"),
    RoomType.DINER: RoomStats(100, {"food": 5}, 2, "agility", "Produces food"),
    RoomType.LIVING_QUARTERS: RoomStats(100, {}, 4, None, "Houses dwellers"),
    RoomType.TRAINING_ROOM: RoomStats(200, {}, 2, None, "Trains SPECIAL stats"),
    RoomType.STORAGE_ROOM: RoomStats(80, {}, 0, None, "Increases storage capacity"),
    RoomType.MEDBAY: RoomStats(150, {}, 2, None, "Heals injured dwellers"),
    RoomType.SCIENCE_LAB: RoomStats(250, {}, 2, "intelligence", "Generates research points"),
    RoomType.RADIO_ROOM: RoomStats(180, {"influence": 3}, 1, "charisma", "Attracts new dwellers", requires_tech="radio_tech"),
    RoomType.WORKSHOP: RoomStats(200, {"materials": 2}, 2, "intelligence", "Crafts equipment", requires_tech="workshop_tech"),
    RoomType.ARMORY: RoomStats(220, {}, 3, "strength", "Stores weapons, trains combat", requires_tech="armory_tech"),
    RoomType.GARDEN: RoomStats(150, {"food": 3}, 2, "intelligence", "Alternative food source", requires_tech="hydroponics"),
    RoomType.GYM: RoomStats(180, {}, 2, "endurance", "Trains stats 50% faster", requires_tech="fitness_program"),
    RoomType.ARCHIVES: RoomStats(300, {"research": 5}, 2, "intelligence", "Generates research points", requires_tech="archive_system"),
}


# Room adjacency bonuses
ADJACENCY_BONUSES = {
    (RoomType.POWER_GENERATOR, RoomType.POWER_GENERATOR): {"production_bonus": 0.15, "name": "Power Grid"},
    (RoomType.WATER_TREATMENT, RoomType.WATER_TREATMENT): {"production_bonus": 0.15, "name": "Water Network"},
    (RoomType.DINER, RoomType.DINER): {"production_bonus": 0.15, "name": "Kitchen Complex"},
    (RoomType.SCIENCE_LAB, RoomType.POWER_GENERATOR): {"production_bonus": 0.10, "name": "Research Power"},
    (RoomType.MEDBAY, RoomType.LIVING_QUARTERS): {"happiness_bonus": 5, "name": "Healthcare Access"},
    (RoomType.TRAINING_ROOM, RoomType.LIVING_QUARTERS): {"happiness_bonus": 3, "name": "Fitness Center"},
    (RoomType.STORAGE_ROOM, RoomType.DINER): {"production_bonus": 0.10, "name": "Kitchen Storage"},
    (RoomType.WORKSHOP, RoomType.ARMORY): {"production_bonus": 0.20, "name": "Manufacturing Hub"},
    (RoomType.GARDEN, RoomType.DINER): {"production_bonus": 0.15, "name": "Farm-to-Table"},
    (RoomType.GYM, RoomType.ARMORY): {"happiness_bonus": 5, "name": "Combat Training"},
    (RoomType.ARCHIVES, RoomType.SCIENCE_LAB): {"production_bonus": 0.25, "name": "Research Complex"},
}


# =============================================================================
# TECHNOLOGY DATA
# =============================================================================

@dataclass
class Technology:
    """Researchable technology"""
    name: str
    description: str
    cost: int
    prerequisites: List[str] = field(default_factory=list)
    unlocks: List[str] = field(default_factory=list)
    bonus: Optional[Dict[str, Any]] = None
    icon: str = "🔬"


TECH_TREE = {
    # Tier 1 - Basic
    "radio_tech": Technology("Radio Technology", "Unlocks Radio Room", 100, [], ["radio_room"], icon="📻"),
    "workshop_tech": Technology("Workshop", "Unlocks Workshop for crafting", 150, [], ["workshop"], icon="🔧"),
    "hydroponics": Technology("Hydroponics", "Unlocks Garden for food", 120, [], ["garden"], icon="🌱"),
    # Tier 2 - Advanced
    "armory_tech": Technology("Armory Systems", "Unlocks Armory", 200, ["workshop_tech"], ["armory"], icon="⚔️"),
    "fitness_program": Technology("Fitness Program", "Unlocks Gym", 180, [], ["gym"], icon="💪"),
    "archive_system": Technology("Archive System", "Unlocks Archives", 250, ["workshop_tech"], ["archives"], icon="📚"),
    # Tier 3 - Bonuses
    "advanced_power": Technology("Advanced Power", "+20% power production", 300, ["workshop_tech"], [],
                                {"production_power_mult": 1.2}, icon="⚡"),
    "water_recycling": Technology("Water Recycling", "+20% water efficiency", 280, ["hydroponics"], [],
                                 {"production_water_mult": 1.2}, icon="💧"),
    "food_preservation": Technology("Food Preservation", "+25% food production", 250, ["hydroponics"], [],
                                   {"production_food_mult": 1.25}, icon="🍖"),
    # Tier 4 - Elite
    "combat_training": Technology("Advanced Combat", "+30% combat effectiveness", 400, ["armory_tech"], [],
                                 {"combat_mult": 1.3}, icon="🎯"),
    "medical_advances": Technology("Medical Advances", "Healing costs 50% less", 350, ["archive_system"], [],
                                  {"healing_cost_mult": 0.5}, icon="⚕️"),
    "automation": Technology("Automation", "Rooms produce with 1 less worker", 500, ["archive_system"], [],
                            {"worker_efficiency": True}, icon="🤖"),
}


# =============================================================================
# POLICY DATA
# =============================================================================

@dataclass
class Policy:
    """Vault policy"""
    name: str
    description: str
    effects: Dict[str, Any]
    cost: int = 0
    requires_government: Optional[GovernmentType] = None
    icon: str = "📜"


POLICY_LIBRARY = {
    # Democracy policies
    "free_rations": Policy("Free Rations", "+10 happiness, +20% food consumption",
                          {"happiness_bonus": 10, "food_mult": 1.2}, cost=50, requires_government=GovernmentType.DEMOCRACY, icon="🍖"),
    "democratic_vote": Policy("Democratic Voting", "+15 happiness, decisions by vote",
                             {"happiness_bonus": 15, "voting": True}, cost=100, requires_government=GovernmentType.DEMOCRACY, icon="🗳️"),
    # Autocracy policies
    "martial_law": Policy("Martial Law", "+30% combat, -10 happiness",
                         {"combat_mult": 1.3, "happiness_penalty": -10}, cost=50, requires_government=GovernmentType.AUTOCRACY, icon="⚔️"),
    "forced_labor": Policy("Forced Labor", "+30% production, -20 happiness",
                          {"production_mult": 1.3, "happiness_penalty": -20}, cost=75, requires_government=GovernmentType.AUTOCRACY, icon="⛏️"),
    # Technocracy policies
    "science_priority": Policy("Science Priority", "+50% research, +10% production",
                              {"research_mult": 1.5, "production_mult": 1.1}, cost=100, requires_government=GovernmentType.TECHNOCRACY, icon="🔬"),
    "efficiency_doctrine": Policy("Efficiency Doctrine", "-20% resource consumption",
                                 {"resource_efficiency": 0.8}, cost=150, requires_government=GovernmentType.TECHNOCRACY, icon="⚙️"),
}


# =============================================================================
# FACTION DATA
# =============================================================================

@dataclass
class Faction:
    """Wasteland faction"""
    name: str
    description: str
    reputation: int = 0
    icon: str = "🏴"


FACTIONS = {
    FactionType.RAIDERS: Faction("Raiders", "Violent marauders who attack settlements", icon="💀"),
    FactionType.BROTHERHOOD: Faction("Brotherhood of Steel", "Techno-zealots hoarding advanced weaponry", icon="🛡️"),
    FactionType.MERCHANTS: Faction("Merchant Guild", "Traders who bring goods from across the wasteland", icon="💰"),
    FactionType.SETTLERS: Faction("Settler Alliance", "Peaceful communities trying to rebuild", icon="🏘️"),
    FactionType.OUTCASTS: Faction("Outcast Survivors", "Desperate refugees seeking shelter", icon="🎒"),
}


# =============================================================================
# TRAIT DATA
# =============================================================================

@dataclass
class Trait:
    """Dweller trait"""
    name: str
    description: str
    trait_type: TraitType
    effects: Dict[str, Any] = field(default_factory=dict)
    inheritable: bool = False
    icon: str = "🔹"


TRAIT_LIBRARY = {
    # Positive traits
    "natural_leader": Trait("Natural Leader", "+15% happiness aura", TraitType.POSITIVE,
                           {"happiness_aura": 0.15}, inheritable=True, icon="👑"),
    "genius": Trait("Genius", "+2 Intelligence", TraitType.POSITIVE,
                   {"intelligence": 2}, inheritable=True, icon="🧠"),
    "athlete": Trait("Athlete", "+2 Strength, +1 Endurance", TraitType.POSITIVE,
                    {"strength": 2, "endurance": 1}, inheritable=True, icon="💪"),
    # Negative traits
    "pessimist": Trait("Pessimist", "-10% happiness", TraitType.NEGATIVE,
                      {"happiness_mult": 0.9}, inheritable=True, icon="😔"),
    "clumsy": Trait("Clumsy", "-1 Agility", TraitType.NEGATIVE,
                   {"agility": -1}, inheritable=True, icon="🤕"),
    # Mutations
    "radiation_resistant": Trait("Radiation Resistant", "50% less radiation damage", TraitType.MUTATION,
                                {"rad_resistance": 0.5}, inheritable=False, icon="☢️"),
    "night_vision": Trait("Night Vision", "Better exploration at night", TraitType.MUTATION,
                         {"exploration_bonus": 0.2}, inheritable=False, icon="👁️"),
}


# =============================================================================
# LEGENDARY ITEMS
# =============================================================================

@dataclass
class LegendaryItem:
    """Legendary equipment"""
    name: str
    description: str
    base_item: str
    power_effect: Dict[str, float]
    unique_ability: str
    icon: str = "⭐"


LEGENDARY_ITEMS = {
    "overseer_pistol": LegendaryItem("Overseer's Pistol", "The weapon of Vault 13's first Overseer",
                                    "rusty_pistol", {"damage_mult": 2.0}, "Inspires nearby dwellers", "🔫"),
    "quantum_armor": LegendaryItem("Quantum Armor", "Armor that phases in and out of reality",
                                  "power_armor", {"defense_mult": 1.5}, "20% dodge chance", "🛡️"),
    "lucky_charm": LegendaryItem("Lucky Charm", "A mysterious four-leaf clover pendant",
                                "", {"luck_mult": 1.5}, "+50% rare loot chance", "🍀"),
}


# =============================================================================
# CHEAT CODES
# =============================================================================

CHEAT_CODES = {
    "rosebud": "caps_10000",
    "poweroverwhelming": "max_resources",
    "showmethemoney": "caps_99999",
    "blacksheepwall": "all_tech",
    "thereisnocowlevel": "easter_egg",
}
