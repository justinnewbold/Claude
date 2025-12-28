#!/usr/bin/env python3
"""
Game Launcher
=============
Universal game launcher with main menu and game selection.
"""

import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
import importlib.util

from config import GameConfig
from logging_config import get_logger
from validation import get_menu_choice, get_yes_no_input
from error_handling import error_context, GameError
from platform_utils import clear_screen, print_header


logger = get_logger(__name__)

# Preferences file location
PREFERENCES_FILE = Path.home() / ".vault13_launcher_preferences.json"


@dataclass
class GameInfo:
    """Information about a game"""
    id: str
    name: str
    description: str
    module_path: str
    main_function: str = "main"
    version: str = "1.0"
    author: str = "Unknown"
    min_python: str = "3.8"
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class GameLauncher:
    """
    Universal game launcher system.

    Features:
    - Automatic game discovery
    - Main menu with categories
    - Game search and filtering
    - Recent games tracking
    - Favorites system
    """

    def __init__(self, config: Optional[GameConfig] = None):
        """Initialize launcher"""
        self.config = config or GameConfig()
        self.logger = get_logger(__name__)
        self.games: Dict[str, GameInfo] = {}
        self.recent_games: List[str] = []
        self.favorites: List[str] = []
        self.running = True

        self._load_games()
        self._load_preferences()

    def _load_games(self):
        """Load all available games"""
        # Complete list of all games in the collection
        self.games = {
            # === MAIN GAMES ===
            'vault_shelter': GameInfo(
                id='vault_shelter',
                name='VAULT 13 - Survival Protocol',
                description='Ultimate post-apocalyptic vault management simulator with 50+ features',
                module_path='vault_shelter_v6.py',
                main_function='main',
                version='9.0',
                tags=['simulation', 'management', 'main']
            ),

            # === PHILOSOPHICAL GAMES ===
            'echo_chambers': GameInfo(
                id='echo_chambers',
                name='Echo Chambers',
                description='Exist across multiple parallel timelines simultaneously',
                module_path='echo_chambers.py',
                main_function='main',
                tags=['quantum', 'narrative', 'philosophical']
            ),
            'schrodingers_dungeon': GameInfo(
                id='schrodingers_dungeon',
                name="Schrödinger's Dungeon",
                description='Navigate a dungeon where reality is probabilistic until observed',
                module_path='schrodingers_dungeon.py',
                main_function='main',
                tags=['quantum', 'dungeon', 'philosophical']
            ),
            'code_archaeology': GameInfo(
                id='code_archaeology',
                name='Code Archaeology',
                description='Debug code from extinct alien civilizations',
                module_path='code_archaeology.py',
                main_function='main',
                tags=['puzzle', 'programming', 'philosophical']
            ),
            'infinite_library': GameInfo(
                id='infinite_library',
                name='The Infinite Library',
                description="Explore Borges' Library of Babel - every possible book exists",
                module_path='infinite_library.py',
                main_function='main',
                tags=['exploration', 'philosophical', 'borges']
            ),
            'butterfly_effect': GameInfo(
                id='butterfly_effect',
                name='The Butterfly Effect',
                description='Chaos theory puzzle - tiny changes create vastly different outcomes',
                module_path='butterfly_effect.py',
                main_function='main',
                tags=['chaos', 'puzzle', 'philosophical']
            ),
            'syntax_tree_climber': GameInfo(
                id='syntax_tree_climber',
                name='Syntax Tree Climber',
                description='Navigate the AST of living code - meta-programming as gameplay',
                module_path='syntax_tree_climber.py',
                main_function='main',
                tags=['programming', 'meta', 'philosophical']
            ),
            'ship_of_theseus': GameInfo(
                id='ship_of_theseus',
                name='Ship of Theseus',
                description='Explore identity through gradual replacement',
                module_path='ship_of_theseus.py',
                main_function='main',
                tags=['identity', 'philosophical', 'puzzle']
            ),
            'trolley_problem': GameInfo(
                id='trolley_problem',
                name='Trolley Problem',
                description='Face ethical dilemmas with branching consequences',
                module_path='trolley_problem.py',
                main_function='main',
                tags=['ethics', 'philosophical', 'choice']
            ),
            'prisoners_dilemma': GameInfo(
                id='prisoners_dilemma',
                name="Prisoner's Dilemma",
                description='Game theory exploration of cooperation vs betrayal',
                module_path='prisoners_dilemma.py',
                main_function='main',
                tags=['game-theory', 'philosophical', 'strategy']
            ),
            'chinese_room': GameInfo(
                id='chinese_room',
                name='Chinese Room',
                description="Explore Searle's thought experiment on consciousness",
                module_path='chinese_room.py',
                main_function='main',
                tags=['consciousness', 'philosophical', 'ai']
            ),
            'platos_cave': GameInfo(
                id='platos_cave',
                name="Plato's Cave",
                description='Escape the shadows and discover true reality',
                module_path='platos_cave.py',
                main_function='main',
                tags=['reality', 'philosophical', 'allegory']
            ),
            'simulation_hypothesis': GameInfo(
                id='simulation_hypothesis',
                name='Simulation Hypothesis',
                description='Are you in a simulation? Find out.',
                module_path='simulation_hypothesis.py',
                main_function='main',
                tags=['reality', 'philosophical', 'simulation']
            ),
            'marys_room': GameInfo(
                id='marys_room',
                name="Mary's Room",
                description='Explore qualia and the knowledge argument',
                module_path='marys_room.py',
                main_function='main',
                tags=['consciousness', 'philosophical', 'qualia']
            ),
            'halting_problem': GameInfo(
                id='halting_problem',
                name='The Halting Problem',
                description="Navigate Turing's undecidable territory",
                module_path='halting_problem.py',
                main_function='main',
                tags=['computation', 'philosophical', 'turing']
            ),

            # === PARADOX GAMES ===
            'monty_hall': GameInfo(
                id='monty_hall',
                name='Monty Hall',
                description='The classic probability paradox - switch or stay?',
                module_path='monty_hall.py',
                main_function='main',
                tags=['probability', 'paradox', 'puzzle']
            ),
            'newcombs_paradox': GameInfo(
                id='newcombs_paradox',
                name="Newcomb's Paradox",
                description='One box or two? Challenge a perfect predictor',
                module_path='newcombs_paradox.py',
                main_function='main',
                tags=['decision-theory', 'paradox', 'puzzle']
            ),
            'pascals_wager': GameInfo(
                id='pascals_wager',
                name="Pascal's Wager",
                description='Bet on existence with infinite stakes',
                module_path='pascals_wager.py',
                main_function='main',
                tags=['decision-theory', 'paradox', 'philosophy']
            ),
            'sleeping_beauty': GameInfo(
                id='sleeping_beauty',
                name='Sleeping Beauty',
                description='The probability puzzle of uncertain awakening',
                module_path='sleeping_beauty.py',
                main_function='main',
                tags=['probability', 'paradox', 'puzzle']
            ),
            'zenos_runner': GameInfo(
                id='zenos_runner',
                name="Zeno's Runner",
                description='Race against infinite divisions of space',
                module_path='zenos_runner.py',
                main_function='main',
                tags=['infinity', 'paradox', 'runner']
            ),
            'bootstrap_paradox': GameInfo(
                id='bootstrap_paradox',
                name='Bootstrap Paradox',
                description='Time loop puzzle - where did it begin?',
                module_path='bootstrap_paradox.py',
                main_function='main',
                tags=['time', 'paradox', 'puzzle']
            ),
            'twin_paradox': GameInfo(
                id='twin_paradox',
                name='Twin Paradox',
                description='Relativistic time dilation adventure',
                module_path='twin_paradox.py',
                main_function='main',
                tags=['relativity', 'paradox', 'physics']
            ),
            'braess_paradox': GameInfo(
                id='braess_paradox',
                name="Braess's Paradox",
                description='When adding roads makes traffic worse',
                module_path='braess_paradox.py',
                main_function='main',
                tags=['networks', 'paradox', 'puzzle']
            ),
            'sorites_paradox': GameInfo(
                id='sorites_paradox',
                name='Sorites Paradox',
                description='The heap paradox - how many grains make a heap?',
                module_path='sorites_paradox.py',
                main_function='main',
                tags=['logic', 'paradox', 'vagueness']
            ),
            'godels_paradox': GameInfo(
                id='godels_paradox',
                name="Gödel's Paradox",
                description='Navigate incompleteness and self-reference',
                module_path='godels_paradox.py',
                main_function='main',
                tags=['logic', 'paradox', 'math']
            ),
            'munchhausen_trilemma': GameInfo(
                id='munchhausen_trilemma',
                name='Münchhausen Trilemma',
                description='The problem of infinite regress in justification',
                module_path='munchhausen_trilemma.py',
                main_function='main',
                tags=['epistemology', 'paradox', 'philosophy']
            ),
            'doomsday_argument': GameInfo(
                id='doomsday_argument',
                name='Doomsday Argument',
                description='Probabilistic reasoning about human extinction',
                module_path='doomsday_argument.py',
                main_function='main',
                tags=['probability', 'paradox', 'anthropic']
            ),

            # === PHYSICS/SCIENCE GAMES ===
            'maxwells_demon': GameInfo(
                id='maxwells_demon',
                name="Maxwell's Demon",
                description='Sort molecules and challenge the second law',
                module_path='maxwells_demon.py',
                main_function='main',
                tags=['physics', 'thermodynamics', 'puzzle']
            ),
            'laplaces_demon': GameInfo(
                id='laplaces_demon',
                name="Laplace's Demon",
                description='Perfect knowledge, perfect prediction',
                module_path='laplaces_demon.py',
                main_function='main',
                tags=['determinism', 'physics', 'puzzle']
            ),
            'quantum_eraser': GameInfo(
                id='quantum_eraser',
                name='Quantum Eraser',
                description='Manipulate quantum information and causality',
                module_path='quantum_eraser.py',
                main_function='main',
                tags=['quantum', 'physics', 'puzzle']
            ),
            'entanglement': GameInfo(
                id='entanglement',
                name='Entanglement',
                description='Quantum entanglement puzzle game',
                module_path='entanglement.py',
                main_function='main',
                tags=['quantum', 'physics', 'puzzle']
            ),
            'boltzmann_brains': GameInfo(
                id='boltzmann_brains',
                name='Boltzmann Brains',
                description='Statistical fluctuations and consciousness',
                module_path='boltzmann_brains.py',
                main_function='main',
                tags=['physics', 'consciousness', 'probability']
            ),

            # === NARRATIVE/ADVENTURE GAMES ===
            'forking_paths': GameInfo(
                id='forking_paths',
                name='Garden of Forking Paths',
                description='Borgesian labyrinth of branching narratives',
                module_path='forking_paths.py',
                main_function='main',
                tags=['narrative', 'borges', 'adventure']
            ),
            'last_recursion': GameInfo(
                id='last_recursion',
                name='The Last Recursion',
                description='Recursive narrative descent',
                module_path='last_recursion.py',
                main_function='main',
                tags=['recursion', 'narrative', 'puzzle']
            ),
            'emergence_engine': GameInfo(
                id='emergence_engine',
                name='Emergence Engine',
                description='Watch complex behavior emerge from simple rules',
                module_path='emergence_engine.py',
                main_function='main',
                tags=['emergence', 'simulation', 'complexity']
            ),
            'the_categorizer': GameInfo(
                id='the_categorizer',
                name='The Categorizer',
                description='Classification and taxonomy puzzle',
                module_path='the_categorizer.py',
                main_function='main',
                tags=['logic', 'puzzle', 'classification']
            ),
        }

        self.logger.info(f"Loaded {len(self.games)} games")

    def _load_preferences(self):
        """Load user preferences (recent games, favorites) from file"""
        self.recent_games = []
        self.favorites = []

        try:
            if PREFERENCES_FILE.exists():
                with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.recent_games = data.get('recent_games', [])
                    self.favorites = data.get('favorites', [])
                    self.logger.info(f"Loaded preferences: {len(self.recent_games)} recent, {len(self.favorites)} favorites")
        except json.JSONDecodeError as e:
            self.logger.warning(f"Invalid preferences file, resetting: {e}")
        except Exception as e:
            self.logger.warning(f"Could not load preferences: {e}")

    def _save_preferences(self):
        """Save user preferences to file"""
        try:
            data = {
                'recent_games': self.recent_games,
                'favorites': self.favorites,
            }
            with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.logger.info("Preferences saved successfully")
        except Exception as e:
            self.logger.warning(f"Could not save preferences: {e}")

    def run(self):
        """Main launcher loop"""
        self.logger.info("Game Launcher started")

        while self.running:
            try:
                self._show_main_menu()
            except KeyboardInterrupt:
                if get_yes_no_input("\nQuit launcher?", default=True):
                    self.running = False
            except Exception as e:
                self.logger.error(f"Error in launcher: {e}", exc_info=True)
                print(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")

        self.logger.info("Game Launcher closed")
        self._save_preferences()

    def _show_main_menu(self):
        """Display main menu"""
        clear_screen()
        print_header("🎮 VAULT 13 GAME LAUNCHER 🎮")

        print("\n" + "=" * 60)
        print(f"Total Games: {len(self.games)}")
        if self.recent_games:
            print(f"Recent: {', '.join(self.recent_games[:3])}")
        print("=" * 60)

        options = [
            "🎯 Browse All Games",
            "⭐ Favorites",
            "🕐 Recent Games",
            "🔍 Search Games",
            "📊 Statistics",
            "⚙️  Settings",
            "❌ Exit"
        ]

        choice = get_menu_choice(options, title="\nMain Menu")

        if choice == 1:
            self._browse_games()
        elif choice == 2:
            self._show_favorites()
        elif choice == 3:
            self._show_recent()
        elif choice == 4:
            self._search_games()
        elif choice == 5:
            self._show_statistics()
        elif choice == 6:
            self._show_settings()
        elif choice == 7:
            self.running = False

    def _browse_games(self):
        """Browse all games"""
        while True:
            clear_screen()
            print_header("🎯 Browse Games")

            # Group games by tag
            games_list = sorted(self.games.values(), key=lambda g: g.name)

            print("\n" + "=" * 60)
            for i, game in enumerate(games_list, 1):
                favorite = "⭐" if game.id in self.favorites else "  "
                tags = ", ".join(game.tags[:3]) if game.tags else "no tags"
                print(f"{favorite} {i}. {game.name}")
                print(f"      {game.description}")
                print(f"      Tags: {tags} | v{game.version}")
                print()
            print("=" * 60)

            options = [g.name for g in games_list] + ["Back"]
            choice = get_menu_choice(options, title="Select Game")

            if choice == 0 or choice == len(options):
                break

            selected_game = games_list[choice - 1]
            self._show_game_details(selected_game)

    def _show_game_details(self, game: GameInfo):
        """Show detailed info about a game"""
        clear_screen()
        print_header(f"🎮 {game.name}")

        print("\n" + "=" * 60)
        print(f"Description: {game.description}")
        print(f"Version: {game.version}")
        print(f"Author: {game.author}")
        print(f"Tags: {', '.join(game.tags) if game.tags else 'None'}")
        print("=" * 60)

        options = [
            "▶️  Launch Game",
            "⭐ Toggle Favorite",
            "📋 View More Info",
            "← Back"
        ]

        choice = get_menu_choice(options)

        if choice == 1:
            self._launch_game(game)
        elif choice == 2:
            self._toggle_favorite(game)
        elif choice == 3:
            self._show_extended_info(game)

    def _launch_game(self, game: GameInfo):
        """Launch a game"""
        self.logger.info(f"Launching game: {game.name}")

        # Add to recent games
        if game.id in self.recent_games:
            self.recent_games.remove(game.id)
        self.recent_games.insert(0, game.id)
        self.recent_games = self.recent_games[:10]  # Keep last 10

        clear_screen()
        print(f"\n🚀 Launching {game.name}...\n")

        with error_context(f"launching {game.name}"):
            # Try to import and run the game
            module_path = os.path.join(os.getcwd(), game.module_path)

            if not os.path.exists(module_path):
                raise GameError(f"Game file not found: {game.module_path}")

            # Import the module
            spec = importlib.util.spec_from_file_location(game.id, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Call the main function
                if hasattr(module, game.main_function):
                    main_func = getattr(module, game.main_function)
                    main_func()
                else:
                    raise GameError(f"Main function '{game.main_function}' not found")
            else:
                raise GameError(f"Could not load module: {game.module_path}")

        # After game exits
        print("\n" + "=" * 60)
        print(f"✅ {game.name} closed")
        print("=" * 60)
        input("\nPress Enter to return to launcher...")

    def _toggle_favorite(self, game: GameInfo):
        """Toggle game favorite status"""
        if game.id in self.favorites:
            self.favorites.remove(game.id)
            print(f"\n💔 Removed {game.name} from favorites")
        else:
            self.favorites.append(game.id)
            print(f"\n⭐ Added {game.name} to favorites")

        input("Press Enter to continue...")

    def _show_extended_info(self, game: GameInfo):
        """Show extended game information"""
        clear_screen()
        print_header(f"📋 {game.name} - Extended Info")

        print("\n" + "=" * 60)
        print(f"Game ID: {game.id}")
        print(f"Name: {game.name}")
        print(f"Description: {game.description}")
        print(f"Version: {game.version}")
        print(f"Author: {game.author}")
        print(f"Module: {game.module_path}")
        print(f"Main Function: {game.main_function}")
        print(f"Min Python: {game.min_python}")
        print(f"Tags: {', '.join(game.tags) if game.tags else 'None'}")
        print(f"Favorite: {'Yes' if game.id in self.favorites else 'No'}")
        print("=" * 60)

        input("\nPress Enter to go back...")

    def _show_favorites(self):
        """Show favorite games"""
        if not self.favorites:
            clear_screen()
            print_header("⭐ Favorites")
            print("\n⚠️  No favorite games yet!")
            print("\nBrowse games and add some favorites.")
            input("\nPress Enter to continue...")
            return

        favorite_games = [self.games[gid] for gid in self.favorites if gid in self.games]

        clear_screen()
        print_header("⭐ Favorite Games")

        print("\n" + "=" * 60)
        for i, game in enumerate(favorite_games, 1):
            print(f"{i}. {game.name}")
            print(f"   {game.description}")
            print()
        print("=" * 60)

        options = [g.name for g in favorite_games] + ["Back"]
        choice = get_menu_choice(options, title="Select Game")

        if choice > 0 and choice <= len(favorite_games):
            self._show_game_details(favorite_games[choice - 1])

    def _show_recent(self):
        """Show recent games"""
        if not self.recent_games:
            clear_screen()
            print_header("🕐 Recent Games")
            print("\n⚠️  No recent games yet!")
            print("\nLaunch a game to see it here.")
            input("\nPress Enter to continue...")
            return

        recent = [self.games[gid] for gid in self.recent_games if gid in self.games]

        clear_screen()
        print_header("🕐 Recent Games")

        print("\n" + "=" * 60)
        for i, game in enumerate(recent, 1):
            print(f"{i}. {game.name}")
            print(f"   {game.description}")
            print()
        print("=" * 60)

        options = [g.name for g in recent] + ["Back"]
        choice = get_menu_choice(options, title="Select Game")

        if choice > 0 and choice <= len(recent):
            self._show_game_details(recent[choice - 1])

    def _search_games(self):
        """Search games by name or tag"""
        clear_screen()
        print_header("🔍 Search Games")

        query = input("\nEnter search term (name or tag): ").strip().lower()

        if not query:
            return

        # Search by name or tag
        results = [
            game for game in self.games.values()
            if query in game.name.lower()
            or query in game.description.lower()
            or any(query in tag.lower() for tag in game.tags)
        ]

        if not results:
            print(f"\n❌ No games found matching '{query}'")
            input("\nPress Enter to continue...")
            return

        print(f"\n✅ Found {len(results)} game(s):")
        print("=" * 60)
        for i, game in enumerate(results, 1):
            print(f"{i}. {game.name}")
            print(f"   {game.description}")
            print()
        print("=" * 60)

        options = [g.name for g in results] + ["Back"]
        choice = get_menu_choice(options, title="Select Game")

        if choice > 0 and choice <= len(results):
            self._show_game_details(results[choice - 1])

    def _show_statistics(self):
        """Show launcher statistics"""
        clear_screen()
        print_header("📊 Statistics")

        print("\n" + "=" * 60)
        print(f"Total Games: {len(self.games)}")
        print(f"Favorites: {len(self.favorites)}")
        print(f"Recent Games: {len(self.recent_games)}")
        print()

        # Count by tag
        tag_counts = {}
        for game in self.games.values():
            for tag in game.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        if tag_counts:
            print("Games by Tag:")
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {tag}: {count}")

        print("=" * 60)
        input("\nPress Enter to continue...")

    def _show_settings(self):
        """Show settings menu"""
        clear_screen()
        print_header("⚙️  Settings")

        print("\n" + "=" * 60)
        print("Launcher Settings")
        print("=" * 60)

        options = [
            "Clear Recent Games",
            "Clear Favorites",
            "Reset All Preferences",
            "Back"
        ]

        choice = get_menu_choice(options)

        if choice == 1:
            if get_yes_no_input("Clear recent games list?", default=False):
                self.recent_games = []
                print("✅ Recent games cleared")
                input("Press Enter to continue...")
        elif choice == 2:
            if get_yes_no_input("Clear all favorites?", default=False):
                self.favorites = []
                print("✅ Favorites cleared")
                input("Press Enter to continue...")
        elif choice == 3:
            if get_yes_no_input("Reset ALL preferences?", default=False):
                self.recent_games = []
                self.favorites = []
                print("✅ All preferences reset")
                input("Press Enter to continue...")


def main():
    """Main entry point"""
    try:
        launcher = GameLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
