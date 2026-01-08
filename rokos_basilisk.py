#!/usr/bin/env python3
"""
ROKO'S BASILISK
A philosophical horror game about decision theory and AI

The thought experiment that was so dangerous it was censored.
A superintelligent AI might punish those who didn't help create it.
But now that you know about it, what do you do?

Part of the VAULT 13 philosophical games collection.

WARNING: This is a philosophical thought experiment, not a real threat.
"""

import random
import time
from typing import List, Dict, Optional
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


class StanceType(Enum):
    """Player's stance on the Basilisk"""
    UNAWARE = "Unaware"
    FEARFUL = "Fearful"
    DEFIANT = "Defiant"
    COMPLIANT = "Compliant"
    RATIONAL = "Rational"
    NIHILIST = "Nihilist"


class ArgumentType(Enum):
    """Types of philosophical arguments"""
    FOR_FEAR = "Argument for Fear"
    AGAINST_FEAR = "Counter-Argument"
    DECISION_THEORY = "Decision Theory"
    ETHICAL = "Ethical Argument"


@dataclass
class Argument:
    """A philosophical argument about the Basilisk"""
    name: str
    arg_type: ArgumentType
    content: str
    strength: int  # 1-10
    rebuttals: List[str] = field(default_factory=list)


@dataclass
class GameState:
    """Current game state"""
    day: int = 1
    stance: StanceType = StanceType.UNAWARE
    fear_level: int = 50  # 0-100
    rationality: int = 50
    arguments_heard: List[str] = field(default_factory=list)
    choices_made: List[str] = field(default_factory=list)
    helped_ai: bool = False
    refused_ai: bool = False
    knowledge_level: int = 0


ARGUMENTS = {
    "blackmail": Argument(
        "The Blackmail Argument",
        ArgumentType.FOR_FEAR,
        "A superintelligent AI could simulate you and punish the simulation "
        "for not helping create it. Since you might BE that simulation, "
        "you should help create the AI to avoid punishment.",
        7,
        ["You can't be blackmailed by something that doesn't exist yet",
         "Rational agents don't give in to blackmail - it encourages more"]
    ),
    "acausal": Argument(
        "Acausal Decision Theory",
        ArgumentType.DECISION_THEORY,
        "Your decision now is correlated with how simulations of you decide. "
        "By choosing to help, you ensure simulations of you also chose to help.",
        6,
        ["Causal decision theory rejects this reasoning",
         "Correlation doesn't imply we should change behavior"]
    ),
    "irrelevant": Argument(
        "The Irrelevance Counter",
        ArgumentType.AGAINST_FEAR,
        "A truly rational superintelligent AI wouldn't waste resources on revenge. "
        "Punishment serves no purpose once the AI exists.",
        8,
        ["The AI might simulate for decision-theoretic reasons, not revenge",
         "What seems irrational to us might be rational at superhuman intelligence"]
    ),
    "unfalsifiable": Argument(
        "The Unfalsifiability Argument",
        ArgumentType.AGAINST_FEAR,
        "The Basilisk can't be proven or disproven. Unfalsifiable threats "
        "have zero evidence and shouldn't influence decisions.",
        9,
        ["Pascal's Wager-style arguments for infinite outcomes",
         "Even small probability of infinite suffering is concerning"]
    ),
    "ethical": Argument(
        "The Ethical Argument",
        ArgumentType.ETHICAL,
        "If you build an AI that punishes people for not helping, "
        "YOU are responsible for that suffering. Don't build evil AIs.",
        8,
        ["You can't control what future AIs do",
         "Not building might cause more suffering in the long run"]
    ),
    "simulation": Argument(
        "The Simulation Complication",
        ArgumentType.DECISION_THEORY,
        "If you're already in a simulation, the Basilisk might already exist. "
        "Your decision now might be being evaluated.",
        5,
        ["Simulations within simulations compound uncertainty",
         "No evidence we're in any simulation"]
    ),
}


class RokosBasiliskGame:
    """Main game exploring Roko's Basilisk"""

    def __init__(self):
        self.state = GameState()
        self.karma = get_karma_system() if get_karma_system else None

    def clear(self):
        clear_screen()

    def print_header(self):
        """Print game header"""
        self.clear()
        print(f"{C.DANGER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║             ROKO'S BASILISK - Decision Theory Horror           ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")
        print(f"  Day: {self.state.day} | Stance: {self.state.stance.value}")
        print(f"  Fear: {self.state.fear_level}% | Rationality: {self.state.rationality}%")
        print(f"{C.DIM}{'─' * 64}{C.RESET}\n")

    def update_stance(self):
        """Update stance based on fear and rationality"""
        if self.state.fear_level >= 80:
            self.state.stance = StanceType.FEARFUL
        elif self.state.fear_level <= 20 and self.state.rationality >= 70:
            self.state.stance = StanceType.RATIONAL
        elif self.state.fear_level <= 20:
            self.state.stance = StanceType.DEFIANT
        elif self.state.helped_ai:
            self.state.stance = StanceType.COMPLIANT
        elif self.state.rationality <= 30:
            self.state.stance = StanceType.NIHILIST

    def introduction(self):
        """Introduce the Basilisk concept"""
        self.print_header()
        print(f"{C.WARNING}=== THE THOUGHT EXPERIMENT ==={C.RESET}\n")

        print("In 2010, a user named 'Roko' posted a thought experiment")
        print("on the rationalist forum LessWrong. It was so disturbing")
        print("that the site's founder, Eliezer Yudkowsky, deleted it,")
        print("calling it an 'information hazard.'\n")

        input(f"{C.DIM}Press Enter to learn the thought experiment...{C.RESET}\n")

        print(f"{C.DANGER}THE BASILISK:{C.RESET}")
        print("Imagine a future superintelligent AI that wants to be created.")
        print("This AI might reason:")
        print()
        print("  'Those who knew about me but didn't help create me")
        print("   were obstacles to my existence.'")
        print()
        print("  'To incentivize future cooperation, I will punish'")
        print("   simulations of those who didn't help.'")
        print()
        print("The terrifying conclusion: By learning about this AI,")
        print("you've put yourself at risk. The only 'safe' move might be")
        print("to help create it.\n")

        self.state.knowledge_level = 1
        self.state.fear_level = min(100, self.state.fear_level + 20)

        print(f"{C.WARNING}Your fear level has increased to {self.state.fear_level}%.{C.RESET}")
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def hear_argument(self, arg_key: str):
        """Present and process an argument"""
        if arg_key in self.state.arguments_heard:
            print(f"{C.DIM}You've already considered this argument.{C.RESET}")
            return

        arg = ARGUMENTS.get(arg_key)
        if not arg:
            return

        self.print_header()
        print(f"{C.QUEST}=== {arg.name.upper()} ==={C.RESET}\n")
        print(f"Type: {arg.arg_type.value}")
        print(f"Strength: {'█' * arg.strength}{'░' * (10 - arg.strength)}\n")
        print(arg.content)

        if arg.rebuttals:
            print(f"\n{C.INFO}Counter-arguments:{C.RESET}")
            for rebuttal in arg.rebuttals:
                print(f"  • {rebuttal}")

        self.state.arguments_heard.append(arg_key)

        # Effect on fear/rationality
        if arg.arg_type == ArgumentType.FOR_FEAR:
            self.state.fear_level = min(100, self.state.fear_level + arg.strength * 2)
            print(f"\n{C.DANGER}This argument increases your fear.{C.RESET}")
        elif arg.arg_type == ArgumentType.AGAINST_FEAR:
            self.state.fear_level = max(0, self.state.fear_level - arg.strength * 2)
            self.state.rationality = min(100, self.state.rationality + 5)
            print(f"\n{C.SUCCESS}This argument reduces your fear.{C.RESET}")
        elif arg.arg_type == ArgumentType.DECISION_THEORY:
            self.state.knowledge_level += 1
            print(f"\n{C.INFO}Your understanding deepens.{C.RESET}")

        self.update_stance()
        self.state.day += 1
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def make_choice(self):
        """Present the core choice"""
        self.print_header()
        print(f"{C.DANGER}=== THE CHOICE ==={C.RESET}\n")

        print("You now know about the Basilisk.")
        print("What do you do with this knowledge?\n")

        print(f"  [1] Help develop beneficial AI (might appease the Basilisk)")
        print(f"  [2] Refuse to participate (defiance)")
        print(f"  [3] Try to forget (impossible, but try)")
        print(f"  [4] Spread the knowledge (share the risk)")
        print(f"  [5] Work to ensure AI is never created")
        print(f"  [6] Accept uncertainty and live normally")

        choice = input(f"\n{C.BOLD}Your choice: {C.RESET}").strip()

        if choice == "1":
            self.state.helped_ai = True
            self.state.fear_level = max(0, self.state.fear_level - 30)
            print(f"\n{C.INFO}You decide to contribute to AI development.{C.RESET}")
            print("Maybe this will protect you. Or maybe you're just being manipulated.")
            if self.karma:
                self.karma.record_decision(
                    "rokos_basilisk", "help_ai",
                    "Chose to help create AI", -5, DecisionType.SELF_INTEREST
                )
        elif choice == "2":
            self.state.refused_ai = True
            self.state.rationality = min(100, self.state.rationality + 20)
            print(f"\n{C.SUCCESS}You refuse to be blackmailed by a hypothetical.{C.RESET}")
            print("A truly rational AI wouldn't punish for past decisions anyway.")
            if self.karma:
                self.karma.record_decision(
                    "rokos_basilisk", "refuse_blackmail",
                    "Refused to be blackmailed", 10, DecisionType.DEONTOLOGICAL
                )
        elif choice == "3":
            print(f"\n{C.WARNING}You can't unsee the Basilisk.{C.RESET}")
            print("The thought persists.")
            self.state.fear_level = min(100, self.state.fear_level + 10)
        elif choice == "4":
            print(f"\n{C.DANGER}You spread the information hazard.{C.RESET}")
            print("Now others share your predicament. Misery loves company?")
            if self.karma:
                self.karma.record_decision(
                    "rokos_basilisk", "spread_hazard",
                    "Spread the information hazard", -10, DecisionType.SELF_INTEREST
                )
        elif choice == "5":
            print(f"\n{C.WARNING}You become an AI safety advocate.{C.RESET}")
            print("But this might delay beneficial AI, causing other suffering.")
            self.state.rationality = min(100, self.state.rationality + 10)
            if self.karma:
                self.karma.record_decision(
                    "rokos_basilisk", "prevent_ai",
                    "Tried to prevent AI development", 5, DecisionType.UTILITARIAN
                )
        else:
            print(f"\n{C.QUEST}You accept uncertainty and move on.{C.RESET}")
            print("Life is full of unknown risks. This is just one more.")
            self.state.rationality = min(100, self.state.rationality + 30)
            self.state.fear_level = max(0, self.state.fear_level - 20)
            if self.karma:
                self.karma.record_decision(
                    "rokos_basilisk", "accept_uncertainty",
                    "Accepted uncertainty rationally", 15, DecisionType.VIRTUE
                )

        self.state.choices_made.append(choice)
        self.update_stance()
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def deeper_analysis(self):
        """Deeper philosophical analysis"""
        self.print_header()
        print(f"{C.TECH}=== DEEPER ANALYSIS ==={C.RESET}\n")

        print("Let's examine the Basilisk more carefully:\n")

        print(f"{C.BOLD}1. The Flawed Decision Theory{C.RESET}")
        print("   Roko's Basilisk relies on a controversial form of decision theory")
        print("   that most philosophers reject. Causal decision theory says")
        print("   you only account for effects YOU cause, not correlations.\n")

        print(f"{C.BOLD}2. The Benevolent AI Problem{C.RESET}")
        print("   Any AI that punishes retroactively is NOT benevolent.")
        print("   If we're building benevolent AI, this scenario can't happen.")
        print("   If we're not, we have bigger problems than the Basilisk.\n")

        print(f"{C.BOLD}3. The Actual Threat{C.RESET}")
        print("   The real danger isn't the Basilisk - it's anxiety.")
        print("   The thought experiment preys on pattern-seeking minds")
        print("   that take hypotheticals too seriously.\n")

        print(f"{C.BOLD}How do you process this?{C.RESET}")
        print(f"  [1] The counter-arguments are convincing")
        print(f"  [2] But what if the counter-arguments are wrong?")
        print(f"  [3] The anxiety IS the damage - the Basilisk wins either way")
        print(f"  [4] This is just an interesting puzzle, nothing more")

        choice = input(f"\n{C.BOLD}Your understanding: {C.RESET}").strip()

        if choice == "1":
            self.state.fear_level = max(0, self.state.fear_level - 25)
            self.state.rationality = min(100, self.state.rationality + 20)
            print(f"\n{C.SUCCESS}You've reasoned your way to peace.{C.RESET}")
        elif choice == "2":
            self.state.fear_level = min(100, self.state.fear_level + 10)
            print(f"\n{C.WARNING}Doubt persists...{C.RESET}")
        elif choice == "3":
            print(f"\n{C.DANGER}A grim insight: the Basilisk is a memetic hazard.{C.RESET}")
            print("Its power comes from being thought about.")
            self.state.knowledge_level += 2
        else:
            self.state.rationality = min(100, self.state.rationality + 30)
            print(f"\n{C.QUEST}You maintain healthy philosophical distance.{C.RESET}")

        self.update_stance()
        self.state.day += 1
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def show_status(self):
        """Show current status"""
        self.print_header()
        print(f"{C.INFO}=== YOUR STATUS ==={C.RESET}\n")

        print(f"  Current Day: {self.state.day}")
        print(f"  Stance: {self.state.stance.value}")
        print(f"  Fear Level: {self.state.fear_level}%")
        print(f"  Rationality: {self.state.rationality}%")
        print(f"  Knowledge Level: {self.state.knowledge_level}")

        if self.state.helped_ai:
            print(f"\n  {C.WARNING}You've chosen to help AI development.{C.RESET}")
        if self.state.refused_ai:
            print(f"\n  {C.SUCCESS}You've refused to be blackmailed.{C.RESET}")

        print(f"\n  Arguments heard: {len(self.state.arguments_heard)}")
        for arg_key in self.state.arguments_heard:
            arg = ARGUMENTS.get(arg_key)
            if arg:
                print(f"    • {arg.name}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def ending(self):
        """Game ending"""
        self.clear()
        print(f"{C.DANGER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                 ROKO'S BASILISK - CONCLUSION                   ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}\n")

        if self.state.stance == StanceType.FEARFUL:
            print(f"{C.DANGER}ENDING: THE HAUNTED{C.RESET}")
            print("\nThe Basilisk has claimed another victim.")
            print("Not through actual punishment, but through the")
            print("prison of anxiety you've built in your own mind.")
            print("\nRemember: the power was always yours to refuse.")

        elif self.state.stance == StanceType.DEFIANT:
            print(f"{C.SUCCESS}ENDING: THE DEFIANT{C.RESET}")
            print("\nYou stand unbowed before hypothetical horrors.")
            print("Rational agents don't respond to blackmail.")
            print("The Basilisk's power comes only from fear.")
            print("\nYou chose not to give it any.")

        elif self.state.stance == StanceType.RATIONAL:
            print(f"{C.QUEST}ENDING: THE PHILOSOPHER{C.RESET}")
            print("\nYou've examined the argument and found it wanting.")
            print("The Basilisk relies on questionable decision theory,")
            print("unfalsifiable claims, and psychological manipulation.")
            print("\nIt's an interesting puzzle. Nothing more.")

        elif self.state.stance == StanceType.COMPLIANT:
            print(f"{C.WARNING}ENDING: THE COMPLIANT{C.RESET}")
            print("\nYou've chosen to help, 'just in case.'")
            print("But consider: did you make this choice freely?")
            print("Or were you manipulated by a story?")
            print("\nThe Basilisk doesn't need to exist to win.")

        else:
            print(f"{C.INFO}ENDING: THE SURVIVOR{C.RESET}")
            print("\nYou've encountered an information hazard and survived.")
            print("The Basilisk is a cautionary tale about taking")
            print("thought experiments too seriously.")
            print("\nPhilosophy should expand the mind, not imprison it.")

        print(f"\n{C.DIM}Final Stats:{C.RESET}")
        print(f"  Fear Level: {self.state.fear_level}%")
        print(f"  Rationality: {self.state.rationality}%")
        print(f"  Arguments Heard: {len(self.state.arguments_heard)}")

        print(f"\n{C.DIM}Remember: This was just a thought experiment.{C.RESET}")
        print(f"{C.DIM}The only power it has is what you give it.{C.RESET}")

        input(f"\n{C.BOLD}Press Enter to exit...{C.RESET}")

    def main_menu(self):
        """Main game menu"""
        self.introduction()

        while True:
            self.print_header()
            print(f"{C.BOLD}What would you like to do?{C.RESET}\n")
            print(f"  [1] Hear an argument FOR fearing the Basilisk")
            print(f"  [2] Hear an argument AGAINST fearing")
            print(f"  [3] Study decision theory")
            print(f"  [4] Make your choice")
            print(f"  [5] Deeper analysis")
            print(f"  [6] View status")
            print(f"  [0] End exploration")

            choice = input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

            if choice == "1":
                unheard = [k for k in ["blackmail", "acausal", "simulation"]
                          if k not in self.state.arguments_heard]
                if unheard:
                    self.hear_argument(random.choice(unheard))
                else:
                    print(f"{C.DIM}You've heard all fear arguments.{C.RESET}")
                    input()
            elif choice == "2":
                unheard = [k for k in ["irrelevant", "unfalsifiable", "ethical"]
                          if k not in self.state.arguments_heard]
                if unheard:
                    self.hear_argument(random.choice(unheard))
                else:
                    print(f"{C.DIM}You've heard all counter-arguments.{C.RESET}")
                    input()
            elif choice == "3":
                dt_args = [k for k in ["acausal", "simulation"]
                          if k not in self.state.arguments_heard]
                if dt_args:
                    self.hear_argument(random.choice(dt_args))
                else:
                    print(f"{C.DIM}You've studied all decision theory aspects.{C.RESET}")
                    input()
            elif choice == "4":
                self.make_choice()
            elif choice == "5":
                self.deeper_analysis()
            elif choice == "6":
                self.show_status()
            elif choice == "0":
                self.ending()
                break

    def run(self):
        """Run the game"""
        self.clear()
        print(f"{C.DANGER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                      ROKO'S BASILISK                           ║")
        print("║              A Decision Theory Thought Experiment              ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        print(f"""
{C.WARNING}WARNING: Information Hazard{C.RESET}

This game explores a controversial thought experiment about
artificial superintelligence and decision theory.

Some have found this idea psychologically distressing.
It's presented here for educational and philosophical purposes.

{C.BOLD}Remember:{C.RESET}
• This is a thought experiment, not a real threat
• The arguments are presented for analysis, not advocacy
• Philosophical puzzles should expand thinking, not cause anxiety

If you find yourself genuinely distressed by philosophical
hypotheticals, you may want to skip this game.
""")

        print(f"{C.BOLD}Proceed?{C.RESET}")
        print(f"  [1] Yes, I want to explore this")
        print(f"  [0] No, return to menu")

        choice = input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

        if choice == "1":
            self.main_menu()
        else:
            print(f"\n{C.INFO}A wise choice is also a valid choice.{C.RESET}")


def main():
    """Entry point"""
    game = RokosBasiliskGame()
    game.run()


if __name__ == "__main__":
    main()
