#!/usr/bin/env python3
"""
GÖDEL'S PARADOX

Some puzzles cannot be solved within the system.
You must step outside to complete them.

Based on Gödel's Incompleteness Theorems:
Any sufficiently complex formal system contains
statements that are true but unprovable within that system.

This game IS its own formal system.
And it is incomplete.
"""

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from colors import C
from platform_utils import clear_screen
from enum import Enum


class RuleType(Enum):
    MOVE = "move"
    TRANSFORM = "transform"
    CREATE = "create"
    DELETE = "delete"

@dataclass
class Rule:
    name: str
    rule_type: RuleType
    description: str
    can_use: bool = True

@dataclass
class Puzzle:
    description: str
    goal: str
    rules: List[Rule]
    solvable_in_system: bool
    meta_hint: str
    level: int

class GodelsParadox:
    def __init__(self):
        self.level = 1
        self.game_over = False
        self.victory = False
        self.meta_awareness = 0
        self.puzzles_solved = 0
        
    def clear_screen(self):
        clear_screen()
        
    def show_intro(self):
        self.clear_screen()
        title = "GÖDEL'S PARADOX"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.PARADOX}"This statement is unprovable."{C.RESET}

{C.DIM}In 1931, Kurt Gödel proved that mathematics is incomplete.
Any formal system complex enough for arithmetic contains
true statements that cannot be proven within that system.{C.RESET}

{C.BOLD}In this game:{C.RESET}
• Each puzzle has formal RULES you must follow
• Some puzzles are SOLVABLE using the rules
• Some puzzles are UNPROVABLE - you must step outside
• Breaking the 4th wall unlocks META-solutions

{C.BOLD}Controls:{C.RESET}
S - Attempt to solve using system rules
M - Try META-solution (step outside the system)
Q - Quit

{C.META}To solve the unsolvable, you must become aware
that you are IN a formal system.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
""")
        input()
        
    def create_puzzle(self, level: int) -> Puzzle:
        if level == 1:
            return Puzzle(
                description="Move object A to position B",
                goal="Object reaches B",
                rules=[
                    Rule("Move Right", RuleType.MOVE, "Can move 1 space right"),
                    Rule("Move Left", RuleType.MOVE, "Can move 1 space left")
                ],
                solvable_in_system=True,
                meta_hint="This one follows the rules.",
                level=1
            )
        elif level == 2:
            return Puzzle(
                description="You must move object to position C, but C is 10 spaces away",
                goal="Reach C in 10 moves",
                rules=[
                    Rule("Move", RuleType.MOVE, "Can only move 1 space per turn"),
                ],
                solvable_in_system=True,
                meta_hint="Count your moves carefully.",
                level=2
            )
        elif level == 3:
            return Puzzle(
                description="Create a new object at position X",
                goal="Object exists at X",
                rules=[
                    Rule("Move", RuleType.MOVE, "Can move objects"),
                    Rule("Delete", RuleType.DELETE, "Can delete objects")
                ],
                solvable_in_system=False,
                meta_hint="You need CREATE, but the rules don't allow it...",
                level=3
            )
        elif level == 4:
            return Puzzle(
                description="This puzzle requires you to do the impossible",
                goal="Solve the unsolvable",
                rules=[
                    Rule("Rule 1", RuleType.MOVE, "You cannot win"),
                    Rule("Rule 2", RuleType.TRANSFORM, "The rules cannot be broken")
                ],
                solvable_in_system=False,
                meta_hint="The game itself must be questioned.",
                level=4
            )
        else:
            self.victory = True
            self.game_over = True
            return None
            
    def show_puzzle(self, puzzle: Puzzle):
        self.clear_screen()
        print(f"\n{C.PARADOX}╔═ PUZZLE {puzzle.level} ═╗{C.RESET}")
        print(f"{C.SYSTEM}Meta-Awareness: {self.meta_awareness}{C.RESET}\n")
        
        print(f"{C.BOLD}PUZZLE:{C.RESET}")
        print(f"{puzzle.description}\n")
        
        print(f"{C.BOLD}GOAL:{C.RESET}")
        print(f"{puzzle.goal}\n")
        
        print(f"{C.BOLD}AVAILABLE RULES:{C.RESET}")
        for rule in puzzle.rules:
            print(f"  • {C.AXIOM}{rule.name}{C.RESET}: {rule.description}")
            
        if not puzzle.solvable_in_system:
            print(f"\n{C.DIM}Something feels wrong about this puzzle...{C.RESET}")
            
    def solve_puzzle(self, puzzle: Puzzle, meta: bool = False):
        self.clear_screen()
        
        if puzzle.solvable_in_system and not meta:
            print(f"\n{C.SUCCESS}✓ SOLVED using system rules!{C.RESET}\n")
            print(f"{C.PROOF}The puzzle was provable within the formal system.{C.RESET}")
            self.puzzles_solved += 1
            input(f"\n{C.SYSTEM}[Press ENTER]{C.RESET}")
            return True
            
        elif not puzzle.solvable_in_system and meta:
            print(f"\n{C.META}✓ META-SOLVED by stepping outside!{C.RESET}\n")
            print(f"{C.PARADOX}This puzzle was UNPROVABLE within the system's rules.{C.RESET}")
            print(f"{C.META}You recognized the incompleteness and transcended it.{C.RESET}")
            self.meta_awareness += 1
            self.puzzles_solved += 1
            input(f"\n{C.SYSTEM}[Press ENTER]{C.RESET}")
            return True
            
        elif not puzzle.solvable_in_system and not meta:
            print(f"\n{C.ERROR}✗ IMPOSSIBLE{C.RESET}\n")
            print(f"This puzzle cannot be solved using the given rules.")
            print(f"{C.DIM}Hint: {puzzle.meta_hint}{C.RESET}")
            input(f"\n{C.SYSTEM}[Press ENTER]{C.RESET}")
            return False
            
        else:  # solvable but using meta
            print(f"\n{C.SYSTEM}You used META-solution on a normal puzzle.{C.RESET}")
            print(f"It worked, but wasn't necessary.")
            self.puzzles_solved += 1
            input(f"\n{C.SYSTEM}[Press ENTER]{C.RESET}")
            return True
            
    def show_ending(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'INCOMPLETENESS UNDERSTOOD'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SUCCESS}You've experienced Gödel's revelation!{C.RESET}

{C.BOLD}Your Stats:{C.RESET}
Puzzles Solved: {self.puzzles_solved}
Meta-Awareness Gained: {self.meta_awareness}

{C.DIM}Gödel's Incompleteness Theorems (1931):{C.RESET}

{C.PARADOX}First Theorem:{C.RESET}
Any consistent formal system F that can express arithmetic
contains true statements that cannot be proven within F.

{C.PARADOX}Second Theorem:{C.RESET}
No consistent formal system can prove its own consistency.

{C.META}What this means:{C.RESET}
• Mathematics is incomplete (has unprovable truths)
• No system can fully validate itself
• There are limits to formal reasoning
• Some truths require stepping outside the system

{C.DIM}You experienced this by:
- Solving normal puzzles within the rules
- Recognizing impossible puzzles
- Stepping outside the system to meta-solve

This is self-awareness of formal limitations.
This is Gödel's gift to humanity.{C.RESET}
""")
        
    def play(self):
        self.show_intro()
        
        while not self.game_over:
            puzzle = self.create_puzzle(self.level)
            if puzzle is None:
                break
                
            self.show_puzzle(puzzle)
            
            print(f"\n{C.SYSTEM}Solve: [S]ystem | [M]eta | [Q]uit: {C.RESET}", end='')
            choice = input().strip().upper()
            
            if choice == 'Q':
                self.game_over = True
                continue
            elif choice == 'S':
                if self.solve_puzzle(puzzle, meta=False):
                    self.level += 1
            elif choice == 'M':
                if self.solve_puzzle(puzzle, meta=True):
                    self.level += 1
                    
        if self.victory:
            self.show_ending()
        else:
            print(f"\n{C.SYSTEM}Exiting formal system...{C.RESET}\n")
            
        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"GÖDEL'S PARADOX")
        print(f"True but unprovable")
        print(f"{'═' * 70}{C.RESET}\n")

def main():
    try:
        game = GodelsParadox()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.PARADOX}System interrupted{C.RESET}\n")

if __name__ == "__main__":
    main()
