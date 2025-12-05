"""
Tests for game_utils module
============================
"""

import pytest
from game_utils import (
    roll_dice,
    chance,
    clamp,
    lerp,
    normalize,
    calculate_stat_bonus,
    calculate_level_xp,
    calculate_damage,
    format_duration,
    pluralize,
    abbreviate_number,
)


class TestRandomGeneration:
    """Test random number generation utilities"""

    def test_roll_dice_range(self):
        """Test dice rolls are in valid range"""
        for _ in range(100):
            result = roll_dice(6, 1)
            assert 1 <= result <= 6

        for _ in range(100):
            result = roll_dice(6, 2)
            assert 2 <= result <= 12

    def test_chance(self):
        """Test probability function"""
        # Test extremes
        assert chance(0.0) is False
        assert chance(1.0) is True

        # Test probability (statistically)
        true_count = sum(1 for _ in range(1000) if chance(0.5))
        assert 400 <= true_count <= 600  # Should be around 500


class TestMathUtilities:
    """Test math utility functions"""

    def test_clamp(self):
        """Test clamping values to range"""
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10

    def test_lerp(self):
        """Test linear interpolation"""
        assert lerp(0, 10, 0.0) == 0
        assert lerp(0, 10, 1.0) == 10
        assert lerp(0, 10, 0.5) == 5
        assert lerp(10, 20, 0.25) == 12.5

    def test_normalize(self):
        """Test normalization"""
        assert normalize(5, 0, 10) == 0.5
        assert normalize(0, 0, 10) == 0.0
        assert normalize(10, 0, 10) == 1.0
        assert normalize(25, 0, 100) == 0.25


class TestStatCalculations:
    """Test game stat calculations"""

    def test_stat_bonus(self):
        """Test SPECIAL stat bonus calculation"""
        # Stat of 1 should give 0.5x multiplier
        assert calculate_stat_bonus(1) == pytest.approx(0.5, rel=0.01)

        # Stat of 5 should give 1.0x multiplier
        assert calculate_stat_bonus(5) == pytest.approx(1.0, rel=0.01)

        # Stat of 10 should give 2.0x multiplier
        assert calculate_stat_bonus(10) == pytest.approx(2.0, rel=0.01)

    def test_level_xp(self):
        """Test XP calculation for levels"""
        xp_level_1 = calculate_level_xp(1)
        xp_level_2 = calculate_level_xp(2)
        xp_level_10 = calculate_level_xp(10)

        # XP should increase with level
        assert xp_level_2 > xp_level_1
        assert xp_level_10 > xp_level_2

        # Check specific value
        assert xp_level_1 == 100  # Base XP

    def test_damage_calculation(self):
        """Test combat damage calculation"""
        # Equal stats should give roughly base damage
        damage = calculate_damage(
            base_damage=10,
            attacker_stat=5,
            defender_stat=5,
            variance=0.0  # No variance for testing
        )
        assert damage == pytest.approx(10, abs=1)

        # Higher attacker stat should increase damage
        high_damage = calculate_damage(
            base_damage=10,
            attacker_stat=10,
            defender_stat=5,
            variance=0.0
        )
        assert high_damage > damage

        # Minimum damage is 1
        min_damage = calculate_damage(
            base_damage=1,
            attacker_stat=1,
            defender_stat=10,
            variance=0.0
        )
        assert min_damage >= 1


class TestTimeFormatting:
    """Test time formatting utilities"""

    def test_format_duration(self):
        """Test duration formatting"""
        assert format_duration(45) == "45s"
        assert format_duration(90) == "1m 30s"
        assert format_duration(120) == "2m"
        assert format_duration(3661) == "1h 1m"
        assert format_duration(86400) == "1d"
        assert format_duration(90000) == "1d 1h"

    def test_format_duration_edge_cases(self):
        """Test edge cases"""
        assert format_duration(0) == "0s"
        assert format_duration(59) == "59s"
        assert format_duration(60) == "1m"
        assert format_duration(3600) == "1h"


class TestTextUtilities:
    """Test text utility functions"""

    def test_pluralize(self):
        """Test pluralization"""
        assert pluralize(0, "dweller") == "0 dwellers"
        assert pluralize(1, "dweller") == "1 dweller"
        assert pluralize(2, "dweller") == "2 dwellers"
        assert pluralize(5, "dweller") == "5 dwellers"

        # Custom plural
        assert pluralize(1, "child", "children") == "1 child"
        assert pluralize(2, "child", "children") == "2 children"

    def test_abbreviate_number(self):
        """Test number abbreviation"""
        assert abbreviate_number(500) == "500"
        assert abbreviate_number(1500) == "1.5K"
        assert abbreviate_number(1_000_000) == "1.0M"
        assert abbreviate_number(2_500_000) == "2.5M"
        assert abbreviate_number(1_000_000_000) == "1.0B"


class TestListUtilities:
    """Test list utility functions"""

    def test_chunk_list(self):
        """Test chunking lists"""
        from game_utils import chunk_list

        items = [1, 2, 3, 4, 5, 6, 7]
        chunks = chunk_list(items, 3)

        assert len(chunks) == 3
        assert chunks[0] == [1, 2, 3]
        assert chunks[1] == [4, 5, 6]
        assert chunks[2] == [7]

    def test_find_by_id(self):
        """Test finding items by ID"""
        from game_utils import find_by_id

        items = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 3, 'name': 'Charlie'}
        ]

        assert find_by_id(items, 2)['name'] == 'Bob'
        assert find_by_id(items, 99) is None

    def test_group_by(self):
        """Test grouping items"""
        from game_utils import group_by

        items = [
            {'type': 'weapon', 'name': 'Sword'},
            {'type': 'weapon', 'name': 'Axe'},
            {'type': 'armor', 'name': 'Shield'}
        ]

        groups = group_by(items, 'type')

        assert len(groups) == 2
        assert len(groups['weapon']) == 2
        assert len(groups['armor']) == 1
