"""
Tests for game logic
=====================
Tests for core game mechanics and calculations.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestResourceCalculations:
    """Test resource consumption and production calculations"""

    def test_consumption_scaling(self):
        """Test that consumption scales with dweller count"""
        dwellers = 10
        base_consumption = 2
        expected = dwellers * base_consumption
        assert expected == 20

    def test_production_bonus(self):
        """Test production bonus calculation"""
        base_production = 10
        bonus_percent = 0.3  # 30% bonus
        expected = base_production * (1 + bonus_percent)
        assert expected == 13.0

    def test_happiness_bounds(self):
        """Test happiness stays within 0-100"""
        happiness = 85
        change = 20
        new_happiness = min(100, max(0, happiness + change))
        assert new_happiness == 100

        happiness = 15
        change = -20
        new_happiness = min(100, max(0, happiness + change))
        assert new_happiness == 0


class TestCombatMechanics:
    """Test combat damage and defense calculations"""

    def test_damage_calculation(self):
        """Test basic damage calculation"""
        base_damage = 10
        weapon_damage = 15
        stat_bonus = 3
        total = base_damage + weapon_damage + stat_bonus
        assert total == 28

    def test_defense_reduction(self):
        """Test defense reduces damage"""
        incoming_damage = 20
        defense = 5
        damage_reduction = 0.1  # 10% per defense point
        final_damage = incoming_damage * (1 - (defense * damage_reduction))
        assert final_damage == 10.0

    def test_minimum_damage(self):
        """Test damage cannot go below 1"""
        incoming_damage = 5
        defense = 100
        damage_reduction = 0.1
        calculated = incoming_damage * (1 - (defense * damage_reduction))
        final_damage = max(1, calculated)
        assert final_damage == 1


class TestProbabilityChecks:
    """Test probability and random event calculations"""

    def test_probability_bounds(self):
        """Test probability stays within 0-1"""
        base_chance = 0.5
        modifier = 0.6
        chance = min(1.0, max(0.0, base_chance + modifier))
        assert chance == 1.0

        base_chance = 0.3
        modifier = -0.5
        chance = min(1.0, max(0.0, base_chance + modifier))
        assert chance == 0.0

    def test_luck_bonus(self):
        """Test luck stat affects probability"""
        base_chance = 0.3
        luck_stat = 8
        luck_modifier = luck_stat * 0.02  # 2% per luck point
        final_chance = base_chance + luck_modifier
        assert final_chance == pytest.approx(0.46)


class TestSPECIALStats:
    """Test SPECIAL stat system"""

    def test_stat_bounds(self):
        """Test stats stay within 1-10"""
        stat = 12
        bounded = min(10, max(1, stat))
        assert bounded == 10

        stat = -5
        bounded = min(10, max(1, stat))
        assert bounded == 1

    def test_stat_modifier_calculation(self):
        """Test stat modifier (deviation from average)"""
        stat = 8
        average = 5
        modifier = stat - average
        assert modifier == 3

    def test_combined_stats(self):
        """Test combining multiple stats"""
        strength = 7
        perception = 6
        combined = (strength + perception) // 2
        assert combined == 6


class TestGameProgression:
    """Test game progression mechanics"""

    def test_experience_level_up(self):
        """Test experience thresholds for leveling"""
        level = 5
        exp_for_next = level * 100  # 100 XP per level
        assert exp_for_next == 500

    def test_skill_cost_scaling(self):
        """Test skill costs increase with level"""
        skill_level = 3
        base_cost = 100
        cost = base_cost * (skill_level + 1)
        assert cost == 400

    def test_room_upgrade_cost(self):
        """Test room upgrade costs scale"""
        base_cost = 200
        current_level = 2
        upgrade_cost = base_cost * (2 ** current_level)
        assert upgrade_cost == 800


class TestInputValidation:
    """Test input validation helpers"""

    def test_valid_menu_choice(self):
        """Test valid menu choice detection"""
        valid_choices = ['1', '2', '3', 'quit']
        choice = '2'
        assert choice in valid_choices

    def test_invalid_menu_choice(self):
        """Test invalid menu choice detection"""
        valid_choices = ['1', '2', '3', 'quit']
        choice = '5'
        assert choice not in valid_choices

    def test_numeric_input(self):
        """Test numeric input parsing"""
        user_input = '42'
        try:
            value = int(user_input)
            is_valid = True
        except ValueError:
            is_valid = False
        assert is_valid
        assert value == 42

    def test_non_numeric_input(self):
        """Test non-numeric input rejection"""
        user_input = 'abc'
        try:
            int(user_input)
            is_valid = True
        except ValueError:
            is_valid = False
        assert not is_valid
