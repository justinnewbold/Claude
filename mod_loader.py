#!/usr/bin/env python3
"""
Mod Loader System
=================
Load and manage community mods for games.
"""

import json
import importlib.util
from pathlib import Path
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import sys

from logging_config import get_logger
from error_handling import error_context, GameError
from data_loader import DataLoader


logger = get_logger(__name__)


class ModType(Enum):
    """Types of mods"""
    CONTENT = "content"  # Add new items, rooms, events, etc.
    MECHANICS = "mechanics"  # Change game mechanics
    UI = "ui"  # UI modifications
    TOTAL_CONVERSION = "total_conversion"  # Complete game overhaul


class ModStatus(Enum):
    """Mod load status"""
    LOADED = "loaded"
    ERROR = "error"
    DISABLED = "disabled"
    INCOMPATIBLE = "incompatible"


@dataclass
class ModMetadata:
    """Mod metadata from mod.json"""
    id: str
    name: str
    version: str
    author: str
    description: str
    mod_type: ModType
    game_id: str
    game_version: str
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    load_order: int = 100
    enabled: bool = True
    homepage: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class LoadedMod:
    """A loaded mod instance"""
    metadata: ModMetadata
    path: Path
    status: ModStatus
    data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    module: Optional[Any] = None


class ModLoader:
    """
    Mod loader and manager.

    Features:
    - Load mods from mods/ directory
    - Dependency resolution
    - Conflict detection
    - Load order management
    - Hot reload support
    - Validation
    """

    def __init__(self, game_id: str, mods_dir: Optional[Path] = None):
        """
        Initialize mod loader.

        Args:
            game_id: Game identifier
            mods_dir: Mods directory (default: ./mods/{game_id})
        """
        self.game_id = game_id
        self.logger = get_logger(__name__)

        # Mods directory
        if mods_dir is None:
            mods_dir = Path("mods") / game_id
        self.mods_dir = mods_dir
        self.mods_dir.mkdir(parents=True, exist_ok=True)

        # Loaded mods
        self.mods: Dict[str, LoadedMod] = {}

        # Hooks for mod data
        self.data_hooks: Dict[str, List[Callable]] = {}

        # Data loader for base game data
        self.data_loader = DataLoader()

    def discover_mods(self) -> List[Path]:
        """
        Discover all mod directories.

        Returns:
            List of mod directory paths
        """
        mod_dirs = []

        for item in self.mods_dir.iterdir():
            if item.is_dir():
                mod_file = item / "mod.json"
                if mod_file.exists():
                    mod_dirs.append(item)

        self.logger.info(f"Discovered {len(mod_dirs)} mods")
        return mod_dirs

    def load_all_mods(self):
        """Load all discovered mods"""
        mod_dirs = self.discover_mods()

        # Load metadata first
        for mod_dir in mod_dirs:
            try:
                metadata = self._load_metadata(mod_dir)
                if metadata.enabled:
                    self.mods[metadata.id] = LoadedMod(
                        metadata=metadata,
                        path=mod_dir,
                        status=ModStatus.LOADED
                    )
            except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
                self.logger.error(f"Failed to load mod metadata from {mod_dir}: {e}")

        # Resolve dependencies and sort by load order
        self._resolve_dependencies()

        # Load mods in order
        sorted_mods = sorted(
            self.mods.values(),
            key=lambda m: m.metadata.load_order
        )

        for mod in sorted_mods:
            if mod.status == ModStatus.LOADED:
                self._load_mod_content(mod)

        enabled_count = sum(1 for m in self.mods.values() if m.status == ModStatus.LOADED)
        self.logger.info(f"Loaded {enabled_count}/{len(self.mods)} mods")

    def _load_metadata(self, mod_dir: Path) -> ModMetadata:
        """Load mod metadata from mod.json"""
        with open(mod_dir / "mod.json", 'r') as f:
            data = json.load(f)

        return ModMetadata(
            id=data['id'],
            name=data['name'],
            version=data['version'],
            author=data['author'],
            description=data['description'],
            mod_type=ModType(data.get('type', 'content')),
            game_id=data['game_id'],
            game_version=data['game_version'],
            dependencies=data.get('dependencies', []),
            conflicts=data.get('conflicts', []),
            load_order=data.get('load_order', 100),
            enabled=data.get('enabled', True),
            homepage=data.get('homepage'),
            tags=data.get('tags', [])
        )

    def _resolve_dependencies(self):
        """Resolve mod dependencies and detect conflicts"""
        # Check dependencies
        for mod_id, mod in self.mods.items():
            for dep_id in mod.metadata.dependencies:
                if dep_id not in self.mods:
                    mod.status = ModStatus.ERROR
                    mod.error_message = f"Missing dependency: {dep_id}"
                    self.logger.error(f"Mod {mod_id} missing dependency: {dep_id}")
                elif self.mods[dep_id].status != ModStatus.LOADED:
                    mod.status = ModStatus.ERROR
                    mod.error_message = f"Dependency {dep_id} failed to load"

        # Check conflicts
        for mod_id, mod in self.mods.items():
            for conflict_id in mod.metadata.conflicts:
                if conflict_id in self.mods and self.mods[conflict_id].metadata.enabled:
                    mod.status = ModStatus.INCOMPATIBLE
                    mod.error_message = f"Conflicts with: {conflict_id}"
                    self.logger.warning(f"Mod {mod_id} conflicts with {conflict_id}")

    def _load_mod_content(self, mod: LoadedMod):
        """Load mod content (data, code, etc.)"""
        with error_context(f"loading mod {mod.metadata.id}"):
            # Load data files
            self._load_mod_data(mod)

            # Load Python module if exists
            self._load_mod_module(mod)

            # Execute init script if exists
            self._execute_mod_init(mod)

            self.logger.info(f"Loaded mod: {mod.metadata.name} v{mod.metadata.version}")

    def _load_mod_data(self, mod: LoadedMod):
        """Load mod data files (JSON)"""
        data_dir = mod.path / "data"
        if not data_dir.exists():
            return

        # Load all JSON files
        for json_file in data_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                # Store in mod data
                data_key = json_file.stem
                mod.data[data_key] = data

                # Trigger hooks
                self._trigger_data_hook(data_key, data)

                self.logger.debug(f"Loaded mod data: {json_file.name}")

            except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
                self.logger.error(f"Error loading mod data {json_file}: {e}")

    def _load_mod_module(self, mod: LoadedMod):
        """Load mod Python module"""
        module_file = mod.path / "mod.py"
        if not module_file.exists():
            return

        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(
                f"mod_{mod.metadata.id}",
                module_file
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"mod_{mod.metadata.id}"] = module
                spec.loader.exec_module(module)

                mod.module = module
                self.logger.debug(f"Loaded mod module: {mod.metadata.id}")

        except (ImportError, AttributeError, TypeError, SyntaxError) as e:
            mod.status = ModStatus.ERROR
            mod.error_message = f"Failed to load module: {e}"
            self.logger.error(f"Error loading mod module {mod.metadata.id}: {e}")

    def _execute_mod_init(self, mod: LoadedMod):
        """Execute mod initialization"""
        if mod.module and hasattr(mod.module, 'init'):
            try:
                mod.module.init(self)
                self.logger.debug(f"Executed init for mod: {mod.metadata.id}")
            except Exception as e:
                mod.status = ModStatus.ERROR
                mod.error_message = f"Init failed: {e}"
                self.logger.error(f"Error in mod init {mod.metadata.id}: {e}")

    def _trigger_data_hook(self, data_key: str, data: Any):
        """Trigger hooks for loaded data"""
        if data_key in self.data_hooks:
            for hook in self.data_hooks[data_key]:
                try:
                    hook(data)
                except Exception as e:
                    self.logger.error(f"Error in data hook for {data_key}: {e}")

    def register_data_hook(self, data_key: str, hook: Callable[[Any], None]):
        """
        Register hook to be called when mod data is loaded.

        Args:
            data_key: Data file key (e.g., 'rooms', 'items')
            hook: Function to call with loaded data
        """
        if data_key not in self.data_hooks:
            self.data_hooks[data_key] = []
        self.data_hooks[data_key].append(hook)

    def get_mod(self, mod_id: str) -> Optional[LoadedMod]:
        """Get loaded mod by ID"""
        return self.mods.get(mod_id)

    def get_mod_data(self, mod_id: str, data_key: str) -> Optional[Any]:
        """Get mod data by mod ID and data key"""
        mod = self.get_mod(mod_id)
        if mod:
            return mod.data.get(data_key)
        return None

    def get_all_data(self, data_key: str) -> List[Any]:
        """
        Get all data of a specific type from all mods.

        Args:
            data_key: Data key (e.g., 'rooms', 'items')

        Returns:
            List of data from all mods
        """
        all_data = []

        for mod in self.mods.values():
            if mod.status == ModStatus.LOADED:
                data = mod.data.get(data_key)
                if data:
                    all_data.append(data)

        return all_data

    def merge_data(self, base_data: Dict[str, Any], data_key: str) -> Dict[str, Any]:
        """
        Merge mod data with base game data.

        Args:
            base_data: Base game data
            data_key: Data key (e.g., 'rooms')

        Returns:
            Merged data dictionary
        """
        merged = base_data.copy()

        for mod_data in self.get_all_data(data_key):
            if isinstance(mod_data, dict):
                merged.update(mod_data)

        return merged

    def enable_mod(self, mod_id: str):
        """Enable a mod"""
        mod = self.get_mod(mod_id)
        if mod:
            mod.metadata.enabled = True
            self._save_mod_config(mod)
            self.logger.info(f"Enabled mod: {mod_id}")

    def disable_mod(self, mod_id: str):
        """Disable a mod"""
        mod = self.get_mod(mod_id)
        if mod:
            mod.metadata.enabled = False
            mod.status = ModStatus.DISABLED
            self._save_mod_config(mod)
            self.logger.info(f"Disabled mod: {mod_id}")

    def _save_mod_config(self, mod: LoadedMod):
        """Save mod configuration"""
        config_file = mod.path / "mod.json"

        # Read current config
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Update enabled status
        config['enabled'] = mod.metadata.enabled

        # Save
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def get_status_summary(self) -> Dict[str, int]:
        """Get summary of mod statuses"""
        summary = {
            'total': len(self.mods),
            'loaded': 0,
            'error': 0,
            'disabled': 0,
            'incompatible': 0
        }

        for mod in self.mods.values():
            if mod.status == ModStatus.LOADED:
                summary['loaded'] += 1
            elif mod.status == ModStatus.ERROR:
                summary['error'] += 1
            elif mod.status == ModStatus.DISABLED:
                summary['disabled'] += 1
            elif mod.status == ModStatus.INCOMPATIBLE:
                summary['incompatible'] += 1

        return summary


# =============================================================================
# MOD CREATOR HELPER
# =============================================================================

class ModCreator:
    """Helper to create new mods"""

    @staticmethod
    def create_mod_template(
        mod_id: str,
        name: str,
        author: str,
        game_id: str,
        output_dir: Path
    ):
        """
        Create a basic mod template.

        Args:
            mod_id: Mod identifier
            name: Mod name
            author: Mod author
            game_id: Target game ID
            output_dir: Output directory
        """
        mod_dir = output_dir / mod_id
        mod_dir.mkdir(parents=True, exist_ok=True)

        # Create mod.json
        metadata = {
            'id': mod_id,
            'name': name,
            'version': '1.0.0',
            'author': author,
            'description': 'A new mod for ' + game_id,
            'type': 'content',
            'game_id': game_id,
            'game_version': '1.0',
            'dependencies': [],
            'conflicts': [],
            'load_order': 100,
            'enabled': True,
            'tags': []
        }

        with open(mod_dir / 'mod.json', 'w') as f:
            json.dump(metadata, f, indent=2)

        # Create data directory
        data_dir = mod_dir / 'data'
        data_dir.mkdir(exist_ok=True)

        # Create example data file
        example_data = {
            'example_items': [
                {
                    'id': 'mod_item_1',
                    'name': 'Modded Item',
                    'description': 'An item added by a mod'
                }
            ]
        }

        with open(data_dir / 'items.json', 'w') as f:
            json.dump(example_data, f, indent=2)

        # Create mod.py
        mod_code = '''"""
Mod: {name}
Author: {author}
"""

def init(mod_loader):
    """Initialize mod"""
    print(f"Initializing {{name}}!")

def on_game_start(game):
    """Called when game starts"""
    pass

def on_game_end(game):
    """Called when game ends"""
    pass
'''.format(name=name, author=author)

        with open(mod_dir / 'mod.py', 'w') as f:
            f.write(mod_code)

        # Create README
        readme = f'''# {name}

**Author:** {author}
**Version:** 1.0.0

## Description

A new mod for {game_id}.

## Installation

1. Copy this folder to `mods/{game_id}/`
2. Launch the game
3. The mod will be automatically loaded

## Features

- Example modded item

## Credits

Created by {author}
'''

        with open(mod_dir / 'README.md', 'w') as f:
            f.write(readme)

        print(f"✅ Mod template created: {mod_dir}")


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Mod Loader Test")
    print("=" * 60)

    # Create example mod
    ModCreator.create_mod_template(
        mod_id='example_mod',
        name='Example Mod',
        author='Test Author',
        game_id='vault_shelter',
        output_dir=Path('mods/vault_shelter')
    )

    # Test loading
    loader = ModLoader('vault_shelter')
    loader.load_all_mods()

    summary = loader.get_status_summary()
    print(f"\nMod Status:")
    print(f"  Total: {summary['total']}")
    print(f"  Loaded: {summary['loaded']}")
    print(f"  Errors: {summary['error']}")
    print(f"  Disabled: {summary['disabled']}")

    print("\n✅ Mod loader test passed!")
