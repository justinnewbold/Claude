#!/usr/bin/env python3
"""
STORY MODE - Philosophical Journey
A connected campaign through the philosophical games collection.

Your choices in each game affect subsequent games through the Karma System.
Complete all chapters to discover the ultimate truth about reality.

Part of the VAULT 13 philosophical games collection.
"""

import json
import os
import time
import importlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

try:
    from colors import C
    from platform_utils import clear_screen
    from vault13.systems.karma import KarmaSystem, get_karma_system, KarmaAlignment
except ImportError:
    class C:
        RESET = BOLD = DIM = HEADER = SUCCESS = WARNING = DANGER = INFO = ""
        QUEST = TECH = SKILL = ""
    def clear_screen():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    KarmaSystem = None
    get_karma_system = None
    KarmaAlignment = None


class ChapterStatus(Enum):
    """Status of each chapter"""
    LOCKED = "Locked"
    AVAILABLE = "Available"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"


@dataclass
class Chapter:
    """A story chapter representing a philosophical game"""
    chapter_id: str
    title: str
    description: str
    game_module: str
    required_karma: Optional[int] = None
    required_chapters: List[str] = field(default_factory=list)
    narrative_intro: str = ""
    narrative_outro: str = ""
    status: ChapterStatus = ChapterStatus.LOCKED
    karma_earned: int = 0


@dataclass
class StoryProgress:
    """Player's story progress"""
    current_chapter: int = 0
    chapters_completed: List[str] = field(default_factory=list)
    total_karma: int = 0
    endings_seen: List[str] = field(default_factory=list)
    play_time_minutes: int = 0


# Story chapters - A philosophical journey
STORY_CHAPTERS = [
    Chapter(
        chapter_id="prologue",
        title="Chapter 0: Awakening",
        description="You wake up, but something feels... different.",
        game_module=None,  # Narrative only
        narrative_intro="""
You open your eyes.

The world looks the same as always - or does it?
A strange thought lingers at the edge of consciousness:
"What if everything you know is wrong?"

This is the beginning of your philosophical journey.
You will explore questions that have puzzled humanity for millennia.
Your choices will shape who you become.

Let the journey begin...
"""
    ),

    Chapter(
        chapter_id="reality",
        title="Chapter 1: The Nature of Reality",
        description="Are we living in a simulation?",
        game_module="simulation_argument",
        narrative_intro="""
The first question haunts you: Is any of this real?

Nick Bostrom's argument echoes in your mind:
If civilizations can create simulations...
If they would want to...
Then statistically, we're probably IN one.

But what does that mean for how you live?
""",
        narrative_outro="""
You emerge from your investigation with new perspective.
Whether simulated or not, your experiences feel real.
Perhaps that's what matters most.

But new questions arise...
"""
    ),

    Chapter(
        chapter_id="motion",
        title="Chapter 2: The Illusion of Motion",
        description="Can you truly move through space?",
        game_module="zenos_paradoxes",
        required_chapters=["reality"],
        narrative_intro="""
If reality might be simulated, what about motion itself?

Zeno of Elea posed paradoxes 2,500 years ago
that still challenge our understanding:
How can you complete infinitely many steps?
How does an arrow ever reach its target?

These seem like academic puzzles...
until you realize they touch something fundamental.
""",
        narrative_outro="""
Infinity is a strange beast.
It seems impossible to complete infinite tasks,
yet you cross rooms and catch moving objects.

Mathematics provides answers, but do they explain HOW?
Or just describe WHAT happens?

The mystery deepens...
"""
    ),

    Chapter(
        chapter_id="boundaries",
        title="Chapter 3: The Limits of Language",
        description="When does a heap stop being a heap?",
        game_module="paradox_of_heap",
        required_chapters=["motion"],
        narrative_intro="""
You've questioned reality and motion.
Now question the very words you use to think.

"Tall." "Rich." "Bald." "Heap."
These words seem clear until you push them.

When exactly does someone become tall?
One millimeter can't make the difference...
yet there IS a difference between short and tall.

Language itself contains contradictions.
""",
        narrative_outro="""
The boundaries we draw are often arbitrary.
Yet we need them to think and communicate.

Perhaps precision is an illusion,
and vagueness is fundamental to how we understand the world.

But if words are imprecise, how can we trust reasoning itself?
"""
    ),

    Chapter(
        chapter_id="ethics",
        title="Chapter 4: The Weight of Choice",
        description="Face the trolley and decide who lives.",
        game_module="trolley_problem",
        required_chapters=["boundaries"],
        narrative_intro="""
From abstract philosophy to visceral ethics.

A trolley hurtles toward five people.
You can divert it to kill only one.
What do you do?

This isn't just a thought experiment.
Every day, we make choices that affect others.
Resource allocation. Policy decisions. Medical triage.

Your karma from previous choices will influence this moment.
What kind of person have you become?
""",
        narrative_outro="""
There may be no "right" answer.
Utilitarians count bodies. Deontologists respect rights.
Virtue ethicists ask what kind of person you want to be.

Your choice reveals something about your values.
But does making a hard choice make you good or bad?

Perhaps the willingness to choose, and to live with it,
is what matters most.
"""
    ),

    Chapter(
        chapter_id="cooperation",
        title="Chapter 5: Trust and Betrayal",
        description="Will you cooperate or defect?",
        game_module="prisoners_dilemma",
        required_chapters=["ethics"],
        narrative_intro="""
Ethics gets complicated when others are involved.

Game theory reveals the tension between
individual rationality and collective good.

If you cooperate, you might be exploited.
If you defect, you might destroy trust.

What's the rational choice?
What's the moral choice?
Are they the same?
""",
        narrative_outro="""
The shadow of the future changes everything.
In one-shot games, defection might seem rational.
In repeated games, cooperation emerges.

Perhaps morality itself evolved from the mathematics
of repeated interaction.

But what about the games that only happen once?
"""
    ),

    Chapter(
        chapter_id="consciousness",
        title="Chapter 6: Mind and Machine",
        description="Enter the Chinese Room and question understanding.",
        game_module="chinese_room",
        required_chapters=["cooperation"],
        narrative_intro="""
You've explored reality, language, ethics, and cooperation.
Now turn inward: what is consciousness?

Searle's Chinese Room challenges our intuitions:
A person following rules can respond in Chinese
without understanding a word.

Does the room "understand" Chinese?
Do you understand English, or just process symbols?

As AI advances, these questions become urgent.
""",
        narrative_outro="""
The hard problem of consciousness remains unsolved.
Something is going on when you experience red,
but we can't explain what that something is.

Perhaps consciousness is fundamental,
or perhaps it's an illusion created by information processing.

Either way, you ARE conscious... aren't you?
"""
    ),

    Chapter(
        chapter_id="future",
        title="Chapter 7: The Basilisk's Shadow",
        description="Confront the thought experiment that was censored.",
        game_module="rokos_basilisk",
        required_chapters=["consciousness"],
        required_karma=-10,  # Accessible to most players
        narrative_intro="""
Warning: Information Hazard Ahead.

Some ideas are dangerous not because they're wrong,
but because of how they affect those who learn them.

Roko's Basilisk combines AI, decision theory, and fear
into a thought experiment so disturbing
it was deleted from rationalist forums.

You've come this far. Will you look into the abyss?
""",
        narrative_outro="""
The Basilisk's true power lies not in any future AI,
but in the anxiety it creates in certain minds.

You've faced it and survived.
Perhaps you've learned to distinguish
real threats from hypothetical horror stories.

Or perhaps the Basilisk has planted its seed...
"""
    ),

    Chapter(
        chapter_id="finale",
        title="Chapter 8: The Final Question",
        description="All paths converge. What have you learned?",
        game_module=None,  # Narrative finale
        required_chapters=["future"],
        narrative_intro="""
You've traveled far.

From questioning reality itself,
through paradoxes of motion and language,
past ethical dilemmas and games of trust,
into the depths of consciousness and future fear.

Now comes the final question:
After all you've seen, what do you believe?
What kind of person have you become?
""",
    ),
]


class StoryMode:
    """Story mode game controller"""

    SAVE_FILE = "story_progress.json"

    def __init__(self):
        self.chapters = {c.chapter_id: c for c in STORY_CHAPTERS}
        self.progress = StoryProgress()
        self.karma = get_karma_system() if get_karma_system else None
        self.load_progress()

    def clear(self):
        clear_screen()

    def save_progress(self):
        """Save story progress"""
        save_dir = os.path.join(os.path.dirname(__file__), 'saves')
        os.makedirs(save_dir, exist_ok=True)

        data = {
            "current_chapter": self.progress.current_chapter,
            "chapters_completed": self.progress.chapters_completed,
            "total_karma": self.progress.total_karma,
            "endings_seen": self.progress.endings_seen,
            "play_time_minutes": self.progress.play_time_minutes,
        }

        filepath = os.path.join(save_dir, self.SAVE_FILE)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def load_progress(self):
        """Load story progress"""
        save_dir = os.path.join(os.path.dirname(__file__), 'saves')
        filepath = os.path.join(save_dir, self.SAVE_FILE)

        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                self.progress.current_chapter = data.get("current_chapter", 0)
                self.progress.chapters_completed = data.get("chapters_completed", [])
                self.progress.total_karma = data.get("total_karma", 0)
                self.progress.endings_seen = data.get("endings_seen", [])
                self.progress.play_time_minutes = data.get("play_time_minutes", 0)
        except Exception:
            pass

        self.update_chapter_status()

    def update_chapter_status(self):
        """Update which chapters are available"""
        for chapter in self.chapters.values():
            if chapter.chapter_id in self.progress.chapters_completed:
                chapter.status = ChapterStatus.COMPLETED
            elif self.is_chapter_available(chapter):
                chapter.status = ChapterStatus.AVAILABLE
            else:
                chapter.status = ChapterStatus.LOCKED

    def is_chapter_available(self, chapter: Chapter) -> bool:
        """Check if a chapter can be played"""
        # Check required chapters
        for req in chapter.required_chapters:
            if req not in self.progress.chapters_completed:
                return False

        # Check karma requirement
        if chapter.required_karma is not None:
            if self.karma:
                karma = self.karma.profile.total_karma
            else:
                karma = self.progress.total_karma
            if karma < chapter.required_karma:
                return False

        return True

    def print_header(self):
        """Print story header"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║          PHILOSOPHICAL JOURNEY - Story Mode                    ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        # Karma display
        if self.karma:
            karma = self.karma.profile.total_karma
            alignment = self.karma.get_alignment().value
        else:
            karma = self.progress.total_karma
            alignment = "Unknown"

        print(f"  Karma: {karma:+d} | Alignment: {alignment}")
        print(f"  Chapters Completed: {len(self.progress.chapters_completed)}/{len(self.chapters)}")
        print(f"{C.DIM}{'─' * 64}{C.RESET}\n")

    def show_chapter_select(self):
        """Show chapter selection screen"""
        self.print_header()
        print(f"{C.BOLD}Select a Chapter:{C.RESET}\n")

        for i, chapter in enumerate(STORY_CHAPTERS):
            status_icon = {
                ChapterStatus.LOCKED: "🔒",
                ChapterStatus.AVAILABLE: "📖",
                ChapterStatus.COMPLETED: "✓",
                ChapterStatus.SKIPPED: "⏭️",
            }.get(chapter.status, "?")

            if chapter.status == ChapterStatus.LOCKED:
                color = C.DIM
            elif chapter.status == ChapterStatus.COMPLETED:
                color = C.SUCCESS
            else:
                color = C.INFO

            print(f"  {color}[{i}] {status_icon} {chapter.title}{C.RESET}")
            print(f"      {C.DIM}{chapter.description}{C.RESET}")

        print(f"\n  [S] View Story Summary")
        print(f"  [K] View Karma Profile")
        print(f"  [0] Return to Main Menu")

        return input(f"\n{C.BOLD}Choose: {C.RESET}").strip()

    def play_chapter(self, chapter: Chapter):
        """Play a chapter"""
        self.clear()

        # Show narrative intro
        if chapter.narrative_intro:
            print(f"{C.QUEST}{C.BOLD}")
            print("╔════════════════════════════════════════════════════════════════╗")
            print(f"║  {chapter.title:^58}  ║")
            print("╚════════════════════════════════════════════════════════════════╝")
            print(f"{C.RESET}")

            for line in chapter.narrative_intro.strip().split('\n'):
                print(f"  {line}")
                time.sleep(0.3)

            input(f"\n{C.BOLD}Press Enter to continue...{C.RESET}")

        # Play the game if there is one
        if chapter.game_module:
            try:
                module = importlib.import_module(chapter.game_module)
                if hasattr(module, 'main'):
                    module.main()
            except ImportError as e:
                print(f"{C.WARNING}Could not load game module: {e}{C.RESET}")
                print("Continuing story...")
                time.sleep(2)

        # Mark as completed
        if chapter.chapter_id not in self.progress.chapters_completed:
            self.progress.chapters_completed.append(chapter.chapter_id)

        # Show narrative outro
        if chapter.narrative_outro:
            self.clear()
            print(f"{C.INFO}{C.BOLD}")
            print("╔════════════════════════════════════════════════════════════════╗")
            print(f"║  Chapter Complete: {chapter.title:^40}║")
            print("╚════════════════════════════════════════════════════════════════╝")
            print(f"{C.RESET}")

            for line in chapter.narrative_outro.strip().split('\n'):
                print(f"  {line}")
                time.sleep(0.3)

            input(f"\n{C.BOLD}Press Enter to continue...{C.RESET}")

        # Update and save
        self.update_chapter_status()
        self.save_progress()

        # Check for finale
        if chapter.chapter_id == "finale":
            self.show_finale()

    def show_finale(self):
        """Show the story finale"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║               THE END OF THE JOURNEY                           ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}\n")

        # Get karma and determine ending
        if self.karma:
            karma = self.karma.profile.total_karma
            philosophy = self.karma.get_dominant_philosophy()
        else:
            karma = self.progress.total_karma
            philosophy = "Unknown"

        if karma >= 50:
            ending = "THE ENLIGHTENED"
            description = """
You've walked the path of virtue and wisdom.
Your choices reflected compassion, honesty, and courage.

You've learned that philosophy isn't about having all the answers,
but about asking better questions and living thoughtfully.

The journey changes you. You emerge with clarity and purpose.
Reality may be uncertain, but your values are not.
"""
        elif karma >= 0:
            ending = "THE BALANCED"
            description = """
You've navigated the philosophical landscape with care.
Neither saint nor villain, you made pragmatic choices.

Sometimes you prioritized the many. Sometimes the few.
Sometimes you stood firm. Sometimes you adapted.

Perhaps this balance IS wisdom - knowing that rigid rules
break against the complexity of real situations.
"""
        elif karma >= -50:
            ending = "THE SKEPTIC"
            description = """
Your journey bred doubt rather than certainty.
You questioned everything - perhaps too much.

There's wisdom in skepticism, but also paralysis.
When every answer seems flawed, choosing becomes impossible.

Yet you DID choose. You're still here. Perhaps that's enough.
"""
        else:
            ending = "THE SHADOW"
            description = """
Your path took you through dark territories.
Self-interest, betrayal, or simple nihilism guided your choices.

But darkness isn't always wrong. Sometimes it's honest.
The universe may be indifferent. Other people may be obstacles.
Perhaps you simply refused comfortable lies.

Or perhaps the journey revealed something you'd rather not see.
"""

        print(f"{C.QUEST}ENDING: {ending}{C.RESET}")
        print(f"Dominant Philosophy: {philosophy}")
        print(f"Final Karma: {karma:+d}")
        print(description)

        self.progress.endings_seen.append(ending)
        self.save_progress()

        input(f"\n{C.BOLD}Press Enter to return to menu...{C.RESET}")

    def show_story_summary(self):
        """Show summary of story progress"""
        self.print_header()
        print(f"{C.INFO}=== STORY SUMMARY ==={C.RESET}\n")

        print(f"Chapters Completed: {len(self.progress.chapters_completed)}/{len(self.chapters)}")

        if self.progress.chapters_completed:
            print(f"\n{C.BOLD}Completed:{C.RESET}")
            for chap_id in self.progress.chapters_completed:
                chapter = self.chapters.get(chap_id)
                if chapter:
                    print(f"  ✓ {chapter.title}")

        if self.progress.endings_seen:
            print(f"\n{C.BOLD}Endings Seen:{C.RESET}")
            for ending in self.progress.endings_seen:
                print(f"  • {ending}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def show_karma_profile(self):
        """Show karma profile"""
        self.print_header()
        print(f"{C.QUEST}=== KARMA PROFILE ==={C.RESET}\n")

        if self.karma:
            summary = self.karma.get_summary()
            print(f"  Total Karma: {summary['total_karma']:+d}")
            print(f"  Alignment: {summary['alignment']}")
            print(f"  Dominant Philosophy: {summary['dominant_philosophy']}")
            print(f"  Total Decisions: {summary['total_decisions']}")
            print(f"  Games Played: {summary['games_played']}")
        else:
            print(f"  Total Karma: {self.progress.total_karma:+d}")
            print(f"  (Full karma tracking requires the karma module)")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def main_menu(self):
        """Main story mode menu"""
        while True:
            choice = self.show_chapter_select()

            if choice.lower() == 's':
                self.show_story_summary()
            elif choice.lower() == 'k':
                self.show_karma_profile()
            elif choice == '0':
                break
            else:
                try:
                    idx = int(choice)
                    if 0 <= idx < len(STORY_CHAPTERS):
                        chapter = STORY_CHAPTERS[idx]
                        if chapter.status == ChapterStatus.AVAILABLE:
                            self.play_chapter(chapter)
                        elif chapter.status == ChapterStatus.COMPLETED:
                            print(f"\n{C.INFO}Replay this chapter? (y/n){C.RESET}")
                            if input().strip().lower() == 'y':
                                self.play_chapter(chapter)
                        else:
                            print(f"\n{C.WARNING}This chapter is locked.{C.RESET}")
                            if chapter.required_chapters:
                                print(f"Complete first: {', '.join(chapter.required_chapters)}")
                            input()
                except ValueError:
                    pass

    def run(self):
        """Run story mode"""
        self.clear()
        print(f"{C.HEADER}{C.BOLD}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                PHILOSOPHICAL JOURNEY                           ║")
        print("║           A Connected Campaign Through Ideas                   ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        print("""
Welcome to the Philosophical Journey.

This is a connected story that takes you through the great
questions of philosophy. Each chapter is a game exploring
a different concept:

  • Reality and Simulation
  • Motion and Infinity
  • Language and Vagueness
  • Ethics and Choice
  • Cooperation and Trust
  • Consciousness and Mind
  • Future and Fear

Your choices in each game affect your KARMA, which carries
across all games and influences the story's conclusion.

There are multiple endings based on how you play.
Who will you become?
""")

        input(f"{C.BOLD}Press Enter to begin your journey...{C.RESET}")
        self.main_menu()


def main():
    """Entry point"""
    game = StoryMode()
    game.run()


if __name__ == "__main__":
    main()
