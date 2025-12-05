"""
Tests for constants module
===========================
"""

import pytest
from constants import (
    validate_stat,
    validate_happiness,
    validate_resource,
    get_difficulty_multiplier,
    STAT_MIN,
    STAT_MAX,
    HAPPINESS_MIN,
    HAPPINESS_MAX,
    DIFFICULTY_MULTIPLIERS
)


class TestStatValidation:
    """Test stat validation functions"""

    def test_validate_stat_within_range(self):
        """Test that valid stats pass through unchanged"""
        assert validate_stat(5) == 5
        assert validate_stat(1) == 1
        assert validate_stat(10) == 10

    def test_validate_stat_below_min(self):
        """Test that stats below minimum are clamped"""
        assert validate_stat(0) == STAT_MIN
        assert validate_stat(-5) == STAT_MIN

    def test_validate_stat_above_max(self):
        """Test that stats above maximum are clamped"""
        assert validate_stat(11) == STAT_MAX
        assert validate_stat(100) == STAT_MAX


class TestHappinessValidation:
    """Test happiness validation"""

    def test_validate_happiness_within_range(self):
        """Test valid happiness values"""
        assert validate_happiness(50.0) == 50.0
        assert validate_happiness(0.0) == 0.0
        assert validate_happiness(100.0) == 100.0

    def test_validate_happiness_below_min(self):
        """Test happiness below minimum"""
        assert validate_happiness(-10.0) == HAPPINESS_MIN

    def test_validate_happiness_above_max(self):
        """Test happiness above maximum"""
        assert validate_happiness(150.0) == HAPPINESS_MAX


class TestResourceValidation:
    """Test resource validation"""

    def test_validate_resource_within_range(self):
        """Test valid resource amounts"""
        assert validate_resource(500) == 500
        assert validate_resource(0) == 0

    def test_validate_resource_negative(self):
        """Test negative resources are clamped to 0"""
        assert validate_resource(-100) == 0

    def test_validate_resource_above_capacity(self):
        """Test resources above capacity are clamped"""
        assert validate_resource(2000, max_capacity=1000) == 1000


class TestDifficultyMultipliers:
    """Test difficulty system"""

    def test_all_difficulties_exist(self):
        """Test all difficulty levels are defined"""
        assert 'easy' in DIFFICULTY_MULTIPLIERS
        assert 'normal' in DIFFICULTY_MULTIPLIERS
        assert 'hard' in DIFFICULTY_MULTIPLIERS
        assert 'survival' in DIFFICULTY_MULTIPLIERS

    def test_get_difficulty_multiplier_valid(self):
        """Test getting valid difficulty multipliers"""
        assert get_difficulty_multiplier('easy', 'resource_production') == 1.5
        assert get_difficulty_multiplier('normal', 'resource_production') == 1.0
        assert get_difficulty_multiplier('hard', 'resource_production') == 0.8

    def test_get_difficulty_multiplier_invalid_difficulty(self):
        """Test invalid difficulty defaults to normal"""
        assert get_difficulty_multiplier('invalid', 'resource_production') == 1.0

    def test_get_difficulty_multiplier_invalid_stat(self):
        """Test invalid stat returns 1.0"""
        assert get_difficulty_multiplier('normal', 'invalid_stat') == 1.0

    def test_difficulty_balance(self):
        """Test that difficulty multipliers make sense"""
        # Easy should have bonuses
        assert get_difficulty_multiplier('easy', 'resource_production') > 1.0
        assert get_difficulty_multiplier('easy', 'enemy_damage') < 1.0

        # Hard should be challenging
        assert get_difficulty_multiplier('hard', 'resource_production') < 1.0
        assert get_difficulty_multiplier('hard', 'enemy_damage') > 1.0
