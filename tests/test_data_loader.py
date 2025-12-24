"""
Tests for data_loader module
=============================
Tests for data loading and validation.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_loader import (
    validate_weapon,
    validate_outfit,
    validate_room,
    validate_skill,
    validate_equipment_data,
    validate_rooms_data,
    validate_skills_data,
    DataLoader,
    DataLoadError,
    DataValidationError,
)


class TestWeaponValidation:
    """Test weapon validation"""

    def test_valid_weapon(self):
        """Test that valid weapons pass validation"""
        weapon = {
            'id': 'test_weapon',
            'name': 'Test Weapon',
            'type': 'weapon',
            'damage': 10,
            'rarity': 'common',
            'cost': 100
        }
        errors = validate_weapon('test_weapon', weapon)
        assert len(errors) == 0

    def test_missing_required_fields(self):
        """Test that missing required fields are detected"""
        weapon = {'id': 'test', 'name': 'Test'}
        errors = validate_weapon('test', weapon)
        assert len(errors) > 0
        assert any('type' in e for e in errors)
        assert any('damage' in e for e in errors)

    def test_invalid_damage(self):
        """Test that negative damage is rejected"""
        weapon = {
            'id': 'test',
            'name': 'Test',
            'type': 'weapon',
            'damage': -5,
            'rarity': 'common',
            'cost': 100
        }
        errors = validate_weapon('test', weapon)
        assert any('non-negative' in e for e in errors)

    def test_invalid_rarity(self):
        """Test that invalid rarity is rejected"""
        weapon = {
            'id': 'test',
            'name': 'Test',
            'type': 'weapon',
            'damage': 10,
            'rarity': 'super_rare',  # Invalid
            'cost': 100
        }
        errors = validate_weapon('test', weapon)
        assert any('rarity' in e for e in errors)


class TestOutfitValidation:
    """Test outfit validation"""

    def test_valid_outfit(self):
        """Test that valid outfits pass validation"""
        outfit = {
            'id': 'test_outfit',
            'name': 'Test Outfit',
            'type': 'outfit',
            'defense': 5,
            'rarity': 'uncommon',
            'cost': 200
        }
        errors = validate_outfit('test_outfit', outfit)
        assert len(errors) == 0

    def test_missing_defense(self):
        """Test that missing defense is detected"""
        outfit = {
            'id': 'test',
            'name': 'Test',
            'type': 'outfit',
            'rarity': 'common',
            'cost': 100
        }
        errors = validate_outfit('test', outfit)
        assert any('defense' in e for e in errors)


class TestRoomValidation:
    """Test room validation"""

    def test_valid_room(self):
        """Test that valid rooms pass validation"""
        room = {
            'id': 'POWER_GENERATOR',
            'name': 'Power Generator',
            'description': 'Generates power',
            'cost': 150,
            'capacity': 2
        }
        errors = validate_room('POWER_GENERATOR', room)
        assert len(errors) == 0

    def test_missing_required_fields(self):
        """Test that missing fields are detected"""
        room = {'id': 'test', 'name': 'Test'}
        errors = validate_room('test', room)
        assert len(errors) > 0
        assert any('description' in e for e in errors)
        assert any('cost' in e for e in errors)


class TestSkillValidation:
    """Test skill validation"""

    def test_valid_skill(self):
        """Test that valid skills pass validation"""
        skill = {
            'id': 'power_expert',
            'name': 'Power Expert',
            'description': 'Master of electrical systems',
            'category': 'production',
            'bonus_type': 'production_power',
            'bonus_value': 0.3,
            'cost': 500
        }
        errors = validate_skill('power_expert', skill)
        assert len(errors) == 0

    def test_invalid_category(self):
        """Test that invalid category is rejected"""
        skill = {
            'id': 'test',
            'name': 'Test',
            'description': 'Test skill',
            'category': 'invalid_category',
            'bonus_type': 'test',
            'bonus_value': 0.1,
            'cost': 100
        }
        errors = validate_skill('test', skill)
        assert any('category' in e for e in errors)


class TestEquipmentDataValidation:
    """Test equipment.json validation"""

    def test_valid_equipment_data(self):
        """Test that valid equipment data passes"""
        data = {
            'weapons': {
                'sword': {
                    'id': 'sword',
                    'name': 'Sword',
                    'type': 'weapon',
                    'damage': 10,
                    'rarity': 'common',
                    'cost': 100
                }
            },
            'outfits': {
                'armor': {
                    'id': 'armor',
                    'name': 'Armor',
                    'type': 'outfit',
                    'defense': 5,
                    'rarity': 'common',
                    'cost': 100
                }
            }
        }
        errors = validate_equipment_data(data)
        assert len(errors) == 0

    def test_missing_sections(self):
        """Test that missing sections are detected"""
        data = {}
        errors = validate_equipment_data(data)
        assert any('weapons' in e for e in errors)
        assert any('outfits' in e for e in errors)


class TestRoomsDataValidation:
    """Test rooms.json validation"""

    def test_valid_rooms_data(self):
        """Test that valid rooms data passes"""
        data = {
            'rooms': {
                'POWER_GENERATOR': {
                    'id': 'POWER_GENERATOR',
                    'name': 'Power Generator',
                    'description': 'Generates power',
                    'cost': 150,
                    'capacity': 2
                }
            }
        }
        errors = validate_rooms_data(data)
        assert len(errors) == 0

    def test_missing_rooms_section(self):
        """Test that missing rooms section is detected"""
        data = {}
        errors = validate_rooms_data(data)
        assert any('rooms' in e for e in errors)


class TestSkillsDataValidation:
    """Test skills.json validation"""

    def test_valid_skills_data(self):
        """Test that valid skills data passes"""
        data = {
            'skills': {
                'power_expert': {
                    'id': 'power_expert',
                    'name': 'Power Expert',
                    'description': 'Master of power',
                    'category': 'production',
                    'bonus_type': 'power',
                    'bonus_value': 0.3,
                    'cost': 500
                }
            }
        }
        errors = validate_skills_data(data)
        assert len(errors) == 0


class TestDataLoader:
    """Test DataLoader class"""

    def test_loader_initialization(self):
        """Test that loader initializes correctly"""
        loader = DataLoader(validate=False)
        assert loader._validate is False

    def test_cache_clearing(self):
        """Test that cache can be cleared"""
        loader = DataLoader(validate=False)
        loader._cache['test'] = {'data': 'test'}
        loader.clear_cache()
        assert len(loader._cache) == 0
