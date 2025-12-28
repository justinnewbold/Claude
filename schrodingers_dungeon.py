#!/usr/bin/env python3
"""
SCHRÖDINGER'S DUNGEON

Every room exists in quantum superposition until you observe it.
Enemies are alive AND dead until you look.
Treasure is there AND not there until you check.

Navigate a dungeon where reality itself is probabilistic.
Manipulate wave functions. Collapse possibilities strategically.
Survive quantum uncertainty.

The cat would be proud. Or dead. Or both.
"""

import random
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import copy

# ANSI colors
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Quantum states
    SUPERPOSED = '\033[38;5;141m'    # Purple - superposition
    OBSERVED = '\033[38;5;51m'       # Cyan - collapsed/observed
    PLAYER = '\033[38;5;226m'        # Yellow
    ENEMY_ALIVE = '\033[38;5;196m'   # Red
    ENEMY_DEAD = '\033[38;5;240m'    # Dark gray
    TREASURE = '\033[38;5;220m'      # Gold
    EMPTY = '\033[38;5;243m'         # Gray
    WALL = '\033[38;5;237m'          # Dark gray

    # UI
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    ERROR = '\033[38;5;203m'
    QUANTUM = '\033[38;5;201m'


class TileState(Enum):
    SUPERPOSED = "superposed"
    COLLAPSED = "collapsed"


@dataclass
class QuantumEntity:
    """An entity that exists in superposition"""
    possible_states: List[str]  # e.g., ["enemy", "empty", "treasure"]
    probabilities: List[float]  # Probabilities for each state
    collapsed_state: Optional[str] = None
    state: TileState = TileState.SUPERPOSED

    def collapse(self) -> str:
        """Collapse the superposition to a single state"""
        if self.state == TileState.COLLAPSED:
            return self.collapsed_state

        # Weighted random choice based on probabilities
        self.collapsed_state = random.choices(
            self.possible_states,
            weights=self.probabilities
        )[0]
        self.state = TileState.COLLAPSED
        return self.collapsed_state

    def get_display(self) -> Tuple[str, str]:
        """Return (symbol, color) for display"""
        if self.state == TileState.SUPERPOSED:
            # Show superposition symbol
            return ("?", C.SUPERPOSED)
        else:
            # Show collapsed state
            if self.collapsed_state == "enemy":
                return ("E", C.ENEMY_ALIVE)
            elif self.collapsed_state == "treasure":
                return ("$", C.TREASURE)
            elif self.collapsed_state == "empty":
                return (".", C.EMPTY)
            elif self.collapsed_state == "dead_enemy":
                return ("✗", C.ENEMY_DEAD)
            else:
                return ("?", C.OBSERVED)


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


class SchrodingersDungeon:
    def __init__(self):
        self.player_pos = (1, 1)
        self.current_room = (0, 0)
        self.rooms: Dict[Tuple[int, int], Room] = {}
        self.player_hp = 10
        self.max_hp = 10
        self.player_gold = 0
        self.observation_power = 1  # How far you can see
        self.quantum_manipulations = 3  # Special ability uses
        self.turns = 0
        self.enemies_defeated = 0
        self.game_over = False
        self.victory = False

        self.generate_room(0, 0)

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def generate_room(self, rx: int, ry: int) -> Room:
        """Generate a new room with quantum entities"""
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

        # Add some internal walls
        num_walls = random.randint(3, 8)
        for _ in range(num_walls):
            wx, wy = random.randint(2, room.width - 3), random.randint(2, room.height - 3)
            if (wx, wy) != (1, 1):  # Don't block spawn
                room.walls.add((wx, wy))

        # Add quantum entities in superposition
        num_entities = random.randint(5, 12)
        for _ in range(num_entities):
            ex, ey = random.randint(1, room.width - 2), random.randint(1, room.height - 2)

            if (ex, ey) in room.walls or (ex, ey) == (1, 1):
                continue

            # Each entity has probability of being enemy, treasure, or empty
            # As you go deeper, more enemies
            depth = abs(rx) + abs(ry)
            enemy_prob = min(0.4 + depth * 0.05, 0.7)
            treasure_prob = 0.2
            empty_prob = 1.0 - enemy_prob - treasure_prob

            entity = QuantumEntity(
                possible_states=["enemy", "treasure", "empty"],
                probabilities=[enemy_prob, treasure_prob, empty_prob]
            )
            room.entities[(ex, ey)] = entity

        # Add exits (doors to other rooms)
        # Top exit
        room.entities[(room.width // 2, 0)] = QuantumEntity(
            possible_states=["exit_north"],
            probabilities=[1.0],
            collapsed_state="exit_north",
            state=TileState.COLLAPSED
        )
        # Bottom exit
        room.entities[(room.width // 2, room.height - 1)] = QuantumEntity(
            possible_states=["exit_south"],
            probabilities=[1.0],
            collapsed_state="exit_south",
            state=TileState.COLLAPSED
        )
        # Left exit
        room.entities[(0, room.height // 2)] = QuantumEntity(
            possible_states=["exit_west"],
            probabilities=[1.0],
            collapsed_state="exit_west",
            state=TileState.COLLAPSED
        )
        # Right exit
        room.entities[(room.width - 1, room.height // 2)] = QuantumEntity(
            possible_states=["exit_east"],
            probabilities=[1.0],
            collapsed_state="exit_east",
            state=TileState.COLLAPSED
        )

        self.rooms[(rx, ry)] = room
        return room

    def show_intro(self):
        """Show intro"""
        self.clear_screen()
        self.print_header("S C H R Ö D I N G E R ' S   D U N G E O N")

        intro = f"""
{C.QUANTUM}"In the quantum realm, nothing is certain until observed."{C.RESET}

{C.DIM}You enter a dungeon that exists in quantum superposition.

Every room is simultaneously:
• Full of enemies AND empty
• Filled with treasure AND barren
• Dangerous AND safe

Until you {C.BOLD}observe{C.RESET}{C.DIM} it.

{C.BOLD}The Quantum Mechanics:{C.RESET}

{C.SUPERPOSED}?{C.RESET} = Superposed entity (multiple states at once)
{C.ENEMY_ALIVE}E{C.RESET} = Collapsed to Enemy (alive)
{C.TREASURE}${C.RESET} = Collapsed to Treasure
{C.EMPTY}.{C.RESET} = Collapsed to Empty
{C.PLAYER}@{C.RESET} = You (the observer)

{C.BOLD}Special Abilities:{C.RESET}

{C.QUANTUM}Q{C.RESET} - Quantum Manipulation: Force favorable collapse
{C.OBSERVED}O{C.RESET} - Observe: Collapse entities at range

{C.DIM}Movement collapses entities you touch.
Observation collapses entities you see.
Quantum manipulation lets you cheat probability.

The dungeon is both dangerous and safe.
Until you look.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def get_room(self) -> Room:
        """Get current room"""
        return self.rooms[self.current_room]

    def observe_area(self, center_x: int, center_y: int, radius: int):
        """Collapse entities in observation radius"""
        room = self.get_room()
        collapsed = []

        for (ex, ey), entity in room.entities.items():
            dist = abs(ex - center_x) + abs(ey - center_y)  # Manhattan distance
            if dist <= radius and entity.state == TileState.SUPERPOSED:
                entity.collapse()
                collapsed.append((ex, ey))

        return collapsed

    def render_room(self):
        """Render the current room"""
        room = self.get_room()

        # Auto-observe area around player
        self.observe_area(self.player_pos[0], self.player_pos[1], self.observation_power)

        print(f"\n{C.QUANTUM}╔═ QUANTUM DUNGEON ═╗{C.RESET}")
        print(f"{C.SYSTEM}Room ({room.x}, {room.y}) | HP: {self.player_hp}/{self.max_hp} | Gold: {self.player_gold} | Q-Power: {self.quantum_manipulations}{C.RESET}\n")

        # Render grid
        for y in range(room.height):
            line = "  "
            for x in range(room.width):
                if (x, y) == self.player_pos:
                    line += f"{C.PLAYER}@{C.RESET}"
                elif (x, y) in room.walls:
                    line += f"{C.WALL}#{C.RESET}"
                elif (x, y) in room.entities:
                    entity = room.entities[(x, y)]
                    symbol, color = entity.get_display()

                    # Special display for exits
                    if entity.collapsed_state and "exit" in entity.collapsed_state:
                        symbol = "▯"
                        color = C.OBSERVED

                    line += f"{color}{symbol}{C.RESET}"
                else:
                    line += f"{C.EMPTY}.{C.RESET}"
            print(line)

        print(f"\n{C.SYSTEM}Move: W/A/S/D | Observe: O | Quantum Manipulate: Q | Quit: X{C.RESET}")

    def move_player(self, dx: int, dy: int):
        """Move player and handle interactions"""
        room = self.get_room()
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        # Check bounds
        if new_x < 0 or new_x >= room.width or new_y < 0 or new_y >= room.height:
            return

        # Check walls
        if (new_x, new_y) in room.walls:
            return

        # Check for entity at new position
        if (new_x, new_y) in room.entities:
            entity = room.entities[(new_x, new_y)]

            # Handle exits
            if entity.collapsed_state and "exit" in entity.collapsed_state:
                parts = entity.collapsed_state.split("_")
                direction = parts[1] if len(parts) > 1 else "unknown"
                self.handle_exit(direction)
                return

            # Collapse on contact
            if entity.state == TileState.SUPERPOSED:
                entity.collapse()

            # Handle collapsed state
            if entity.collapsed_state == "enemy":
                self.combat(new_x, new_y)
                return
            elif entity.collapsed_state == "treasure":
                gold = random.randint(3, 8)
                self.player_gold += gold
                print(f"\n{C.SUCCESS}Found {gold} gold!{C.RESET}")
                time.sleep(0.5)
                del room.entities[(new_x, new_y)]
            elif entity.collapsed_state == "empty":
                pass  # Just empty space

        # Move player
        self.player_pos = (new_x, new_y)
        self.turns += 1

    def combat(self, enemy_x: int, enemy_y: int):
        """Fight an enemy"""
        room = self.get_room()

        print(f"\n{C.ENEMY_ALIVE}Combat! An enemy appeared!{C.RESET}")
        time.sleep(0.5)

        # Simple combat
        enemy_hp = random.randint(2, 4)
        player_damage = random.randint(1, 3)

        enemy_hp -= player_damage

        if enemy_hp <= 0:
            print(f"{C.SUCCESS}Enemy defeated!{C.RESET}")
            room.entities[(enemy_x, enemy_y)].collapsed_state = "dead_enemy"
            self.enemies_defeated += 1
            time.sleep(0.5)
        else:
            # Enemy hits back
            enemy_damage = random.randint(1, 2)
            self.player_hp -= enemy_damage
            print(f"{C.ERROR}Enemy hits you for {enemy_damage} damage!{C.RESET}")
            time.sleep(0.5)

            if self.player_hp <= 0:
                self.game_over = True
                return

    def handle_exit(self, direction: str):
        """Move to adjacent room"""
        rx, ry = self.current_room

        if direction == "north":
            ry -= 1
            spawn = (self.get_room().width // 2, self.get_room().height - 2)
        elif direction == "south":
            ry += 1
            spawn = (self.get_room().width // 2, 1)
        elif direction == "west":
            rx -= 1
            spawn = (self.get_room().width - 2, self.get_room().height // 2)
        elif direction == "east":
            rx += 1
            spawn = (1, self.get_room().height // 2)

        self.current_room = (rx, ry)
        self.generate_room(rx, ry)
        self.player_pos = spawn

        print(f"\n{C.OBSERVED}Entering new room ({rx}, {ry})...{C.RESET}")
        time.sleep(0.5)

    def quantum_manipulate(self):
        """Use quantum manipulation to force favorable outcome"""
        if self.quantum_manipulations <= 0:
            print(f"\n{C.ERROR}No quantum manipulations remaining!{C.RESET}")
            time.sleep(0.5)
            return

        room = self.get_room()

        print(f"\n{C.QUANTUM}Quantum Manipulation active!{C.RESET}")
        print(f"{C.DIM}Forcing favorable wave function collapse...{C.RESET}\n")

        # Force all nearby superposed entities to collapse to non-enemy states
        manipulated = 0
        for (ex, ey), entity in room.entities.items():
            dist = abs(ex - self.player_pos[0]) + abs(ey - self.player_pos[1])
            if dist <= 3 and entity.state == TileState.SUPERPOSED:
                # Force collapse to treasure or empty (no enemies)
                entity.possible_states = ["treasure", "empty"]
                entity.probabilities = [0.6, 0.4]
                entity.collapse()
                manipulated += 1

        self.quantum_manipulations -= 1

        print(f"{C.SUCCESS}Manipulated {manipulated} quantum states!{C.RESET}")
        time.sleep(1)

    def observe_power(self):
        """Use observation at range"""
        print(f"\n{C.OBSERVED}Observing distant entities...{C.RESET}")

        # Collapse entities in larger radius
        collapsed = self.observe_area(
            self.player_pos[0],
            self.player_pos[1],
            self.observation_power + 2
        )

        print(f"{C.SUCCESS}Observed {len(collapsed)} quantum entities!{C.RESET}")
        time.sleep(1)

    def show_victory(self):
        """Show victory screen"""
        self.clear_screen()
        self.print_header("Q U A N T U M   V I C T O R Y")

        victory = f"""
{C.SUCCESS}You survived the quantum dungeon!{C.RESET}

{C.DIM}By observing, collapsing, and manipulating quantum states,
you navigated a reality that was simultaneously all things.{C.RESET}

{C.BOLD}Statistics:{C.RESET}
• Rooms explored: {len(self.rooms)}
• Enemies defeated: {self.enemies_defeated}
• Gold collected: {self.player_gold}
• Turns taken: {self.turns}
• Final HP: {self.player_hp}/{self.max_hp}

{C.QUANTUM}"Reality is merely probability until observed."{C.RESET}

{C.DIM}The cat is both alive and dead.
Until you opened the box.{C.RESET}
"""
        print(victory)

    def show_defeat(self):
        """Show defeat screen"""
        self.clear_screen()
        self.print_header("W A V E   F U N C T I O N   C O L L A P S E D")

        defeat = f"""
{C.ERROR}Your wave function collapsed to the dead state.{C.RESET}

{C.DIM}In one timeline, you survived.
In this one, you didn't.{C.RESET}

{C.BOLD}Statistics:{C.RESET}
• Rooms explored: {len(self.rooms)}
• Enemies defeated: {self.enemies_defeated}
• Gold collected: {self.player_gold}
• Turns survived: {self.turns}

{C.QUANTUM}Perhaps in another quantum branch, another you succeeded.{C.RESET}
"""
        print(defeat)

    def play(self):
        """Main game loop"""
        self.show_intro()

        # Victory condition: survive 10 rooms
        victory_rooms = 10

        while not self.game_over:
            self.clear_screen()
            self.render_room()

            # Check victory
            if len(self.rooms) >= victory_rooms and self.player_hp > 0:
                self.victory = True
                self.game_over = True
                break

            # Get input
            try:
                import sys, tty, termios
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)

                if ch.lower() == 'w':
                    self.move_player(0, -1)
                elif ch.lower() == 's':
                    self.move_player(0, 1)
                elif ch.lower() == 'a':
                    self.move_player(-1, 0)
                elif ch.lower() == 'd':
                    self.move_player(1, 0)
                elif ch.lower() == 'q':
                    self.quantum_manipulate()
                elif ch.lower() == 'o':
                    self.observe_power()
                elif ch.lower() == 'x':
                    self.game_over = True
                    self.victory = False

            except (ImportError, termios.error):
                cmd = input(f"\n{C.SYSTEM}Command (w/a/s/d/q/o/x): {C.RESET}").lower().strip()
                if cmd == 'w':
                    self.move_player(0, -1)
                elif cmd == 's':
                    self.move_player(0, 1)
                elif cmd == 'a':
                    self.move_player(-1, 0)
                elif cmd == 'd':
                    self.move_player(1, 0)
                elif cmd == 'q':
                    self.quantum_manipulate()
                elif cmd == 'o':
                    self.observe_power()
                elif cmd == 'x':
                    self.game_over = True
                    self.victory = False

        # Game over
        if self.victory:
            self.show_victory()
        else:
            self.show_defeat()

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"SCHRÖDINGER'S DUNGEON")
        print(f"Where observation determines reality")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = SchrodingersDungeon()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.QUANTUM}Wave function interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}Quantum anomaly: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
