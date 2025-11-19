#!/usr/bin/env python3
"""
VAULT 13 - SURVIVAL PROTOCOL v5.0 MEGA EDITION
The Ultimate Vault Management Experience

NEW v5.0 MEGA FEATURES (9 Major Systems):

OPTION A - FULL RPG EXPERIENCE:
- Relationships & Breeding System - Romance, families, children with inherited stats
- Research & Tech Tree - 20+ technologies to unlock
- Vault Policies & Government - Democracy, Autocracy, or Technocracy

OPTION B - DYNAMIC WORLD:
- Trading & Merchant System - Buy/sell with wasteland traders
- Faction System - 5 factions with reputation and unique quests
- Major Disasters & Crises - Vault-wide catastrophes

OPTION C - MASSIVE CONTENT:
- 6 New Room Types - Radio, Workshop, Armory, Garden, Gym, Archives
- Crafting System - Craft equipment from resources
- Seasonal Events & Calendar - 4 seasons with unique effects

ALL v4.0 FEATURES INCLUDED:
- AI Quests, Expeditions, Skills, Objectives, Adjacency Bonuses

ALL v3.0 AI FEATURES INCLUDED:
- AI Advisor, Dialogue, Natural Language

ALL v2.0 CORE FEATURES INCLUDED:
- Rush, Upgrades, Combat, Equipment, Rationing

REQUIRES: pip install anthropic (optional for AI features)
"""

import random
import time
import os
import sys
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict

# AI Integration
AI_ENABLED = False
try:
    import anthropic
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    if API_KEY:
        ai_client = anthropic.Anthropic(api_key=API_KEY)
        AI_ENABLED = True
        print("🤖 AI Features: ENABLED")
    else:
        print("⚠️  AI Features: DISABLED (set ANTHROPIC_API_KEY to enable)")
except ImportError:
    print("⚠️  AI Features: DISABLED (install: pip install anthropic)")


class C:
    """ANSI Color codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # UI Colors
    HEADER = '\033[38;5;51m'
    BORDER = '\033[38;5;39m'
    SUCCESS = '\033[38;5;46m'
    WARNING = '\033[38;5;226m'
    DANGER = '\033[38;5;196m'
    INFO = '\033[38;5;159m'
    AI = '\033[38;5;129m'
    QUEST = '\033[38;5;213m'
    SKILL = '\033[38;5;190m'
    TRADE = '\033[38;5;208m'  # Orange for trading
    FACTION = '\033[38;5;165m'  # Magenta for factions
    TECH = '\033[38;5;87m'  # Cyan for tech
    POLICY = '\033[38;5;99m'  # Purple for policies

    # Resource Colors
    POWER = '\033[38;5;226m'
    WATER = '\033[38;5;51m'
    FOOD = '\033[38;5;208m'
    CAPS = '\033[38;5;226m'

    # Room Colors
    ROOM_POWER = '\033[38;5;220m'
    ROOM_WATER = '\033[38;5;45m'
    ROOM_FOOD = '\033[38;5;214m'
    ROOM_LIVING = '\033[38;5;141m'
    ROOM_TRAINING = '\033[38;5;118m'
    ROOM_STORAGE = '\033[38;5;250m'
    ROOM_EMPTY = '\033[38;5;237m'

    # Status Colors
    HAPPY = '\033[38;5;82m'
    NEUTRAL = '\033[38;5;226m'
    SAD = '\033[38;5;196m'


# =============================================================================
# ENUMS
# =============================================================================

class RoomType(Enum):
    """All room types"""
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
    # NEW v5.0 Rooms
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


# NEW v5.0 Enums
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


# =============================================================================
# DATA CLASSES
# =============================================================================

# Personality traits
PERSONALITY_TRAITS = {
    "outlook": ["Optimistic", "Pessimistic", "Pragmatic", "Cynical"],
    "work_ethic": ["Hardworking", "Lazy", "Ambitious", "Laid-back"],
    "social": ["Friendly", "Reserved", "Charismatic", "Awkward"],
    "courage": ["Brave", "Cautious", "Reckless", "Cowardly"]
}


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


@dataclass
class Equipment:
    """Dweller equipment"""
    name: str
    equipment_type: EquipmentType
    stat_bonus: Dict[str, int] = field(default_factory=dict)
    damage: int = 0
    defense: int = 0
    icon: str = "⚔️"
    crafting_recipe: Optional[Dict[str, int]] = None  # NEW v5.0: can be crafted

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
    # NEW v5.0: Craftable weapons
    "combat_rifle": Equipment("Combat Rifle", EquipmentType.WEAPON, damage=20, icon="🔫",
                             crafting_recipe={"metal": 3, "electronics": 2}),
    "sniper_rifle": Equipment("Sniper Rifle", EquipmentType.WEAPON, damage=30, icon="🎯",
                             crafting_recipe={"metal": 5, "electronics": 3}),

    # Outfits
    "vault_suit": Equipment("Vault Suit", EquipmentType.OUTFIT, stat_bonus={"endurance": 1}, icon="👔"),
    "scientist_coat": Equipment("Scientist Coat", EquipmentType.OUTFIT, stat_bonus={"intelligence": 2}, icon="🥼"),
    "power_armor": Equipment("Power Armor", EquipmentType.OUTFIT, stat_bonus={"strength": 3, "endurance": 2}, icon="🛡️"),
    # NEW v5.0: Craftable outfits
    "reinforced_armor": Equipment("Reinforced Armor", EquipmentType.OUTFIT, stat_bonus={"endurance": 3}, defense=10, icon="🛡️",
                                 crafting_recipe={"metal": 4, "cloth": 2}),
}


@dataclass
class RoomStats:
    """Room configuration"""
    cost: int
    production: Dict[str, int]
    capacity: int
    stat_required: Optional[str] = None
    description: str = ""
    upgrade_cost_multiplier: float = 1.5
    requires_tech: Optional[str] = None  # NEW v5.0: tech requirement


ROOM_CONFIGS = {
    # Original rooms
    RoomType.POWER_GENERATOR: RoomStats(150, {"power": 5}, 2, "strength", "Generates electrical power"),
    RoomType.WATER_TREATMENT: RoomStats(120, {"water": 5}, 2, "perception", "Purifies water"),
    RoomType.DINER: RoomStats(100, {"food": 5}, 2, "agility", "Produces food"),
    RoomType.LIVING_QUARTERS: RoomStats(100, {}, 4, None, "Houses dwellers"),
    RoomType.TRAINING_ROOM: RoomStats(200, {}, 2, None, "Trains SPECIAL stats"),
    RoomType.STORAGE_ROOM: RoomStats(80, {}, 0, None, "Increases storage capacity"),
    RoomType.MEDBAY: RoomStats(150, {}, 2, None, "Heals injured dwellers"),
    RoomType.SCIENCE_LAB: RoomStats(250, {}, 2, "intelligence", "Generates research points"),

    # NEW v5.0 Rooms
    RoomType.RADIO_ROOM: RoomStats(
        cost=180,
        production={"influence": 3},
        capacity=1,
        stat_required="charisma",
        description="Attracts new dwellers, communicates with factions",
        requires_tech="radio_tech"
    ),
    RoomType.WORKSHOP: RoomStats(
        cost=200,
        production={"materials": 2},
        capacity=2,
        stat_required="intelligence",
        description="Crafts equipment and gathers materials",
        requires_tech="workshop_tech"
    ),
    RoomType.ARMORY: RoomStats(
        cost=220,
        production={},
        capacity=3,
        stat_required="strength",
        description="Stores weapons, trains combat skills",
        requires_tech="armory_tech"
    ),
    RoomType.GARDEN: RoomStats(
        cost=150,
        production={"food": 3},
        capacity=2,
        stat_required="intelligence",
        description="Alternative food source, requires no power",
        requires_tech="hydroponics"
    ),
    RoomType.GYM: RoomStats(
        cost=180,
        production={},
        capacity=2,
        stat_required="endurance",
        description="Trains stats 50% faster than Training Room",
        requires_tech="fitness_program"
    ),
    RoomType.ARCHIVES: RoomStats(
        cost=300,
        production={"research": 5},
        capacity=2,
        stat_required="intelligence",
        description="Generates research points, stores knowledge",
        requires_tech="archive_system"
    ),
}


# Room adjacency bonuses (from v4.0)
ADJACENCY_BONUSES = {
    (RoomType.POWER_GENERATOR, RoomType.POWER_GENERATOR): {"production_bonus": 0.15, "name": "Power Grid"},
    (RoomType.WATER_TREATMENT, RoomType.WATER_TREATMENT): {"production_bonus": 0.15, "name": "Water Network"},
    (RoomType.DINER, RoomType.DINER): {"production_bonus": 0.15, "name": "Kitchen Complex"},
    (RoomType.SCIENCE_LAB, RoomType.POWER_GENERATOR): {"production_bonus": 0.10, "name": "Research Power"},
    (RoomType.MEDBAY, RoomType.LIVING_QUARTERS): {"happiness_bonus": 5, "name": "Healthcare Access"},
    (RoomType.TRAINING_ROOM, RoomType.LIVING_QUARTERS): {"happiness_bonus": 3, "name": "Fitness Center"},
    (RoomType.STORAGE_ROOM, RoomType.DINER): {"production_bonus": 0.10, "name": "Kitchen Storage"},
    # NEW v5.0 adjacencies
    (RoomType.WORKSHOP, RoomType.ARMORY): {"production_bonus": 0.20, "name": "Manufacturing Hub"},
    (RoomType.GARDEN, RoomType.DINER): {"production_bonus": 0.15, "name": "Farm-to-Table"},
    (RoomType.GYM, RoomType.ARMORY): {"happiness_bonus": 5, "name": "Combat Training"},
    (RoomType.ARCHIVES, RoomType.SCIENCE_LAB): {"production_bonus": 0.25, "name": "Research Complex"},
}


# NEW v5.0: Technologies
@dataclass
class Technology:
    """Researchable technology"""
    name: str
    description: str
    cost: int  # research points
    prerequisites: List[str] = field(default_factory=list)
    unlocks: List[str] = field(default_factory=list)  # room types, policies, etc.
    bonus: Optional[Dict[str, any]] = None
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


# NEW v5.0: Policies
@dataclass
class Policy:
    """Vault policy"""
    name: str
    description: str
    effects: Dict[str, any]
    cost: int = 0  # influence cost
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


# NEW v5.0: Factions
@dataclass
class Faction:
    """Wasteland faction"""
    name: str
    description: str
    reputation: int = 0  # -100 to +100
    icon: str = "🏴"


FACTIONS = {
    FactionType.RAIDERS: Faction("Raiders", "Violent marauders who attack settlements", icon="💀"),
    FactionType.BROTHERHOOD: Faction("Brotherhood of Steel", "Techno-zealots hoarding advanced weaponry", icon="🛡️"),
    FactionType.MERCHANTS: Faction("Merchant Guild", "Traders who bring goods from across the wasteland", icon="💰"),
    FactionType.SETTLERS: Faction("Settler Alliance", "Peaceful communities trying to rebuild", icon="🏘️"),
    FactionType.OUTCASTS: Faction("Outcast Survivors", "Desperate refugees seeking shelter", icon="🎒"),
}


# (Continued in next part due to length constraints...)
# NEW v5.0: Relationship System
@dataclass
class Relationship:
    """Relationship between two dwellers"""
    dweller1: str
    dweller2: str
    relationship_type: RelationshipType = RelationshipType.STRANGER
    affection: int = 0  # 0-100
    days_together: int = 0
    is_married: bool = False
    children: List[str] = field(default_factory=list)


# NEW v5.0: Disaster
@dataclass
class Disaster:
    """Major vault disaster"""
    disaster_type: DisasterType
    severity: int  # 1-10
    start_day: int
    duration: int  # days
    effects: Dict[str, any] = field(default_factory=dict)
    resolved: bool = False


# NEW v5.0: Trade Offer
@dataclass
class TradeOffer:
    """Merchant trade offer"""
    item_id: str
    item_name: str
    price: int
    quantity: int = 1
    is_buying: bool = False  # True = merchant buys from you


# NEW v5.0: Crafting Recipe
@dataclass
class CraftingRecipe:
    """Recipe for crafting"""
    output: str  # equipment ID
    materials: Dict[str, int]  # material_type: amount
    caps_cost: int = 0
    requires_tech: Optional[str] = None


# Enhanced Dweller class for v5.0
@dataclass
class Dweller:
    """Enhanced dweller with relationships and breeding"""
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
    weapon: Optional[str] = None
    outfit: Optional[str] = None
    # AI Personality (v3.0)
    personality_outlook: str = "Pragmatic"
    personality_work_ethic: str = "Hardworking"
    personality_social: str = "Friendly"
    personality_courage: str = "Cautious"
    recent_dialogue: str = ""
    # Progression (v4.0)
    learned_skills: List[str] = field(default_factory=list)
    experience: int = 0
    level: int = 1
    on_expedition: bool = False
    expedition_return_day: int = 0
    # NEW v5.0: Relationships & Breeding
    age: int = 25  # years
    gender: str = "M"  # M or F
    parent1: Optional[str] = None  # parent names
    parent2: Optional[str] = None
    is_child: bool = False
    child_grow_day: Optional[int] = None  # day when child becomes adult
    relationships: Dict[str, int] = field(default_factory=dict)  # dweller_name: affection (0-100)
    partner: Optional[str] = None
    pregnant: bool = False
    due_day: Optional[int] = None

    def get_stat(self, stat_name: str) -> int:
        """Get SPECIAL stat with equipment bonuses"""
        base_stat = getattr(self, stat_name.lower(), 5)
        bonus = 0
        if self.outfit and self.outfit in EQUIPMENT_LIBRARY:
            outfit = EQUIPMENT_LIBRARY[self.outfit]
            bonus += outfit.stat_bonus.get(stat_name.lower(), 0)
        return min(10, base_stat + bonus)

    def get_combat_power(self) -> int:
        """Combat power with skills"""
        weapon_damage = 0
        if self.weapon and self.weapon in EQUIPMENT_LIBRARY:
            weapon_damage = EQUIPMENT_LIBRARY[self.weapon].damage

        base_power = self.get_stat("strength") + weapon_damage

        if "sharp_shooter" in self.learned_skills:
            base_power = int(base_power * (1 + SKILL_LIBRARY["sharp_shooter"].bonus_value))
        if "tank" in self.learned_skills:
            base_power = int(base_power * 1.2)

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

    def add_experience(self, amount: int):
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
        """Get personality"""
        return f"{self.personality_outlook}, {self.personality_work_ethic}, {self.personality_social}, {self.personality_courage}"

    def modify_stat(self, stat_name: str, amount: int):
        """Modify SPECIAL"""
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


@dataclass
class Room:
    """Enhanced room"""
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

    def get_production(self, dwellers_list: List[Dweller], adjacency_bonus: float = 0.0, 
                      tech_bonuses: Dict[str, float] = None, policy_bonuses: Dict[str, float] = None) -> Dict[str, int]:
        """Calculate production with ALL bonuses"""
        if self.room_type == RoomType.EMPTY or self.under_construction or self.on_fire or self.has_incident:
            return {}

        config = ROOM_CONFIGS.get(self.room_type)
        if not config or not config.production:
            return {}

        production = config.production.copy()
        base_multiplier = self.level
        worker_count = len(self.assigned_dwellers)

        if worker_count > 0 or config.room_type == RoomType.GARDEN:  # Garden works without workers
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

            # NEW v5.0: Tech bonuses
            tech_mult = 1.0
            if tech_bonuses:
                resource_type = list(production.keys())[0] if production else None
                if resource_type == "power":
                    tech_mult *= tech_bonuses.get("production_power_mult", 1.0)
                elif resource_type == "water":
                    tech_mult *= tech_bonuses.get("production_water_mult", 1.0)
                elif resource_type == "food":
                    tech_mult *= tech_bonuses.get("production_food_mult", 1.0)

            # NEW v5.0: Policy bonuses
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
        """Can rush"""
        return (self.rush_cooldown == 0 and
                not self.under_construction and
                not self.on_fire and
                not self.has_incident and
                len(self.assigned_dwellers) > 0 and
                self.room_type in [RoomType.POWER_GENERATOR, RoomType.WATER_TREATMENT, 
                                  RoomType.DINER, RoomType.GARDEN, RoomType.WORKSHOP])


@dataclass
class Resources:
    """Vault resources"""
    power: int = 20
    power_max: int = 30
    water: int = 20
    water_max: int = 30
    food: int = 20
    food_max: int = 30
    caps: int = 500
    # NEW v5.0 resources
    research: int = 0  # research points
    influence: int = 0  # for policies and radio
    materials: int = 0  # crafting materials
    metal: int = 0
    electronics: int = 0
    cloth: int = 0

    def add(self, resource: str, amount: int):
        """Add resource"""
        if resource in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            current = getattr(self, resource)
            setattr(self, resource, current + amount)
        else:
            current = getattr(self, resource)
            max_val = getattr(self, f"{resource}_max")
            setattr(self, resource, min(max_val, current + amount))

    def remove(self, resource: str, amount: int) -> bool:
        """Remove resource"""
        current = getattr(self, resource, 0)
        if current >= amount:
            setattr(self, resource, current - amount)
            return True
        return False

    def consume_with_rationing(self, resource: str, amount: int) -> int:
        """Consume with rationing"""
        current = getattr(self, resource)
        actual = min(current, amount)
        setattr(self, resource, current - actual)
        return actual

    def has_enough(self, resource: str, amount: int) -> bool:
        """Check if enough"""
        return getattr(self, resource, 0) >= amount

    def is_critical(self, resource: str) -> bool:
        """Check critical"""
        if resource in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            return getattr(self, resource, 0) < 50
        current = getattr(self, resource)
        max_val = getattr(self, f"{resource}_max")
        return current < max_val * 0.2


# Quest, Expedition, Objective (from v4.0 - keeping same)
@dataclass
class Quest:
    """AI-generated quest"""
    id: str
    title: str
    description: str
    status: QuestStatus = QuestStatus.ACTIVE
    current_step: int = 0
    steps: List[Dict] = field(default_factory=list)
    rewards: Dict[str, int] = field(default_factory=dict)
    created_day: int = 1
    faction: Optional[FactionType] = None  # NEW v5.0: faction quests

    def get_current_step_text(self) -> str:
        if self.current_step < len(self.steps):
            return self.steps[self.current_step].get("description", "")
        return "Quest completed!"

    def advance_step(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.status = QuestStatus.COMPLETED


@dataclass
class Expedition:
    """Wasteland expedition"""
    dweller_name: str
    destination: str
    duration: int
    return_day: int
    difficulty: int
    potential_loot: List[str] = field(default_factory=list)

    def is_complete(self, current_day: int) -> bool:
        return current_day >= self.return_day


@dataclass
class VaultObjective:
    """Victory objective"""
    objective_type: ObjectiveType
    description: str
    requirements: Dict[str, any]
    progress: Dict[str, any] = field(default_factory=dict)
    completed: bool = False

    def check_completion(self, game) -> bool:
        """Check completion"""
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
        elif self.objective_type == ObjectiveType.RESEARCH:  # NEW
            return game.resources.research >= 5000
        return False


# (Continue with AI helpers and game class...)
# =============================================================================
# AI HELPER FUNCTIONS (Enhanced from v4.0)
# =============================================================================

def call_ai_model(prompt: str, max_tokens: int = 500, system_prompt: str = "") -> str:
    """Call AI with fallback"""
    if not AI_ENABLED:
        return generate_fallback_response(prompt)
    try:
        messages = [{"role": "user", "content": prompt}]
        response = ai_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "You are the AI assistant for Vault 13.",
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        return generate_fallback_response(prompt)


def generate_fallback_response(prompt: str) -> str:
    """Fallback responses"""
    prompt_lower = prompt.lower()
    if "dialogue" in prompt_lower or "comment" in prompt_lower:
        return random.choice([
            "Another day in the vault. Could be worse.",
            "Just doing my part to keep everyone alive.",
            "I wonder what the surface looks like now...",
            "At least we have each other down here.",
        ])
    elif "quest" in prompt_lower:
        return json.dumps({
            "title": "Demo Quest",
            "description": "[AI disabled]",
            "steps": [{"description": "Complete demo objective", "type": "demo"}],
            "rewards": {"caps": 100}
        })
    elif "advisor" in prompt_lower:
        return "⚠️ AI disabled. Set ANTHROPIC_API_KEY to enable full advisor."
    else:
        return "[AI unavailable]"


def generate_quest(game) -> Quest:
    """Generate AI quest"""
    if not AI_ENABLED:
        return Quest(
            id=f"quest_{game.day}",
            title="Resource Shortage",
            description="Gather resources to survive.",
            steps=[{"description": "Accumulate 50 food", "type": "resource"}],
            rewards={"caps": 200},
            created_day=game.day
        )
    
    vault_state = {
        "day": game.day,
        "dwellers": len(game.dwellers),
        "caps": game.resources.caps,
        "government": game.government.value if game.government else "None"
    }
    
    prompt = f"""Generate a Fallout-style vault quest.
Vault State: {json.dumps(vault_state)}

Return ONLY valid JSON:
{{
    "title": "Quest Name",
    "description": "Brief description",
    "steps": [{{"description": "Step 1", "type": "resource"}}],
    "rewards": {{"caps": 100}}
}}"""
    
    try:
        response = call_ai_model(prompt, max_tokens=300)
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            quest_data = json.loads(response[json_start:json_end])
            return Quest(
                id=f"quest_{game.day}_{random.randint(1000, 9999)}",
                title=quest_data["title"],
                description=quest_data["description"],
                steps=quest_data["steps"],
                rewards=quest_data.get("rewards", {"caps": 100}),
                created_day=game.day
            )
    except:
        pass
    
    return Quest(id=f"quest_{game.day}", title="Vault Emergency", 
                description="Handle crisis.", steps=[{"description": "Survive", "type": "survival"}],
                rewards={"caps": 150}, created_day=game.day)


def get_dweller_dialogue(dweller: Dweller, context: str, game_state: dict) -> str:
    """Generate dweller dialogue"""
    if not AI_ENABLED:
        return generate_fallback_response("dialogue")
    
    prompt = f"""Generate a short comment (1-2 sentences) for this dweller.

Dweller: {dweller.name} (Age {dweller.age}, {dweller.gender})
Personality: {dweller.get_personality_summary()}
Health: {dweller.health}% | Happiness: {dweller.happiness}%
{"Child (cannot work)" if dweller.is_child else f"Level {dweller.level}"}
Context: {context}

Generate a witty, Fallout-themed comment. No quotes."""
    
    return call_ai_model(prompt, max_tokens=100)


# (Continuing with massive game class - this will be the largest class yet!)
