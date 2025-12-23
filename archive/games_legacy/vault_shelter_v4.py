#!/usr/bin/env python3
"""
VAULT 13 - SURVIVAL PROTOCOL v4.0 ULTIMATE EDITION
A vault management simulation with AI-powered features and advanced gameplay

NEW v4.0 FEATURES:
- AI Quest Generator - Procedural multi-turn story campaigns
- Wasteland Exploration - Send dwellers on expeditions
- Vault Objectives - Multiple victory conditions
- Dweller Skills - RPG progression system
- Room Adjacency - Spatial strategy bonuses

v3.0 FEATURES:
- AI Overseer Advisor
- Dweller Personalities & Dialogue
- Natural Language Commands

v2.0 FEATURES:
- Rush Production, Room Upgrades, Active Combat
- Equipment System, Smart Rationing
- Enhanced Visualization

REQUIRES: pip install anthropic (or runs in demo mode without API key)
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

# AI Integration - graceful fallback if not available
AI_ENABLED = False
try:
    import anthropic
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    if API_KEY:
        ai_client = anthropic.Anthropic(api_key=API_KEY)
        AI_ENABLED = True
        print("🤖 AI Features: ENABLED")
    else:
        print("⚠️  AI Features: DISABLED (set ANTHROPIC_API_KEY environment variable to enable)")
except ImportError:
    print("⚠️  AI Features: DISABLED (install anthropic: pip install anthropic)")


class C:
    """ANSI Color codes for terminal styling"""
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
    AI = '\033[38;5;129m'  # Purple for AI
    QUEST = '\033[38;5;213m'  # Pink for quests
    SKILL = '\033[38;5;190m'  # Yellow-green for skills

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


class RoomType(Enum):
    """Types of rooms that can be built in the vault"""
    EMPTY = "Empty"
    POWER_GENERATOR = "Power Generator"
    WATER_TREATMENT = "Water Treatment"
    DINER = "Diner"
    LIVING_QUARTERS = "Living Quarters"
    TRAINING_ROOM = "Training Room"
    STORAGE_ROOM = "Storage Room"
    MEDBAY = "Medbay"
    SCIENCE_LAB = "Science Lab"


class EquipmentType(Enum):
    """Types of equipment"""
    WEAPON = "Weapon"
    OUTFIT = "Outfit"


class QuestStatus(Enum):
    """Quest status"""
    ACTIVE = "Active"
    COMPLETED = "Completed"
    FAILED = "Failed"


class ObjectiveType(Enum):
    """Victory condition types"""
    UTOPIA = "Utopia"  # Achieve perfect happiness
    ECONOMIC = "Economic"  # Accumulate wealth
    RESEARCH = "Research"  # Complete science goals
    MILITARY = "Military"  # Build strong defenses
    EXODUS = "Exodus"  # Successfully evacuate to surface
    SURVIVAL = "Survival"  # Survive X days


# Personality trait options
PERSONALITY_TRAITS = {
    "outlook": ["Optimistic", "Pessimistic", "Pragmatic", "Cynical"],
    "work_ethic": ["Hardworking", "Lazy", "Ambitious", "Laid-back"],
    "social": ["Friendly", "Reserved", "Charismatic", "Awkward"],
    "courage": ["Brave", "Cautious", "Reckless", "Cowardly"]
}


# NEW v4.0: Dweller Skills System
@dataclass
class Skill:
    """A learnable skill that provides bonuses"""
    name: str
    description: str
    stat_requirement: Dict[str, int]  # e.g., {"strength": 5, "intelligence": 3}
    bonus_type: str  # production, combat, happiness, etc.
    bonus_value: float
    icon: str = "⭐"


SKILL_LIBRARY = {
    # Production Skills
    "power_expert": Skill(
        "Power Expert",
        "Increases power production by 30%",
        {"strength": 6, "intelligence": 5},
        "production_power",
        0.3,
        "⚡"
    ),
    "water_purifier": Skill(
        "Water Purifier",
        "Increases water production by 30%",
        {"perception": 6, "intelligence": 5},
        "production_water",
        0.3,
        "💧"
    ),
    "master_chef": Skill(
        "Master Chef",
        "Increases food production by 30%",
        {"agility": 6, "charisma": 5},
        "production_food",
        0.3,
        "🍖"
    ),

    # Combat Skills
    "sharp_shooter": Skill(
        "Sharp Shooter",
        "Increases weapon damage by 50%",
        {"perception": 7, "agility": 6},
        "combat_damage",
        0.5,
        "🎯"
    ),
    "tank": Skill(
        "Tank",
        "Reduces damage taken by 30%",
        {"strength": 7, "endurance": 7},
        "combat_defense",
        0.3,
        "🛡️"
    ),

    # Exploration Skills
    "wasteland_survivor": Skill(
        "Wasteland Survivor",
        "Reduces exploration time by 25%",
        {"endurance": 6, "luck": 6},
        "exploration_speed",
        0.25,
        "🏜️"
    ),
    "scavenger": Skill(
        "Scavenger",
        "Finds 50% more loot",
        {"perception": 6, "luck": 7},
        "exploration_loot",
        0.5,
        "🔍"
    ),

    # Utility Skills
    "leader": Skill(
        "Leader",
        "Boosts nearby dwellers' happiness by 10%",
        {"charisma": 8, "intelligence": 6},
        "happiness_aura",
        0.1,
        "👑"
    ),
    "medic": Skill(
        "Medic",
        "Heals faster and can treat others",
        {"intelligence": 7, "charisma": 5},
        "healing",
        0.3,
        "⚕️"
    ),
}


@dataclass
class Equipment:
    """Equipment that can be given to dwellers"""
    name: str
    equipment_type: EquipmentType
    stat_bonus: Dict[str, int] = field(default_factory=dict)
    damage: int = 0
    icon: str = "⚔️"

    def get_description(self) -> str:
        if self.equipment_type == EquipmentType.WEAPON:
            return f"Damage: {self.damage}"
        else:
            bonuses = ", ".join([f"+{v} {k.upper()[0]}" for k, v in self.stat_bonus.items()])
            return f"Bonuses: {bonuses}"


# Equipment library
EQUIPMENT_LIBRARY = {
    "rusty_pistol": Equipment("Rusty Pistol", EquipmentType.WEAPON, damage=5, icon="🔫"),
    "laser_rifle": Equipment("Laser Rifle", EquipmentType.WEAPON, damage=15, icon="⚡"),
    "plasma_gun": Equipment("Plasma Gun", EquipmentType.WEAPON, damage=25, icon="💚"),
    "vault_suit": Equipment("Vault Suit", EquipmentType.OUTFIT, stat_bonus={"endurance": 1}, icon="👔"),
    "scientist_coat": Equipment("Scientist Coat", EquipmentType.OUTFIT, stat_bonus={"intelligence": 2}, icon="🥼"),
    "power_armor": Equipment("Power Armor", EquipmentType.OUTFIT, stat_bonus={"strength": 3, "endurance": 2}, icon="🛡️"),
}


@dataclass
class RoomStats:
    """Stats for different room types"""
    cost: int
    production: Dict[str, int]
    capacity: int
    stat_required: Optional[str] = None
    description: str = ""
    upgrade_cost_multiplier: float = 1.5


ROOM_CONFIGS = {
    RoomType.POWER_GENERATOR: RoomStats(
        cost=150,
        production={"power": 5},
        capacity=2,
        stat_required="strength",
        description="Generates electrical power for the vault"
    ),
    RoomType.WATER_TREATMENT: RoomStats(
        cost=120,
        production={"water": 5},
        capacity=2,
        stat_required="perception",
        description="Purifies water for dwellers"
    ),
    RoomType.DINER: RoomStats(
        cost=100,
        production={"food": 5},
        capacity=2,
        stat_required="agility",
        description="Produces food to feed dwellers"
    ),
    RoomType.LIVING_QUARTERS: RoomStats(
        cost=100,
        production={},
        capacity=4,
        description="Houses dwellers and increases population cap"
    ),
    RoomType.TRAINING_ROOM: RoomStats(
        cost=200,
        production={},
        capacity=2,
        description="Train dwellers to improve their stats"
    ),
    RoomType.STORAGE_ROOM: RoomStats(
        cost=80,
        production={},
        capacity=0,
        description="Increases resource storage capacity"
    ),
    RoomType.MEDBAY: RoomStats(
        cost=150,
        production={},
        capacity=2,
        description="Heals injured dwellers"
    ),
    RoomType.SCIENCE_LAB: RoomStats(
        cost=250,
        production={},
        capacity=2,
        stat_required="intelligence",
        description="Research new technologies"
    ),
}


# NEW v4.0: Room Adjacency Bonuses
ADJACENCY_BONUSES = {
    # Same-type rooms get efficiency bonus
    (RoomType.POWER_GENERATOR, RoomType.POWER_GENERATOR): {"production_bonus": 0.15, "name": "Power Grid"},
    (RoomType.WATER_TREATMENT, RoomType.WATER_TREATMENT): {"production_bonus": 0.15, "name": "Water Network"},
    (RoomType.DINER, RoomType.DINER): {"production_bonus": 0.15, "name": "Kitchen Complex"},

    # Synergistic combinations
    (RoomType.SCIENCE_LAB, RoomType.POWER_GENERATOR): {"production_bonus": 0.10, "name": "Research Power"},
    (RoomType.MEDBAY, RoomType.LIVING_QUARTERS): {"happiness_bonus": 5, "name": "Healthcare Access"},
    (RoomType.TRAINING_ROOM, RoomType.LIVING_QUARTERS): {"happiness_bonus": 3, "name": "Fitness Center"},
    (RoomType.STORAGE_ROOM, RoomType.DINER): {"production_bonus": 0.10, "name": "Kitchen Storage"},
}


@dataclass
class Dweller:
    """A vault dweller with SPECIAL stats, skills, and AI personality"""
    name: str
    strength: int = 5
    perception: int = 5
    endurance: int = 5
    charisma: int = 5
    intelligence: int = 5
    agility: int = 5
    luck: int = 5
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

    # NEW v4.0: Skills and Progression
    learned_skills: List[str] = field(default_factory=list)
    experience: int = 0
    level: int = 1

    # NEW v4.0: Exploration
    on_expedition: bool = False
    expedition_return_day: int = 0

    def get_stat(self, stat_name: str) -> int:
        """Get a specific SPECIAL stat with equipment bonuses"""
        base_stat = getattr(self, stat_name.lower(), 5)
        bonus = 0

        if self.outfit and self.outfit in EQUIPMENT_LIBRARY:
            outfit = EQUIPMENT_LIBRARY[self.outfit]
            bonus += outfit.stat_bonus.get(stat_name.lower(), 0)

        return min(10, base_stat + bonus)

    def get_combat_power(self) -> int:
        """Get combat effectiveness with skill bonuses"""
        weapon_damage = 0
        if self.weapon and self.weapon in EQUIPMENT_LIBRARY:
            weapon_damage = EQUIPMENT_LIBRARY[self.weapon].damage

        base_power = self.get_stat("strength") + weapon_damage

        # Apply combat skill bonuses
        if "sharp_shooter" in self.learned_skills:
            base_power = int(base_power * (1 + SKILL_LIBRARY["sharp_shooter"].bonus_value))

        return base_power

    def can_learn_skill(self, skill_key: str) -> bool:
        """Check if dweller meets requirements for a skill"""
        if skill_key in self.learned_skills:
            return False

        skill = SKILL_LIBRARY.get(skill_key)
        if not skill:
            return False

        for stat, required in skill.stat_requirement.items():
            if self.get_stat(stat) < required:
                return False

        return True

    def learn_skill(self, skill_key: str) -> bool:
        """Learn a new skill if requirements met"""
        if self.can_learn_skill(skill_key):
            self.learned_skills.append(skill_key)
            return True
        return False

    def add_experience(self, amount: int):
        """Add experience and level up if needed"""
        self.experience += amount
        xp_needed = self.level * 100
        if self.experience >= xp_needed:
            self.level += 1
            self.experience -= xp_needed
            return True
        return False

    def get_personality_summary(self) -> str:
        """Get personality trait summary"""
        return f"{self.personality_outlook}, {self.personality_work_ethic}, {self.personality_social}, {self.personality_courage}"

    def modify_stat(self, stat_name: str, amount: int):
        """Modify a SPECIAL stat"""
        current = getattr(self, stat_name.lower(), 5)
        setattr(self, stat_name.lower(), max(1, min(10, current + amount)))

    def modify_happiness(self, amount: int):
        """Modify dweller happiness"""
        self.happiness = max(0, min(100, self.happiness + amount))

    def modify_health(self, amount: int):
        """Modify dweller health"""
        self.health = max(0, min(100, self.health + amount))


@dataclass
class Room:
    """A room in the vault"""
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

    def get_production(self, dwellers_list: List[Dweller], adjacency_bonus: float = 0.0) -> Dict[str, int]:
        """Calculate room production with worker stats, level, skills, and adjacency bonuses"""
        if self.room_type == RoomType.EMPTY or self.under_construction or self.on_fire or self.has_incident:
            return {}

        config = ROOM_CONFIGS.get(self.room_type)
        if not config or not config.production:
            return {}

        production = config.production.copy()
        base_multiplier = self.level
        worker_count = len(self.assigned_dwellers)

        if worker_count > 0:
            # Stat multiplier
            if config.stat_required:
                total_stat = 0
                skill_bonus = 0

                for dweller_name in self.assigned_dwellers:
                    dweller = next((d for d in dwellers_list if d.name == dweller_name), None)
                    if dweller:
                        total_stat += dweller.get_stat(config.stat_required)

                        # NEW v4.0: Check for production skills
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

            for resource in production:
                production[resource] = int(production[resource] * base_multiplier * worker_multiplier *
                                          stat_multiplier * skill_multiplier * adjacency_multiplier)

        return production

    def can_assign_dweller(self) -> bool:
        """Check if more dwellers can be assigned to this room"""
        if self.room_type == RoomType.EMPTY or self.under_construction:
            return False
        config = ROOM_CONFIGS.get(self.room_type)
        return len(self.assigned_dwellers) < config.capacity if config else False

    def get_upgrade_cost(self) -> int:
        """Get cost to upgrade room to next level"""
        if self.level >= 3:
            return 0
        config = ROOM_CONFIGS.get(self.room_type)
        if not config:
            return 0
        return int(config.cost * config.upgrade_cost_multiplier * self.level)

    def can_rush(self) -> bool:
        """Check if room can be rushed"""
        return (self.rush_cooldown == 0 and
                not self.under_construction and
                not self.on_fire and
                not self.has_incident and
                len(self.assigned_dwellers) > 0 and
                self.room_type in [RoomType.POWER_GENERATOR, RoomType.WATER_TREATMENT, RoomType.DINER])


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

    def add(self, resource: str, amount: int):
        """Add resources with max cap"""
        if resource == "caps":
            self.caps += amount
        else:
            current = getattr(self, resource)
            max_val = getattr(self, f"{resource}_max")
            setattr(self, resource, min(max_val, current + amount))

    def remove(self, resource: str, amount: int) -> bool:
        """Remove resources, return False if insufficient"""
        current = getattr(self, resource)
        if current >= amount:
            setattr(self, resource, current - amount)
            return True
        return False

    def consume_with_rationing(self, resource: str, amount: int) -> int:
        """Consume resources with rationing. Returns actual amount consumed."""
        current = getattr(self, resource)
        actual = min(current, amount)
        setattr(self, resource, current - actual)
        return actual

    def has_enough(self, resource: str, amount: int) -> bool:
        """Check if enough resources available"""
        return getattr(self, resource) >= amount

    def is_critical(self, resource: str) -> bool:
        """Check if resource is at critical levels"""
        if resource == "caps":
            return self.caps < 50
        current = getattr(self, resource)
        max_val = getattr(self, f"{resource}_max")
        return current < max_val * 0.2


# NEW v4.0: Quest System
@dataclass
class Quest:
    """An AI-generated quest"""
    id: str
    title: str
    description: str
    status: QuestStatus = QuestStatus.ACTIVE
    current_step: int = 0
    steps: List[Dict] = field(default_factory=list)
    rewards: Dict[str, int] = field(default_factory=dict)
    created_day: int = 1

    def get_current_step_text(self) -> str:
        if self.current_step < len(self.steps):
            return self.steps[self.current_step].get("description", "")
        return "Quest completed!"

    def advance_step(self):
        """Move to next quest step"""
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.status = QuestStatus.COMPLETED


# NEW v4.0: Expedition System
@dataclass
class Expedition:
    """A wasteland expedition"""
    dweller_name: str
    destination: str
    duration: int  # in days
    return_day: int
    difficulty: int  # 1-10
    potential_loot: List[str] = field(default_factory=list)

    def is_complete(self, current_day: int) -> bool:
        return current_day >= self.return_day


# NEW v4.0: Vault Objectives
@dataclass
class VaultObjective:
    """A victory condition"""
    objective_type: ObjectiveType
    description: str
    requirements: Dict[str, any]
    progress: Dict[str, any] = field(default_factory=dict)
    completed: bool = False

    def check_completion(self, game) -> bool:
        """Check if objective is met"""
        if self.objective_type == ObjectiveType.UTOPIA:
            # All dwellers at 90+ happiness
            return all(d.happiness >= 90 for d in game.dwellers) and len(game.dwellers) >= 10

        elif self.objective_type == ObjectiveType.ECONOMIC:
            # Accumulate 10,000 caps
            return game.resources.caps >= self.requirements.get("caps", 10000)

        elif self.objective_type == ObjectiveType.SURVIVAL:
            # Survive 100 days
            return game.day >= self.requirements.get("days", 100)

        elif self.objective_type == ObjectiveType.MILITARY:
            # All dwellers armed and trained
            armed = sum(1 for d in game.dwellers if d.weapon)
            return armed >= 15 and len(game.dwellers) >= 15

        elif self.objective_type == ObjectiveType.EXODUS:
            # Successfully complete 10 wasteland expeditions
            return self.progress.get("expeditions_completed", 0) >= 10

        return False


# =============================================================================
# AI HELPER FUNCTIONS
# =============================================================================

def call_ai_model(prompt: str, max_tokens: int = 500, system_prompt: str = "") -> str:
    """Call AI model with fallback to demo mode"""
    if not AI_ENABLED:
        return generate_fallback_response(prompt)

    try:
        messages = [{"role": "user", "content": prompt}]

        response = ai_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "You are a helpful AI assistant for Vault 13, a post-apocalyptic vault management game.",
            messages=messages
        )

        return response.content[0].text
    except Exception as e:
        print(f"{C.WARNING}AI Error: {e}{C.RESET}")
        return generate_fallback_response(prompt)


def generate_fallback_response(prompt: str) -> str:
    """Generate demo responses when AI is disabled"""
    prompt_lower = prompt.lower()

    if "dialogue" in prompt_lower or "comment" in prompt_lower:
        comments = [
            "Another day in the vault. Could be worse.",
            "Just doing my part to keep everyone alive.",
            "I wonder what the surface looks like now...",
            "At least we have each other down here.",
            "Work hard, stay safe, that's my motto."
        ]
        return random.choice(comments)

    elif "quest" in prompt_lower:
        return json.dumps({
            "title": "Demo Quest",
            "description": "[AI disabled - Set ANTHROPIC_API_KEY for procedural quests]",
            "steps": [
                {"description": "Complete this demo objective", "type": "demo"}
            ],
            "rewards": {"caps": 100}
        })

    elif "advisor" in prompt_lower or "analyze" in prompt_lower:
        return """⚠️  CRITICAL CONCERNS:
- AI features disabled (demo mode)
- Set ANTHROPIC_API_KEY to enable full advisor

💡 RECOMMENDATIONS:
1. Focus on balanced resource production
2. Keep dwellers assigned to appropriate rooms
3. Upgrade key production rooms when possible

[This is a demo message. Enable AI for full strategic analysis]"""

    elif "command" in prompt_lower:
        return '{"action": "unknown", "message": "AI command parsing disabled. Use menu controls."}'

    else:
        return "[AI response unavailable - demo mode]"


# NEW v4.0: AI Quest Generation
def generate_quest(game) -> Quest:
    """Generate a new quest using AI"""
    if not AI_ENABLED:
        # Fallback quest
        return Quest(
            id=f"quest_{game.day}",
            title="Resource Shortage",
            description="The vault is running low on supplies. Gather resources to survive.",
            steps=[
                {"description": "Accumulate 50 food", "type": "resource", "target": "food", "amount": 50},
                {"description": "Accumulate 50 water", "type": "resource", "target": "water", "amount": 50}
            ],
            rewards={"caps": 200},
            created_day=game.day
        )

    # Build context for AI
    vault_state = {
        "day": game.day,
        "dweller_count": len(game.dwellers),
        "avg_happiness": sum(d.happiness for d in game.dwellers) // len(game.dwellers) if game.dwellers else 0,
        "caps": game.resources.caps,
        "recent_events": game.event_log[-3:] if game.event_log else []
    }

    prompt = f"""Generate a Fallout-style vault quest for Vault 13.

Vault State: {json.dumps(vault_state)}

Create a 2-3 step quest that fits the current situation. Return ONLY valid JSON:
{{
    "title": "Quest Name",
    "description": "Brief quest description (1-2 sentences)",
    "steps": [
        {{"description": "Step 1 objective", "type": "resource|build|assign|explore"}},
        {{"description": "Step 2 objective", "type": "resource|build|assign|explore"}}
    ],
    "rewards": {{"caps": 100, "equipment": "optional_item_key"}}
}}

Make it dramatic and Fallout-themed!"""

    try:
        response = call_ai_model(prompt, max_tokens=300)
        # Extract JSON
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

    # Fallback
    return Quest(
        id=f"quest_{game.day}",
        title="Vault Emergency",
        description="Handle the current vault crisis.",
        steps=[{"description": "Maintain positive resource flow for 3 turns", "type": "survival"}],
        rewards={"caps": 150},
        created_day=game.day
    )


def get_dweller_dialogue(dweller: Dweller, context: str, game_state: dict) -> str:
    """Generate contextual dialogue for a dweller"""
    if not AI_ENABLED:
        return generate_fallback_response("dialogue")

    prompt = f"""Generate a short, in-character comment (1-2 sentences max) for this Fallout-style vault dweller.

Dweller: {dweller.name}
Personality: {dweller.get_personality_summary()}
Health: {dweller.health}% | Happiness: {dweller.happiness}%
Level: {dweller.level} | Skills: {', '.join(dweller.learned_skills) if dweller.learned_skills else 'None'}
SPECIAL: S:{dweller.strength} P:{dweller.perception} E:{dweller.endurance} C:{dweller.charisma} I:{dweller.intelligence} A:{dweller.agility} L:{dweller.luck}
Equipped: {("Weapon: " + dweller.weapon) if dweller.weapon else "No weapon"}, {("Outfit: " + dweller.outfit) if dweller.outfit else "No outfit"}
Status: {"On expedition" if dweller.on_expedition else ("Working" if dweller.assigned_room else "Idle")}

Context: {context}

Generate a witty, Fallout-themed comment that fits their personality. Keep it brief and natural. No quotes, just the dialogue."""

    return call_ai_model(prompt, max_tokens=100)


def get_advisor_analysis(game, question: Optional[str] = None) -> str:
    """Get strategic analysis from AI advisor"""
    if not AI_ENABLED:
        return generate_fallback_response("advisor")

    # Build concise game state
    state = {
        "day": game.day,
        "resources": {
            "power": f"{game.resources.power}/{game.resources.power_max}",
            "water": f"{game.resources.water}/{game.resources.water_max}",
            "food": f"{game.resources.food}/{game.resources.food_max}",
            "caps": game.resources.caps
        },
        "dwellers": len(game.dwellers),
        "avg_happiness": sum(d.happiness for d in game.dwellers) // len(game.dwellers) if game.dwellers else 0,
        "active_quests": len([q for q in game.active_quests if q.status == QuestStatus.ACTIVE]),
        "objective": game.current_objective.objective_type.value if game.current_objective else "None"
    }

    prompt = f"""You are the AI Overseer Advisor for Vault 13. Analyze this vault and provide strategic advice.

Vault State:
{json.dumps(state, indent=2)}

Recent Events: {', '.join(game.event_log[-3:]) if game.event_log else 'None yet'}

{'Player Question: ' + question if question else 'Provide general strategic analysis.'}

Give concise, actionable advice in this format:
⚠️  CRITICAL CONCERNS: (list any immediate threats)
💡 RECOMMENDATIONS: (2-3 specific actions to take)
📊 LONG-TERM STRATEGY: (optional, 1 sentence)

Be specific. Keep it under 200 words."""

    return call_ai_model(prompt, max_tokens=400)


def parse_natural_language_command(text: str, game) -> dict:
    """Parse natural language command into game action"""
    if not AI_ENABLED:
        return {"action": "unknown", "message": "AI command parsing disabled. Use menu controls."}

    prompt = f"""Parse this player command into a game action.

Command: "{text}"

Available actions: assign_dweller, rush_room, upgrade_room, build_room, equip_item, view_status, send_expedition, view_quest, advisor, end_turn

Return ONLY valid JSON:
{{
    "action": "action_name",
    "parameters": {{"param": "value"}},
    "message": "confirmation message for user"
}}

If unclear, use action: "clarify"."""

    try:
        response = call_ai_model(prompt, max_tokens=200)
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            return json.loads(response[json_start:json_end])
    except:
        pass

    return {"action": "error", "message": "Couldn't parse command. Try: 'assign Sarah to power generator'"}


# =============================================================================
# MAIN GAME CLASS (v4.0 Ultimate Edition)
# =============================================================================

class VaultGame:
    """Main game class for Vault 13 v4.0 with all features"""

    def __init__(self):
        self.day = 1
        self.resources = Resources()
        self.dwellers: List[Dweller] = []
        self.vault_layout: List[List[Room]] = []
        self.event_log: List[str] = []
        self.equipment_inventory: List[str] = []
        self.game_over = False
        self.max_floors = 10
        self.floors_unlocked = 3

        # AI Features (v3.0)
        self.nl_mode = False

        # NEW v4.0 Features
        self.active_quests: List[Quest] = []
        self.completed_quests: List[Quest] = []
        self.active_expeditions: List[Expedition] = []
        self.current_objective: Optional[VaultObjective] = None
        self.available_objectives: List[VaultObjective] = []

        # Initialize
        self._initialize_vault()
        self._create_starting_dwellers()
        self._create_objectives()

        # Starting equipment
        self.equipment_inventory = ["rusty_pistol", "vault_suit", "laser_rifle"]

        # Start with a quest
        self.active_quests.append(generate_quest(self))

    def _initialize_vault(self):
        """Create initial vault layout"""
        for floor in range(3):
            floor_rooms = []
            for pos in range(3):
                if floor == 0 and pos == 0:
                    room = Room(RoomType.POWER_GENERATOR, floor, pos)
                elif floor == 0 and pos == 1:
                    room = Room(RoomType.WATER_TREATMENT, floor, pos)
                elif floor == 1 and pos == 0:
                    room = Room(RoomType.LIVING_QUARTERS, floor, pos)
                else:
                    room = Room(RoomType.EMPTY, floor, pos)
                floor_rooms.append(room)
            self.vault_layout.append(floor_rooms)

    def _create_starting_dwellers(self):
        """Create initial dwellers with personalities and skills"""
        first_names = ["Sarah", "John", "Emma", "Michael", "Alice", "David", "Lisa", "James"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

        for i in range(4):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            dweller = Dweller(
                name=name,
                strength=random.randint(3, 7),
                perception=random.randint(3, 7),
                endurance=random.randint(3, 7),
                charisma=random.randint(3, 7),
                intelligence=random.randint(3, 7),
                agility=random.randint(3, 7),
                luck=random.randint(3, 7),
                happiness=random.randint(60, 80),
                personality_outlook=random.choice(PERSONALITY_TRAITS["outlook"]),
                personality_work_ethic=random.choice(PERSONALITY_TRAITS["work_ethic"]),
                personality_social=random.choice(PERSONALITY_TRAITS["social"]),
                personality_courage=random.choice(PERSONALITY_TRAITS["courage"])
            )
            self.dwellers.append(dweller)

        # Assign starting dwellers
        self.dwellers[0].assigned_room = (0, 0)
        self.vault_layout[0][0].assigned_dwellers.append(self.dwellers[0].name)
        self.dwellers[1].assigned_room = (0, 1)
        self.vault_layout[0][1].assigned_dwellers.append(self.dwellers[1].name)

    def _create_objectives(self):
        """Create available victory conditions"""
        self.available_objectives = [
            VaultObjective(
                ObjectiveType.SURVIVAL,
                "Survive 100 days in the wasteland",
                {"days": 100}
            ),
            VaultObjective(
                ObjectiveType.UTOPIA,
                "Create a perfect vault (10+ dwellers, all 90+ happiness)",
                {"min_dwellers": 10, "min_happiness": 90}
            ),
            VaultObjective(
                ObjectiveType.ECONOMIC,
                "Accumulate 10,000 caps",
                {"caps": 10000}
            ),
            VaultObjective(
                ObjectiveType.MILITARY,
                "Build a strong military (15 armed dwellers)",
                {"armed_dwellers": 15}
            ),
            VaultObjective(
                ObjectiveType.EXODUS,
                "Complete 10 successful wasteland expeditions",
                {"expeditions": 10}
            ),
        ]

        # Start with survival objective
        self.current_objective = self.available_objectives[0]

    def calculate_adjacency_bonus(self, floor: int, position: int) -> float:
        """Calculate production bonus from adjacent rooms"""
        bonus = 0.0
        room = self.vault_layout[floor][position]

        if room.room_type == RoomType.EMPTY:
            return 0.0

        # Check left neighbor
        if position > 0:
            neighbor = self.vault_layout[floor][position - 1]
            key = (room.room_type, neighbor.room_type)
            reverse_key = (neighbor.room_type, room.room_type)

            if key in ADJACENCY_BONUSES:
                bonus += ADJACENCY_BONUSES[key].get("production_bonus", 0)
            elif reverse_key in ADJACENCY_BONUSES:
                bonus += ADJACENCY_BONUSES[reverse_key].get("production_bonus", 0)

        # Check right neighbor
        if position < 2:
            neighbor = self.vault_layout[floor][position + 1]
            key = (room.room_type, neighbor.room_type)
            reverse_key = (neighbor.room_type, room.room_type)

            if key in ADJACENCY_BONUSES:
                bonus += ADJACENCY_BONUSES[key].get("production_bonus", 0)
            elif reverse_key in ADJACENCY_BONUSES:
                bonus += ADJACENCY_BONUSES[reverse_key].get("production_bonus", 0)

        return bonus

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Print game header"""
        ai_status = f"{C.AI}🤖 AI{C.RESET}" if AI_ENABLED else f"{C.DIM}🤖{C.RESET}"
        nl_status = f"{C.AI}💬{C.RESET}" if self.nl_mode else ""
        quest_count = len([q for q in self.active_quests if q.status == QuestStatus.ACTIVE])
        quest_status = f"{C.QUEST}📜{quest_count}{C.RESET}" if quest_count > 0 else ""

        print(f"\n{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║          VAULT 13 - SURVIVAL PROTOCOL v4.0 ULTIMATE              ║{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║  DAY {self.day:4d}  {ai_status} {nl_status} {quest_status}                                           ║{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}\n")

    def print_resources(self):
        """Print resource status"""
        power_bar = self._get_resource_bar(self.resources.power, self.resources.power_max)
        water_bar = self._get_resource_bar(self.resources.water, self.resources.water_max)
        food_bar = self._get_resource_bar(self.resources.food, self.resources.food_max)

        power_color = C.DANGER if self.resources.is_critical("power") else C.POWER
        water_color = C.DANGER if self.resources.is_critical("water") else C.WATER
        food_color = C.DANGER if self.resources.is_critical("food") else C.FOOD

        print(f"{C.BOLD}Resources:{C.RESET}")
        print(f"  {power_color}⚡ Power: {power_bar} {self.resources.power}/{self.resources.power_max}{C.RESET}")
        print(f"  {water_color}💧 Water: {water_bar} {self.resources.water}/{self.resources.water_max}{C.RESET}")
        print(f"  {food_color}🍖 Food:  {food_bar} {self.resources.food}/{self.resources.food_max}{C.RESET}")
        print(f"  {C.CAPS}💰 Caps:  {self.resources.caps}{C.RESET}")
        print()

    def _get_resource_bar(self, current: int, maximum: int) -> str:
        """Generate a resource bar visualization"""
        bar_length = 20
        filled = int((current / maximum) * bar_length) if maximum > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        return f"[{bar}]"

    def print_dweller_info(self):
        """Print dweller summary"""
        available_dwellers = [d for d in self.dwellers if not d.on_expedition]
        total_happiness = sum(d.happiness for d in available_dwellers) // len(available_dwellers) if available_dwellers else 0
        happiness_color = C.HAPPY if total_happiness >= 60 else C.NEUTRAL if total_happiness >= 30 else C.SAD

        print(f"{C.BOLD}Population:{C.RESET}")
        print(f"  Dwellers: {C.INFO}{len(available_dwellers)}{C.RESET} ({len(self.active_expeditions)} on expedition)")
        print(f"  Average Happiness: {happiness_color}{total_happiness}%{C.RESET}")

        if self.current_objective:
            obj_progress = ""
            if self.current_objective.objective_type == ObjectiveType.SURVIVAL:
                progress = f"{self.day}/{self.current_objective.requirements['days']}"
                obj_progress = f"Day {progress}"
            elif self.current_objective.objective_type == ObjectiveType.ECONOMIC:
                progress = f"{self.resources.caps}/{self.current_objective.requirements['caps']}"
                obj_progress = f"{progress} caps"
            elif self.current_objective.objective_type == ObjectiveType.EXODUS:
                completed = self.current_objective.progress.get("expeditions_completed", 0)
                progress = f"{completed}/{self.current_objective.requirements.get('expeditions', 10)}"
                obj_progress = f"{progress} expeditions"

            print(f"  Objective: {C.INFO}{self.current_objective.objective_type.value}{C.RESET} - {obj_progress}")

        print()

    def print_vault_layout(self):
        """Print vault layout with adjacency indicators"""
        print(f"{C.BOLD}Vault Layout:{C.RESET}")
        print(f"{C.BORDER}{'═' * 75}{C.RESET}")

        for floor_idx, floor in enumerate(self.vault_layout):
            floor_str = f"{C.DIM}F{floor_idx + 1}:{C.RESET} "

            for pos, room in enumerate(floor):
                bonus = self.calculate_adjacency_bonus(floor_idx, pos)
                room_str = self._get_enhanced_room_display(room, bonus)
                floor_str += f"{room_str} "

            print(floor_str)

        print(f"{C.BORDER}{'═' * 75}{C.RESET}\n")

    def _get_enhanced_room_display(self, room: Room, adjacency_bonus: float = 0) -> str:
        """Get enhanced room display with indicators"""
        room_colors = {
            RoomType.EMPTY: C.ROOM_EMPTY,
            RoomType.POWER_GENERATOR: C.ROOM_POWER,
            RoomType.WATER_TREATMENT: C.ROOM_WATER,
            RoomType.DINER: C.ROOM_FOOD,
            RoomType.LIVING_QUARTERS: C.ROOM_LIVING,
            RoomType.TRAINING_ROOM: C.ROOM_TRAINING,
            RoomType.STORAGE_ROOM: C.ROOM_STORAGE,
            RoomType.MEDBAY: C.SUCCESS,
            RoomType.SCIENCE_LAB: C.INFO,
        }

        color = room_colors.get(room.room_type, C.RESET)

        room_icons = {
            RoomType.POWER_GENERATOR: "⚡",
            RoomType.WATER_TREATMENT: "💧",
            RoomType.DINER: "🍖",
            RoomType.LIVING_QUARTERS: "🏠",
            RoomType.TRAINING_ROOM: "💪",
            RoomType.STORAGE_ROOM: "📦",
            RoomType.MEDBAY: "⚕️",
            RoomType.SCIENCE_LAB: "🔬",
            RoomType.EMPTY: "░░",
        }

        icon = room_icons.get(room.room_type, "  ")
        level_display = ["", "I", "II", "III"][min(room.level, 3)] if room.room_type != RoomType.EMPTY else ""
        worker_count = len(room.assigned_dwellers)
        worker_icons = "👤" * min(worker_count, 2)

        status = ""
        if room.on_fire:
            status = "🔥"
        elif room.has_incident:
            status = "⚠️"
        elif room.rush_cooldown > 0:
            status = "⏳"
        elif adjacency_bonus > 0:
            status = "✨"

        if room.room_type == RoomType.EMPTY:
            return f"{color}[{icon:^6s}]{C.RESET}"
        else:
            return f"{color}[{icon}{level_display:2s}{worker_icons:2s}{status}]{C.RESET}"

    def print_event_log(self):
        """Print recent events"""
        if not self.event_log:
            return

        print(f"{C.BOLD}Recent Events:{C.RESET}")
        for event in self.event_log[-5:]:
            print(f"  {C.DIM}•{C.RESET} {event}")
        print()

    def print_menu(self):
        """Print action menu"""
        print(f"{C.BOLD}Actions:{C.RESET}")
        print(f"  {C.SUCCESS}[B]{C.RESET} Build Room       {C.SUCCESS}[U]{C.RESET} Upgrade Room    {C.SUCCESS}[H]{C.RESET} Rush Production")
        print(f"  {C.SUCCESS}[D]{C.RESET} Manage Dwellers  {C.SUCCESS}[R]{C.RESET} Assign Workers  {C.SUCCESS}[I]{C.RESET} Fight Incident")
        print(f"  {C.SUCCESS}[G]{C.RESET} Manage Equipment {C.SUCCESS}[V]{C.RESET} View Details    {C.SUCCESS}[E]{C.RESET} End Turn")

        # v4.0 features
        print(f"  {C.QUEST}[Q]{C.RESET} View Quests      {C.QUEST}[X]{C.RESET} Expeditions     {C.SKILL}[K]{C.RESET} Learn Skills")
        print(f"  {C.INFO}[O]{C.RESET} Objectives       {C.SUCCESS}[S]{C.RESET} Save Game       {C.DANGER}[Z]{C.RESET} Quit")

        if AI_ENABLED:
            print(f"  {C.AI}[A]{C.RESET} AI Advisor       {C.AI}[T]{C.RESET} Talk to Dweller  {C.AI}[N]{C.RESET} Natural Language")

        print()

    # =================================================================
    # QUEST SYSTEM (v4.0)
    # =================================================================

    def view_quests_menu(self):
        """View and manage active quests"""
        self.clear_screen()
        self.print_header()

        print(f"{C.QUEST}{C.BOLD}📜 ACTIVE QUESTS{C.RESET}\n")

        active = [q for q in self.active_quests if q.status == QuestStatus.ACTIVE]

        if not active:
            print(f"{C.DIM}No active quests. New quests appear randomly or can be generated with AI.{C.RESET}\n")

            if AI_ENABLED:
                choice = input(f"{C.QUEST}Generate new quest? (y/n): {C.RESET}").strip().lower()
                if choice == 'y':
                    print(f"\n{C.QUEST}Generating quest...{C.RESET}\n")
                    new_quest = generate_quest(self)
                    self.active_quests.append(new_quest)
                    self.log_event(f"New quest: {new_quest.title}")
                    print(f"{C.SUCCESS}✓ Quest generated: {new_quest.title}{C.RESET}")
                    print(f"{new_quest.description}\n")

            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        for idx, quest in enumerate(active, 1):
            print(f"{C.BOLD}[{idx}] {quest.title}{C.RESET}")
            print(f"    {quest.description}")
            print(f"    Progress: Step {quest.current_step + 1}/{len(quest.steps)}")
            print(f"    {C.QUEST}→{C.RESET} {quest.get_current_step_text()}")
            print()

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    # =================================================================
    # EXPEDITION SYSTEM (v4.0)
    # =================================================================

    def expedition_menu(self):
        """Send dwellers on wasteland expeditions"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}🏜️  WASTELAND EXPEDITIONS{C.RESET}\n")

        # Show active expeditions
        if self.active_expeditions:
            print(f"{C.INFO}Active Expeditions:{C.RESET}")
            for exp in self.active_expeditions:
                days_left = exp.return_day - self.day
                print(f"  • {exp.dweller_name} - {exp.destination} (returns in {days_left} days)")
            print()

        # Show available dwellers
        available = [d for d in self.dwellers if not d.on_expedition and not d.assigned_room]

        if not available:
            print(f"{C.WARNING}No idle dwellers available for expeditions.{C.RESET}\n")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        print(f"{C.BOLD}Available Dwellers:{C.RESET}")
        for idx, dweller in enumerate(available, 1):
            combat = dweller.get_combat_power()
            survival_score = (dweller.endurance + dweller.luck + dweller.perception) // 3
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - Combat: {combat}, Survival: {survival_score}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select dweller to send: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                dweller = available[idx]

                # Choose destination
                destinations = [
                    ("Nearby Ruins", 2, 3),
                    ("Old Supermarket", 3, 5),
                    ("Military Base", 5, 7),
                    ("Distant City", 7, 10)
                ]

                print(f"\n{C.BOLD}Destinations:{C.RESET}")
                for i, (name, duration, difficulty) in enumerate(destinations, 1):
                    print(f"  {C.SUCCESS}[{i}]{C.RESET} {name} - {duration} days, Difficulty: {difficulty}/10")

                dest_choice = input(f"\nSelect destination: ").strip()
                dest_idx = int(dest_choice) - 1

                if 0 <= dest_idx < len(destinations):
                    name, duration, difficulty = destinations[dest_idx]

                    # Apply wasteland_survivor skill
                    if "wasteland_survivor" in dweller.learned_skills:
                        duration = max(1, int(duration * (1 - SKILL_LIBRARY["wasteland_survivor"].bonus_value)))
                        print(f"{C.SKILL}Wasteland Survivor skill reduces expedition time!{C.RESET}")

                    expedition = Expedition(
                        dweller_name=dweller.name,
                        destination=name,
                        duration=duration,
                        return_day=self.day + duration,
                        difficulty=difficulty,
                        potential_loot=["caps", "equipment", "resources"]
                    )

                    dweller.on_expedition = True
                    dweller.expedition_return_day = expedition.return_day
                    self.active_expeditions.append(expedition)
                    self.log_event(f"{dweller.name} departed for {name}")

                    print(f"\n{C.SUCCESS}✓ {dweller.name} departed for {name}!{C.RESET}")
                    print(f"  Returns on day {expedition.return_day}")

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def process_expedition_returns(self):
        """Check for returning expeditions"""
        returning = [exp for exp in self.active_expeditions if exp.is_complete(self.day)]

        for exp in returning:
            dweller = next((d for d in self.dwellers if d.name == exp.dweller_name), None)
            if not dweller:
                continue

            dweller.on_expedition = False
            dweller.expedition_return_day = 0

            # Calculate success based on difficulty and dweller stats
            survival_score = (dweller.endurance + dweller.luck + dweller.perception) // 3
            success_chance = max(30, min(95, 100 - (exp.difficulty * 8) + (survival_score * 5)))

            if random.randint(1, 100) <= success_chance:
                # Success!
                loot_caps = random.randint(50, 200) * exp.difficulty

                # Apply scavenger skill
                if "scavenger" in dweller.learned_skills:
                    loot_caps = int(loot_caps * (1 + SKILL_LIBRARY["scavenger"].bonus_value))

                self.resources.caps += loot_caps
                dweller.add_experience(exp.difficulty * 20)

                # Random equipment
                if random.random() < 0.3:
                    equipment_found = random.choice(list(EQUIPMENT_LIBRARY.keys()))
                    if equipment_found not in self.equipment_inventory:
                        self.equipment_inventory.append(equipment_found)
                        self.log_event(f"✨ {dweller.name} found {EQUIPMENT_LIBRARY[equipment_found].name}!")

                self.log_event(f"✓ {dweller.name} returned from {exp.destination} (+{loot_caps} caps)")
                dweller.modify_happiness(10)

                # Update exodus objective
                if self.current_objective and self.current_objective.objective_type == ObjectiveType.EXODUS:
                    self.current_objective.progress["expeditions_completed"] = \
                        self.current_objective.progress.get("expeditions_completed", 0) + 1

            else:
                # Failure - dweller injured
                damage = random.randint(20, 50)
                dweller.modify_health(-damage)
                dweller.modify_happiness(-15)
                self.log_event(f"⚠️ {dweller.name} returned injured from {exp.destination} (-{damage} health)")

            self.active_expeditions.remove(exp)

    # =================================================================
    # SKILLS SYSTEM (v4.0)
    # =================================================================

    def learn_skills_menu(self):
        """Learn new skills for dwellers"""
        self.clear_screen()
        self.print_header()

        print(f"{C.SKILL}{C.BOLD}⭐ DWELLER SKILLS{C.RESET}\n")

        # Select dweller
        print(f"{C.BOLD}Select Dweller:{C.RESET}")
        for idx, dweller in enumerate(self.dwellers, 1):
            if dweller.on_expedition:
                continue
            skills_count = len(dweller.learned_skills)
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} (Lvl {dweller.level}) - {skills_count} skills")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select dweller: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.dwellers):
                dweller = self.dwellers[idx]

                self.clear_screen()
                self.print_header()

                print(f"{C.SKILL}{C.BOLD}⭐ SKILLS FOR {dweller.name.upper()}{C.RESET}\n")

                # Show current skills
                if dweller.learned_skills:
                    print(f"{C.BOLD}Current Skills:{C.RESET}")
                    for skill_key in dweller.learned_skills:
                        skill = SKILL_LIBRARY[skill_key]
                        print(f"  {skill.icon} {skill.name} - {skill.description}")
                    print()

                # Show available skills
                available_skills = []
                for skill_key, skill in SKILL_LIBRARY.items():
                    if dweller.can_learn_skill(skill_key):
                        available_skills.append((skill_key, skill))

                if not available_skills:
                    print(f"{C.WARNING}No skills available. Train SPECIAL stats to unlock more skills.{C.RESET}\n")
                else:
                    print(f"{C.BOLD}Available Skills:{C.RESET}")
                    for i, (skill_key, skill) in enumerate(available_skills, 1):
                        req_str = ", ".join([f"{k.upper()}≥{v}" for k, v in skill.stat_requirement.items()])
                        print(f"  {C.SUCCESS}[{i}]{C.RESET} {skill.icon} {skill.name}")
                        print(f"      {C.DIM}{skill.description}{C.RESET}")
                        print(f"      Requirements: {req_str}")
                        print()

                    skill_choice = input(f"Select skill to learn (or 0 to cancel): ").strip()

                    if skill_choice != "0":
                        try:
                            skill_idx = int(skill_choice) - 1
                            if 0 <= skill_idx < len(available_skills):
                                skill_key, skill = available_skills[skill_idx]
                                if dweller.learn_skill(skill_key):
                                    self.log_event(f"{dweller.name} learned {skill.name}!")
                                    print(f"\n{C.SUCCESS}✓ {dweller.name} learned {skill.name}!{C.RESET}")
                        except (ValueError, IndexError):
                            pass

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    # =================================================================
    # OBJECTIVES SYSTEM (v4.0)
    # =================================================================

    def objectives_menu(self):
        """View and change victory objectives"""
        self.clear_screen()
        self.print_header()

        print(f"{C.INFO}{C.BOLD}🎯 VAULT OBJECTIVES{C.RESET}\n")

        print(f"{C.BOLD}Current Objective:{C.RESET}")
        if self.current_objective:
            print(f"  {C.INFO}{self.current_objective.objective_type.value}{C.RESET} - {self.current_objective.description}")

            # Show progress
            if self.current_objective.objective_type == ObjectiveType.SURVIVAL:
                progress = f"{self.day}/{self.current_objective.requirements['days']}"
                pct = (self.day / self.current_objective.requirements['days']) * 100
                print(f"  Progress: {progress} ({pct:.0f}%)")
            elif self.current_objective.objective_type == ObjectiveType.ECONOMIC:
                progress = f"{self.resources.caps}/{self.current_objective.requirements['caps']}"
                pct = (self.resources.caps / self.current_objective.requirements['caps']) * 100
                print(f"  Progress: {progress} ({pct:.0f}%)")

            # Check completion
            if self.current_objective.check_completion(self):
                print(f"\n{C.SUCCESS}🎉 OBJECTIVE COMPLETE! 🎉{C.RESET}")
                self.current_objective.completed = True

        print(f"\n{C.BOLD}Available Objectives:{C.RESET}")
        for idx, obj in enumerate(self.available_objectives, 1):
            status = "✓" if obj.completed else " "
            marker = "→" if obj == self.current_objective else " "
            print(f"  {marker} {C.SUCCESS}[{idx}]{C.RESET} [{status}] {obj.objective_type.value} - {obj.description}")

        print(f"\n  {C.SUCCESS}[C]{C.RESET} Change objective")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"Select option: ").strip().lower()

        if choice == 'c':
            obj_choice = input(f"Select new objective (1-{len(self.available_objectives)}): ").strip()
            try:
                idx = int(obj_choice) - 1
                if 0 <= idx < len(self.available_objectives):
                    self.current_objective = self.available_objectives[idx]
                    print(f"\n{C.SUCCESS}✓ Objective changed to: {self.current_objective.objective_type.value}{C.RESET}")
            except (ValueError, IndexError):
                pass

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    # (Continue with remaining methods in next part...)

    def log_event(self, message: str):
        """Add event to log"""
        self.event_log.append(message)
        if len(self.event_log) > 50:
            self.event_log = self.event_log[-50:]
    # =================================================================
    # v3.0 AI FEATURES
    # =================================================================

    def ai_advisor_menu(self):
        """Interact with AI Overseer Advisor"""
        if not AI_ENABLED:
            print(f"\n{C.WARNING}AI features disabled. Set ANTHROPIC_API_KEY to enable.{C.RESET}")
            input("\nPress Enter to continue...")
            return

        self.clear_screen()
        self.print_header()

        print(f"{C.AI}{C.BOLD}🤖 AI OVERSEER ADVISOR{C.RESET}\n")
        print(f"Ask me anything about your vault strategy, or leave blank for general analysis.\n")
        print(f"{C.DIM}Examples: 'why is morale low?' 'what should I build next?' 'analyze my production'{C.RESET}\n")

        question = input(f"{C.AI}Your question (or Enter for analysis): {C.RESET}").strip()

        print(f"\n{C.AI}Analyzing vault...{C.RESET}\n")

        analysis = get_advisor_analysis(self, question if question else None)

        print(f"{C.AI}{C.BOLD}ADVISOR REPORT:{C.RESET}\n")
        print(analysis)

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def talk_to_dweller_menu(self):
        """Generate AI dialogue for dwellers"""
        if not AI_ENABLED:
            print(f"\n{C.WARNING}AI features disabled. Set ANTHROPIC_API_KEY to enable.{C.RESET}")
            input("\nPress Enter to continue...")
            return

        self.clear_screen()
        self.print_header()

        print(f"{C.AI}{C.BOLD}💬 TALK TO DWELLER{C.RESET}\n")
        print(f"Select a dweller to hear their thoughts:\n")

        for idx, dweller in enumerate(self.dwellers, 1):
            if dweller.on_expedition:
                continue
            health_icon = "❤️" if dweller.health > 70 else "💔" if dweller.health < 40 else "💛"
            mood_icon = "😊" if dweller.happiness > 60 else "😐" if dweller.happiness > 30 else "😢"
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} {health_icon}{mood_icon} - {dweller.get_personality_summary()}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.AI}Select dweller: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.dwellers):
                dweller = self.dwellers[idx]

                # Generate context
                context = "general check-in"
                if dweller.health < 50:
                    context = "injured and in pain"
                elif dweller.happiness < 40:
                    context = "unhappy and considering leaving"
                elif not dweller.assigned_room:
                    context = "idle and bored"
                elif dweller.weapon and dweller.outfit:
                    context = "well-equipped and confident"

                print(f"\n{C.AI}Generating dialogue...{C.RESET}\n")

                dialogue = get_dweller_dialogue(dweller, context, {})
                dweller.recent_dialogue = dialogue

                print(f"{C.BOLD}{dweller.name}:{C.RESET}")
                print(f'"{dialogue}"')
                print()

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def natural_language_mode(self):
        """Toggle natural language command mode"""
        if not AI_ENABLED:
            print(f"\n{C.WARNING}AI features disabled. Set ANTHROPIC_API_KEY to enable.{C.RESET}")
            input("\nPress Enter to continue...")
            return

        self.nl_mode = not self.nl_mode

        if self.nl_mode:
            print(f"\n{C.AI}{C.BOLD}💬 NATURAL LANGUAGE MODE ENABLED{C.RESET}")
            print(f"\n{C.INFO}You can now type commands in plain English!{C.RESET}")
            print(f"{C.DIM}Examples:{C.RESET}")
            print(f"  - 'assign sarah to power generator'")
            print(f"  - 'send john on expedition'")
            print(f"  - 'what's my food production?'")
            print(f"  - Type 'menu' to return to normal controls\n")
            input("Press Enter to continue...")
        else:
            print(f"\n{C.INFO}Natural language mode disabled. Using menu controls.{C.RESET}")
            input("Press Enter to continue...")

    def process_nl_command(self, text: str):
        """Process a natural language command"""
        if text.lower() in ['menu', 'exit', 'quit nl', 'normal']:
            self.nl_mode = False
            print(f"{C.INFO}Returning to menu mode.{C.RESET}")
            time.sleep(1)
            return

        print(f"\n{C.AI}Processing command...{C.RESET}\n")
        result = parse_natural_language_command(text, self)
        print(f"{C.INFO}{result.get('message', 'Command processed')}{C.RESET}")
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    # =================================================================
    # v2.0 CORE FEATURES
    # =================================================================

    def build_room_menu(self):
        """Build new rooms"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}🏗️  BUILD ROOM{C.RESET}\n")

        # Show available room types
        buildable_rooms = [
            (RoomType.POWER_GENERATOR, ROOM_CONFIGS[RoomType.POWER_GENERATOR]),
            (RoomType.WATER_TREATMENT, ROOM_CONFIGS[RoomType.WATER_TREATMENT]),
            (RoomType.DINER, ROOM_CONFIGS[RoomType.DINER]),
            (RoomType.LIVING_QUARTERS, ROOM_CONFIGS[RoomType.LIVING_QUARTERS]),
            (RoomType.STORAGE_ROOM, ROOM_CONFIGS[RoomType.STORAGE_ROOM]),
            (RoomType.MEDBAY, ROOM_CONFIGS[RoomType.MEDBAY]),
            (RoomType.TRAINING_ROOM, ROOM_CONFIGS[RoomType.TRAINING_ROOM]),
            (RoomType.SCIENCE_LAB, ROOM_CONFIGS[RoomType.SCIENCE_LAB]),
        ]

        print(f"{C.BOLD}Available Rooms:{C.RESET}")
        for idx, (room_type, config) in enumerate(buildable_rooms, 1):
            affordable = "✓" if self.resources.caps >= config.cost else "✗"
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} [{affordable}] {room_type.value} - {config.cost} caps")
            print(f"      {C.DIM}{config.description}{C.RESET}")

        print(f"\n  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select room type: ").strip()

        if choice == "0":
            return

        try:
            room_idx = int(choice) - 1
            if 0 <= room_idx < len(buildable_rooms):
                room_type, config = buildable_rooms[room_idx]

                if not self.resources.has_enough("caps", config.cost):
                    print(f"\n{C.DANGER}Not enough caps! Need {config.cost}, have {self.resources.caps}{C.RESET}")
                    input("\nPress Enter to continue...")
                    return

                # Select location
                print(f"\n{C.BOLD}Select Location:{C.RESET}")
                empty_slots = []
                for f_idx, floor in enumerate(self.vault_layout):
                    for p_idx, room in enumerate(floor):
                        if room.room_type == RoomType.EMPTY:
                            empty_slots.append((f_idx, p_idx))
                            print(f"  {C.SUCCESS}[{len(empty_slots)}]{C.RESET} Floor {f_idx + 1}, Position {p_idx + 1}")

                if not empty_slots:
                    print(f"\n{C.WARNING}No empty slots available!{C.RESET}")
                    input("\nPress Enter to continue...")
                    return

                loc_choice = input(f"\nSelect location: ").strip()
                loc_idx = int(loc_choice) - 1

                if 0 <= loc_idx < len(empty_slots):
                    floor, pos = empty_slots[loc_idx]

                    # Build room
                    self.vault_layout[floor][pos].room_type = room_type
                    self.vault_layout[floor][pos].under_construction = False
                    self.resources.remove("caps", config.cost)
                    self.log_event(f"Built {room_type.value} on Floor {floor + 1}")

                    print(f"\n{C.SUCCESS}✓ {room_type.value} built on Floor {floor + 1}!{C.RESET}")

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def upgrade_room_menu(self):
        """Upgrade existing rooms"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}⬆️  UPGRADE ROOM{C.RESET}\n")

        # Find upgradeable rooms
        upgradeable = []
        for floor in self.vault_layout:
            for room in floor:
                if room.room_type != RoomType.EMPTY and room.level < 3:
                    upgradeable.append(room)

        if not upgradeable:
            print(f"{C.WARNING}No rooms available for upgrade.{C.RESET}\n")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        print(f"{C.BOLD}Upgradeable Rooms:{C.RESET}")
        for idx, room in enumerate(upgradeable, 1):
            cost = room.get_upgrade_cost()
            affordable = "✓" if self.resources.caps >= cost else "✗"
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} [{affordable}] {room.room_type.value} (Lvl {room.level}) - {cost} caps")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select room to upgrade: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(upgradeable):
                room = upgradeable[idx]
                cost = room.get_upgrade_cost()

                if self.resources.has_enough("caps", cost):
                    room.level += 1
                    self.resources.remove("caps", cost)
                    self.log_event(f"Upgraded {room.room_type.value} to Level {room.level}")
                    print(f"\n{C.SUCCESS}✓ {room.room_type.value} upgraded to Level {room.level}!{C.RESET}")
                else:
                    print(f"\n{C.DANGER}Not enough caps!{C.RESET}")

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def rush_production_menu(self):
        """Rush room production"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}⚡ RUSH PRODUCTION{C.RESET}\n")

        rushable = []
        for floor in self.vault_layout:
            for room in floor:
                if room.can_rush():
                    rushable.append(room)

        if not rushable:
            print(f"{C.WARNING}No rooms available to rush.{C.RESET}\n")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        print(f"{C.BOLD}Rushable Rooms:{C.RESET}")
        for idx, room in enumerate(rushable, 1):
            workers = room.assigned_dwellers
            avg_luck = 5
            if workers:
                dweller_objs = [d for d in self.dwellers if d.name in workers]
                avg_luck = sum(d.luck for d in dweller_objs) // len(dweller_objs) if dweller_objs else 5

            success_rate = 50 + (avg_luck * 5)
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} (Success: {success_rate}%)")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select room to rush: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(rushable):
                room = rushable[idx]
                workers = [d for d in self.dwellers if d.name in room.assigned_dwellers]
                avg_luck = sum(d.luck for d in workers) // len(workers) if workers else 5
                success_rate = 50 + (avg_luck * 5)

                print(f"\n{C.INFO}Rushing {room.room_type.value}... (Success rate: {success_rate}%){C.RESET}")
                time.sleep(0.5)

                if random.randint(1, 100) <= success_rate:
                    # Success!
                    production = room.get_production(self.dwellers)
                    bonus_amount = sum(production.values()) * 3
                    bonus_caps = random.randint(30, 60)

                    for resource, amount in production.items():
                        self.resources.add(resource, amount * 3)

                    self.resources.add("caps", bonus_caps)
                    room.rush_cooldown = 3

                    print(f"\n{C.SUCCESS}✨ SUCCESS! Produced extra resources and earned {bonus_caps} caps!{C.RESET}")
                    self.log_event(f"Successfully rushed {room.room_type.value}")
                else:
                    # Failure - incident
                    room.has_incident = True
                    room.incident_strength = random.randint(5, 10)
                    print(f"\n{C.DANGER}💥 FAILURE! Incident in {room.room_type.value}!{C.RESET}")
                    self.log_event(f"Rush failed - incident in {room.room_type.value}")

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def fight_incident_menu(self):
        """Fight incidents in rooms"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}⚔️  FIGHT INCIDENT{C.RESET}\n")

        incidents = []
        for floor in self.vault_layout:
            for room in floor:
                if room.has_incident:
                    incidents.append(room)

        if not incidents:
            print(f"{C.INFO}No active incidents.{C.RESET}\n")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        print(f"{C.BOLD}Active Incidents:{C.RESET}")
        for idx, room in enumerate(incidents, 1):
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} - Threat Level: {room.incident_strength}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select incident to fight: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(incidents):
                room = incidents[idx]

                # Select fighters
                available = [d for d in self.dwellers if not d.on_expedition]
                print(f"\n{C.BOLD}Available Dwellers:{C.RESET}")
                for i, dweller in enumerate(available, 1):
                    combat_power = dweller.get_combat_power()
                    print(f"  {C.SUCCESS}[{i}]{C.RESET} {dweller.name} - Combat Power: {combat_power}")

                fighters_input = input(f"\nSelect up to 3 fighters (e.g., '1,2,3'): ").strip()
                fighter_indices = [int(x.strip()) - 1 for x in fighters_input.split(',') if x.strip()]

                fighters = [available[i] for i in fighter_indices if 0 <= i < len(available)][:3]

                if fighters:
                    total_combat = sum(f.get_combat_power() for f in fighters)
                    print(f"\n{C.INFO}Total Combat Power: {total_combat} vs Incident: {room.incident_strength}{C.RESET}")
                    time.sleep(0.5)

                    if total_combat >= room.incident_strength:
                        print(f"\n{C.SUCCESS}✓ Incident resolved!{C.RESET}")
                        room.has_incident = False
                        room.incident_strength = 0
                        self.log_event(f"Incident resolved in {room.room_type.value}")
                        for fighter in fighters:
                            fighter.add_experience(10)
                    else:
                        damage_per_fighter = max(5, (room.incident_strength - total_combat) // len(fighters))
                        for fighter in fighters:
                            fighter.modify_health(-damage_per_fighter)
                        print(f"\n{C.WARNING}⚠️ Fighters took damage but incident weakened!{C.RESET}")
                        room.incident_strength = max(0, room.incident_strength - total_combat)

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def manage_equipment_menu(self):
        """Manage dweller equipment"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}🎒 MANAGE EQUIPMENT{C.RESET}\n")

        if not self.equipment_inventory:
            print(f"{C.WARNING}No equipment in inventory.{C.RESET}\n")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        print(f"{C.BOLD}Inventory:{C.RESET}")
        for idx, equip_key in enumerate(self.equipment_inventory, 1):
            equipment = EQUIPMENT_LIBRARY[equip_key]
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {equipment.icon} {equipment.name} - {equipment.get_description()}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select equipment to assign: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.equipment_inventory):
                equip_key = self.equipment_inventory[idx]
                equipment = EQUIPMENT_LIBRARY[equip_key]

                # Select dweller
                print(f"\n{C.BOLD}Select Dweller:{C.RESET}")
                available = [d for d in self.dwellers if not d.on_expedition]
                for i, dweller in enumerate(available, 1):
                    current = ""
                    if equipment.equipment_type == EquipmentType.WEAPON and dweller.weapon:
                        current = f"(has {EQUIPMENT_LIBRARY[dweller.weapon].name})"
                    elif equipment.equipment_type == EquipmentType.OUTFIT and dweller.outfit:
                        current = f"(has {EQUIPMENT_LIBRARY[dweller.outfit].name})"
                    print(f"  {C.SUCCESS}[{i}]{C.RESET} {dweller.name} {current}")

                dweller_choice = input(f"\nSelect dweller: ").strip()
                dweller_idx = int(dweller_choice) - 1

                if 0 <= dweller_idx < len(available):
                    dweller = available[dweller_idx]

                    # Equip
                    if equipment.equipment_type == EquipmentType.WEAPON:
                        if dweller.weapon:
                            self.equipment_inventory.append(dweller.weapon)
                        dweller.weapon = equip_key
                    else:
                        if dweller.outfit:
                            self.equipment_inventory.append(dweller.outfit)
                        dweller.outfit = equip_key

                    self.equipment_inventory.remove(equip_key)
                    print(f"\n{C.SUCCESS}✓ Equipped {equipment.name} to {dweller.name}!{C.RESET}")
                    self.log_event(f"{dweller.name} equipped {equipment.name}")

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def assign_workers_menu(self):
        """Assign dwellers to rooms"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}👷 ASSIGN WORKERS{C.RESET}\n")

        # Find idle dwellers
        idle = [d for d in self.dwellers if not d.assigned_room and not d.on_expedition]

        if not idle:
            print(f"{C.WARNING}No idle dwellers available.{C.RESET}\n")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            return

        print(f"{C.BOLD}Idle Dwellers:{C.RESET}")
        for idx, dweller in enumerate(idle, 1):
            best_stat = max([("STR", dweller.strength), ("PER", dweller.perception),
                            ("END", dweller.endurance), ("CHA", dweller.charisma),
                            ("INT", dweller.intelligence), ("AGI", dweller.agility),
                            ("LCK", dweller.luck)], key=lambda x: x[1])
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - Best: {best_stat[0]}:{best_stat[1]}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"Select dweller: ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(idle):
                dweller = idle[idx]

                # Find assignable rooms
                assignable = []
                for floor in self.vault_layout:
                    for room in floor:
                        if room.can_assign_dweller():
                            assignable.append(room)

                if not assignable:
                    print(f"\n{C.WARNING}No rooms with available slots.{C.RESET}")
                    input("\nPress Enter to continue...")
                    return

                print(f"\n{C.BOLD}Available Rooms:{C.RESET}")
                for i, room in enumerate(assignable, 1):
                    workers = len(room.assigned_dwellers)
                    capacity = ROOM_CONFIGS[room.room_type].capacity
                    print(f"  {C.SUCCESS}[{i}]{C.RESET} {room.room_type.value} ({workers}/{capacity})")

                room_choice = input(f"\nSelect room: ").strip()
                room_idx = int(room_choice) - 1

                if 0 <= room_idx < len(assignable):
                    room = assignable[room_idx]
                    room.assigned_dwellers.append(dweller.name)
                    dweller.assigned_room = (room.floor, room.position)
                    print(f"\n{C.SUCCESS}✓ {dweller.name} assigned to {room.room_type.value}!{C.RESET}")
                    self.log_event(f"{dweller.name} assigned to {room.room_type.value}")

        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def manage_dwellers_menu(self):
        """Manage dwellers (heal, unassign, etc.)"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}👥 MANAGE DWELLERS{C.RESET}\n")
        print(f"  {C.SUCCESS}[1]{C.RESET} Unassign Dweller")
        print(f"  {C.SUCCESS}[2]{C.RESET} Heal Dweller (50 caps)")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"Select option: ").strip()

        if choice == "1":
            # Unassign
            assigned = [d for d in self.dwellers if d.assigned_room]
            if not assigned:
                print(f"\n{C.WARNING}No assigned dwellers.{C.RESET}")
                input("\nPress Enter to continue...")
                return

            print(f"\n{C.BOLD}Assigned Dwellers:{C.RESET}")
            for idx, dweller in enumerate(assigned, 1):
                floor, pos = dweller.assigned_room
                room = self.vault_layout[floor][pos]
                print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - {room.room_type.value}")

            dweller_choice = input(f"\nSelect dweller to unassign: ").strip()
            try:
                idx = int(dweller_choice) - 1
                if 0 <= idx < len(assigned):
                    dweller = assigned[idx]
                    floor, pos = dweller.assigned_room
                    room = self.vault_layout[floor][pos]
                    room.assigned_dwellers.remove(dweller.name)
                    dweller.assigned_room = None
                    print(f"\n{C.SUCCESS}✓ {dweller.name} unassigned.{C.RESET}")
            except (ValueError, IndexError):
                pass

        elif choice == "2":
            # Heal
            injured = [d for d in self.dwellers if d.health < 100]
            if not injured:
                print(f"\n{C.INFO}All dwellers are healthy!{C.RESET}")
                input("\nPress Enter to continue...")
                return

            print(f"\n{C.BOLD}Injured Dwellers:{C.RESET}")
            for idx, dweller in enumerate(injured, 1):
                print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - Health: {dweller.health}%")

            dweller_choice = input(f"\nSelect dweller to heal: ").strip()
            try:
                idx = int(dweller_choice) - 1
                if 0 <= idx < len(injured):
                    if self.resources.has_enough("caps", 50):
                        dweller = injured[idx]
                        dweller.modify_health(50)
                        self.resources.remove("caps", 50)
                        print(f"\n{C.SUCCESS}✓ {dweller.name} healed!{C.RESET}")
                        self.log_event(f"{dweller.name} healed (+50 health)")
                    else:
                        print(f"\n{C.DANGER}Not enough caps!{C.RESET}")
            except (ValueError, IndexError):
                pass

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def view_details_menu(self):
        """View detailed information"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}📊 VIEW DETAILS{C.RESET}\n")
        print(f"  {C.SUCCESS}[1]{C.RESET} View All Dwellers")
        print(f"  {C.SUCCESS}[2]{C.RESET} View All Rooms")
        print(f"  {C.SUCCESS}[3]{C.RESET} View Event History")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"Select option: ").strip()

        if choice == "1":
            self.clear_screen()
            self.print_header()
            print(f"{C.BOLD}ALL DWELLERS:{C.RESET}\n")
            for dweller in self.dwellers:
                status = "ON EXPEDITION" if dweller.on_expedition else ("WORKING" if dweller.assigned_room else "IDLE")
                print(f"{C.BOLD}{dweller.name}{C.RESET} (Lvl {dweller.level}) - {status}")
                print(f"  Health: {dweller.health}% | Happiness: {dweller.happiness}%")
                print(f"  SPECIAL: S:{dweller.strength} P:{dweller.perception} E:{dweller.endurance} C:{dweller.charisma} I:{dweller.intelligence} A:{dweller.agility} L:{dweller.luck}")
                if dweller.learned_skills:
                    print(f"  Skills: {', '.join([SKILL_LIBRARY[s].name for s in dweller.learned_skills])}")
                print()
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

        elif choice == "2":
            self.clear_screen()
            self.print_header()
            print(f"{C.BOLD}ALL ROOMS:{C.RESET}\n")
            for floor_idx, floor in enumerate(self.vault_layout):
                for room in floor:
                    if room.room_type != RoomType.EMPTY:
                        adjacency_bonus = self.calculate_adjacency_bonus(floor_idx, room.position)
                        production = room.get_production(self.dwellers, adjacency_bonus)
                        prod_str = ", ".join([f"+{v} {k}" for k, v in production.items()]) if production else "None"
                        bonus_str = f" (+{adjacency_bonus*100:.0f}% adjacency)" if adjacency_bonus > 0 else ""
                        print(f"{room.room_type.value} (Lvl {room.level}) - Floor {floor_idx + 1}")
                        print(f"  Workers: {len(room.assigned_dwellers)}/{ROOM_CONFIGS[room.room_type].capacity}")
                        print(f"  Production: {prod_str}{bonus_str}")
                        print()
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

        elif choice == "3":
            self.clear_screen()
            self.print_header()
            print(f"{C.BOLD}EVENT HISTORY:{C.RESET}\n")
            for event in self.event_log[-20:]:
                print(f"  • {event}")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    # =================================================================
    # TURN PROCESSING (with v4.0 integration)
    # =================================================================

    def process_turn(self):
        """Process end of turn with all features"""
        self.day += 1

        # 1. Production
        for floor_idx, floor in enumerate(self.vault_layout):
            for pos, room in enumerate(floor):
                adjacency_bonus = self.calculate_adjacency_bonus(floor_idx, pos)
                production = room.get_production(self.dwellers, adjacency_bonus)
                for resource, amount in production.items():
                    self.resources.add(resource, amount)

        # 2. Consumption with rationing
        dweller_count = len([d for d in self.dwellers if not d.on_expedition])
        power_consumed = self.resources.consume_with_rationing("power", dweller_count)
        water_consumed = self.resources.consume_with_rationing("water", dweller_count)
        food_consumed = self.resources.consume_with_rationing("food", dweller_count)

        # Penalties for insufficient resources
        if power_consumed < dweller_count:
            for dweller in self.dwellers:
                dweller.modify_happiness(-2)

        if water_consumed < dweller_count:
            for dweller in self.dwellers:
                dweller.modify_health(-5)
                dweller.modify_happiness(-3)

        if food_consumed < dweller_count:
            for dweller in self.dwellers:
                dweller.modify_health(-3)
                dweller.modify_happiness(-2)

        # 3. Random events (20% chance)
        if random.random() < 0.2:
            events = [
                self._event_new_arrival,
                self._event_resource_find,
                self._event_raider_attack,
                self._event_skill_gain,
            ]
            random.choice(events)()

        # 4. Update room cooldowns
        for floor in self.vault_layout:
            for room in floor:
                if room.rush_cooldown > 0:
                    room.rush_cooldown -= 1

        # 5. Process expedition returns (v4.0)
        self.process_expedition_returns()

        # 6. Quest progression (v4.0) - random chance for new quest
        if random.random() < 0.1 and AI_ENABLED:
            active_count = len([q for q in self.active_quests if q.status == QuestStatus.ACTIVE])
            if active_count < 3:
                new_quest = generate_quest(self)
                self.active_quests.append(new_quest)
                self.log_event(f"📜 New quest available: {new_quest.title}")

        # 7. Check for game over
        if all(d.health <= 0 for d in self.dwellers):
            self.game_over = True

        self.log_event(f"=== Day {self.day} ===")

    def _event_new_arrival(self):
        """Random event: new dweller arrives"""
        first_names = ["Sarah", "John", "Emma", "Michael", "Alice", "David", "Lisa", "James", "Chris", "Taylor"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore"]

        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        new_dweller = Dweller(
            name=name,
            strength=random.randint(2, 8),
            perception=random.randint(2, 8),
            endurance=random.randint(2, 8),
            charisma=random.randint(2, 8),
            intelligence=random.randint(2, 8),
            agility=random.randint(2, 8),
            luck=random.randint(2, 8),
            happiness=random.randint(50, 70),
            personality_outlook=random.choice(PERSONALITY_TRAITS["outlook"]),
            personality_work_ethic=random.choice(PERSONALITY_TRAITS["work_ethic"]),
            personality_social=random.choice(PERSONALITY_TRAITS["social"]),
            personality_courage=random.choice(PERSONALITY_TRAITS["courage"])
        )
        self.dwellers.append(new_dweller)
        self.log_event(f"👤 {name} joined the vault!")

    def _event_resource_find(self):
        """Random event: find resources"""
        resources_found = {
            "power": random.randint(5, 15),
            "water": random.randint(5, 15),
            "food": random.randint(5, 15),
            "caps": random.randint(30, 80)
        }

        for resource, amount in resources_found.items():
            self.resources.add(resource, amount)

        self.log_event(f"✨ Found resources! (+{resources_found['caps']} caps)")

    def _event_raider_attack(self):
        """Random event: raiders attack"""
        damage = random.randint(10, 25)
        for dweller in self.dwellers[:min(3, len(self.dwellers))]:
            dweller.modify_health(-damage)
            dweller.modify_happiness(-10)

        self.log_event(f"💀 Raiders attacked! Dwellers injured.")

    def _event_skill_gain(self):
        """Random event: dweller improves stats"""
        if self.dwellers:
            dweller = random.choice(self.dwellers)
            stat = random.choice(["strength", "perception", "endurance", "charisma", "intelligence", "agility", "luck"])
            dweller.modify_stat(stat, 1)
            self.log_event(f"📈 {dweller.name} improved {stat.upper()}!")

    # =================================================================
    # SAVE/LOAD SYSTEM
    # =================================================================

    def save_game(self):
        """Save game state"""
        save_data = {
            "day": self.day,
            "resources": asdict(self.resources),
            "dwellers": [asdict(d) for d in self.dwellers],
            "vault_layout": [[asdict(r) for r in floor] for floor in self.vault_layout],
            "event_log": self.event_log[-50:],
            "equipment_inventory": self.equipment_inventory,
            "active_quests": [asdict(q) for q in self.active_quests],
            "completed_quests": [asdict(q) for q in self.completed_quests],
            "current_objective_type": self.current_objective.objective_type.value if self.current_objective else None
        }

        with open("vault_save_v4.json", "w") as f:
            json.dump(save_data, f, indent=2)

        print(f"\n{C.SUCCESS}✓ Game saved!{C.RESET}")
        time.sleep(1)

    # =================================================================
    # GAME LOOP
    # =================================================================

    def game_loop(self):
        """Main game loop"""
        while not self.game_over:
            self.clear_screen()
            self.print_header()
            self.print_resources()
            self.print_dweller_info()
            self.print_vault_layout()
            self.print_event_log()
            self.print_menu()

            if self.nl_mode:
                command = input(f"{C.AI}💬 > {C.RESET}").strip()
                if command:
                    self.process_nl_command(command)
                continue

            choice = input(f"{C.BOLD}> {C.RESET}").strip().lower()

            if choice == 'b':
                self.build_room_menu()
            elif choice == 'u':
                self.upgrade_room_menu()
            elif choice == 'h':
                self.rush_production_menu()
            elif choice == 'd':
                self.manage_dwellers_menu()
            elif choice == 'r':
                self.assign_workers_menu()
            elif choice == 'i':
                self.fight_incident_menu()
            elif choice == 'g':
                self.manage_equipment_menu()
            elif choice == 'e':
                self.process_turn()
                time.sleep(1)
            elif choice == 'v':
                self.view_details_menu()
            elif choice == 'q':
                self.view_quests_menu()
            elif choice == 'x':
                self.expedition_menu()
            elif choice == 'k':
                self.learn_skills_menu()
            elif choice == 'o':
                self.objectives_menu()
            elif choice == 'a' and AI_ENABLED:
                self.ai_advisor_menu()
            elif choice == 't' and AI_ENABLED:
                self.talk_to_dweller_menu()
            elif choice == 'n' and AI_ENABLED:
                self.natural_language_mode()
            elif choice == 's':
                self.save_game()
            elif choice == 'z':
                confirm = input(f"\n{C.WARNING}Quit? (y/n): {C.RESET}").strip().lower()
                if confirm == 'y':
                    break

        if self.game_over:
            self.clear_screen()
            print(f"\n{C.DANGER}{C.BOLD}GAME OVER{C.RESET}\n")
            print(f"Your vault survived {self.day} days.\n")
            input("Press Enter to exit...")

    def show_intro(self):
        """Show game introduction"""
        self.clear_screen()

        ai_status = f"{C.AI}🤖 AI FEATURES: ENABLED{C.RESET}" if AI_ENABLED else f"{C.WARNING}🤖 AI FEATURES: DISABLED{C.RESET}"

        intro_text = f"""
{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            VAULT 13 - SURVIVAL PROTOCOL v4.0 ULTIMATE                ║
║                                                                      ║
║          Welcome to the Post-Nuclear Age, Overseer!                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}

{ai_status}

{C.BOLD}NEW in v4.0 ULTIMATE EDITION:{C.RESET}
  • {C.QUEST}📜 AI Quest Generator{C.RESET} - Procedural story campaigns
  • {C.INFO}🏜️  Wasteland Expeditions{C.RESET} - Send dwellers to explore
  • {C.SKILL}⭐ Dweller Skills System{C.RESET} - RPG progression & abilities
  • {C.INFO}🎯 Victory Objectives{C.RESET} - Multiple ways to win
  • {C.SUCCESS}✨ Room Adjacency Bonuses{C.RESET} - Strategic placement matters

{C.BOLD}v3.0 AI Features:{C.RESET}
  • AI Overseer Advisor, Dweller Dialogue, Natural Language Commands

{C.BOLD}v2.0 Core Features:{C.RESET}
  • Rush Production, Room Upgrades, Combat, Equipment, Smart Rationing

{C.SUCCESS}The ultimate vault management experience awaits!{C.RESET}
"""
        print(intro_text)
        input(f"\n{C.BOLD}Press Enter to begin...{C.RESET}")


def main():
    """Main entry point"""
    print(f"\n{C.HEADER}Loading VAULT 13 v4.0 Ultimate Edition...{C.RESET}\n")
    time.sleep(1)

    game = VaultGame()
    game.show_intro()
    game.game_loop()

    print(f"\n{C.INFO}Thank you for playing VAULT 13 v4.0!{C.RESET}\n")


if __name__ == '__main__':
    main()
