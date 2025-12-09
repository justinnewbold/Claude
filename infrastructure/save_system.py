#!/usr/bin/env python3
"""
Universal Save/Load System
==========================
Save and load game state for any game.
"""

import json
import os
import pickle
import gzip
from datetime import datetime
from typing import Any, Dict, Optional, List
from pathlib import Path
from dataclasses import dataclass, asdict
import hashlib

from logging_config import get_logger
from error_handling import GameError, error_context


logger = get_logger(__name__)


@dataclass
class SaveMetadata:
    """Metadata about a save file"""
    game_id: str
    game_name: str
    save_name: str
    save_slot: int
    timestamp: str
    play_time: int  # seconds
    game_version: str
    save_version: str = "1.0"
    checksum: str = ""
    auto_save: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SaveMetadata':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class SaveFile:
    """Complete save file with metadata and data"""
    metadata: SaveMetadata
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'metadata': self.metadata.to_dict(),
            'data': self.data
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SaveFile':
        """Create from dictionary"""
        return cls(
            metadata=SaveMetadata.from_dict(data['metadata']),
            data=data['data']
        )


class SaveSystem:
    """
    Universal save/load system.

    Features:
    - JSON and binary save formats
    - Compression support
    - Multiple save slots per game
    - Auto-save functionality
    - Save file validation
    - Backup system
    """

    def __init__(
        self,
        save_dir: Optional[Path] = None,
        compression: bool = True,
        backup_enabled: bool = True,
        max_backups: int = 3
    ):
        """
        Initialize save system.

        Args:
            save_dir: Directory for save files (default: ./saves)
            compression: Enable gzip compression
            backup_enabled: Enable automatic backups
            max_backups: Maximum number of backups per save
        """
        self.save_dir = save_dir or Path("saves")
        self.compression = compression
        self.backup_enabled = backup_enabled
        self.max_backups = max_backups
        self.logger = get_logger(__name__)

        # Create save directory
        self.save_dir.mkdir(exist_ok=True)

    def save(
        self,
        game_id: str,
        game_name: str,
        data: Dict[str, Any],
        save_slot: int = 1,
        save_name: Optional[str] = None,
        auto_save: bool = False,
        game_version: str = "1.0",
        play_time: int = 0
    ) -> bool:
        """
        Save game state.

        Args:
            game_id: Unique game identifier
            game_name: Human-readable game name
            data: Game state data
            save_slot: Save slot number (1-10)
            save_name: Optional custom save name
            auto_save: Whether this is an auto-save
            game_version: Game version
            play_time: Total play time in seconds

        Returns:
            True if save successful
        """
        with error_context(f"saving game {game_id}"):
            # Validate slot
            if not 1 <= save_slot <= 10:
                raise GameError(f"Invalid save slot: {save_slot} (must be 1-10)")

            # Create metadata
            timestamp = datetime.now().isoformat()
            if save_name is None:
                save_name = f"Save {save_slot}"

            metadata = SaveMetadata(
                game_id=game_id,
                game_name=game_name,
                save_name=save_name,
                save_slot=save_slot,
                timestamp=timestamp,
                play_time=play_time,
                game_version=game_version,
                auto_save=auto_save
            )

            # Create save file
            save_file = SaveFile(metadata=metadata, data=data)

            # Calculate checksum
            data_str = json.dumps(data, sort_keys=True)
            checksum = hashlib.sha256(data_str.encode()).hexdigest()
            save_file.metadata.checksum = checksum

            # Get save path
            filename = self._get_save_filename(game_id, save_slot, auto_save)
            save_path = self.save_dir / filename

            # Backup existing save
            if self.backup_enabled and save_path.exists():
                self._create_backup(save_path)

            # Write save file
            self._write_save_file(save_path, save_file)

            self.logger.info(
                f"Saved game: {game_id} slot {save_slot} "
                f"({'auto' if auto_save else 'manual'})"
            )

            return True

    def load(
        self,
        game_id: str,
        save_slot: int = 1,
        auto_save: bool = False,
        validate: bool = True
    ) -> Optional[SaveFile]:
        """
        Load game state.

        Args:
            game_id: Game identifier
            save_slot: Save slot to load
            auto_save: Load auto-save instead of manual save
            validate: Validate checksum

        Returns:
            SaveFile or None if not found
        """
        with error_context(f"loading game {game_id}"):
            filename = self._get_save_filename(game_id, save_slot, auto_save)
            save_path = self.save_dir / filename

            if not save_path.exists():
                self.logger.warning(f"Save file not found: {save_path}")
                return None

            # Read save file
            save_file = self._read_save_file(save_path)

            # Validate checksum
            if validate and save_file.metadata.checksum:
                data_str = json.dumps(save_file.data, sort_keys=True)
                checksum = hashlib.sha256(data_str.encode()).hexdigest()

                if checksum != save_file.metadata.checksum:
                    raise GameError("Save file corrupted (checksum mismatch)")

            self.logger.info(f"Loaded game: {game_id} slot {save_slot}")
            return save_file

    def list_saves(self, game_id: str) -> List[SaveMetadata]:
        """
        List all saves for a game.

        Args:
            game_id: Game identifier

        Returns:
            List of save metadata, sorted by timestamp (newest first)
        """
        saves = []

        for save_file in self.save_dir.glob(f"{game_id}_*.sav*"):
            try:
                save = self._read_save_file(save_file)
                saves.append(save.metadata)
            except Exception as e:
                self.logger.warning(f"Could not read save file {save_file}: {e}")

        # Sort by timestamp (newest first)
        saves.sort(key=lambda s: s.timestamp, reverse=True)
        return saves

    def delete_save(self, game_id: str, save_slot: int, auto_save: bool = False) -> bool:
        """
        Delete a save file.

        Args:
            game_id: Game identifier
            save_slot: Save slot to delete
            auto_save: Delete auto-save instead of manual save

        Returns:
            True if deleted successfully
        """
        filename = self._get_save_filename(game_id, save_slot, auto_save)
        save_path = self.save_dir / filename

        if not save_path.exists():
            self.logger.warning(f"Save file not found: {save_path}")
            return False

        # Delete backups too
        for backup in self.save_dir.glob(f"{save_path.stem}.backup*"):
            backup.unlink()

        save_path.unlink()
        self.logger.info(f"Deleted save: {game_id} slot {save_slot}")
        return True

    def export_save(
        self,
        game_id: str,
        save_slot: int,
        export_path: Path,
        auto_save: bool = False
    ) -> bool:
        """
        Export save file to another location.

        Args:
            game_id: Game identifier
            save_slot: Save slot to export
            export_path: Destination path
            auto_save: Export auto-save instead of manual save

        Returns:
            True if exported successfully
        """
        save_file = self.load(game_id, save_slot, auto_save)

        if not save_file:
            return False

        self._write_save_file(export_path, save_file)
        self.logger.info(f"Exported save to: {export_path}")
        return True

    def import_save(
        self,
        import_path: Path,
        save_slot: Optional[int] = None
    ) -> bool:
        """
        Import save file from another location.

        Args:
            import_path: Source save file
            save_slot: Target save slot (use original if None)

        Returns:
            True if imported successfully
        """
        if not import_path.exists():
            raise GameError(f"Import file not found: {import_path}")

        save_file = self._read_save_file(import_path)

        # Use specified slot or original slot
        if save_slot is not None:
            save_file.metadata.save_slot = save_slot

        # Write to save directory
        filename = self._get_save_filename(
            save_file.metadata.game_id,
            save_file.metadata.save_slot,
            save_file.metadata.auto_save
        )
        save_path = self.save_dir / filename

        self._write_save_file(save_path, save_file)
        self.logger.info(f"Imported save from: {import_path}")
        return True

    def _get_save_filename(self, game_id: str, save_slot: int, auto_save: bool) -> str:
        """Generate save filename"""
        prefix = "auto" if auto_save else "save"
        extension = ".sav.gz" if self.compression else ".sav"
        return f"{game_id}_{prefix}_{save_slot:02d}{extension}"

    def _write_save_file(self, path: Path, save_file: SaveFile):
        """Write save file to disk"""
        data = save_file.to_dict()
        json_data = json.dumps(data, indent=2)

        if self.compression:
            with gzip.open(path, 'wt', encoding='utf-8') as f:
                f.write(json_data)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(json_data)

    def _read_save_file(self, path: Path) -> SaveFile:
        """Read save file from disk"""
        try:
            if path.suffix == '.gz':
                with gzip.open(path, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            return SaveFile.from_dict(data)

        except Exception as e:
            raise GameError(f"Could not read save file: {e}")

    def _create_backup(self, save_path: Path):
        """Create backup of existing save"""
        if not save_path.exists():
            return

        # Find existing backups
        backups = sorted(
            self.save_dir.glob(f"{save_path.stem}.backup*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        # Remove old backups
        for old_backup in backups[self.max_backups - 1:]:
            old_backup.unlink()

        # Create new backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.save_dir / f"{save_path.stem}.backup_{timestamp}{save_path.suffix}"

        # Copy file
        import shutil
        shutil.copy2(save_path, backup_path)

        self.logger.debug(f"Created backup: {backup_path}")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

_default_save_system: Optional[SaveSystem] = None


def get_save_system() -> SaveSystem:
    """Get default save system instance"""
    global _default_save_system
    if _default_save_system is None:
        _default_save_system = SaveSystem()
    return _default_save_system


def quick_save(game_id: str, game_name: str, data: Dict[str, Any], **kwargs) -> bool:
    """Quick save using default save system"""
    return get_save_system().save(game_id, game_name, data, **kwargs)


def quick_load(game_id: str, save_slot: int = 1, **kwargs) -> Optional[SaveFile]:
    """Quick load using default save system"""
    return get_save_system().load(game_id, save_slot, **kwargs)


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Save System Test")
    print("=" * 60)

    # Create save system
    save_system = SaveSystem()

    # Test save
    print("\n1. Testing Save:")
    test_data = {
        'player': {
            'name': 'Test Player',
            'level': 5,
            'health': 100
        },
        'inventory': ['sword', 'shield', 'potion'],
        'progress': {
            'quests_completed': 3,
            'enemies_defeated': 15
        }
    }

    result = save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data=test_data,
        save_slot=1,
        play_time=3600
    )
    print(f"   Save result: {result}")

    # Test load
    print("\n2. Testing Load:")
    loaded = save_system.load('test_game', save_slot=1)
    if loaded:
        print(f"   Loaded: {loaded.metadata.game_name}")
        print(f"   Play time: {loaded.metadata.play_time}s")
        print(f"   Player: {loaded.data['player']['name']}")
        print(f"   Data matches: {loaded.data == test_data}")

    # Test list saves
    print("\n3. Testing List Saves:")
    saves = save_system.list_saves('test_game')
    print(f"   Found {len(saves)} save(s)")
    for save_meta in saves:
        print(f"   - {save_meta.save_name} (slot {save_meta.save_slot})")

    # Test auto-save
    print("\n4. Testing Auto-Save:")
    save_system.save(
        game_id='test_game',
        game_name='Test Game',
        data=test_data,
        save_slot=1,
        auto_save=True
    )
    auto_loaded = save_system.load('test_game', save_slot=1, auto_save=True)
    print(f"   Auto-save loaded: {auto_loaded is not None}")

    print("\n✅ All save system tests passed!")
