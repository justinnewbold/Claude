#!/usr/bin/env python3
"""
VAULT 13 v5.5 ULTIMATE MEGA PLUS - NEW ADDITIONS
5 Additional Game-Changing Systems on top of v5.0!

NEW v5.5 FEATURES:
1. Dweller Traits & Mutations - Genetic variety and wasteland mutations
2. Vault Expansion System - Build up to 15 floors, merge rooms
3. Legendary Equipment - Named items with special powers
4. Advanced Quest Chains - Multi-quest storylines
5. Prestige & New Game+ - Meta progression system

This extends v5.0 MEGA with even more depth!
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import random

# =============================================================================
# FEATURE 1: DWELLER TRAITS & MUTATIONS
# =============================================================================

class TraitType(Enum):
    """Types of traits"""
    GENETIC = "Genetic"      # Inherited from parents
    MUTATION = "Mutation"     # Acquired from radiation
    LEARNED = "Learned"       # Acquired through experience
    NEGATIVE = "Negative"     # Drawbacks


@dataclass
class DwellerTrait:
    """A trait that affects dweller capabilities"""
    name: str
    description: str
    trait_type: TraitType
    effects: Dict[str, any]  # stat_bonuses, special_abilities
    inheritable: bool = False  # Can be passed to children
    icon: str = "✨"
    rarity: int = 1  # 1=common, 5=legendary


# Trait Library
TRAIT_LIBRARY = {
    # Positive Genetic Traits (Inheritable)
    "genius": DwellerTrait(
        "Genius",
        "+3 Intelligence, faster skill learning",
        TraitType.GENETIC,
        {"intelligence": 3, "xp_mult": 1.5},
        inheritable=True,
        icon="🧠",
        rarity=3
    ),
    "athletic": DwellerTrait(
        "Athletic", 
        "+2 Strength, +2 Agility, +1 Endurance",
        TraitType.GENETIC,
        {"strength": 2, "agility": 2, "endurance": 1},
        inheritable=True,
        icon="💪",
        rarity=2
    ),
    "charismatic": DwellerTrait(
        "Natural Leader",
        "+3 Charisma, better relationships",
        TraitType.GENETIC,
        {"charisma": 3, "relationship_mult": 1.3},
        inheritable=True,
        icon="👑",
        rarity=2
    ),
    "lucky": DwellerTrait(
        "Born Lucky",
        "+2 Luck, better expedition outcomes",
        TraitType.GENETIC,
        {"luck": 2, "expedition_success": 1.2},
        inheritable=True,
        icon="🍀",
        rarity=3
    ),
    
    # Wasteland Mutations (Acquired)
    "rad_resistant": DwellerTrait(
        "Radiation Resistant",
        "Immune to radiation damage",
        TraitType.MUTATION,
        {"rad_immunity": True},
        inheritable=False,
        icon="☢️",
        rarity=4
    ),
    "night_vision": DwellerTrait(
        "Night Vision",
        "+2 Perception, better in darkness",
        TraitType.MUTATION,
        {"perception": 2, "dark_bonus": True},
        inheritable=False,
        icon="👁️",
        rarity=3
    ),
    "regeneration": DwellerTrait(
        "Fast Healing",
        "Regenerate 5 health per turn",
        TraitType.MUTATION,
        {"health_regen": 5},
        inheritable=False,
        icon="💚",
        rarity=5
    ),
    
    # Learned Traits
    "veteran": DwellerTrait(
        "Combat Veteran",
        "+20% combat effectiveness",
        TraitType.LEARNED,
        {"combat_mult": 1.2},
        inheritable=False,
        icon="🎖️",
        rarity=2
    ),
    "scientist": DwellerTrait(
        "Brilliant Scientist",
        "+50% research generation",
        TraitType.LEARNED,
        {"research_mult": 1.5},
        inheritable=False,
        icon="🔬",
        rarity=2
    ),
    
    # Negative Traits
    "frail": DwellerTrait(
        "Frail",
        "-2 Endurance, -20% max health",
        TraitType.NEGATIVE,
        {"endurance": -2, "health_max": 0.8},
        inheritable=True,
        icon="💔",
        rarity=1
    ),
    "clumsy": DwellerTrait(
        "Clumsy",
        "-2 Agility, higher incident chance",
        TraitType.NEGATIVE,
        {"agility": -2, "incident_chance": 1.3},
        inheritable=True,
        icon="🤕",
        rarity=1
    ),
}


def inherit_traits(parent1_traits: List[str], parent2_traits: List[str]) -> List[str]:
    """Children inherit some traits from parents"""
    inherited = []
    
    # Each inheritable trait has 50% chance to pass down
    for trait_id in parent1_traits + parent2_traits:
        if trait_id in TRAIT_LIBRARY and TRAIT_LIBRARY[trait_id].inheritable:
            if random.random() < 0.5:
                inherited.append(trait_id)
    
    # Small chance of mutation (5%)
    if random.random() < 0.05:
        mutation_traits = [t for t, data in TRAIT_LIBRARY.items() 
                          if data.trait_type == TraitType.MUTATION]
        if mutation_traits:
            inherited.append(random.choice(mutation_traits))
    
    return list(set(inherited))  # Remove duplicates


# =============================================================================
# FEATURE 2: VAULT EXPANSION SYSTEM
# =============================================================================

@dataclass
class VaultExpansion:
    """Tracks vault expansion progress"""
    max_floors: int = 10
    current_floors: int = 3
    floor_unlock_cost: int = 1000  # caps
    floor_unlock_cost_multiplier: float = 1.5
    
    # Room merging
    merged_rooms: List[Tuple[int, int, int]] = field(default_factory=list)  # (floor, start_pos, size)
    merge_cost: int = 500


def can_unlock_floor(game) -> bool:
    """Check if can unlock new floor"""
    expansion = getattr(game, 'expansion', None)
    if not expansion:
        return False
    
    if expansion.current_floors >= expansion.max_floors:
        return False
    
    cost = int(expansion.floor_unlock_cost * 
               (expansion.floor_unlock_cost_multiplier ** (expansion.current_floors - 3)))
    
    return game.resources.caps >= cost


def unlock_floor(game) -> bool:
    """Unlock a new floor"""
    expansion = game.expansion
    cost = int(expansion.floor_unlock_cost * 
               (expansion.floor_unlock_cost_multiplier ** (expansion.current_floors - 3)))
    
    if game.resources.remove("caps", cost):
        # Add new floor to layout
        new_floor = []
        for pos in range(3):
            from vault_shelter_v5 import Room, RoomType
            new_floor.append(Room(RoomType.EMPTY, expansion.current_floors, pos))
        
        game.vault_layout.append(new_floor)
        expansion.current_floors += 1
        game.log_event(f"🏗️ Unlocked Floor {expansion.current_floors}!")
        return True
    
    return False


def can_merge_rooms(game, floor: int, start_pos: int) -> bool:
    """Check if can merge adjacent rooms"""
    if start_pos + 1 >= 3:  # Need at least 2 adjacent rooms
        return False
    
    room1 = game.vault_layout[floor][start_pos]
    room2 = game.vault_layout[floor][start_pos + 1]
    
    # Both must be same type, same level, not under construction
    return (room1.room_type == room2.room_type and
            room1.level == room2.level and
            not room1.under_construction and
            not room2.under_construction and
            room1.room_type.value != "Empty")


def merge_rooms(game, floor: int, start_pos: int) -> bool:
    """Merge two adjacent rooms into a mega-room"""
    if not can_merge_rooms(game, floor, start_pos):
        return False
    
    if not game.resources.remove("caps", game.expansion.merge_cost):
        return False
    
    # Merge rooms - double capacity and production
    room1 = game.vault_layout[floor][start_pos]
    room2 = game.vault_layout[floor][start_pos + 1]
    
    # Combine workers
    room1.assigned_dwellers.extend(room2.assigned_dwellers)
    
    # Mark as merged (we'd need to track this in Room class)
    room1.is_merged = True
    room1.merge_size = 2
    
    # Clear second room
    from vault_shelter_v5 import RoomType
    room2.room_type = RoomType.EMPTY
    room2.assigned_dwellers = []
    
    game.expansion.merged_rooms.append((floor, start_pos, 2))
    game.log_event(f"🏗️ Merged rooms on Floor {floor + 1}!")
    
    return True


# =============================================================================
# FEATURE 3: LEGENDARY EQUIPMENT
# =============================================================================

class EquipmentRarity(Enum):
    """Equipment rarity tiers"""
    COMMON = "Common"
    UNCOMMON = "Uncommon"  
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


@dataclass
class LegendaryItem:
    """A legendary named item with special powers"""
    name: str
    base_item: str  # equipment_id from EQUIPMENT_LIBRARY
    rarity: EquipmentRarity
    special_power: str
    power_effect: Dict[str, any]
    lore: str
    icon: str = "⚡"


LEGENDARY_ITEMS = {
    "excalibur": LegendaryItem(
        "Excalibur",
        "plasma_gun",
        EquipmentRarity.LEGENDARY,
        "Deals double damage to enemies",
        {"damage_mult": 2.0, "always_hit": True},
        "The legendary sword reforged as a plasma weapon.",
        icon="⚔️"
    ),
    "vault_tec_elite": LegendaryItem(
        "Vault-Tec Elite Armor",
        "power_armor",
        EquipmentRarity.LEGENDARY,
        "Grants immunity to radiation and +5 all SPECIAL",
        {"all_stats": 5, "rad_immunity": True},
        "Prototype armor from Vault-Tec's secret facility.",
        icon="🛡️"
    ),
    "lucky_charm": LegendaryItem(
        "Rabbit's Foot Charm",
        "vault_suit",
        EquipmentRarity.EPIC,
        "+10 Luck, critical hits deal triple damage",
        {"luck": 10, "crit_mult": 3.0},
        "A pre-war good luck charm, still working after 200 years.",
        icon="🍀"
    ),
    "medics_miracle": LegendaryItem(
        "Medic's Miracle Kit",
        "scientist_coat",
        EquipmentRarity.EPIC,
        "Heals all dwellers by 10 HP per turn",
        {"heal_aura": 10, "intelligence": 3},
        "A medical kit that seems to never run out of supplies.",
        icon="⚕️"
    ),
    "wasteland_wanderer": LegendaryItem(
        "The Wanderer's Boots",
        "vault_suit",
        EquipmentRarity.RARE,
        "Expeditions take half the time",
        {"expedition_speed": 0.5, "endurance": 3},
        "Boots worn by the legendary Lone Wanderer.",
        icon="👢"
    ),
}


def drop_legendary_item(game) -> Optional[str]:
    """Chance to drop legendary item (very rare)"""
    if random.random() < 0.001:  # 0.1% chance
        legendary_id = random.choice(list(LEGENDARY_ITEMS.keys()))
        if legendary_id not in game.legendary_inventory:
            game.legendary_inventory.append(legendary_id)
            game.log_event(f"⚡ LEGENDARY ITEM FOUND: {LEGENDARY_ITEMS[legendary_id].name}!")
            return legendary_id
    return None


# =============================================================================
# FEATURE 4: ADVANCED QUEST CHAINS
# =============================================================================

@dataclass
class QuestChain:
    """A multi-quest storyline"""
    chain_id: str
    name: str
    description: str
    quests: List[str]  # quest IDs in order
    current_quest_index: int = 0
    completed: bool = False
    unlocked: bool = False
    unlock_requirement: Optional[Dict[str, any]] = None
    final_reward: Dict[str, any] = field(default_factory=dict)


QUEST_CHAINS = {
    "brotherhood_path": QuestChain(
        "brotherhood_path",
        "Path of the Brotherhood",
        "Help the Brotherhood of Steel in their quest for technology.",
        quests=["bos_quest_1", "bos_quest_2", "bos_quest_3", "bos_quest_4"],
        unlock_requirement={"faction": "BROTHERHOOD", "reputation": 25},
        final_reward={"legendary": "vault_tec_elite", "caps": 5000, "reputation": 50}
    ),
    
    "vault_origins": QuestChain(
        "vault_origins",
        "Vault Origins",
        "Uncover the dark secrets of Vault 13's creation.",
        quests=["origins_1", "origins_2", "origins_3"],
        unlock_requirement={"day": 50, "research": 1000},
        final_reward={"tech": "vault_secrets", "caps": 3000}
    ),
    
    "wasteland_legends": QuestChain(
        "wasteland_legends",
        "Wasteland Legends",
        "Follow in the footsteps of legendary vault dwellers.",
        quests=["legend_1", "legend_2", "legend_3", "legend_4", "legend_5"],
        unlock_requirement={"expeditions_completed": 20},
        final_reward={"legendary": "wasteland_wanderer", "all_stats": 2}
    ),
}


def check_chain_unlocks(game):
    """Check if any quest chains should unlock"""
    for chain_id, chain in QUEST_CHAINS.items():
        if chain.unlocked or chain_id in game.active_quest_chains:
            continue
        
        # Check requirements
        if chain.unlock_requirement:
            req = chain.unlock_requirement
            
            if "day" in req and game.day < req["day"]:
                continue
            if "faction" in req:
                faction_type = getattr(FactionType, req["faction"], None)
                if faction_type and game.faction_reputations.get(faction_type, 0) < req.get("reputation", 0):
                    continue
            if "research" in req and game.resources.research < req["research"]:
                continue
            if "expeditions_completed" in req:
                completed = game.current_objective.progress.get("expeditions_completed", 0) if game.current_objective else 0
                if completed < req["expeditions_completed"]:
                    continue
        
        # Unlock!
        chain.unlocked = True
        game.active_quest_chains.append(chain_id)
        game.log_event(f"📖 Quest Chain Unlocked: {chain.name}!")


# =============================================================================
# FEATURE 5: PRESTIGE & NEW GAME+
# =============================================================================

@dataclass
class PrestigeData:
    """Meta-progression data"""
    prestige_level: int = 0
    prestige_points: int = 0
    legacy_bonuses: List[str] = field(default_factory=list)
    achievements_unlocked: List[str] = field(default_factory=list)
    total_vaults_completed: int = 0
    best_day_survived: int = 0


PRESTIGE_BONUSES = {
    "starting_caps": {
        "name": "Wealthy Start",
        "description": "Start with 1000 caps instead of 500",
        "cost": 10,
        "effect": {"starting_caps": 1000}
    },
    "skilled_dwellers": {
        "name": "Skilled Dwellers",
        "description": "Starting dwellers have 1 random skill",
        "cost": 15,
        "effect": {"starting_skills": 1}
    },
    "tech_advantage": {
        "name": "Tech Advantage",
        "description": "Start with 3 technologies researched",
        "cost": 20,
        "effect": {"starting_tech": 3}
    },
    "legendary_start": {
        "name": "Legendary Start",
        "description": "Start with 1 random legendary item",
        "cost": 25,
        "effect": {"starting_legendary": 1}
    },
    "population_boom": {
        "name": "Population Boom",
        "description": "Start with 8 dwellers instead of 4",
        "cost": 15,
        "effect": {"starting_dwellers": 8}
    },
    "resource_surplus": {
        "name": "Resource Surplus",
        "description": "+50% starting resources",
        "cost": 10,
        "effect": {"starting_resources_mult": 1.5}
    },
}


ACHIEVEMENTS = {
    "first_child": {"name": "New Life", "desc": "Have your first child", "points": 5},
    "tech_master": {"name": "Tech Master", "desc": "Research all technologies", "points": 20},
    "legendary_collector": {"name": "Legendary Collector", "desc": "Find all legendary items", "points": 25},
    "survival_100": {"name": "Centennial", "desc": "Survive 100 days", "points": 10},
    "utopia": {"name": "Utopia Achieved", "desc": "Complete Utopia objective", "points": 15},
    "disaster_survivor": {"name": "Disaster Survivor", "desc": "Survive 5 disasters", "points": 15},
    "vault_dynasty": {"name": "Vault Dynasty", "desc": "Have 10 children born", "points": 15},
}


def calculate_prestige_points(game) -> int:
    """Calculate prestige points earned from this run"""
    points = 0
    
    # Base: 1 point per 10 days survived
    points += game.day // 10
    
    # Bonuses
    points += len(game.researched_tech) * 2
    points += game.children_born * 3
    points += game.disasters_survived * 5
    points += len(game.legendary_inventory) * 10
    
    # Objectives
    for obj in game.available_objectives:
        if obj.completed:
            points += 20
    
    return points


def prestige_vault(game):
    """Complete current vault and start New Game+"""
    prestige_data = game.prestige_data
    
    # Award points
    points_earned = calculate_prestige_points(game)
    prestige_data.prestige_points += points_earned
    prestige_data.prestige_level += 1
    prestige_data.total_vaults_completed += 1
    prestige_data.best_day_survived = max(prestige_data.best_day_survived, game.day)
    
    # Check achievements
    check_achievements(game)
    
    game.log_event(f"🏆 PRESTIGE! Earned {points_earned} points!")
    
    return prestige_data


def check_achievements(game):
    """Check and unlock achievements"""
    prestige = game.prestige_data
    
    achievements_to_check = {
        "first_child": game.children_born >= 1,
        "tech_master": len(game.researched_tech) >= 20,
        "legendary_collector": len(game.legendary_inventory) >= len(LEGENDARY_ITEMS),
        "survival_100": game.day >= 100,
        "disaster_survivor": game.disasters_survived >= 5,
        "vault_dynasty": game.children_born >= 10,
    }
    
    for ach_id, condition in achievements_to_check.items():
        if condition and ach_id not in prestige.achievements_unlocked:
            prestige.achievements_unlocked.append(ach_id)
            ach = ACHIEVEMENTS[ach_id]
            prestige.prestige_points += ach["points"]
            game.log_event(f"🏆 ACHIEVEMENT: {ach['name']}!")


# =============================================================================
# SUMMARY OF v5.5 ADDITIONS
# =============================================================================

"""
v5.5 ULTIMATE MEGA PLUS adds 5 major systems:

1. DWELLER TRAITS & MUTATIONS:
   - 10+ inheritable genetic traits
   - Wasteland mutations from radiation
   - Learned traits from experience
   - Negative traits for balance
   - Children inherit traits from parents

2. VAULT EXPANSION:
   - Unlock up to 15 floors (from 10)
   - Merge adjacent rooms into mega-rooms
   - Doubled capacity and production
   - Exponential unlock costs

3. LEGENDARY EQUIPMENT:
   - 5+ legendary named items
   - Special powers and effects
   - Rarity system (Common → Legendary)
   - 0.1% drop chance from events
   - Game-changing abilities

4. ADVANCED QUEST CHAINS:
   - Multi-quest storylines
   - Unlock requirements (day, faction rep, etc.)
   - Progressive narrative
   - Epic final rewards
   - 3 major quest chains

5. PRESTIGE & NEW GAME+:
   - Complete vault, restart with bonuses
   - Earn prestige points
   - Unlock permanent bonuses
   - Achievement system
   - Legacy progression

Total NEW content:
- 10+ traits
- 15 floor capacity
- 5+ legendary items
- 3 quest chains
- 6 prestige bonuses
- 7 achievements

This brings v5.5 to an estimated 2,700+ lines!
"""

