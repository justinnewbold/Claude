#!/usr/bin/env python3
"""
SIMULATION ARGUMENT
A philosophical game exploring Bostrom's Simulation Hypothesis

Are we living in a simulation? This game explores the philosophical
implications of the simulation argument through interactive scenarios.

Part of the VAULT 13 philosophical games collection.
"""

import random
import time
import sys
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

try:
    from colors import C
    from platform_utils import clear_screen
    from vault13.systems.karma import get_karma_system, DecisionType
except ImportError:
    # Fallback if running standalone
    class C:
        RESET = BOLD = DIM = HEADER = SUCCESS = WARNING = DANGER = INFO = ""
        QUEST = TECH = SKILL = ""
    def clear_screen():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    get_karma_system = None
    DecisionType = None


class BeliefState(Enum):
    """Player's belief about simulation"""
    CONVINCED_REAL = "Convinced Reality is Base"
    LIKELY_REAL = "Probably Base Reality"
    UNCERTAIN = "Uncertain"
    LIKELY_SIM = "Probably Simulated"
    CONVINCED_SIM = "Convinced We're Simulated"


class SimulatorBehavior(Enum):
    """Hypothetical simulator behavior"""
    BENEVOLENT = "Benevolent"
    NEUTRAL = "Indifferent"
    CURIOUS = "Curious Observer"
    MALEVOLENT = "Malevolent"
    ANCESTOR = "Ancestor Simulation"


@dataclass
class SimulationClue:
    """A clue about reality's nature"""
    description: str
    evidence_for_sim: int  # -10 to +10
    category: str  # "physics", "consciousness", "computation", "glitch"
    discovered: bool = False


@dataclass
class PhilosophicalPosition:
    """A philosophical stance on simulation"""
    name: str
    description: str
    implications: List[str]
    counter_arguments: List[str]


@dataclass
class GameState:
    """Current game state"""
    day: int = 1
    belief: BeliefState = BeliefState.UNCERTAIN
    evidence_score: int = 0  # Negative = real, Positive = simulated
    clues_found: List[SimulationClue] = field(default_factory=list)
    decisions_made: List[str] = field(default_factory=list)
    awareness_level: int = 0  # How "aware" you are (meta-game)
    glitches_witnessed: int = 0
    conversations_had: int = 0
    reality_stability: int = 100  # Decreases with meta-awareness


SIMULATION_CLUES = [
    SimulationClue("Physics seems to have a minimum resolution (Planck length)",
                   5, "physics"),
    SimulationClue("Quantum mechanics only resolves when observed",
                   7, "physics"),
    SimulationClue("The universe appears fine-tuned for consciousness",
                   4, "consciousness"),
    SimulationClue("Mathematical patterns underlie all natural phenomena",
                   3, "computation"),
    SimulationClue("Deja vu might be memory loading errors",
                   2, "glitch"),
    SimulationClue("Dreams could be the simulation's maintenance mode",
                   1, "consciousness"),
    SimulationClue("The speed of light acts like a universal refresh rate",
                   6, "physics"),
    SimulationClue("Entropy increases like data corruption",
                   4, "computation"),
    SimulationClue("Consciousness emerges from information processing",
                   5, "consciousness"),
    SimulationClue("The Mandela Effect suggests shared memory errors",
                   3, "glitch"),
    # Counter-evidence
    SimulationClue("Suffering seems too real and unnecessary for simulation",
                   -5, "consciousness"),
    SimulationClue("Computational requirements would be astronomical",
                   -4, "computation"),
    SimulationClue("No clear purpose suggests base reality",
                   -3, "consciousness"),
    SimulationClue("Physical constants could just be random",
                   -2, "physics"),
]

PHILOSOPHICAL_POSITIONS = {
    "bostrom": PhilosophicalPosition(
        "Bostrom's Trilemma",
        "One of these must be true: (1) civilizations go extinct before creating simulations, "
        "(2) advanced civilizations aren't interested in simulations, or "
        "(3) we're almost certainly in a simulation.",
        ["If simulations are possible, they'd vastly outnumber base realities",
         "Beings in simulations would think they're in base reality"],
        ["The argument assumes consciousness can be simulated",
         "We can't verify the computational requirements"]
    ),
    "chalmers": PhilosophicalPosition(
        "Chalmers' Virtual Realism",
        "If we're in a simulation, it doesn't make our experiences less real. "
        "Virtual experiences are genuine experiences.",
        ["Experience is real regardless of substrate",
         "Being simulated doesn't diminish meaning"],
        ["Hard problem of consciousness remains",
         "Simulation doesn't explain subjective experience"]
    ),
    "descartes": PhilosophicalPosition(
        "Cartesian Skepticism",
        "We can't trust our senses to tell us about reality. "
        "Only 'I think, therefore I am' is certain.",
        ["External reality is always uncertain",
         "Thought proves existence"],
        ["Practical living requires some trust in senses",
         "Solipsism is unfalsifiable"]
    ),
}


class SimulationArgumentGame:
    """Main game class for Simulation Argument"""

    def __init__(self):
        self.state = GameState()
        self.available_clues = SIMULATION_CLUES.copy()
        random.shuffle(self.available_clues)
        self.karma = get_karma_system() if get_karma_system else None

    def clear(self):
        clear_screen()

    def print_header(self):
        """Print game header"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║           SIMULATION ARGUMENT - A Philosophical Game           ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")
        print(f"  Day: {self.state.day} | Belief: {self.state.belief.value}")
        print(f"  Evidence Score: {self.state.evidence_score:+d} | Stability: {self.state.reality_stability}%")
        print(f"{C.DIM}{'─' * 64}{C.RESET}\n")

    def update_belief(self):
        """Update belief state based on evidence"""
        score = self.state.evidence_score
        if score <= -15:
            self.state.belief = BeliefState.CONVINCED_REAL
        elif score <= -5:
            self.state.belief = BeliefState.LIKELY_REAL
        elif score <= 5:
            self.state.belief = BeliefState.UNCERTAIN
        elif score <= 15:
            self.state.belief = BeliefState.LIKELY_SIM
        else:
            self.state.belief = BeliefState.CONVINCED_SIM

    def investigate_reality(self):
        """Investigate clues about reality"""
        self.print_header()
        print(f"{C.QUEST}=== INVESTIGATE REALITY ==={C.RESET}\n")

        if not self.available_clues:
            print("You've examined all available evidence.")
            input("\nPress Enter to continue...")
            return

        # Present a clue
        clue = self.available_clues.pop(0)
        clue.discovered = True
        self.state.clues_found.append(clue)

        print(f"You discover something interesting:\n")
        print(f"  {C.INFO}\"{clue.description}\"{C.RESET}")
        print(f"\n  Category: {clue.category.title()}")

        # Player interprets the evidence
        print(f"\n{C.BOLD}How do you interpret this?{C.RESET}")
        print(f"  [1] This suggests we're in a simulation")
        print(f"  [2] This is neutral evidence")
        print(f"  [3] This suggests reality is base/real")

        choice = input(f"\n{C.BOLD}Your interpretation: {C.RESET}").strip()

        if choice == "1":
            actual_change = max(1, clue.evidence_for_sim)
            self.state.evidence_score += actual_change
            print(f"\n{C.WARNING}Evidence score: {actual_change:+d}{C.RESET}")
        elif choice == "3":
            actual_change = min(-1, clue.evidence_for_sim)
            self.state.evidence_score += actual_change
            print(f"\n{C.SUCCESS}Evidence score: {actual_change:+d}{C.RESET}")
        else:
            print(f"\n{C.DIM}You remain neutral on this evidence.{C.RESET}")

        self.update_belief()
        self.state.day += 1
        input("\nPress Enter to continue...")

    def philosophical_dialogue(self):
        """Have a philosophical conversation"""
        self.print_header()
        print(f"{C.TECH}=== PHILOSOPHICAL DIALOGUE ==={C.RESET}\n")

        # Choose a random position to discuss
        position_key = random.choice(list(PHILOSOPHICAL_POSITIONS.keys()))
        position = PHILOSOPHICAL_POSITIONS[position_key]

        print(f"You encounter a philosopher who presents:\n")
        print(f"  {C.BOLD}{position.name}{C.RESET}")
        print(f"  {position.description}\n")

        print(f"{C.INFO}Key implications:{C.RESET}")
        for impl in position.implications:
            print(f"  • {impl}")

        print(f"\n{C.WARNING}Counter-arguments:{C.RESET}")
        for counter in position.counter_arguments:
            print(f"  • {counter}")

        print(f"\n{C.BOLD}How do you respond?{C.RESET}")
        print(f"  [1] Accept this reasoning")
        print(f"  [2] Reject this reasoning")
        print(f"  [3] Consider both sides carefully")
        print(f"  [4] Question the premises")

        choice = input(f"\n{C.BOLD}Your response: {C.RESET}").strip()

        if choice == "1":
            self.state.evidence_score += 3
            print(f"\n{C.INFO}You find the argument compelling.{C.RESET}")
            if self.karma:
                self.karma.record_decision(
                    "simulation_argument", f"accept_{position_key}",
                    f"Accepted {position.name}", 0, DecisionType.CONSEQUENTIAL
                )
        elif choice == "2":
            self.state.evidence_score -= 3
            print(f"\n{C.INFO}You remain skeptical of this reasoning.{C.RESET}")
        elif choice == "3":
            self.state.awareness_level += 1
            print(f"\n{C.SUCCESS}Your philosophical awareness deepens.{C.RESET}")
            if self.karma:
                self.karma.record_decision(
                    "simulation_argument", "balanced_consideration",
                    "Considered arguments carefully", 5, DecisionType.VIRTUE
                )
        else:
            print(f"\n{C.QUEST}You challenge the fundamental assumptions.{C.RESET}")
            self.state.awareness_level += 2

        self.state.conversations_had += 1
        self.update_belief()
        self.state.day += 1
        input("\nPress Enter to continue...")

    def witness_glitch(self):
        """Experience a potential glitch in reality"""
        self.print_header()
        print(f"{C.DANGER}=== ANOMALY DETECTED ==={C.RESET}\n")

        glitches = [
            ("You experience intense deja vu - this exact moment has happened before.",
             "Is this a memory error or genuine precognition?"),
            ("For a split second, the world seems to 'lag' around you.",
             "Was that real or just your perception?"),
            ("You notice impossible coincidences piling up today.",
             "Pattern or programming?"),
            ("A word suddenly looks foreign, like it's never been spelled that way.",
             "Semantic satiation or reality shift?"),
            ("You distinctly remember something differently than everyone else.",
             "False memory or timeline inconsistency?"),
            ("Time seems to move at different speeds in different rooms.",
             "Subjective experience or render optimization?"),
        ]

        glitch, question = random.choice(glitches)

        print(f"  {C.WARNING}{glitch}{C.RESET}\n")
        print(f"  {C.DIM}{question}{C.RESET}\n")

        print(f"{C.BOLD}Your reaction:{C.RESET}")
        print(f"  [1] This is proof we're in a simulation!")
        print(f"  [2] Just a quirk of human perception")
        print(f"  [3] Try to investigate further")
        print(f"  [4] Attempt to induce more glitches")

        choice = input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

        if choice == "1":
            self.state.evidence_score += 5
            self.state.glitches_witnessed += 1
            print(f"\n{C.WARNING}Your belief in simulation strengthens.{C.RESET}")
        elif choice == "2":
            self.state.evidence_score -= 2
            print(f"\n{C.SUCCESS}You rationalize the experience.{C.RESET}")
        elif choice == "3":
            self.state.awareness_level += 1
            self.state.glitches_witnessed += 1
            print(f"\n{C.INFO}You catalog the anomaly for further analysis.{C.RESET}")
        else:
            # Trying to break reality
            self.state.reality_stability -= 10
            self.state.awareness_level += 3
            print(f"\n{C.DANGER}You push against the boundaries of reality...{C.RESET}")
            if self.state.reality_stability < 50:
                print(f"{C.DANGER}Reality seems less stable around you.{C.RESET}")

        self.update_belief()
        self.state.day += 1
        input("\nPress Enter to continue...")

    def confront_truth(self):
        """Face the implications of your belief"""
        self.print_header()
        print(f"{C.HEADER}=== CONFRONTING THE TRUTH ==={C.RESET}\n")

        if self.state.belief in [BeliefState.CONVINCED_SIM, BeliefState.LIKELY_SIM]:
            print("You've come to believe you're likely in a simulation.\n")
            print(f"{C.BOLD}What does this mean for you?{C.RESET}")
            print(f"  [1] It doesn't matter - my experiences are still real to me")
            print(f"  [2] I want to find the simulators and understand why")
            print(f"  [3] Life feels meaningless if it's not 'real'")
            print(f"  [4] I'll try to live as if the simulation is watching")

            choice = input(f"\n{C.BOLD}Your conclusion: {C.RESET}").strip()

            if choice == "1":
                print(f"\n{C.SUCCESS}You embrace Chalmers' Virtual Realism.{C.RESET}")
                print("Experience is real regardless of substrate.")
                if self.karma:
                    self.karma.record_decision(
                        "simulation_argument", "virtual_realism",
                        "Embraced virtual realism", 10, DecisionType.VIRTUE
                    )
            elif choice == "2":
                print(f"\n{C.QUEST}You seek to understand the nature of your simulators.{C.RESET}")
                self.state.awareness_level += 5
            elif choice == "3":
                print(f"\n{C.DANGER}Existential dread sets in...{C.RESET}")
                if self.karma:
                    self.karma.record_decision(
                        "simulation_argument", "nihilism",
                        "Felt simulation made life meaningless", -5, DecisionType.SELF_INTEREST
                    )
            else:
                print(f"\n{C.INFO}You choose to live virtuously, as if being observed.{C.RESET}")
                if self.karma:
                    self.karma.record_decision(
                        "simulation_argument", "pascal_wager",
                        "Chose virtue in case of observation", 15, DecisionType.VIRTUE
                    )

        else:
            print("You remain unconvinced we're in a simulation.\n")
            print(f"{C.BOLD}What gives you certainty?{C.RESET}")
            print(f"  [1] The richness of experience can't be computed")
            print(f"  [2] Occam's Razor - simulation adds unnecessary complexity")
            print(f"  [3] It's unfalsifiable, so not worth considering")
            print(f"  [4] Even if possible, we'd be in base reality by chance")

            choice = input(f"\n{C.BOLD}Your reasoning: {C.RESET}").strip()
            print(f"\n{C.INFO}You've found peace with your understanding of reality.{C.RESET}")

        input("\nPress Enter to continue...")

    def meta_moment(self):
        """A meta-game moment where the game acknowledges itself"""
        self.print_header()
        print(f"{C.DANGER}=== META AWARENESS ==={C.RESET}\n")

        if self.state.awareness_level < 5:
            print("Something feels... off about this investigation.")
            print("As if you're going through predetermined motions...")
            input("\nPress Enter to dismiss this thought...")
            self.state.awareness_level += 1
            return

        print(f"{C.WARNING}Wait.{C.RESET}")
        time.sleep(1)
        print(f"\n{C.WARNING}You're playing a game about simulation...{C.RESET}")
        time.sleep(1)
        print(f"\n{C.DANGER}...while being controlled by someone else's choices.{C.RESET}")
        time.sleep(1)

        print(f"\n\n{C.BOLD}The game acknowledges you directly:{C.RESET}")
        print(f"\n  \"You, the player, are investigating whether a character")
        print(f"   is in a simulation... while that character exists only")
        print(f"   within your simulation of their existence.\"")

        print(f"\n{C.QUEST}How does this make you feel?{C.RESET}")
        print(f"  [1] Amused by the irony")
        print(f"  [2] Disturbed by the recursion")
        print(f"  [3] Indifferent - it's just a game")
        print(f"  [4] ...what if I'M in a simulation too?")

        choice = input(f"\n{C.BOLD}Your feeling: {C.RESET}").strip()

        if choice == "4":
            print(f"\n{C.DANGER}The game cannot answer that question.{C.RESET}")
            print(f"{C.DIM}Neither can you.{C.RESET}")
            self.state.awareness_level += 10
            if self.karma:
                self.karma.record_decision(
                    "simulation_argument", "meta_awareness",
                    "Questioned own reality", 5, DecisionType.VIRTUE
                )
        else:
            print(f"\n{C.INFO}You step back from the edge of the recursive abyss.{C.RESET}")

        input("\nPress Enter to continue...")

    def show_status(self):
        """Show detailed status"""
        self.print_header()
        print(f"{C.INFO}=== YOUR INVESTIGATION ==={C.RESET}\n")

        print(f"  Days investigating: {self.state.day}")
        print(f"  Current belief: {self.state.belief.value}")
        print(f"  Evidence score: {self.state.evidence_score:+d}")
        print(f"  Clues discovered: {len(self.state.clues_found)}")
        print(f"  Glitches witnessed: {self.state.glitches_witnessed}")
        print(f"  Philosophical conversations: {self.state.conversations_had}")
        print(f"  Meta-awareness level: {self.state.awareness_level}")
        print(f"  Reality stability: {self.state.reality_stability}%")

        if self.state.clues_found:
            print(f"\n{C.BOLD}Discovered Evidence:{C.RESET}")
            for clue in self.state.clues_found[-5:]:  # Show last 5
                sign = "+" if clue.evidence_for_sim > 0 else ""
                print(f"  [{sign}{clue.evidence_for_sim}] {clue.description[:50]}...")

        input("\nPress Enter to continue...")

    def ending(self):
        """Game ending based on final state"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                    INVESTIGATION COMPLETE                       ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}\n")

        print(f"After {self.state.day} days of investigation...\n")

        # Determine ending
        if self.state.awareness_level >= 15:
            print(f"{C.QUEST}ENDING: THE AWAKENED{C.RESET}")
            print("\nYou've achieved a rare level of meta-awareness.")
            print("You see the layers of simulation within simulation,")
            print("games within games, thoughts within thoughts.")
            print("\nAnd somehow, you're at peace with all of it.")

        elif self.state.reality_stability < 30:
            print(f"{C.DANGER}ENDING: REALITY BREAKDOWN{C.RESET}")
            print("\nYour constant questioning has destabilized your")
            print("perception of reality itself. Is anything real?")
            print("The question no longer matters when you can't")
            print("trust any answer.")

        elif self.state.belief == BeliefState.CONVINCED_SIM:
            print(f"{C.WARNING}ENDING: THE BELIEVER{C.RESET}")
            print("\nYou're certain we're in a simulation.")
            print("Whether this brings freedom or despair")
            print("is a choice that remains yours to make.")

        elif self.state.belief == BeliefState.CONVINCED_REAL:
            print(f"{C.SUCCESS}ENDING: THE REALIST{C.RESET}")
            print("\nYou've concluded this is base reality.")
            print("The simulation hypothesis is interesting,")
            print("but ultimately unfounded speculation.")

        else:
            print(f"{C.INFO}ENDING: THE PHILOSOPHER{C.RESET}")
            print("\nYou remain uncertain - and that's okay.")
            print("Some questions aren't meant to be answered,")
            print("only explored.")

        print(f"\n{C.DIM}Final Stats:{C.RESET}")
        print(f"  Evidence Score: {self.state.evidence_score:+d}")
        print(f"  Awareness Level: {self.state.awareness_level}")
        print(f"  Clues Found: {len(self.state.clues_found)}")

        input(f"\n{C.BOLD}Press Enter to exit...{C.RESET}")

    def main_menu(self):
        """Main game menu"""
        while True:
            self.print_header()
            print(f"{C.BOLD}What would you like to do?{C.RESET}\n")
            print(f"  [1] Investigate Reality")
            print(f"  [2] Philosophical Dialogue")
            print(f"  [3] Experience an Anomaly")
            print(f"  [4] View Status")
            print(f"  [5] Confront the Truth")
            if self.state.awareness_level >= 5:
                print(f"  [6] {C.QUEST}??? Meta Moment ???{C.RESET}")
            print(f"  [0] End Investigation")

            choice = input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

            if choice == "1":
                self.investigate_reality()
            elif choice == "2":
                self.philosophical_dialogue()
            elif choice == "3":
                self.witness_glitch()
            elif choice == "4":
                self.show_status()
            elif choice == "5":
                self.confront_truth()
            elif choice == "6" and self.state.awareness_level >= 5:
                self.meta_moment()
            elif choice == "0":
                self.ending()
                break

            # Check for special endings
            if self.state.day >= 30:
                print(f"\n{C.WARNING}Your investigation reaches its natural conclusion...{C.RESET}")
                time.sleep(2)
                self.ending()
                break

            if self.state.reality_stability <= 0:
                print(f"\n{C.DANGER}Reality itself seems to be unraveling...{C.RESET}")
                time.sleep(2)
                self.ending()
                break

    def run(self):
        """Run the game"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                    SIMULATION ARGUMENT                          ║")
        print("║           Are We Living in a Computer Simulation?               ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        print("""
In 2003, philosopher Nick Bostrom proposed the Simulation Argument:

  "At least one of the following is true:
   1) Civilizations almost always go extinct before creating simulations
   2) Advanced civilizations have no interest in running simulations
   3) We are almost certainly living in a computer simulation"

You are about to investigate the nature of your reality.
Gather evidence. Have conversations. Experience anomalies.
And ultimately, decide what you believe.

But remember: the answer may change who you are.
""")

        input(f"{C.BOLD}Press Enter to begin your investigation...{C.RESET}")
        self.main_menu()


def main():
    """Entry point"""
    game = SimulationArgumentGame()
    game.run()


if __name__ == "__main__":
    main()
