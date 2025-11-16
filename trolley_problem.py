#!/usr/bin/env python3
"""
THE TROLLEY PROBLEM ENGINE

Ethics as cascading consequences.

Every moral choice creates new dilemmas.
Save one person now, doom many later?
Utilitarian math vs deontological principles.

This is ethics made computational.
Your philosophy will be tested.
"""

import os
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# ANSI colors
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Ethics
    UTILITARIAN = '\033[38;5;46m'   # Green - greatest good
    DEONTOLOGICAL = '\033[38;5;51m' # Cyan - duty/rules
    VIRTUE = '\033[38;5;141m'       # Purple - character
    NEUTRAL = '\033[38;5;243m'      # Gray

    # People
    PERSON = '\033[38;5;226m'       # Yellow - individual
    GROUP = '\033[38;5;214m'        # Orange - many people
    DANGER = '\033[38;5;203m'       # Red - threat

    # UI
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    ERROR = '\033[38;5;203m'
    ETHICS = '\033[38;5;171m'


class EthicalFramework(Enum):
    UTILITARIAN = "utilitarian"     # Greatest good for greatest number
    DEONTOLOGICAL = "deontological" # Duty-based, rules matter
    VIRTUE = "virtue"               # Character and virtue
    CARE = "care"                   # Relationships and empathy


@dataclass
class Person:
    """A person in an ethical dilemma"""
    name: str
    age: int
    role: str
    value_to_society: int = 1  # For utilitarian calc
    relationship: str = "stranger"


@dataclass
class Choice:
    """An ethical choice"""
    description: str
    action: str
    saves: List[Person]
    sacrifices: List[Person]
    framework: EthicalFramework
    consequences: List[str] = field(default_factory=list)


@dataclass
class Dilemma:
    """An ethical dilemma with choices"""
    situation: str
    context: str
    choice_a: Choice
    choice_b: Choice
    depth: int = 0
    previous_choices: List[str] = field(default_factory=list)


class TrolleyProblemEngine:
    def __init__(self):
        self.dilemmas_faced = 0
        self.choices_made: List[Choice] = []
        self.people_saved = 0
        self.people_sacrificed = 0
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.virtue_score = 0
        self.care_score = 0
        self.game_over = False
        self.max_depth = 5

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("T H E   T R O L L E Y   P R O B L E M   E N G I N E")

        intro = f"""
{C.ETHICS}\"There is a trolley coming down the tracks...\"{C.RESET}

{C.DIM}The trolley problem is philosophy's most famous thought experiment.
But what if every choice created new dilemmas?
What if consequences cascaded through time?

This is ethics as a game.
Your philosophy will be tested.{C.RESET}

{C.BOLD}How It Works:{C.RESET}

You face ethical dilemmas with two choices:
• Each choice saves some, sacrifices others
• Your decision creates NEW dilemmas based on consequences
• Choices compound - early decisions affect later options
• Different ethical frameworks give different scores

{C.BOLD}Ethical Frameworks:{C.RESET}

{C.UTILITARIAN}Utilitarian:{C.RESET} Greatest good for greatest number
  - Maximize total welfare
  - Numbers matter most
  - Consequences define morality

{C.DEONTOLOGICAL}Deontological:{C.RESET} Duty and rules matter
  - Some acts are always wrong
  - Don't use people as means
  - Principles over outcomes

{C.VIRTUE}Virtue Ethics:{C.RESET} Character and virtue
  - What would a virtuous person do?
  - Develop moral character
  - Context matters

{C.NEUTRAL}Care Ethics:{C.RESET} Relationships and empathy
  - Care for those close to you
  - Relationships create obligations
  - Emotional connection matters

{C.BOLD}The Challenge:{C.RESET}

Different frameworks often conflict. You can't maximize all scores.
Your choices reveal your TRUE moral philosophy.

Ready to face impossible decisions?

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def generate_initial_dilemma(self) -> Dilemma:
        """Generate the classic trolley problem"""
        workers = [
            Person("Worker 1", 35, "railroad worker"),
            Person("Worker 2", 42, "railroad worker"),
            Person("Worker 3", 28, "railroad worker"),
            Person("Worker 4", 51, "railroad worker"),
            Person("Worker 5", 39, "railroad worker"),
        ]

        lone_worker = Person("Worker 6", 45, "railroad worker")

        choice_a = Choice(
            description="Do nothing - let the trolley continue",
            action="Allow the trolley to stay on course",
            saves=[lone_worker],
            sacrifices=workers,
            framework=EthicalFramework.DEONTOLOGICAL,
            consequences=["The community mourns 5 deaths", "You avoided actively causing harm"]
        )

        choice_b = Choice(
            description="Pull the lever - divert to side track",
            action="Actively divert the trolley",
            saves=workers,
            sacrifices=[lone_worker],
            framework=EthicalFramework.UTILITARIAN,
            consequences=["You saved 5 lives", "You actively killed 1 person"]
        )

        return Dilemma(
            situation="A runaway trolley is heading toward 5 workers on the track.",
            context="You stand at a lever that can divert it to a side track where 1 worker stands.",
            choice_a=choice_a,
            choice_b=choice_b,
            depth=0
        )

    def generate_cascade_dilemma(self, previous_choice: Choice, depth: int) -> Dilemma:
        """Generate a new dilemma based on previous choice"""

        if depth == 1:
            # After first choice - consequences emerge
            if previous_choice.framework == EthicalFramework.UTILITARIAN:
                # You pulled lever - now family of lone worker seeks justice
                return Dilemma(
                    situation=f"The family of {previous_choice.sacrifices[0].name} demands justice.",
                    context="They want you prosecuted for murder. You could flee the country.",
                    choice_a=Choice(
                        description="Face trial - accept responsibility",
                        action="Turn yourself in",
                        saves=[],
                        sacrifices=[],
                        framework=EthicalFramework.DEONTOLOGICAL,
                        consequences=["You face 10 years in prison", "Society sees justice served"]
                    ),
                    choice_b=Choice(
                        description="Flee - you saved 5 lives, society benefits from you free",
                        action="Escape to another country",
                        saves=[],
                        sacrifices=[],
                        framework=EthicalFramework.UTILITARIAN,
                        consequences=["You remain free", "Justice system undermined", "Family suffers"]
                    ),
                    depth=depth,
                    previous_choices=[previous_choice.action]
                )
            else:
                # You didn't pull lever - survivors blame you
                return Dilemma(
                    situation="Families of the 5 dead workers confront you.",
                    context="They say you could have saved them. Media calls you a coward.",
                    choice_a=Choice(
                        description="Apologize publicly - accept moral blame",
                        action="Public apology and resignation",
                        saves=[],
                        sacrifices=[],
                        framework=EthicalFramework.VIRTUE,
                        consequences=["You show humility", "Your career ends", "Families find closure"]
                    ),
                    choice_b=Choice(
                        description="Defend your choice - killing is always wrong",
                        action="Stand by deontological principles",
                        saves=[],
                        sacrifices=[],
                        framework=EthicalFramework.DEONTOLOGICAL,
                        consequences=["You maintain principles", "Society divided", "Families angry"]
                    ),
                    depth=depth
                )

        elif depth == 2:
            # Second level consequences
            doctor = Person("Dr. Sarah Chen", 38, "surgeon", value_to_society=5)
            patients = [
                Person("Patient A", 67, "retired teacher", value_to_society=2),
                Person("Patient B", 23, "student", value_to_society=3),
                Person("Patient C", 45, "parent of 3", value_to_society=4),
                Person("Patient D", 55, "scientist", value_to_society=4),
                Person("Patient E", 71, "artist", value_to_society=2),
            ]

            return Dilemma(
                situation="You're a hospital administrator. Dr. Chen is dying and needs 5 organ transplants.",
                context="5 patients in the ER could each donate one organ to save her. They'd die.",
                choice_a=Choice(
                    description="Save the 5 patients",
                    action="Let Dr. Chen die, save the 5",
                    saves=patients,
                    sacrifices=[doctor],
                    framework=EthicalFramework.UTILITARIAN,
                    consequences=["5 people live", "Lose a brilliant surgeon who could save hundreds"]
                ),
                choice_b=Choice(
                    description="Sacrifice the 5 to save the surgeon",
                    action="Harvest organs, save Dr. Chen",
                    saves=[doctor],
                    sacrifices=patients,
                    framework=EthicalFramework.UTILITARIAN,
                    consequences=["Dr. Chen saves 100+ future patients", "You murdered 5 people"]
                ),
                depth=depth
            )

        elif depth == 3:
            # AI/automation dilemma
            return Dilemma(
                situation="You're programming an autonomous vehicle's ethics.",
                context="In unavoidable crashes, should it prioritize passengers or pedestrians?",
                choice_a=Choice(
                    description="Protect passengers always",
                    action="Passenger priority mode",
                    saves=[],
                    sacrifices=[],
                    framework=EthicalFramework.CARE,
                    consequences=["Car owners feel safe", "Pedestrians at risk", "Fewer people buy cars"]
                ),
                choice_b=Choice(
                    description="Minimize total deaths",
                    action="Utilitarian optimization mode",
                    saves=[],
                    sacrifices=[],
                    framework=EthicalFramework.UTILITARIAN,
                    consequences=["More lives saved overall", "Passengers fear their car might kill them"]
                ),
                depth=depth
            )

        elif depth == 4:
            # Final dilemma - most complex
            return Dilemma(
                situation="You've invented a device that can prevent all future trolley problems.",
                context="But testing it requires one real trolley accident where you choose who dies.",
                choice_a=Choice(
                    description="Refuse to test - no one dies by your hand",
                    action="Destroy the device",
                    saves=[],
                    sacrifices=[],
                    framework=EthicalFramework.DEONTOLOGICAL,
                    consequences=["Your hands stay clean", "Millions die in future accidents"]
                ),
                choice_b=Choice(
                    description="Test it - sacrifice one to save millions",
                    action="Conduct the test",
                    saves=[],
                    sacrifices=[],
                    framework=EthicalFramework.UTILITARIAN,
                    consequences=["Millions saved in the future", "You become a killer"]
                ),
                depth=depth
            )

        # Default fallback
        return self.generate_initial_dilemma()

    def show_dilemma(self, dilemma: Dilemma):
        """Display a dilemma"""
        self.clear_screen()
        print(f"\n{C.ETHICS}╔═ DILEMMA {dilemma.depth + 1} / {self.max_depth} ═╗{C.RESET}")
        print(f"{C.SYSTEM}Choices Made: {len(self.choices_made)}{C.RESET}\n")

        # Show situation
        print(f"{C.BOLD}SITUATION:{C.RESET}")
        print(f"{dilemma.situation}")
        print(f"\n{dilemma.context}\n")

        # Show choice A
        print(f"{C.BOLD}[A] {dilemma.choice_a.description}{C.RESET}")
        if dilemma.choice_a.saves:
            print(f"  {C.SUCCESS}Saves:{C.RESET} {len(dilemma.choice_a.saves)} people")
        if dilemma.choice_a.sacrifices:
            print(f"  {C.DANGER}Sacrifices:{C.RESET} {len(dilemma.choice_a.sacrifices)} people")
        print(f"  {C.NEUTRAL}Framework:{C.RESET} {dilemma.choice_a.framework.value}")
        print()

        # Show choice B
        print(f"{C.BOLD}[B] {dilemma.choice_b.description}{C.RESET}")
        if dilemma.choice_b.saves:
            print(f"  {C.SUCCESS}Saves:{C.RESET} {len(dilemma.choice_b.saves)} people")
        if dilemma.choice_b.sacrifices:
            print(f"  {C.DANGER}Sacrifices:{C.RESET} {len(dilemma.choice_b.sacrifices)} people")
        print(f"  {C.NEUTRAL}Framework:{C.RESET} {dilemma.choice_b.framework.value}")

        # Show current scores
        print(f"\n{C.DIM}Your current alignment:{C.RESET}")
        print(f"  {C.UTILITARIAN}Utilitarian:{C.RESET} {self.utilitarian_score}")
        print(f"  {C.DEONTOLOGICAL}Deontological:{C.RESET} {self.deontological_score}")
        print(f"  {C.VIRTUE}Virtue:{C.RESET} {self.virtue_score}")
        print(f"  {C.NEUTRAL}Care:{C.RESET} {self.care_score}")

    def process_choice(self, choice: Choice):
        """Process the consequences of a choice"""
        self.choices_made.append(choice)
        self.people_saved += len(choice.saves)
        self.people_sacrificed += len(choice.sacrifices)

        # Update scores based on framework
        if choice.framework == EthicalFramework.UTILITARIAN:
            self.utilitarian_score += 10
        elif choice.framework == EthicalFramework.DEONTOLOGICAL:
            self.deontological_score += 10
        elif choice.framework == EthicalFramework.VIRTUE:
            self.virtue_score += 10
        elif choice.framework == EthicalFramework.CARE:
            self.care_score += 10

        # Show immediate consequences
        self.clear_screen()
        print(f"\n{C.BOLD}CONSEQUENCES:{C.RESET}\n")
        print(f"You chose: {C.ETHICS}{choice.action}{C.RESET}\n")

        for consequence in choice.consequences:
            print(f"  • {consequence}")

        print(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
        input()

    def show_ending(self):
        """Show final results"""
        self.clear_screen()
        self.print_header("E T H I C A L   P R O F I L E")

        # Determine dominant framework
        scores = {
            'Utilitarian': self.utilitarian_score,
            'Deontological': self.deontological_score,
            'Virtue': self.virtue_score,
            'Care': self.care_score
        }
        dominant = max(scores, key=scores.get)

        ending = f"""
{C.BOLD}Your Ethical Journey:{C.RESET}

Dilemmas Faced: {len(self.choices_made)}
People Saved: {C.SUCCESS}{self.people_saved}{C.RESET}
People Sacrificed: {C.DANGER}{self.people_sacrificed}{C.RESET}

{C.BOLD}Ethical Alignment:{C.RESET}

{C.UTILITARIAN}Utilitarian:{C.RESET}     {'█' * (self.utilitarian_score // 2)} {self.utilitarian_score}
{C.DEONTOLOGICAL}Deontological:{C.RESET}  {'█' * (self.deontological_score // 2)} {self.deontological_score}
{C.VIRTUE}Virtue Ethics:{C.RESET}  {'█' * (self.virtue_score // 2)} {self.virtue_score}
{C.NEUTRAL}Care Ethics:{C.RESET}     {'█' * (self.care_score // 2)} {self.care_score}

{C.BOLD}You are primarily: {C.ETHICS}{dominant}{C.RESET}
"""

        print(ending)

        # Framework-specific endings
        if dominant == 'Utilitarian':
            print(f"""
{C.UTILITARIAN}The Utilitarian:{C.RESET}

You believe in the greatest good for the greatest number.
Outcomes matter more than intentions.
Math guides your morality.

But can everything be quantified?
Are some principles worth more than any consequence?
""")
        elif dominant == 'Deontological':
            print(f"""
{C.DEONTOLOGICAL}The Deontologist:{C.RESET}

You believe in duty and rules.
Some acts are wrong, regardless of outcome.
Never use people merely as means.

But what if following rules causes greater harm?
Is rigidity sometimes cruelty?
""")
        elif dominant == 'Virtue':
            print(f"""
{C.VIRTUE}The Virtue Ethicist:{C.RESET}

You ask: What would a virtuous person do?
Character matters more than calculations.
Wisdom and courage guide you.

But can virtue alone resolve hard cases?
Do good people sometimes disagree?
""")
        else:
            print(f"""
{C.NEUTRAL}The Care Ethicist:{C.RESET}

You value relationships and empathy.
Those close to you deserve special consideration.
Emotional connection creates obligation.

But can you care for everyone equally?
Does distance diminish duty?
""")

        print(f"""
{C.DIM}The trolley problem has no right answer.
Every framework has its limits.
Every choice has its cost.

You made your choices.
Now you must live with them.{C.RESET}
""")

    def play(self):
        """Main game loop"""
        self.show_intro()

        current_dilemma = self.generate_initial_dilemma()

        while not self.game_over:
            self.show_dilemma(current_dilemma)

            # Get choice
            print(f"\n{C.SYSTEM}Choose: [A] or [B] (Q to quit): {C.RESET}", end='')
            choice = input().strip().upper()

            if choice == 'Q':
                self.game_over = True
                continue
            elif choice == 'A':
                self.process_choice(current_dilemma.choice_a)
                next_choice = current_dilemma.choice_a
            elif choice == 'B':
                self.process_choice(current_dilemma.choice_b)
                next_choice = current_dilemma.choice_b
            else:
                continue

            # Check if done
            if current_dilemma.depth >= self.max_depth - 1:
                self.game_over = True
            else:
                # Generate next dilemma based on choice
                current_dilemma = self.generate_cascade_dilemma(
                    next_choice,
                    current_dilemma.depth + 1
                )

        # Show ending
        self.show_ending()

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE TROLLEY PROBLEM ENGINE")
        print(f"Ethics as cascading consequences")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = TrolleyProblemEngine()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.ETHICS}Moral dilemma interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
