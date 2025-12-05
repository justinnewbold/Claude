#!/usr/bin/env python3
"""
Tests for Localization System
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from localization import Localization, t, tp


@pytest.fixture
def temp_loc_dir():
    """Create temporary localization directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_localization_creation(temp_loc_dir):
    """Test creating localization instance"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)
    assert loc.current_language == 'en'
    assert 'en' in loc.translations


def test_get_translation(temp_loc_dir):
    """Test getting translations"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    assert loc.get('ui.yes') == 'Yes'
    assert loc.get('ui.no') == 'No'


def test_missing_translation_fallback(temp_loc_dir):
    """Test fallback for missing translations"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    # Missing key should return the key itself
    assert loc.get('missing.key') == 'missing.key'


def test_variable_substitution(temp_loc_dir):
    """Test variable substitution in translations"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    # Add custom translation with variable
    loc.translations['en']['greeting'] = 'Hello, {name}!'

    result = loc.get('greeting', name='Alice')
    assert result == 'Hello, Alice!'


def test_pluralization(temp_loc_dir):
    """Test pluralization"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    # Add plural translations
    loc.translations['en']['items'] = {
        'zero': 'No items',
        'one': '1 item',
        'other': '{count} items'
    }

    assert loc.get_plural('items', 0) == 'No items'
    assert loc.get_plural('items', 1) == '1 item'
    assert loc.get_plural('items', 5) == '5 items'


def test_language_switching(temp_loc_dir):
    """Test switching languages"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    # Add Spanish translations
    loc.translations['es'] = {
        'ui': {
            'yes': 'Sí',
            'no': 'No'
        }
    }

    loc.set_language('es')
    assert loc.current_language == 'es'
    assert loc.get('ui.yes') == 'Sí'


def test_fallback_to_english(temp_loc_dir):
    """Test fallback to English for missing translations"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    # Add Spanish with missing key
    loc.translations['es'] = {
        'ui': {
            'yes': 'Sí'
        }
    }

    loc.set_language('es')

    # Existing translation
    assert loc.get('ui.yes') == 'Sí'

    # Missing translation should fallback to English
    assert loc.get('ui.no') == 'No'


def test_get_all_keys(temp_loc_dir):
    """Test getting all translation keys"""
    loc = Localization('test_game', localization_dir=temp_loc_dir)

    keys = loc.get_all_keys('en')
    assert 'ui.yes' in keys
    assert 'ui.no' in keys
    assert 'msg.game_saved' in keys
