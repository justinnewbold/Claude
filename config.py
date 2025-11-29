#!/usr/bin/env python3
"""
Configuration Module for VAULT 13 Game Collection
==================================================
Centralized configuration with platform-aware paths and settings.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

# Import platform utilities
try:
    from platform_utils import (
        get_app_data_dir, get_config_dir, get_save_dir,
        get_log_dir, get_cache_dir, get_game_root,
        is_windows, is_macos, is_linux, supports_color, supports_unicode
    )
except ImportError:
    # Fallback if platform_utils not available
    def get_app_data_dir(app_name="vault13"):
        return Path.home() / f'.{app_name}'

    def get_config_dir(app_name="vault13"):
        return get_app_data_dir(app_name)

    def get_save_dir(app_name="vault13"):
        return get_app_data_dir(app_name) / 'saves'

    def get_log_dir(app_name="vault13"):
        return get_app_data_dir(app_name) / 'logs'

    def get_cache_dir(app_name="vault13"):
        return get_app_data_dir(app_name) / 'cache'

    def get_game_root():
        return Path(__file__).parent.resolve()

    def is_windows():
        return os.name == 'nt'

    def is_macos():
        import platform
        return platform.system() == 'Darwin'

    def is_linux():
        import platform
        return platform.system() == 'Linux'

    def supports_color():
        return True

    def supports_unicode():
        return True


# =============================================================================
# APPLICATION INFO
# =============================================================================

APP_NAME = "vault13"
APP_VERSION = "9.0.0"
APP_DISPLAY_NAME = "VAULT 13 - Survival Protocol"
APP_AUTHOR = "The Vault Collective"


# =============================================================================
# DIRECTORY PATHS
# =============================================================================

class Paths:
    """Centralized path management."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Core directories
        self.game_root = get_game_root()
        self.app_data = get_app_data_dir(APP_NAME)
        self.config_dir = get_config_dir(APP_NAME)
        self.save_dir = get_save_dir(APP_NAME)
        self.log_dir = get_log_dir(APP_NAME)
        self.cache_dir = get_cache_dir(APP_NAME)

        # Ensure directories exist
        for dir_path in [self.app_data, self.config_dir, self.save_dir, self.log_dir, self.cache_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    @property
    def config_file(self) -> Path:
        """Path to the main configuration file."""
        return self.config_dir / 'config.json'

    @property
    def settings_file(self) -> Path:
        """Path to user settings file."""
        return self.config_dir / 'settings.json'

    @property
    def achievements_file(self) -> Path:
        """Path to achievements data file."""
        return self.app_data / 'achievements.json'

    @property
    def leaderboard_file(self) -> Path:
        """Path to leaderboard data file."""
        return self.app_data / 'leaderboard.json'

    @property
    def stats_file(self) -> Path:
        """Path to statistics data file."""
        return self.app_data / 'stats.json'

    def get_save_file(self, slot: int = 0) -> Path:
        """Get path to a specific save slot."""
        if slot == 0:
            return self.save_dir / 'vault_save.json'
        return self.save_dir / f'vault_save_{slot}.json'

    def get_autosave_file(self) -> Path:
        """Get path to autosave file."""
        return self.save_dir / 'autosave.json'

    def list_save_files(self) -> list:
        """List all save files."""
        return list(self.save_dir.glob('*.json'))


# Global paths instance
paths = Paths()


# =============================================================================
# GAME SETTINGS
# =============================================================================

class Difficulty(Enum):
    """Game difficulty levels."""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    SURVIVAL = "survival"


class ColorTheme(Enum):
    """Color theme options."""
    DEFAULT = "default"
    HIGH_CONTRAST = "high_contrast"
    DARK = "dark"
    LIGHT = "light"
    COLORBLIND = "colorblind"


@dataclass
class GameSettings:
    """User-configurable game settings."""

    # Display settings
    color_enabled: bool = True
    unicode_enabled: bool = True
    color_theme: str = "default"
    show_animations: bool = True
    animation_speed: float = 1.0

    # Gameplay settings
    difficulty: str = "normal"
    autosave_enabled: bool = True
    autosave_interval: int = 60  # seconds
    tutorial_completed: bool = False

    # Audio settings (for future use)
    sound_enabled: bool = True
    music_enabled: bool = True
    sound_volume: float = 0.7
    music_volume: float = 0.5

    # Advanced settings
    debug_mode: bool = False
    show_fps: bool = False
    log_level: str = "INFO"

    # AI settings
    ai_enabled: bool = False
    ai_api_key: str = ""

    def __post_init__(self):
        """Validate and adjust settings based on platform capabilities."""
        if not supports_color():
            self.color_enabled = False
        if not supports_unicode():
            self.unicode_enabled = False


@dataclass
class GameBalance:
    """Game balance configuration (for modding/tweaking)."""

    # Resource rates
    power_production_rate: float = 1.0
    water_production_rate: float = 1.0
    food_production_rate: float = 1.0
    resource_consumption_rate: float = 1.0

    # Dweller settings
    starting_dwellers: int = 3
    max_dwellers: int = 200
    happiness_decay_rate: float = 0.1
    health_regen_rate: float = 0.05

    # Event settings
    event_frequency: float = 1.0
    disaster_frequency: float = 1.0
    positive_event_chance: float = 0.5

    # Economy
    starting_caps: int = 500
    room_cost_multiplier: float = 1.0
    upgrade_cost_multiplier: float = 1.0

    # Combat
    combat_damage_multiplier: float = 1.0
    enemy_health_multiplier: float = 1.0


# =============================================================================
# CONFIGURATION MANAGER
# =============================================================================

class Config:
    """Main configuration manager."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.paths = paths
        self.settings = GameSettings()
        self.balance = GameBalance()
        self._load()

    def _load(self):
        """Load configuration from files."""
        # Load settings
        if self.paths.settings_file.exists():
            try:
                with open(self.paths.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load settings: {e}")

        # Load balance (if custom balance file exists)
        balance_file = self.paths.config_dir / 'balance.json'
        if balance_file.exists():
            try:
                with open(balance_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self.balance, key):
                            setattr(self.balance, key, value)
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        """Save configuration to files."""
        # Save settings
        try:
            with open(self.paths.settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")

    def reset_settings(self):
        """Reset settings to defaults."""
        self.settings = GameSettings()
        self.save()

    def reset_balance(self):
        """Reset game balance to defaults."""
        self.balance = GameBalance()

    def get_difficulty_multipliers(self) -> Dict[str, float]:
        """Get multipliers based on current difficulty."""
        difficulty = self.settings.difficulty.lower()

        multipliers = {
            'easy': {
                'resource_production': 1.5,
                'resource_consumption': 0.7,
                'event_frequency': 0.5,
                'disaster_frequency': 0.3,
                'enemy_damage': 0.7,
            },
            'normal': {
                'resource_production': 1.0,
                'resource_consumption': 1.0,
                'event_frequency': 1.0,
                'disaster_frequency': 1.0,
                'enemy_damage': 1.0,
            },
            'hard': {
                'resource_production': 0.8,
                'resource_consumption': 1.2,
                'event_frequency': 1.3,
                'disaster_frequency': 1.5,
                'enemy_damage': 1.3,
            },
            'survival': {
                'resource_production': 0.5,
                'resource_consumption': 1.5,
                'event_frequency': 2.0,
                'disaster_frequency': 2.0,
                'enemy_damage': 2.0,
            },
        }

        return multipliers.get(difficulty, multipliers['normal'])


# Global config instance
config = Config()


# =============================================================================
# GAME REGISTRY
# =============================================================================

@dataclass
class GameInfo:
    """Information about a game in the collection."""
    id: str
    name: str
    file: str
    description: str = ""
    category: str = "other"
    version: str = "1.0"
    playable: bool = True


# Registry of all games in the collection
GAME_REGISTRY: Dict[str, GameInfo] = {
    # Main Games - Primary Entry Point
    'vault13_progression': GameInfo(
        id='vault13_progression',
        name='VAULT 13 - Training Protocol',
        file='vault13_progression.py',
        description='12 training vaults leading to the main Vault 13 experience with star ratings and narrative fragments',
        category='main',
        version='10.0'
    ),
    'vault_shelter_v10': GameInfo(
        id='vault_shelter_v10',
        name='VAULT 13 v10.0 - Comprehensive Evolution',
        file='vault_shelter_v10.py',
        description='Full vault management with all 10 phases of improvements',
        category='main',
        version='10.0'
    ),
    'vault_shelter_v6': GameInfo(
        id='vault_shelter_v6',
        name='VAULT 13 v9.0 - Ultimate Evolution',
        file='vault_shelter_v6.py',
        description='Complete vault management with mental health, diseases, and full simulation',
        category='main',
        version='9.0'
    ),
    'vault_shelter_v5.5': GameInfo(
        id='vault_shelter_v5.5',
        name='VAULT 13 v5.5 - Extended',
        file='vault_shelter_v5.5.py',
        description='Extended version with traits and mutations',
        category='main',
        version='5.5'
    ),
    'vault_shelter_v5': GameInfo(
        id='vault_shelter_v5',
        name='VAULT 13 v5.0 - Mega',
        file='vault_shelter_v5.py',
        description='9 game systems including families, tech trees, and trading',
        category='main',
        version='5.0'
    ),
    'vault_shelter_v4': GameInfo(
        id='vault_shelter_v4',
        name='VAULT 13 v4.0 - Ultimate',
        file='vault_shelter_v4.py',
        description='Quest system, exploration, and skill trees',
        category='main',
        version='4.0'
    ),
    'vault_shelter_ai': GameInfo(
        id='vault_shelter_ai',
        name='VAULT 13 v3.0 - AI Edition',
        file='vault_shelter_ai.py',
        description='AI advisor integration with Claude',
        category='main',
        version='3.0'
    ),
    'vault_shelter': GameInfo(
        id='vault_shelter',
        name='VAULT 13 v2.0 - Classic',
        file='vault_shelter.py',
        description='Classic vault survival experience',
        category='main',
        version='2.0'
    ),

    # Quantum & Physics Mini-Games
    'echo_chambers': GameInfo(
        id='echo_chambers',
        name='Echo Chambers',
        file='echo_chambers.py',
        description='Navigate through decaying timelines and echoes',
        category='quantum'
    ),
    'schrodingers_dungeon': GameInfo(
        id='schrodingers_dungeon',
        name="Schrodinger's Dungeon",
        file='schrodingers_dungeon.py',
        description='Quantum superposition dungeon crawler',
        category='quantum'
    ),
    'quantum_eraser': GameInfo(
        id='quantum_eraser',
        name='Quantum Eraser',
        file='quantum_eraser.py',
        description='Explore quantum measurement and observation',
        category='quantum'
    ),
    'entanglement': GameInfo(
        id='entanglement',
        name='Entanglement',
        file='entanglement.py',
        description='Quantum entanglement puzzle game',
        category='quantum'
    ),
    'butterfly_effect': GameInfo(
        id='butterfly_effect',
        name='The Butterfly Effect',
        file='butterfly_effect.py',
        description='Chaos theory and cascading consequences',
        category='physics'
    ),
    'emergence_engine': GameInfo(
        id='emergence_engine',
        name='The Emergence Engine',
        file='emergence_engine.py',
        description='Emergent behavior and cellular automata',
        category='physics'
    ),
    'maxwells_demon': GameInfo(
        id='maxwells_demon',
        name="Maxwell's Demon",
        file='maxwells_demon.py',
        description='Thermodynamics thought experiment',
        category='physics'
    ),
    'laplaces_demon': GameInfo(
        id='laplaces_demon',
        name="Laplace's Demon",
        file='laplaces_demon.py',
        description='Determinism and prediction',
        category='physics'
    ),
    'twin_paradox': GameInfo(
        id='twin_paradox',
        name='Twin Paradox',
        file='twin_paradox.py',
        description='Time dilation and relativity',
        category='physics'
    ),

    # Computation & Logic Mini-Games
    'halting_problem': GameInfo(
        id='halting_problem',
        name='The Halting Problem',
        file='halting_problem.py',
        description='Computability and undecidability',
        category='computation'
    ),
    'last_recursion': GameInfo(
        id='last_recursion',
        name='The Last Recursion',
        file='last_recursion.py',
        description='Stack frames and recursive descent',
        category='computation'
    ),
    'syntax_tree_climber': GameInfo(
        id='syntax_tree_climber',
        name='Syntax Tree Climber',
        file='syntax_tree_climber.py',
        description='Navigate abstract syntax trees',
        category='computation'
    ),
    'code_archaeology': GameInfo(
        id='code_archaeology',
        name='Code Archaeology',
        file='code_archaeology.py',
        description='Explore and decode ancient code',
        category='computation'
    ),
    'godels_paradox': GameInfo(
        id='godels_paradox',
        name="Godel's Paradox",
        file='godels_paradox.py',
        description='Incompleteness and self-reference',
        category='logic'
    ),
    'infinite_library': GameInfo(
        id='infinite_library',
        name='The Infinite Library',
        file='infinite_library.py',
        description='Borges-inspired infinite book exploration',
        category='logic'
    ),
    'zenos_runner': GameInfo(
        id='zenos_runner',
        name="Zeno's Runner",
        file='zenos_runner.py',
        description='Infinity and paradoxes of motion',
        category='logic'
    ),
    'sorites_paradox': GameInfo(
        id='sorites_paradox',
        name='Sorites Paradox',
        file='sorites_paradox.py',
        description='The paradox of the heap',
        category='logic'
    ),

    # Philosophy & Decision Mini-Games
    'chinese_room': GameInfo(
        id='chinese_room',
        name='The Chinese Room',
        file='chinese_room.py',
        description='Consciousness and understanding',
        category='philosophy'
    ),
    'marys_room': GameInfo(
        id='marys_room',
        name="Mary's Room",
        file='marys_room.py',
        description='Knowledge and qualia',
        category='philosophy'
    ),
    'platos_cave': GameInfo(
        id='platos_cave',
        name="Plato's Cave",
        file='platos_cave.py',
        description='Reality and perception',
        category='philosophy'
    ),
    'ship_of_theseus': GameInfo(
        id='ship_of_theseus',
        name='Ship of Theseus',
        file='ship_of_theseus.py',
        description='Identity and persistence',
        category='philosophy'
    ),
    'trolley_problem': GameInfo(
        id='trolley_problem',
        name='Trolley Problem',
        file='trolley_problem.py',
        description='Ethics and moral dilemmas',
        category='decision'
    ),
    'prisoners_dilemma': GameInfo(
        id='prisoners_dilemma',
        name="Prisoner's Dilemma",
        file='prisoners_dilemma.py',
        description='Game theory and cooperation',
        category='decision'
    ),
    'newcombs_paradox': GameInfo(
        id='newcombs_paradox',
        name="Newcomb's Paradox",
        file='newcombs_paradox.py',
        description='Free will and prediction',
        category='decision'
    ),
    'pascals_wager': GameInfo(
        id='pascals_wager',
        name="Pascal's Wager",
        file='pascals_wager.py',
        description='Decision theory and belief',
        category='decision'
    ),
    'monty_hall': GameInfo(
        id='monty_hall',
        name='Monty Hall',
        file='monty_hall.py',
        description='Probability and intuition',
        category='decision'
    ),
    'sleeping_beauty': GameInfo(
        id='sleeping_beauty',
        name='Sleeping Beauty',
        file='sleeping_beauty.py',
        description='Probability and self-location',
        category='decision'
    ),

    # Other Mini-Games
    'forking_paths': GameInfo(
        id='forking_paths',
        name='Garden of Forking Paths',
        file='forking_paths.py',
        description='Branching narratives and choices',
        category='other'
    ),
    'bootstrap_paradox': GameInfo(
        id='bootstrap_paradox',
        name='Bootstrap Paradox',
        file='bootstrap_paradox.py',
        description='Time travel and causality',
        category='other'
    ),
    'boltzmann_brains': GameInfo(
        id='boltzmann_brains',
        name='Boltzmann Brains',
        file='boltzmann_brains.py',
        description='Statistical mechanics and existence',
        category='other'
    ),
    'simulation_hypothesis': GameInfo(
        id='simulation_hypothesis',
        name='Simulation Hypothesis',
        file='simulation_hypothesis.py',
        description='Are we living in a simulation?',
        category='other'
    ),
    'doomsday_argument': GameInfo(
        id='doomsday_argument',
        name='Doomsday Argument',
        file='doomsday_argument.py',
        description='Probability and human extinction',
        category='other'
    ),
    'munchhausen_trilemma': GameInfo(
        id='munchhausen_trilemma',
        name='Munchhausen Trilemma',
        file='munchhausen_trilemma.py',
        description='Justification and knowledge',
        category='other'
    ),
    'braess_paradox': GameInfo(
        id='braess_paradox',
        name="Braess's Paradox",
        file='braess_paradox.py',
        description='Networks and counterintuitive behavior',
        category='other'
    ),
    'the_categorizer': GameInfo(
        id='the_categorizer',
        name='The Categorizer',
        file='the_categorizer.py',
        description='Classification and taxonomy',
        category='other'
    ),
}


def get_games_by_category(category: str) -> list:
    """Get all games in a specific category."""
    return [g for g in GAME_REGISTRY.values() if g.category == category]


def get_all_categories() -> list:
    """Get all unique categories."""
    return list(set(g.category for g in GAME_REGISTRY.values()))


def get_game_path(game_id: str) -> Optional[Path]:
    """Get the full path to a game file."""
    if game_id in GAME_REGISTRY:
        return paths.game_root / GAME_REGISTRY[game_id].file
    return None


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_save_path(slot: int = 0) -> Path:
    """Get the path to a save file slot."""
    return paths.get_save_file(slot)


def get_autosave_path() -> Path:
    """Get the path to the autosave file."""
    return paths.get_autosave_file()


def load_json(file_path: Path) -> Optional[Dict]:
    """Load a JSON file safely."""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return None


def save_json(file_path: Path, data: Dict) -> bool:
    """Save data to a JSON file safely."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == '__main__':
    print(f"{APP_DISPLAY_NAME} v{APP_VERSION}")
    print("=" * 50)

    print(f"\nPaths:")
    print(f"  Game root: {paths.game_root}")
    print(f"  App data:  {paths.app_data}")
    print(f"  Config:    {paths.config_dir}")
    print(f"  Saves:     {paths.save_dir}")
    print(f"  Logs:      {paths.log_dir}")

    print(f"\nSettings:")
    print(f"  Color enabled:   {config.settings.color_enabled}")
    print(f"  Unicode enabled: {config.settings.unicode_enabled}")
    print(f"  Difficulty:      {config.settings.difficulty}")

    print(f"\nGames by category:")
    for category in sorted(get_all_categories()):
        games = get_games_by_category(category)
        print(f"  {category}: {len(games)} games")

    print(f"\nTotal games: {len(GAME_REGISTRY)}")
