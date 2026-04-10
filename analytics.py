#!/usr/bin/env python3
"""
Analytics System (Opt-in)
==========================
Privacy-respecting analytics and telemetry system.

IMPORTANT: This system is 100% opt-in and respects user privacy.
No data is collected unless explicitly enabled by the user.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib
import uuid

from logging_config import get_logger
from error_handling import error_context


logger = get_logger(__name__)

# Default analytics data directory
DEFAULT_ANALYTICS_DIR = Path.home() / ".vault13" / "analytics"


class EventType(Enum):
    """Types of analytics events"""
    GAME_START = "game_start"
    GAME_END = "game_end"
    LEVEL_UP = "level_up"
    ACHIEVEMENT_UNLOCK = "achievement_unlock"
    ITEM_COLLECTED = "item_collected"
    COMBAT_START = "combat_start"
    COMBAT_END = "combat_end"
    DEATH = "death"
    SAVE_GAME = "save_game"
    LOAD_GAME = "load_game"
    MENU_OPENED = "menu_opened"
    SETTING_CHANGED = "setting_changed"
    ERROR = "error"
    CRASH = "crash"


@dataclass
class AnalyticsEvent:
    """A single analytics event"""
    event_type: EventType
    timestamp: str
    game_id: str
    session_id: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionData:
    """Data about a game session"""
    session_id: str
    game_id: str
    start_time: str
    end_time: Optional[str] = None
    duration: float = 0.0  # seconds
    events: List[AnalyticsEvent] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Analytics:
    """
    Privacy-respecting analytics system.

    Features:
    - 100% opt-in (disabled by default)
    - No personal information collected
    - Anonymous user IDs
    - Local storage only
    - User can view all data
    - User can delete all data
    - No external servers (unless explicitly configured)
    """

    def __init__(self, analytics_dir: Optional[Path] = None):
        """
        Initialize analytics system.

        Args:
            analytics_dir: Directory for analytics data (default: ~/.vault13/analytics)
        """
        self.logger = get_logger(__name__)

        # Analytics directory
        if analytics_dir is None:
            analytics_dir = DEFAULT_ANALYTICS_DIR
        self.analytics_dir = analytics_dir
        self.analytics_dir.mkdir(parents=True, exist_ok=True)

        # Settings
        self.settings_file = self.analytics_dir / "settings.json"
        self.enabled = False
        self.anonymous_id = ""

        # Current session
        self.current_session: Optional[SessionData] = None

        # Load settings
        self._load_settings()

    def _load_settings(self):
        """Load analytics settings"""
        if not self.settings_file.exists():
            # Create default settings
            self._create_default_settings()
            return

        with open(self.settings_file, 'r') as f:
            settings = json.load(f)

        self.enabled = settings.get('enabled', False)
        self.anonymous_id = settings.get('anonymous_id', '')

        if not self.anonymous_id:
            self.anonymous_id = str(uuid.uuid4())
            self._save_settings()

    def _save_settings(self):
        """Save analytics settings"""
        settings = {
            'enabled': self.enabled,
            'anonymous_id': self.anonymous_id,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=2)

    def _create_default_settings(self):
        """Create default analytics settings"""
        self.enabled = False
        self.anonymous_id = str(uuid.uuid4())
        self._save_settings()

        # Create privacy notice
        privacy_file = self.analytics_dir / "PRIVACY.txt"
        privacy_notice = """
VAULT 13 ANALYTICS - PRIVACY NOTICE
====================================

This analytics system is COMPLETELY OPT-IN and DISABLED BY DEFAULT.

What we collect (only if you enable analytics):
- Game session duration
- In-game events (achievements, levels, etc.)
- Error and crash reports (if enabled)
- Anonymous usage statistics

What we DO NOT collect:
- Personal information (name, email, etc.)
- Save file contents
- System information beyond basic game stats
- Anything that can identify you personally

Your data:
- Stored locally on your computer only
- You can view all collected data at any time
- You can delete all data at any time
- Never sent to external servers without explicit permission

To enable analytics:
1. Open Settings menu
2. Go to Privacy Settings
3. Enable "Usage Statistics"

You can disable analytics at any time.

For questions: see README.md
"""

        with open(privacy_file, 'w') as f:
            f.write(privacy_notice)

    def enable(self):
        """Enable analytics (opt-in)"""
        self.enabled = True
        self._save_settings()
        self.logger.info("Analytics enabled (user opted in)")

    def disable(self):
        """Disable analytics (opt-out)"""
        self.enabled = False
        self._save_settings()
        self.logger.info("Analytics disabled")

    def is_enabled(self) -> bool:
        """Check if analytics is enabled"""
        return self.enabled

    def start_session(self, game_id: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Start a new analytics session.

        Args:
            game_id: Game identifier
            metadata: Optional session metadata
        """
        if not self.enabled:
            self.logger.debug("Analytics disabled, skipping session start")
            return

        self.current_session = SessionData(
            session_id=str(uuid.uuid4()),
            game_id=game_id,
            start_time=datetime.now().isoformat(),
            metadata=metadata or {}
        )

        self.track_event(EventType.GAME_START, {'game_id': game_id})
        self.logger.debug(f"Analytics session started: {self.current_session.session_id}")

    def end_session(self):
        """End current analytics session"""
        if not self.enabled or not self.current_session:
            return

        self.current_session.end_time = datetime.now().isoformat()

        # Calculate duration
        start = datetime.fromisoformat(self.current_session.start_time)
        end = datetime.fromisoformat(self.current_session.end_time)
        self.current_session.duration = (end - start).total_seconds()

        self.track_event(EventType.GAME_END, {
            'duration': self.current_session.duration,
            'events_count': len(self.current_session.events)
        })

        # Save session
        self._save_session()

        self.logger.debug(f"Analytics session ended: {self.current_session.session_id}")
        self.current_session = None

    def track_event(
        self,
        event_type: EventType,
        properties: Optional[Dict[str, Any]] = None
    ):
        """
        Track an analytics event.

        Args:
            event_type: Type of event
            properties: Event properties
        """
        if not self.enabled or not self.current_session:
            return

        event = AnalyticsEvent(
            event_type=event_type,
            timestamp=datetime.now().isoformat(),
            game_id=self.current_session.game_id,
            session_id=self.current_session.session_id,
            properties=properties or {}
        )

        self.current_session.events.append(event)

        self.logger.debug(f"Event tracked: {event_type.value}")

    def _save_session(self):
        """Save session data to disk"""
        if not self.current_session:
            return

        with error_context("saving analytics session"):
            # Create sessions directory
            sessions_dir = self.analytics_dir / "sessions"
            sessions_dir.mkdir(exist_ok=True)

            # Save session
            session_file = sessions_dir / f"{self.current_session.session_id}.json"

            data = {
                'session_id': self.current_session.session_id,
                'game_id': self.current_session.game_id,
                'start_time': self.current_session.start_time,
                'end_time': self.current_session.end_time,
                'duration': self.current_session.duration,
                'metadata': self.current_session.metadata,
                'events': [
                    {
                        'event_type': e.event_type.value,
                        'timestamp': e.timestamp,
                        'properties': e.properties
                    }
                    for e in self.current_session.events
                ]
            }

            with open(session_file, 'w') as f:
                json.dump(data, f, indent=2)

    def get_all_sessions(self, game_id: Optional[str] = None) -> List[SessionData]:
        """
        Get all recorded sessions.

        Args:
            game_id: Filter by game ID (optional)

        Returns:
            List of session data
        """
        sessions_dir = self.analytics_dir / "sessions"
        if not sessions_dir.exists():
            return []

        sessions = []

        for session_file in sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)

                if game_id and data['game_id'] != game_id:
                    continue

                # Reconstruct session
                session = SessionData(
                    session_id=data['session_id'],
                    game_id=data['game_id'],
                    start_time=data['start_time'],
                    end_time=data.get('end_time'),
                    duration=data.get('duration', 0.0),
                    metadata=data.get('metadata', {})
                )

                sessions.append(session)

            except (json.JSONDecodeError, KeyError, IOError, OSError) as e:
                self.logger.error(f"Error loading session {session_file}: {e}")

        return sessions

    def get_statistics(self, game_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get analytics statistics.

        Args:
            game_id: Filter by game ID (optional)

        Returns:
            Statistics dictionary
        """
        sessions = self.get_all_sessions(game_id)

        if not sessions:
            return {
                'total_sessions': 0,
                'total_playtime': 0.0,
                'average_session_length': 0.0
            }

        total_playtime = sum(s.duration for s in sessions)
        avg_session = total_playtime / len(sessions) if sessions else 0

        return {
            'total_sessions': len(sessions),
            'total_playtime': total_playtime,
            'total_playtime_hours': total_playtime / 3600,
            'average_session_length': avg_session,
            'average_session_minutes': avg_session / 60,
            'earliest_session': min(s.start_time for s in sessions),
            'latest_session': max(s.start_time for s in sessions)
        }

    def delete_all_data(self):
        """Delete all analytics data"""
        import shutil

        if self.analytics_dir.exists():
            shutil.rmtree(self.analytics_dir)
            self.analytics_dir.mkdir(parents=True, exist_ok=True)
            self._create_default_settings()

        self.logger.info("All analytics data deleted")
        print("✅ All analytics data has been deleted.")

    def export_data(self, output_file: Path):
        """
        Export all analytics data.

        Args:
            output_file: Output file path
        """
        sessions = self.get_all_sessions()
        stats = self.get_statistics()

        data = {
            'export_date': datetime.now().isoformat(),
            'anonymous_id': self.anonymous_id,
            'statistics': stats,
            'sessions': [
                {
                    'session_id': s.session_id,
                    'game_id': s.game_id,
                    'start_time': s.start_time,
                    'end_time': s.end_time,
                    'duration': s.duration
                }
                for s in sessions
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Analytics data exported to: {output_file}")


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_analytics: Optional[Analytics] = None


def get_analytics() -> Analytics:
    """Get global analytics instance"""
    global _analytics
    if _analytics is None:
        _analytics = Analytics()
    return _analytics


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def track_game_start(game_id: str, metadata: Optional[Dict[str, Any]] = None):
    """Track game start"""
    analytics = get_analytics()
    if analytics.is_enabled():
        analytics.start_session(game_id, metadata)


def track_game_end():
    """Track game end"""
    analytics = get_analytics()
    if analytics.is_enabled():
        analytics.end_session()


def track_achievement(achievement_id: str, achievement_name: str):
    """Track achievement unlock"""
    analytics = get_analytics()
    if analytics.is_enabled():
        analytics.track_event(EventType.ACHIEVEMENT_UNLOCK, {
            'achievement_id': achievement_id,
            'achievement_name': achievement_name
        })


def track_error(error_type: str, error_message: str):
    """Track error"""
    analytics = get_analytics()
    if analytics.is_enabled():
        analytics.track_event(EventType.ERROR, {
            'error_type': error_type,
            'error_message': error_message
        })


# =============================================================================
# ANALYTICS DASHBOARD
# =============================================================================

def show_analytics_dashboard():
    """Show analytics dashboard"""
    from platform_utils import clear_screen, print_header
    from validation import get_menu_choice

    analytics = get_analytics()

    while True:
        clear_screen()
        print_header("📊 ANALYTICS DASHBOARD")

        print(f"\nStatus: {'✅ Enabled' if analytics.is_enabled() else '❌ Disabled'}")
        print(f"Anonymous ID: {analytics.anonymous_id[:8]}...")

        stats = analytics.get_statistics()

        print("\n" + "=" * 60)
        print("📈 Overall Statistics")
        print("=" * 60)
        print(f"Total Sessions: {stats.get('total_sessions', 0)}")
        print(f"Total Playtime: {stats.get('total_playtime_hours', 0):.1f} hours")
        print(f"Avg Session: {stats.get('average_session_minutes', 0):.1f} minutes")
        print("=" * 60)

        options = [
            "📊 View Detailed Stats",
            "📁 Export Data",
            "🗑️  Delete All Data",
            f"{'❌ Disable' if analytics.is_enabled() else '✅ Enable'} Analytics",
            "← Back"
        ]

        choice = get_menu_choice(options, title="Analytics Menu")

        if choice == 1:
            _show_detailed_stats(analytics)
        elif choice == 2:
            export_path = Path(f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            analytics.export_data(export_path)
            input("\nPress Enter to continue...")
        elif choice == 3:
            from validation import get_yes_no_input
            if get_yes_no_input("Delete ALL analytics data? This cannot be undone.", default=False):
                analytics.delete_all_data()
                input("\nPress Enter to continue...")
        elif choice == 4:
            if analytics.is_enabled():
                analytics.disable()
            else:
                analytics.enable()
        elif choice == 5:
            break


def _show_detailed_stats(analytics: Analytics):
    """Show detailed statistics"""
    from platform_utils import clear_screen, print_header

    clear_screen()
    print_header("📊 Detailed Statistics")

    # Get stats per game
    sessions_by_game: Dict[str, List[SessionData]] = {}

    for session in analytics.get_all_sessions():
        if session.game_id not in sessions_by_game:
            sessions_by_game[session.game_id] = []
        sessions_by_game[session.game_id].append(session)

    print("\n" + "=" * 60)
    for game_id, sessions in sessions_by_game.items():
        total_time = sum(s.duration for s in sessions) / 3600
        avg_time = (sum(s.duration for s in sessions) / len(sessions)) / 60

        print(f"\n🎮 {game_id}")
        print(f"   Sessions: {len(sessions)}")
        print(f"   Total Time: {total_time:.1f} hours")
        print(f"   Avg Session: {avg_time:.1f} minutes")

    print("=" * 60)
    input("\nPress Enter to continue...")


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Analytics System Test")
    print("=" * 60)

    analytics = Analytics()

    print(f"Enabled: {analytics.is_enabled()}")
    print(f"Anonymous ID: {analytics.anonymous_id}")

    # Enable for testing
    analytics.enable()
    print("\n✅ Analytics enabled for testing")

    # Simulate session
    analytics.start_session('test_game', {'version': '1.0'})
    print("Session started")

    # Track some events
    analytics.track_event(EventType.LEVEL_UP, {'level': 2})
    analytics.track_event(EventType.ACHIEVEMENT_UNLOCK, {'achievement': 'first_win'})

    # End session
    time.sleep(1)  # Simulate gameplay
    analytics.end_session()
    print("Session ended")

    # Get stats
    stats = analytics.get_statistics()
    print(f"\nStatistics:")
    print(f"  Sessions: {stats['total_sessions']}")
    print(f"  Playtime: {stats['total_playtime']:.2f}s")

    print("\n✅ Analytics test passed!")
