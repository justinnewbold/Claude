#!/usr/bin/env python3
"""
ZENO'S PARADOXES
A philosophical game about infinity, motion, and the nature of space and time

Achilles can never catch the tortoise.
An arrow in flight is always at rest.
You can never cross a room.

Or can you?

Part of the VAULT 13 philosophical games collection.
"""

import random
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

try:
    from colors import C
    from platform_utils import clear_screen
    from vault13.systems.karma import get_karma_system, DecisionType
except ImportError:
    class C:
        RESET = BOLD = DIM = HEADER = SUCCESS = WARNING = DANGER = INFO = ""
        QUEST = TECH = SKILL = ""
    def clear_screen():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    get_karma_system = None
    DecisionType = None


class ParadoxType(Enum):
    """Types of Zeno's paradoxes"""
    DICHOTOMY = "The Dichotomy"
    ACHILLES = "Achilles and the Tortoise"
    ARROW = "The Arrow"
    STADIUM = "The Stadium"


@dataclass
class ParadoxState:
    """State of a paradox exploration"""
    paradox_type: ParadoxType
    steps_taken: int = 0
    distance_covered: float = 0.0
    target_distance: float = 100.0
    infinite_steps: int = 0
    resolved: bool = False


@dataclass
class PhilosophicalSolution:
    """A proposed solution to the paradoxes"""
    name: str
    era: str
    solution: str
    problems: List[str]


@dataclass
class GameState:
    """Overall game state"""
    paradoxes_explored: List[ParadoxType] = field(default_factory=list)
    understanding: int = 0
    frustration: int = 0  # Too much = existential crisis
    solutions_considered: List[str] = field(default_factory=list)


SOLUTIONS = {
    "aristotle": PhilosophicalSolution(
        "Aristotle's Distinction",
        "Ancient Greece",
        "Potential infinity differs from actual infinity. "
        "We can potentially divide forever, but we traverse ACTUAL finite distance.",
        ["Doesn't explain how we complete infinitely many tasks",
         "Why should potential vs actual matter for motion?"]
    ),
    "calculus": PhilosophicalSolution(
        "Mathematical Solution (Calculus)",
        "17th Century",
        "An infinite series can have a finite sum. "
        "1/2 + 1/4 + 1/8 + ... = 1. Infinite steps, finite time.",
        ["This describes what happens, not HOW it happens",
         "Is mathematics about reality or just our models?"]
    ),
    "quantum": PhilosophicalSolution(
        "Quantum Discreteness",
        "20th Century",
        "Space and time might be discrete at the Planck scale. "
        "There's a minimum distance, so infinite division is impossible.",
        ["Planck length is a scale, not necessarily a minimum",
         "Quantum mechanics might not apply to macro objects"]
    ),
    "supertask": PhilosophicalSolution(
        "Supertask Completion",
        "Modern Philosophy",
        "We CAN complete infinitely many tasks in finite time. "
        "Each task takes less time, and the series converges.",
        ["Is 'completing' infinitely many tasks coherent?",
         "What happens 'after' an infinite series?"]
    ),
    "dialetheism": PhilosophicalSolution(
        "Dialetheism",
        "Contemporary",
        "Maybe the paradoxes reveal true contradictions in reality. "
        "Some things can be both true and false.",
        ["Extremely counterintuitive",
         "Most logicians reject true contradictions"]
    ),
}


class ZenosParadoxesGame:
    """Main game exploring Zeno's paradoxes"""

    def __init__(self):
        self.state = GameState()
        self.current_paradox: Optional[ParadoxState] = None
        self.karma = get_karma_system() if get_karma_system else None

    def clear(self):
        clear_screen()

    def print_header(self):
        """Print game header"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║           ZENO'S PARADOXES - Infinity and Motion               ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")
        print(f"  Understanding: {self.state.understanding} | Frustration: {self.state.frustration}%")
        print(f"  Paradoxes Explored: {len(self.state.paradoxes_explored)}")
        print(f"{C.DIM}{'─' * 64}{C.RESET}\n")

    def explore_dichotomy(self):
        """The Dichotomy paradox - you can never complete a journey"""
        self.print_header()
        print(f"{C.QUEST}=== THE DICHOTOMY PARADOX ==={C.RESET}\n")

        print("To reach a destination, you must first go halfway.")
        print("Before you can go halfway, you must go a quarter of the way.")
        print("Before that, an eighth. Then a sixteenth...")
        print("\nBefore you can START moving, you must complete INFINITELY many tasks!")
        print("But you can't complete infinitely many tasks.")
        print("Therefore... you can never begin to move?\n")

        print(f"{C.BOLD}Let's try to cross a room (10 meters):{C.RESET}")
        input(f"\n{C.DIM}Press Enter to attempt movement...{C.RESET}")

        self.current_paradox = ParadoxState(
            paradox_type=ParadoxType.DICHOTOMY,
            target_distance=10.0
        )

        distances = [5.0, 2.5, 1.25, 0.625, 0.3125, 0.15625]

        for i, dist in enumerate(distances):
            self.print_header()
            remaining = self.current_paradox.target_distance - self.current_paradox.distance_covered
            fraction = 2 ** (i + 1)

            print(f"Step {i+1}: Move 1/{fraction} of the way")
            print(f"Distance to cover: {dist:.4f} meters")

            # Visual progress bar
            progress = self.current_paradox.distance_covered / self.current_paradox.target_distance
            bar_length = 40
            filled = int(progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\n[{bar}] {progress*100:.2f}%\n")

            print(f"{C.WARNING}But wait! Before you can move this distance,{C.RESET}")
            print(f"you must first move HALF of it ({dist/2:.4f}m)")
            print(f"And before that, half of THAT ({dist/4:.4f}m)...")

            self.current_paradox.distance_covered += dist
            self.current_paradox.infinite_steps += 1

            print(f"\n{C.INFO}Total distance: {self.current_paradox.distance_covered:.4f}m{C.RESET}")
            input(f"{C.DIM}Press Enter to continue...{C.RESET}")

        # Resolution attempt
        self.print_header()
        print(f"{C.SUCCESS}Somehow, you HAVE moved!{C.RESET}\n")
        print("Despite needing to complete infinitely many 'half-way' points,")
        print("you successfully crossed the room.\n")

        print(f"{C.BOLD}How do you explain this?{C.RESET}")
        print(f"  [1] The paradox is wrong - I obviously moved")
        print(f"  [2] Time is also infinitely divisible, so infinite steps = finite time")
        print(f"  [3] Space isn't actually infinitely divisible")
        print(f"  [4] I don't know, but reality beats logic")

        choice = input(f"\n{C.BOLD}Your explanation: {C.RESET}").strip()

        if choice == "2":
            self.state.understanding += 2
            print(f"\n{C.SUCCESS}You've grasped the calculus solution!{C.RESET}")
        elif choice == "3":
            self.state.understanding += 1
            print(f"\n{C.INFO}The quantum discreteness view!{C.RESET}")
        elif choice == "4":
            self.state.frustration = min(100, self.state.frustration + 10)
            print(f"\n{C.WARNING}Honest, but unsatisfying.{C.RESET}")
        else:
            print(f"\n{C.DIM}That's not really an explanation...{C.RESET}")

        self.state.paradoxes_explored.append(ParadoxType.DICHOTOMY)
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def explore_achilles(self):
        """Achilles and the Tortoise paradox"""
        self.print_header()
        print(f"{C.QUEST}=== ACHILLES AND THE TORTOISE ==={C.RESET}\n")

        print("The swift Achilles races a tortoise.")
        print("Being a good sport, he gives the tortoise a 100m head start.")
        print("Achilles runs 10x faster than the tortoise.\n")

        print(f"{C.WARNING}Zeno's argument:{C.RESET}")
        print("  1. Achilles must first reach where the tortoise WAS")
        print("  2. But by then, the tortoise has moved forward")
        print("  3. Achilles must then reach that NEW position")
        print("  4. But the tortoise has moved again...")
        print("  5. This continues FOREVER")
        print("\nTherefore, Achilles can NEVER catch the tortoise!\n")

        input(f"{C.DIM}Press Enter to simulate the race...{C.RESET}")

        achilles_pos = 0.0
        tortoise_pos = 100.0
        step = 0

        positions = []
        while step < 10:
            self.print_header()
            step += 1

            # Visual race track
            track_length = 60
            ach_marker = int((achilles_pos / 150) * track_length)
            tort_marker = int((tortoise_pos / 150) * track_length)

            track = ["."] * track_length
            if ach_marker < track_length:
                track[ach_marker] = "A"
            if tort_marker < track_length:
                track[tort_marker] = "T"

            print(f"Step {step}:")
            print(f"  Start: {''.join(track)}")
            print(f"  Achilles: {achilles_pos:.2f}m | Tortoise: {tortoise_pos:.2f}m")
            print(f"  Gap: {tortoise_pos - achilles_pos:.2f}m\n")

            # Achilles reaches where tortoise was
            achilles_pos = tortoise_pos
            # Tortoise moves 1/10 as far as Achilles did
            tortoise_pos = tortoise_pos + (tortoise_pos - positions[-1][1] if positions else 10)

            # Simplified movement
            gap = tortoise_pos - achilles_pos
            tortoise_pos = achilles_pos + gap * 0.1

            positions.append((achilles_pos, tortoise_pos))
            time.sleep(0.3)

        print(f"{C.DANGER}The gap keeps shrinking but never reaches zero!{C.RESET}")
        print("...in Zeno's infinite step model.\n")

        print(f"{C.SUCCESS}But in reality:{C.RESET}")
        print("Achilles catches the tortoise at 111.11 meters")
        print("after just 11.11 seconds.\n")

        print(f"{C.BOLD}The key insight:{C.RESET}")
        print("Zeno describes infinitely many EVENTS,")
        print("but they take place in FINITE time.")
        print("1/2 + 1/4 + 1/8 + ... = 1 (not infinity!)")

        self.state.understanding += 2
        self.state.paradoxes_explored.append(ParadoxType.ACHILLES)
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def explore_arrow(self):
        """The Arrow paradox - motion is impossible"""
        self.print_header()
        print(f"{C.QUEST}=== THE ARROW PARADOX ==={C.RESET}\n")

        print("Consider an arrow in flight.\n")

        print("At any given INSTANT, the arrow occupies a space")
        print("exactly equal to its own size.")
        print("If it occupied more space, it would be in two places at once.")
        print("If it occupied less, it wouldn't fully exist.\n")

        print(f"{C.WARNING}But if at every instant the arrow is at rest,{C.RESET}")
        print(f"{C.WARNING}and time is made of instants...{C.RESET}")
        print(f"{C.DANGER}When does the arrow MOVE?{C.RESET}\n")

        # ASCII arrow animation
        for i in range(8):
            self.print_header()
            print("The Arrow Paradox\n")
            space = " " * (i * 4)
            print(f"{space}→===>{C.RESET}")
            print(f"\n{C.INFO}Instant {i+1}: The arrow is HERE.{C.RESET}")
            print(f"At this exact moment, is it moving or stationary?")
            time.sleep(0.4)

        print(f"\n{C.BOLD}The paradox challenges the concept of instantaneous velocity:{C.RESET}")
        print("• At any single instant, there's no 'motion' visible")
        print("• Motion seems to require comparison across time")
        print("• But if time is just a series of instants...\n")

        print(f"{C.BOLD}How do you resolve this?{C.RESET}")
        print(f"  [1] Motion is a property of intervals, not instants")
        print(f"  [2] Instants don't really exist - time is continuous")
        print(f"  [3] The arrow HAS velocity at each instant (calculus)")
        print(f"  [4] Motion is an illusion - only positions are real")

        choice = input(f"\n{C.BOLD}Your resolution: {C.RESET}").strip()

        if choice == "3":
            self.state.understanding += 3
            print(f"\n{C.SUCCESS}The calculus solution:{C.RESET}")
            print("Velocity is defined as a LIMIT - the derivative of position.")
            print("An instant CAN have a velocity, defined by its relationship")
            print("to infinitesimally close moments.")
            if self.karma:
                self.karma.record_decision(
                    "zenos_paradoxes", "calculus_solution",
                    "Applied calculus to motion paradox", 5, DecisionType.CONSEQUENTIAL
                )
        elif choice == "1":
            self.state.understanding += 2
            print(f"\n{C.INFO}The process view:{C.RESET}")
            print("Motion is fundamentally about intervals, not points.")
            print("Asking about motion 'at an instant' may be confused.")
        elif choice == "4":
            self.state.frustration = min(100, self.state.frustration + 15)
            print(f"\n{C.WARNING}A radical view - motion is illusion?{C.RESET}")
            print("This echoes some interpretations of physics,")
            print("but seems to conflict with experience.")

        self.state.paradoxes_explored.append(ParadoxType.ARROW)
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def explore_solutions(self):
        """Explore philosophical solutions"""
        self.print_header()
        print(f"{C.TECH}=== PHILOSOPHICAL SOLUTIONS ==={C.RESET}\n")

        for key, solution in SOLUTIONS.items():
            if key not in self.state.solutions_considered:
                print(f"{C.BOLD}{solution.name} ({solution.era}){C.RESET}")
                print(f"  {solution.solution}")
                print(f"  Problems:")
                for problem in solution.problems:
                    print(f"    - {problem}")
                print()

        print(f"{C.BOLD}Which solution do you find most convincing?{C.RESET}")
        print(f"  [1] Aristotle - Potential vs Actual infinity")
        print(f"  [2] Calculus - Infinite series with finite sums")
        print(f"  [3] Quantum - Space/time might be discrete")
        print(f"  [4] Supertasks - We CAN complete infinite tasks")
        print(f"  [5] Dialetheism - True contradictions exist")
        print(f"  [6] None are satisfying")

        choice = input(f"\n{C.BOLD}Your choice: {C.RESET}").strip()

        solution_map = {
            "1": "aristotle", "2": "calculus", "3": "quantum",
            "4": "supertask", "5": "dialetheism"
        }

        if choice in solution_map:
            selected = solution_map[choice]
            self.state.solutions_considered.append(selected)
            sol = SOLUTIONS[selected]
            print(f"\n{C.INFO}You lean toward {sol.name}.{C.RESET}")
            self.state.understanding += 2
        else:
            self.state.frustration = min(100, self.state.frustration + 10)
            print(f"\n{C.WARNING}Perhaps the paradoxes are genuinely unresolved.{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def meta_reflection(self):
        """Meta-level reflection on what the paradoxes teach"""
        self.print_header()
        print(f"{C.QUEST}=== WHAT DO THE PARADOXES TEACH? ==={C.RESET}\n")

        print("Zeno's paradoxes have puzzled thinkers for 2,500 years.")
        print("Even with calculus and modern physics, debates continue.\n")

        print(f"{C.BOLD}What have we learned?{C.RESET}")
        print("  1. Our intuitions about infinity can mislead us")
        print("  2. 'Obvious' concepts like motion hide complexity")
        print("  3. Mathematics and physics may not fully capture reality")
        print("  4. Some questions may be about CONCEPTS, not THINGS\n")

        print(f"{C.BOLD}The paradoxes might reveal:{C.RESET}")
        print("  • Limits of human reasoning about infinity")
        print("  • The gap between mathematical models and reality")
        print("  • Deep questions about the nature of space and time")
        print("  • The difference between description and explanation\n")

        print(f"{C.BOLD}Your takeaway?{C.RESET}")
        print(f"  [1] The paradoxes are solved by mathematics")
        print(f"  [2] The paradoxes reveal real mysteries")
        print(f"  [3] The paradoxes are linguistic confusion")
        print(f"  [4] I appreciate the beauty of the puzzle itself")

        choice = input(f"\n{C.BOLD}Your view: {C.RESET}").strip()

        if choice == "1":
            print(f"\n{C.SUCCESS}A confident resolution!{C.RESET}")
            self.state.understanding += 2
        elif choice == "2":
            print(f"\n{C.QUEST}Intellectual humility is wise.{C.RESET}")
            self.state.understanding += 3
            if self.karma:
                self.karma.record_decision(
                    "zenos_paradoxes", "accept_mystery",
                    "Accepted deep mystery in paradoxes", 5, DecisionType.VIRTUE
                )
        elif choice == "4":
            print(f"\n{C.INFO}The aesthetic appreciation of philosophy!{C.RESET}")
            self.state.understanding += 2

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def show_status(self):
        """Show current status"""
        self.print_header()
        print(f"{C.INFO}=== YOUR STATUS ==={C.RESET}\n")

        print(f"  Understanding: {self.state.understanding}")
        print(f"  Frustration: {self.state.frustration}%")
        print(f"  Paradoxes Explored: {len(self.state.paradoxes_explored)}")

        if self.state.paradoxes_explored:
            print(f"\n  Explored:")
            for p in self.state.paradoxes_explored:
                print(f"    • {p.value}")

        if self.state.solutions_considered:
            print(f"\n  Solutions Considered:")
            for s in self.state.solutions_considered:
                sol = SOLUTIONS.get(s)
                if sol:
                    print(f"    • {sol.name}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def ending(self):
        """Game ending"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║              ZENO'S PARADOXES - CONCLUSION                     ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}\n")

        if self.state.understanding >= 10:
            print(f"{C.SUCCESS}ENDING: THE PHILOSOPHER{C.RESET}")
            print("\nYou've deeply engaged with these ancient puzzles.")
            print("Whether you've 'solved' them or simply appreciated them,")
            print("you've joined a 2,500-year conversation about")
            print("the nature of motion, infinity, and reality.")

        elif self.state.frustration >= 50:
            print(f"{C.DANGER}ENDING: THE FRUSTRATED{C.RESET}")
            print("\nThe paradoxes have gotten to you.")
            print("Perhaps that's appropriate - they've frustrated")
            print("some of history's greatest minds too.")
            print("The discomfort IS the philosophical experience.")

        elif len(self.state.paradoxes_explored) >= 3:
            print(f"{C.INFO}ENDING: THE EXPLORER{C.RESET}")
            print("\nYou've toured the major paradoxes.")
            print("Each one reveals something about how we think")
            print("about space, time, and motion.")
            print("The journey was the destination.")

        else:
            print(f"{C.QUEST}ENDING: THE CURIOUS{C.RESET}")
            print("\nYou've begun to explore Zeno's challenges.")
            print("There's more to discover - the Arrow, the Stadium,")
            print("and the many solutions proposed over millennia.")

        print(f"\n{C.DIM}Final Stats:{C.RESET}")
        print(f"  Understanding: {self.state.understanding}")
        print(f"  Paradoxes Explored: {len(self.state.paradoxes_explored)}")

        print(f"\n{C.DIM}\"What is changeless cannot be measured by time,{C.RESET}")
        print(f"{C.DIM} and what is in flux cannot be said to exist.\" - Parmenides{C.RESET}")

        input(f"\n{C.BOLD}Press Enter to exit...{C.RESET}")

    def main_menu(self):
        """Main game menu"""
        while True:
            self.print_header()
            print(f"{C.BOLD}Choose a paradox to explore:{C.RESET}\n")
            print(f"  [1] The Dichotomy - You can never complete a journey")
            print(f"  [2] Achilles and the Tortoise - The swift never catch the slow")
            print(f"  [3] The Arrow - An arrow in flight is always at rest")
            print(f"  [4] Explore Philosophical Solutions")
            print(f"  [5] Meta-Reflection")
            print(f"  [6] View Status")
            print(f"  [0] End Exploration")

            choice = input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

            if choice == "1":
                self.explore_dichotomy()
            elif choice == "2":
                self.explore_achilles()
            elif choice == "3":
                self.explore_arrow()
            elif choice == "4":
                self.explore_solutions()
            elif choice == "5":
                self.meta_reflection()
            elif choice == "6":
                self.show_status()
            elif choice == "0":
                self.ending()
                break

    def run(self):
        """Run the game"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     ZENO'S PARADOXES                           ║")
        print("║          Ancient Puzzles About Motion and Infinity             ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        print("""
Around 450 BCE, the philosopher Zeno of Elea created a set of
paradoxes that have puzzled thinkers for two and a half millennia.

These paradoxes seem to prove that motion is impossible.
And yet... we move. We cross rooms. Arrows hit targets.
Achilles catches tortoises (given enough time).

So what's wrong with Zeno's reasoning?
Or is something wrong with our understanding of motion?

These paradoxes touch on:
  • The nature of infinity
  • The continuity of space and time
  • The relationship between mathematics and reality
  • The limits of human reasoning

Let's explore them together.
""")

        input(f"{C.BOLD}Press Enter to begin...{C.RESET}")
        self.main_menu()


def main():
    """Entry point"""
    game = ZenosParadoxesGame()
    game.run()


if __name__ == "__main__":
    main()
