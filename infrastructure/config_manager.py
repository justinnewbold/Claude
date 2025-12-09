#!/usr/bin/env python3
"""
Configuration Management System
================================
User preferences and game settings management.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from logging_config import get_logger
from error_handling import error_context, GameError


logger = get_logger(__name__)


class TextSpeed(Enum):
    """Text display speed options"""
    INSTANT = 0.0
    FAST = 0.01
    NORMAL = 0.03
    SLOW = 0.05
    VERY_SLOW = 0.08


class Difficulty(Enum):
    """Game difficulty levels"""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    EXTREME = "extreme"


class ColorScheme(Enum):
    """Terminal color schemes"""
    DEFAULT = "default"
    HIGH_CONTRAST = "high_contrast"
    MONOCHROME = "monochrome"
    COLORBLIND = "colorblind"
    CUSTOM = "custom"


@dataclass
class DisplaySettings:
    """Display-related settings"""
    text_speed: TextSpeed = TextSpeed.NORMAL
    color_scheme: ColorScheme = ColorScheme.DEFAULT
    show_tooltips: bool = True
    show_animations: bool = True
    screen_width: int = 80
    screen_height: int = 24
    fps: int = 30


@dataclass
class GameplaySettings:
    """Gameplay-related settings"""
    difficulty: Difficulty = Difficulty.NORMAL
    auto_save: bool = True
    auto_save_interval: int = 5  # turns
    confirm_quit: bool = True
    confirm_dangerous_actions: bool = True
    tutorial_enabled: bool = True
    hints_enabled: bool = True


@dataclass
class AudioSettings:
    """Audio settings (for future sound support)"""
    sound_enabled: bool = True
    music_enabled: bool = True
    music_volume: float = 0.7
    sfx_volume: float = 0.8
    voice_volume: float = 1.0


@dataclass
class AccessibilitySettings:
    """Accessibility options"""
    high_contrast_mode: bool = False
    large_text: bool = False
    screen_reader_mode: bool = False
    reduced_motion: bool = False
    colorblind_mode: Optional[str] = None  # deuteranopia, protanopia, tritanopia


@dataclass
class KeyBindings:
    """Keyboard key bindings"""
    up: str = 'w'
    down: str = 's'
    left: str = 'a'
    right: str = 'd'
    confirm: str = 'enter'
    cancel: str = 'esc'
    menu: str = 'tab'
    inventory: str = 'i'
    map: str = 'm'
    help: str = 'h'
    quicksave: str = 'f5'
    quickload: str = 'f9'


@dataclass
class PrivacySettings:
    """Privacy and telemetry settings"""
    analytics_enabled: bool = False
    crash_reports_enabled: bool = True
    usage_stats_enabled: bool = False
    cloud_saves_enabled: bool = False


class ConfigManager:
    """
    Manages user configuration and preferences.

    Features:
    - Save/load user preferences
    - Per-game settings override
    - Default values
    - Migration of old configs
    - Validation
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_dir: Directory for config files (default: ~/.vault13)
        """
        self.logger = get_logger(__name__)

        # Config directory
        if config_dir is None:
            config_dir = Path.home() / ".vault13"
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Config file paths
        self.main_config_file = self.config_dir / "config.json"
        self.games_config_dir = self.config_dir / "games"
        self.games_config_dir.mkdir(exist_ok=True)

        # Settings
        self.display = DisplaySettings()
        self.gameplay = GameplaySettings()
        self.audio = AudioSettings()
        self.accessibility = AccessibilitySettings()
        self.keybindings = KeyBindings()
        self.privacy = PrivacySettings()

        # Game-specific overrides
        self.game_configs: Dict[str, Dict[str, Any]] = {}

        # Load existing config
        self.load()

    def load(self):
        """Load configuration from disk"""
        if not self.main_config_file.exists():
            self.logger.info("No config file found, using defaults")
            return

        with error_context("loading configuration"):
            with open(self.main_config_file, 'r') as f:
                data = json.load(f)

            # Load settings sections
            if 'display' in data:
                self._load_display(data['display'])
            if 'gameplay' in data:
                self._load_gameplay(data['gameplay'])
            if 'audio' in data:
                self._load_audio(data['audio'])
            if 'accessibility' in data:
                self._load_accessibility(data['accessibility'])
            if 'keybindings' in data:
                self._load_keybindings(data['keybindings'])
            if 'privacy' in data:
                self._load_privacy(data['privacy'])

            self.logger.info("Configuration loaded")

    def save(self):
        """Save configuration to disk"""
        with error_context("saving configuration"):
            data = {
                'version': '1.0',
                'display': self._serialize_display(),
                'gameplay': self._serialize_gameplay(),
                'audio': self._serialize_audio(),
                'accessibility': self._serialize_accessibility(),
                'keybindings': asdict(self.keybindings),
                'privacy': asdict(self.privacy)
            }

            with open(self.main_config_file, 'w') as f:
                json.dump(data, f, indent=2)

            self.logger.info("Configuration saved")

    def _load_display(self, data: Dict[str, Any]):
        """Load display settings"""
        self.display.text_speed = TextSpeed(data.get('text_speed', TextSpeed.NORMAL.value))
        self.display.color_scheme = ColorScheme(data.get('color_scheme', ColorScheme.DEFAULT.value))
        self.display.show_tooltips = data.get('show_tooltips', True)
        self.display.show_animations = data.get('show_animations', True)
        self.display.screen_width = data.get('screen_width', 80)
        self.display.screen_height = data.get('screen_height', 24)
        self.display.fps = data.get('fps', 30)

    def _load_gameplay(self, data: Dict[str, Any]):
        """Load gameplay settings"""
        self.gameplay.difficulty = Difficulty(data.get('difficulty', Difficulty.NORMAL.value))
        self.gameplay.auto_save = data.get('auto_save', True)
        self.gameplay.auto_save_interval = data.get('auto_save_interval', 5)
        self.gameplay.confirm_quit = data.get('confirm_quit', True)
        self.gameplay.confirm_dangerous_actions = data.get('confirm_dangerous_actions', True)
        self.gameplay.tutorial_enabled = data.get('tutorial_enabled', True)
        self.gameplay.hints_enabled = data.get('hints_enabled', True)

    def _load_audio(self, data: Dict[str, Any]):
        """Load audio settings"""
        self.audio.sound_enabled = data.get('sound_enabled', True)
        self.audio.music_enabled = data.get('music_enabled', True)
        self.audio.music_volume = data.get('music_volume', 0.7)
        self.audio.sfx_volume = data.get('sfx_volume', 0.8)
        self.audio.voice_volume = data.get('voice_volume', 1.0)

    def _load_accessibility(self, data: Dict[str, Any]):
        """Load accessibility settings"""
        self.accessibility.high_contrast_mode = data.get('high_contrast_mode', False)
        self.accessibility.large_text = data.get('large_text', False)
        self.accessibility.screen_reader_mode = data.get('screen_reader_mode', False)
        self.accessibility.reduced_motion = data.get('reduced_motion', False)
        self.accessibility.colorblind_mode = data.get('colorblind_mode')

    def _load_keybindings(self, data: Dict[str, Any]):
        """Load key bindings"""
        for key, value in data.items():
            if hasattr(self.keybindings, key):
                setattr(self.keybindings, key, value)

    def _load_privacy(self, data: Dict[str, Any]):
        """Load privacy settings"""
        self.privacy.analytics_enabled = data.get('analytics_enabled', False)
        self.privacy.crash_reports_enabled = data.get('crash_reports_enabled', True)
        self.privacy.usage_stats_enabled = data.get('usage_stats_enabled', False)
        self.privacy.cloud_saves_enabled = data.get('cloud_saves_enabled', False)

    def _serialize_display(self) -> Dict[str, Any]:
        """Serialize display settings"""
        return {
            'text_speed': self.display.text_speed.value,
            'color_scheme': self.display.color_scheme.value,
            'show_tooltips': self.display.show_tooltips,
            'show_animations': self.display.show_animations,
            'screen_width': self.display.screen_width,
            'screen_height': self.display.screen_height,
            'fps': self.display.fps
        }

    def _serialize_gameplay(self) -> Dict[str, Any]:
        """Serialize gameplay settings"""
        return {
            'difficulty': self.gameplay.difficulty.value,
            'auto_save': self.gameplay.auto_save,
            'auto_save_interval': self.gameplay.auto_save_interval,
            'confirm_quit': self.gameplay.confirm_quit,
            'confirm_dangerous_actions': self.gameplay.confirm_dangerous_actions,
            'tutorial_enabled': self.gameplay.tutorial_enabled,
            'hints_enabled': self.gameplay.hints_enabled
        }

    def _serialize_audio(self) -> Dict[str, Any]:
        """Serialize audio settings"""
        return asdict(self.audio)

    def _serialize_accessibility(self) -> Dict[str, Any]:
        """Serialize accessibility settings"""
        return asdict(self.accessibility)

    def load_game_config(self, game_id: str) -> Dict[str, Any]:
        """
        Load game-specific configuration.

        Args:
            game_id: Game identifier

        Returns:
            Game-specific settings
        """
        game_config_file = self.games_config_dir / f"{game_id}.json"

        if not game_config_file.exists():
            return {}

        with open(game_config_file, 'r') as f:
            return json.load(f)

    def save_game_config(self, game_id: str, config: Dict[str, Any]):
        """
        Save game-specific configuration.

        Args:
            game_id: Game identifier
            config: Game settings to save
        """
        game_config_file = self.games_config_dir / f"{game_id}.json"

        with open(game_config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.display = DisplaySettings()
        self.gameplay = GameplaySettings()
        self.audio = AudioSettings()
        self.accessibility = AccessibilitySettings()
        self.keybindings = KeyBindings()
        self.privacy = PrivacySettings()
        self.logger.info("Configuration reset to defaults")

    def get_text_delay(self) -> float:
        """Get current text speed delay"""
        return self.display.text_speed.value

    def should_show_tutorial(self) -> bool:
        """Check if tutorial should be shown"""
        return self.gameplay.tutorial_enabled

    def should_auto_save(self) -> bool:
        """Check if auto-save is enabled"""
        return self.gameplay.auto_save


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


# =============================================================================
# SETTINGS UI
# =============================================================================

def show_settings_menu():
    """Show interactive settings menu"""
    from validation import get_menu_choice, get_yes_no_input
    from platform_utils import clear_screen, print_header

    config = get_config()

    while True:
        clear_screen()
        print_header("⚙️  SETTINGS")

        options = [
            "🎨 Display Settings",
            "🎮 Gameplay Settings",
            "🔊 Audio Settings",
            "♿ Accessibility Settings",
            "⌨️  Key Bindings",
            "🔒 Privacy Settings",
            "💾 Save Settings",
            "🔄 Reset to Defaults",
            "← Back"
        ]

        choice = get_menu_choice(options, title="Settings Menu")

        if choice == 1:
            _show_display_settings(config)
        elif choice == 2:
            _show_gameplay_settings(config)
        elif choice == 3:
            _show_audio_settings(config)
        elif choice == 4:
            _show_accessibility_settings(config)
        elif choice == 5:
            _show_keybindings(config)
        elif choice == 6:
            _show_privacy_settings(config)
        elif choice == 7:
            config.save()
            print("\n✅ Settings saved!")
            input("Press Enter...")
        elif choice == 8:
            if get_yes_no_input("Reset all settings to defaults?", default=False):
                config.reset_to_defaults()
                config.save()
                print("\n✅ Settings reset!")
                input("Press Enter...")
        elif choice == 9:
            break


def _show_display_settings(config: ConfigManager):
    """Show display settings submenu"""
    print("\n📋 Display Settings")
    print(f"  Text Speed: {config.display.text_speed.name}")
    print(f"  Color Scheme: {config.display.color_scheme.name}")
    print(f"  Show Tooltips: {config.display.show_tooltips}")
    print(f"  Show Animations: {config.display.show_animations}")
    input("\nPress Enter to continue...")


def _show_gameplay_settings(config: ConfigManager):
    """Show gameplay settings submenu"""
    print("\n📋 Gameplay Settings")
    print(f"  Difficulty: {config.gameplay.difficulty.name}")
    print(f"  Auto-Save: {config.gameplay.auto_save}")
    print(f"  Auto-Save Interval: {config.gameplay.auto_save_interval} turns")
    print(f"  Tutorial: {config.gameplay.tutorial_enabled}")
    print(f"  Hints: {config.gameplay.hints_enabled}")
    input("\nPress Enter to continue...")


def _show_audio_settings(config: ConfigManager):
    """Show audio settings submenu"""
    print("\n📋 Audio Settings")
    print(f"  Sound: {config.audio.sound_enabled}")
    print(f"  Music: {config.audio.music_enabled}")
    print(f"  Music Volume: {int(config.audio.music_volume * 100)}%")
    print(f"  SFX Volume: {int(config.audio.sfx_volume * 100)}%")
    input("\nPress Enter to continue...")


def _show_accessibility_settings(config: ConfigManager):
    """Show accessibility settings submenu"""
    print("\n📋 Accessibility Settings")
    print(f"  High Contrast: {config.accessibility.high_contrast_mode}")
    print(f"  Large Text: {config.accessibility.large_text}")
    print(f"  Screen Reader: {config.accessibility.screen_reader_mode}")
    print(f"  Reduced Motion: {config.accessibility.reduced_motion}")
    print(f"  Colorblind Mode: {config.accessibility.colorblind_mode or 'Off'}")
    input("\nPress Enter to continue...")


def _show_keybindings(config: ConfigManager):
    """Show key bindings submenu"""
    print("\n📋 Key Bindings")
    print(f"  Up: {config.keybindings.up}")
    print(f"  Down: {config.keybindings.down}")
    print(f"  Left: {config.keybindings.left}")
    print(f"  Right: {config.keybindings.right}")
    print(f"  Menu: {config.keybindings.menu}")
    print(f"  Inventory: {config.keybindings.inventory}")
    print(f"  Quicksave: {config.keybindings.quicksave}")
    print(f"  Quickload: {config.keybindings.quickload}")
    input("\nPress Enter to continue...")


def _show_privacy_settings(config: ConfigManager):
    """Show privacy settings submenu"""
    print("\n📋 Privacy Settings")
    print(f"  Analytics: {config.privacy.analytics_enabled}")
    print(f"  Crash Reports: {config.privacy.crash_reports_enabled}")
    print(f"  Usage Stats: {config.privacy.usage_stats_enabled}")
    print(f"  Cloud Saves: {config.privacy.cloud_saves_enabled}")
    input("\nPress Enter to continue...")


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Configuration Manager Test")
    print("=" * 60)

    # Create config
    config = ConfigManager()

    print(f"Config directory: {config.config_dir}")
    print(f"Text speed: {config.display.text_speed.name}")
    print(f"Difficulty: {config.gameplay.difficulty.name}")
    print(f"Auto-save: {config.gameplay.auto_save}")

    # Test save
    config.save()
    print("\n✅ Configuration saved!")

    # Test load
    config2 = ConfigManager()
    print(f"\n✅ Configuration loaded!")
    print(f"Text speed: {config2.display.text_speed.name}")

    # Test settings menu
    print("\n" + "=" * 60)
    show_settings_menu()
