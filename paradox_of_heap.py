#!/usr/bin/env python3
"""
PARADOX OF THE HEAP (Sorites Paradox)
A philosophical puzzle game about vagueness and boundaries

When does a heap of sand stop being a heap?
If you remove one grain, it's still a heap.
But if you keep removing grains, eventually it's not.
So where's the boundary?

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


class VagueProperty(Enum):
    """Properties that exhibit vagueness"""
    HEAP = "Heap of Sand"
    BALD = "Baldness"
    TALL = "Tallness"
    RICH = "Wealth"
    OLD = "Age"
    RED = "Redness"


@dataclass
class SoritesCase:
    """A sorites puzzle case"""
    property_type: VagueProperty
    current_value: int
    max_value: int
    unit: str
    description: str
    threshold_guesses: List[int] = field(default_factory=list)


@dataclass
class PhilosophicalView:
    """A philosophical view on vagueness"""
    name: str
    description: str
    solution: str
    problems: List[str]


PHILOSOPHICAL_VIEWS = {
    "epistemicism": PhilosophicalView(
        "Epistemicism",
        "There IS a precise boundary, we just can't know it.",
        "Vague predicates have sharp boundaries we're ignorant of.",
        ["Why would language have unknowable meanings?",
         "Seems to deny the nature of vague concepts"]
    ),
    "supervaluationism": PhilosophicalView(
        "Supervaluationism",
        "Vague statements are neither true nor false in borderline cases.",
        "Truth-value gaps exist; 'is a heap' has no truth value at boundaries.",
        ["Violates classical logic (law of excluded middle)",
         "How do we reason with truth-value gaps?"]
    ),
    "degree_theory": PhilosophicalView(
        "Degree Theory",
        "Truth comes in degrees, not just true/false.",
        "51 grains might be '0.6 heap' - partially true.",
        ["What determines the exact degree?",
         "Still seems to require sharp boundaries between degrees"]
    ),
    "contextualism": PhilosophicalView(
        "Contextualism",
        "The boundary shifts based on context.",
        "What counts as 'heap' depends on the situation.",
        ["Doesn't explain where any specific boundary is",
         "Seems to avoid rather than solve the problem"]
    ),
}


class ParadoxOfHeapGame:
    """Main game exploring the sorites paradox"""

    def __init__(self):
        self.current_case: Optional[SoritesCase] = None
        self.cases_explored = 0
        self.philosophical_insight = 0
        self.karma = get_karma_system() if get_karma_system else None
        self.player_view: Optional[str] = None
        self.contradictions_found = 0

    def clear(self):
        clear_screen()

    def print_header(self):
        """Print game header"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║         PARADOX OF THE HEAP - The Sorites Paradox              ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")
        print(f"  Cases Explored: {self.cases_explored} | Insight: {self.philosophical_insight}")
        print(f"  Contradictions Found: {self.contradictions_found}")
        print(f"{C.DIM}{'─' * 64}{C.RESET}\n")

    def create_heap_case(self) -> SoritesCase:
        """Create the classic heap of sand case"""
        return SoritesCase(
            property_type=VagueProperty.HEAP,
            current_value=10000,
            max_value=10000,
            unit="grains of sand",
            description="A pile of sand on the beach"
        )

    def create_baldness_case(self) -> SoritesCase:
        """Create baldness case"""
        return SoritesCase(
            property_type=VagueProperty.BALD,
            current_value=100000,
            max_value=100000,
            unit="hairs",
            description="A person's head of hair"
        )

    def create_tall_case(self) -> SoritesCase:
        """Create tallness case"""
        return SoritesCase(
            property_type=VagueProperty.TALL,
            current_value=200,
            max_value=200,
            unit="centimeters",
            description="A person's height"
        )

    def create_wealth_case(self) -> SoritesCase:
        """Create wealth case"""
        return SoritesCase(
            property_type=VagueProperty.RICH,
            current_value=1000000,
            max_value=1000000,
            unit="dollars",
            description="A person's net worth"
        )

    def explore_heap(self):
        """Classic heap exploration"""
        self.print_header()
        self.current_case = self.create_heap_case()

        print(f"{C.QUEST}=== THE HEAP OF SAND ==={C.RESET}\n")
        print("Before you is a pile of 10,000 grains of sand.")
        print("This is clearly a HEAP of sand.\n")

        print(f"{C.BOLD}The Paradox:{C.RESET}")
        print("  Premise 1: 10,000 grains is a heap")
        print("  Premise 2: Removing one grain from a heap leaves a heap")
        print("  Conclusion: Therefore, 1 grain is a heap (by repeated application)")
        print("\nBut that's absurd! Where does the heap become a non-heap?\n")

        input(f"{C.DIM}Press Enter to begin removal...{C.RESET}")

        # Progressive removal
        milestones = [9999, 5000, 1000, 500, 100, 50, 10, 5, 2, 1]
        previous_answer = "heap"

        for grains in milestones:
            self.current_case.current_value = grains
            self.print_header()
            print(f"{C.INFO}You now have {grains:,} {self.current_case.unit}.{C.RESET}\n")

            # Visual representation
            if grains >= 1000:
                visual = "🏔️  " + "·" * min(20, grains // 500)
            elif grains >= 100:
                visual = "⛰️  " + "·" * min(15, grains // 10)
            elif grains >= 10:
                visual = "🗻 " + "·" * grains
            else:
                visual = "· " * grains

            print(f"  {visual}\n")

            print(f"{C.BOLD}Is this still a heap?{C.RESET}")
            print(f"  [1] Yes, still a heap")
            print(f"  [2] No, not a heap anymore")
            print(f"  [3] I can't decide (borderline)")

            choice = input(f"\n{C.BOLD}Your answer: {C.RESET}").strip()

            if choice == "1":
                current_answer = "heap"
            elif choice == "2":
                current_answer = "not_heap"
                if previous_answer == "heap":
                    print(f"\n{C.WARNING}Interesting! You've identified a boundary.{C.RESET}")
                    print(f"Between {milestones[milestones.index(grains)-1]:,} and {grains:,} grains,")
                    print("the heap became a non-heap for you.")
                    self.current_case.threshold_guesses.append(grains)
                    self.contradictions_found += 1
            else:
                current_answer = "borderline"
                print(f"\n{C.INFO}You've found a borderline case!{C.RESET}")
                self.philosophical_insight += 1

            previous_answer = current_answer
            time.sleep(0.5)

        # Final reflection
        self.print_header()
        print(f"{C.QUEST}=== REFLECTION ==={C.RESET}\n")

        if self.current_case.threshold_guesses:
            threshold = self.current_case.threshold_guesses[-1]
            print(f"You identified {threshold:,} grains as your threshold.")
            print(f"\n{C.WARNING}But consider:{C.RESET}")
            print(f"  • Was {threshold + 1} grains REALLY a heap?")
            print(f"  • If yes, why isn't {threshold}?")
            print(f"  • What magical property did that ONE grain have?\n")
        else:
            print("You maintained that even 1 grain is a heap!")
            print("That's... logically consistent but seems wrong.\n")

        input(f"{C.DIM}Press Enter to continue...{C.RESET}")
        self.cases_explored += 1

    def explore_baldness(self):
        """Baldness sorites"""
        self.print_header()
        self.current_case = self.create_baldness_case()

        print(f"{C.QUEST}=== THE BALDNESS PARADOX ==={C.RESET}\n")
        print("A person with 100,000 hairs is clearly NOT bald.")
        print("A person with 0 hairs IS bald.\n")

        print(f"{C.BOLD}The Question:{C.RESET}")
        print("At what exact number of hairs does someone become bald?\n")

        hair_counts = [100000, 50000, 10000, 5000, 1000, 500, 100, 50, 10, 1, 0]

        for hairs in hair_counts:
            self.print_header()
            print(f"{C.INFO}This person has {hairs:,} hairs.{C.RESET}\n")

            # ASCII head representation
            if hairs >= 50000:
                print("    ~~~~~~")
                print("   ~~~~~~~~")
                print("  ( o   o )")
                print("   (  <  )")
                print("    \\___/")
            elif hairs >= 1000:
                print("    ~~~~~~")
                print("   ~      ~")
                print("  ( o   o )")
                print("   (  <  )")
                print("    \\___/")
            elif hairs >= 100:
                print("     ----")
                print("   .      .")
                print("  ( o   o )")
                print("   (  <  )")
                print("    \\___/")
            else:
                print("     ____")
                print("   .      .")
                print("  ( o   o )")
                print("   (  <  )")
                print("    \\___/")

            print(f"\n{C.BOLD}Is this person bald?{C.RESET}")
            print(f"  [1] Yes, bald")
            print(f"  [2] No, not bald")
            print(f"  [3] Borderline/Balding")

            choice = input(f"\n{C.BOLD}Your judgment: {C.RESET}").strip()

            if choice == "3":
                self.philosophical_insight += 1
                print(f"\n{C.INFO}You recognize the vagueness inherent in 'bald'.{C.RESET}")
            time.sleep(0.3)

        self.cases_explored += 1
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def philosophical_discussion(self):
        """Discuss philosophical solutions"""
        self.print_header()
        print(f"{C.TECH}=== PHILOSOPHICAL VIEWS ON VAGUENESS ==={C.RESET}\n")

        views = list(PHILOSOPHICAL_VIEWS.items())

        for key, view in views:
            print(f"{C.BOLD}{view.name}{C.RESET}")
            print(f"  {view.description}")
            print(f"  Solution: {view.solution}")
            print(f"  Problems:")
            for problem in view.problems:
                print(f"    - {problem}")
            print()

        print(f"{C.BOLD}Which view resonates with you?{C.RESET}")
        print(f"  [1] Epistemicism - Sharp but unknowable boundaries")
        print(f"  [2] Supervaluationism - Truth-value gaps")
        print(f"  [3] Degree Theory - Truth in degrees")
        print(f"  [4] Contextualism - Context-dependent boundaries")
        print(f"  [5] None - The paradox is genuinely unresolvable")

        choice = input(f"\n{C.BOLD}Your view: {C.RESET}").strip()

        view_map = {
            "1": "epistemicism",
            "2": "supervaluationism",
            "3": "degree_theory",
            "4": "contextualism",
            "5": "nihilism"
        }

        self.player_view = view_map.get(choice, "undecided")

        if choice == "5":
            print(f"\n{C.WARNING}You accept the paradox as genuinely paradoxical.{C.RESET}")
            print("Perhaps some concepts are inherently incoherent.")
            self.philosophical_insight += 3
            if self.karma:
                self.karma.record_decision(
                    "paradox_heap", "accept_paradox",
                    "Accepted paradox as unresolvable", 5, DecisionType.VIRTUE
                )
        else:
            selected_view = PHILOSOPHICAL_VIEWS.get(self.player_view)
            if selected_view:
                print(f"\n{C.INFO}You lean toward {selected_view.name}.{C.RESET}")
                print(f"This suggests you believe: {selected_view.solution}")
            self.philosophical_insight += 2

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def practical_implications(self):
        """Explore practical implications of vagueness"""
        self.print_header()
        print(f"{C.QUEST}=== PRACTICAL IMPLICATIONS ==={C.RESET}\n")

        print("The sorites paradox isn't just abstract philosophy.")
        print("It affects real decisions every day:\n")

        scenarios = [
            ("Legal Drinking Age",
             "At 20 years 364 days, you're too immature to drink.\n"
             "At 21 years 0 days, you're responsible enough.\n"
             "Did you magically mature overnight?"),

            ("Poverty Line",
             "At $12,759/year, you're in poverty and qualify for aid.\n"
             "At $12,761/year, you're not in poverty.\n"
             "Is $2 really the difference between poverty and not?"),

            ("Life and Death",
             "At what exact moment does a person die?\n"
             "Brain death? Heart stop? Last breath?\n"
             "The law must choose a precise point."),

            ("Species Boundaries",
             "Was there a first human?\n"
             "Every child is the same species as its parents.\n"
             "So how did we become a different species from ancestors?"),
        ]

        for i, (title, scenario) in enumerate(scenarios, 1):
            print(f"{C.BOLD}{i}. {title}{C.RESET}")
            print(f"   {scenario}\n")

        print(f"{C.BOLD}How should society handle these boundaries?{C.RESET}")
        print(f"  [1] Accept arbitrary but consistent cutoffs")
        print(f"  [2] Use gradual scales instead of sharp lines")
        print(f"  [3] Decide case-by-case with human judgment")
        print(f"  [4] The arbitrariness is a fundamental injustice")

        choice = input(f"\n{C.BOLD}Your approach: {C.RESET}").strip()

        if choice == "1":
            print(f"\n{C.INFO}Pragmatic. Laws need clear lines, even if arbitrary.{C.RESET}")
            if self.karma:
                self.karma.record_decision(
                    "paradox_heap", "pragmatic_boundaries",
                    "Accepted arbitrary legal boundaries", 0, DecisionType.UTILITARIAN
                )
        elif choice == "2":
            print(f"\n{C.SUCCESS}Progressive. Graduated systems better capture reality.{C.RESET}")
            self.philosophical_insight += 2
        elif choice == "3":
            print(f"\n{C.WARNING}Human judgment can be inconsistent and biased.{C.RESET}")
            print("But perhaps that flexibility is necessary.")
        else:
            print(f"\n{C.DANGER}A difficult truth. Many legal systems are arbitrary.{C.RESET}")
            self.philosophical_insight += 3

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def meta_puzzle(self):
        """A meta-level puzzle about the paradox itself"""
        self.print_header()
        print(f"{C.DANGER}=== THE PARADOX OF THE PARADOX ==={C.RESET}\n")

        print("Consider this:")
        print("  • 10 contradictions is clearly 'many contradictions'")
        print("  • 1 contradiction is clearly 'a few contradictions'")
        print("  • At what point do 'a few' become 'many'?\n")

        print(f"{C.WARNING}The sorites paradox itself exhibits the sorites paradox!{C.RESET}")
        print("How many examples of vagueness do you need before you have")
        print("'a lot' of examples?\n")

        print(f"{C.BOLD}Does this meta-level recursion:{C.RESET}")
        print(f"  [1] Make the paradox worse")
        print(f"  [2] Show that vagueness is fundamental")
        print(f"  [3] Suggest we need new logical tools")
        print(f"  [4] Prove language itself is incoherent")

        choice = input(f"\n{C.BOLD}Your conclusion: {C.RESET}").strip()

        if choice == "2":
            print(f"\n{C.QUEST}Perhaps vagueness is a feature, not a bug.{C.RESET}")
            print("Language that's too precise might be unusable.")
            self.philosophical_insight += 3
        elif choice == "3":
            print(f"\n{C.INFO}Fuzzy logic and similar tools attempt this.{C.RESET}")
            print("But do they solve the paradox or just formalize it?")
            self.philosophical_insight += 2

        self.cases_explored += 1
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def show_status(self):
        """Show exploration status"""
        self.print_header()
        print(f"{C.INFO}=== EXPLORATION STATUS ==={C.RESET}\n")

        print(f"  Cases Explored: {self.cases_explored}")
        print(f"  Philosophical Insight: {self.philosophical_insight}")
        print(f"  Contradictions Identified: {self.contradictions_found}")

        if self.player_view:
            view_name = self.player_view.replace("_", " ").title()
            print(f"  Your Philosophical Stance: {view_name}")

        if self.current_case and self.current_case.threshold_guesses:
            print(f"\n  Identified Boundaries:")
            for threshold in self.current_case.threshold_guesses:
                print(f"    - {threshold:,} {self.current_case.unit}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def ending(self):
        """Game ending"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║              PARADOX OF THE HEAP - CONCLUSION                  ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}\n")

        if self.philosophical_insight >= 10:
            print(f"{C.QUEST}ENDING: THE ENLIGHTENED{C.RESET}")
            print("\nYou've deeply understood the paradox.")
            print("Vagueness is woven into the fabric of language and thought.")
            print("Sharp boundaries are often our imposition on a continuous world.")

        elif self.player_view == "nihilism":
            print(f"{C.DANGER}ENDING: THE RADICAL{C.RESET}")
            print("\nYou reject easy solutions.")
            print("Perhaps our concepts are fundamentally flawed.")
            print("Or perhaps the paradox reveals something profound")
            print("about the limits of logic.")

        elif self.player_view:
            view = PHILOSOPHICAL_VIEWS.get(self.player_view)
            if view:
                print(f"{C.INFO}ENDING: THE {view.name.upper()}{C.RESET}")
                print(f"\nYou've adopted {view.name} as your view.")
                print(f"Solution: {view.solution}")

        else:
            print(f"{C.SUCCESS}ENDING: THE EXPLORER{C.RESET}")
            print("\nYou've explored the paradox without committing to a solution.")
            print("Sometimes the journey of inquiry is more valuable")
            print("than arriving at an answer.")

        print(f"\n{C.DIM}Final Stats:{C.RESET}")
        print(f"  Philosophical Insight: {self.philosophical_insight}")
        print(f"  Cases Explored: {self.cases_explored}")

        input(f"\n{C.BOLD}Press Enter to exit...{C.RESET}")

    def main_menu(self):
        """Main game menu"""
        while True:
            self.print_header()
            print(f"{C.BOLD}Choose an exploration:{C.RESET}\n")
            print(f"  [1] The Heap of Sand (Classic)")
            print(f"  [2] The Baldness Paradox")
            print(f"  [3] Philosophical Discussion")
            print(f"  [4] Practical Implications")
            print(f"  [5] Meta-Puzzle")
            print(f"  [6] View Status")
            print(f"  [0] End Exploration")

            choice = input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

            if choice == "1":
                self.explore_heap()
            elif choice == "2":
                self.explore_baldness()
            elif choice == "3":
                self.philosophical_discussion()
            elif choice == "4":
                self.practical_implications()
            elif choice == "5":
                self.meta_puzzle()
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
        print("║               PARADOX OF THE HEAP                              ║")
        print("║                 The Sorites Paradox                            ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        print("""
The ancient Greek philosopher Eubulides posed this puzzle:

  "Would you say that a heap of sand minus one grain is still a heap?"
  "Yes."
  "Would you say that removing another grain leaves a heap?"
  "Yes."
  "Then by continuing this logic, even a single grain is a heap!"

This is the Sorites Paradox (from Greek 'soros' meaning 'heap').
It reveals something strange about how we use words like 'heap',
'tall', 'bald', 'rich', and countless others.

Where does a heap stop being a heap?
If you can't say exactly, how can the word mean anything?
""")

        input(f"{C.BOLD}Press Enter to begin exploring...{C.RESET}")
        self.main_menu()


def main():
    """Entry point"""
    game = ParadoxOfHeapGame()
    game.run()


if __name__ == "__main__":
    main()
