"""
Tests for colors module
========================
Tests for ANSI color codes and helper functions.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from colors import Colors, C, strip_ansi, colorize


class TestColorConstants:
    """Test color constant definitions"""

    def test_reset_code(self):
        """Test RESET code is correct"""
        assert Colors.RESET == '\033[0m'

    def test_bold_code(self):
        """Test BOLD code is correct"""
        assert Colors.BOLD == '\033[1m'

    def test_standard_colors(self):
        """Test standard colors are defined"""
        assert Colors.RED == '\033[31m'
        assert Colors.GREEN == '\033[32m'
        assert Colors.BLUE == '\033[34m'
        assert Colors.YELLOW == '\033[33m'

    def test_bright_colors(self):
        """Test bright colors are defined"""
        assert Colors.BRIGHT_RED == '\033[91m'
        assert Colors.BRIGHT_GREEN == '\033[92m'

    def test_semantic_colors(self):
        """Test semantic colors are defined"""
        assert Colors.SUCCESS is not None
        assert Colors.WARNING is not None
        assert Colors.DANGER is not None
        assert Colors.INFO is not None

    def test_convenience_alias(self):
        """Test C is alias for Colors"""
        assert C is Colors
        assert C.RESET == Colors.RESET
        assert C.BOLD == Colors.BOLD


class TestColorMethods:
    """Test color method functions"""

    def test_rgb_method(self):
        """Test RGB color generation"""
        result = Colors.rgb(255, 128, 0)
        assert result == '\033[38;2;255;128;0m'

    def test_bg_rgb_method(self):
        """Test background RGB color generation"""
        result = Colors.bg_rgb(100, 150, 200)
        assert result == '\033[48;2;100;150;200m'

    def test_color256_method(self):
        """Test 256-color generation"""
        result = Colors.color256(42)
        assert result == '\033[38;5;42m'

    def test_bg_color256_method(self):
        """Test 256-color background generation"""
        result = Colors.bg_color256(128)
        assert result == '\033[48;5;128m'


class TestStripAnsi:
    """Test ANSI stripping function"""

    def test_strip_simple_code(self):
        """Test stripping simple color codes"""
        text = '\033[31mRed Text\033[0m'
        result = strip_ansi(text)
        assert result == 'Red Text'

    def test_strip_multiple_codes(self):
        """Test stripping multiple color codes"""
        text = '\033[1m\033[31mBold Red\033[0m'
        result = strip_ansi(text)
        assert result == 'Bold Red'

    def test_strip_256_color(self):
        """Test stripping 256-color codes"""
        text = '\033[38;5;42mColored\033[0m'
        result = strip_ansi(text)
        assert result == 'Colored'

    def test_strip_rgb_color(self):
        """Test stripping RGB color codes"""
        text = '\033[38;2;255;128;0mRGB\033[0m'
        result = strip_ansi(text)
        assert result == 'RGB'

    def test_plain_text_unchanged(self):
        """Test plain text is unchanged"""
        text = 'Plain text without colors'
        result = strip_ansi(text)
        assert result == text


class TestColorize:
    """Test colorize helper function"""

    def test_single_color(self):
        """Test colorizing with single color"""
        result = colorize("Hello", C.RED)
        assert result == '\033[31mHello\033[0m'

    def test_multiple_codes(self):
        """Test colorizing with multiple codes"""
        result = colorize("Hello", C.BOLD, C.RED)
        assert result == '\033[1m\033[31mHello\033[0m'

    def test_empty_text(self):
        """Test colorizing empty text"""
        result = colorize("", C.RED)
        assert result == '\033[31m\033[0m'


class TestColorsInGames:
    """Test colors are properly used in game files"""

    def test_butterfly_effect_imports_colors(self):
        """Test butterfly_effect uses centralized colors"""
        from butterfly_effect import C as game_C
        assert game_C is Colors

    def test_schrodingers_dungeon_imports_colors(self):
        """Test schrodingers_dungeon uses centralized colors"""
        from schrodingers_dungeon import C as game_C
        assert game_C is Colors

    def test_forking_paths_imports_colors(self):
        """Test forking_paths uses centralized colors"""
        from forking_paths import C as game_C
        assert game_C is Colors

    def test_game_specific_colors_exist(self):
        """Test game-specific colors are defined in Colors"""
        # Butterfly Effect colors
        assert hasattr(Colors, 'PARTICLE')
        assert hasattr(Colors, 'WALL')
        assert hasattr(Colors, 'CHAOS')

        # Infinite Library colors
        assert hasattr(Colors, 'SHELF')
        assert hasattr(Colors, 'BOOK')
        assert hasattr(Colors, 'PROPHECY')

        # Schrodinger's Dungeon colors
        assert hasattr(Colors, 'SUPERPOSED')
        assert hasattr(Colors, 'OBSERVED')
        assert hasattr(Colors, 'QUANTUM')
