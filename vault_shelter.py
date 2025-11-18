#!/usr/bin/env python3
"""
VAULT 13 - SURVIVAL PROTOCOL
A vault management simulation inspired by Fallout Shelter

Manage your underground vault, allocate resources, assign dwellers to rooms,
and survive against random events. Build, expand, and keep your dwellers happy!
"""

import random
import time
import os
import sys
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum


class C:
    """ANSI Color codes for terminal styling"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # UI Colors
    HEADER = '\033[38;5;51m'      # Cyan
    BORDER = '\033[38;5;39m'      # Blue
    SUCCESS = '\033[38;5;46m'     # Green
    WARNING = '\033[38;5;226m'    # Yellow
    DANGER = '\033[38;5;196m'     # Red
    INFO = '\033[38;5;159m'       # Light cyan

    # Resource Colors
    POWER = '\033[38;5;226m'      # Yellow (electricity)
    WATER = '\033[38;5;51m'       # Cyan (water)
    FOOD = '\033[38;5;208m'       # Orange (food)
    CAPS = '\033[38;5;226m'       # Yellow (money)

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


@dataclass
class RoomStats:
    """Stats for different room types"""
    cost: int
    production: Dict[str, int]
    capacity: int
    stat_required: Optional[str] = None
    description: str = ""


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
    assigned_room: Optional[Tuple[int, int]] = None  # (floor, position)

    def get_stat(self, stat_name: str) -> int:
        """Get a specific SPECIAL stat"""
        return getattr(self, stat_name.lower(), 5)

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

    def get_production(self) -> Dict[str, int]:
        """Calculate room production based on assigned dwellers and level"""
        if self.room_type == RoomType.EMPTY or self.under_construction:
            return {}

        config = ROOM_CONFIGS.get(self.room_type)
        if not config:
            return {}

        # Base production
        production = config.production.copy()

        # Bonus from dwellers and level
        worker_count = len(self.assigned_dwellers)
        if worker_count > 0:
            for resource in production:
                production[resource] = int(production[resource] * (1 + worker_count * 0.2) * self.level)

        return production

    def can_assign_dweller(self) -> bool:
        """Check if more dwellers can be assigned to this room"""
        if self.room_type == RoomType.EMPTY or self.under_construction:
            return False
        config = ROOM_CONFIGS.get(self.room_type)
        return len(self.assigned_dwellers) < config.capacity if config else False


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


@dataclass
class GameEvent:
    """Random event that can occur in the vault"""
    title: str
    description: str
    effect: str
    severity: str  # "info", "warning", "danger"


class VaultGame:
    """Main game class for Vault 13"""

    def __init__(self):
        self.day = 1
        self.resources = Resources()
        self.dwellers: List[Dweller] = []
        self.vault_layout: List[List[Room]] = []
        self.event_log: List[str] = []
        self.game_over = False
        self.max_floors = 10
        self.floors_unlocked = 3

        # Initialize vault
        self._initialize_vault()
        self._create_starting_dwellers()

    def _initialize_vault(self):
        """Create initial vault layout"""
        # Start with 3 floors, 3 rooms each
        for floor in range(3):
            floor_rooms = []
            for pos in range(3):
                if floor == 0 and pos == 0:
                    # Starting power room
                    room = Room(RoomType.POWER_GENERATOR, floor, pos)
                elif floor == 0 and pos == 1:
                    # Starting water room
                    room = Room(RoomType.WATER_TREATMENT, floor, pos)
                elif floor == 1 and pos == 0:
                    # Starting living quarters
                    room = Room(RoomType.LIVING_QUARTERS, floor, pos)
                else:
                    # Empty rooms
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

        # Assign starting dwellers to rooms
        self.dwellers[0].assigned_room = (0, 0)  # Power
        self.vault_layout[0][0].assigned_dwellers.append(self.dwellers[0].name)

        self.dwellers[1].assigned_room = (0, 1)  # Water
        self.vault_layout[0][1].assigned_dwellers.append(self.dwellers[1].name)

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Print game header"""
        print(f"\n{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.HEADER}{C.BOLD}║                  VAULT 13 - SURVIVAL PROTOCOL                        ║{C.RESET}")
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
        """Print vault room layout"""
        print(f"{C.BOLD}Vault Layout:{C.RESET}")
        print(f"{C.BORDER}{'─' * 70}{C.RESET}")

        for floor_idx, floor in enumerate(self.vault_layout):
            floor_str = f"{C.DIM}Floor {floor_idx + 1}:{C.RESET} "
            for room in floor:
                room_str = self._get_room_display(room)
                floor_str += f"{room_str}  "
            print(floor_str)

        print(f"{C.BORDER}{'─' * 70}{C.RESET}\n")

    def _get_room_display(self, room: Room) -> str:
        """Get colored room display string"""
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
        room_name = room.room_type.value

        # Truncate room name if too long
        if len(room_name) > 15:
            room_name = room_name[:12] + "..."

        # Add worker count
        worker_display = f"({len(room.assigned_dwellers)})" if room.assigned_dwellers else ""

        # Add status indicators
        status = ""
        if room.under_construction:
            status = "🔨"
        elif room.on_fire:
            status = "🔥"
        elif room.has_incident:
            status = "⚠️ "

        return f"{color}[{room_name:15s}]{worker_display}{status}{C.RESET}"

    def print_event_log(self):
        """Print recent events"""
        if not self.event_log:
            return

        print(f"{C.BOLD}Recent Events:{C.RESET}")
        for event in self.event_log[-5:]:  # Show last 5 events
            print(f"  {C.DIM}•{C.RESET} {event}")
        print()

    def print_menu(self):
        """Print action menu"""
        print(f"{C.BOLD}Actions:{C.RESET}")
        print(f"  {C.SUCCESS}[B]{C.RESET} Build Room      {C.SUCCESS}[D]{C.RESET} Manage Dwellers")
        print(f"  {C.SUCCESS}[R]{C.RESET} Assign Workers  {C.SUCCESS}[E]{C.RESET} End Turn")
        print(f"  {C.SUCCESS}[V]{C.RESET} View Details    {C.SUCCESS}[S]{C.RESET} Save Game")
        print(f"  {C.DANGER}[Q]{C.RESET} Quit Game")
        print()

    def process_turn(self):
        """Process end of turn - production, consumption, events"""
        self.day += 1

        # Resource production
        for floor in self.vault_layout:
            for room in floor:
                if not room.under_construction and not room.has_incident:
                    production = room.get_production()
                    for resource, amount in production.items():
                        self.resources.add(resource, amount)
                        if amount > 0:
                            self.add_event(f"{room.room_type.value} produced {amount} {resource}")

        # Resource consumption
        dweller_count = len(self.dwellers)
        power_consumption = dweller_count * 1
        water_consumption = dweller_count * 1
        food_consumption = dweller_count * 1

        self.resources.remove("power", power_consumption)
        self.resources.remove("water", water_consumption)
        self.resources.remove("food", food_consumption)

        # Check critical resources
        if self.resources.is_critical("power"):
            self.add_event(f"{C.WARNING}⚠️  Power running critically low!{C.RESET}")
            self._apply_resource_penalty("power")

        if self.resources.is_critical("water"):
            self.add_event(f"{C.WARNING}⚠️  Water running critically low!{C.RESET}")
            self._apply_resource_penalty("water")

        if self.resources.is_critical("food"):
            self.add_event(f"{C.WARNING}⚠️  Food running critically low!{C.RESET}")
            self._apply_resource_penalty("food")

        # Random events (20% chance per turn)
        if random.random() < 0.2:
            self._trigger_random_event()

        # Dweller happiness updates
        self._update_dweller_happiness()

        # Check game over conditions
        self._check_game_over()

    def _apply_resource_penalty(self, resource: str):
        """Apply penalties for critical resource levels"""
        for dweller in self.dwellers:
            dweller.modify_happiness(-5)
            if resource in ["food", "water"]:
                dweller.modify_health(-10)

    def _update_dweller_happiness(self):
        """Update dweller happiness based on conditions"""
        avg_happiness = sum(d.happiness for d in self.dwellers) // len(self.dwellers) if self.dwellers else 50

        for dweller in self.dwellers:
            # Base happiness change
            happiness_change = 0

            # Assigned to work
            if dweller.assigned_room:
                happiness_change += 2
            else:
                happiness_change -= 3

            # Health affects happiness
            if dweller.health < 50:
                happiness_change -= 5

            # Random variation
            happiness_change += random.randint(-2, 3)

            dweller.modify_happiness(happiness_change)

    def _trigger_random_event(self):
        """Trigger a random event"""
        events = [
            self._event_new_arrival,
            self._event_raider_attack,
            self._event_fire,
            self._event_rad_roach_infestation,
            self._event_resource_find,
            self._event_dweller_skill_up,
        ]

        event = random.choice(events)
        event()

    def _event_new_arrival(self):
        """New dweller arrives at vault"""
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
        self.add_event(f"{C.SUCCESS}👤 New arrival: {name} joined the vault!{C.RESET}")

    def _event_raider_attack(self):
        """Raiders attack the vault"""
        damage = random.randint(5, 15)
        if self.dwellers:
            victim = random.choice(self.dwellers)
            victim.modify_health(-damage)
            victim.modify_happiness(-10)
            self.add_event(f"{C.DANGER}💀 Raider attack! {victim.name} lost {damage} health!{C.RESET}")

    def _event_fire(self):
        """Fire breaks out in a room"""
        # Find occupied rooms
        occupied_rooms = []
        for floor in self.vault_layout:
            for room in floor:
                if room.room_type != RoomType.EMPTY and not room.under_construction:
                    occupied_rooms.append(room)

        if occupied_rooms:
            room = random.choice(occupied_rooms)
            room.on_fire = True
            self.add_event(f"{C.DANGER}🔥 Fire in {room.room_type.value} on Floor {room.floor + 1}!{C.RESET}")

    def _event_rad_roach_infestation(self):
        """Rad roaches infest a room"""
        occupied_rooms = []
        for floor in self.vault_layout:
            for room in floor:
                if room.room_type != RoomType.EMPTY and not room.under_construction:
                    occupied_rooms.append(room)

        if occupied_rooms:
            room = random.choice(occupied_rooms)
            room.has_incident = True
            self.add_event(f"{C.WARNING}🪳 Rad roach infestation in {room.room_type.value}!{C.RESET}")

    def _event_resource_find(self):
        """Dwellers find extra resources"""
        resources = ["power", "water", "food"]
        resource = random.choice(resources)
        amount = random.randint(5, 15)
        self.resources.add(resource, amount)

        caps_found = random.randint(10, 50)
        self.resources.caps += caps_found

        self.add_event(f"{C.SUCCESS}✨ Found {amount} {resource} and {caps_found} caps!{C.RESET}")

    def _event_dweller_skill_up(self):
        """Random dweller improves a skill"""
        if self.dwellers:
            dweller = random.choice(self.dwellers)
            stats = ["strength", "perception", "endurance", "charisma", "intelligence", "agility", "luck"]
            stat = random.choice(stats)
            dweller.modify_stat(stat, 1)
            dweller.modify_happiness(5)
            self.add_event(f"{C.SUCCESS}📈 {dweller.name} improved their {stat}!{C.RESET}")

    def _check_game_over(self):
        """Check if game over conditions are met"""
        # All dwellers dead
        alive_dwellers = [d for d in self.dwellers if d.health > 0]
        if not alive_dwellers:
            self.game_over = True
            self.add_event(f"{C.DANGER}💀 All dwellers have perished. GAME OVER.{C.RESET}")
            return

        # Critical resources at 0 for too long
        if self.resources.power == 0 and self.resources.water == 0:
            self.game_over = True
            self.add_event(f"{C.DANGER}⚠️  Vault systems failed. GAME OVER.{C.RESET}")
            return

    def add_event(self, event: str):
        """Add event to log"""
        self.event_log.append(event)

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
            (RoomType.MEDBAY, "⚕️ "),
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
                    # Build the room
                    self.resources.remove("caps", config.cost)
                    room.room_type = room_type
                    room.under_construction = False  # Instant build for now

                    self.add_event(f"{C.SUCCESS}Built {room_type.value} on Floor {floor + 1}{C.RESET}")
                    print(f"\n{C.SUCCESS}Room built successfully!{C.RESET}")

                    # Update storage capacity
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

        # Show unassigned dwellers
        unassigned = [d for d in self.dwellers if d.assigned_room is None]

        if not unassigned:
            print(f"{C.INFO}All dwellers are currently assigned to rooms.{C.RESET}\n")
            input("Press Enter to continue...")
            return

        print(f"{C.BOLD}Unassigned Dwellers:{C.RESET}\n")
        for idx, dweller in enumerate(unassigned, 1):
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name}")
            print(f"      S:{dweller.strength} P:{dweller.perception} E:{dweller.endurance} " +
                  f"C:{dweller.charisma} I:{dweller.intelligence} A:{dweller.agility} L:{dweller.luck}")
            print(f"      Health: {dweller.health}% Happiness: {dweller.happiness}%")
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
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {room.room_type.value} (Floor {room.floor + 1}, Pos {room.position + 1}) - Workers: {workers}")

        print(f"  {C.DANGER}[0]{C.RESET} Cancel\n")

        choice = input(f"{C.BOLD}Select room: {C.RESET}").strip()

        if choice == "0":
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_rooms):
                room = available_rooms[choice_idx]

                # Assign dweller
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
            print(f"  SPECIAL: S:{dweller.strength} P:{dweller.perception} E:{dweller.endurance} " +
                  f"C:{dweller.charisma} I:{dweller.intelligence} A:{dweller.agility} L:{dweller.luck}")

            if dweller.assigned_room:
                floor, pos = dweller.assigned_room
                room = self.vault_layout[floor][pos]
                print(f"  Assigned: {room.room_type.value} (Floor {floor + 1})")
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
                    production = room.get_production()
                    prod_str = ", ".join([f"+{v} {k}" for k, v in production.items()]) if production else "No production"
                    workers = len(room.assigned_dwellers)

                    print(f"  {C.BOLD}{room.room_type.value}{C.RESET} - {prod_str}")
                    print(f"    Workers: {workers} - Level: {room.level}")

                    if room.assigned_dwellers:
                        print(f"    Assigned: {', '.join(room.assigned_dwellers)}")

                    if room.on_fire:
                        print(f"    {C.DANGER}🔥 ON FIRE!{C.RESET}")
                    if room.has_incident:
                        print(f"    {C.WARNING}⚠️  INCIDENT IN PROGRESS{C.RESET}")
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
            for event in self.event_log[-20:]:  # Show last 20 events
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
        print(f"  {C.SUCCESS}[3]{C.RESET} Train Dweller (if training room available)")
        print(f"  {C.DANGER}[0]{C.RESET} Back\n")

        choice = input(f"{C.BOLD}Select option: {C.RESET}").strip()

        if choice == "1":
            self.unassign_dweller()
        elif choice == "2":
            self.heal_dweller()
        elif choice == "3":
            print(f"{C.INFO}Training feature coming soon!{C.RESET}")
            input("\nPress Enter to continue...")

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
            print(f"  {C.SUCCESS}[{idx}]{C.RESET} {dweller.name} - {room.room_type.value} (Floor {floor + 1})")

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

                # Unassign
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

                # Heal
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
            "event_log": self.event_log[-50:],  # Save last 50 events
        }

        try:
            with open("vault_save.json", "w") as f:
                json.dump(save_data, f, indent=2, default=str)

            print(f"\n{C.SUCCESS}Game saved successfully!{C.RESET}")
            self.add_event("Game saved")
        except Exception as e:
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
                    # Convert room_type string back to enum
                    r_data["room_type"] = RoomType(r_data["room_type"])
                    room = Room(**r_data)
                    floor.append(room)
                self.vault_layout.append(floor)

            self.event_log = save_data.get("event_log", [])

            print(f"\n{C.SUCCESS}Game loaded successfully!{C.RESET}")
            input("\nPress Enter to continue...")
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"\n{C.DANGER}Failed to load game: {e}{C.RESET}")
            input("\nPress Enter to continue...")
            return False

    def show_intro(self):
        """Show game introduction"""
        self.clear_screen()

        intro_text = f"""
{C.HEADER}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                  VAULT 13 - SURVIVAL PROTOCOL                        ║
║                                                                      ║
║            Welcome to the Post-Nuclear Age, Overseer!                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}

{C.INFO}After the Great War, you've been selected as Overseer of Vault 13,
one of the last bastions of humanity.{C.RESET}

{C.BOLD}Your mission:{C.RESET}
  • Manage vault resources (Power, Water, Food)
  • Assign dwellers to production rooms
  • Build and expand your underground shelter
  • Respond to random events and crises
  • Keep your dwellers happy and healthy
  • Ensure the survival of humanity!

{C.BOLD}Game Mechanics:{C.RESET}
  • {C.POWER}⚡ Power{C.RESET} - Keeps vault systems running
  • {C.WATER}💧 Water{C.RESET} - Essential for dweller survival
  • {C.FOOD}🍖 Food{C.RESET} - Keeps dwellers fed and happy
  • {C.CAPS}💰 Caps{C.RESET} - Currency for building and healing

{C.WARNING}Warning:{C.RESET} Let any critical resource run dry for too long,
and your vault will fail!

{C.BOLD}Controls:{C.RESET}
  • Use letter keys to select menu options
  • Each turn represents one day in the vault
  • Build strategically and assign dwellers wisely

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
            elif choice == 'd':
                self.manage_dwellers_menu()
            elif choice == 'r':
                self.assign_workers_menu()
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
