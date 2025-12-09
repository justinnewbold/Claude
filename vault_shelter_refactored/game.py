#!/usr/bin/env python3
"""
Vault Shelter - Refactored Game
================================
Modular architecture demonstrating extracted components.

This is a refactored version of vault_shelter_v6.py showcasing:
- Clean separation of concerns
- Modular imports
- Maintainable codebase
- Same functionality, better organization
"""

import random
import os
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Import base infrastructure
from base_game import TurnBasedGame, GameMetadata
from save_system import get_save_system
from achievements import AchievementSystem, Achievement, AchievementCategory, AchievementRarity
from config_manager import get_config
from validation import get_menu_choice, get_yes_no_input
from logging_config import get_logger

# Import extracted vault modules
from vault_shelter_refactored.dweller import (
    Dweller,
    create_random_dweller,
    calculate_child_stats,
    get_relationship_status,
    SPECIAL_STATS
)
from vault_shelter_refactored.room import (
    Room,
    RoomType,
    RoomConfig,
    DEFAULT_ROOM_CONFIGS,
    calculate_adjacency_bonus,
    get_room_icon,
    get_room_name
)
from vault_shelter_refactored.resources import (
    ResourceManager,
    ResourceType,
    format_resource_bar,
    calculate_optimal_production,
    predict_shortage
)


# =============================================================================
# MAIN GAME CLASS
# =============================================================================

class VaultShelterRefactored(TurnBasedGame):
    """
    Refactored Vault Shelter game using modular architecture.

    Demonstrates clean separation:
    - Dwellers (dweller.py)
    - Rooms (room.py)
    - Resources (resources.py)
    - Game logic (this file)
    """

    def __init__(self):
        super().__init__(GameMetadata(
            name="Vault Shelter",
            version="6.0 (Refactored)",
            description="Post-apocalyptic vault management with modular architecture"
        ))

        # Infrastructure
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.save_system = get_save_system()
        self.achievements = AchievementSystem('vault_shelter')

        # Core game state using extracted modules
        self.resources = ResourceManager()
        self.dwellers: List[Dweller] = []
        self.vault_layout: List[List[Room]] = []

        # Game state
        self.day = 1
        self.game_over = False
        self.max_floors = 10
        self.floors_unlocked = 3
        self.rooms_per_floor = 5

        # Event log
        self.event_log: List[str] = []
        self.max_log_entries = 10

        # Equipment inventory
        self.equipment_inventory: List[str] = []

        # Statistics
        self.children_born = 0
        self.rooms_built = 0
        self.disasters_survived = 0

        # Setup achievements
        self._setup_achievements()

        # Initialize vault
        self._initialize_vault()

        self.logger.info("Vault Shelter (Refactored) initialized")

    def _setup_achievements(self):
        """Register game achievements"""
        achievements = [
            Achievement(
                id="first_dweller",
                name="New Arrival",
                description="Welcome your first dweller",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.COMMON,
                points=5,
                icon="👤",
                requirements={'dwellers': 1}
            ),
            Achievement(
                id="population_10",
                name="Growing Community",
                description="Reach 10 dwellers",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.UNCOMMON,
                points=15,
                icon="👥",
                requirements={'dwellers': 10}
            ),
            Achievement(
                id="first_room",
                name="Master Builder",
                description="Build your first room",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.COMMON,
                points=5,
                icon="🏗️",
                requirements={'rooms_built': 1}
            ),
            Achievement(
                id="survive_30",
                name="Vault Veteran",
                description="Survive 30 days",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.UNCOMMON,
                points=20,
                icon="🛡️",
                requirements={'days_survived': 30}
            ),
            Achievement(
                id="first_child",
                name="New Generation",
                description="Welcome the first vault-born child",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.RARE,
                points=25,
                icon="👶",
                requirements={'children_born': 1}
            )
        ]

        for achievement in achievements:
            self.achievements.register_achievement(achievement)

    def _initialize_vault(self):
        """Initialize starting vault layout and dwellers"""
        # Create vault layout
        for floor in range(self.max_floors):
            floor_rooms = []
            for position in range(self.rooms_per_floor):
                if floor < self.floors_unlocked and position < 3:
                    # Starting rooms
                    if position == 0:
                        room = Room(
                            room_type=RoomType.POWER_GENERATOR,
                            floor=floor,
                            position=position
                        )
                    elif position == 1:
                        room = Room(
                            room_type=RoomType.WATER_TREATMENT,
                            floor=floor,
                            position=position
                        )
                    else:
                        room = Room(
                            room_type=RoomType.GARDEN,
                            floor=floor,
                            position=position
                        )
                else:
                    # Empty rooms
                    room = Room(
                        room_type=RoomType.EMPTY,
                        floor=floor,
                        position=position
                    )
                floor_rooms.append(room)
            self.vault_layout.append(floor_rooms)

        # Create starting dwellers
        starter_names = ["Sarah", "John", "Maria", "David", "Lisa"]
        for name in starter_names:
            dweller = create_random_dweller(name)
            self.dwellers.append(dweller)

        # Track achievement
        self.achievements.update_progress('first_dweller', {'dwellers': len(self.dwellers)})

        self.log_event(f"Vault initialized with {len(self.dwellers)} dwellers")

    def setup(self):
        """Initialize game"""
        self.logger.info("Game setup started")
        self.print_intro()

    def print_intro(self):
        """Show game introduction"""
        self.clear_screen()
        self.print_header("VAULT SHELTER - REFACTORED")

        print("""
╔═══════════════════════════════════════════════════════════╗
║             VAULT SHELTER - SURVIVAL PROTOCOL             ║
║                   Refactored Architecture                 ║
╚═══════════════════════════════════════════════════════════╝

The year is 2077. Nuclear war has devastated the world.
You are the Overseer of Vault 67, humanity's last hope.

Your mission:
• Manage vault resources (power, water, food)
• Assign dwellers to production rooms
• Build and upgrade your vault
• Keep your population happy and healthy
• Survive as long as possible

This version demonstrates:
✅ Modular architecture
✅ Separated concerns (Dweller, Room, Resources)
✅ Clean imports
✅ Maintainable codebase

Good luck, Overseer.
        """)

        input("\nPress Enter to begin...")

    def render(self):
        """Render game state"""
        self.clear_screen()
        self.print_header(f"Vault Shelter - Day {self.day}")

        # Resources section
        print("\n┌─ RESOURCES ─────────────────────────────────────┐")
        print(f"│ {format_resource_bar('Power', self.resources.power, self.resources.power_storage, 12)} │")
        print(f"│ {format_resource_bar('Water', self.resources.water, self.resources.water_storage, 12)} │")
        print(f"│ {format_resource_bar('Food', self.resources.food, self.resources.food_storage, 12)} │")
        print(f"│ 💰 Caps: {self.resources.caps}                                │")
        print("└─────────────────────────────────────────────────┘")

        # Population section
        print(f"\n┌─ POPULATION ────────────────────────────────────┐")
        print(f"│ 👥 Dwellers: {len(self.dwellers)}                              │")
        adults = [d for d in self.dwellers if not d.is_child]
        children = [d for d in self.dwellers if d.is_child]
        print(f"│    Adults: {len(adults)} | Children: {len(children)}                   │")
        avg_happiness = sum(d.happiness for d in self.dwellers) / len(self.dwellers) if self.dwellers else 0
        print(f"│ 😊 Avg Happiness: {avg_happiness:.0f}%                       │")
        print("└─────────────────────────────────────────────────┘")

        # Vault layout preview (simplified)
        print("\n┌─ VAULT LAYOUT ──────────────────────────────────┐")
        for floor_idx, floor in enumerate(self.vault_layout[:3]):  # Show first 3 floors
            if floor_idx >= self.floors_unlocked:
                print(f"│ Floor {floor_idx + 1}: [LOCKED]                              │")
            else:
                icons = [get_room_icon(room.room_type) for room in floor[:3]]
                print(f"│ Floor {floor_idx + 1}: {' '.join(icons)}                                 │")
        print("└─────────────────────────────────────────────────┘")

        # Recent events
        if self.event_log:
            print("\n┌─ RECENT EVENTS ─────────────────────────────────┐")
            for event in self.event_log[-5:]:
                truncated = event[:45] + "..." if len(event) > 45 else event
                print(f"│ • {truncated.ljust(46)} │")
            print("└─────────────────────────────────────────────────┘")

        # Menu
        print("\n" + "═" * 50)
        print("Actions:")
        print("  1. Manage Dwellers")
        print("  2. Manage Rooms")
        print("  3. Build/Upgrade")
        print("  4. Next Day")
        print("  5. Save Game")
        print("  6. Achievements")
        print("  7. Quit")
        print("═" * 50)

    def handle_input(self, key: Optional[str] = None):
        """Handle player input"""
        choice = input("\nChoice: ").strip()

        if choice == '1':
            self.manage_dwellers()
        elif choice == '2':
            self.manage_rooms()
        elif choice == '3':
            self.build_menu()
        elif choice == '4':
            self.advance_day()
        elif choice == '5':
            self.save_game()
        elif choice == '6':
            self.view_achievements()
        elif choice == '7':
            if get_yes_no_input("Really quit?"):
                self.quit()
        else:
            print("Invalid choice!")
            input("Press Enter...")

    def manage_dwellers(self):
        """Dweller management screen"""
        self.clear_screen()
        self.print_header("Dweller Management")

        if not self.dwellers:
            print("\nNo dwellers in vault!")
            input("\nPress Enter...")
            return

        print("\nDwellers:")
        for idx, dweller in enumerate(self.dwellers, 1):
            status = "👶 Child" if dweller.is_child else "👤 Adult"
            room_str = f"@ {dweller.assigned_room}" if dweller.assigned_room else "Idle"
            print(f"{idx}. {dweller.name} - {status} - ❤️ {dweller.health}% - 😊 {dweller.happiness}% - {room_str}")

        print("\nOptions:")
        print("  1. View dweller details")
        print("  2. Assign to room")
        print("  3. Back")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            try:
                idx = int(input("Dweller number: ")) - 1
                if 0 <= idx < len(self.dwellers):
                    self.view_dweller_details(self.dwellers[idx])
            except ValueError:
                print("Invalid input!")
                input("Press Enter...")
        elif choice == '2':
            self.assign_dweller_to_room()

    def view_dweller_details(self, dweller: Dweller):
        """Show detailed dweller info"""
        self.clear_screen()
        self.print_header(f"Dweller: {dweller.name}")

        print(f"\nAge: {dweller.age}")
        print(f"Gender: {dweller.gender}")
        print(f"Health: {dweller.health}%")
        print(f"Happiness: {dweller.happiness}%")

        print("\n┌─ SPECIAL Stats ─────────────────────┐")
        for stat in SPECIAL_STATS:
            value = dweller.get_stat(stat)
            bar = "█" * value + "░" * (10 - value)
            print(f"│ {stat.title()}: {bar} {value:2d}/10 │")
        print("└─────────────────────────────────────┘")

        if dweller.learned_skills:
            print(f"\nSkills: {', '.join(dweller.learned_skills)}")

        if dweller.assigned_room:
            print(f"\nAssigned to: Room {dweller.assigned_room}")

        input("\nPress Enter...")

    def assign_dweller_to_room(self):
        """Assign a dweller to a room"""
        print("\n(Not implemented in this demo)")
        input("Press Enter...")

    def manage_rooms(self):
        """Room management screen"""
        self.clear_screen()
        self.print_header("Room Management")

        # List all non-empty rooms
        rooms = []
        for floor in self.vault_layout:
            for room in floor:
                if room.room_type != RoomType.EMPTY:
                    rooms.append(room)

        if not rooms:
            print("\nNo rooms built yet!")
            input("\nPress Enter...")
            return

        print("\nRooms:")
        for idx, room in enumerate(rooms, 1):
            name = get_room_name(room.room_type)
            workers = len(room.assigned_dwellers)
            capacity = room.get_capacity()
            print(f"{idx}. {name} (Floor {room.floor + 1}) - Level {room.level} - Workers: {workers}/{capacity}")

        input("\nPress Enter...")

    def build_menu(self):
        """Building menu"""
        self.clear_screen()
        self.print_header("Build/Upgrade")

        print("\nAvailable rooms:")
        configs = list(DEFAULT_ROOM_CONFIGS.values())
        for idx, config in enumerate(configs, 1):
            print(f"{idx}. {config.icon} {config.name} - Cost: {config.cost} caps")

        print(f"\n{len(configs) + 1}. Cancel")

        try:
            choice = int(input("\nChoice: "))
            if 1 <= choice <= len(configs):
                config = configs[choice - 1]
                self.build_room(config)
        except ValueError:
            pass

    def build_room(self, config: RoomConfig):
        """Build a new room"""
        # Check resources
        if not self.resources.consume_resource('caps', config.cost):
            print(f"\n❌ Not enough caps! Need {config.cost}, have {self.resources.caps}")
            input("Press Enter...")
            return

        # Find empty room slot
        for floor in range(self.floors_unlocked):
            for pos in range(self.rooms_per_floor):
                room = self.vault_layout[floor][pos]
                if room.room_type == RoomType.EMPTY:
                    # Build here
                    room.room_type = config.room_type
                    room.level = 1
                    self.rooms_built += 1

                    self.log_event(f"Built {config.name} on Floor {floor + 1}")
                    print(f"\n✅ Built {config.name} on Floor {floor + 1}")

                    # Track achievement
                    self.achievements.update_progress('first_room', {'rooms_built': self.rooms_built})

                    input("Press Enter...")
                    return

        print("\n❌ No empty room slots available!")
        input("Press Enter...")

    def advance_day(self):
        """Progress to next day"""
        self.day += 1
        self.turn += 1

        # Calculate production
        total_production = {
            'power': 0,
            'water': 0,
            'food': 0
        }

        for floor in self.vault_layout:
            for room in floor:
                production = room.get_production(
                    dwellers_list=self.dwellers,
                    room_configs=DEFAULT_ROOM_CONFIGS,
                    adjacency_bonus=calculate_adjacency_bonus(room, [r for f in self.vault_layout for r in f])
                )
                for resource, amount in production.items():
                    if resource in total_production:
                        total_production[resource] += amount

        # Add production
        for resource, amount in total_production.items():
            self.resources.add_resource(resource, amount)

        # Apply consumption
        population = len(self.dwellers)
        shortages = self.resources.apply_consumption(population)

        # Check shortages
        for resource, has_shortage in shortages.items():
            if has_shortage:
                self.log_event(f"⚠️  {resource.title()} shortage!")
                # Reduce happiness
                for dweller in self.dwellers:
                    dweller.happiness = max(0, dweller.happiness - 5)

        # Record history
        self.resources.record_history()

        # Age children
        for dweller in self.dwellers:
            if dweller.is_child:
                dweller.age += 1
                if dweller.age >= 18:
                    dweller.is_child = False
                    self.log_event(f"{dweller.name} has grown up!")

        # Random events
        if random.random() < 0.1:
            self._random_event()

        self.log_event(f"Day {self.day} completed")

        # Track achievement
        self.achievements.update_progress('survive_30', {'days_survived': self.day})
        self.achievements.update_progress('population_10', {'dwellers': len(self.dwellers)})

    def _random_event(self):
        """Trigger a random event"""
        events = [
            "A stranger arrives at the vault door!",
            "Dwellers find extra supplies in storage.",
            "Minor power surge detected.",
            "Dwellers are in good spirits today!"
        ]

        event = random.choice(events)
        self.log_event(f"📰 {event}")

        # Handle some events
        if "stranger" in event and random.random() > 0.5:
            new_dweller = create_random_dweller(f"Newcomer{random.randint(1, 999)}")
            self.dwellers.append(new_dweller)
            self.log_event(f"✅ {new_dweller.name} joined the vault!")

    def view_achievements(self):
        """View achievements screen"""
        self.clear_screen()
        self.print_header("Achievements")

        stats = self.achievements.get_statistics()
        print(f"\n🏆 Progress: {stats['unlocked']}/{stats['total_achievements']}")
        print(f"⭐ Points: {stats['earned_points']}/{stats['total_points']}\n")

        print("Unlocked:")
        for ach in self.achievements.get_unlocked():
            print(f"  ✅ {ach.icon} {ach.name} - {ach.description} ({ach.points} pts)")

        print("\nLocked:")
        for ach in self.achievements.get_locked():
            print(f"  🔒 {ach.name} - {ach.description}")

        input("\n\nPress Enter to continue...")

    def update(self):
        """Update game state"""
        # Check game over
        if self.resources.power <= 0 and self.resources.water <= 0 and self.resources.food <= 0:
            self.game_over = True
            self.log_event("💀 Vault has fallen...")
            self.quit()

        # Auto-save
        if self.config.should_auto_save():
            if self.day % self.config.gameplay.auto_save_interval == 0:
                self.save_game()

    def save_game(self):
        """Save game state"""
        save_data = {
            'day': self.day,
            'turn': self.turn,
            'resources': self.resources.to_dict(),
            'dwellers': [d.to_dict() for d in self.dwellers],
            'vault_layout': [[r.to_dict() for r in floor] for floor in self.vault_layout],
            'event_log': self.event_log,
            'children_born': self.children_born,
            'rooms_built': self.rooms_built,
            'disasters_survived': self.disasters_survived,
            'floors_unlocked': self.floors_unlocked,
        }

        self.save_system.save(
            game_id='vault_shelter_refactored',
            game_name='Vault Shelter (Refactored)',
            data=save_data,
            save_slot=1,
            play_time=self.day * 60  # Approximate playtime
        )

        print("\n💾 Game saved successfully!")
        self.logger.info(f"Game saved at day {self.day}")
        input("Press Enter...")

    def log_event(self, message: str):
        """Add event to log"""
        self.event_log.append(f"Day {self.day}: {message}")
        if len(self.event_log) > self.max_log_entries:
            self.event_log.pop(0)

    def cleanup(self):
        """Cleanup on exit"""
        self.logger.info(f"Game ended - Day: {self.day}, Population: {len(self.dwellers)}")

        print(f"\n{'=' * 60}")
        print("Final Stats:")
        print(f"  Days Survived: {self.day}")
        print(f"  Final Population: {len(self.dwellers)}")
        print(f"  Rooms Built: {self.rooms_built}")
        print(f"  Children Born: {self.children_born}")
        print(f"  Final Caps: {self.resources.caps}")
        print(f"{'=' * 60}")


def main():
    """Main entry point"""
    game = VaultShelterRefactored()
    game.run()


if __name__ == '__main__':
    main()
