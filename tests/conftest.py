"""
Pytest Configuration and Shared Fixtures
=========================================
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import game modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_stats():
    """Sample SPECIAL stats for testing"""
    return {
        "strength": 5,
        "perception": 6,
        "endurance": 7,
        "charisma": 4,
        "intelligence": 8,
        "agility": 5,
        "luck": 6
    }


@pytest.fixture
def mock_game_state():
    """Mock game state for testing"""
    return {
        "turn": 1,
        "resources": {
            "power": 100,
            "water": 100,
            "food": 100,
            "caps": 500
        },
        "dwellers": [],
        "rooms": []
    }


@pytest.fixture(autouse=True)
def disable_terminal_effects(monkeypatch):
    """Disable terminal color codes and effects during tests"""
    import os
    monkeypatch.setenv('NO_COLOR', '1')
    monkeypatch.setenv('TERM', 'dumb')
