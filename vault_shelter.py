#!/usr/bin/env python3
"""
VAULT 13 - SURVIVAL PROTOCOL v2.0
A vault management simulation inspired by Fallout Shelter

NEW FEATURES:
- Rush Production mechanic
- Room Upgrades (Level 1-3)
- Active Incident Resolution (combat fires/infestations)
- Enhanced Vault Visualization
- Equipment System (weapons & outfits)
- Smart Resource Allocation
"""

import random
import time
import os
import sys
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from colors import C
from platform_utils import clear_screen
from enum import Enum



    # UI Colors
    HEADER = '\033[38;5;51m'
    BORDER = '\033[38;5;39m'
    SUCCESS = '\033[38;5;46m'
    WARNING = '\033[38;5;226m'
    DANGER = '\033[38;5;196m'
    INFO = '\033[38;5;159m'

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


@dataclass
class Equipment:
    """Equipment that can be given to dwellers"""
    name: str
    equipment_type: EquipmentType
    stat_bonus: Dict[str, int] = field(default_factory=dict)  # e.g., {"strength": 2}
    damage: int = 0  # For weapons
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
    # Weapons
    "rusty_pistol": Equipment("Rusty Pistol", EquipmentType.WEAPON, damage=5, icon="🔫"),
    "laser_rifle": Equipment("Laser Rifle", EquipmentType.WEAPON, damage=15, icon="⚡"),
    "plasma_gun": Equipment("Plasma Gun", EquipmentType.WEAPON, damage=25, icon="💚"),

    # Outfits
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
    """A vault dweller with SPECIAL stats"""
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
    weapon: Optional[str] = None  # Equipment key
    outfit: Optional[str] = None  # Equipment key

    def get_stat(self, stat_name: str) -> int:
        """Get a specific SPECIAL stat with equipment bonuses"""
        base_stat = getattr(self, stat_name.lower(), 5)
        bonus = 0

        # Add outfit bonuses
        if self.outfit and self.outfit in EQUIPMENT_LIBRARY:
            outfit = EQUIPMENT_LIBRARY[self.outfit]
            bonus += outfit.stat_bonus.get(stat_name.lower(), 0)

        return min(10, base_stat + bonus)

    def get_combat_power(self) -> int:
        """Get combat effectiveness"""
        weapon_damage = 0
        if self.weapon and self.weapon in EQUIPMENT_LIBRARY:
            weapon_damage = EQUIPMENT_LIBRARY[self.weapon].damage

        # Base damage from strength + weapon
        return self.get_stat("strength") + weapon_damage

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
    incident_strength: int = 0  # For combat
    rush_cooldown: int = 0  # Turns until can rush again

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

        # Base production multiplied by level
        base_multiplier = self.level

        # Worker bonus: each worker adds 20%
        worker_count = len(self.assigned_dwellers)
        if worker_count > 0:
            # Get average stat of workers for relevant stat
            if config.stat_required:
                total_stat = 0
                for dweller_name in self.assigned_dwellers:
                    dweller = next((d for d in dwellers_list if d.name == dweller_name), None)
                    if dweller:
                        total_stat += dweller.get_stat(config.stat_required)
                avg_stat = total_stat / worker_count if worker_count > 0 else 5
                stat_multiplier = avg_stat / 5  # 5 is average
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


class VaultGame:
    """Main game class for Vault 13"""

    def __init__(self):
        self.day = 1
        self.resources = Resources()
        self.dwellers: List[Dweller] = []
        self.vault_layout: List[List[Room]] = []
        self.event_log: List[str] = []
        self.equipment_inventory: List[str] = []  # Equipment keys
        self.game_over = False
        self.max_floors = 10
        self.floors_unlocked = 3

        # Initialize vault
        self._initialize_vault()
        self._create_starting_dwellers()

        # Starting equipment
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
        """Create initial dwellers"""
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
                happiness=random.randint(60, 80)
            )
            self.dwellers.append(dweller)

        # Assign starting dwellers
        self.dwellers[0].assigned_room = (0, 0)
        self.vault_layout[0][0].assigned_dwellers.append(self.dwellers[0].name)

        self.dwellers[1].assigned_room = (0, 1)
        self.vault_layout[0][1].assigned_dwellers.append(self.dwellers[1].name)

    def clear_screen(self):
        """Clear terminal screen"""
        clear_screen()

    def print_header(self):
        """Print game header"""
        print(f"\n{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║              VAULT 13 - SURVIVAL PROTOCOL v2.0                       ║{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║                         DAY {self.day:4d}                                    ║{C.RESET}")
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

        # Room icons
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

        # Show room level with roman numerals
        level_display = ["", "I", "II", "III"][min(room.level, 3)] if room.room_type != RoomType.EMPTY else ""

        # Worker icons
        worker_count = len(room.assigned_dwellers)
        worker_icons = "👤" * min(worker_count, 3)

        # Status indicators
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
        print(f"  {C.SUCCESS}[S]{C.RESET} Save Game        {C.DANGER}[Q]{C.RESET} Quit Game")
        print()

    def process_turn(self):
        """Process end of turn"""
        self.day += 1

        # Decrease rush cooldowns
        for floor in self.vault_layout:
            for room in floor:
                if room.rush_cooldown > 0:
                    room.rush_cooldown -= 1

        # Resource production
        for floor in self.vault_layout:
            for room in floor:
                if not room.under_construction and not room.on_fire and not room.has_incident:
                    production = room.get_production(self.dwellers)
                    for resource, amount in production.items():
                        self.resources.add(resource, amount)

        # Resource consumption with smart allocation
        dweller_count = len(self.dwellers)
        power_needed = dweller_count * 1
        water_needed = dweller_count * 1
        food_needed = dweller_count * 1

        power_consumed = self.resources.consume_with_rationing("power", power_needed)
        water_consumed = self.resources.consume_with_rationing("water", water_needed)
        food_consumed = self.resources.consume_with_rationing("food", food_needed)

        # Apply penalties for shortfalls
        if power_consumed < power_needed:
            shortage = power_needed - power_consumed
            self._apply_shortage_penalty("power", shortage, dweller_count)

        if water_consumed < water_needed:
            shortage = water_needed - water_consumed
            self._apply_shortage_penalty("water", shortage, dweller_count)

        if food_consumed < food_needed:
            shortage = food_needed - food_consumed
            self._apply_shortage_penalty("food", shortage, dweller_count)

        # Auto-resolve some incidents
        for floor in self.vault_layout:
            for room in floor:
                if room.on_fire or room.has_incident:
                    # 30% chance to auto-resolve each turn
                    if random.random() < 0.3:
                        if room.on_fire:
                            room.on_fire = False
                            self.add_event(f"{C.SUCCESS}Fire in {room.room_type.value} burned out{C.RESET}")
                        if room.has_incident:
                            room.has_incident = False
                            room.incident_strength = 0
                            self.add_event(f"{C.SUCCESS}Incident in {room.room_type.value} resolved{C.RESET}")

        # Random events
        if random.random() < 0.2:
            self._trigger_random_event()

        # Dweller happiness updates
        self._update_dweller_happiness()

        # Check game over
        self._check_game_over()

    def _apply_shortage_penalty(self, resource: str, shortage: int, total_dwellers: int):
        """Apply penalties when resources run short"""
        if shortage == 0:
            return

        # Randomly select dwellers to suffer
        affected_count = min(shortage, total_dwellers)
        affected = random.sample(self.dwellers, affected_count)

        for dweller in affected:
            if resource == "power":
                dweller.modify_happiness(-3)
            elif resource in ["water", "food"]:
                dweller.modify_health(-8)
                dweller.modify_happiness(-5)

        self.add_event(f"{C.DANGER}⚠️ Not enough {resource}! {affected_count} dwellers affected{C.RESET}")

    def _update_dweller_happiness(self):
        """Update dweller happiness"""
        for dweller in self.dwellers:
            happiness_change = 0

            if dweller.assigned_room:
                happiness_change += 2
            else:
                happiness_change -= 3

            if dweller.health < 50:
                happiness_change -= 5

            if dweller.weapon or dweller.outfit:
                happiness_change += 1

            happiness_change += random.randint(-2, 3)
            dweller.modify_happiness(happiness_change)

    def rush_production_menu(self):
        """Rush production in a room"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}RUSH PRODUCTION{C.RESET}\n")
        print("Rush a room to instantly produce resources!")
        print(f"{C.WARNING}Warning: Risk of fire or incident on failure!{C.RESET}\n")

        rushable_rooms = []
        for floor in self.vault_layout:
            for room in floor:
                if room.can_rush():
                    rushable_rooms.append(room)

        if not rushable_rooms:
            print(f"{C.INFO}No rooms available to rush.{C.RESET}\n")
            input("Press Enter to continue...")
            return

        for idx, room in enumerate(rushable_rooms, 1):
            # Calculate success chance based on luck
            workers_luck = 0
            for dweller_name in room.assigned_dwellers:
                dweller = next((d for d in self.dwellers if d.name == dweller_name), None)
                if dweller:
                    workers_luck += dweller.get_stat("luck")
            avg_luck = workers_luck / len(room.assigned_dwellers) if room.assigned_dwellers else 5
            success_chance = min(95, 40 + (avg_luck * 5))

            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} (Floor {room.floor + 1})")
            print(f"      Workers: {len(room.assigned_dwellers)}")
            print(f"      Success Chance: {C.SUCCESS if success_chance >= 70 else C.WARNING}{success_chance}%{C.RESET}")
            print()

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select room to rush: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(rushable_rooms):
                self._execute_rush(rushable_rooms[choice_idx])
        except ValueError:
            print(f"{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def _execute_rush(self, room: Room):
        """Execute a rush attempt"""
        # Calculate success chance
        workers_luck = 0
        for dweller_name in room.assigned_dwellers:
            dweller = next((d for d in self.dwellers if d.name == dweller_name), None)
            if dweller:
                workers_luck += dweller.get_stat("luck")
        avg_luck = workers_luck / len(room.assigned_dwellers) if room.assigned_dwellers else 5
        success_chance = min(95, 40 + (avg_luck * 5))

        # Roll for success
        roll = random.randint(1, 100)

        if roll <= success_chance:
            # SUCCESS!
            production = room.get_production(self.dwellers)
            bonus_multiplier = 2 + (room.level * 0.5)

            for resource, amount in production.items():
                bonus_amount = int(amount * bonus_multiplier)
                self.resources.add(resource, bonus_amount)
                print(f"\n{C.SUCCESS}✨ RUSH SUCCESS! Produced {bonus_amount} {resource}!{C.RESET}")
                self.add_event(f"{C.SUCCESS}Rush succeeded in {room.room_type.value} - produced {bonus_amount} {resource}{C.RESET}")

            # Bonus caps
            caps_bonus = random.randint(20, 50)
            self.resources.caps += caps_bonus

            # Happiness boost
            for dweller_name in room.assigned_dwellers:
                dweller = next((d for d in self.dwellers if d.name == dweller_name), None)
                if dweller:
                    dweller.modify_happiness(10)

            room.rush_cooldown = 3
        else:
            # FAILURE!
            print(f"\n{C.DANGER}💥 RUSH FAILED!{C.RESET}")

            # 50/50 fire or incident
            if random.random() < 0.5:
                room.on_fire = True
                print(f"{C.DANGER}🔥 Fire broke out!{C.RESET}")
                self.add_event(f"{C.DANGER}Rush failed in {room.room_type.value} - fire!{C.RESET}")
            else:
                room.has_incident = True
                room.incident_strength = random.randint(10, 25)
                print(f"{C.WARNING}⚠️ Incident occurred!{C.RESET}")
                self.add_event(f"{C.WARNING}Rush failed in {room.room_type.value} - incident!{C.RESET}")

            # Happiness penalty
            for dweller_name in room.assigned_dwellers:
                dweller = next((d for d in self.dwellers if d.name == dweller_name), None)
                if dweller:
                    dweller.modify_happiness(-15)

            room.rush_cooldown = 5

    def fight_incident_menu(self):
        """Fight fires or incidents"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}FIGHT INCIDENT{C.RESET}\n")

        # Find rooms with incidents
        incident_rooms = []
        for floor in self.vault_layout:
            for room in floor:
                if room.on_fire or room.has_incident:
                    incident_rooms.append(room)

        if not incident_rooms:
            print(f"{C.INFO}No incidents to fight!{C.RESET}\n")
            input("Press Enter to continue...")
            return

        for idx, room in enumerate(incident_rooms, 1):
            incident_type = "🔥 FIRE" if room.on_fire else f"⚠️ INCIDENT (Strength: {room.incident_strength})"
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} (Floor {room.floor + 1}) - {incident_type}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select incident to fight: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(incident_rooms):
                self._select_fighters(incident_rooms[choice_idx])
        except ValueError:
            print(f"{C.DANGER}Invalid choice!{C.RESET}")

    def _select_fighters(self, room: Room):
        """Select dwellers to fight incident"""
        print(f"\n{C.BOLD}Select dwellers to fight (max 3):{C.RESET}\n")

        for idx, dweller in enumerate(self.dwellers, 1):
            combat_power = dweller.get_combat_power()
            weapon_str = f" {EQUIPMENT_LIBRARY[dweller.weapon].icon}" if dweller.weapon else ""
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - Combat: {combat_power}{weapon_str} (HP: {dweller.health}%)")

        print(f"\n{C.INFO}Enter dweller numbers separated by spaces (e.g., '1 3 5'):{C.RESET}")
        choice = input("> ").strip()

        if not choice:
            return

        try:
            indices = [int(x) - 1 for x in choice.split()]
            fighters = [self.dwellers[i] for i in indices if 0 <= i < len(self.dwellers)][:3]

            if fighters:
                self._execute_combat(room, fighters)
        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid selection!{C.RESET}")

        input("\nPress Enter to continue...")

    def _execute_combat(self, room: Room, fighters: List[Dweller]):
        """Execute combat against incident"""
        total_combat = sum(d.get_combat_power() for d in fighters)

        if room.on_fire:
            # Fire requires total combat > 20
            required = 20
            if total_combat >= required:
                room.on_fire = False
                print(f"\n{C.SUCCESS}🎉 Fire extinguished!{C.RESET}")
                self.add_event(f"{C.SUCCESS}Fire in {room.room_type.value} extinguished by {len(fighters)} dwellers{C.RESET}")

                # Small damage to fighters
                for fighter in fighters:
                    damage = random.randint(3, 8)
                    fighter.modify_health(-damage)
            else:
                print(f"\n{C.DANGER}Fire too strong! Need combat power {required}, have {total_combat}{C.RESET}")
                # Damage fighters
                for fighter in fighters:
                    damage = random.randint(10, 20)
                    fighter.modify_health(-damage)

        elif room.has_incident:
            # Incident requires defeating incident_strength
            if total_combat >= room.incident_strength:
                room.has_incident = False
                room.incident_strength = 0
                print(f"\n{C.SUCCESS}🎉 Incident resolved!{C.RESET}")
                self.add_event(f"{C.SUCCESS}Incident in {room.room_type.value} defeated{C.RESET}")

                # Reward caps
                caps_reward = random.randint(30, 60)
                self.resources.caps += caps_reward
                print(f"{C.CAPS}Found {caps_reward} caps!{C.RESET}")

                # Minor damage
                for fighter in fighters:
                    damage = random.randint(2, 5)
                    fighter.modify_health(-damage)
            else:
                print(f"\n{C.WARNING}Incident too strong! Need {room.incident_strength}, have {total_combat}{C.RESET}")
                # Damage based on strength difference
                damage_per_dweller = (room.incident_strength - total_combat) // len(fighters)
                for fighter in fighters:
                    fighter.modify_health(-max(5, damage_per_dweller))

    def upgrade_room_menu(self):
        """Upgrade a room to next level"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}UPGRADE ROOM{C.RESET}\n")

        upgradeable = []
        for floor in self.vault_layout:
            for room in floor:
                if room.room_type != RoomType.EMPTY and room.level < 3:
                    upgradeable.append(room)

        if not upgradeable:
            print(f"{C.INFO}No rooms available to upgrade.{C.RESET}\n")
            input("Press Enter to continue...")
            return

        for idx, room in enumerate(upgradeable, 1):
            cost = room.get_upgrade_cost()
            next_level = room.level + 1
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} Lv.{room.level} → Lv.{next_level}")
            print(f"      Cost: {C.CAPS}{cost} caps{C.RESET}")
            print(f"      Floor {room.floor + 1}, Production x{next_level}")
            print()

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select room to upgrade: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(upgradeable):
                room = upgradeable[choice_idx]
                cost = room.get_upgrade_cost()

                if self.resources.has_enough("caps", cost):
                    self.resources.remove("caps", cost)
                    room.level += 1
                    print(f"\n{C.SUCCESS}Room upgraded to Level {room.level}!{C.RESET}")
                    self.add_event(f"{C.SUCCESS}Upgraded {room.room_type.value} to Lv.{room.level}{C.RESET}")
                else:
                    print(f"\n{C.DANGER}Not enough caps! Need {cost}, have {self.resources.caps}{C.RESET}")
        except ValueError:
            print(f"{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def manage_equipment_menu(self):
        """Manage equipment"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}EQUIPMENT MANAGEMENT{C.RESET}\n")
        print(f"  {C.SUCCESS}[1]{C.RESET} Equip Item to Dweller")
        print(f"  {C.SUCCESS}[2]{C.RESET} Unequip Item")
        print(f"  {C.SUCCESS}[3]{C.RESET} View Inventory")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"{C.BOLD}Select option: {C.RESET}").strip()

        if choice == "1":
            self.equip_item_menu()
        elif choice == "2":
            self.unequip_item_menu()
        elif choice == "3":
            self.view_equipment_inventory()

    def equip_item_menu(self):
        """Equip item to dweller"""
        print(f"\n{C.BOLD}Available Equipment:{C.RESET}\n")

        if not self.equipment_inventory:
            print(f"{C.INFO}No equipment in inventory.{C.RESET}\n")
            input("Press Enter to continue...")
            return

        for idx, eq_key in enumerate(self.equipment_inventory, 1):
            eq = EQUIPMENT_LIBRARY[eq_key]
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {eq.icon} {eq.name} ({eq.equipment_type.value})")
            print(f"      {eq.get_description()}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        eq_choice = input(f"{C.BOLD}Select equipment: {C.RESET}").strip()

        if eq_choice == "0":
            return

        try:
            eq_idx = int(eq_choice) - 1
            if 0 <= eq_idx < len(self.equipment_inventory):
                eq_key = self.equipment_inventory[eq_idx]
                eq = EQUIPMENT_LIBRARY[eq_key]

                print(f"\n{C.BOLD}Select dweller:{C.RESET}\n")
                for idx, dweller in enumerate(self.dwellers, 1):
                    print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name}")

                dweller_choice = input(f"{C.BOLD}> {C.RESET}").strip()
                dweller_idx = int(dweller_choice) - 1

                if 0 <= dweller_idx < len(self.dwellers):
                    dweller = self.dwellers[dweller_idx]

                    if eq.equipment_type == EquipmentType.WEAPON:
                        if dweller.weapon:
                            self.equipment_inventory.append(dweller.weapon)
                        dweller.weapon = eq_key
                    else:
                        if dweller.outfit:
                            self.equipment_inventory.append(dweller.outfit)
                        dweller.outfit = eq_key

                    self.equipment_inventory.remove(eq_key)
                    print(f"\n{C.SUCCESS}Equipped {eq.name} to {dweller.name}!{C.RESET}")
                    self.add_event(f"{dweller.name} equipped {eq.name}")
        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def unequip_item_menu(self):
        """Unequip item from dweller"""
        print(f"\n{C.BOLD}Equipped Items:{C.RESET}\n")

        equipped_dwellers = [(d, "weapon") for d in self.dwellers if d.weapon] + \
                           [(d, "outfit") for d in self.dwellers if d.outfit]

        if not equipped_dwellers:
            print(f"{C.INFO}No items currently equipped.{C.RESET}\n")
            input("Press Enter to continue...")
            return

        for idx, (dweller, slot) in enumerate(equipped_dwellers, 1):
            eq_key = getattr(dweller, slot)
            eq = EQUIPMENT_LIBRARY[eq_key]
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name}: {eq.icon} {eq.name}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select item to unequip: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(equipped_dwellers):
                dweller, slot = equipped_dwellers[choice_idx]
                eq_key = getattr(dweller, slot)
                eq = EQUIPMENT_LIBRARY[eq_key]

                setattr(dweller, slot, None)
                self.equipment_inventory.append(eq_key)
                print(f"\n{C.SUCCESS}Unequipped {eq.name} from {dweller.name}!{C.RESET}")
        except (ValueError, IndexError):
            print(f"{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def view_equipment_inventory(self):
        """View equipment inventory"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}EQUIPMENT INVENTORY{C.RESET}\n")

        if not self.equipment_inventory:
            print(f"{C.INFO}No equipment in inventory.{C.RESET}\n")
        else:
            for eq_key in self.equipment_inventory:
                eq = EQUIPMENT_LIBRARY[eq_key]
                print(f"  {eq.icon} {C.BOLD}{eq.name}{C.RESET} ({eq.equipment_type.value})")
                print(f"     {eq.get_description()}")
                print()

        print(f"{C.BOLD}EQUIPPED ITEMS:{C.RESET}\n")
        for dweller in self.dwellers:
            items = []
            if dweller.weapon:
                items.append(f"{EQUIPMENT_LIBRARY[dweller.weapon].icon} {EQUIPMENT_LIBRARY[dweller.weapon].name}")
            if dweller.outfit:
                items.append(f"{EQUIPMENT_LIBRARY[dweller.outfit].icon} {EQUIPMENT_LIBRARY[dweller.outfit].name}")

            if items:
                print(f"  {dweller.name}: {', '.join(items)}")

        input("\n\nPress Enter to continue...")

    def _trigger_random_event(self):
        """Trigger random events"""
        events = [
            self._event_new_arrival,
            self._event_raider_attack,
            self._event_fire,
            self._event_rad_roach_infestation,
            self._event_resource_find,
            self._event_dweller_skill_up,
            self._event_equipment_find,
        ]
        random.choice(events)()

    def _event_new_arrival(self):
        """New dweller arrives"""
        first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Sam", "Blake"]
        last_names = ["Anderson", "Thomas", "Moore", "Martin", "Jackson", "White", "Harris", "Clark"]

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
        )
        self.dwellers.append(new_dweller)
        self.add_event(f"{C.SUCCESS}👤 {name} joined the vault!{C.RESET}")

    def _event_raider_attack(self):
        """Raiders attack"""
        if self.dwellers:
            victim = random.choice(self.dwellers)
            damage = random.randint(5, 15)
            victim.modify_health(-damage)
            victim.modify_happiness(-10)
            self.add_event(f"{C.DANGER}💀 Raiders! {victim.name} lost {damage} HP{C.RESET}")

    def _event_fire(self):
        """Fire event"""
        occupied = [r for floor in self.vault_layout for r in floor if r.room_type != RoomType.EMPTY]
        if occupied:
            room = random.choice(occupied)
            room.on_fire = True
            self.add_event(f"{C.DANGER}🔥 Fire in {room.room_type.value}!{C.RESET}")

    def _event_rad_roach_infestation(self):
        """Rad roaches"""
        occupied = [r for floor in self.vault_layout for r in floor if r.room_type != RoomType.EMPTY]
        if occupied:
            room = random.choice(occupied)
            room.has_incident = True
            room.incident_strength = random.randint(10, 20)
            self.add_event(f"{C.WARNING}🪳 Rad roaches in {room.room_type.value}!{C.RESET}")

    def _event_resource_find(self):
        """Find resources"""
        resource = random.choice(["power", "water", "food"])
        amount = random.randint(5, 15)
        self.resources.add(resource, amount)
        caps = random.randint(10, 50)
        self.resources.caps += caps
        self.add_event(f"{C.SUCCESS}✨ Found {amount} {resource} and {caps} caps!{C.RESET}")

    def _event_dweller_skill_up(self):
        """Dweller skill improves"""
        if self.dwellers:
            dweller = random.choice(self.dwellers)
            stat = random.choice(["strength", "perception", "endurance", "charisma", "intelligence", "agility", "luck"])
            dweller.modify_stat(stat, 1)
            dweller.modify_happiness(5)
            self.add_event(f"{C.SUCCESS}📈 {dweller.name} +1 {stat}!{C.RESET}")

    def _event_equipment_find(self):
        """Find equipment"""
        available = ["rusty_pistol", "laser_rifle", "vault_suit", "scientist_coat"]
        found = random.choice(available)
        self.equipment_inventory.append(found)
        eq = EQUIPMENT_LIBRARY[found]
        self.add_event(f"{C.SUCCESS}🎁 Found {eq.icon} {eq.name}!{C.RESET}")

    def _check_game_over(self):
        """Check game over"""
        alive = [d for d in self.dwellers if d.health > 0]
        if not alive:
            self.game_over = True
            self.add_event(f"{C.DANGER}💀 All dwellers dead. GAME OVER.{C.RESET}")
            return

        if self.resources.power == 0 and self.resources.water == 0:
            self.game_over = True
            self.add_event(f"{C.DANGER}⚠️ Vault systems failed. GAME OVER.{C.RESET}")
            return

    def add_event(self, event: str):
        """Add event to log"""
        self.event_log.append(event)

    # (Keeping existing methods: build_room_menu, assign_workers_menu, etc.)
    # For brevity, I'll include the modified game_loop and key methods

    def build_room_menu(self):
        """Show build room menu"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}BUILD ROOM{C.RESET}\n")
        print("Available room types:\n")

        room_types = [
            (RoomType.POWER_GENERATOR, "⚡"),
            (RoomType.WATER_TREATMENT, "💧"),
            (RoomType.DINER, "🍖"),
            (RoomType.LIVING_QUARTERS, "🏠"),
            (RoomType.STORAGE_ROOM, "📦"),
            (RoomType.TRAINING_ROOM, "💪"),
            (RoomType.MEDBAY, "⚕️"),
            (RoomType.SCIENCE_LAB, "🔬"),
        ]

        for idx, (room_type, icon) in enumerate(room_types, 1):
            config = ROOM_CONFIGS[room_type]
            production_str = ", ".join([f"+{v} {k}" for k, v in config.production.items()]) if config.production else "No production"

            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {icon} {C.BOLD}{room_type.value}{C.RESET}")
            print(f"      Cost: {C.CAPS}{config.cost} caps{C.RESET}")
            print(f"      {config.description}")
            print(f"      {production_str}, Capacity: {config.capacity} dwellers")
            print()

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select room type to build: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(room_types):
                room_type = room_types[choice_idx][0]
                self.select_room_location(room_type)
        except ValueError:
            print(f"{C.DANGER}Invalid choice!{C.RESET}")
            time.sleep(1)

    def select_room_location(self, room_type: RoomType):
        """Select location to build room"""
        config = ROOM_CONFIGS[room_type]

        if not self.resources.has_enough("caps", config.cost):
            print(f"\n{C.DANGER}Not enough caps! Need {config.cost}, have {self.resources.caps}{C.RESET}")
            input("\nPress Enter to continue...")
            return

        print(f"\n{C.BOLD}Select location (floor,position format: e.g., 1,2):{C.RESET}")
        print("Current vault layout:\n")

        for floor_idx, floor in enumerate(self.vault_layout):
            print(f"Floor {floor_idx + 1}: ", end="")
            for pos_idx, room in enumerate(floor):
                if room.room_type == RoomType.EMPTY:
                    print(f"{C.SUCCESS}[{floor_idx + 1},{pos_idx + 1} Available]{C.RESET} ", end="")
                else:
                    print(f"[{floor_idx + 1},{pos_idx + 1} Occupied] ", end="")
            print()

        location = input(f"\n{C.BOLD}Enter location (or 0 to cancel): {C.RESET}").strip()

        if location == "0":
            return

        try:
            floor_str, pos_str = location.split(",")
            floor = int(floor_str) - 1
            position = int(pos_str) - 1

            if 0 <= floor < len(self.vault_layout) and 0 <= position < len(self.vault_layout[floor]):
                room = self.vault_layout[floor][position]

                if room.room_type == RoomType.EMPTY:
                    self.resources.remove("caps", config.cost)
                    room.room_type = room_type
                    room.under_construction = False

                    self.add_event(f"{C.SUCCESS}Built {room_type.value} on Floor {floor + 1}{C.RESET}")
                    print(f"\n{C.SUCCESS}Room built successfully!{C.RESET}")

                    if room_type == RoomType.STORAGE_ROOM:
                        self.resources.power_max += 20
                        self.resources.water_max += 20
                        self.resources.food_max += 20
                else:
                    print(f"\n{C.DANGER}That location is already occupied!{C.RESET}")
            else:
                print(f"\n{C.DANGER}Invalid location!{C.RESET}")
        except (ValueError, IndexError):
            print(f"\n{C.DANGER}Invalid input format! Use: floor,position{C.RESET}")

        input("\nPress Enter to continue...")

    def assign_workers_menu(self):
        """Assign dwellers to rooms"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}ASSIGN WORKERS{C.RESET}\n")

        unassigned = [d for d in self.dwellers if d.assigned_room is None]

        if not unassigned:
            print(f"{C.INFO}All dwellers are currently assigned to rooms.{C.RESET}\n")
            input("Press Enter to continue...")
            return

        print(f"{C.BOLD}Unassigned Dwellers:{C.RESET}\n")
        for idx, dweller in enumerate(unassigned, 1):
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name}")
            print(f"      S:{dweller.get_stat('strength')} P:{dweller.get_stat('perception')} E:{dweller.get_stat('endurance')} " +
                  f"C:{dweller.get_stat('charisma')} I:{dweller.get_stat('intelligence')} A:{dweller.get_stat('agility')} L:{dweller.get_stat('luck')}")
            print(f"      Health: {dweller.health}% Happiness: {dweller.happiness}%")
            if dweller.weapon or dweller.outfit:
                items = []
                if dweller.weapon:
                    items.append(EQUIPMENT_LIBRARY[dweller.weapon].icon)
                if dweller.outfit:
                    items.append(EQUIPMENT_LIBRARY[dweller.outfit].icon)
                print(f"      Equipment: {' '.join(items)}")
            print()

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select dweller to assign: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(unassigned):
                dweller = unassigned[choice_idx]
                self.select_room_for_dweller(dweller)
        except ValueError:
            print(f"{C.DANGER}Invalid choice!{C.RESET}")
            time.sleep(1)

    def select_room_for_dweller(self, dweller: Dweller):
        """Select room to assign dweller to"""
        print(f"\n{C.BOLD}Available rooms for {dweller.name}:{C.RESET}\n")

        available_rooms = []
        for floor in self.vault_layout:
            for room in floor:
                if room.can_assign_dweller():
                    available_rooms.append(room)

        if not available_rooms:
            print(f"{C.DANGER}No rooms available for assignment!{C.RESET}")
            input("\nPress Enter to continue...")
            return

        for idx, room in enumerate(available_rooms, 1):
            config = ROOM_CONFIGS[room.room_type]
            workers = f"{len(room.assigned_dwellers)}/{config.capacity}"
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} Lv.{room.level} (Floor {room.floor + 1}, Pos {room.position + 1}) - Workers: {workers}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select room: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_rooms):
                room = available_rooms[choice_idx]

                dweller.assigned_room = (room.floor, room.position)
                room.assigned_dwellers.append(dweller.name)

                self.add_event(f"{dweller.name} assigned to {room.room_type.value}")
                print(f"\n{C.SUCCESS}Dweller assigned successfully!{C.RESET}")
        except ValueError:
            print(f"{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def view_details_menu(self):
        """View detailed information"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}VIEW DETAILS{C.RESET}\n")
        print(f"  {C.SUCCESS}[1]{C.RESET} View All Dwellers")
        print(f"  {C.SUCCESS}[2]{C.RESET} View All Rooms")
        print(f"  {C.SUCCESS}[3]{C.RESET} View Event History")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"{C.BOLD}Select option: {C.RESET}").strip()

        if choice == "1":
            self.view_all_dwellers()
        elif choice == "2":
            self.view_all_rooms()
        elif choice == "3":
            self.view_event_history()

    def view_all_dwellers(self):
        """View all dwellers with details"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}ALL DWELLERS ({len(self.dwellers)}){C.RESET}\n")

        for dweller in self.dwellers:
            status_color = C.SUCCESS if dweller.health > 70 else C.WARNING if dweller.health > 30 else C.DANGER
            happiness_color = C.HAPPY if dweller.happiness > 60 else C.NEUTRAL if dweller.happiness > 30 else C.SAD

            print(f"{C.BOLD}{dweller.name}{C.RESET}")
            print(f"  Health: {status_color}{dweller.health}%{C.RESET}  Happiness: {happiness_color}{dweller.happiness}%{C.RESET}")
            print(f"  SPECIAL: S:{dweller.get_stat('strength')} P:{dweller.get_stat('perception')} E:{dweller.get_stat('endurance')} " +
                  f"C:{dweller.get_stat('charisma')} I:{dweller.get_stat('intelligence')} A:{dweller.get_stat('agility')} L:{dweller.get_stat('luck')}")

            if dweller.weapon:
                weapon = EQUIPMENT_LIBRARY[dweller.weapon]
                print(f"  Weapon: {weapon.icon} {weapon.name} (Dmg: {weapon.damage})")
            if dweller.outfit:
                outfit = EQUIPMENT_LIBRARY[dweller.outfit]
                print(f"  Outfit: {outfit.icon} {outfit.name}")

            if dweller.assigned_room:
                floor, pos = dweller.assigned_room
                room = self.vault_layout[floor][pos]
                print(f"  Assigned: {room.room_type.value} Lv.{room.level} (Floor {floor + 1})")
            else:
                print(f"  {C.WARNING}Not assigned to any room{C.RESET}")
            print()

        input("Press Enter to continue...")

    def view_all_rooms(self):
        """View all rooms with details"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}ALL ROOMS{C.RESET}\n")

        for floor_idx, floor in enumerate(self.vault_layout):
            print(f"{C.BOLD}Floor {floor_idx + 1}:{C.RESET}")
            for room in floor:
                if room.room_type == RoomType.EMPTY:
                    print(f"  {C.ROOM_EMPTY}[Empty Slot]{C.RESET}")
                else:
                    production = room.get_production(self.dwellers)
                    prod_str = ", ".join([f"+{v} {k}" for k, v in production.items()]) if production else "No production"
                    workers = len(room.assigned_dwellers)

                    print(f"  {C.BOLD}{room.room_type.value} Lv.{room.level}{C.RESET} - {prod_str}")
                    print(f"    Workers: {workers}")

                    if room.assigned_dwellers:
                        print(f"    Assigned: {', '.join(room.assigned_dwellers)}")

                    if room.can_rush():
                        print(f"    {C.SUCCESS}✓ Can Rush{C.RESET}")
                    elif room.rush_cooldown > 0:
                        print(f"    {C.WARNING}Rush cooldown: {room.rush_cooldown} turns{C.RESET}")

                    if room.on_fire:
                        print(f"    {C.DANGER}🔥 ON FIRE!{C.RESET}")
                    if room.has_incident:
                        print(f"    {C.WARNING}⚠️ INCIDENT (Strength: {room.incident_strength}){C.RESET}")
            print()

        input("Press Enter to continue...")

    def view_event_history(self):
        """View full event history"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}EVENT HISTORY{C.RESET}\n")

        if not self.event_log:
            print(f"{C.INFO}No events yet.{C.RESET}\n")
        else:
            for event in self.event_log[-20:]:
                print(f"  • {event}")

        print()
        input("Press Enter to continue...")

    def manage_dwellers_menu(self):
        """Manage dweller actions"""
        self.clear_screen()
        self.print_header()

        print(f"{C.BOLD}MANAGE DWELLERS{C.RESET}\n")
        print(f"  {C.SUCCESS}[1]{C.RESET} Unassign Dweller from Room")
        print(f"  {C.SUCCESS}[2]{C.RESET} Heal Dweller (costs 50 caps)")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"{C.BOLD}Select option: {C.RESET}").strip()

        if choice == "1":
            self.unassign_dweller()
        elif choice == "2":
            self.heal_dweller()

    def unassign_dweller(self):
        """Unassign a dweller from their room"""
        assigned = [d for d in self.dwellers if d.assigned_room is not None]

        if not assigned:
            print(f"\n{C.INFO}No dwellers are currently assigned.{C.RESET}")
            input("\nPress Enter to continue...")
            return

        print(f"\n{C.BOLD}Assigned Dwellers:{C.RESET}\n")
        for idx, dweller in enumerate(assigned, 1):
            floor, pos = dweller.assigned_room
            room = self.vault_layout[floor][pos]
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - {room.room_type.value} Lv.{room.level} (Floor {floor + 1})")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select dweller to unassign: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(assigned):
                dweller = assigned[choice_idx]
                floor, pos = dweller.assigned_room
                room = self.vault_layout[floor][pos]

                room.assigned_dwellers.remove(dweller.name)
                dweller.assigned_room = None

                self.add_event(f"{dweller.name} unassigned from {room.room_type.value}")
                print(f"\n{C.SUCCESS}Dweller unassigned!{C.RESET}")
        except (ValueError, IndexError):
            print(f"\n{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def heal_dweller(self):
        """Heal an injured dweller"""
        injured = [d for d in self.dwellers if d.health < 100]

        if not injured:
            print(f"\n{C.INFO}All dwellers are at full health!{C.RESET}")
            input("\nPress Enter to continue...")
            return

        heal_cost = 50
        if not self.resources.has_enough("caps", heal_cost):
            print(f"\n{C.DANGER}Not enough caps! Need {heal_cost}, have {self.resources.caps}{C.RESET}")
            input("\nPress Enter to continue...")
            return

        print(f"\n{C.BOLD}Injured Dwellers:{C.RESET}\n")
        for idx, dweller in enumerate(injured, 1):
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - Health: {dweller.health}%")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")
        print(f"Healing cost: {C.CAPS}{heal_cost} caps{C.RESET}\n")

        choice = input(f"{C.BOLD}Select dweller to heal: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(injured):
                dweller = injured[choice_idx]

                self.resources.remove("caps", heal_cost)
                dweller.modify_health(50)
                dweller.modify_happiness(10)

                self.add_event(f"{dweller.name} was healed")
                print(f"\n{C.SUCCESS}{dweller.name} healed to {dweller.health}% health!{C.RESET}")
        except ValueError:
            print(f"\n{C.DANGER}Invalid choice!{C.RESET}")

        input("\nPress Enter to continue...")

    def save_game(self):
        """Save game state to file"""
        save_data = {
            "day": self.day,
            "resources": asdict(self.resources),
            "dwellers": [asdict(d) for d in self.dwellers],
            "vault_layout": [[asdict(r) for r in floor] for floor in self.vault_layout],
            "equipment_inventory": self.equipment_inventory,
            "event_log": self.event_log[-50:],
        }

        try:
            with open("vault_save.json", "w") as f:
                json.dump(save_data, f, indent=2, default=str)

            print(f"\n{C.SUCCESS}Game saved successfully!{C.RESET}")
            self.add_event("Game saved")
        except (IOError, OSError) as e:
            print(f"\n{C.DANGER}Failed to save game: {e}{C.RESET}")

        input("\nPress Enter to continue...")

    def load_game(self):
        """Load game state from file"""
        try:
            with open("vault_save.json", "r") as f:
                save_data = json.load(f)

            self.day = save_data["day"]
            self.resources = Resources(**save_data["resources"])

            self.dwellers = []
            for d_data in save_data["dwellers"]:
                dweller = Dweller(**d_data)
                self.dwellers.append(dweller)

            self.vault_layout = []
            for floor_data in save_data["vault_layout"]:
                floor = []
                for r_data in floor_data:
                    r_data["room_type"] = RoomType(r_data["room_type"])
                    room = Room(**r_data)
                    floor.append(room)
                self.vault_layout.append(floor)

            self.equipment_inventory = save_data.get("equipment_inventory", [])
            self.event_log = save_data.get("event_log", [])

            print(f"\n{C.SUCCESS}Game loaded successfully!{C.RESET}")
            input("\nPress Enter to continue...")
            return True
        except FileNotFoundError:
            return False
        except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
            print(f"\n{C.DANGER}Failed to load game: {e}{C.RESET}")
            input("\nPress Enter to continue...")
            return False

    def show_intro(self):
        """Show game introduction"""
        self.clear_screen()

        intro_text = f"""
{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              VAULT 13 - SURVIVAL PROTOCOL v2.0                       ║
║                                                                      ║
║            Welcome to the Post-Nuclear Age, Overseer!                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}

{C.INFO}After the Great War, you've been selected as Overseer of Vault 13,
one of the last bastions of humanity.{C.RESET}

{C.BOLD}NEW FEATURES in v2.0:{C.RESET}
  • {C.SUCCESS}Rush Production{C.RESET} - Risk/reward instant resources
  • {C.SUCCESS}Room Upgrades{C.RESET} - Level 1 → 2 → 3 for better output
  • {C.SUCCESS}Active Combat{C.RESET} - Fight fires & incidents manually
  • {C.SUCCESS}Equipment System{C.RESET} - Equip weapons & outfits
  • {C.SUCCESS}Smart Rationing{C.RESET} - Fair resource distribution

{C.BOLD}Resources:{C.RESET}
  • {C.POWER}⚡ Power{C.RESET} - Vault systems  • {C.WATER}💧 Water{C.RESET} - Survival
  • {C.FOOD}🍖 Food{C.RESET} - Sustenance      • {C.CAPS}💰 Caps{C.RESET} - Currency

{C.SUCCESS}Good luck, Overseer! The future of humanity rests in your hands!{C.RESET}
"""
        print(intro_text)
        input(f"\n{C.BOLD}Press Enter to begin...{C.RESET}")

        # Check for saved game
        self.clear_screen()
        print(f"\n{C.BOLD}Checking for saved game...{C.RESET}\n")

        if os.path.exists("vault_save.json"):
            choice = input(f"{C.SUCCESS}Saved game found! Load it? (y/n): {C.RESET}").strip().lower()
            if choice == 'y':
                self.load_game()

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
            elif choice == 's':
                self.save_game()
            elif choice == 'q':
                confirm = input(f"\n{C.WARNING}Are you sure you want to quit? (y/n): {C.RESET}").strip().lower()
                if confirm == 'y':
                    break

        if self.game_over:
            self.show_game_over()

    def show_game_over(self):
        """Show game over screen"""
        self.clear_screen()

        print(f"""
{C.DANGER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                          GAME OVER                                   ║
║                                                                      ║
║                    Vault 13 Has Fallen                               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}

{C.BOLD}Final Statistics:{C.RESET}
  Days Survived: {C.INFO}{self.day}{C.RESET}
  Final Population: {C.INFO}{len(self.dwellers)}{C.RESET}
  Caps Remaining: {C.CAPS}{self.resources.caps}{C.RESET}

{C.DIM}The wasteland claims another vault...{C.RESET}
""")
        input(f"\n{C.BOLD}Press Enter to exit...{C.RESET}")


def main():
    """Main entry point"""
    game = VaultGame()
    game.show_intro()
    game.game_loop()


if __name__ == '__main__':
    main()
