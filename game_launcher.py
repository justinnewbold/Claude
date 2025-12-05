#!/usr/bin/env python3
"""
Game Launcher
=============
Universal game launcher with main menu and game selection.
"""

import sys
import os
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
import importlib.util

from config import GameConfig
from logging_config import get_logger
from validation import get_menu_choice, get_yes_no_input
from error_handling import error_context, GameError
from platform_utils import clear_screen, print_header


logger = get_logger(__name__)


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
        # Manually registered games (you can add auto-discovery later)
        self.games = {
            'vault_shelter': GameInfo(
                id='vault_shelter',
                name='Vault Shelter Simulator',
                description='Manage a post-apocalyptic vault shelter',
                module_path='vault_shelter_v6.py',
                main_function='main',
                version='6.0',
                tags=['simulation', 'management', 'fallout']
            ),
            'echo_chambers': GameInfo(
                id='echo_chambers',
                name='Echo Chambers',
                description='Quantum timeline exploration game',
                module_path='echo_chambers.py',
                main_function='main',
                version='1.0',
                tags=['sci-fi', 'text-adventure', 'quantum']
            ),
            'space_explorer': GameInfo(
                id='space_explorer',
                name='Space Explorer',
                description='Explore the cosmos',
                module_path='space_explorer.py',
                main_function='main',
                version='1.0',
                tags=['space', 'exploration']
            ),
            'dungeon_crawler': GameInfo(
                id='dungeon_crawler',
                name='Dungeon Crawler',
                description='Classic dungeon exploration',
                module_path='dungeon_crawler.py',
                main_function='main',
                version='1.0',
                tags=['fantasy', 'rpg', 'dungeon']
            ),
            'trading_post': GameInfo(
                id='trading_post',
                name='Trading Post',
                description='Resource trading simulation',
                module_path='trading_post.py',
                main_function='main',
                version='1.0',
                tags=['trading', 'economy']
            )
        }

        self.logger.info(f"Loaded {len(self.games)} games")

    def _load_preferences(self):
        """Load user preferences (recent games, favorites)"""
        # TODO: Load from save file
        self.recent_games = []
        self.favorites = []

    def _save_preferences(self):
        """Save user preferences"""
        # TODO: Save to file
        pass

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
