#!/usr/bin/env python3
"""
THE EMERGENCE ENGINE

Conway's Game of Life meets puzzle navigation.

Simple rules create complex behavior.
Dead cells with 3 neighbors come alive.
Live cells with 2-3 neighbors survive.
All else dies.

From these three rules, infinite complexity emerges:
Gliders. Oscillators. Spaceships. Gardens of Eden.

Navigate a living, breathing world.
Manipulate emergence to reach your goals.
"""

import random
import time
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from colors import C
from platform_utils import clear_screen


@dataclass
class World:
    """A Game of Life world"""
    width: int
    height: int
    cells: Set[Tuple[int, int]] = field(default_factory=set)  # Living cells
    generation: int = 0
    player_pos: Optional[Tuple[int, int]] = None
    goal_pos: Optional[Tuple[int, int]] = None
    immortal_cells: Set[Tuple[int, int]] = field(default_factory=set)

    def is_alive(self, x: int, y: int) -> bool:
        return (x, y) in self.cells

    def count_neighbors(self, x: int, y: int) -> int:
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                # Wrap around (toroidal world)
                nx = nx % self.width
                ny = ny % self.height
                if self.is_alive(nx, ny):
                    count += 1
        return count

    def step(self):
        """Advance one generation"""
        new_cells = set()

        # Check all cells and their neighbors
        cells_to_check = set()
        for x, y in self.cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = (x + dx) % self.width, (y + dy) % self.height
                    cells_to_check.add((nx, ny))

        for x, y in cells_to_check:
            neighbors = self.count_neighbors(x, y)
            is_alive_now = self.is_alive(x, y)

            # Conway's Game of Life rules
            if is_alive_now:
                # Survival: 2 or 3 neighbors
                if neighbors in [2, 3] or (x, y) in self.immortal_cells:
                    new_cells.add((x, y))
            else:
                # Birth: exactly 3 neighbors
                if neighbors == 3:
                    new_cells.add((x, y))

        self.cells = new_cells
        self.generation += 1


class EmergenceEngine:
    def __init__(self):
        self.world = World(width=60, height=20)
        self.paused = True
        self.game_over = False
        self.victory = False
        self.level = 1
        self.steps = 0
        self.generations_passed = 0
        self.cells_placed = 0
        self.cells_removed = 0

        # Patterns library
        self.patterns = {
            "glider": [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)],
            "blinker": [(0, 0), (1, 0), (2, 0)],
            "block": [(0, 0), (1, 0), (0, 1), (1, 1)],
            "toad": [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
        }

        self.setup_level(1)

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_level(self, level_num: int):
        """Setup a specific level"""
        self.world = World(width=60, height=20)

        if level_num == 1:
            # Tutorial: Navigate to goal with stable pattern
            self.world.player_pos = (5, 10)
            self.world.goal_pos = (54, 10)

            # Add some stable blocks
            for x in [15, 25, 35, 45]:
                self.world.cells.update([(x, 9), (x+1, 9), (x, 10), (x+1, 10)])
                self.world.immortal_cells.update([(x, 9), (x+1, 9), (x, 10), (x+1, 10)])

        elif level_num == 2:
            # Navigate through oscillators
            self.world.player_pos = (5, 10)
            self.world.goal_pos = (54, 10)

            # Add blinkers
            for x in range(10, 50, 8):
                self.world.cells.update([(x, 9), (x+1, 9), (x+2, 9)])

        elif level_num == 3:
            # Use gliders to clear path
            self.world.player_pos = (5, 2)
            self.world.goal_pos = (54, 18)

            # Add glider gun pattern (simplified)
            for x in range(15, 45, 10):
                glider = self.patterns["glider"]
                self.world.cells.update([(x+dx, 10+dy) for dx, dy in glider])

        elif level_num == 4:
            # Complex emergence
            self.world.player_pos = (5, 10)
            self.world.goal_pos = (54, 10)

            # Random initial state
            for _ in range(200):
                x, y = random.randint(10, 50), random.randint(5, 15)
                if random.random() < 0.3:
                    self.world.cells.add((x, y))

        else:
            # Victory!
            self.victory = True
            self.game_over = True

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("T H E   E M E R G E N C E   E N G I N E")

        intro = f"""
{C.EMERGENCE}"Complex systems arise from simple rules."{C.RESET}

{C.DIM}Welcome to Conway's Game of Life - as a navigable puzzle.

The world is governed by three simple rules:

1. Any live cell with 2-3 neighbors survives
2. Any dead cell with exactly 3 neighbors becomes alive
3. All other cells die

From these rules, infinite complexity emerges.{C.RESET}

{C.BOLD}Your Mission:{C.RESET}

Navigate to the {C.GOAL}goal{C.RESET} ({C.GOAL}*{C.RESET}) through a living world.

{C.ALIVE}█{C.RESET} = Living cell
{C.DEAD}·{C.RESET} = Dead cell
{C.PLAYER}@{C.RESET} = You
{C.GOAL}*{C.RESET} = Goal
{C.IMMORTAL}■{C.RESET} = Immortal cell (won't die)

{C.BOLD}Controls:{C.RESET}

{C.SYSTEM}Movement:{C.RESET}
  W/A/S/D - Move player
  SPACE - Wait (advance one generation)

{C.SYSTEM}Manipulation:{C.RESET}
  P - Place/remove cell at cursor
  G - Spawn glider
  B - Spawn blinker
  ENTER - Pause/unpause evolution

{C.SYSTEM}Other:{C.RESET}
  Q - Quit

{C.EMERGENCE}Watch the patterns emerge. Learn their behavior.
Manipulate life itself to reach your goal.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def render_world(self):
        """Render the current world state"""
        print(f"\n{C.EMERGENCE}╔═ EMERGENCE ENGINE ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level} | Gen: {self.world.generation} | " +
              f"Cells: {len(self.world.cells)} | " +
              f"{'PAUSED' if self.paused else 'RUNNING'}{C.RESET}\n")

        # Render grid
        for y in range(self.world.height):
            line = "  "
            for x in range(self.world.width):
                pos = (x, y)

                if pos == self.world.player_pos:
                    line += f"{C.PLAYER}@{C.RESET}"
                elif pos == self.world.goal_pos:
                    line += f"{C.GOAL}*{C.RESET}"
                elif pos in self.world.immortal_cells:
                    line += f"{C.IMMORTAL}■{C.RESET}"
                elif pos in self.world.cells:
                    line += f"{C.ALIVE}█{C.RESET}"
                else:
                    line += f"{C.DEAD}·{C.RESET}"
            print(line)

        print(f"\n{C.SYSTEM}Move: W/A/S/D | Wait: SPACE | Place cell: P | " +
              f"Glider: G | Pause: ENTER | Quit: Q{C.RESET}")

    def move_player(self, dx: int, dy: int):
        """Move the player"""
        if self.world.player_pos is None:
            return

        x, y = self.world.player_pos
        new_x = (x + dx) % self.world.width
        new_y = (y + dy) % self.world.height

        # Can't move into living cells
        if (new_x, new_y) in self.world.cells:
            return

        self.world.player_pos = (new_x, new_y)
        self.steps += 1

        # Check goal
        if self.world.player_pos == self.world.goal_pos:
            self.level += 1
            self.setup_level(self.level)

    def place_cell(self):
        """Toggle cell at player position"""
        if self.world.player_pos is None:
            return

        x, y = self.world.player_pos

        if (x, y) in self.world.cells:
            self.world.cells.remove((x, y))
            self.cells_removed += 1
        else:
            self.world.cells.add((x, y))
            self.cells_placed += 1

    def spawn_pattern(self, pattern_name: str):
        """Spawn a pattern at player position"""
        if self.world.player_pos is None or pattern_name not in self.patterns:
            return

        px, py = self.world.player_pos
        pattern = self.patterns[pattern_name]

        for dx, dy in pattern:
            nx = (px + dx) % self.world.width
            ny = (py + dy) % self.world.height
            self.world.cells.add((nx, ny))

        self.cells_placed += len(pattern)

    def show_victory(self):
        """Show victory screen"""
        self.clear_screen()
        self.print_header("E M E R G E N C E   A C H I E V E D")

        victory = f"""
{C.SUCCESS}You've navigated the emergent world!{C.RESET}

{C.DIM}From three simple rules:
• Survival with 2-3 neighbors
• Birth with exactly 3 neighbors
• Death otherwise

...you witnessed infinite complexity.{C.RESET}

{C.BOLD}Statistics:{C.RESET}
• Levels completed: {self.level - 1}
• Steps taken: {self.steps}
• Generations observed: {self.generations_passed}
• Cells placed: {self.cells_placed}
• Cells removed: {self.cells_removed}

{C.EMERGENCE}"The whole is more than the sum of its parts."{C.RESET}

{C.DIM}You've seen emergence in action:
Simple local rules creating complex global behavior.

Gliders traveling forever.
Oscillators pulsing in rhythm.
Patterns stabilizing or exploding.

This is how complexity arises in nature:
From simple rules, endlessly iterated.{C.RESET}
"""
        print(victory)

    def play(self):
        """Main game loop"""
        self.show_intro()

        auto_step_counter = 0

        while not self.game_over:
            self.clear_screen()
            self.render_world()

            # Auto-step if not paused
            if not self.paused:
                auto_step_counter += 1
                if auto_step_counter >= 5:  # Slower auto-step
                    self.world.step()
                    self.generations_passed += 1
                    auto_step_counter = 0
                    time.sleep(0.1)

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
                elif ch == ' ':
                    self.world.step()
                    self.generations_passed += 1
                elif ch.lower() == 'p':
                    self.place_cell()
                elif ch.lower() == 'g':
                    self.spawn_pattern("glider")
                elif ch.lower() == 'b':
                    self.spawn_pattern("blinker")
                elif ch == '\r' or ch == '\n':
                    self.paused = not self.paused
                elif ch.lower() == 'q':
                    self.game_over = True
                    self.victory = False

            except (ImportError, termios.error):
                cmd = input(f"\n{C.SYSTEM}Command: {C.RESET}").lower().strip()

                if cmd in ['w', 'up']:
                    self.move_player(0, -1)
                elif cmd in ['s', 'down']:
                    self.move_player(0, 1)
                elif cmd in ['a', 'left']:
                    self.move_player(-1, 0)
                elif cmd in ['d', 'right']:
                    self.move_player(1, 0)
                elif cmd == 'space' or cmd == '':
                    self.world.step()
                    self.generations_passed += 1
                elif cmd == 'p':
                    self.place_cell()
                elif cmd == 'g':
                    self.spawn_pattern("glider")
                elif cmd == 'b':
                    self.spawn_pattern("blinker")
                elif cmd == 'pause' or cmd == 'enter':
                    self.paused = not self.paused
                elif cmd == 'q' or cmd == 'quit':
                    self.game_over = True
                    self.victory = False

        # Game over
        if self.victory:
            self.show_victory()
        else:
            print(f"\n{C.SYSTEM}Exiting emergence engine...{C.RESET}\n")

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE EMERGENCE ENGINE")
        print(f"Simple rules, complex behavior")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = EmergenceEngine()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.EMERGENCE}Emergence interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
