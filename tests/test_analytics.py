#!/usr/bin/env python3
"""
Tests for Analytics System
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import time

from analytics import Analytics, EventType


@pytest.fixture
def temp_analytics_dir():
    """Create temporary analytics directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_analytics_disabled_by_default(temp_analytics_dir):
    """Test analytics is disabled by default"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    assert not analytics.is_enabled()


def test_analytics_opt_in(temp_analytics_dir):
    """Test opting into analytics"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    analytics.enable()
    assert analytics.is_enabled()


def test_analytics_session(temp_analytics_dir):
    """Test analytics session tracking"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    analytics.enable()

    analytics.start_session('test_game', {'version': '1.0'})
    assert analytics.current_session is not None
    assert analytics.current_session.game_id == 'test_game'

    time.sleep(0.1)  # Small delay

    analytics.end_session()
    assert analytics.current_session is None


def test_analytics_event_tracking(temp_analytics_dir):
    """Test tracking events"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    analytics.enable()

    analytics.start_session('test_game')
    analytics.track_event(EventType.LEVEL_UP, {'level': 2})
    analytics.track_event(EventType.ACHIEVEMENT_UNLOCK, {'achievement': 'first_win'})

    assert len(analytics.current_session.events) == 2

    analytics.end_session()


def test_analytics_no_tracking_when_disabled(temp_analytics_dir):
    """Test that no tracking happens when disabled"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    # Leave disabled

    analytics.start_session('test_game')
    assert analytics.current_session is None


def test_analytics_statistics(temp_analytics_dir):
    """Test getting analytics statistics"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    analytics.enable()

    # Create and end a session
    analytics.start_session('test_game')
    time.sleep(0.1)
    analytics.end_session()

    stats = analytics.get_statistics()
    assert stats['total_sessions'] == 1
    assert stats['total_playtime'] > 0


def test_analytics_delete_data(temp_analytics_dir):
    """Test deleting all analytics data"""
    analytics = Analytics(analytics_dir=temp_analytics_dir)
    analytics.enable()

    analytics.start_session('test_game')
    analytics.end_session()

    analytics.delete_all_data()

    stats = analytics.get_statistics()
    assert stats['total_sessions'] == 0
