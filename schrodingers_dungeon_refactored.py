#!/usr/bin/env python3
"""
Schrödinger's Dungeon - Refactored
===================================
Every room exists in quantum superposition until you observe it.

This is a complete migration to the new infrastructure demonstrating:
- TurnBasedGame base class
- Save/load system
- Achievement tracking
- Configuration management
- Analytics (opt-in)
- Localization ready
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum

from base_game import TurnBasedGame, GameMetadata
from validation import get_menu_choice, get_yes_no_input
from logging_config import get_logger
from config_manager import get_config
from save_system import get_save_system
from achievements import AchievementSystem, Achievement, AchievementCategory, AchievementRarity
from analytics import get_analytics, track_game_start, track_game_end, EventType


# =============================================================================
# QUANTUM MECHANICS
# =============================================================================

class TileState(Enum):
    """Quantum state of a tile"""
    SUPERPOSED = "superposed"
    COLLAPSED = "collapsed"


@dataclass
class QuantumEntity:
    """An entity that exists in superposition"""
    possible_states: List[str]
    probabilities: List[float]
    collapsed_state: Optional[str] = None
    state: TileState = TileState.SUPERPOSED

    def collapse(self) -> str:
        """Collapse the superposition to a single state"""
        if self.state == TileState.COLLAPSED:
            return self.collapsed_state

        self.collapsed_state = random.choices(
            self.possible_states,
            weights=self.probabilities
        )[0]
        self.state = TileState.COLLAPSED
        return self.collapsed_state

    def get_symbol(self) -> str:
        """Get display symbol"""
        if self.state == TileState.SUPERPOSED:
            return "?"
        elif self.collapsed_state == "enemy":
            return "E"
        elif self.collapsed_state == "treasure":
            return "$"
        elif self.collapsed_state == "dead_enemy":
            return "✗"
        else:
            return "."


@dataclass
class Room:
    """A room in the dungeon"""
    x: int
    y: int
    entities: Dict[Tuple[int, int], QuantumEntity] = field(default_factory=dict)
    observed: bool = False
    walls: Set[Tuple[int, int]] = field(default_factory=set)
    width: int = 15
    height: int = 8


# =============================================================================
# MAIN GAME CLASS
# =============================================================================

class SchrodingersDungeon(TurnBasedGame):
    """
    Quantum dungeon crawler using modern infrastructure.

    Complete migration demonstrating all new features.
    """

    def __init__(self):
        super().__init__(GameMetadata(
            name="Schrödinger's Dungeon",
            version="2.0 (Refactored)",
            description="Quantum superposition dungeon crawler"
        ))

        # Infrastructure
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.save_system = get_save_system()
        self.achievements = AchievementSystem('schrodingers_dungeon')
        self.analytics = get_analytics()

        # Game state
        self.player_pos = (1, 1)
        self.current_room = (0, 0)
        self.rooms: Dict[Tuple[int, int], Room] = {}
        self.player_hp = 10
        self.max_hp = 10
        self.player_gold = 0
        self.observation_power = 1
        self.quantum_manipulations = 3
        self.enemies_defeated = 0
        self.victory = False

        # Setup achievements
        self._setup_achievements()

        # Generate starting room
        self.generate_room(0, 0)

        self.logger.info("Schrödinger's Dungeon initialized (refactored)")

        # Start analytics
        if self.analytics.is_enabled():
            track_game_start('schrodingers_dungeon', {'version': '2.0'})

    def _setup_achievements(self):
        """Setup game achievements"""
        achievements = [
            Achievement(
                id="first_collapse",
                name="Observer",
                description="Collapse your first quantum state",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.COMMON,
                points=5,
                icon="👁️",
                requirements={'collapses': 1}
            ),
            Achievement(
                id="quantum_warrior",
                name="Quantum Warrior",
                description="Defeat 10 enemies",
                category=AchievementCategory.COMBAT,
                rarity=AchievementRarity.UNCOMMON,
                points=15,
                icon="⚔️",
                requirements={'enemies_defeated': 10}
            ),
            Achievement(
                id="gold_collector",
                name="Greedy Observer",
                description="Collect 100 gold",
                category=AchievementCategory.COLLECTION,
                rarity=AchievementRarity.UNCOMMON,
                points=15,
                icon="💰",
                requirements={'gold_collected': 100}
            ),
            Achievement(
                id="survive_20",
                name="Quantum Survivor",
                description="Survive 20 turns",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.RARE,
                points=20,
                icon="🛡️",
                requirements={'turns_survived': 20}
            )
        ]

        for achievement in achievements:
            self.achievements.register_achievement(achievement)

    def setup(self):
        """Initialize game"""
        self.logger.info("Game setup started")
        self.print_intro()

    def print_intro(self):
        """Show game introduction"""
        self.clear_screen()
        self.print_header("SCHRÖDINGER'S DUNGEON v2.0")

        print("""
Every room exists in quantum superposition until you observe it.
Enemies are alive AND dead until you look.
Treasure is there AND not there until you check.

Navigate a dungeon where reality itself is probabilistic.

Controls:
  W/A/S/D - Move
  O - Observe (collapse nearby quantum states)
  Q - Quantum manipulation (special ability)
  M - Menu
        """)

        input("\nPress Enter to begin...")

    def render(self):
        """Render game state"""
        self.clear_screen()
        self.print_header(f"Schrödinger's Dungeon - Turn {self.turn}")

        # Player stats
        print(f"\n❤️  HP: {self.player_hp}/{self.max_hp}")
        print(f"💰 Gold: {self.player_gold}")
        print(f"👁️  Observation Power: {self.observation_power}")
        print(f"🌀 Quantum Manipulations: {self.quantum_manipulations}")
        print(f"⚔️  Enemies Defeated: {self.enemies_defeated}")

        # Render current room
        print(f"\n📍 Room: {self.current_room}")
        self._render_room()

        # Instructions
        print(f"\n⌨️  W/A/S/D: Move | O: Observe | Q: Quantum | M: Menu")

    def _render_room(self):
        """Render current room"""
        room = self.rooms.get(self.current_room)
        if not room:
            return

        print()
        for y in range(room.height):
            line = ""
            for x in range(room.width):
                pos = (x, y)

                if pos == self.player_pos:
                    line += "@"
                elif pos in room.walls:
                    line += "#"
                elif pos in room.entities:
                    entity = room.entities[pos]
                    line += entity.get_symbol()
                else:
                    line += "."

            print(line)

    def handle_input(self, key: Optional[str] = None):
        """Handle player input"""
        print("\nAction: ", end='')
        action = input().strip().lower()

        if action in ['w', 'a', 's', 'd']:
            self.move_player(action)
        elif action == 'o':
            self.observe()
        elif action == 'q':
            self.quantum_manipulation()
        elif action == 'm':
            self._show_menu()
        else:
            print("Invalid action!")
            input("Press Enter...")

    def move_player(self, direction: str):
        """Move player"""
        dx, dy = 0, 0

        if direction == 'w':
            dy = -1
        elif direction == 's':
            dy = 1
        elif direction == 'a':
            dx = -1
        elif direction == 'd':
            dx = 1

        new_pos = (self.player_pos[0] + dx, self.player_pos[1] + dy)
        room = self.rooms[self.current_room]

        # Check walls
        if new_pos in room.walls:
            print("Wall blocking!")
            input("Press Enter...")
            return

        # Check entities
        if new_pos in room.entities:
            entity = room.entities[new_pos]

            if entity.state == TileState.SUPERPOSED:
                # Force collapse
                state = entity.collapse()
                self.handle_collapsed_entity(state, new_pos)
            else:
                # Already collapsed
                self.handle_collapsed_entity(entity.collapsed_state, new_pos)

        # Move player
        self.player_pos = new_pos
        self.logger.debug(f"Player moved to {new_pos}")

    def handle_collapsed_entity(self, state: str, pos: Tuple[int, int]):
        """Handle interaction with collapsed entity"""
        room = self.rooms[self.current_room]

        if state == "enemy":
            # Combat!
            damage = random.randint(1, 3)
            self.player_hp -= damage
            print(f"\n⚔️  Enemy attacks! -{damage} HP")

            # Fight back
            if random.random() > 0.5:
                print("You defeat the enemy!")
                room.entities[pos].collapsed_state = "dead_enemy"
                self.enemies_defeated += 1

                # Track achievement
                self.achievements.update_progress('quantum_warrior', {
                    'enemies_defeated': self.enemies_defeated
                })

                # Track analytics
                if self.analytics.is_enabled():
                    self.analytics.track_event(EventType.COMBAT_END, {
                        'victory': True,
                        'enemies_defeated': self.enemies_defeated
                    })

            input("Press Enter...")

        elif state == "treasure":
            gold = random.randint(5, 15)
            self.player_gold += gold
            print(f"\n💰 Found {gold} gold!")

            # Remove treasure
            del room.entities[pos]

            # Track achievement
            self.achievements.update_progress('gold_collector', {
                'gold_collected': self.player_gold
            })

            input("Press Enter...")

        elif state == "dead_enemy":
            print("\nA defeated enemy...")
            input("Press Enter...")

    def observe(self):
        """Observe and collapse nearby quantum states"""
        room = self.rooms[self.current_room]
        collapsed_count = 0

        # Collapse entities within observation range
        for pos, entity in room.entities.items():
            if entity.state == TileState.SUPERPOSED:
                distance = abs(pos[0] - self.player_pos[0]) + abs(pos[1] - self.player_pos[1])
                if distance <= self.observation_power:
                    entity.collapse()
                    collapsed_count += 1

        print(f"\n👁️  Collapsed {collapsed_count} quantum states")

        # Track achievement
        if collapsed_count > 0:
            self.achievements.update_progress('first_collapse', {'collapses': 1})

        input("Press Enter...")

    def quantum_manipulation(self):
        """Use quantum manipulation ability"""
        if self.quantum_manipulations <= 0:
            print("\n❌ No quantum manipulations left!")
            input("Press Enter...")
            return

        self.quantum_manipulations -= 1

        # Reroll a random entity
        room = self.rooms[self.current_room]
        if room.entities:
            pos = random.choice(list(room.entities.keys()))
            entity = room.entities[pos]
            entity.state = TileState.SUPERPOSED
            entity.collapsed_state = None

            print(f"\n🌀 Quantum state reset at {pos}!")
            input("Press Enter...")

    def _show_menu(self):
        """Show in-game menu"""
        options = [
            "💾 Save Game",
            "📊 View Achievements",
            "⚙️  Settings",
            "❌ Quit to Main Menu",
            "← Back to Game"
        ]

        choice = get_menu_choice(options, title="Menu")

        if choice == 1:
            self.save_game()
        elif choice == 2:
            self._view_achievements()
        elif choice == 3:
            from config_manager import show_settings_menu
            show_settings_menu()
        elif choice == 4:
            if get_yes_no_input("Quit to main menu? (unsaved progress will be lost)"):
                self.quit()

    def _view_achievements(self):
        """View achievements"""
        self.clear_screen()
        self.print_header("Achievements")

        stats = self.achievements.get_statistics()
        print(f"\n🏆 Progress: {stats['unlocked']}/{stats['total_achievements']}")
        print(f"⭐ Points: {stats['earned_points']}/{stats['total_points']}\n")

        print("Unlocked:")
        for ach in self.achievements.get_unlocked():
            print(f"  ✅ {ach.icon} {ach.name} - {ach.description}")

        print("\nLocked:")
        for ach in self.achievements.get_locked():
            print(f"  🔒 {ach.name} - {ach.description}")

        input("\nPress Enter to continue...")

    def update(self):
        """Update game state"""
        # Track survival achievement
        self.achievements.update_progress('survive_20', {
            'turns_survived': self.turn
        })

        # Check game over
        if self.player_hp <= 0:
            self.game_over = True
            self.quit()

        # Auto-save
        if self.config.should_auto_save():
            if self.turn % self.config.gameplay.auto_save_interval == 0:
                self.save_game()

    def generate_room(self, rx: int, ry: int) -> Room:
        """Generate a new quantum room"""
        if (rx, ry) in self.rooms:
            return self.rooms[(rx, ry)]

        room = Room(x=rx, y=ry)

        # Add walls (border)
        for x in range(room.width):
            room.walls.add((x, 0))
            room.walls.add((x, room.height - 1))
        for y in range(room.height):
            room.walls.add((0, y))
            room.walls.add((room.width - 1, y))

        # Add quantum entities
        num_entities = random.randint(5, 12)
        for _ in range(num_entities):
            x = random.randint(2, room.width - 3)
            y = random.randint(2, room.height - 3)
            pos = (x, y)

            if pos != (1, 1) and pos not in room.walls:
                # Create quantum entity
                entity = QuantumEntity(
                    possible_states=["enemy", "treasure", "empty"],
                    probabilities=[0.4, 0.3, 0.3]
                )
                room.entities[pos] = entity

        self.rooms[(rx, ry)] = room
        return room

    def save_game(self):
        """Save game state"""
        save_data = {
            'player_pos': self.player_pos,
            'current_room': self.current_room,
            'player_hp': self.player_hp,
            'max_hp': self.max_hp,
            'player_gold': self.player_gold,
            'observation_power': self.observation_power,
            'quantum_manipulations': self.quantum_manipulations,
            'enemies_defeated': self.enemies_defeated,
            'turn': self.turn
        }

        self.save_system.save(
            game_id='schrodingers_dungeon',
            game_name="Schrödinger's Dungeon",
            data=save_data,
            save_slot=1,
            play_time=self.turn * 15
        )

        print("\n💾 Game saved successfully!")
        self.logger.info("Game saved")
        input("Press Enter...")

    def cleanup(self):
        """Cleanup on exit"""
        if self.analytics.is_enabled():
            track_game_end()

        self.logger.info(f"Game ended - Gold: {self.player_gold}, Enemies: {self.enemies_defeated}")

        print(f"\n{'='*60}")
        print("Final Stats:")
        print(f"  Turns Survived: {self.turn}")
        print(f"  Gold Collected: {self.player_gold}")
        print(f"  Enemies Defeated: {self.enemies_defeated}")
        print(f"  HP Remaining: {self.player_hp}/{self.max_hp}")
        print(f"{'='*60}")


def main():
    """Main entry point"""
    game = SchrodingersDungeon()
    game.run()


if __name__ == '__main__':
    main()
