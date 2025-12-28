#!/usr/bin/env python3
"""
ENTANGLEMENT

Quantum entangled puzzle blocks.
When you move one, the other moves too.
Spooky action at a distance, made playable.

In quantum mechanics, entanglement is when particles become correlated
such that measuring one instantly affects the other, regardless of distance.

In this puzzle game, blocks are quantum entangled.
Push one, its partner moves.
Rotate one, its partner rotates.
Navigate them both to goals simultaneously.

This is quantum correlation as a puzzle mechanic.
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
from colors import C
from platform_utils import clear_screen


class BlockType(Enum):
    EMPTY = "."
    WALL = "#"
    PLAYER = "@"
    GOAL = "O"
    BLOCK_A = "A"  # Cyan entangled pair
    BLOCK_B = "B"  # Magenta entangled pair
    BLOCK_C = "C"  # Yellow entangled pair
    BLOCK_D = "D"  # Green entangled pair


@dataclass
class Block:
    """An entangled block"""
    block_type: BlockType
    position: Tuple[int, int]
    entangled_with: Optional['Block'] = None


@dataclass
class Level:
    """A puzzle level"""
    width: int
    height: int
    grid: List[List[BlockType]]
    player_pos: Tuple[int, int]
    blocks: List[Block] = field(default_factory=list)
    goals: Set[Tuple[int, int]] = field(default_factory=set)
    moves: int = 0


class Entanglement:
    def __init__(self):
        self.level_num = 1
        self.game_over = False
        self.victory = False
        self.level: Optional[Level] = None

        self.setup_level(1)

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_level(self, level_num: int):
        """Setup a specific level"""

        if level_num == 1:
            # Tutorial: Two entangled blocks, simple push
            width, height = 20, 10
            grid = [[BlockType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls
            for x in range(width):
                grid[0][x] = BlockType.WALL
                grid[height-1][x] = BlockType.WALL
            for y in range(height):
                grid[y][0] = BlockType.WALL
                grid[y][width-1] = BlockType.WALL

            # Player
            player_pos = (2, 5)

            # Entangled pair A
            block1 = Block(BlockType.BLOCK_A, (5, 5))
            block2 = Block(BlockType.BLOCK_A, (10, 5))
            block1.entangled_with = block2
            block2.entangled_with = block1

            blocks = [block1, block2]

            # Goals
            goals = {(15, 5), (15, 4)}

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                player_pos=player_pos,
                blocks=blocks,
                goals=goals
            )

        elif level_num == 2:
            # Two pairs, more complex
            width, height = 20, 12
            grid = [[BlockType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls
            for x in range(width):
                grid[0][x] = BlockType.WALL
                grid[height-1][x] = BlockType.WALL
            for y in range(height):
                grid[y][0] = BlockType.WALL
                grid[y][width-1] = BlockType.WALL

            # Add divider
            for y in range(3, 9):
                grid[y][10] = BlockType.WALL

            player_pos = (2, 6)

            # Pair A - left side
            block1 = Block(BlockType.BLOCK_A, (3, 6))
            block2 = Block(BlockType.BLOCK_A, (7, 6))
            block1.entangled_with = block2
            block2.entangled_with = block1

            # Pair B - crosses divider
            block3 = Block(BlockType.BLOCK_B, (8, 4))
            block4 = Block(BlockType.BLOCK_B, (12, 8))
            block3.entangled_with = block4
            block4.entangled_with = block3

            blocks = [block1, block2, block3, block4]
            goals = {(15, 6), (15, 7), (5, 3), (5, 4)}

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                player_pos=player_pos,
                blocks=blocks,
                goals=goals
            )

        elif level_num == 3:
            # Chain reaction: A→B→C
            width, height = 25, 10
            grid = [[BlockType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls
            for x in range(width):
                grid[0][x] = BlockType.WALL
                grid[height-1][x] = BlockType.WALL
            for y in range(height):
                grid[y][0] = BlockType.WALL
                grid[y][width-1] = BlockType.WALL

            player_pos = (2, 5)

            # Three pairs in sequence
            block1 = Block(BlockType.BLOCK_A, (5, 5))
            block2 = Block(BlockType.BLOCK_A, (10, 5))
            block1.entangled_with = block2
            block2.entangled_with = block1

            block3 = Block(BlockType.BLOCK_B, (11, 5))
            block4 = Block(BlockType.BLOCK_B, (16, 5))
            block3.entangled_with = block4
            block4.entangled_with = block3

            block5 = Block(BlockType.BLOCK_C, (17, 5))
            block6 = Block(BlockType.BLOCK_C, (22, 5))
            block5.entangled_with = block6
            block6.entangled_with = block5

            blocks = [block1, block2, block3, block4, block5, block6]
            goals = {(22, 3), (22, 4), (22, 5), (22, 6), (22, 7), (22, 8)}

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                player_pos=player_pos,
                blocks=blocks,
                goals=goals
            )

        elif level_num == 4:
            # Complex maze
            width, height = 22, 14
            grid = [[BlockType.EMPTY for _ in range(width)] for _ in range(height)]

            # Walls - create maze
            for x in range(width):
                grid[0][x] = BlockType.WALL
                grid[height-1][x] = BlockType.WALL
            for y in range(height):
                grid[y][0] = BlockType.WALL
                grid[y][width-1] = BlockType.WALL

            # Internal walls
            for y in range(2, 8):
                grid[y][7] = BlockType.WALL
            for y in range(6, 12):
                grid[y][14] = BlockType.WALL
            for x in range(7, 14):
                grid[6][x] = BlockType.WALL

            player_pos = (2, 7)

            # Multiple entangled pairs
            block1 = Block(BlockType.BLOCK_A, (4, 4))
            block2 = Block(BlockType.BLOCK_A, (10, 10))
            block1.entangled_with = block2
            block2.entangled_with = block1

            block3 = Block(BlockType.BLOCK_B, (11, 4))
            block4 = Block(BlockType.BLOCK_B, (17, 10))
            block3.entangled_with = block4
            block4.entangled_with = block3

            blocks = [block1, block2, block3, block4]
            goals = {(18, 3), (18, 4), (18, 10), (18, 11)}

            self.level = Level(
                width=width,
                height=height,
                grid=grid,
                player_pos=player_pos,
                blocks=blocks,
                goals=goals
            )

        else:
            # Victory!
            self.victory = True
            self.game_over = True

    def get_block_at(self, x: int, y: int) -> Optional[Block]:
        """Get block at position"""
        for block in self.level.blocks:
            if block.position == (x, y):
                return block
        return None

    def get_block_color(self, block_type: BlockType) -> str:
        """Get color for block type"""
        if block_type == BlockType.BLOCK_A:
            return C.PAIR_A
        elif block_type == BlockType.BLOCK_B:
            return C.PAIR_B
        elif block_type == BlockType.BLOCK_C:
            return C.PAIR_C
        elif block_type == BlockType.BLOCK_D:
            return C.PAIR_D
        return C.RESET

    def is_position_free(self, x: int, y: int) -> bool:
        """Check if position is empty"""
        if not (0 <= x < self.level.width and 0 <= y < self.level.height):
            return False

        if self.level.grid[y][x] == BlockType.WALL:
            return False

        if self.get_block_at(x, y):
            return False

        return True

    def push_block(self, block: Block, dx: int, dy: int) -> bool:
        """Push a block and its entangled partner"""
        x, y = block.position
        new_x, new_y = x + dx, y + dy

        # Check if new position is free
        if not self.is_position_free(new_x, new_y):
            return False

        # If entangled, check if partner can also move
        if block.entangled_with:
            partner = block.entangled_with
            px, py = partner.position
            partner_new_x, partner_new_y = px + dx, py + dy

            if not self.is_position_free(partner_new_x, partner_new_y):
                return False

            # Both can move - move partner first
            partner.position = (partner_new_x, partner_new_y)

        # Move this block
        block.position = (new_x, new_y)
        return True

    def move_player(self, dx: int, dy: int):
        """Move player and potentially push blocks"""
        px, py = self.level.player_pos
        new_x, new_y = px + dx, py + dy

        # Check bounds
        if not (0 <= new_x < self.level.width and 0 <= new_y < self.level.height):
            return

        # Check wall
        if self.level.grid[new_y][new_x] == BlockType.WALL:
            return

        # Check if pushing a block
        block_at_new = self.get_block_at(new_x, new_y)
        if block_at_new:
            # Try to push the block
            if self.push_block(block_at_new, dx, dy):
                self.level.player_pos = (new_x, new_y)
                self.level.moves += 1
        else:
            # Just move
            self.level.player_pos = (new_x, new_y)
            self.level.moves += 1

    def check_victory(self) -> bool:
        """Check if all goals are covered by blocks"""
        for goal in self.level.goals:
            if not self.get_block_at(*goal):
                return False
        return True

    def render_level(self):
        """Render the current level"""
        print(f"\n{C.QUANTUM}╔═ ENTANGLEMENT ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level_num} | Moves: {self.level.moves}{C.RESET}")
        print(f"{C.SYSTEM}Goals remaining: {len(self.level.goals) - sum(1 for g in self.level.goals if self.get_block_at(*g))}{C.RESET}\n")

        for y in range(self.level.height):
            line = "  "
            for x in range(self.level.width):
                pos = (x, y)

                # Check what's at this position
                if pos == self.level.player_pos:
                    line += f"{C.PLAYER}@{C.RESET}"
                elif pos in self.level.goals:
                    block = self.get_block_at(x, y)
                    if block:
                        color = self.get_block_color(block.block_type)
                        line += f"{color}{C.BOLD}◆{C.RESET}"  # Block on goal
                    else:
                        line += f"{C.GOAL}○{C.RESET}"  # Empty goal
                elif self.level.grid[y][x] == BlockType.WALL:
                    line += f"{C.WALL}█{C.RESET}"
                else:
                    block = self.get_block_at(x, y)
                    if block:
                        color = self.get_block_color(block.block_type)
                        line += f"{color}■{C.RESET}"
                    else:
                        line += f"{C.DIM}·{C.RESET}"

            print(line)

        # Show entanglement pairs
        print(f"\n{C.BOLD}Entangled Pairs:{C.RESET}")
        seen = set()
        for block in self.level.blocks:
            if block not in seen and block.entangled_with:
                partner = block.entangled_with
                seen.add(block)
                seen.add(partner)

                color = self.get_block_color(block.block_type)
                x1, y1 = block.position
                x2, y2 = partner.position
                print(f"  {color}■{C.RESET} ({x1},{y1}) {C.LINK}⟷{C.RESET} {color}■{C.RESET} ({x2},{y2})")

        print(f"\n{C.SYSTEM}Move: W/A/S/D | Reset: R | Quit: Q{C.RESET}")

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("E N T A N G L E M E N T")

        intro = f"""
{C.QUANTUM}\"Spooky action at a distance.\"{C.RESET}

— Einstein's description of quantum entanglement

{C.DIM}In quantum mechanics, entanglement is when particles become
correlated such that measuring one instantly affects the other,
regardless of the distance between them.

In this puzzle game, blocks are quantum entangled.{C.RESET}

{C.BOLD}How It Works:{C.RESET}

When two blocks are entangled:
• Push one block → Its partner moves the same direction
• Both blocks move simultaneously
• Distance doesn't matter (spooky!)
• They're quantum-correlated

{C.BOLD}Symbols:{C.RESET}

{C.PLAYER}@{C.RESET} = You (the player)
{C.WALL}█{C.RESET} = Wall (immovable)
{C.GOAL}○{C.RESET} = Goal (target position)
{C.PAIR_A}■{C.RESET} = Entangled block (cyan pair)
{C.PAIR_B}■{C.RESET} = Entangled block (magenta pair)
{C.PAIR_C}■{C.RESET} = Entangled block (yellow pair)
{C.LINK}⟷{C.RESET} = Entanglement link

{C.BOLD}Objective:{C.RESET}

Get all blocks onto goal positions {C.GOAL}○{C.RESET}
When successful, they show as: {C.PAIR_A}{C.BOLD}◆{C.RESET}

{C.BOLD}Controls:{C.RESET}

{C.SYSTEM}Movement:{C.RESET}
  W - Move up
  A - Move left
  S - Move down
  D - Move right

{C.SYSTEM}Other:{C.RESET}
  R - Reset level
  Q - Quit

{C.QUANTUM}When you push an entangled block,
both blocks move simultaneously.
This is quantum correlation.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def show_victory_screen(self):
        """Show level complete screen"""
        self.clear_screen()
        print(f"\n{C.SUCCESS}╔═ LEVEL COMPLETE! ═╗{C.RESET}\n")
        print(f"{C.SYSTEM}Level {self.level_num} completed in {self.level.moves} moves!{C.RESET}")
        print(f"\n{C.QUANTUM}All blocks entangled with their goals.{C.RESET}")
        print(f"\n{C.SYSTEM}[Press N for next level, or any key to continue]{C.RESET}")

    def show_final_victory(self):
        """Show final victory screen"""
        self.clear_screen()
        self.print_header("Q U A N T U M   M A S T E R Y")

        victory = f"""
{C.SUCCESS}You've mastered quantum entanglement!{C.RESET}

{C.DIM}Through gameplay, you experienced:

• Quantum correlation - entangled particles affecting each other
• Action at a distance - no physical connection needed
• Synchronized state - moving together instantly
• The paradox Einstein called \"spooky\"{C.RESET}

{C.BOLD}Real Quantum Entanglement:{C.RESET}

{C.QUANTUM}EPR Paradox (1935):{C.RESET}
Einstein, Podolsky, and Rosen questioned whether entanglement
meant faster-than-light communication. It doesn't - but the
correlation IS instant, which troubled Einstein.

{C.QUANTUM}Bell's Theorem (1964):{C.RESET}
John Stewart Bell proved that entanglement is real, not just
hidden variables. The universe genuinely has \"spooky action.\"

{C.QUANTUM}Modern Applications:{C.RESET}
• Quantum computing - entangled qubits for computation
• Quantum cryptography - unbreakable encryption
• Quantum teleportation - transferring quantum states
• Quantum sensing - ultra-precise measurements

{C.BOLD}What You Learned:{C.RESET}

{C.LINK}Correlation:{C.RESET} How particles share states
{C.LINK}Simultaneity:{C.RESET} Instant effects across distance
{C.LINK}Coordination:{C.RESET} Managing multiple entangled systems
{C.LINK}Quantum logic:{C.RESET} Thinking in correlated pairs

{C.QUANTUM}\"The world is not made of stuff,
but of correlations between stuff.\"{C.RESET}

{C.DIM}You navigated those correlations.
You manipulated entanglement.
You are quantum-aware.{C.RESET}
"""
        print(victory)

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            self.clear_screen()
            self.render_level()

            # Check victory
            if self.check_victory():
                self.show_victory_screen()

                # Get input for next level
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
                        continue
                    elif ch.lower() == 'q':
                        self.game_over = True
                        continue
                except (ImportError, termios.error):
                    cmd = input().strip().lower()
                    if cmd == 'n':
                        self.level_num += 1
                        self.setup_level(self.level_num)
                        continue
                    elif cmd == 'q':
                        self.game_over = True
                        continue

            # Get movement input
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
                    self.victory = False

            except (ImportError, termios.error):
                # Fallback
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
                    self.victory = False

        # Game over
        if self.victory:
            self.show_final_victory()
        else:
            print(f"\n{C.SYSTEM}Exiting quantum realm...{C.RESET}\n")

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"ENTANGLEMENT")
        print(f"Spooky action at a distance")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = Entanglement()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.QUANTUM}Correlation broken{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
