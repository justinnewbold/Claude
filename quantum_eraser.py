#!/usr/bin/env python3
"""
QUANTUM ERASER

Your future choices change the past.

Based on the delayed-choice quantum eraser experiment:
Measurements made LATER determine what happened EARLIER.

Navigate mazes where causality runs backwards.
Your destination determines your path.
The future creates the past.

This is retrocausality made playable.
"""

import os
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from colors import C
from platform_utils import clear_screen
from enum import Enum


class CellType(Enum):
    EMPTY = "."
    WALL = "#"
    PLAYER = "@"
    GOAL = "G"
    DETECTOR_A = "A"  # Measures path A
    DETECTOR_B = "B"  # Measures path B
    ERASER = "E"      # Erases which-path info


@dataclass
class QuantumPath:
    """A path in superposition"""
    positions: List[Tuple[int, int]]
    measured: bool = False
    erased: bool = False
    path_type: Optional[str] = None  # 'A' or 'B'


@dataclass
class Level:
    """A puzzle level"""
    width: int
    height: int
    grid: List[List[CellType]]
    start: Tuple[int, int]
    goal: Tuple[int, int]
    detectors: List[Tuple[int, int, str]]  # x, y, type
    erasers: List[Tuple[int, int]]
    player_pos: Tuple[int, int] = None
    paths: List[QuantumPath] = field(default_factory=list)
    current_path: List[Tuple[int, int]] = field(default_factory=list)
    moves: int = 0


class QuantumEraser:
    def __init__(self):
        self.level_num = 1
        self.game_over = False
        self.victory = False
        self.level: Optional[Level] = None
        self.in_replay = False
        self.replay_history: List[Tuple[int, int]] = []

        self.setup_level(1)

    def clear_screen(self):
        clear_screen()

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_level(self, level_num: int):
        """Setup a specific level"""

        if level_num == 1:
            # Tutorial: Simple path with one detector
            width, height = 15, 10
            grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls
            for x in range(width):
                grid[0][x] = CellType.WALL
                grid[height-1][x] = CellType.WALL
            for y in range(height):
                grid[y][0] = CellType.WALL
                grid[y][width-1] = CellType.WALL

            # Start and goal
            start = (2, 5)
            goal = (12, 5)
            grid[goal[1]][goal[0]] = CellType.GOAL

            # Detector A
            grid[5][7] = CellType.DETECTOR_A
            detectors = [(7, 5, 'A')]

            erasers = []

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                start=start,
                goal=goal,
                detectors=detectors,
                erasers=erasers,
                player_pos=start
            )

        elif level_num == 2:
            # Two paths, choose which to take
            width, height = 20, 12
            grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls
            for x in range(width):
                grid[0][x] = CellType.WALL
                grid[height-1][x] = CellType.WALL
            for y in range(height):
                grid[y][0] = CellType.WALL
                grid[y][width-1] = CellType.WALL

            # Center wall creating two paths
            for y in range(3, 9):
                grid[y][10] = CellType.WALL

            start = (2, 6)
            goal = (17, 6)
            grid[goal[1]][goal[0]] = CellType.GOAL

            # Detectors on each path
            grid[6][5] = CellType.DETECTOR_A
            grid[6][15] = CellType.DETECTOR_B
            detectors = [(5, 6, 'A'), (15, 6, 'B')]

            erasers = []

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                start=start,
                goal=goal,
                detectors=detectors,
                erasers=erasers,
                player_pos=start
            )

        elif level_num == 3:
            # Eraser level - erase which-path information
            width, height = 25, 12
            grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls
            for x in range(width):
                grid[0][x] = CellType.WALL
                grid[height-1][x] = CellType.WALL
            for y in range(height):
                grid[y][0] = CellType.WALL
                grid[y][width-1] = CellType.WALL

            # Complex paths
            for y in range(3, 9):
                grid[y][8] = CellType.WALL
                grid[y][16] = CellType.WALL

            start = (2, 6)
            goal = (22, 6)
            grid[goal[1]][goal[0]] = CellType.GOAL

            # Detectors
            grid[6][12] = CellType.DETECTOR_A
            detectors = [(12, 6, 'A')]

            # Eraser
            grid[6][20] = CellType.ERASER
            erasers = [(20, 6)]

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                start=start,
                goal=goal,
                detectors=detectors,
                erasers=erasers,
                player_pos=start
            )

        else:
            # Victory!
            self.victory = True
            self.game_over = True

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("Q U A N T U M   E R A S E R")

        intro = f"""
{C.QUANTUM}\"The future determines the past.\"{C.RESET}

{C.DIM}In 1999, physicists performed the delayed-choice quantum eraser experiment.

The result: Measurements made AFTER a particle passed through slits
retroactively determined WHICH slit it went through.

The future changed the past.{C.RESET}

{C.BOLD}How It Works:{C.RESET}

• Navigate from start (@) to goal (G)
• You move in SUPERPOSITION - all possible paths at once
• Detectors (A/B) measure which path you took
• Erasers (E) delete which-path information
• Your FUTURE choices determine your PAST path

{C.BOLD}The Paradox:{C.RESET}

When you reach a detector:
  - Your path RETROACTIVELY becomes definite
  - You were "always" on that path
  - But you weren't until you measured it

When you reach an eraser:
  - Which-path info is destroyed
  - You're back in superposition
  - The past becomes uncertain again

{C.BOLD}Symbols:{C.RESET}

{C.PLAYER}@{C.RESET} = You (in superposition)
{C.GOAL}G{C.RESET} = Goal
{C.DETECTOR}A/B{C.RESET} = Detectors (measure which path)
{C.ERASED}E{C.RESET} = Eraser (delete path info)
{C.WALL}#{C.RESET} = Wall

{C.BOLD}Controls:{C.RESET}

W/A/S/D - Move
R - Reset level
Q - Quit

{C.QUANTUM}Causality runs backwards here.
Your future creates your past.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def render_level(self):
        """Render the current level"""
        print(f"\n{C.QUANTUM}╔═ QUANTUM ERASER ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level_num} | Moves: {self.level.moves}{C.RESET}")

        # Show quantum state
        if self.level.current_path:
            measured = any(self.is_detector(pos) for pos in self.level.current_path)
            erased = any(self.is_eraser(pos) for pos in self.level.current_path)

            if erased:
                print(f"{C.ERASED}State: Superposition (erased){C.RESET}")
            elif measured:
                print(f"{C.MEASURED}State: Definite path{C.RESET}")
            else:
                print(f"{C.SUPERPOSED}State: Superposition{C.RESET}")
        else:
            print(f"{C.SUPERPOSED}State: Superposition{C.RESET}")

        print()

        # Render grid
        for y in range(self.level.height):
            line = "  "
            for x in range(self.level.width):
                pos = (x, y)

                if pos == self.level.player_pos:
                    line += f"{C.PLAYER}@{C.RESET}"
                elif pos in self.level.current_path:
                    line += f"{C.SUPERPOSED}·{C.RESET}"
                elif self.level.grid[y][x] == CellType.WALL:
                    line += f"{C.WALL}█{C.RESET}"
                elif self.level.grid[y][x] == CellType.GOAL:
                    line += f"{C.GOAL}G{C.RESET}"
                elif self.level.grid[y][x] == CellType.DETECTOR_A:
                    line += f"{C.DETECTOR}A{C.RESET}"
                elif self.level.grid[y][x] == CellType.DETECTOR_B:
                    line += f"{C.DETECTOR}B{C.RESET}"
                elif self.level.grid[y][x] == CellType.ERASER:
                    line += f"{C.ERASED}E{C.RESET}"
                else:
                    line += f"{C.DIM}·{C.RESET}"
            print(line)

        print(f"\n{C.SYSTEM}Move: W/A/S/D | Reset: R | Quit: Q{C.RESET}")

    def is_detector(self, pos: Tuple[int, int]) -> bool:
        """Check if position is a detector"""
        return any(det[0:2] == pos for det in self.level.detectors)

    def is_eraser(self, pos: Tuple[int, int]) -> bool:
        """Check if position is an eraser"""
        return pos in self.level.erasers

    def move_player(self, dx: int, dy: int):
        """Move player"""
        px, py = self.level.player_pos
        new_x, new_y = px + dx, py + dy

        # Check bounds and walls
        if not (0 <= new_x < self.level.width and 0 <= new_y < self.level.height):
            return

        if self.level.grid[new_y][new_x] == CellType.WALL:
            return

        # Move
        self.level.player_pos = (new_x, new_y)
        self.level.current_path.append((new_x, new_y))
        self.level.moves += 1

        # Check for goal
        if (new_x, new_y) == self.level.goal:
            self.show_victory_screen()

    def show_victory_screen(self):
        """Show level complete"""
        self.clear_screen()
        print(f"\n{C.SUCCESS}╔═ LEVEL COMPLETE! ═╗{C.RESET}\n")
        print(f"{C.SYSTEM}Completed in {self.level.moves} moves{C.RESET}")

        # Analyze path
        passed_detector = any(self.is_detector(pos) for pos in self.level.current_path)
        passed_eraser = any(self.is_eraser(pos) for pos in self.level.current_path)

        if passed_eraser:
            print(f"\n{C.ERASED}You erased which-path information.{C.RESET}")
            print(f"{C.QUANTUM}Your path remained in superposition.{C.RESET}")
        elif passed_detector:
            print(f"\n{C.MEASURED}You were measured by a detector.{C.RESET}")
            print(f"{C.QUANTUM}Your path retroactively became definite.{C.RESET}")
        else:
            print(f"\n{C.SUPERPOSED}You remained in superposition.{C.RESET}")

        print(f"\n{C.SYSTEM}[Press N for next level, or ENTER to continue]{C.RESET}")

        try:
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

            if ch.lower() == 'n':
                self.level_num += 1
                self.setup_level(self.level_num)
        except (ImportError, AttributeError, OSError):
            cmd = input().strip().lower()
            if cmd == 'n':
                self.level_num += 1
                self.setup_level(self.level_num)

    def show_final_victory(self):
        """Show final victory"""
        self.clear_screen()
        self.print_header("R E T R O C A U S A L I T Y   M A S T E R E D")

        victory = f"""
{C.SUCCESS}You've mastered backward causality!{C.RESET}

{C.DIM}The delayed-choice quantum eraser shows:

• The future can determine the past
• Measurement creates reality retroactively
• Which-path information can be erased
• Causality is more flexible than we thought{C.RESET}

{C.BOLD}The Real Experiment:{C.RESET}

In 1999, Yoon-Ho Kim et al. performed this experiment:
- Photons passed through double slits
- Which-path detectors were placed AFTER the slits
- Erasers could delete which-path info
- Results: Future measurements determined past behavior

{C.QUANTUM}The future literally changed the past.{C.RESET}

{C.BOLD}Implications:{C.RESET}

• Time is not necessarily one-directional
• Causality is contextual
• The universe is deeply strange
• Measurement is creative, not just observational

{C.DIM}You navigated paradoxes of time and causality.
You experienced retrocausality.
The future shaped the past.{C.RESET}
"""
        print(victory)

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            self.clear_screen()
            self.render_level()

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
                elif ch.lower() == 'r':
                    self.setup_level(self.level_num)
                elif ch.lower() == 'q':
                    self.game_over = True

            except (ImportError, AttributeError, OSError):
                cmd = input(f"\n{C.SYSTEM}Command: {C.RESET}").lower().strip()

                if cmd in ['w', 'up']:
                    self.move_player(0, -1)
                elif cmd in ['s', 'down']:
                    self.move_player(0, 1)
                elif cmd in ['a', 'left']:
                    self.move_player(-1, 0)
                elif cmd in ['d', 'right']:
                    self.move_player(1, 0)
                elif cmd == 'r' or cmd == 'reset':
                    self.setup_level(self.level_num)
                elif cmd == 'q' or cmd == 'quit':
                    self.game_over = True

        # Show ending
        if self.victory:
            self.show_final_victory()
        else:
            print(f"\n{C.SYSTEM}Exiting quantum realm...{C.RESET}\n")

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"QUANTUM ERASER")
        print(f"The future determines the past")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = QuantumEraser()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.QUANTUM}Causality interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
