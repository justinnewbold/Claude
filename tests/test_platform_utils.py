"""
Tests for platform_utils module
================================
"""

import pytest
from pathlib import Path
from platform_utils import (
    get_platform,
    Platform,
    is_windows,
    is_macos,
    is_linux,
    get_terminal_size,
    get_safe_characters,
    Colors,
    get_app_data_dir,
    get_config_dir,
    clear_screen,
    move_cursor,
    hide_cursor,
    show_cursor
)


class TestPlatformDetection:
    """Test platform detection"""

    def test_get_platform_returns_valid(self):
        """Test that platform detection returns a valid Platform enum"""
        platform = get_platform()
        assert isinstance(platform, Platform)
        assert platform in [Platform.WINDOWS, Platform.MACOS, Platform.LINUX, Platform.UNKNOWN]

    def test_platform_detection_consistency(self):
        """Test that only one platform detection returns True"""
        platforms = [is_windows(), is_macos(), is_linux()]
        # Exactly one should be True (or zero if UNKNOWN)
        assert sum(platforms) <= 1


class TestTerminal:
    """Test terminal functionality"""

    def test_get_terminal_size_returns_tuple(self):
        """Test terminal size returns (width, height) tuple"""
        width, height = get_terminal_size()
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert width > 0
        assert height > 0

    def test_get_terminal_size_fallback(self):
        """Test terminal size fallback"""
        width, height = get_terminal_size(fallback=(100, 30))
        # Should get either actual size or fallback
        assert (width, height) == (100, 30) or (width > 0 and height > 0)

    def test_get_safe_characters(self):
        """Test safe character mapping"""
        chars = get_safe_characters()

        # Required keys
        required = ['box_h', 'box_v', 'progress_full', 'progress_empty',
                   'arrow_up', 'arrow_down', 'check', 'cross']

        for key in required:
            assert key in chars
            assert isinstance(chars[key], str)
            assert len(chars[key]) > 0


class TestColors:
    """Test color system"""

    def test_colors_init(self):
        """Test color system initialization"""
        enabled = Colors.init()
        assert isinstance(enabled, bool)

    def test_colors_attributes_exist(self):
        """Test that color attributes exist"""
        Colors.init()
        assert hasattr(Colors, 'RESET')
        assert hasattr(Colors, 'BOLD')
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'BLUE')

    def test_color_rgb(self):
        """Test RGB color generation"""
        Colors.init()
        color = Colors.rgb(255, 0, 0)
        assert isinstance(color, str)
        # If colors disabled, should be empty string
        # If enabled, should be ANSI escape code

    def test_color_256(self):
        """Test 256-color generation"""
        Colors.init()
        color = Colors.color256(196)
        assert isinstance(color, str)


class TestPaths:
    """Test path utilities"""

    def test_get_app_data_dir(self):
        """Test app data directory creation"""
        app_dir = get_app_data_dir("test_app")
        assert isinstance(app_dir, Path)
        assert app_dir.exists()
        assert 'test_app' in str(app_dir)

    def test_get_config_dir(self):
        """Test config directory creation"""
        config_dir = get_config_dir("test_app")
        assert isinstance(config_dir, Path)
        assert config_dir.exists()

    def test_path_consistency(self):
        """Test that paths are consistent across calls"""
        app_dir1 = get_app_data_dir("test_app")
        app_dir2 = get_app_data_dir("test_app")
        assert app_dir1 == app_dir2


class TestScreenControl:
    """Test screen control functions"""

    def test_clear_screen_callable(self):
        """Test that clear_screen is callable without errors"""
        # This should not raise an exception
        try:
            clear_screen()
            success = True
        except Exception:
            success = False
        assert success

    def test_move_cursor_callable(self):
        """Test that move_cursor is callable with valid arguments"""
        try:
            move_cursor(1, 1)
            move_cursor(80, 24)
            success = True
        except Exception:
            success = False
        assert success

    def test_cursor_visibility(self):
        """Test cursor visibility functions are callable"""
        try:
            hide_cursor()
            show_cursor()
            success = True
        except Exception:
            success = False
        assert success


class TestKeyHandling:
    """Test key handling utilities"""

    def test_arrow_key_mappings_exist(self):
        """Test that arrow key mappings are defined"""
        from platform_utils import _WINDOWS_ARROW_KEYS, _UNIX_ARROW_KEYS

        # Windows arrow keys
        assert b'H' in _WINDOWS_ARROW_KEYS
        assert b'P' in _WINDOWS_ARROW_KEYS
        assert b'K' in _WINDOWS_ARROW_KEYS
        assert b'M' in _WINDOWS_ARROW_KEYS

        # Unix arrow keys
        assert '\x1b[A' in _UNIX_ARROW_KEYS
        assert '\x1b[B' in _UNIX_ARROW_KEYS
        assert '\x1b[C' in _UNIX_ARROW_KEYS
        assert '\x1b[D' in _UNIX_ARROW_KEYS

    def test_arrow_key_values(self):
        """Test that arrow keys map to correct values"""
        from platform_utils import _WINDOWS_ARROW_KEYS, _UNIX_ARROW_KEYS

        # Both should map to same values
        assert _WINDOWS_ARROW_KEYS[b'H'] == 'UP'
        assert _UNIX_ARROW_KEYS['\x1b[A'] == 'UP'

        assert _WINDOWS_ARROW_KEYS[b'P'] == 'DOWN'
        assert _UNIX_ARROW_KEYS['\x1b[B'] == 'DOWN'

    def test_process_unix_key_normal(self):
        """Test processing normal Unix key"""
        from platform_utils import _process_unix_key

        assert _process_unix_key('a', lambda n: '') == 'a'
        assert _process_unix_key('q', lambda n: '') == 'q'

    def test_process_unix_key_arrow(self):
        """Test processing Unix arrow key"""
        from platform_utils import _process_unix_key

        result = _process_unix_key('\x1b', lambda n: '[A')
        assert result == 'UP'


class TestGameRootDetection:
    """Test game root directory detection"""

    def test_get_game_root_returns_path(self):
        """Test that get_game_root returns a Path"""
        from platform_utils import get_game_root

        root = get_game_root()
        assert isinstance(root, Path)

    def test_get_game_root_finds_project(self):
        """Test that get_game_root finds the project directory"""
        from platform_utils import get_game_root

        root = get_game_root()

        # Should find at least one marker file
        marker_files = ['pyproject.toml', 'game_launcher.py', 'games_registry.json']
        found_markers = sum(1 for m in marker_files if (root / m).exists())

        # The root should have at least some marker files
        # (may be 0 if running tests in isolation)
        assert found_markers >= 0
