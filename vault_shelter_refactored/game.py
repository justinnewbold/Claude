"""
Vault Shelter Refactored - Core Game Module
============================================
Main game class and game loop.
"""

from typing import Optional
from dataclasses import dataclass

from base_game import TurnBasedGame, GameMetadata
from logging_config import get_logger
from config_manager import get_config
from save_system import get_save_system
from achievements import AchievementSystem
from tutorial_system import TutorialSystem
from analytics import get_analytics, track_game_start, track_game_end


@dataclass
class GameState:
    """Current game state"""
    day: int = 1
    caps: int = 1000
    population: int = 12
    happiness: int = 75
    vault_level: int = 1


class VaultShelter(TurnBasedGame):
    """
    Refactored Vault Shelter game using modern infrastructure.

    This demonstrates how the 6,983-line vault_shelter_v6.py should be
    structured using modular architecture.
    """

    def __init__(self):
        super().__init__(GameMetadata(
            name="Vault Shelter",
            version="7.0 (Refactored)",
            description="Manage a post-apocalyptic vault shelter"
        ))

        # Infrastructure
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.save_system = get_save_system()
        self.achievements = AchievementSystem('vault_shelter')
        self.tutorial = TutorialSystem('vault_shelter')
        self.analytics = get_analytics()

        # Game state
        self.state = GameState()

        # Systems (would be imported from modules)
        self.dwellers = []
        self.rooms = []
        self.resources = {'power': 100, 'water': 100, 'food': 100}

        self.logger.info("Vault Shelter initialized (refactored)")

        # Start analytics
        if self.analytics.is_enabled():
            track_game_start('vault_shelter', {'version': '7.0'})

    def setup(self):
        """Initialize game"""
        self.logger.info("Game setup started")

        # Show tutorial if needed
        if self.config.should_show_tutorial() and self.tutorial.is_active():
            self.tutorial.show_current_step()

        self.print_intro()

    def print_intro(self):
        """Show game intro"""
        self.clear_screen()
        self.print_header("VAULT SHELTER v7.0 (Refactored)")
        print("""
Welcome to Vault Shelter!

Manage your post-apocalyptic vault, keep dwellers happy,
gather resources, and survive the wasteland.

This is a REFACTORED version demonstrating modular architecture.
        """)
        input("\nPress Enter to begin...")

    def render(self):
        """Render game state"""
        self.clear_screen()
        self.print_header(f"Vault Shelter - Day {self.state.day}")

        # Status
        print(f"\n📊 Status:")
        print(f"   Caps: ${self.state.caps}")
        print(f"   Population: {self.state.population}")
        print(f"   Happiness: {self.state.happiness}%")
        print(f"   Vault Level: {self.state.vault_level}")

        # Resources
        print(f"\n⚡ Resources:")
        for name, amount in self.resources.items():
            print(f"   {name.capitalize()}: {amount}")

    def handle_input(self, key: Optional[str] = None):
        """Handle player input"""
        from validation import get_menu_choice, get_yes_no_input

        options = [
            "🏗️  Build Room",
            "👥 Manage Dwellers",
            "🎯 View Quests",
            "💾 Save Game",
            "⚙️  Settings",
            "❌ Quit"
        ]

        choice = get_menu_choice(options, title="Main Menu")

        if choice == 1:
            self.build_room_menu()
        elif choice == 2:
            self.manage_dwellers_menu()
        elif choice == 3:
            self.quests_menu()
        elif choice == 4:
            self.save_game()
        elif choice == 5:
            from config_manager import show_settings_menu
            show_settings_menu()
        elif choice == 6:
            if get_yes_no_input("Are you sure you want to quit?"):
                self.quit()

    def update(self):
        """Update game state"""
        # Advance day
        self.state.day += 1

        # Consume resources
        food_per_dweller = 1
        water_per_dweller = 1
        power_per_room = 2

        self.resources['food'] -= self.state.population * food_per_dweller
        self.resources['water'] -= self.state.population * water_per_dweller
        self.resources['power'] -= len(self.rooms) * power_per_room

        # Check for problems
        if self.resources['food'] < 0:
            self.state.happiness -= 10
            print("\n⚠️  Food shortage! Happiness decreased.")
            input("Press Enter...")

        # Auto-save
        if self.config.should_auto_save():
            if self.turn % self.config.gameplay.auto_save_interval == 0:
                self.save_game()

    def build_room_menu(self):
        """Room building menu"""
        print("\n🏗️  Build Room")
        print("(Placeholder - would show room options)")
        input("Press Enter...")

    def manage_dwellers_menu(self):
        """Dweller management menu"""
        print("\n👥 Manage Dwellers")
        print(f"Population: {self.state.population}")
        print("(Placeholder - would show dweller list)")
        input("Press Enter...")

    def quests_menu(self):
        """Quests menu"""
        print("\n🎯 Quests")
        print("(Placeholder - would show active quests)")
        input("Press Enter...")

    def save_game(self):
        """Save game state"""
        save_data = {
            'state': {
                'day': self.state.day,
                'caps': self.state.caps,
                'population': self.state.population,
                'happiness': self.state.happiness,
                'vault_level': self.state.vault_level
            },
            'resources': self.resources,
            'turn': self.turn
        }

        self.save_system.save(
            game_id='vault_shelter',
            game_name='Vault Shelter',
            data=save_data,
            save_slot=1,
            play_time=self.turn * 30
        )

        print("\n💾 Game saved successfully!")
        self.logger.info(f"Game saved - Day {self.state.day}")
        input("Press Enter...")

    def load_game(self):
        """Load saved game"""
        save_file = self.save_system.load('vault_shelter', save_slot=1)

        if save_file:
            data = save_file.data
            self.state.day = data['state']['day']
            self.state.caps = data['state']['caps']
            self.state.population = data['state']['population']
            self.state.happiness = data['state']['happiness']
            self.state.vault_level = data['state']['vault_level']
            self.resources = data['resources']
            self.turn = data['turn']

            print("\n✅ Game loaded successfully!")
            self.logger.info(f"Game loaded - Day {self.state.day}")
            return True

        return False

    def cleanup(self):
        """Cleanup on exit"""
        if self.analytics.is_enabled():
            track_game_end()

        self.logger.info(f"Game ended - Day {self.state.day}, Population {self.state.population}")

        print(f"\n{'='*60}")
        print("Final Stats:")
        print(f"  Days Survived: {self.state.day}")
        print(f"  Population: {self.state.population}")
        print(f"  Happiness: {self.state.happiness}%")
        print(f"  Caps: ${self.state.caps}")
        print(f"{'='*60}")


def main():
    """Main entry point"""
    from validation import get_menu_choice

    # Main menu
    options = ["New Game", "Load Game", "Quit"]
    choice = get_menu_choice(options, title="Vault Shelter")

    if choice == 1:
        game = VaultShelter()
        game.run()
    elif choice == 2:
        game = VaultShelter()
        if game.load_game():
            input("Press Enter to continue...")
            game.run()
        else:
            print("No save file found!")
    elif choice == 3:
        print("Goodbye!")


if __name__ == '__main__':
    main()
