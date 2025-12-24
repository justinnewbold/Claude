"""
Tests for save_system module
=============================
Tests for save/load functionality and input validation.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from save_system import (
    sanitize_filename,
    validate_save_name,
    SaveMetadata,
    SaveFile,
)
from error_handling import GameError


class TestFilenameSanitization:
    """Test filename sanitization functions"""

    def test_valid_filename(self):
        """Test that valid filenames pass through"""
        assert sanitize_filename("vault_save") == "vault_save"
        assert sanitize_filename("game-save-01") == "game-save-01"
        assert sanitize_filename("save.backup") == "save.backup"

    def test_empty_filename_rejected(self):
        """Test that empty filenames are rejected"""
        with pytest.raises(GameError, match="cannot be empty"):
            sanitize_filename("")

    def test_path_traversal_rejected(self):
        """Test that path traversal attempts are rejected"""
        with pytest.raises(GameError, match="path traversal"):
            sanitize_filename("../../../etc/passwd")

        with pytest.raises(GameError, match="path traversal"):
            sanitize_filename("..\\windows\\system32")

    def test_path_separators_rejected(self):
        """Test that path separators are rejected"""
        with pytest.raises(GameError, match="path separators"):
            sanitize_filename("path/to/file")

        with pytest.raises(GameError, match="path separators"):
            sanitize_filename("path\\to\\file")

    def test_windows_reserved_names_rejected(self):
        """Test that Windows reserved names are rejected"""
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1']
        for name in reserved_names:
            with pytest.raises(GameError, match="reserved name"):
                sanitize_filename(name)
            with pytest.raises(GameError, match="reserved name"):
                sanitize_filename(name.lower())

    def test_invalid_characters_rejected(self):
        """Test that invalid characters are rejected"""
        with pytest.raises(GameError, match="invalid characters"):
            sanitize_filename("file<>name")

        with pytest.raises(GameError, match="invalid characters"):
            sanitize_filename("file:name")

        with pytest.raises(GameError, match="invalid characters"):
            sanitize_filename("file|name")

    def test_filename_too_long_rejected(self):
        """Test that overly long filenames are rejected"""
        long_name = "a" * 101
        with pytest.raises(GameError, match="too long"):
            sanitize_filename(long_name)


class TestSaveNameValidation:
    """Test save name validation functions"""

    def test_valid_save_names(self):
        """Test that valid save names are accepted"""
        assert validate_save_name("My Save Game") == "My Save Game"
        assert validate_save_name("Save-01") == "Save-01"
        assert validate_save_name("  trimmed  ") == "trimmed"

    def test_empty_save_name_rejected(self):
        """Test that empty save names are rejected"""
        with pytest.raises(GameError, match="cannot be empty"):
            validate_save_name("")

        with pytest.raises(GameError, match="cannot be empty"):
            validate_save_name("   ")

    def test_save_name_too_long_rejected(self):
        """Test that overly long save names are rejected"""
        long_name = "a" * 51
        with pytest.raises(GameError, match="too long"):
            validate_save_name(long_name)

    def test_special_characters_removed(self):
        """Test that special characters are sanitized"""
        result = validate_save_name("Save <script>alert('xss')</script>")
        assert "<" not in result
        assert ">" not in result
        assert "'" not in result


class TestSaveMetadata:
    """Test SaveMetadata dataclass"""

    def test_create_metadata(self):
        """Test creating save metadata"""
        meta = SaveMetadata(
            game_id="vault_shelter",
            game_name="Vault Shelter",
            save_name="Test Save",
            save_slot=1,
            timestamp="2024-01-01T00:00:00",
            play_time=3600,
            game_version="6.0"
        )

        assert meta.game_id == "vault_shelter"
        assert meta.save_slot == 1
        assert meta.play_time == 3600

    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary"""
        meta = SaveMetadata(
            game_id="test",
            game_name="Test Game",
            save_name="Save 1",
            save_slot=1,
            timestamp="2024-01-01T00:00:00",
            play_time=0,
            game_version="1.0"
        )

        d = meta.to_dict()
        assert d['game_id'] == "test"
        assert d['save_slot'] == 1

    def test_metadata_from_dict(self):
        """Test creating metadata from dictionary"""
        data = {
            'game_id': 'test',
            'game_name': 'Test Game',
            'save_name': 'Save 1',
            'save_slot': 1,
            'timestamp': '2024-01-01T00:00:00',
            'play_time': 100,
            'game_version': '1.0',
            'save_version': '1.0',
            'checksum': '',
            'auto_save': False
        }

        meta = SaveMetadata.from_dict(data)
        assert meta.game_id == "test"
        assert meta.play_time == 100


class TestSaveFile:
    """Test SaveFile dataclass"""

    def test_create_save_file(self):
        """Test creating a save file"""
        meta = SaveMetadata(
            game_id="test",
            game_name="Test",
            save_name="Save",
            save_slot=1,
            timestamp="2024-01-01T00:00:00",
            play_time=0,
            game_version="1.0"
        )

        save = SaveFile(
            metadata=meta,
            data={"resources": {"power": 100}}
        )

        assert save.metadata.game_id == "test"
        assert save.data["resources"]["power"] == 100

    def test_save_file_to_dict(self):
        """Test converting save file to dictionary"""
        meta = SaveMetadata(
            game_id="test",
            game_name="Test",
            save_name="Save",
            save_slot=1,
            timestamp="2024-01-01T00:00:00",
            play_time=0,
            game_version="1.0"
        )

        save = SaveFile(metadata=meta, data={"test": True})
        d = save.to_dict()

        assert "metadata" in d
        assert "data" in d
        assert d["data"]["test"] is True
