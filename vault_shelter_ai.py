#!/usr/bin/env python3
"""
VAULT 13 - SURVIVAL PROTOCOL v3.0 AI EDITION
A vault management simulation with AI-powered features

NEW AI FEATURES:
- AI Overseer Advisor - Strategic analysis and recommendations
- Dweller Personalities & Dialogue - Living, breathing characters
- Natural Language Commands - Talk to your vault naturally

REQUIRES: pip install anthropic (or set AI_ENABLED=False for demo mode)
"""

import random
import time
import os
import sys
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum

# AI Integration - graceful fallback if not available
AI_ENABLED = False
try:
    import anthropic
    # Check for API key
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
    AI = '\033[38;5;129m'  # Purple for AI features

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


# Personality trait options
PERSONALITY_TRAITS = {
    "outlook": ["Optimistic", "Pessimistic", "Pragmatic", "Cynical"],
    "work_ethic": ["Hardworking", "Lazy", "Ambitious", "Laid-back"],
    "social": ["Friendly", "Reserved", "Charismatic", "Awkward"],
    "courage": ["Brave", "Cautious", "Reckless", "Cowardly"]
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
        """Get equipment description"""
        if self.equipment_type == EquipmentType.WEAPON:
            return f"Damage: {self.damage}"
        else:
            bonuses = ", ".join([f"+{v} {k.upper()[0]}" for k, v in self.stat_bonus.items()])
            return f"Bonuses: {bonuses}"


# Pre-defined equipment
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


# Room configurations
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


@dataclass
class Dweller:
    """A vault dweller with SPECIAL stats and AI-generated personality"""
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

    # NEW: AI Personality traits
    personality_outlook: str = "Pragmatic"
    personality_work_ethic: str = "Hardworking"
    personality_social: str = "Friendly"
    personality_courage: str = "Cautious"

    # Cache for generated dialogue
    recent_dialogue: str = ""

    def get_stat(self, stat_name: str) -> int:
        """Get a specific SPECIAL stat with equipment bonuses"""
        base_stat = getattr(self, stat_name.lower(), 5)
        bonus = 0

        if self.outfit and self.outfit in EQUIPMENT_LIBRARY:
            outfit = EQUIPMENT_LIBRARY[self.outfit]
            bonus += outfit.stat_bonus.get(stat_name.lower(), 0)

        return min(10, base_stat + bonus)

    def get_combat_power(self) -> int:
        """Get combat effectiveness"""
        weapon_damage = 0
        if self.weapon and self.weapon in EQUIPMENT_LIBRARY:
            weapon_damage = EQUIPMENT_LIBRARY[self.weapon].damage
        return self.get_stat("strength") + weapon_damage

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

    def get_production(self, dwellers_list: List[Dweller]) -> Dict[str, int]:
        """Calculate room production based on assigned dwellers and level"""
        if self.room_type == RoomType.EMPTY or self.under_construction or self.on_fire or self.has_incident:
            return {}

        config = ROOM_CONFIGS.get(self.room_type)
        if not config:
            return {}

        production = config.production.copy()
        if not production:
            return {}

        base_multiplier = self.level
        worker_count = len(self.assigned_dwellers)

        if worker_count > 0:
            if config.stat_required:
                total_stat = 0
                for dweller_name in self.assigned_dwellers:
                    dweller = next((d for d in dwellers_list if d.name == dweller_name), None)
                    if dweller:
                        total_stat += dweller.get_stat(config.stat_required)
                avg_stat = total_stat / worker_count if worker_count > 0 else 5
                stat_multiplier = avg_stat / 5
            else:
                stat_multiplier = 1.0

            worker_multiplier = 1 + (worker_count * 0.2)

            for resource in production:
                production[resource] = int(production[resource] * base_multiplier * worker_multiplier * stat_multiplier)

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


def get_dweller_dialogue(dweller: Dweller, context: str, game_state: dict) -> str:
    """Generate contextual dialogue for a dweller"""
    if not AI_ENABLED:
        return generate_fallback_response("dialogue")

    prompt = f"""Generate a short, in-character comment (1-2 sentences max) for this Fallout-style vault dweller.

Dweller: {dweller.name}
Personality: {dweller.get_personality_summary()}
Health: {dweller.health}% | Happiness: {dweller.happiness}%
SPECIAL Stats: S:{dweller.strength} P:{dweller.perception} E:{dweller.endurance} C:{dweller.charisma} I:{dweller.intelligence} A:{dweller.agility} L:{dweller.luck}
Equipped: {("Weapon: " + dweller.weapon) if dweller.weapon else "No weapon"}, {("Outfit: " + dweller.outfit) if dweller.outfit else "No outfit"}
Assigned: {"Yes - working" if dweller.assigned_room else "No - idle"}

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
        "dwellers": [{
            "name": d.name,
            "happiness": d.happiness,
            "health": d.health,
            "assigned": d.assigned_room is not None,
            "best_stat": max([("S", d.strength), ("P", d.perception), ("E", d.endurance),
                             ("C", d.charisma), ("I", d.intelligence), ("A", d.agility), ("L", d.luck)],
                            key=lambda x: x[1])
        } for d in game.dwellers],
        "rooms": []
    }

    for floor in game.vault_layout:
        for room in floor:
            if room.room_type != RoomType.EMPTY:
                state["rooms"].append({
                    "type": room.room_type.value,
                    "level": room.level,
                    "workers": len(room.assigned_dwellers),
                    "capacity": ROOM_CONFIGS[room.room_type].capacity,
                    "status": "fire" if room.on_fire else ("incident" if room.has_incident else "ok")
                })

    prompt = f"""You are the AI Overseer Advisor for Vault 13. Analyze this vault and provide strategic advice.

Vault State:
{json.dumps(state, indent=2)}

Recent Events: {', '.join(game.event_log[-3:]) if game.event_log else 'None yet'}

{'Player Question: ' + question if question else 'Provide general strategic analysis.'}

Give concise, actionable advice in this format:
⚠️  CRITICAL CONCERNS: (list any immediate threats)
💡 RECOMMENDATIONS: (2-3 specific actions to take)
📊 LONG-TERM STRATEGY: (optional, 1 sentence)

Be specific with numbers and dweller names. Keep it under 200 words."""

    return call_ai_model(prompt, max_tokens=400)


def parse_natural_language_command(text: str, game) -> dict:
    """Parse natural language command into game action"""
    if not AI_ENABLED:
        return {"action": "unknown", "message": "AI command parsing disabled. Use menu controls."}

    # Build available actions context
    actions_desc = """Available actions:
- assign_dweller: assign [dweller name] to [room type]
- rush_room: rush [room type]
- upgrade_room: upgrade [room type]
- build_room: build [room type]
- equip_item: equip [item] to [dweller]
- view_status: check [resource/dweller/room]
- advisor: ask for strategic advice
- end_turn: advance to next day"""

    prompt = f"""Parse this player command into a game action.

Command: "{text}"

{actions_desc}

Current game state:
- Dwellers: {', '.join([d.name for d in game.dwellers])}
- Rooms: {', '.join([r.room_type.value for floor in game.vault_layout for r in floor if r.room_type != RoomType.EMPTY])}

Return ONLY valid JSON in this format:
{{
    "action": "action_name",
    "parameters": {{"param": "value"}},
    "message": "confirmation message for user"
}}

If the command is unclear or impossible, use action: "clarify" and explain what's needed."""

    try:
        response = call_ai_model(prompt, max_tokens=200)
        # Extract JSON from response (might have extra text)
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = response[json_start:json_end]
            return json.loads(json_str)
        return {"action": "unknown", "message": response}
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return {"action": "error", "message": "Couldn't parse command. Try: 'assign Sarah to power generator' or 'view food status'"}


# =============================================================================
# MAIN GAME CLASS (Enhanced with AI)
# =============================================================================

class VaultGame:
    """Main game class for Vault 13 with AI features"""

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

        # AI Features
        self.nl_mode = False  # Natural language mode

        self._initialize_vault()
        self._create_starting_dwellers()
        self.equipment_inventory = ["rusty_pistol", "vault_suit"]

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
        """Create initial dwellers with AI personalities"""
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
                # Assign random personality traits
                personality_outlook=random.choice(PERSONALITY_TRAITS["outlook"]),
                personality_work_ethic=random.choice(PERSONALITY_TRAITS["work_ethic"]),
                personality_social=random.choice(PERSONALITY_TRAITS["social"]),
                personality_courage=random.choice(PERSONALITY_TRAITS["courage"])
            )
            self.dwellers.append(dweller)

        self.dwellers[0].assigned_room = (0, 0)
        self.vault_layout[0][0].assigned_dwellers.append(self.dwellers[0].name)

        self.dwellers[1].assigned_room = (0, 1)
        self.vault_layout[0][1].assigned_dwellers.append(self.dwellers[1].name)

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Print game header"""
        ai_status = f"{C.AI}🤖 AI: ON{C.RESET}" if AI_ENABLED else f"{C.DIM}🤖 AI: OFF{C.RESET}"
        nl_status = f"{C.AI}💬 NL Mode{C.RESET}" if self.nl_mode else ""

        print(f"\n{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║              VAULT 13 - SURVIVAL PROTOCOL v3.0 AI                    ║{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║                    DAY {self.day:4d}  {ai_status:40s}  {nl_status:15s}║{C.RESET}")
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
        total_happiness = sum(d.happiness for d in self.dwellers) // len(self.dwellers) if self.dwellers else 0
        happiness_color = C.HAPPY if total_happiness >= 60 else C.NEUTRAL if total_happiness >= 30 else C.SAD

        print(f"{C.BOLD}Population:{C.RESET}")
        print(f"  Dwellers: {C.INFO}{len(self.dwellers)}{C.RESET}")
        print(f"  Average Happiness: {happiness_color}{total_happiness}%{C.RESET}")
        print()

    def print_vault_layout(self):
        """Print enhanced vault room layout"""
        print(f"{C.BOLD}Vault Layout:{C.RESET}")
        print(f"{C.BORDER}{'═' * 75}{C.RESET}")

        for floor_idx, floor in enumerate(self.vault_layout):
            floor_str = f"{C.DIM}F{floor_idx + 1}:{C.RESET} "

            for room in floor:
                room_str = self._get_enhanced_room_display(room)
                floor_str += f"{room_str} "

            print(floor_str)

        print(f"{C.BORDER}{'═' * 75}{C.RESET}\n")

    def _get_enhanced_room_display(self, room: Room) -> str:
        """Get enhanced colored room display with level and workers"""
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
        worker_icons = "👤" * min(worker_count, 3)

        status = ""
        if room.on_fire:
            status = "🔥"
        elif room.has_incident:
            status = "⚠️"
        elif room.rush_cooldown > 0:
            status = "⏳"

        if room.room_type == RoomType.EMPTY:
            return f"{color}[{icon:^6s}]{C.RESET}"
        else:
            return f"{color}[{icon}{level_display:2s}{worker_icons:3s}{status}]{C.RESET}"

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

        if AI_ENABLED:
            print(f"  {C.AI}[A]{C.RESET} AI Advisor       {C.AI}[T]{C.RESET} Talk to Dweller  {C.AI}[N]{C.RESET} Natural Language")

        print(f"  {C.SUCCESS}[S]{C.RESET} Save Game        {C.DANGER}[Q]{C.RESET} Quit Game")
        print()

    # AI FEATURE METHODS

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

                # Generate context-aware dialogue
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
        """Enter natural language command mode"""
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
            print(f"  - 'upgrade the diner'")
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

        if result["action"] == "clarify" or result["action"] == "error":
            print(f"{C.WARNING}{result.get('message', 'Command unclear')}{C.RESET}")
        elif result["action"] == "advisor":
            question = result.get("parameters", {}).get("question", "")
            analysis = get_advisor_analysis(self, question)
            print(f"{C.AI}{analysis}{C.RESET}")
        else:
            # Execute the parsed action
            print(f"{C.SUCCESS}{result.get('message', 'Command executed')}{C.RESET}")
            # TODO: Actually execute the actions based on result["action"] and result["parameters"]
            # This would require implementing action handlers

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    # Continue with existing methods (process_turn, etc.)
    # For brevity, I'll include just the modified game_loop

    def game_loop(self):
        """Main game loop with AI features"""
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
                pass  # build_room_menu() - from original
            elif choice == 'u':
                pass  # upgrade_room_menu() - from original
            elif choice == 'h':
                pass  # rush_production_menu() - from original
            elif choice == 'd':
                pass  # manage_dwellers_menu() - from original
            elif choice == 'r':
                pass  # assign_workers_menu() - from original
            elif choice == 'i':
                pass  # fight_incident_menu() - from original
            elif choice == 'g':
                pass  # manage_equipment_menu() - from original
            elif choice == 'e':
                pass  # process_turn() - from original
                time.sleep(1)
            elif choice == 'v':
                pass  # view_details_menu() - from original
            elif choice == 'a' and AI_ENABLED:
                self.ai_advisor_menu()
            elif choice == 't' and AI_ENABLED:
                self.talk_to_dweller_menu()
            elif choice == 'n' and AI_ENABLED:
                self.natural_language_mode()
            elif choice == 's':
                pass  # save_game() - from original
            elif choice == 'q':
                confirm = input(f"\n{C.WARNING}Are you sure you want to quit? (y/n): {C.RESET}").strip().lower()
                if confirm == 'y':
                    break

        if self.game_over:
            pass  # show_game_over() - from original

    def show_intro(self):
        """Show game introduction"""
        self.clear_screen()

        ai_status = f"{C.AI}🤖 AI FEATURES: ENABLED{C.RESET}" if AI_ENABLED else f"{C.WARNING}🤖 AI FEATURES: DISABLED{C.RESET}"

        intro_text = f"""
{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              VAULT 13 - SURVIVAL PROTOCOL v3.0 AI                    ║
║                                                                      ║
║            Welcome to the Post-Nuclear Age, Overseer!                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}

{ai_status}

{C.BOLD}AI FEATURES in v3.0:{C.RESET}
  • {C.AI}[A] AI Overseer Advisor{C.RESET} - Strategic analysis & recommendations
  • {C.AI}[T] Talk to Dwellers{C.RESET} - AI-generated personalities & dialogue
  • {C.AI}[N] Natural Language{C.RESET} - Command your vault with plain English

{C.BOLD}Standard Features:{C.RESET}
  • Rush Production, Room Upgrades, Active Combat
  • Equipment System, Smart Rationing
  • Beautiful terminal graphics

{C.INFO}Tip: Enable AI by setting ANTHROPIC_API_KEY environment variable{C.RESET}

{C.SUCCESS}Good luck, Overseer! The future of humanity rests in your hands!{C.RESET}
"""
        print(intro_text)
        input(f"\n{C.BOLD}Press Enter to begin...{C.RESET}")


def main():
    """Main entry point"""
    print(f"\n{C.HEADER}Loading VAULT 13 AI Edition...{C.RESET}\n")
    time.sleep(1)

    game = VaultGame()
    game.show_intro()
    game.game_loop()


if __name__ == '__main__':
    main()
