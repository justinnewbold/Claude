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
