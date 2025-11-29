#!/usr/bin/env python3
"""
VAULT 13 - THE FULL VAULT SHELTER v10.0
========================================
Progression System: 12 Training Vaults Leading to the Main Experience

Features:
- Linear unlock progression: Must beat each vault once to unlock the next
- Replay freedom: Can replay any unlocked vault anytime
- Fragment narrative: Story pieces revealed with each vault completion
- Star rating system: 1-3 stars per vault for mastery/replayability
"""

import json
import os
import random
import time
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from enum import Enum

# Import platform utilities for save paths
try:
    from platform_utils import get_save_dir, get_app_data_dir
except ImportError:
    def get_save_dir(app_name="vault13"):
        return Path.home() / f'.{app_name}' / 'saves'
    def get_app_data_dir(app_name="vault13"):
        return Path.home() / f'.{app_name}'


# =============================================================================
# ANSI COLORS
# =============================================================================

class C:
    """ANSI Color codes for the terminal UI"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'

    # Vault theme colors
    HEADER = '\033[38;5;51m'      # Cyan
    BORDER = '\033[38;5;39m'      # Blue
    SUCCESS = '\033[38;5;46m'     # Green
    WARNING = '\033[38;5;226m'    # Yellow
    DANGER = '\033[38;5;196m'     # Red
    INFO = '\033[38;5;159m'       # Light cyan
    LOCKED = '\033[38;5;240m'     # Dark gray
    UNLOCKED = '\033[38;5;250m'   # Light gray
    COMPLETED = '\033[38;5;46m'   # Green
    STAR = '\033[38;5;226m'       # Gold/Yellow
    FRAGMENT = '\033[38;5;213m'   # Pink/Magenta
    VAULT = '\033[38;5;208m'      # Orange
    FINALE = '\033[38;5;201m'     # Bright magenta


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


# =============================================================================
# TRAINING VAULT DEFINITIONS
# =============================================================================

@dataclass
class TrainingVault:
    """Definition of a training vault (mini-game)"""
    id: str
    number: int  # 1-12
    name: str
    file: str
    description: str
    theme: str
    difficulty: int  # 1-3
    # Star thresholds for rating
    star_thresholds: Dict[str, int] = field(default_factory=dict)
    # Narrative fragment revealed on first completion
    fragment: str = ""
    # Tips for getting 3 stars
    mastery_hint: str = ""


# The 12 Training Vaults - Ordered for thematic progression
TRAINING_VAULTS: List[TrainingVault] = [
    # ACT 1: Foundations of Thought (Vaults 1-4)
    TrainingVault(
        id="platos_cave",
        number=1,
        name="Plato's Cave",
        file="platos_cave.py",
        description="Question the nature of reality and perception",
        theme="Philosophy",
        difficulty=1,
        star_thresholds={"time": 300, "choices": 5, "ending": "enlightenment"},
        fragment="FRAGMENT 1/12: 'The shadows we see are but echoes of truth...'",
        mastery_hint="Seek all three perspectives before making your choice"
    ),
    TrainingVault(
        id="prisoners_dilemma",
        number=2,
        name="Prisoner's Dilemma",
        file="prisoners_dilemma.py",
        description="Learn the foundations of cooperation and trust",
        theme="Game Theory",
        difficulty=1,
        star_thresholds={"wins": 7, "cooperations": 5, "score": 100},
        fragment="FRAGMENT 2/12: '...in the depths of Vault 13, trust was currency...'",
        mastery_hint="Cooperation breeds cooperation. Tit-for-tat wins wars."
    ),
    TrainingVault(
        id="monty_hall",
        number=3,
        name="Monty Hall",
        file="monty_hall.py",
        description="Master probability and counterintuitive thinking",
        theme="Probability",
        difficulty=1,
        star_thresholds={"correct_switches": 5, "win_rate": 0.6, "rounds": 10},
        fragment="FRAGMENT 3/12: '...the Overseer always offered a choice: stay or switch...'",
        mastery_hint="Always switch. The math is clear."
    ),
    TrainingVault(
        id="trolley_problem",
        number=4,
        name="Trolley Problem",
        file="trolley_problem.py",
        description="Confront moral dilemmas with no right answer",
        theme="Ethics",
        difficulty=2,
        star_thresholds={"scenarios": 5, "consistency": 0.8, "reflection": True},
        fragment="FRAGMENT 4/12: '...but when the lever appeared, every dweller froze...'",
        mastery_hint="Consistency in ethics reveals character. Choose wisely, but choose."
    ),

    # ACT 2: Mind and Machine (Vaults 5-8)
    TrainingVault(
        id="chinese_room",
        number=5,
        name="The Chinese Room",
        file="chinese_room.py",
        description="Explore consciousness and the nature of understanding",
        theme="Philosophy of Mind",
        difficulty=2,
        star_thresholds={"translations": 10, "insight_score": 80, "ending": "understanding"},
        fragment="FRAGMENT 5/12: '...the vault's AI passed every test, yet understood nothing...'",
        mastery_hint="Syntax is not semantics. Look beyond the symbols."
    ),
    TrainingVault(
        id="ship_of_theseus",
        number=6,
        name="Ship of Theseus",
        file="ship_of_theseus.py",
        description="Question identity through gradual transformation",
        theme="Identity",
        difficulty=2,
        star_thresholds={"repairs": 10, "identity_score": 90, "philosophical_depth": 3},
        fragment="FRAGMENT 6/12: '...piece by piece, Vault 13 was rebuilt, but was it still home?...'",
        mastery_hint="Every plank tells a story. Replace with intention."
    ),
    TrainingVault(
        id="butterfly_effect",
        number=7,
        name="The Butterfly Effect",
        file="butterfly_effect.py",
        description="Witness how small changes cascade into chaos",
        theme="Chaos Theory",
        difficulty=2,
        star_thresholds={"predictions": 5, "cascade_control": 3, "optimal_outcome": True},
        fragment="FRAGMENT 7/12: '...one wrong decision in the generator room, and...'",
        mastery_hint="The smallest flutter can topple empires. Plan three moves ahead."
    ),
    TrainingVault(
        id="halting_problem",
        number=8,
        name="The Halting Problem",
        file="halting_problem.py",
        description="Face the limits of computation and knowledge",
        theme="Computation",
        difficulty=3,
        star_thresholds={"programs_analyzed": 15, "correct_predictions": 12, "paradox_solved": True},
        fragment="FRAGMENT 8/12: '...the vault's computer ran endlessly, seeking an answer that didn't exist...'",
        mastery_hint="Some programs halt. Some don't. Knowing which is the key."
    ),

    # ACT 3: Quantum Uncertainty (Vaults 9-10)
    TrainingVault(
        id="schrodingers_dungeon",
        number=9,
        name="Schrodinger's Dungeon",
        file="schrodingers_dungeon.py",
        description="Navigate a dungeon of quantum superposition",
        theme="Quantum Mechanics",
        difficulty=3,
        star_thresholds={"levels_cleared": 5, "superposition_mastery": 0.8, "cat_saved": True},
        fragment="FRAGMENT 9/12: '...in Vault 13's deepest level, doors were both open and closed...'",
        mastery_hint="Observation collapses possibility. Choose when to look."
    ),
    TrainingVault(
        id="echo_chambers",
        number=10,
        name="Echo Chambers",
        file="echo_chambers.py",
        description="Navigate decaying timelines and parallel echoes",
        theme="Parallel Timelines",
        difficulty=3,
        star_thresholds={"echoes_collected": 10, "timeline_stability": 0.9, "perfect_sync": True},
        fragment="FRAGMENT 10/12: '...each echo whispered a different history of the vault...'",
        mastery_hint="Listen to all echoes before committing to a timeline."
    ),

    # ACT 4: Ultimate Truth (Vaults 11-12)
    TrainingVault(
        id="bootstrap_paradox",
        number=11,
        name="Bootstrap Paradox",
        file="bootstrap_paradox.py",
        description="Unravel the mysteries of time and causality",
        theme="Time Travel",
        difficulty=3,
        star_thresholds={"loops_resolved": 3, "paradox_score": 100, "origin_found": True},
        fragment="FRAGMENT 11/12: '...the message that started it all came from Vault 13's future...'",
        mastery_hint="The origin may not exist. Create meaning from the loop."
    ),
    TrainingVault(
        id="simulation_hypothesis",
        number=12,
        name="Simulation Hypothesis",
        file="simulation_hypothesis.py",
        description="Question the very nature of your existence",
        theme="Reality",
        difficulty=3,
        star_thresholds={"layers_discovered": 5, "truth_score": 100, "awakening": True},
        fragment="FRAGMENT 12/12: '...and the Overseer finally understood: Vault 13 was a test all along.'",
        mastery_hint="Base reality is a construct. The simulation is the message."
    ),
]


# =============================================================================
# PROGRESSION DATA MODEL
# =============================================================================

@dataclass
class VaultProgress:
    """Progress for a single vault"""
    vault_id: str
    completed: bool = False
    best_stars: int = 0  # 0-3
    times_played: int = 0
    best_score: int = 0
    fastest_time: Optional[float] = None
    fragment_unlocked: bool = False
    first_completed_date: Optional[str] = None


@dataclass
class PlayerProgression:
    """Overall player progression state"""
    # Vault completion tracking
    vault_progress: Dict[str, VaultProgress] = field(default_factory=dict)

    # Total stars earned
    total_stars: int = 0

    # Narrative fragments collected
    fragments_collected: List[str] = field(default_factory=list)

    # The finale (Vault 13 main game) unlocked
    finale_unlocked: bool = False
    finale_completed: bool = False

    # Meta stats
    total_playtime_seconds: float = 0.0
    first_played_date: Optional[str] = None
    last_played_date: Optional[str] = None

    # Achievements
    achievements: List[str] = field(default_factory=list)

    def get_highest_unlocked_vault(self) -> int:
        """Get the highest vault number that is unlocked"""
        # Vault 1 is always unlocked
        highest = 1
        for i, vault in enumerate(TRAINING_VAULTS, 1):
            if vault.id in self.vault_progress:
                progress = self.vault_progress[vault.id]
                if progress.completed:
                    highest = min(i + 1, 12)  # Unlock next, max 12
        return highest

    def is_vault_unlocked(self, vault_number: int) -> bool:
        """Check if a specific vault is unlocked"""
        if vault_number == 1:
            return True
        return vault_number <= self.get_highest_unlocked_vault()

    def is_vault_completed(self, vault_id: str) -> bool:
        """Check if a vault has been completed at least once"""
        if vault_id in self.vault_progress:
            return self.vault_progress[vault_id].completed
        return False

    def get_vault_stars(self, vault_id: str) -> int:
        """Get the best star rating for a vault"""
        if vault_id in self.vault_progress:
            return self.vault_progress[vault_id].best_stars
        return 0

    def count_completed_vaults(self) -> int:
        """Count total vaults completed"""
        return sum(1 for p in self.vault_progress.values() if p.completed)

    def check_finale_unlock(self) -> bool:
        """Check if all 12 vaults are completed to unlock the finale"""
        completed = self.count_completed_vaults()
        if completed >= 12 and not self.finale_unlocked:
            self.finale_unlocked = True
            return True
        return False


# =============================================================================
# STAR RATING SYSTEM
# =============================================================================

class StarRating:
    """Calculates star ratings based on performance"""

    @staticmethod
    def calculate_stars(vault: TrainingVault, performance: Dict) -> int:
        """
        Calculate 1-3 stars based on performance metrics.

        Performance dict can contain:
        - time: seconds taken
        - score: numeric score
        - completion_percentage: 0.0-1.0
        - special_achievements: list of achievements
        """
        stars = 1  # Base star for completion

        # Check various performance metrics
        thresholds = vault.star_thresholds

        # Time-based bonus
        if "time" in performance and "time" in thresholds:
            if performance["time"] <= thresholds["time"]:
                stars += 1

        # Score-based bonus
        if "score" in performance and "score" in thresholds:
            if performance["score"] >= thresholds["score"]:
                stars += 1

        # Completion percentage bonus
        if "completion" in performance:
            if performance["completion"] >= 0.9:
                stars = max(stars, 2)
            if performance["completion"] >= 1.0:
                stars = 3

        # Special achievement bonus
        if "special" in performance and performance["special"]:
            stars = min(stars + 1, 3)

        return min(stars, 3)

    @staticmethod
    def render_stars(count: int, max_stars: int = 3) -> str:
        """Render star display"""
        filled = C.STAR + "★" * count + C.RESET
        empty = C.DIM + "☆" * (max_stars - count) + C.RESET
        return filled + empty


# =============================================================================
# NARRATIVE FRAGMENT SYSTEM
# =============================================================================

# The full narrative that fragments piece together
VAULT_13_NARRATIVE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     THE STORY OF VAULT 13                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

In the aftermath of the Great War, Vault 13 was sealed with 1,000 souls inside.
But this vault was different. It wasn't designed for survival—it was designed
for evolution.

The shadows we see are but echoes of truth... in the depths of Vault 13, trust
was currency... the Overseer always offered a choice: stay or switch... but
when the lever appeared, every dweller froze...

The vault's AI passed every test, yet understood nothing... piece by piece,
Vault 13 was rebuilt, but was it still home?... one wrong decision in the
generator room, and... the vault's computer ran endlessly, seeking an answer
that didn't exist...

In Vault 13's deepest level, doors were both open and closed... each echo
whispered a different history of the vault... the message that started it all
came from Vault 13's future...

And the Overseer finally understood: Vault 13 was a test all along.

The training wasn't for survival. It was for transcendence.

Now, Overseer, you have learned:
  - To question reality
  - To cooperate and compete
  - To calculate odds
  - To make impossible choices
  - To understand understanding
  - To preserve identity through change
  - To predict chaos
  - To accept limits
  - To embrace uncertainty
  - To hear all timelines
  - To create causality
  - To see through the simulation

You are ready.

VAULT 13 AWAITS.
"""

class NarrativeSystem:
    """Manages the fragment narrative system"""

    @staticmethod
    def get_fragment(vault_id: str) -> Optional[str]:
        """Get the narrative fragment for a vault"""
        for vault in TRAINING_VAULTS:
            if vault.id == vault_id:
                return vault.fragment
        return None

    @staticmethod
    def render_collected_fragments(progression: PlayerProgression) -> str:
        """Render all collected fragments as a narrative"""
        lines = []
        lines.append(f"\n{C.FRAGMENT}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        lines.append(f"{C.FRAGMENT}{C.BOLD}║                    NARRATIVE FRAGMENTS                               ║{C.RESET}")
        lines.append(f"{C.FRAGMENT}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}\n")

        if not progression.fragments_collected:
            lines.append(f"{C.DIM}No fragments collected yet. Complete vaults to reveal the story...{C.RESET}")
        else:
            for i, fragment in enumerate(sorted(progression.fragments_collected), 1):
                lines.append(f"{C.FRAGMENT}  {fragment}{C.RESET}")
                lines.append("")

        collected = len(progression.fragments_collected)
        total = 12

        lines.append(f"\n{C.DIM}Fragments collected: {collected}/{total}{C.RESET}")

        if collected == 12:
            lines.append(f"\n{C.SUCCESS}{C.BOLD}✦ ALL FRAGMENTS COLLECTED ✦{C.RESET}")
            lines.append(f"{C.FINALE}The full story awaits in Vault 13...{C.RESET}")

        return "\n".join(lines)

    @staticmethod
    def show_full_narrative():
        """Display the complete narrative (only when all fragments collected)"""
        clear_screen()
        print(f"{C.FRAGMENT}{VAULT_13_NARRATIVE}{C.RESET}")
        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")


# =============================================================================
# SAVE/LOAD SYSTEM
# =============================================================================

class ProgressionSaveSystem:
    """Handles saving and loading progression state"""

    SAVE_FILE = "vault13_progression.json"

    @classmethod
    def get_save_path(cls) -> Path:
        """Get the save file path"""
        save_dir = get_save_dir("vault13")
        save_dir.mkdir(parents=True, exist_ok=True)
        return save_dir / cls.SAVE_FILE

    @classmethod
    def save(cls, progression: PlayerProgression) -> bool:
        """Save progression to file"""
        try:
            save_path = cls.get_save_path()

            # Convert to serializable format
            data = {
                "version": "1.0",
                "vault_progress": {
                    vault_id: asdict(progress)
                    for vault_id, progress in progression.vault_progress.items()
                },
                "total_stars": progression.total_stars,
                "fragments_collected": progression.fragments_collected,
                "finale_unlocked": progression.finale_unlocked,
                "finale_completed": progression.finale_completed,
                "total_playtime_seconds": progression.total_playtime_seconds,
                "first_played_date": progression.first_played_date,
                "last_played_date": progression.last_played_date,
                "achievements": progression.achievements,
            }

            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"{C.DANGER}Error saving progression: {e}{C.RESET}")
            return False

    @classmethod
    def load(cls) -> PlayerProgression:
        """Load progression from file"""
        try:
            save_path = cls.get_save_path()

            if not save_path.exists():
                return PlayerProgression()

            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            progression = PlayerProgression()

            # Restore vault progress
            for vault_id, progress_data in data.get("vault_progress", {}).items():
                progression.vault_progress[vault_id] = VaultProgress(
                    vault_id=progress_data["vault_id"],
                    completed=progress_data.get("completed", False),
                    best_stars=progress_data.get("best_stars", 0),
                    times_played=progress_data.get("times_played", 0),
                    best_score=progress_data.get("best_score", 0),
                    fastest_time=progress_data.get("fastest_time"),
                    fragment_unlocked=progress_data.get("fragment_unlocked", False),
                    first_completed_date=progress_data.get("first_completed_date"),
                )

            # Restore other fields
            progression.total_stars = data.get("total_stars", 0)
            progression.fragments_collected = data.get("fragments_collected", [])
            progression.finale_unlocked = data.get("finale_unlocked", False)
            progression.finale_completed = data.get("finale_completed", False)
            progression.total_playtime_seconds = data.get("total_playtime_seconds", 0.0)
            progression.first_played_date = data.get("first_played_date")
            progression.last_played_date = data.get("last_played_date")
            progression.achievements = data.get("achievements", [])

            return progression

        except Exception as e:
            print(f"{C.WARNING}Error loading progression: {e}. Starting fresh.{C.RESET}")
            return PlayerProgression()


# =============================================================================
# VAULT 13 HUB UI
# =============================================================================

class Vault13Hub:
    """The main hub interface for Vault 13 progression"""

    def __init__(self):
        self.progression = ProgressionSaveSystem.load()
        self.running = True

        # Record first play date
        if not self.progression.first_played_date:
            from datetime import datetime
            self.progression.first_played_date = datetime.now().isoformat()

    def save_and_quit(self):
        """Save progress and exit"""
        from datetime import datetime
        self.progression.last_played_date = datetime.now().isoformat()
        ProgressionSaveSystem.save(self.progression)
        self.running = False

    def print_header(self):
        """Print the hub header"""
        print(f"{C.HEADER}{C.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                              ║")
        print("║   ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗    ██╗██████╗                     ║")
        print("║   ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝   ███║╚════██╗                    ║")
        print("║   ██║   ██║███████║██║   ██║██║     ██║      ╚██║ █████╔╝                    ║")
        print("║   ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║       ██║ ╚═══██╗                    ║")
        print("║    ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║       ██║██████╔╝                    ║")
        print("║     ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝       ╚═╝╚═════╝                     ║")
        print("║                                                                              ║")
        print("║              THE FULL VAULT SHELTER v10.0 - TRAINING PROTOCOL                ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

    def print_progress_bar(self):
        """Print overall progress"""
        completed = self.progression.count_completed_vaults()
        total = 12
        stars = self.progression.total_stars
        max_stars = 36  # 12 vaults * 3 stars each

        # Progress bar
        filled = int((completed / total) * 20)
        bar = f"{C.SUCCESS}{'█' * filled}{C.DIM}{'░' * (20 - filled)}{C.RESET}"

        print(f"\n{C.BOLD}TRAINING PROGRESS:{C.RESET} {bar} {completed}/{total} Vaults")
        print(f"{C.BOLD}TOTAL STARS:{C.RESET}       {StarRating.render_stars(0, 0)}{C.STAR}{'★' * min(stars, max_stars)}{C.RESET} {stars}/{max_stars}")
        print(f"{C.BOLD}FRAGMENTS:{C.RESET}         {len(self.progression.fragments_collected)}/12 collected")

        if self.progression.finale_unlocked:
            print(f"\n{C.FINALE}{C.BOLD}✦ VAULT 13 FINALE UNLOCKED ✦{C.RESET}")

    def print_vault_grid(self):
        """Print the vault selection grid"""
        print(f"\n{C.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.BOLD}║                         TRAINING VAULTS                                      ║{C.RESET}")
        print(f"{C.BOLD}╚══════════════════════════════════════════════════════════════════════════════╝{C.RESET}\n")

        highest_unlocked = self.progression.get_highest_unlocked_vault()

        # Display vaults in a 4x3 grid
        for row in range(3):
            for col in range(4):
                vault_num = row * 4 + col + 1
                if vault_num > 12:
                    continue

                vault = TRAINING_VAULTS[vault_num - 1]
                is_unlocked = vault_num <= highest_unlocked
                is_completed = self.progression.is_vault_completed(vault.id)
                stars = self.progression.get_vault_stars(vault.id)

                # Determine display style
                if is_completed:
                    color = C.COMPLETED
                    status = "✓"
                    star_display = StarRating.render_stars(stars)
                elif is_unlocked:
                    color = C.UNLOCKED
                    status = "○"
                    star_display = StarRating.render_stars(0)
                else:
                    color = C.LOCKED
                    status = "🔒"
                    star_display = f"{C.DIM}☆☆☆{C.RESET}"

                # Format vault name (truncate if needed)
                name = vault.name[:14] if len(vault.name) > 14 else vault.name

                print(f"  {color}[{vault_num:2}]{C.RESET} {status} {name:14} {star_display}", end="  ")

            print()  # New line after each row

        # The finale
        print(f"\n{C.BOLD}{'─' * 78}{C.RESET}")

        if self.progression.finale_unlocked:
            finale_status = f"{C.FINALE}✦ UNLOCKED ✦{C.RESET}" if not self.progression.finale_completed else f"{C.SUCCESS}✓ COMPLETED{C.RESET}"
            print(f"\n  {C.FINALE}[13]{C.RESET} {C.BOLD}VAULT 13 - THE FULL EXPERIENCE{C.RESET}  {finale_status}")
        else:
            remaining = 12 - self.progression.count_completed_vaults()
            print(f"\n  {C.LOCKED}[13]{C.RESET} {C.DIM}VAULT 13 - ???  (Complete {remaining} more vaults to unlock){C.RESET}")

    def print_menu(self):
        """Print the menu options"""
        print(f"\n{C.BOLD}COMMANDS:{C.RESET}")
        print(f"  {C.SUCCESS}[1-12]{C.RESET} Select a training vault")
        if self.progression.finale_unlocked:
            print(f"  {C.FINALE}[13]{C.RESET}   Enter Vault 13 Finale")
        print(f"  {C.INFO}[F]{C.RESET}    View collected fragments")
        print(f"  {C.INFO}[S]{C.RESET}    View statistics")
        print(f"  {C.INFO}[H]{C.RESET}    Help & hints")
        print(f"  {C.DANGER}[Q]{C.RESET}    Save & quit")

    def show_vault_details(self, vault: TrainingVault):
        """Show details for a specific vault"""
        clear_screen()

        is_unlocked = self.progression.is_vault_unlocked(vault.number)
        is_completed = self.progression.is_vault_completed(vault.id)
        stars = self.progression.get_vault_stars(vault.id)
        progress = self.progression.vault_progress.get(vault.id)

        print(f"\n{C.VAULT}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VAULT}{C.BOLD}║  VAULT {vault.number:02}  │  {vault.name:52} ║{C.RESET}")
        print(f"{C.VAULT}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")

        if not is_unlocked:
            print(f"\n{C.LOCKED}{C.BOLD}🔒 LOCKED{C.RESET}")
            print(f"\n{C.DIM}Complete Vault {vault.number - 1} to unlock this training.{C.RESET}")
            input(f"\n{C.DIM}Press Enter to return...{C.RESET}")
            return

        # Vault info
        print(f"\n{C.BOLD}Theme:{C.RESET}       {vault.theme}")
        print(f"{C.BOLD}Difficulty:{C.RESET}  {'⚔️' * vault.difficulty}{'  ' * (3 - vault.difficulty)}")
        print(f"\n{C.BOLD}Description:{C.RESET}")
        print(f"  {vault.description}")

        # Stats
        if progress:
            print(f"\n{C.BOLD}Your Progress:{C.RESET}")
            print(f"  Status:       {'✓ Completed' if is_completed else '○ In Progress'}")
            print(f"  Best Rating:  {StarRating.render_stars(stars)}")
            print(f"  Times Played: {progress.times_played}")
            if progress.best_score > 0:
                print(f"  Best Score:   {progress.best_score}")
            if progress.fastest_time:
                print(f"  Fastest Time: {progress.fastest_time:.1f}s")
        else:
            print(f"\n{C.DIM}Not yet attempted{C.RESET}")

        # Mastery hint
        if is_completed and stars < 3:
            print(f"\n{C.WARNING}{C.BOLD}Mastery Hint:{C.RESET}")
            print(f"  {C.DIM}{vault.mastery_hint}{C.RESET}")

        # Actions
        print(f"\n{C.BOLD}Actions:{C.RESET}")
        print(f"  {C.SUCCESS}[P]{C.RESET} Play this vault")
        print(f"  {C.DANGER}[B]{C.RESET} Back to hub")

        choice = input(f"\n{C.BOLD}>{C.RESET} ").strip().lower()

        if choice == 'p':
            self.launch_vault(vault)

    def launch_vault(self, vault: TrainingVault):
        """Launch a training vault mini-game"""
        clear_screen()

        print(f"\n{C.HEADER}{C.BOLD}Launching {vault.name}...{C.RESET}")
        print(f"{C.DIM}Theme: {vault.theme}{C.RESET}")
        print(f"\n{C.WARNING}Note: Complete the game to earn stars and unlock the next vault.{C.RESET}")
        time.sleep(1.5)

        # Track playtime
        start_time = time.time()

        # Check if the game file exists
        game_path = Path(__file__).parent / vault.file

        if not game_path.exists():
            print(f"\n{C.WARNING}Game file not found: {vault.file}{C.RESET}")
            print(f"{C.DIM}Simulating game completion for demo...{C.RESET}")
            time.sleep(2)

            # Simulate game result for demo
            simulated_result = {
                "completed": True,
                "score": random.randint(50, 100),
                "time": random.randint(60, 300),
                "completion": random.uniform(0.7, 1.0),
            }
            self.process_vault_result(vault, simulated_result)
        else:
            try:
                # Launch the actual game
                result = subprocess.run(
                    [sys.executable, str(game_path)],
                    capture_output=False
                )

                # After game ends, prompt for result (in real implementation,
                # games would report back their results)
                self.prompt_for_result(vault)

            except Exception as e:
                print(f"\n{C.DANGER}Error launching game: {e}{C.RESET}")
                input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

        # Record playtime
        elapsed = time.time() - start_time
        self.progression.total_playtime_seconds += elapsed

    def prompt_for_result(self, vault: TrainingVault):
        """Prompt for game result (temporary until games report results)"""
        clear_screen()

        print(f"\n{C.HEADER}{C.BOLD}Game Complete: {vault.name}{C.RESET}")
        print(f"\n{C.DIM}How did you do?{C.RESET}")
        print(f"  {C.SUCCESS}[1]{C.RESET} Won / Completed successfully")
        print(f"  {C.WARNING}[2]{C.RESET} Partial completion")
        print(f"  {C.DANGER}[3]{C.RESET} Did not complete")

        choice = input(f"\n{C.BOLD}>{C.RESET} ").strip()

        if choice == '1':
            result = {"completed": True, "completion": 1.0, "special": random.random() > 0.5}
        elif choice == '2':
            result = {"completed": True, "completion": random.uniform(0.5, 0.8)}
        else:
            result = {"completed": False, "completion": random.uniform(0.1, 0.4)}

        self.process_vault_result(vault, result)

    def process_vault_result(self, vault: TrainingVault, result: Dict):
        """Process the result of playing a vault"""
        vault_id = vault.id

        # Get or create progress record
        if vault_id not in self.progression.vault_progress:
            self.progression.vault_progress[vault_id] = VaultProgress(vault_id=vault_id)

        progress = self.progression.vault_progress[vault_id]
        progress.times_played += 1

        # Calculate stars
        stars = 0
        if result.get("completed", False):
            stars = StarRating.calculate_stars(vault, result)

            # First completion?
            first_completion = not progress.completed

            if first_completion:
                progress.completed = True
                from datetime import datetime
                progress.first_completed_date = datetime.now().isoformat()

                # Unlock fragment
                fragment = NarrativeSystem.get_fragment(vault_id)
                if fragment and fragment not in self.progression.fragments_collected:
                    progress.fragment_unlocked = True
                    self.progression.fragments_collected.append(fragment)

                    clear_screen()
                    print(f"\n{C.FRAGMENT}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
                    print(f"{C.FRAGMENT}{C.BOLD}║                    NARRATIVE FRAGMENT UNLOCKED                       ║{C.RESET}")
                    print(f"{C.FRAGMENT}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")
                    print(f"\n{C.FRAGMENT}{fragment}{C.RESET}")
                    input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

            # Update best stars
            if stars > progress.best_stars:
                old_stars = progress.best_stars
                progress.best_stars = stars
                self.progression.total_stars += (stars - old_stars)

            # Update best score
            if result.get("score", 0) > progress.best_score:
                progress.best_score = result.get("score", 0)

            # Update fastest time
            if result.get("time"):
                if progress.fastest_time is None or result["time"] < progress.fastest_time:
                    progress.fastest_time = result["time"]

        # Show result
        clear_screen()
        print(f"\n{C.VAULT}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VAULT}{C.BOLD}║                         VAULT RESULT                                 ║{C.RESET}")
        print(f"{C.VAULT}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")

        print(f"\n  Vault:    {vault.name}")
        print(f"  Status:   {'✓ Completed' if result.get('completed') else '✗ Not completed'}")
        print(f"  Rating:   {StarRating.render_stars(stars)}")

        if result.get("completed"):
            # Check for new unlocks
            if vault.number < 12:
                next_vault = TRAINING_VAULTS[vault.number]
                print(f"\n  {C.SUCCESS}Vault {vault.number + 1} unlocked: {next_vault.name}{C.RESET}")

            # Check for finale unlock
            if self.progression.check_finale_unlock():
                print(f"\n{C.FINALE}{C.BOLD}  ✦ VAULT 13 FINALE NOW UNLOCKED! ✦{C.RESET}")
                print(f"{C.FINALE}  All training complete. The true vault awaits...{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

        # Save after each vault
        ProgressionSaveSystem.save(self.progression)

    def show_fragments(self):
        """Display collected narrative fragments"""
        clear_screen()
        print(NarrativeSystem.render_collected_fragments(self.progression))

        if len(self.progression.fragments_collected) == 12:
            print(f"\n{C.SUCCESS}[V]{C.RESET} View the complete story")

        print(f"\n{C.DANGER}[B]{C.RESET} Back")

        choice = input(f"\n{C.BOLD}>{C.RESET} ").strip().lower()

        if choice == 'v' and len(self.progression.fragments_collected) == 12:
            NarrativeSystem.show_full_narrative()

    def show_statistics(self):
        """Display player statistics"""
        clear_screen()

        print(f"\n{C.INFO}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.INFO}{C.BOLD}║                         STATISTICS                                   ║{C.RESET}")
        print(f"{C.INFO}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")

        print(f"\n{C.BOLD}Progress:{C.RESET}")
        print(f"  Vaults Completed:  {self.progression.count_completed_vaults()}/12")
        print(f"  Total Stars:       {self.progression.total_stars}/36")
        print(f"  Fragments:         {len(self.progression.fragments_collected)}/12")
        print(f"  Finale Status:     {'Unlocked' if self.progression.finale_unlocked else 'Locked'}")

        # Playtime
        total_seconds = self.progression.total_playtime_seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        print(f"\n{C.BOLD}Time:{C.RESET}")
        print(f"  Total Playtime:    {hours}h {minutes}m")

        if self.progression.first_played_date:
            print(f"  First Played:      {self.progression.first_played_date[:10]}")
        if self.progression.last_played_date:
            print(f"  Last Played:       {self.progression.last_played_date[:10]}")

        # Per-vault stats
        print(f"\n{C.BOLD}Vault Details:{C.RESET}")
        for vault in TRAINING_VAULTS:
            if vault.id in self.progression.vault_progress:
                p = self.progression.vault_progress[vault.id]
                stars = StarRating.render_stars(p.best_stars)
                plays = p.times_played
                print(f"  {vault.number:2}. {vault.name:24} {stars}  ({plays} plays)")
            else:
                print(f"  {vault.number:2}. {vault.name:24} {C.DIM}Not attempted{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def show_help(self):
        """Display help and hints"""
        clear_screen()

        print(f"\n{C.INFO}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.INFO}{C.BOLD}║                           HELP                                       ║{C.RESET}")
        print(f"{C.INFO}{C.BOLD}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")

        print(f"\n{C.BOLD}HOW TO PLAY:{C.RESET}")
        print(f"""
  Vault 13 is a progression-based experience with 12 training vaults
  and a final main experience.

  {C.BOLD}1. Linear Unlock{C.RESET}
     Complete each vault to unlock the next one.
     Vault 1 is always available.

  {C.BOLD}2. Star Ratings{C.RESET}
     Each vault can award 1-3 stars based on performance:
       ★☆☆  Basic completion
       ★★☆  Good performance
       ★★★  Mastery achieved

  {C.BOLD}3. Replay Freedom{C.RESET}
     Any unlocked vault can be replayed anytime.
     Try for higher star ratings!

  {C.BOLD}4. Narrative Fragments{C.RESET}
     Completing a vault for the first time reveals
     a piece of the Vault 13 story.

  {C.BOLD}5. The Finale{C.RESET}
     Complete all 12 training vaults to unlock
     Vault 13: The Full Experience.
""")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def launch_finale(self):
        """Launch the Vault 13 finale (main game)"""
        if not self.progression.finale_unlocked:
            print(f"\n{C.DANGER}Finale not yet unlocked!{C.RESET}")
            time.sleep(1)
            return

        clear_screen()

        print(f"\n{C.FINALE}{C.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                              ║")
        print("║                        ✦ VAULT 13 ✦                                         ║")
        print("║                                                                              ║")
        print("║               THE TRAINING IS COMPLETE, OVERSEER.                            ║")
        print("║                                                                              ║")
        print("║           YOU HAVE LEARNED:                                                  ║")
        print("║             • To question reality                                            ║")
        print("║             • To cooperate and compete                                       ║")
        print("║             • To calculate odds                                              ║")
        print("║             • To make impossible choices                                     ║")
        print("║             • To understand understanding                                    ║")
        print("║             • To preserve identity through change                            ║")
        print("║             • To predict chaos                                               ║")
        print("║             • To accept limits                                               ║")
        print("║             • To embrace uncertainty                                         ║")
        print("║             • To hear all timelines                                          ║")
        print("║             • To create causality                                            ║")
        print("║             • To see through the simulation                                  ║")
        print("║                                                                              ║")
        print("║                    NOW, ENTER VAULT 13.                                      ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.RESET}")

        print(f"\n  {C.SUCCESS}[ENTER]{C.RESET} Begin the full Vault 13 experience")
        print(f"  {C.DANGER}[B]{C.RESET}     Back to hub")

        choice = input(f"\n{C.BOLD}>{C.RESET} ").strip().lower()

        if choice == '' or choice == 'enter':
            # Launch the main vault game
            main_game = Path(__file__).parent / "vault_shelter_v10.py"

            if main_game.exists():
                try:
                    subprocess.run([sys.executable, str(main_game)])
                    self.progression.finale_completed = True
                    ProgressionSaveSystem.save(self.progression)
                except Exception as e:
                    print(f"\n{C.DANGER}Error launching Vault 13: {e}{C.RESET}")
            else:
                print(f"\n{C.WARNING}Vault 13 main game not found at: {main_game}{C.RESET}")
                print(f"{C.DIM}Please ensure vault_shelter_v10.py is in the same directory.{C.RESET}")

            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")

    def run(self):
        """Main hub loop"""
        while self.running:
            clear_screen()
            self.print_header()
            self.print_progress_bar()
            self.print_vault_grid()
            self.print_menu()

            choice = input(f"\n{C.BOLD}>{C.RESET} ").strip().lower()

            # Handle vault selection (1-12)
            if choice.isdigit():
                vault_num = int(choice)
                if 1 <= vault_num <= 12:
                    vault = TRAINING_VAULTS[vault_num - 1]
                    self.show_vault_details(vault)
                elif vault_num == 13 and self.progression.finale_unlocked:
                    self.launch_finale()
            elif choice == 'f':
                self.show_fragments()
            elif choice == 's':
                self.show_statistics()
            elif choice == 'h':
                self.show_help()
            elif choice == 'q':
                self.save_and_quit()

        print(f"\n{C.INFO}Progress saved. See you next time, Overseer!{C.RESET}\n")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point for Vault 13 progression"""
    hub = Vault13Hub()
    hub.run()


if __name__ == '__main__':
    main()
