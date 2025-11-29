#!/usr/bin/env python3
"""
VAULT 13 - v10.0 ULTIMATE ENHANCEMENTS
All improvements organized by phase

This module adds comprehensive new features to Vault 13:
- Phase 1: Quick Wins (shortcuts, random names, bulk actions)
- Phase 2: Enhanced Trade & Economy
- Phase 3: Dweller Specialization & Career Paths
- Phase 4: Expedition Overhaul
- Phase 5: Seasons & Time Progression
- Phase 6: UX Polish & Accessibility
- Phase 7: Statistics & Analytics
- Phase 8: Radio Station & Diplomacy
- Phase 9: Legacy/Generational System
- Phase 10: Code Quality Infrastructure
"""

import random
import time
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set, Any
from enum import Enum
from datetime import datetime
from collections import defaultdict

# =============================================================================
# PHASE 1: QUICK WINS
# =============================================================================

# Random name generator
FIRST_NAMES_MALE = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan",
    "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin",
    "Scott", "Brandon", "Benjamin", "Samuel", "Raymond", "Gregory", "Frank",
    "Alexander", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose",
    # Wasteland-themed names
    "Atom", "Rad", "Nuka", "Blast", "Vault", "Pip", "Wasteland", "Raider",
    "Dogmeat", "Fawkes", "Boone", "Arcade", "Rex", "Veronica", "Cass"
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna", "Brenda",
    "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine",
    "Debra", "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather",
    # Wasteland-themed names
    "Nova", "Moira", "Sierra", "Rose", "Sunny", "Willow", "Tandi", "Lynette"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
    "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera",
    # Vault-themed last names
    "Vault", "Bunker", "Shelter", "Haven", "Underground", "Atomic", "Radcliffe",
    "Steele", "Power", "Fusion", "Nuka", "Rad", "Fallout", "Wastelander"
]


def generate_random_name(gender: str = None) -> str:
    """Generate a random dweller name"""
    if gender is None:
        gender = random.choice(["M", "F"])

    if gender == "M":
        first = random.choice(FIRST_NAMES_MALE)
    else:
        first = random.choice(FIRST_NAMES_FEMALE)

    last = random.choice(LAST_NAMES)
    return f"{first} {last}"


def generate_unique_name(existing_names: List[str], gender: str = None, max_attempts: int = 100) -> str:
    """Generate a unique name not in the existing list"""
    for _ in range(max_attempts):
        name = generate_random_name(gender)
        if name not in existing_names:
            return name
    # Fallback: add a number
    base_name = generate_random_name(gender)
    counter = 2
    while f"{base_name} {counter}" in existing_names:
        counter += 1
    return f"{base_name} {counter}"


# Keyboard shortcuts cheat sheet
KEYBOARD_SHORTCUTS = {
    "Essential": {
        "B": "Build new rooms",
        "U": "Upgrade rooms",
        "H": "Rush production",
        "D": "Manage dwellers",
        "E": "End turn / advance day",
        "?": "Show help & shortcuts",
        "/": "Command palette (search)",
        "~": "Quick actions menu",
    },
    "Management": {
        "Q": "View quests",
        "X": "Expeditions",
        "T": "Technology/Research",
        "C": "Craft items",
        "K": "Skills menu",
        "O": "Objectives",
    },
    "Society": {
        "F": "Families & relationships",
        "P": "Policies & government",
        "I": "Disasters",
        "M": "Merchant/Trade",
        "L": "Factions",
    },
    "Advanced": {
        "V": "Vault expansion",
        "G": "Legendary items",
        "R": "Prestige & achievements",
        "Y": "Pets",
        "N": "Daily challenges",
        "J": "Dweller stories",
    },
    "Views": {
        "1": "Dashboard overview",
        "2": "Dweller details",
        "3": "Timeline/History",
        "4": "Settings",
        "5": "Population pyramid",
        "6": "Faction radar",
        "7": "Tech tree map",
        "8": "Export data",
        "9": "Performance stats",
    },
    "System": {
        "S": "Save game",
        "Z": "Quit game",
        "A": "AI Advisor",
        "W": "Talk to dweller",
    }
}


def show_keyboard_shortcuts():
    """Display formatted keyboard shortcuts"""
    print("\n" + "=" * 60)
    print("                 KEYBOARD SHORTCUTS")
    print("=" * 60)

    for category, shortcuts in KEYBOARD_SHORTCUTS.items():
        print(f"\n  {category.upper()}:")
        for key, desc in shortcuts.items():
            print(f"    [{key}] {desc}")

    print("\n" + "=" * 60)
    print("  TIP: Type full words too! 'build', 'upgrade', 'quest'...")
    print("=" * 60 + "\n")


# Bulk Actions System
@dataclass
class BulkAction:
    """Represents a bulk action that can be performed on multiple items"""
    name: str
    description: str
    action_type: str  # "assign", "heal", "equip", "train"


BULK_ACTIONS = {
    "assign_idle": BulkAction("Assign All Idle", "Assign all idle dwellers to optimal rooms", "assign"),
    "heal_all": BulkAction("Heal All", "Heal all injured dwellers (costs caps)", "heal"),
    "equip_best": BulkAction("Auto-Equip Best", "Equip best available gear to all", "equip"),
    "unassign_all": BulkAction("Unassign All", "Remove all dwellers from rooms", "unassign"),
    "train_all": BulkAction("Train All Idle", "Send all idle dwellers to training", "train"),
    "collect_all": BulkAction("Collect All Resources", "Collect from all production rooms", "collect"),
}


def get_optimal_room_for_dweller(dweller, rooms) -> Optional[Tuple[int, int]]:
    """Find the best room for a dweller based on their stats"""
    stat_to_room = {
        "strength": "Power Generator",
        "perception": "Water Treatment",
        "agility": "Diner",
        "intelligence": "Science Lab",
        "charisma": "Radio Room",
    }

    # Find dweller's best stat
    stats = {
        "strength": dweller.strength,
        "perception": dweller.perception,
        "agility": dweller.agility,
        "intelligence": dweller.intelligence,
        "charisma": dweller.charisma,
    }
    best_stat = max(stats, key=stats.get)
    preferred_room_type = stat_to_room.get(best_stat)

    # Find available room of that type
    for floor_idx, floor in enumerate(rooms):
        for pos_idx, room in enumerate(floor):
            if (room.room_type.value == preferred_room_type and
                room.can_assign_dweller()):
                return (floor_idx, pos_idx)

    # Fallback: any available production room
    for floor_idx, floor in enumerate(rooms):
        for pos_idx, room in enumerate(floor):
            if room.can_assign_dweller() and room.room_type.value not in ["Empty", "Living Quarters", "Storage Room"]:
                return (floor_idx, pos_idx)

    return None


# Room Efficiency Indicators
def calculate_room_efficiency(room, dwellers_list) -> dict:
    """Calculate and return room efficiency metrics"""
    config = room.room_type

    efficiency = {
        "worker_efficiency": 0.0,
        "level_bonus": room.level * 0.25,
        "adjacency_bonus": 0.0,
        "total_efficiency": 0.0,
        "rating": "N/A",
        "color": "gray",
        "recommendations": []
    }

    if room.room_type.value == "Empty":
        return efficiency

    # Calculate worker efficiency based on stat match
    stat_required = None
    stat_mapping = {
        "Power Generator": "strength",
        "Water Treatment": "perception",
        "Diner": "agility",
        "Science Lab": "intelligence",
        "Radio Room": "charisma",
    }

    stat_required = stat_mapping.get(room.room_type.value)

    if room.assigned_dwellers and stat_required:
        total_stat = 0
        for name in room.assigned_dwellers:
            dweller = next((d for d in dwellers_list if d.name == name), None)
            if dweller:
                total_stat += getattr(dweller, stat_required, 5)

        avg_stat = total_stat / len(room.assigned_dwellers)
        efficiency["worker_efficiency"] = (avg_stat / 10) * 100

        if avg_stat < 5:
            efficiency["recommendations"].append(f"Assign dwellers with higher {stat_required.upper()}")

    # Check capacity
    capacity = getattr(room, 'capacity', 2)
    if len(room.assigned_dwellers) < capacity:
        efficiency["recommendations"].append(f"Add {capacity - len(room.assigned_dwellers)} more worker(s)")

    # Calculate total
    efficiency["total_efficiency"] = (
        efficiency["worker_efficiency"] * 0.6 +
        efficiency["level_bonus"] * 100 * 0.3 +
        efficiency["adjacency_bonus"] * 0.1
    )

    # Rating
    if efficiency["total_efficiency"] >= 80:
        efficiency["rating"] = "Excellent"
        efficiency["color"] = "green"
    elif efficiency["total_efficiency"] >= 60:
        efficiency["rating"] = "Good"
        efficiency["color"] = "yellow"
    elif efficiency["total_efficiency"] >= 40:
        efficiency["rating"] = "Average"
        efficiency["color"] = "orange"
    else:
        efficiency["rating"] = "Poor"
        efficiency["color"] = "red"

    return efficiency


# Smart Action Recommendations
def get_recommended_actions(game_state: dict) -> List[dict]:
    """Generate smart recommendations based on current game state"""
    recommendations = []

    # Check resources
    if game_state.get("food", 100) < 20:
        recommendations.append({
            "priority": 1,
            "action": "Build Diner",
            "reason": "Food critically low!",
            "command": "b",
            "icon": "!"
        })

    if game_state.get("water", 100) < 20:
        recommendations.append({
            "priority": 1,
            "action": "Build Water Treatment",
            "reason": "Water critically low!",
            "command": "b",
            "icon": "!"
        })

    if game_state.get("power", 100) < 20:
        recommendations.append({
            "priority": 1,
            "action": "Build Power Generator",
            "reason": "Power critically low!",
            "command": "b",
            "icon": "!"
        })

    # Check idle dwellers
    idle_count = game_state.get("idle_dwellers", 0)
    if idle_count > 0:
        recommendations.append({
            "priority": 2,
            "action": f"Assign {idle_count} idle dweller(s)",
            "reason": "Idle dwellers not contributing",
            "command": "d",
            "icon": "i"
        })

    # Check for injured
    injured_count = game_state.get("injured_dwellers", 0)
    if injured_count > 0:
        recommendations.append({
            "priority": 2,
            "action": f"Heal {injured_count} injured dweller(s)",
            "reason": "Injured dwellers have reduced productivity",
            "command": "d",
            "icon": "+"
        })

    # Check happiness
    unhappy_count = game_state.get("unhappy_dwellers", 0)
    if unhappy_count > 0:
        recommendations.append({
            "priority": 3,
            "action": "Improve vault happiness",
            "reason": f"{unhappy_count} unhappy dweller(s)",
            "command": "4",
            "icon": ":"
        })

    # Suggest upgrades if caps available
    if game_state.get("caps", 0) > 500:
        recommendations.append({
            "priority": 4,
            "action": "Upgrade a room",
            "reason": "Improve production efficiency",
            "command": "u",
            "icon": "^"
        })

    # Suggest research
    if not game_state.get("researching", False):
        recommendations.append({
            "priority": 3,
            "action": "Start research",
            "reason": "Unlock new technologies",
            "command": "t",
            "icon": "?"
        })

    # Suggest expedition if available
    if game_state.get("expedition_ready", False):
        recommendations.append({
            "priority": 3,
            "action": "Send an expedition",
            "reason": "Explore the wasteland for loot",
            "command": "x",
            "icon": ">"
        })

    # Sort by priority
    recommendations.sort(key=lambda x: x["priority"])

    return recommendations[:5]  # Top 5 recommendations


# =============================================================================
# PHASE 2: ENHANCED TRADE & ECONOMY SYSTEM
# =============================================================================

class CaravanType(Enum):
    """Types of trading caravans"""
    MERCHANT = "Merchant Guild"
    WEAPONS = "Arms Dealer"
    MEDICAL = "Medical Supplies"
    TECH = "Tech Trader"
    SCAVENGER = "Scavenger"
    BLACK_MARKET = "Black Market"


@dataclass
class TradeCaravan:
    """A trading caravan that visits the vault"""
    caravan_id: str
    caravan_type: CaravanType
    name: str
    arrival_day: int
    departure_day: int
    reputation_required: int = 0
    trades: List['TradeItem'] = field(default_factory=list)
    special_dialogue: str = ""
    faction_affiliation: Optional[str] = None
    price_modifier: float = 1.0  # Affected by reputation and events


@dataclass
class TradeItem:
    """An item available for trade"""
    item_id: str
    name: str
    base_price: int
    quantity: int
    item_type: str  # "weapon", "armor", "consumable", "resource", "rare"
    is_buying: bool = False  # True = caravan buys from you
    price_trend: float = 1.0  # Dynamic pricing multiplier
    rarity: int = 1  # 1-5
    description: str = ""


@dataclass
class EconomicEvent:
    """Economic events that affect prices"""
    event_id: str
    name: str
    description: str
    affected_items: List[str]  # item types affected
    price_multiplier: float
    duration_days: int
    start_day: int


ECONOMIC_EVENTS = {
    "shortage": {
        "name": "Supply Shortage",
        "description": "Wasteland trade routes disrupted",
        "affected_items": ["food", "water"],
        "price_multiplier": 1.5,
        "duration": 5
    },
    "surplus": {
        "name": "Supply Surplus",
        "description": "Good hunting season",
        "affected_items": ["food"],
        "price_multiplier": 0.7,
        "duration": 5
    },
    "tech_boom": {
        "name": "Tech Discovery",
        "description": "Pre-war cache found nearby",
        "affected_items": ["weapon", "tech"],
        "price_multiplier": 0.8,
        "duration": 3
    },
    "raider_activity": {
        "name": "Raider Activity",
        "description": "Raiders disrupting trade",
        "affected_items": ["all"],
        "price_multiplier": 1.3,
        "duration": 7
    },
}


class TradingSystem:
    """Manages all trading operations"""

    def __init__(self):
        self.active_caravans: List[TradeCaravan] = []
        self.trade_history: List[dict] = []
        self.economic_events: List[EconomicEvent] = []
        self.market_prices: Dict[str, float] = {
            "food": 1.0, "water": 1.0, "power": 1.0,
            "weapon": 1.0, "armor": 1.0, "medical": 1.0
        }
        self.total_traded_value: int = 0
        self.favorite_trader: Optional[str] = None

    def generate_caravan(self, day: int, vault_reputation: Dict[str, int]) -> TradeCaravan:
        """Generate a random trading caravan"""
        caravan_type = random.choice(list(CaravanType))

        caravan = TradeCaravan(
            caravan_id=f"caravan_{day}_{random.randint(1000, 9999)}",
            caravan_type=caravan_type,
            name=self._generate_caravan_name(caravan_type),
            arrival_day=day,
            departure_day=day + random.randint(2, 4),
        )

        # Generate trade items based on type
        caravan.trades = self._generate_trade_items(caravan_type)

        # Apply reputation modifier
        faction = self._get_faction_for_type(caravan_type)
        if faction and faction in vault_reputation:
            rep = vault_reputation[faction]
            if rep > 50:
                caravan.price_modifier = 0.9  # 10% discount
            elif rep < -50:
                caravan.price_modifier = 1.2  # 20% markup

        return caravan

    def _generate_caravan_name(self, caravan_type: CaravanType) -> str:
        """Generate a thematic caravan name"""
        prefixes = {
            CaravanType.MERCHANT: ["Lucky", "Honest", "Trusty", "Grand"],
            CaravanType.WEAPONS: ["Iron", "Steel", "Combat", "Heavy"],
            CaravanType.MEDICAL: ["Doc", "Healer's", "Life", "Remedy"],
            CaravanType.TECH: ["Circuit", "Spark", "Binary", "Tech"],
            CaravanType.SCAVENGER: ["Rusty", "Salvage", "Junk", "Finder's"],
            CaravanType.BLACK_MARKET: ["Shadow", "Midnight", "Silent", "Dark"],
        }

        suffixes = ["Caravan", "Trading Co.", "Supplies", "Express", "Goods"]

        prefix = random.choice(prefixes.get(caravan_type, ["Trade"]))
        suffix = random.choice(suffixes)

        return f"{prefix} {suffix}"

    def _generate_trade_items(self, caravan_type: CaravanType) -> List[TradeItem]:
        """Generate items based on caravan type"""
        items = []

        item_pools = {
            CaravanType.MERCHANT: [
                ("Food Rations", 10, "consumable", 5),
                ("Clean Water", 8, "consumable", 5),
                ("Stimpak", 50, "medical", 3),
                ("Caps Stash", 100, "currency", 1),
            ],
            CaravanType.WEAPONS: [
                ("10mm Pistol", 100, "weapon", 2),
                ("Combat Rifle", 250, "weapon", 1),
                ("Laser Pistol", 200, "weapon", 1),
                ("Ammo Box", 30, "consumable", 5),
                ("Combat Armor", 300, "armor", 1),
            ],
            CaravanType.MEDICAL: [
                ("Stimpak", 40, "medical", 5),
                ("RadAway", 35, "medical", 3),
                ("Med-X", 50, "medical", 2),
                ("Doctor's Bag", 100, "medical", 1),
                ("Blood Pack", 25, "medical", 3),
            ],
            CaravanType.TECH: [
                ("Fusion Cell", 30, "tech", 5),
                ("Circuitry", 40, "tech", 3),
                ("Sensor Module", 60, "tech", 2),
                ("Energy Weapon", 350, "weapon", 1),
                ("Robot Parts", 80, "tech", 2),
            ],
            CaravanType.SCAVENGER: [
                ("Scrap Metal", 5, "resource", 10),
                ("Cloth", 8, "resource", 8),
                ("Electronics", 15, "resource", 5),
                ("Random Weapon", 80, "weapon", 1),
                ("Pre-War Artifact", 200, "rare", 1),
            ],
            CaravanType.BLACK_MARKET: [
                ("Mysterious Serum", 150, "rare", 1),
                ("Stolen Tech", 300, "tech", 1),
                ("Legendary Parts", 500, "rare", 1),
                ("Questionable Stimpaks", 25, "medical", 5),
                ("Hot Goods", 100, "rare", 2),
            ],
        }

        pool = item_pools.get(caravan_type, item_pools[CaravanType.MERCHANT])

        for name, price, item_type, qty in pool:
            items.append(TradeItem(
                item_id=name.lower().replace(" ", "_"),
                name=name,
                base_price=price,
                quantity=qty,
                item_type=item_type,
            ))

        return items

    def _get_faction_for_type(self, caravan_type: CaravanType) -> Optional[str]:
        """Get associated faction for caravan type"""
        mapping = {
            CaravanType.MERCHANT: "Merchant Guild",
            CaravanType.WEAPONS: "Brotherhood",
            CaravanType.SCAVENGER: "Settler Alliance",
        }
        return mapping.get(caravan_type)

    def calculate_price(self, item: TradeItem, is_selling: bool = False) -> int:
        """Calculate final price with all modifiers"""
        price = item.base_price * item.price_trend

        # Apply economic events
        for event in self.economic_events:
            if item.item_type in event.affected_items or "all" in event.affected_items:
                price *= event.price_multiplier

        # Selling discount
        if is_selling:
            price *= 0.6  # Vault sells at 60% of buy price

        return max(1, int(price))

    def execute_trade(self, item: TradeItem, quantity: int, is_buying: bool,
                     vault_caps: int) -> Tuple[bool, str, int]:
        """Execute a trade transaction"""
        price = self.calculate_price(item, not is_buying)
        total_cost = price * quantity

        if is_buying:
            if vault_caps < total_cost:
                return False, "Not enough caps!", 0
            if quantity > item.quantity:
                return False, "Not enough in stock!", 0

            item.quantity -= quantity
            self.trade_history.append({
                "type": "buy",
                "item": item.name,
                "quantity": quantity,
                "cost": total_cost
            })
            self.total_traded_value += total_cost
            return True, f"Purchased {quantity}x {item.name}", -total_cost
        else:
            # Selling
            item.quantity += quantity
            self.trade_history.append({
                "type": "sell",
                "item": item.name,
                "quantity": quantity,
                "earned": total_cost
            })
            self.total_traded_value += total_cost
            return True, f"Sold {quantity}x {item.name}", total_cost


# =============================================================================
# PHASE 3: DWELLER SPECIALIZATION & CAREER PATHS
# =============================================================================

class CareerPath(Enum):
    """Career specialization paths for dwellers"""
    ENGINEER = "Engineer"
    SCIENTIST = "Scientist"
    SOLDIER = "Soldier"
    MEDIC = "Medic"
    LEADER = "Leader"
    EXPLORER = "Explorer"
    CRAFTSMAN = "Craftsman"


@dataclass
class CareerLevel:
    """A level within a career path"""
    level: int
    title: str
    requirements: Dict[str, int]  # stat requirements
    experience_required: int
    bonuses: Dict[str, float]
    special_ability: Optional[str] = None


CAREER_PATHS = {
    CareerPath.ENGINEER: {
        "description": "Masters of power and machinery",
        "primary_stat": "strength",
        "secondary_stat": "intelligence",
        "levels": [
            CareerLevel(1, "Apprentice", {"strength": 3}, 0, {"power_production": 0.1}),
            CareerLevel(2, "Technician", {"strength": 5}, 100, {"power_production": 0.2}),
            CareerLevel(3, "Engineer", {"strength": 6, "intelligence": 4}, 300, {"power_production": 0.3, "repair_speed": 0.2}),
            CareerLevel(4, "Senior Engineer", {"strength": 7, "intelligence": 5}, 600, {"power_production": 0.4, "repair_speed": 0.3}),
            CareerLevel(5, "Chief Engineer", {"strength": 8, "intelligence": 6}, 1000, {"power_production": 0.5, "repair_speed": 0.5}, "Emergency Power Boost"),
        ]
    },
    CareerPath.SCIENTIST: {
        "description": "Researchers and innovators",
        "primary_stat": "intelligence",
        "secondary_stat": "perception",
        "levels": [
            CareerLevel(1, "Lab Assistant", {"intelligence": 3}, 0, {"research_speed": 0.1}),
            CareerLevel(2, "Researcher", {"intelligence": 5}, 100, {"research_speed": 0.2}),
            CareerLevel(3, "Scientist", {"intelligence": 6, "perception": 4}, 300, {"research_speed": 0.3, "tech_discount": 0.1}),
            CareerLevel(4, "Lead Scientist", {"intelligence": 7, "perception": 5}, 600, {"research_speed": 0.4, "tech_discount": 0.2}),
            CareerLevel(5, "Chief Scientist", {"intelligence": 8, "perception": 6}, 1000, {"research_speed": 0.5, "tech_discount": 0.3}, "Eureka Moment"),
        ]
    },
    CareerPath.SOLDIER: {
        "description": "Protectors of the vault",
        "primary_stat": "strength",
        "secondary_stat": "endurance",
        "levels": [
            CareerLevel(1, "Recruit", {"strength": 3}, 0, {"combat_damage": 0.1}),
            CareerLevel(2, "Guard", {"strength": 5}, 100, {"combat_damage": 0.2, "defense": 0.1}),
            CareerLevel(3, "Soldier", {"strength": 6, "endurance": 4}, 300, {"combat_damage": 0.3, "defense": 0.2}),
            CareerLevel(4, "Sergeant", {"strength": 7, "endurance": 5}, 600, {"combat_damage": 0.4, "defense": 0.3, "squad_bonus": 0.1}),
            CareerLevel(5, "Commander", {"strength": 8, "endurance": 6}, 1000, {"combat_damage": 0.5, "defense": 0.4, "squad_bonus": 0.2}, "Rally Cry"),
        ]
    },
    CareerPath.MEDIC: {
        "description": "Healers and caretakers",
        "primary_stat": "intelligence",
        "secondary_stat": "charisma",
        "levels": [
            CareerLevel(1, "First Aid", {"intelligence": 3}, 0, {"healing_power": 0.1}),
            CareerLevel(2, "Nurse", {"intelligence": 5}, 100, {"healing_power": 0.2}),
            CareerLevel(3, "Medic", {"intelligence": 6, "charisma": 4}, 300, {"healing_power": 0.3, "medicine_efficiency": 0.2}),
            CareerLevel(4, "Doctor", {"intelligence": 7, "charisma": 5}, 600, {"healing_power": 0.4, "medicine_efficiency": 0.3}),
            CareerLevel(5, "Chief Medical Officer", {"intelligence": 8, "charisma": 6}, 1000, {"healing_power": 0.5, "medicine_efficiency": 0.5}, "Miracle Cure"),
        ]
    },
    CareerPath.LEADER: {
        "description": "Inspirers and organizers",
        "primary_stat": "charisma",
        "secondary_stat": "intelligence",
        "levels": [
            CareerLevel(1, "Speaker", {"charisma": 3}, 0, {"happiness_aura": 0.05}),
            CareerLevel(2, "Coordinator", {"charisma": 5}, 100, {"happiness_aura": 0.1, "work_efficiency": 0.05}),
            CareerLevel(3, "Supervisor", {"charisma": 6, "intelligence": 4}, 300, {"happiness_aura": 0.15, "work_efficiency": 0.1}),
            CareerLevel(4, "Manager", {"charisma": 7, "intelligence": 5}, 600, {"happiness_aura": 0.2, "work_efficiency": 0.15}),
            CareerLevel(5, "Overseer's Aide", {"charisma": 8, "intelligence": 6}, 1000, {"happiness_aura": 0.3, "work_efficiency": 0.2}, "Inspiring Speech"),
        ]
    },
    CareerPath.EXPLORER: {
        "description": "Wasteland adventurers",
        "primary_stat": "endurance",
        "secondary_stat": "luck",
        "levels": [
            CareerLevel(1, "Scout", {"endurance": 3}, 0, {"exploration_speed": 0.1}),
            CareerLevel(2, "Pathfinder", {"endurance": 5}, 100, {"exploration_speed": 0.2, "loot_bonus": 0.1}),
            CareerLevel(3, "Explorer", {"endurance": 6, "luck": 4}, 300, {"exploration_speed": 0.3, "loot_bonus": 0.2}),
            CareerLevel(4, "Veteran Explorer", {"endurance": 7, "luck": 5}, 600, {"exploration_speed": 0.4, "loot_bonus": 0.3, "survival_chance": 0.1}),
            CareerLevel(5, "Wasteland Legend", {"endurance": 8, "luck": 6}, 1000, {"exploration_speed": 0.5, "loot_bonus": 0.5, "survival_chance": 0.2}, "Sixth Sense"),
        ]
    },
    CareerPath.CRAFTSMAN: {
        "description": "Makers and builders",
        "primary_stat": "agility",
        "secondary_stat": "intelligence",
        "levels": [
            CareerLevel(1, "Helper", {"agility": 3}, 0, {"crafting_speed": 0.1}),
            CareerLevel(2, "Apprentice", {"agility": 5}, 100, {"crafting_speed": 0.2, "material_efficiency": 0.1}),
            CareerLevel(3, "Craftsman", {"agility": 6, "intelligence": 4}, 300, {"crafting_speed": 0.3, "material_efficiency": 0.2}),
            CareerLevel(4, "Master Craftsman", {"agility": 7, "intelligence": 5}, 600, {"crafting_speed": 0.4, "material_efficiency": 0.3, "quality_bonus": 0.1}),
            CareerLevel(5, "Legendary Artisan", {"agility": 8, "intelligence": 6}, 1000, {"crafting_speed": 0.5, "material_efficiency": 0.5, "quality_bonus": 0.2}, "Masterwork Creation"),
        ]
    },
}


@dataclass
class MentorshipRelation:
    """Mentorship between dwellers"""
    mentor_id: str
    student_id: str
    career_path: CareerPath
    progress: float = 0.0  # 0-100
    days_mentoring: int = 0
    completed: bool = False


class CareerSystem:
    """Manages dweller careers and mentorships"""

    def __init__(self):
        self.dweller_careers: Dict[str, dict] = {}  # dweller_id -> career data
        self.active_mentorships: List[MentorshipRelation] = []
        self.promotions_given: int = 0

    def assign_career(self, dweller_id: str, career: CareerPath):
        """Assign a dweller to a career path"""
        self.dweller_careers[dweller_id] = {
            "career": career,
            "level": 1,
            "experience": 0,
            "promoted_dates": [],
        }

    def add_experience(self, dweller_id: str, amount: int) -> Optional[str]:
        """Add career experience and check for promotion"""
        if dweller_id not in self.dweller_careers:
            return None

        career_data = self.dweller_careers[dweller_id]
        career_data["experience"] += amount

        # Check for promotion
        career_info = CAREER_PATHS[career_data["career"]]
        current_level = career_data["level"]

        if current_level < 5:
            next_level = career_info["levels"][current_level]
            if career_data["experience"] >= next_level.experience_required:
                career_data["level"] = current_level + 1
                self.promotions_given += 1
                return f"Promoted to {next_level.title}!"

        return None

    def get_career_bonuses(self, dweller_id: str) -> Dict[str, float]:
        """Get all bonuses from a dweller's career"""
        if dweller_id not in self.dweller_careers:
            return {}

        career_data = self.dweller_careers[dweller_id]
        career_info = CAREER_PATHS[career_data["career"]]
        level_info = career_info["levels"][career_data["level"] - 1]

        return level_info.bonuses

    def start_mentorship(self, mentor_id: str, student_id: str) -> bool:
        """Start a mentorship relationship"""
        if mentor_id not in self.dweller_careers:
            return False

        mentor_career = self.dweller_careers[mentor_id]["career"]
        mentor_level = self.dweller_careers[mentor_id]["level"]

        if mentor_level < 3:  # Must be level 3+ to mentor
            return False

        # Check if student is already in a mentorship
        for m in self.active_mentorships:
            if m.student_id == student_id and not m.completed:
                return False

        self.active_mentorships.append(MentorshipRelation(
            mentor_id=mentor_id,
            student_id=student_id,
            career_path=mentor_career,
        ))

        # Auto-assign career to student if they don't have one
        if student_id not in self.dweller_careers:
            self.assign_career(student_id, mentor_career)

        return True

    def update_mentorships(self):
        """Update all active mentorships (call each turn)"""
        for mentorship in self.active_mentorships:
            if mentorship.completed:
                continue

            # Progress increases each day
            mentorship.progress += random.uniform(2, 5)
            mentorship.days_mentoring += 1

            if mentorship.progress >= 100:
                mentorship.completed = True
                # Bonus XP for completing mentorship
                self.add_experience(mentorship.student_id, 50)


# =============================================================================
# PHASE 4: EXPEDITION OVERHAUL
# =============================================================================

class LocationType(Enum):
    """Types of discoverable wasteland locations"""
    RUINS = "Ruins"
    VAULT = "Abandoned Vault"
    MILITARY = "Military Base"
    TOWN = "Ruined Town"
    FACTORY = "Factory"
    HOSPITAL = "Hospital"
    SCHOOL = "School"
    LABORATORY = "Research Lab"
    BUNKER = "Underground Bunker"
    CAVE = "Cave System"


@dataclass
class WastelandLocation:
    """A discoverable location in the wasteland"""
    location_id: str
    name: str
    location_type: LocationType
    distance: int  # In hours
    danger_level: int  # 1-10
    discovered: bool = False
    cleared: bool = False
    loot_quality: int = 1  # 1-5
    special_loot: Optional[str] = None
    can_establish_outpost: bool = False
    description: str = ""


@dataclass
class ExpeditionStage:
    """A stage in a multi-stage expedition"""
    stage_number: int
    description: str
    encounter_type: str  # "combat", "loot", "choice", "rest", "hazard"
    difficulty: int
    choices: List[str] = field(default_factory=list)
    outcomes: Dict[str, dict] = field(default_factory=dict)
    completed: bool = False


@dataclass
class EnhancedExpedition:
    """Multi-stage expedition with companions"""
    expedition_id: str
    destination: WastelandLocation
    team: List[str]  # dweller IDs
    leader_id: str
    stages: List[ExpeditionStage] = field(default_factory=list)
    current_stage: int = 0
    loot_collected: List[str] = field(default_factory=list)
    total_damage_taken: int = 0
    start_day: int = 0
    estimated_return: int = 0
    status: str = "preparing"  # preparing, traveling, exploring, returning, completed
    log: List[str] = field(default_factory=list)


class ExpeditionSystem:
    """Manages all expedition operations"""

    def __init__(self):
        self.known_locations: List[WastelandLocation] = []
        self.active_expeditions: List[EnhancedExpedition] = []
        self.completed_expeditions: int = 0
        self.outposts: List[WastelandLocation] = []
        self.expedition_log: List[str] = []

    def initialize_locations(self):
        """Generate initial wasteland locations"""
        location_templates = [
            ("Dusty Town Ruins", LocationType.RUINS, 4, 2, 2),
            ("Abandoned Factory", LocationType.FACTORY, 6, 4, 3),
            ("Old Military Outpost", LocationType.MILITARY, 8, 6, 4),
            ("Vault 15", LocationType.VAULT, 12, 7, 5),
            ("Radiated Hospital", LocationType.HOSPITAL, 5, 5, 3),
            ("Pre-War School", LocationType.SCHOOL, 3, 2, 2),
            ("Research Facility Alpha", LocationType.LABORATORY, 10, 8, 5),
            ("Deep Caves", LocationType.CAVE, 7, 5, 3),
        ]

        for name, loc_type, dist, danger, loot in location_templates:
            self.known_locations.append(WastelandLocation(
                location_id=name.lower().replace(" ", "_"),
                name=name,
                location_type=loc_type,
                distance=dist,
                danger_level=danger,
                loot_quality=loot,
                discovered=random.random() < 0.3,  # 30% start discovered
            ))

    def discover_location(self) -> Optional[WastelandLocation]:
        """Discover a new location"""
        undiscovered = [loc for loc in self.known_locations if not loc.discovered]
        if undiscovered:
            location = random.choice(undiscovered)
            location.discovered = True
            return location
        return None

    def create_expedition(self, destination: WastelandLocation, team: List[str],
                         leader_id: str, current_day: int) -> EnhancedExpedition:
        """Create a new multi-stage expedition"""
        expedition = EnhancedExpedition(
            expedition_id=f"exp_{current_day}_{random.randint(1000, 9999)}",
            destination=destination,
            team=team,
            leader_id=leader_id,
            start_day=current_day,
            estimated_return=current_day + destination.distance * 2,
        )

        # Generate stages
        expedition.stages = self._generate_stages(destination)

        self.active_expeditions.append(expedition)
        return expedition

    def _generate_stages(self, destination: WastelandLocation) -> List[ExpeditionStage]:
        """Generate expedition stages based on location"""
        stages = []
        num_stages = 3 + (destination.danger_level // 3)

        stage_types = ["travel", "encounter", "loot", "choice", "hazard"]

        for i in range(num_stages):
            if i == 0:
                stage_type = "travel"
            elif i == num_stages - 1:
                stage_type = "loot"
            else:
                stage_type = random.choice(stage_types)

            stage = ExpeditionStage(
                stage_number=i + 1,
                description=self._generate_stage_description(stage_type, destination),
                encounter_type=stage_type,
                difficulty=destination.danger_level,
            )

            if stage_type == "choice":
                stage.choices = ["Go left path", "Go right path", "Scout ahead carefully"]
                stage.outcomes = {
                    "Go left path": {"loot": True, "damage": 10},
                    "Go right path": {"loot": False, "damage": 0, "discovery": True},
                    "Scout ahead carefully": {"loot": True, "damage": 0, "time": 2},
                }

            stages.append(stage)

        return stages

    def _generate_stage_description(self, stage_type: str, location: WastelandLocation) -> str:
        """Generate description for expedition stage"""
        descriptions = {
            "travel": [
                "The team makes their way through the wasteland...",
                "Traveling across the dusty roads...",
                "The journey continues under the scorching sun...",
            ],
            "encounter": [
                "A group of raiders blocks the path!",
                "Wild creatures emerge from the ruins!",
                "An unexpected patrol crosses your route!",
            ],
            "loot": [
                f"The team reaches {location.name} and begins searching...",
                "A promising cache of supplies is found!",
                "Pre-war containers are scattered around...",
            ],
            "choice": [
                "The path splits ahead. Which way?",
                "A locked door blocks progress. Find another way or try to open it?",
                "A mysterious survivor offers to trade information...",
            ],
            "hazard": [
                "Radiation levels spike dangerously!",
                "The floor gives way beneath your feet!",
                "A toxic cloud drifts across the area!",
            ],
        }

        return random.choice(descriptions.get(stage_type, ["The expedition continues..."]))

    def process_stage(self, expedition: EnhancedExpedition, choice: Optional[str] = None) -> dict:
        """Process the current stage of an expedition"""
        stage = expedition.stages[expedition.current_stage]
        result = {"success": True, "message": "", "loot": [], "damage": 0}

        if stage.encounter_type == "encounter":
            # Combat resolution
            team_power = len(expedition.team) * 10  # Simplified
            enemy_power = stage.difficulty * 5

            if team_power > enemy_power:
                result["message"] = "Victory! The team defeats the enemies."
                result["loot"].append("combat_loot")
            else:
                result["message"] = "The team barely survives the encounter."
                result["damage"] = enemy_power - team_power + 10

        elif stage.encounter_type == "loot":
            loot_amount = expedition.destination.loot_quality
            for _ in range(loot_amount):
                result["loot"].append(f"loot_{random.randint(1, 100)}")
            result["message"] = f"Found {loot_amount} items!"

        elif stage.encounter_type == "choice" and choice:
            outcome = stage.outcomes.get(choice, {})
            if outcome.get("loot"):
                result["loot"].append("choice_loot")
            result["damage"] = outcome.get("damage", 0)
            result["message"] = f"Chose: {choice}"

        elif stage.encounter_type == "hazard":
            result["damage"] = stage.difficulty * 2
            result["message"] = "The team navigates the hazard carefully."

        else:
            result["message"] = stage.description

        # Apply results
        expedition.total_damage_taken += result["damage"]
        expedition.loot_collected.extend(result["loot"])
        expedition.log.append(f"Stage {stage.stage_number}: {result['message']}")
        stage.completed = True
        expedition.current_stage += 1

        # Check if expedition is complete
        if expedition.current_stage >= len(expedition.stages):
            expedition.status = "returning"

        return result


# =============================================================================
# PHASE 5: SEASONS & TIME SYSTEM
# =============================================================================

class Season(Enum):
    """Seasons affecting the vault"""
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"
    WINTER = "Winter"
    RADSTORM = "Radstorm Season"  # Special season


@dataclass
class SeasonEffect:
    """Effects of a season on the vault"""
    resource_modifiers: Dict[str, float]  # production multipliers
    event_chances: Dict[str, float]  # event probability modifiers
    mood_modifier: int  # happiness modifier
    special_events: List[str]  # season-specific events
    description: str


SEASON_EFFECTS = {
    Season.SPRING: SeasonEffect(
        resource_modifiers={"food": 1.2, "water": 1.1, "power": 1.0},
        event_chances={"raider": 0.8, "trader": 1.2, "recruits": 1.3},
        mood_modifier=5,
        special_events=["spring_festival", "new_growth", "travelers_arrive"],
        description="New life blooms across the wasteland. Good hunting and foraging."
    ),
    Season.SUMMER: SeasonEffect(
        resource_modifiers={"food": 1.0, "water": 0.8, "power": 1.1},
        event_chances={"raider": 1.2, "trader": 1.0, "drought": 1.5},
        mood_modifier=0,
        special_events=["heat_wave", "water_shortage", "summer_celebration"],
        description="Scorching heat makes water scarce but power systems work efficiently."
    ),
    Season.AUTUMN: SeasonEffect(
        resource_modifiers={"food": 1.3, "water": 1.0, "power": 1.0},
        event_chances={"raider": 0.9, "trader": 1.3, "harvest": 2.0},
        mood_modifier=10,
        special_events=["harvest_festival", "trade_fair", "preparation_time"],
        description="Harvest season brings abundance. Time to stockpile for winter."
    ),
    Season.WINTER: SeasonEffect(
        resource_modifiers={"food": 0.7, "water": 0.9, "power": 1.3},
        event_chances={"raider": 0.5, "trader": 0.7, "cold_snap": 1.5},
        mood_modifier=-10,
        special_events=["winter_festival", "hibernation", "cold_snap"],
        description="Cold grips the wasteland. Power demand is high, foraging is difficult."
    ),
    Season.RADSTORM: SeasonEffect(
        resource_modifiers={"food": 0.5, "water": 0.5, "power": 0.8},
        event_chances={"raider": 0.3, "trader": 0.2, "mutation": 2.0, "radiation": 3.0},
        mood_modifier=-20,
        special_events=["radstorm", "mutation_outbreak", "shelter_lockdown"],
        description="Deadly radiation storms sweep the wasteland. Stay indoors!"
    ),
}


class TimeSystem:
    """Manages time progression and seasons"""

    def __init__(self):
        self.current_day: int = 1
        self.current_season: Season = Season.SPRING
        self.days_in_season: int = 0
        self.season_length: int = 25  # Days per season
        self.year: int = 1
        self.special_events_triggered: Set[str] = set()
        self.season_history: List[Tuple[int, Season]] = []

    def advance_day(self) -> Optional[dict]:
        """Advance time by one day"""
        self.current_day += 1
        self.days_in_season += 1

        result = {"day": self.current_day, "events": []}

        # Check for season change
        if self.days_in_season >= self.season_length:
            result["season_change"] = self._advance_season()

        # Check for year change
        if self.current_day % (self.season_length * 4) == 0:
            self.year += 1
            result["new_year"] = self.year

        # Random radstorm chance (rare)
        if self.current_season != Season.RADSTORM and random.random() < 0.01:
            result["radstorm_warning"] = True

        return result

    def _advance_season(self) -> dict:
        """Move to the next season"""
        self.days_in_season = 0
        self.season_history.append((self.current_day, self.current_season))

        season_order = [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER]
        current_idx = season_order.index(self.current_season) if self.current_season in season_order else 0
        next_idx = (current_idx + 1) % 4

        old_season = self.current_season
        self.current_season = season_order[next_idx]

        return {
            "old_season": old_season,
            "new_season": self.current_season,
            "effects": SEASON_EFFECTS[self.current_season]
        }

    def get_current_effects(self) -> SeasonEffect:
        """Get current season effects"""
        return SEASON_EFFECTS.get(self.current_season, SEASON_EFFECTS[Season.SPRING])

    def trigger_radstorm(self, duration: int = 3):
        """Trigger a radstorm season"""
        self.season_history.append((self.current_day, self.current_season))
        self.current_season = Season.RADSTORM
        self.season_length = duration
        self.days_in_season = 0


# =============================================================================
# PHASE 6: UX POLISH & ACCESSIBILITY
# =============================================================================

@dataclass
class UndoAction:
    """Represents an action that can be undone"""
    action_type: str
    description: str
    data: dict
    day: int


class UndoSystem:
    """Manages undo/redo functionality"""

    def __init__(self, max_history: int = 20):
        self.undo_stack: List[UndoAction] = []
        self.redo_stack: List[UndoAction] = []
        self.max_history = max_history

    def record_action(self, action_type: str, description: str, data: dict, day: int):
        """Record an action for potential undo"""
        action = UndoAction(action_type, description, data, day)
        self.undo_stack.append(action)

        # Clear redo stack on new action
        self.redo_stack.clear()

        # Limit history size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack = self.undo_stack[-self.max_history:]

    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0

    def get_undo_description(self) -> Optional[str]:
        """Get description of last undoable action"""
        if self.undo_stack:
            return self.undo_stack[-1].description
        return None

    def pop_undo(self) -> Optional[UndoAction]:
        """Pop the last action for undo"""
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            return action
        return None

    def pop_redo(self) -> Optional[UndoAction]:
        """Pop from redo stack"""
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            return action
        return None


# Sound indicators (ASCII representation)
SOUND_EFFECTS = {
    "click": "   click   ",
    "success": " *ding* ",
    "error": " *bzzt* ",
    "alert": " BEEP! ",
    "construction": " *hammer* *hammer* ",
    "combat": " *bang* *pow* ",
    "discovery": " *sparkle* ",
    "levelup": " LEVEL UP! ",
    "trade": " *ka-ching* ",
    "door": " *whoosh* ",
}


class AccessibilitySettings:
    """Accessibility configuration"""

    def __init__(self):
        self.high_contrast_mode: bool = False
        self.screen_reader_mode: bool = False
        self.reduced_motion: bool = False
        self.large_text: bool = False
        self.colorblind_mode: str = "none"  # "none", "deuteranopia", "protanopia", "tritanopia"
        self.sound_indicators: bool = True
        self.animation_speed: float = 1.0  # 0.5 = slower, 2.0 = faster
        self.auto_advance_delay: float = 2.0  # seconds

    def get_color_adjusted(self, color_name: str) -> str:
        """Get color adjusted for colorblind mode"""
        colorblind_palettes = {
            "deuteranopia": {
                "green": "blue",
                "red": "orange",
            },
            "protanopia": {
                "green": "blue",
                "red": "yellow",
            },
            "tritanopia": {
                "blue": "cyan",
                "yellow": "magenta",
            },
        }

        if self.colorblind_mode in colorblind_palettes:
            return colorblind_palettes[self.colorblind_mode].get(color_name, color_name)
        return color_name

    def format_for_screen_reader(self, text: str) -> str:
        """Format text for screen reader compatibility"""
        if not self.screen_reader_mode:
            return text

        # Remove decorative elements
        text = text.replace("═", "-")
        text = text.replace("║", "|")
        text = text.replace("╔", "+")
        text = text.replace("╗", "+")
        text = text.replace("╚", "+")
        text = text.replace("╝", "+")
        text = text.replace("█", "#")
        text = text.replace("░", ".")

        # Expand emoji descriptions
        emoji_descriptions = {
            "": "(heart)",
            "": "(happy)",
            "": "(sad)",
            "": "(power)",
            "": "(water)",
            "": "(food)",
        }

        for emoji, desc in emoji_descriptions.items():
            text = text.replace(emoji, desc)

        return text


# =============================================================================
# PHASE 7: STATISTICS & ANALYTICS
# =============================================================================

@dataclass
class VaultStatistics:
    """Comprehensive vault statistics"""
    # Resource stats
    total_power_generated: int = 0
    total_water_produced: int = 0
    total_food_grown: int = 0
    peak_caps: int = 0

    # Population stats
    total_births: int = 0
    total_deaths: int = 0
    total_recruits: int = 0
    peak_population: int = 0

    # Activity stats
    total_expeditions: int = 0
    successful_expeditions: int = 0
    failed_expeditions: int = 0
    locations_discovered: int = 0

    # Combat stats
    raids_defended: int = 0
    raiders_defeated: int = 0
    total_damage_dealt: int = 0
    total_damage_taken: int = 0

    # Economic stats
    total_traded_value: int = 0
    items_crafted: int = 0
    items_sold: int = 0
    items_bought: int = 0

    # Research stats
    technologies_researched: int = 0
    total_research_points: int = 0

    # Time stats
    days_survived: int = 0
    longest_streak_without_incident: int = 0
    current_streak: int = 0


class AnalyticsDashboard:
    """Analytics and visualization system"""

    def __init__(self):
        self.stats = VaultStatistics()
        self.resource_history: Dict[str, List[int]] = defaultdict(list)
        self.population_history: List[int] = []
        self.happiness_history: List[float] = []
        self.daily_snapshots: List[dict] = []

    def record_daily_snapshot(self, game_state: dict):
        """Record a daily snapshot of vault state"""
        snapshot = {
            "day": game_state.get("day", 0),
            "population": game_state.get("population", 0),
            "happiness": game_state.get("avg_happiness", 50),
            "power": game_state.get("power", 0),
            "water": game_state.get("water", 0),
            "food": game_state.get("food", 0),
            "caps": game_state.get("caps", 0),
        }
        self.daily_snapshots.append(snapshot)

        # Update histories
        self.population_history.append(snapshot["population"])
        self.happiness_history.append(snapshot["happiness"])
        for resource in ["power", "water", "food", "caps"]:
            self.resource_history[resource].append(snapshot[resource])

        # Keep only last 100 days
        if len(self.daily_snapshots) > 100:
            self.daily_snapshots = self.daily_snapshots[-100:]

    def generate_ascii_chart(self, data: List[int], width: int = 50, height: int = 10,
                            title: str = "") -> str:
        """Generate an ASCII line chart"""
        if not data:
            return "No data available"

        lines = []
        if title:
            lines.append(title.center(width))
            lines.append("=" * width)

        max_val = max(data) if max(data) > 0 else 1
        min_val = min(data)

        # Normalize data to height
        normalized = []
        for val in data[-width:]:
            if max_val == min_val:
                normalized.append(height // 2)
            else:
                normalized.append(int((val - min_val) / (max_val - min_val) * (height - 1)))

        # Build chart
        chart_chars = "▁▂▃▄▅▆▇█"

        for row in range(height - 1, -1, -1):
            line = ""
            for col, val in enumerate(normalized):
                if val >= row:
                    line += "█"
                else:
                    line += " "

            # Add axis label
            if row == height - 1:
                lines.append(f"{max_val:>6} |{line}")
            elif row == 0:
                lines.append(f"{min_val:>6} |{line}")
            else:
                lines.append(f"       |{line}")

        # X-axis
        lines.append("       +" + "-" * len(normalized))

        return "\n".join(lines)

    def generate_sparkline(self, data: List[int], width: int = 20) -> str:
        """Generate a compact sparkline"""
        if not data:
            return " " * width

        chars = "▁▂▃▄▅▆▇█"
        max_val = max(data) if max(data) > 0 else 1
        min_val = min(data)

        result = ""
        sample = data[-width:] if len(data) > width else data

        for val in sample:
            if max_val == min_val:
                idx = len(chars) // 2
            else:
                idx = int((val - min_val) / (max_val - min_val) * (len(chars) - 1))
            result += chars[idx]

        return result.ljust(width)

    def export_to_csv(self, filename: str = "vault_stats.csv") -> bool:
        """Export statistics to CSV"""
        try:
            import csv

            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)

                # Header
                writer.writerow(["Day", "Population", "Happiness", "Power", "Water", "Food", "Caps"])

                # Data
                for snapshot in self.daily_snapshots:
                    writer.writerow([
                        snapshot["day"],
                        snapshot["population"],
                        snapshot["happiness"],
                        snapshot["power"],
                        snapshot["water"],
                        snapshot["food"],
                        snapshot["caps"],
                    ])

            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def get_summary_report(self) -> str:
        """Generate a text summary report"""
        s = self.stats

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    VAULT STATISTICS REPORT                    ║
╚══════════════════════════════════════════════════════════════╝

SURVIVAL
  Days Survived: {s.days_survived}
  Longest Peaceful Streak: {s.longest_streak_without_incident} days

POPULATION
  Current Population: {self.population_history[-1] if self.population_history else 0}
  Peak Population: {s.peak_population}
  Total Births: {s.total_births}
  Total Deaths: {s.total_deaths}
  Net Growth: {s.total_births + s.total_recruits - s.total_deaths}

RESOURCES
  Total Power Generated: {s.total_power_generated:,}
  Total Water Produced: {s.total_water_produced:,}
  Total Food Grown: {s.total_food_grown:,}
  Peak Caps: {s.peak_caps:,}

EXPLORATION
  Expeditions Completed: {s.total_expeditions}
  Success Rate: {(s.successful_expeditions/max(1,s.total_expeditions)*100):.1f}%
  Locations Discovered: {s.locations_discovered}

COMBAT
  Raids Defended: {s.raids_defended}
  Raiders Defeated: {s.raiders_defeated}
  Damage Dealt: {s.total_damage_dealt:,}
  Damage Taken: {s.total_damage_taken:,}

ECONOMY
  Total Trade Value: {s.total_traded_value:,} caps
  Items Crafted: {s.items_crafted}

RESEARCH
  Technologies: {s.technologies_researched}
  Total Research: {s.total_research_points:,} points
"""
        return report


# =============================================================================
# PHASE 8: RADIO STATION & DIPLOMACY
# =============================================================================

@dataclass
class RadioProgram:
    """A radio program that can be broadcast"""
    program_id: str
    name: str
    program_type: str  # "music", "news", "propaganda", "recruitment", "drama"
    effects: Dict[str, float]
    popularity: int = 50
    cooldown: int = 0


@dataclass
class RadioStation:
    """The vault's radio station"""
    is_active: bool = False
    current_program: Optional[RadioProgram] = None
    broadcast_range: int = 1  # Affects recruitment
    dj: Optional[str] = None  # Dweller ID
    programs: List[RadioProgram] = field(default_factory=list)
    listeners: int = 0
    reputation_boost: int = 0


class RadioSystem:
    """Manages radio broadcasting"""

    def __init__(self):
        self.station = RadioStation()
        self.broadcast_history: List[str] = []
        self.wasteland_news: List[str] = []
        self._initialize_programs()

    def _initialize_programs(self):
        """Set up default radio programs"""
        self.station.programs = [
            RadioProgram("music_classical", "Classical Selections", "music",
                        {"happiness": 0.1, "productivity": 0.05}, popularity=60),
            RadioProgram("music_jazz", "Vault Jazz Hour", "music",
                        {"happiness": 0.15, "stress": -0.1}, popularity=70),
            RadioProgram("news_wasteland", "Wasteland News", "news",
                        {"information": 0.2, "recruitment": 0.1}, popularity=50),
            RadioProgram("propaganda_unity", "Unity Hour", "propaganda",
                        {"loyalty": 0.2, "happiness": 0.05}, popularity=40),
            RadioProgram("recruitment_beacon", "Recruitment Beacon", "recruitment",
                        {"recruitment": 0.3, "reputation": 0.1}, popularity=55),
            RadioProgram("drama_wastes", "Tales from the Wastes", "drama",
                        {"happiness": 0.2, "entertainment": 0.3}, popularity=75),
        ]

    def activate_station(self, dj_id: str) -> bool:
        """Activate the radio station with a DJ"""
        self.station.is_active = True
        self.station.dj = dj_id
        return True

    def set_program(self, program_id: str) -> bool:
        """Change the current broadcast program"""
        for program in self.station.programs:
            if program.program_id == program_id:
                if program.cooldown <= 0:
                    self.station.current_program = program
                    program.cooldown = 5  # 5 turn cooldown after use
                    self.broadcast_history.append(program.name)
                    return True
        return False

    def process_broadcast(self) -> Dict[str, float]:
        """Process effects of current broadcast"""
        effects = {}

        if self.station.is_active and self.station.current_program:
            program = self.station.current_program
            effects = program.effects.copy()

            # DJ charisma bonus
            if self.station.dj:
                effects = {k: v * 1.2 for k, v in effects.items()}

        # Reduce cooldowns
        for program in self.station.programs:
            if program.cooldown > 0:
                program.cooldown -= 1

        return effects

    def generate_news(self, game_events: List[str]) -> str:
        """Generate wasteland news based on events"""
        news_templates = [
            "Reports of increased raider activity in the north...",
            "Traders report good conditions on the southern routes.",
            "A settlement was discovered near the old highway.",
            "Strange lights seen over the mountains last night.",
            "Water prices are fluctuating across the wasteland.",
        ]

        if game_events:
            news = f"Breaking: {random.choice(game_events)}"
        else:
            news = random.choice(news_templates)

        self.wasteland_news.append(news)
        return news


@dataclass
class DiplomaticRelation:
    """Diplomatic standing with a faction"""
    faction_id: str
    reputation: int = 0  # -100 to 100
    treaties: List[str] = field(default_factory=list)
    trade_agreement: bool = False
    alliance: bool = False
    at_war: bool = False
    recent_actions: List[str] = field(default_factory=list)


class DiplomacySystem:
    """Manages faction relations and diplomacy"""

    def __init__(self):
        self.relations: Dict[str, DiplomaticRelation] = {}
        self.diplomatic_events: List[str] = []
        self._initialize_factions()

    def _initialize_factions(self):
        """Initialize faction relationships"""
        factions = [
            ("raiders", -50),
            ("brotherhood", 0),
            ("merchant_guild", 20),
            ("settler_alliance", 10),
            ("outcasts", 0),
        ]

        for faction_id, starting_rep in factions:
            self.relations[faction_id] = DiplomaticRelation(
                faction_id=faction_id,
                reputation=starting_rep,
            )

    def modify_reputation(self, faction_id: str, amount: int, reason: str = "") -> int:
        """Modify reputation with a faction"""
        if faction_id not in self.relations:
            return 0

        relation = self.relations[faction_id]
        old_rep = relation.reputation
        relation.reputation = max(-100, min(100, relation.reputation + amount))

        if reason:
            relation.recent_actions.append(f"{reason}: {amount:+d}")

        # Check for status changes
        self._check_diplomatic_status(faction_id)

        return relation.reputation - old_rep

    def _check_diplomatic_status(self, faction_id: str):
        """Check if diplomatic status should change"""
        relation = self.relations[faction_id]

        if relation.reputation >= 75 and not relation.alliance:
            self.diplomatic_events.append(f"{faction_id} is ready to form an alliance!")
        elif relation.reputation <= -75 and not relation.at_war:
            self.diplomatic_events.append(f"{faction_id} declares hostilities!")
            relation.at_war = True
        elif relation.reputation > -50 and relation.at_war:
            self.diplomatic_events.append(f"Ceasefire possible with {faction_id}")

    def propose_treaty(self, faction_id: str, treaty_type: str) -> bool:
        """Propose a treaty with a faction"""
        if faction_id not in self.relations:
            return False

        relation = self.relations[faction_id]

        # Requirements for different treaties
        requirements = {
            "trade": 25,
            "non_aggression": 0,
            "alliance": 75,
            "mutual_defense": 50,
        }

        required_rep = requirements.get(treaty_type, 50)

        if relation.reputation >= required_rep:
            relation.treaties.append(treaty_type)
            if treaty_type == "trade":
                relation.trade_agreement = True
            elif treaty_type == "alliance":
                relation.alliance = True
            return True

        return False

    def get_faction_status(self, faction_id: str) -> str:
        """Get human-readable faction status"""
        if faction_id not in self.relations:
            return "Unknown"

        relation = self.relations[faction_id]
        rep = relation.reputation

        if relation.at_war:
            return "At War"
        elif relation.alliance:
            return "Allied"
        elif rep >= 50:
            return "Friendly"
        elif rep >= 0:
            return "Neutral"
        elif rep >= -50:
            return "Unfriendly"
        else:
            return "Hostile"


# =============================================================================
# PHASE 9: LEGACY/GENERATIONAL SYSTEM
# =============================================================================

@dataclass
class DwellerLegacy:
    """Legacy information for a deceased dweller"""
    name: str
    birth_day: int
    death_day: int
    cause_of_death: str
    achievements: List[str]
    children: List[str]
    career_peak: str
    notable_actions: List[str]
    memorial_message: str = ""


@dataclass
class FamilyTree:
    """Family tree for a dweller lineage"""
    founder_id: str
    founder_name: str
    current_generation: int = 1
    total_members: int = 1
    living_members: int = 1
    deceased_members: List[DwellerLegacy] = field(default_factory=list)
    family_traits: List[str] = field(default_factory=list)  # Inherited traits
    family_reputation: int = 0
    notable_achievements: List[str] = field(default_factory=list)


class LegacySystem:
    """Manages generational progression and family legacies"""

    def __init__(self):
        self.family_trees: Dict[str, FamilyTree] = {}
        self.vault_generation: int = 1
        self.legendary_dwellers: List[DwellerLegacy] = []
        self.vault_legacy_points: int = 0
        self.inherited_bonuses: Dict[str, float] = {}

    def create_family_tree(self, founder_id: str, founder_name: str) -> FamilyTree:
        """Create a new family tree"""
        tree = FamilyTree(
            founder_id=founder_id,
            founder_name=founder_name,
        )
        self.family_trees[founder_id] = tree
        return tree

    def record_birth(self, child_id: str, parent1_id: str, parent2_id: str):
        """Record a birth in family trees"""
        # Find parent's family tree
        for tree in self.family_trees.values():
            if tree.founder_id in [parent1_id, parent2_id]:
                tree.total_members += 1
                tree.living_members += 1

                # Check for generation advancement
                # (simplified - in full impl would track actual generations)
                if tree.total_members % 5 == 0:
                    tree.current_generation += 1
                    self.vault_generation = max(self.vault_generation, tree.current_generation)

                return tree

        return None

    def record_death(self, dweller_id: str, dweller_name: str, cause: str,
                    achievements: List[str], children: List[str], career: str):
        """Record a dweller's death and create legacy"""
        legacy = DwellerLegacy(
            name=dweller_name,
            birth_day=0,  # Would be tracked in full impl
            death_day=0,  # Current day
            cause_of_death=cause,
            achievements=achievements,
            children=children,
            career_peak=career,
            notable_actions=[],
        )

        # Check if this dweller was notable
        if len(achievements) >= 5 or len(children) >= 3:
            self.legendary_dwellers.append(legacy)
            self.vault_legacy_points += 10

        # Update family tree
        for tree in self.family_trees.values():
            if tree.founder_id == dweller_id:
                tree.deceased_members.append(legacy)
                tree.living_members -= 1
                return legacy

        return legacy

    def calculate_inherited_bonuses(self, parent1_traits: List[str],
                                   parent2_traits: List[str]) -> Dict[str, float]:
        """Calculate bonuses inherited from parents"""
        bonuses = {}

        # Combine unique traits
        all_traits = set(parent1_traits + parent2_traits)

        trait_bonuses = {
            "genius": {"intelligence": 0.1, "research_speed": 0.05},
            "athletic": {"strength": 0.1, "endurance": 0.05},
            "charismatic": {"charisma": 0.1, "happiness_aura": 0.03},
            "lucky": {"luck": 0.1, "critical_chance": 0.05},
        }

        for trait in all_traits:
            if trait in trait_bonuses:
                for stat, bonus in trait_bonuses[trait].items():
                    bonuses[stat] = bonuses.get(stat, 0) + bonus

        return bonuses

    def get_dynasty_report(self) -> str:
        """Generate a dynasty/legacy report"""
        report_lines = [
            "=" * 50,
            "           VAULT DYNASTY REPORT",
            "=" * 50,
            f"\nVault Generation: {self.vault_generation}",
            f"Legacy Points: {self.vault_legacy_points}",
            f"Legendary Dwellers: {len(self.legendary_dwellers)}",
            f"\nFamily Lines: {len(self.family_trees)}",
        ]

        for tree_id, tree in self.family_trees.items():
            report_lines.append(f"\n  {tree.founder_name} Dynasty:")
            report_lines.append(f"    Generation: {tree.current_generation}")
            report_lines.append(f"    Total Members: {tree.total_members}")
            report_lines.append(f"    Living: {tree.living_members}")

        if self.legendary_dwellers:
            report_lines.append("\n\nHALL OF LEGENDS:")
            for legend in self.legendary_dwellers[-5:]:  # Last 5
                report_lines.append(f"  {legend.name} - {legend.career_peak}")
                report_lines.append(f"    Achievements: {len(legend.achievements)}")

        return "\n".join(report_lines)


# =============================================================================
# PHASE 10: CODE QUALITY INFRASTRUCTURE
# =============================================================================

import logging
from enum import IntEnum


class LogLevel(IntEnum):
    """Log severity levels"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class GameLogger:
    """Structured logging system for the game"""

    def __init__(self, log_file: str = "vault_game.log"):
        self.log_file = log_file
        self.log_level = LogLevel.INFO
        self.logs: List[dict] = []
        self.max_memory_logs = 1000

        # Set up file logging
        try:
            self.file_handler = open(log_file, 'a')
        except:
            self.file_handler = None

    def set_level(self, level: LogLevel):
        """Set minimum log level"""
        self.log_level = level

    def _log(self, level: LogLevel, category: str, message: str, data: dict = None):
        """Internal logging method"""
        if level < self.log_level:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "category": category,
            "message": message,
            "data": data or {},
        }

        # Memory log
        self.logs.append(log_entry)
        if len(self.logs) > self.max_memory_logs:
            self.logs = self.logs[-self.max_memory_logs:]

        # File log
        if self.file_handler:
            try:
                self.file_handler.write(json.dumps(log_entry) + "\n")
                self.file_handler.flush()
            except:
                pass

    def debug(self, category: str, message: str, data: dict = None):
        self._log(LogLevel.DEBUG, category, message, data)

    def info(self, category: str, message: str, data: dict = None):
        self._log(LogLevel.INFO, category, message, data)

    def warning(self, category: str, message: str, data: dict = None):
        self._log(LogLevel.WARNING, category, message, data)

    def error(self, category: str, message: str, data: dict = None):
        self._log(LogLevel.ERROR, category, message, data)

    def critical(self, category: str, message: str, data: dict = None):
        self._log(LogLevel.CRITICAL, category, message, data)

    def get_recent_logs(self, count: int = 50, level: LogLevel = None,
                       category: str = None) -> List[dict]:
        """Get recent log entries with optional filtering"""
        logs = self.logs

        if level:
            logs = [l for l in logs if LogLevel[l["level"]] >= level]
        if category:
            logs = [l for l in logs if l["category"] == category]

        return logs[-count:]

    def close(self):
        """Close file handler"""
        if self.file_handler:
            self.file_handler.close()


class ConfigValidator:
    """Validates game configuration and save files"""

    SAVE_SCHEMA = {
        "version": str,
        "day": int,
        "resources": dict,
        "dwellers": list,
        "vault_layout": list,
    }

    DWELLER_SCHEMA = {
        "name": str,
        "strength": int,
        "perception": int,
        "endurance": int,
        "charisma": int,
        "intelligence": int,
        "agility": int,
        "luck": int,
        "health": int,
        "happiness": int,
    }

    @classmethod
    def validate_save_file(cls, save_data: dict) -> Tuple[bool, List[str]]:
        """Validate a save file structure"""
        errors = []

        # Check required fields
        for field, expected_type in cls.SAVE_SCHEMA.items():
            if field not in save_data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(save_data[field], expected_type):
                errors.append(f"Invalid type for {field}: expected {expected_type.__name__}")

        # Validate dwellers
        if "dwellers" in save_data:
            for i, dweller in enumerate(save_data["dwellers"]):
                dweller_errors = cls._validate_dweller(dweller, i)
                errors.extend(dweller_errors)

        # Validate resources
        if "resources" in save_data:
            resources = save_data["resources"]
            for resource in ["power", "water", "food", "caps"]:
                if resource in resources and resources[resource] < 0:
                    errors.append(f"Negative {resource} value: {resources[resource]}")

        return len(errors) == 0, errors

    @classmethod
    def _validate_dweller(cls, dweller: dict, index: int) -> List[str]:
        """Validate a single dweller"""
        errors = []
        prefix = f"Dweller[{index}]"

        for field, expected_type in cls.DWELLER_SCHEMA.items():
            if field not in dweller:
                errors.append(f"{prefix}: Missing field {field}")
            elif not isinstance(dweller[field], expected_type):
                errors.append(f"{prefix}: Invalid type for {field}")

        # Validate stat ranges
        stats = ["strength", "perception", "endurance", "charisma",
                "intelligence", "agility", "luck"]
        for stat in stats:
            if stat in dweller:
                val = dweller[stat]
                if not (1 <= val <= 10):
                    errors.append(f"{prefix}: {stat} out of range (1-10): {val}")

        # Validate health/happiness
        for field in ["health", "happiness"]:
            if field in dweller:
                val = dweller[field]
                if not (0 <= val <= 100):
                    errors.append(f"{prefix}: {field} out of range (0-100): {val}")

        return errors

    @classmethod
    def attempt_recovery(cls, save_data: dict) -> dict:
        """Attempt to recover/fix a corrupted save file"""
        recovered = save_data.copy()

        # Set defaults for missing required fields
        defaults = {
            "version": "10.0",
            "day": 1,
            "resources": {"power": 20, "water": 20, "food": 20, "caps": 500},
            "dwellers": [],
            "vault_layout": [],
        }

        for field, default in defaults.items():
            if field not in recovered:
                recovered[field] = default

        # Clamp stat values
        if "dwellers" in recovered:
            for dweller in recovered["dwellers"]:
                for stat in ["strength", "perception", "endurance", "charisma",
                           "intelligence", "agility", "luck"]:
                    if stat in dweller:
                        dweller[stat] = max(1, min(10, dweller[stat]))

                for field in ["health", "happiness"]:
                    if field in dweller:
                        dweller[field] = max(0, min(100, dweller[field]))

        # Ensure non-negative resources
        if "resources" in recovered:
            for key in recovered["resources"]:
                if recovered["resources"][key] < 0:
                    recovered["resources"][key] = 0

        return recovered


# =============================================================================
# INTEGRATION: MAIN ENHANCEMENT LOADER
# =============================================================================

class VaultEnhancementPack:
    """Main class to integrate all enhancement systems"""

    VERSION = "10.0"

    def __init__(self):
        # Phase 1: Quick Wins - integrated via functions

        # Phase 2: Trading
        self.trading = TradingSystem()

        # Phase 3: Careers
        self.careers = CareerSystem()

        # Phase 4: Expeditions
        self.expeditions = ExpeditionSystem()
        self.expeditions.initialize_locations()

        # Phase 5: Seasons
        self.time = TimeSystem()

        # Phase 6: UX
        self.undo = UndoSystem()
        self.accessibility = AccessibilitySettings()

        # Phase 7: Analytics
        self.analytics = AnalyticsDashboard()

        # Phase 8: Radio & Diplomacy
        self.radio = RadioSystem()
        self.diplomacy = DiplomacySystem()

        # Phase 9: Legacy
        self.legacy = LegacySystem()

        # Phase 10: Code Quality
        self.logger = GameLogger()

        self.logger.info("init", "Enhancement pack initialized", {"version": self.VERSION})

    def get_enhancement_summary(self) -> str:
        """Get a summary of all enhancements"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║          VAULT 13 v{self.VERSION} - ULTIMATE ENHANCEMENTS              ║
╚══════════════════════════════════════════════════════════════╝

Phase 1: Quick Wins
  - Random name generator ({len(FIRST_NAMES_MALE) + len(FIRST_NAMES_FEMALE)} first names, {len(LAST_NAMES)} last names)
  - Keyboard shortcuts cheat sheet
  - Bulk actions system ({len(BULK_ACTIONS)} actions)
  - Room efficiency indicators
  - Smart action recommendations

Phase 2: Trade & Economy
  - {len(CaravanType)} caravan types
  - Dynamic pricing system
  - Economic events
  - Faction-based trade bonuses

Phase 3: Career Paths
  - {len(CAREER_PATHS)} career specializations
  - 5 levels per career
  - Mentorship system
  - Special abilities at max level

Phase 4: Expedition Overhaul
  - {len(self.expeditions.known_locations)} discoverable locations
  - Multi-stage expeditions
  - Team companions
  - Permanent outposts

Phase 5: Seasons & Time
  - {len(Season)} seasons with unique effects
  - Seasonal events
  - Weather impacts

Phase 6: UX Polish
  - Undo/Redo system
  - Accessibility options
  - Sound indicators
  - Colorblind modes

Phase 7: Analytics
  - Resource tracking
  - ASCII charts
  - CSV export
  - Comprehensive statistics

Phase 8: Radio & Diplomacy
  - Radio station with {len(self.radio.station.programs)} programs
  - Faction diplomacy
  - Treaties and alliances

Phase 9: Legacy System
  - Family trees
  - Generational tracking
  - Hall of Legends
  - Inherited bonuses

Phase 10: Code Quality
  - Structured logging
  - Save file validation
  - Error recovery
"""


# Quick test if run directly
if __name__ == "__main__":
    print("VAULT 13 Enhancement Pack v10.0")
    print("=" * 50)

    pack = VaultEnhancementPack()
    print(pack.get_enhancement_summary())

    # Test some features
    print("\nTesting random name generation:")
    for _ in range(5):
        print(f"  - {generate_random_name()}")

    print("\nTesting keyboard shortcuts:")
    show_keyboard_shortcuts()

    print("\nAll systems initialized successfully!")
