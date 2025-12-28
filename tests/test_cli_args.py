"""
Tests for cli_args module
==========================
"""

import pytest
import sys
from unittest.mock import patch


class TestGameArgs:
    """Test GameArgs dataclass"""

    def test_default_values(self):
        """Test default GameArgs values"""
        from cli_args import GameArgs
        args = GameArgs()
        assert args.demo is False
        assert args.quick is False
        assert args.no_color is False
        assert args.debug is False
        assert args.seed is None
        assert args.difficulty == "normal"
        assert args.save_file is None

    def test_custom_values(self):
        """Test GameArgs with custom values"""
        from cli_args import GameArgs
        args = GameArgs(
            demo=True,
            quick=True,
            seed=42,
            difficulty="hard"
        )
        assert args.demo is True
        assert args.quick is True
        assert args.seed == 42
        assert args.difficulty == "hard"


class TestArgumentParser:
    """Test argument parser creation"""

    def test_create_parser(self):
        """Test creating argument parser"""
        from cli_args import create_argument_parser

        parser = create_argument_parser(
            "Test Game",
            "A test game",
            "1.0"
        )

        assert parser is not None
        assert parser.prog == "test_game"

    def test_parse_demo_flag(self):
        """Test parsing --demo flag"""
        from cli_args import parse_game_args

        with patch.object(sys, 'argv', ['test', '--demo']):
            args = parse_game_args("Test", "Test game")
            assert args.demo is True

    def test_parse_quick_flag(self):
        """Test parsing --quick flag"""
        from cli_args import parse_game_args

        with patch.object(sys, 'argv', ['test', '--quick']):
            args = parse_game_args("Test", "Test game")
            assert args.quick is True

    def test_parse_seed(self):
        """Test parsing --seed argument"""
        from cli_args import parse_game_args

        with patch.object(sys, 'argv', ['test', '--seed', '42']):
            args = parse_game_args("Test", "Test game")
            assert args.seed == 42

    def test_parse_difficulty(self):
        """Test parsing --difficulty argument"""
        from cli_args import parse_game_args

        with patch.object(sys, 'argv', ['test', '--difficulty', 'hard']):
            args = parse_game_args("Test", "Test game")
            assert args.difficulty == "hard"

    def test_parse_no_color(self):
        """Test parsing --no-color flag"""
        from cli_args import parse_game_args
        import os

        with patch.object(sys, 'argv', ['test', '--no-color']):
            args = parse_game_args("Test", "Test game")
            assert args.no_color is True

    def test_parse_debug(self):
        """Test parsing --debug flag"""
        from cli_args import parse_game_args

        with patch.object(sys, 'argv', ['test', '--debug']):
            args = parse_game_args("Test", "Test game")
            assert args.debug is True

    def test_parse_combined_flags(self):
        """Test parsing multiple flags together"""
        from cli_args import parse_game_args

        with patch.object(sys, 'argv', ['test', '--demo', '--quick', '--debug', '--seed', '123']):
            args = parse_game_args("Test", "Test game")
            assert args.demo is True
            assert args.quick is True
            assert args.debug is True
            assert args.seed == 123


class TestGameRunner:
    """Test GameRunner class"""

    def test_runner_creation(self):
        """Test creating a GameRunner"""
        from cli_args import GameRunner

        runner = GameRunner("Test Game", "Description", "1.0")
        assert runner.game_name == "Test Game"
        assert runner.description == "Description"
        assert runner.version == "1.0"

    def test_main_decorator(self):
        """Test @runner.main decorator"""
        from cli_args import GameRunner

        runner = GameRunner("Test", "Test", "1.0")

        @runner.main
        def my_main(args):
            return "called"

        assert runner._main_func is my_main


class TestQuickParse:
    """Test quick_parse function"""

    def test_quick_parse(self):
        """Test quick_parse convenience function"""
        from cli_args import quick_parse

        with patch.object(sys, 'argv', ['my_game.py']):
            args = quick_parse()
            assert args is not None
            assert args.demo is False
