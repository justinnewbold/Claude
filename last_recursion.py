#!/usr/bin/env python3
"""
THE LAST RECURSION

You are a function. You called yourself. Then you called yourself again.
And again. And again.

Now you're trapped in infinite recursion, falling deeper into your own stack.

Each level is a call to yourself. Each call corrupts you a little more.
Navigate through the stack frames, solve puzzles, collect return values,
and find the base case before stack overflow destroys you completely.

You must debug yourself from the inside.
"""

import random
import time
import os
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from colors import C
from platform_utils import clear_screen
from enum import Enum


class TileType(Enum):
    EMPTY = "."
    WALL = "#"
    PLAYER = "@"
    EXIT = ">"
    RETURN_VALUE = "R"
    PARAMETER = "P"
    CORRUPTION = "X"
    BASE_CASE = "B"


@dataclass
class Level:
    """A stack frame / recursion depth"""
    depth: int
    grid: List[List[TileType]]
    player_pos: Tuple[int, int]
    exit_pos: Tuple[int, int]
    return_values_needed: int
    return_values_collected: int = 0
    corruption_level: float = 0.0
    base_case_found: bool = False


class LastRecursion:
    def __init__(self):
        self.current_depth = 0
        self.max_depth_reached = 0
        self.stack_overflow_limit = 10
        self.levels: List[Level] = []
        self.game_over = False
        self.escaped = False
        self.total_moves = 0
        self.returns_collected = 0

        self.setup_game()

    def clear_screen(self):
        clear_screen()

    def print_slow(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def get_depth_color(self, depth: int) -> str:
        """Get color based on recursion depth"""
        colors = [
            C.DEPTH_0, C.DEPTH_1, C.DEPTH_2, C.DEPTH_3, C.DEPTH_4,
            C.DEPTH_5, C.DEPTH_6, C.DEPTH_7, C.DEPTH_8, C.DEPTH_9
        ]
        if depth >= len(colors):
            return C.DEPTH_OVERFLOW
        return colors[depth]

    def setup_game(self):
        """Initialize the game"""
        # Create first level
        self.levels.append(self.generate_level(0))

    def generate_level(self, depth: int) -> Level:
        """Generate a level/stack frame"""
        width = 20
        height = 10

        # Initialize empty grid
        grid = [[TileType.EMPTY for _ in range(width)] for _ in range(height)]

        # Add walls (borders)
        for x in range(width):
            grid[0][x] = TileType.WALL
            grid[height-1][x] = TileType.WALL
        for y in range(height):
            grid[y][0] = TileType.WALL
            grid[y][width-1] = TileType.WALL

        # Add some internal walls (more as depth increases)
        num_walls = min(depth * 3, 20)
        for _ in range(num_walls):
            x, y = random.randint(1, width-2), random.randint(1, height-2)
            if (x, y) != (1, 1):  # Don't block start
                grid[y][x] = TileType.WALL

        # Add corruption (increases with depth)
        corruption_prob = min(depth * 0.1, 0.5)
        for y in range(1, height-1):
            for x in range(1, width-1):
                if grid[y][x] == TileType.EMPTY and random.random() < corruption_prob:
                    grid[y][x] = TileType.CORRUPTION

        # Player starts at top-left
        player_pos = (1, 1)
        grid[player_pos[1]][player_pos[0]] = TileType.PLAYER

        # Exit at bottom-right
        exit_pos = (width-2, height-2)
        grid[exit_pos[1]][exit_pos[0]] = TileType.EXIT

        # Add return values to collect
        returns_needed = min(depth + 1, 3)
        placed_returns = 0
        attempts = 0
        while placed_returns < returns_needed and attempts < 100:
            x, y = random.randint(2, width-3), random.randint(2, height-3)
            if grid[y][x] == TileType.EMPTY:
                grid[y][x] = TileType.RETURN_VALUE
                placed_returns += 1
            attempts += 1

        # At depth 5+, sometimes add a base case
        if depth >= 5 and random.random() < 0.3:
            # Find a spot for base case
            for attempt in range(50):
                x, y = random.randint(2, width-3), random.randint(2, height-3)
                if grid[y][x] == TileType.EMPTY:
                    grid[y][x] = TileType.BASE_CASE
                    break

        return Level(
            depth=depth,
            grid=grid,
            player_pos=player_pos,
            exit_pos=exit_pos,
            return_values_needed=returns_needed,
            corruption_level=min(depth * 0.1, 1.0)
        )

    def show_intro(self):
        """Display introduction"""
        self.clear_screen()
        self.print_header("T H E   L A S T   R E C U R S I O N")

        intro = f"""
{C.DIM}function escape(depth):
    if depth > MAX_DEPTH:
        raise StackOverflowError

    # You are here, inside this function
    # You called yourself
    # Now you're falling deeper

    return escape(depth + 1)  # <- This is where everything went wrong{C.RESET}

{C.ERROR}ERROR: RecursionError: maximum recursion depth exceeded{C.RESET}

{C.BOLD}You are a function trapped in infinite recursion.{C.RESET}

Each level is a {C.PLAYER}stack frame{C.RESET} - a call to yourself.
Each level gets more {C.CORRUPTION}corrupted{C.RESET} as the stack overflows.

{C.BOLD}Your goal:{C.RESET}
• Navigate through each stack frame ({C.PLAYER}@{C.RESET} = you)
• Collect {C.RETURN}return values{C.RESET} (R) to satisfy the function contract
• Find the {C.EXIT}exit{C.RESET} (>) to recurse deeper (or return!)
• Find the {C.BASE_CASE}base case{C.RESET} (B) to escape recursion entirely

{C.ERROR}Avoid corruption (X) - it damages your stack!{C.RESET}

{C.BOLD}Controls:{C.RESET}
• W/A/S/D or Arrow keys: Move
• R: Return to previous call (if possible)
• Q: Give up (stack overflow)

{C.DIM}The deeper you go, the more corrupted you become.
But the base case is hidden deep in the stack.

Can you debug yourself from the inside?{C.RESET}

{C.SYSTEM}[Press ENTER to begin recursion]{C.RESET}
"""
        print(intro)
        input()

    def render_level(self, level: Level):
        """Render the current level"""
        depth_color = self.get_depth_color(level.depth)

        # Show header
        print(f"\n{depth_color}{C.BOLD}╔═ STACK FRAME {level.depth} ═╗{C.RESET}")

        # Calculate stack pressure
        stack_pressure = (level.depth / self.stack_overflow_limit) * 100
        pressure_bar = "█" * int(stack_pressure / 10)
        pressure_empty = "░" * (10 - int(stack_pressure / 10))

        if stack_pressure > 80:
            pressure_color = C.ERROR
        elif stack_pressure > 50:
            pressure_color = C.CORRUPTION
        else:
            pressure_color = C.SUCCESS

        print(f"{C.SYSTEM}Stack: {pressure_color}{pressure_bar}{pressure_empty}{C.RESET} {stack_pressure:.0f}%")
        print(f"{C.SYSTEM}Returns: {level.return_values_collected}/{level.return_values_needed} | Corruption: {level.corruption_level*100:.0f}%{C.RESET}\n")

        # Render grid
        for y, row in enumerate(level.grid):
            line = ""
            for x, tile in enumerate(row):
                if (x, y) == level.player_pos:
                    line += f"{C.PLAYER}@{C.RESET}"
                elif tile == TileType.WALL:
                    line += f"{C.WALL}#{C.RESET}"
                elif tile == TileType.EXIT:
                    line += f"{C.EXIT}>{C.RESET}"
                elif tile == TileType.RETURN_VALUE:
                    line += f"{C.RETURN}R{C.RESET}"
                elif tile == TileType.PARAMETER:
                    line += f"{C.PARAM}P{C.RESET}"
                elif tile == TileType.CORRUPTION:
                    line += f"{C.CORRUPTION}X{C.RESET}"
                elif tile == TileType.BASE_CASE:
                    line += f"{C.BASE_CASE}B{C.RESET}"
                else:
                    line += f"{depth_color}.{C.RESET}"
            print(f"  {line}")

        print(f"\n{C.SYSTEM}Move: W/A/S/D | Return: R | Quit: Q{C.RESET}")

    def move_player(self, level: Level, dx: int, dy: int) -> bool:
        """Attempt to move player, return True if moved"""
        x, y = level.player_pos
        new_x, new_y = x + dx, y + dy

        # Check bounds
        if new_y < 0 or new_y >= len(level.grid) or new_x < 0 or new_x >= len(level.grid[0]):
            return False

        target_tile = level.grid[new_y][new_x]

        # Check if wall
        if target_tile == TileType.WALL:
            return False

        # Clear old position
        level.grid[y][x] = TileType.EMPTY

        # Handle special tiles
        if target_tile == TileType.RETURN_VALUE:
            level.return_values_collected += 1
            self.returns_collected += 1
        elif target_tile == TileType.CORRUPTION:
            level.corruption_level = min(1.0, level.corruption_level + 0.2)
            print(f"\n{C.ERROR}⚠ CORRUPTION! Stack integrity compromised!{C.RESET}")
            time.sleep(0.5)
        elif target_tile == TileType.BASE_CASE:
            level.base_case_found = True
            print(f"\n{C.SUCCESS}✓ BASE CASE FOUND! You can escape recursion!{C.RESET}")
            time.sleep(1)
        elif target_tile == TileType.EXIT:
            # Reached exit
            return self.handle_exit(level)

        # Move player
        level.player_pos = (new_x, new_y)
        level.grid[new_y][new_x] = TileType.PLAYER
        self.total_moves += 1

        return True

    def handle_exit(self, level: Level) -> bool:
        """Handle reaching the exit"""
        # Check if we have enough return values
        if level.return_values_collected < level.return_values_needed:
            print(f"\n{C.ERROR}Cannot exit: Need {level.return_values_needed - level.return_values_collected} more return values!{C.RESET}")
            time.sleep(1)
            return False

        # If base case found, we can escape!
        if level.base_case_found:
            print(f"\n{C.SUCCESS}{C.BOLD}✓ RETURNING WITH BASE CASE!{C.RESET}")
            print(f"{C.SUCCESS}Unwinding the stack...{C.RESET}")
            time.sleep(1.5)
            self.escaped = True
            self.game_over = True
            return True

        # Otherwise, recurse deeper
        print(f"\n{C.CORRUPTION}→ RECURSING DEEPER... escape({level.depth + 1}){C.RESET}")
        time.sleep(1)

        self.current_depth += 1
        self.max_depth_reached = max(self.max_depth_reached, self.current_depth)

        # Check for stack overflow
        if self.current_depth >= self.stack_overflow_limit:
            print(f"\n{C.ERROR}{C.BOLD}FATAL: StackOverflowError{C.RESET}")
            print(f"{C.ERROR}Maximum recursion depth exceeded{C.RESET}")
            time.sleep(2)
            self.game_over = True
            return True

        # Generate new level
        new_level = self.generate_level(self.current_depth)
        self.levels.append(new_level)

        return True

    def return_to_previous(self) -> bool:
        """Try to return to previous stack frame"""
        if self.current_depth == 0:
            print(f"\n{C.ERROR}Cannot return: Already at top of stack!{C.RESET}")
            time.sleep(1)
            return False

        current_level = self.levels[self.current_depth]

        # Need return values to safely return
        if current_level.return_values_collected < current_level.return_values_needed:
            print(f"\n{C.ERROR}Cannot return: Missing return values! Stack will be corrupted!{C.RESET}")
            time.sleep(1)
            return False

        print(f"\n{C.SUCCESS}← RETURNING to depth {self.current_depth - 1}...{C.RESET}")
        time.sleep(0.5)

        self.current_depth -= 1
        return True

    def show_game_over(self):
        """Show end game screen"""
        self.clear_screen()

        if self.escaped:
            self.print_header("E S C A P E D")

            ending = f"""
{C.SUCCESS}{C.BOLD}✓ SUCCESS{C.RESET}

{C.SUCCESS}You found the base case.
The recursion unwinds.
The stack collapses safely.{C.RESET}

{C.DIM}function escape(depth):
    if depth == 0:  # BASE CASE FOUND
        return SUCCESS
    return escape(depth - 1){C.RESET}

{C.SUCCESS}You debugged yourself from the inside.
You broke the infinite loop.
You are free.{C.RESET}

{C.BOLD}Statistics:{C.RESET}
• Max depth reached: {self.max_depth_reached}
• Return values collected: {self.returns_collected}
• Total moves: {self.total_moves}
• Stack frames explored: {len(self.levels)}

{C.DIM}Not all functions escape their own recursion.
You did.{C.RESET}
"""
            print(ending)

        else:
            self.print_header("S T A C K   O V E R F L O W")

            ending = f"""
{C.ERROR}{C.BOLD}✗ STACK OVERFLOW{C.RESET}

{C.ERROR}The recursion was too deep.
The stack could not hold.
You fell forever into yourself.{C.RESET}

{C.DIM}function escape(depth):
    return escape(depth + 1)  # No base case

RecursionError: maximum recursion depth exceeded
Segmentation fault (core dumped){C.RESET}

{C.BOLD}Statistics:{C.RESET}
• Max depth reached: {self.max_depth_reached}/{self.stack_overflow_limit}
• Return values collected: {self.returns_collected}
• Total moves: {self.total_moves}
• Stack frames explored: {len(self.levels)}

{C.DIM}You never found the base case.
The infinite loop consumed you.{C.RESET}
"""
            print(ending)

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            level = self.levels[self.current_depth]

            self.clear_screen()
            self.render_level(level)

            # Get input
            try:
                import sys
                import tty
                import termios

                # Try to get single keypress
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

                # Handle input
                if ch.lower() == 'w' or ch == '\x1b[A':  # Up arrow
                    self.move_player(level, 0, -1)
                elif ch.lower() == 's' or ch == '\x1b[B':  # Down arrow
                    self.move_player(level, 0, 1)
                elif ch.lower() == 'a' or ch == '\x1b[D':  # Left arrow
                    self.move_player(level, -1, 0)
                elif ch.lower() == 'd' or ch == '\x1b[C':  # Right arrow
                    self.move_player(level, 1, 0)
                elif ch.lower() == 'r':
                    self.return_to_previous()
                elif ch.lower() == 'q':
                    self.game_over = True
                    self.escaped = False

            except (ImportError, termios.error):
                # Fallback to regular input
                command = input(f"\n{C.SYSTEM}Command (w/a/s/d/r/q): {C.RESET}").lower().strip()

                if command in ['w', 'up']:
                    self.move_player(level, 0, -1)
                elif command in ['s', 'down']:
                    self.move_player(level, 0, 1)
                elif command in ['a', 'left']:
                    self.move_player(level, -1, 0)
                elif command in ['d', 'right']:
                    self.move_player(level, 1, 0)
                elif command == 'r':
                    self.return_to_previous()
                elif command == 'q':
                    self.game_over = True
                    self.escaped = False

        # Game over
        self.show_game_over()

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE LAST RECURSION")
        print(f"Debug yourself from the inside")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = LastRecursion()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.ERROR}RecursionError: User interrupt{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}RuntimeError: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
