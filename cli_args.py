#!/usr/bin/env python3
"""
Command-Line Arguments for Games
=================================
Provides standardized CLI argument parsing for all games.

Usage in games:
    from cli_args import GameArgs, parse_game_args

    args = parse_game_args("My Game", "A cool game")

    if args.demo:
        run_demo_mode()
    elif args.quick:
        skip_animations = True

    if args.seed:
        random.seed(args.seed)
"""

import argparse
import random
import os
from dataclasses import dataclass
from typing import Optional, List
from platform_utils import Colors


@dataclass
class GameArgs:
    """Parsed command-line arguments for a game"""
    # Display modes
    demo: bool = False          # Auto-play demonstration mode
    quick: bool = False         # Skip animations and intros
    no_color: bool = False      # Disable ANSI colors
    debug: bool = False         # Enable debug/verbose logging

    # Game control
    seed: Optional[int] = None  # Random seed for reproducibility
    difficulty: str = "normal"  # Difficulty level
    save_file: Optional[str] = None  # Save file to load

    # Info flags
    show_help: bool = False     # Show help (handled by argparse)
    show_version: bool = False  # Show version info
    show_stats: bool = False    # Show game statistics

    # Raw args for game-specific handling
    extra_args: List[str] = None

    def __post_init__(self):
        if self.extra_args is None:
            self.extra_args = []

        # Apply no_color globally
        if self.no_color:
            os.environ['NO_COLOR'] = '1'


def create_argument_parser(game_name: str, description: str,
                          version: str = "1.0") -> argparse.ArgumentParser:
    """
    Create a standardized argument parser for a game.

    Args:
        game_name: Name of the game
        description: Short description
        version: Version string

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog=game_name.lower().replace(' ', '_'),
        description=f"{game_name}: {description}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python {game_name.lower().replace(' ', '_')}.py --demo     Run in demo mode
  python {game_name.lower().replace(' ', '_')}.py --quick    Skip intros/animations
  python {game_name.lower().replace(' ', '_')}.py --seed 42  Use fixed random seed
  python {game_name.lower().replace(' ', '_')}.py --debug    Enable debug output
"""
    )

    # Version
    parser.add_argument(
        '--version', '-V',
        action='version',
        version=f'{game_name} v{version}'
    )

    # Display modes
    display_group = parser.add_argument_group('Display Options')
    display_group.add_argument(
        '--demo', '-d',
        action='store_true',
        help='Run in demo/auto-play mode'
    )
    display_group.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Skip intro sequences and reduce animation delays'
    )
    display_group.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output (for accessibility or piping)'
    )

    # Game control
    game_group = parser.add_argument_group('Game Options')
    game_group.add_argument(
        '--seed', '-s',
        type=int,
        metavar='N',
        help='Set random seed for reproducible runs'
    )
    game_group.add_argument(
        '--difficulty',
        choices=['easy', 'normal', 'hard', 'nightmare'],
        default='normal',
        help='Set difficulty level (default: normal)'
    )
    game_group.add_argument(
        '--load', '-l',
        metavar='FILE',
        dest='save_file',
        help='Load a saved game file'
    )

    # Debug/development
    debug_group = parser.add_argument_group('Development Options')
    debug_group.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug/verbose output'
    )
    debug_group.add_argument(
        '--stats',
        action='store_true',
        dest='show_stats',
        help='Show game statistics and exit'
    )

    return parser


def parse_game_args(game_name: str, description: str,
                   version: str = "1.0",
                   custom_args: Optional[List[argparse.Action]] = None) -> GameArgs:
    """
    Parse command-line arguments for a game.

    Args:
        game_name: Name of the game
        description: Short description
        version: Version string
        custom_args: Additional custom arguments to add

    Returns:
        GameArgs dataclass with parsed values

    Example:
        args = parse_game_args("Echo Chambers", "Quantum narrative game")
        if args.demo:
            run_demo()
    """
    parser = create_argument_parser(game_name, description, version)

    # Parse known args, collect extras for game-specific handling
    namespace, extra = parser.parse_known_args()

    # Build GameArgs
    game_args = GameArgs(
        demo=namespace.demo,
        quick=namespace.quick,
        no_color=namespace.no_color,
        debug=namespace.debug,
        seed=namespace.seed,
        difficulty=namespace.difficulty,
        save_file=namespace.save_file,
        show_stats=namespace.show_stats,
        extra_args=extra
    )

    # Apply seed if specified
    if game_args.seed is not None:
        random.seed(game_args.seed)

    # Configure colors
    if game_args.no_color:
        _disable_colors()

    return game_args


def _disable_colors():
    """Disable all ANSI colors"""
    os.environ['NO_COLOR'] = '1'
    # Also disable in Colors class if available
    try:
        for attr in dir(Colors):
            if attr.isupper() and not attr.startswith('_'):
                setattr(Colors, attr, '')
    except (AttributeError, TypeError):
        pass


class GameRunner:
    """
    Helper class for running games with CLI argument support.

    Usage:
        runner = GameRunner("My Game", "Description", "1.0")

        @runner.main
        def main(args: GameArgs):
            # Your game logic here
            if args.demo:
                run_demo()
            else:
                run_game()

        # In if __name__ == '__main__':
        runner.run()
    """

    def __init__(self, game_name: str, description: str, version: str = "1.0"):
        self.game_name = game_name
        self.description = description
        self.version = version
        self._main_func = None

    def main(self, func):
        """Decorator to register the main game function"""
        self._main_func = func
        return func

    def run(self):
        """Parse arguments and run the game"""
        args = parse_game_args(self.game_name, self.description, self.version)

        if args.show_stats:
            self._show_stats()
            return

        if self._main_func:
            try:
                self._main_func(args)
            except KeyboardInterrupt:
                print("\n\nGame interrupted.")
            except Exception as e:
                if args.debug:
                    raise
                print(f"\nError: {e}")
        else:
            print("No main function registered!")

    def _show_stats(self):
        """Show game statistics"""
        try:
            from game_state import get_state_manager
            state = get_state_manager()

            game_id = self.game_name.lower().replace(' ', '_')
            stats = state._get_or_create_stats(game_id)

            print(f"\n{self.game_name} Statistics")
            print("=" * 40)
            print(f"Times Played: {stats.play_count}")
            print(f"High Score: {stats.high_score}")
            print(f"Total Play Time: {state.format_play_time(state.get_play_time(game_id))}")
            print(f"Wins: {stats.wins}")
            print(f"Losses: {stats.losses}")
            if stats.wins + stats.losses > 0:
                win_rate = stats.wins / (stats.wins + stats.losses) * 100
                print(f"Win Rate: {win_rate:.1f}%")
            print(f"Achievements: {len(stats.achievements)}")
            if stats.last_played:
                print(f"Last Played: {stats.last_played}")
            print("=" * 40)
        except ImportError:
            print("Statistics not available (game_state module not found)")


# Convenience function for simple games
def quick_parse() -> GameArgs:
    """Quick parse with default game name from script"""
    import sys
    script_name = os.path.basename(sys.argv[0]).replace('.py', '').replace('_', ' ').title()
    return parse_game_args(script_name, "A game")


if __name__ == '__main__':
    # Demo
    print("CLI Args Module Demo")
    print("=" * 40)

    args = parse_game_args(
        "Demo Game",
        "A demonstration of CLI argument parsing",
        "1.0"
    )

    print(f"\nParsed Arguments:")
    print(f"  demo: {args.demo}")
    print(f"  quick: {args.quick}")
    print(f"  no_color: {args.no_color}")
    print(f"  debug: {args.debug}")
    print(f"  seed: {args.seed}")
    print(f"  difficulty: {args.difficulty}")
    print(f"  save_file: {args.save_file}")
    print(f"  extra_args: {args.extra_args}")

    print("\nTry running with: --help, --demo, --quick, --seed 42, etc.")
