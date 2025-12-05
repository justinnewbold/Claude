#!/usr/bin/env python3
"""
Base Game Class
===============
Shared base class for all games in the collection.
Provides common functionality and enforces consistent interface.
"""

import os
import sys
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

from logging_config import setup_game_logger, log_performance, log_exceptions


class GameState(Enum):
    """Standard game states"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"


@dataclass
class GameMetadata:
    """Metadata about a game"""
    name: str
    version: str
    description: str
    author: str = "The Vault Collective"
    category: str = "other"


class BaseGame(ABC):
    """
    Abstract base class for all games.

    Provides:
    - Common initialization
    - Terminal management
    - Input handling
    - State management
    - Logging
    - Performance tracking
    """

    def __init__(self, metadata: GameMetadata):
        self.metadata = metadata
        self.state = GameState.MENU
        self.running = False
        self.logger = setup_game_logger(metadata.name.lower().replace(' ', '_'))

        # Performance tracking
        self.frame_count = 0
        self.start_time = time.time()

        self.logger.info(f"Initializing {metadata.name} v{metadata.version}")

    # =========================================================================
    # ABSTRACT METHODS - Must be implemented by subclasses
    # =========================================================================

    @abstractmethod
    def setup(self) -> None:
        """Initialize game state. Called once at start."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Update game logic. Called each frame/turn."""
        pass

    @abstractmethod
    def render(self) -> None:
        """Render game state to terminal. Called after update."""
        pass

    @abstractmethod
    def handle_input(self, key: str) -> None:
        """Handle user input. Called when input received."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources. Called on exit."""
        pass

    # =========================================================================
    # CONCRETE METHODS - Provided by base class
    # =========================================================================

    def run(self) -> None:
        """
        Main game loop.
        Override if you need custom loop behavior.
        """
        try:
            self.running = True
            self.setup()
            self.show_intro()

            while self.running:
                self.frame_count += 1

                # Update game state
                self.update()

                # Render
                self.render()

                # Check for exit conditions
                if self.state in [GameState.GAME_OVER, GameState.VICTORY]:
                    self.show_ending()
                    break

        except KeyboardInterrupt:
            self.logger.info("Game interrupted by user")
            print("\n\nGame interrupted. Thanks for playing!")
        except Exception as e:
            self.logger.exception(f"Fatal error: {e}")
            print(f"\n\nFatal error occurred: {e}")
            raise
        finally:
            self.cleanup()
            self.show_cursor()
            self.logger.info(f"Game session ended. Frames: {self.frame_count}, "
                           f"Duration: {time.time() - self.start_time:.1f}s")

    # =========================================================================
    # TERMINAL MANAGEMENT
    # =========================================================================

    def clear_screen(self) -> None:
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def hide_cursor(self) -> None:
        """Hide terminal cursor"""
        print('\033[?25l', end='', flush=True)

    def show_cursor(self) -> None:
        """Show terminal cursor"""
        print('\033[?25h', end='', flush=True)

    def move_cursor(self, x: int, y: int) -> None:
        """Move cursor to position (1-indexed)"""
        print(f'\033[{y};{x}H', end='', flush=True)

    def set_title(self, title: str) -> None:
        """Set terminal window title"""
        if os.name == 'nt':
            os.system(f'title {title}')
        else:
            print(f'\033]0;{title}\007', end='', flush=True)

    # =========================================================================
    # UI HELPERS
    # =========================================================================

    def print_header(self, text: str, width: int = 70) -> None:
        """Print a styled header"""
        print(f"\n{'═' * width}")
        print(f"{text.center(width)}")
        print(f"{'═' * width}\n")

    def print_box(self, text: str, width: int = 60, title: str = "") -> None:
        """Print text in a box"""
        lines = text.split('\n')

        # Top border
        if title:
            title_text = f"╡ {title} ╞"
            padding = (width - len(title_text)) // 2
            print(f"╔{'═' * padding}{title_text}{'═' * (width - padding - len(title_text))}╗")
        else:
            print(f"╔{'═' * width}╗")

        # Content
        for line in lines:
            padding = width - len(line) - 2
            print(f"║ {line}{' ' * padding} ║")

        # Bottom border
        print(f"╚{'═' * width}╝")

    def wait_for_input(self, prompt: str = "Press Enter to continue...") -> None:
        """Wait for user input"""
        input(f"\n{prompt}")

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask for confirmation"""
        default_hint = "[Y/n]" if default else "[y/N]"
        response = input(f"{message} {default_hint}: ").strip().lower()

        if not response:
            return default

        return response in ['y', 'yes', '1', 'true']

    # =========================================================================
    # EFFECTS
    # =========================================================================

    def typewriter(self, text: str, delay: float = 0.03) -> None:
        """Print text with typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            if char not in ' \n':
                time.sleep(delay)
        print()

    def bell(self) -> None:
        """Sound terminal bell"""
        print('\a', end='', flush=True)

    # =========================================================================
    # GAME LIFECYCLE HOOKS
    # =========================================================================

    def show_intro(self) -> None:
        """Show intro screen. Override to customize."""
        self.clear_screen()
        self.print_header(f"{self.metadata.name} v{self.metadata.version}")
        print(f"{self.metadata.description}\n")
        self.wait_for_input()

    def show_ending(self) -> None:
        """Show ending screen. Override to customize."""
        self.clear_screen()

        if self.state == GameState.VICTORY:
            self.print_header("VICTORY!")
        else:
            self.print_header("GAME OVER")

        self.wait_for_input()

    def pause(self) -> None:
        """Pause the game"""
        self.state = GameState.PAUSED
        self.logger.info("Game paused")

    def resume(self) -> None:
        """Resume the game"""
        self.state = GameState.PLAYING
        self.logger.info("Game resumed")

    def quit(self) -> None:
        """Quit the game"""
        self.running = False
        self.logger.info("Game quit by user")

    # =========================================================================
    # SAVE/LOAD INTERFACE
    # =========================================================================

    def save_game(self) -> Optional[Dict[str, Any]]:
        """
        Save game state. Override to implement saving.
        Should return dict of serializable data.
        """
        self.logger.warning("Save not implemented for this game")
        return None

    def load_game(self, data: Dict[str, Any]) -> bool:
        """
        Load game state. Override to implement loading.
        Should return True on success.
        """
        self.logger.warning("Load not implemented for this game")
        return False

    # =========================================================================
    # UTILITY
    # =========================================================================

    def get_runtime(self) -> float:
        """Get runtime in seconds"""
        return time.time() - self.start_time

    def get_fps(self) -> float:
        """Get average FPS"""
        runtime = self.get_runtime()
        if runtime == 0:
            return 0
        return self.frame_count / runtime

    def log_stats(self) -> None:
        """Log performance statistics"""
        self.logger.info(
            f"Stats: Frames={self.frame_count}, "
            f"Runtime={self.get_runtime():.1f}s, "
            f"FPS={self.get_fps():.1f}"
        )


# =============================================================================
# TURN-BASED GAME BASE CLASS
# =============================================================================

class TurnBasedGame(BaseGame):
    """
    Base class for turn-based games.
    Provides turn counter and simplified loop.
    """

    def __init__(self, metadata: GameMetadata):
        super().__init__(metadata)
        self.turn = 0

    def run(self) -> None:
        """Turn-based game loop"""
        try:
            self.running = True
            self.setup()
            self.show_intro()

            while self.running:
                self.turn += 1
                self.logger.debug(f"Turn {self.turn}")

                # Clear and render
                self.clear_screen()
                self.render()

                # Get input
                try:
                    user_input = input("\n> ").strip()
                    self.handle_input(user_input)
                except EOFError:
                    break

                # Update state
                self.update()

                # Check exit conditions
                if self.state in [GameState.GAME_OVER, GameState.VICTORY]:
                    self.show_ending()
                    break

        except KeyboardInterrupt:
            self.logger.info("Game interrupted")
            print("\n\nGame interrupted.")
        except Exception as e:
            self.logger.exception(f"Fatal error: {e}")
            raise
        finally:
            self.cleanup()
            self.show_cursor()
            self.logger.info(f"Game ended after {self.turn} turns")


# =============================================================================
# EXAMPLE IMPLEMENTATION
# =============================================================================

class ExampleGame(TurnBasedGame):
    """Example game showing how to use the base class"""

    def __init__(self):
        metadata = GameMetadata(
            name="Example Game",
            version="1.0",
            description="A simple example game",
            category="example"
        )
        super().__init__(metadata)
        self.score = 0

    def setup(self) -> None:
        """Initialize game"""
        self.score = 0
        self.state = GameState.PLAYING
        self.logger.info("Example game setup complete")

    def update(self) -> None:
        """Update game state"""
        # Game logic here
        pass

    def render(self) -> None:
        """Render game"""
        self.print_header(f"{self.metadata.name} - Turn {self.turn}")
        print(f"Score: {self.score}")
        print("\nCommands: [s]core, [q]uit")

    def handle_input(self, key: str) -> None:
        """Handle input"""
        if key == 's':
            self.score += 10
            print("Score increased!")
        elif key == 'q':
            if self.confirm("Really quit?"):
                self.quit()

    def cleanup(self) -> None:
        """Cleanup"""
        self.logger.info(f"Final score: {self.score}")


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Base Game Class Module")
    print("=" * 60)
    print("\nThis module provides base classes for all games.")
    print("\nExample game implementation:")
    print()

    # Run example game
    if input("Run example game? [y/N]: ").lower() == 'y':
        game = ExampleGame()
        game.run()
