#!/usr/bin/env python3
"""
VAULT 13 Game Enhancements Module v1.0
======================================
Additional features and visual improvements for the VAULT 13 game collection.

Features:
- Advanced Weather System with effects
- Enhanced Notification Center
- Improved ASCII Art Generator
- Sound Effects (terminal bell)
- Screen Transitions
- Mini-map visualization
"""

import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum
from datetime import datetime


# =============================================================================
# ENHANCED COLOR SYSTEM
# =============================================================================

class Theme:
    """Enhanced color theme with gradients and effects"""

    # Base colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

    # Vault Theme Colors
    VAULT_BLUE = '\033[38;5;33m'
    VAULT_GOLD = '\033[38;5;220m'
    VAULT_GREEN = '\033[38;5;46m'
    VAULT_RED = '\033[38;5;196m'
    VAULT_CYAN = '\033[38;5;51m'
    VAULT_PURPLE = '\033[38;5;141m'
    VAULT_ORANGE = '\033[38;5;208m'
    VAULT_PINK = '\033[38;5;213m'

    # Gradient helpers
    @staticmethod
    def gradient_text(text: str, start_color: int, end_color: int) -> str:
        """Apply a gradient effect to text"""
        if len(text) == 0:
            return text

        result = []
        step = (end_color - start_color) / max(len(text) - 1, 1)

        for i, char in enumerate(text):
            color = int(start_color + step * i)
            result.append(f'\033[38;5;{color}m{char}')

        return ''.join(result) + '\033[0m'

    @staticmethod
    def rainbow_text(text: str) -> str:
        """Apply rainbow colors to text"""
        colors = [196, 208, 226, 46, 51, 21, 129]
        result = []

        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result.append(f'\033[38;5;{color}m{char}')

        return ''.join(result) + '\033[0m'

    @staticmethod
    def pulse_color(base_color: int, intensity: float) -> str:
        """Get a pulsing color effect"""
        # Adjust brightness based on intensity (0.0 to 1.0)
        adjusted = max(16, min(255, base_color + int(intensity * 20)))
        return f'\033[38;5;{adjusted}m'


# =============================================================================
# WEATHER SYSTEM
# =============================================================================

class WeatherType(Enum):
    """Weather conditions that affect the vault"""
    CLEAR = "Clear"
    CLOUDY = "Cloudy"
    RAIN = "Rain"
    STORM = "Storm"
    RADIATION_STORM = "Radiation Storm"
    DUST_STORM = "Dust Storm"
    ACID_RAIN = "Acid Rain"
    HEAT_WAVE = "Heat Wave"
    COLD_SNAP = "Cold Snap"
    FOG = "Fog"


@dataclass
class WeatherEffect:
    """Effects of weather on vault systems"""
    power_modifier: float = 1.0
    water_modifier: float = 1.0
    food_modifier: float = 1.0
    happiness_modifier: float = 0.0
    health_modifier: float = 0.0
    event_chance_modifier: float = 1.0
    exploration_modifier: float = 1.0
    description: str = ""
    duration_range: Tuple[int, int] = (1, 5)
    icon: str = "☀️"
    animation_frames: List[str] = field(default_factory=list)


# Weather definitions with effects
WEATHER_EFFECTS: Dict[WeatherType, WeatherEffect] = {
    WeatherType.CLEAR: WeatherEffect(
        power_modifier=1.1,  # Solar power bonus
        happiness_modifier=2,
        exploration_modifier=1.2,
        description="Perfect wasteland conditions",
        duration_range=(3, 8),
        icon="☀️",
        animation_frames=["☀️ ", " ☀️", "☀️ "]
    ),
    WeatherType.CLOUDY: WeatherEffect(
        power_modifier=0.9,
        description="Overcast skies reduce solar efficiency",
        duration_range=(2, 6),
        icon="☁️",
        animation_frames=["☁️ ", "☁ ", " ☁️"]
    ),
    WeatherType.RAIN: WeatherEffect(
        water_modifier=1.3,  # Rain collection bonus
        power_modifier=0.8,
        happiness_modifier=-1,
        exploration_modifier=0.8,
        description="Rain provides water but reduces visibility",
        duration_range=(1, 4),
        icon="🌧️",
        animation_frames=["🌧️", "💧", "🌧️", "💧"]
    ),
    WeatherType.STORM: WeatherEffect(
        power_modifier=0.5,
        water_modifier=1.5,
        happiness_modifier=-3,
        event_chance_modifier=1.5,
        exploration_modifier=0.3,
        description="Dangerous storm conditions",
        duration_range=(1, 3),
        icon="⛈️",
        animation_frames=["⛈️", "⚡", "🌩️", "⚡"]
    ),
    WeatherType.RADIATION_STORM: WeatherEffect(
        power_modifier=0.7,
        health_modifier=-5,
        happiness_modifier=-5,
        event_chance_modifier=2.0,
        exploration_modifier=0.0,
        description="DANGER: High radiation levels outside!",
        duration_range=(1, 2),
        icon="☢️",
        animation_frames=["☢️ ", " ☢️", "⚠️ ", " ⚠️"]
    ),
    WeatherType.DUST_STORM: WeatherEffect(
        power_modifier=0.6,
        food_modifier=0.9,
        happiness_modifier=-2,
        exploration_modifier=0.2,
        description="Dust reduces visibility and clogs filters",
        duration_range=(1, 3),
        icon="🌪️",
        animation_frames=["🌪️", "💨", "🌫️", "💨"]
    ),
    WeatherType.ACID_RAIN: WeatherEffect(
        water_modifier=0.5,  # Can't collect acid rain
        health_modifier=-3,
        happiness_modifier=-4,
        exploration_modifier=0.1,
        description="Corrosive precipitation damages equipment",
        duration_range=(1, 2),
        icon="🧪",
        animation_frames=["🧪", "💚", "🧪", "💀"]
    ),
    WeatherType.HEAT_WAVE: WeatherEffect(
        power_modifier=1.3,  # More solar
        water_modifier=0.7,  # More evaporation
        food_modifier=0.9,
        happiness_modifier=-3,
        health_modifier=-2,
        description="Extreme heat taxes cooling systems",
        duration_range=(2, 5),
        icon="🔥",
        animation_frames=["🔥", "🌡️", "☀️", "🔥"]
    ),
    WeatherType.COLD_SNAP: WeatherEffect(
        power_modifier=0.7,  # Heating costs
        water_modifier=0.8,  # Frozen pipes
        happiness_modifier=-2,
        health_modifier=-1,
        description="Freezing temperatures require extra heating",
        duration_range=(2, 4),
        icon="❄️",
        animation_frames=["❄️", "🥶", "❄️", "🌨️"]
    ),
    WeatherType.FOG: WeatherEffect(
        exploration_modifier=0.5,
        event_chance_modifier=1.3,
        description="Limited visibility outside the vault",
        duration_range=(1, 3),
        icon="🌫️",
        animation_frames=["🌫️", "  ", "🌫️", " 🌫️"]
    ),
}


class WeatherSystem:
    """Manages weather conditions and their effects"""

    def __init__(self):
        self.current_weather = WeatherType.CLEAR
        self.days_remaining = 0
        self.forecast: List[WeatherType] = []
        self.weather_history: List[Tuple[int, WeatherType]] = []
        self.day = 0
        self._generate_forecast()

    def _generate_forecast(self, days: int = 5):
        """Generate weather forecast for upcoming days"""
        self.forecast = []
        weights = {
            WeatherType.CLEAR: 25,
            WeatherType.CLOUDY: 20,
            WeatherType.RAIN: 15,
            WeatherType.STORM: 8,
            WeatherType.RADIATION_STORM: 3,
            WeatherType.DUST_STORM: 10,
            WeatherType.ACID_RAIN: 2,
            WeatherType.HEAT_WAVE: 8,
            WeatherType.COLD_SNAP: 7,
            WeatherType.FOG: 12,
        }

        weather_types = list(weights.keys())
        weather_weights = list(weights.values())

        for _ in range(days):
            weather = random.choices(weather_types, weights=weather_weights)[0]
            self.forecast.append(weather)

    def advance_day(self) -> Tuple[WeatherType, Optional[str]]:
        """Advance to the next day and potentially change weather"""
        self.day += 1
        message = None

        if self.days_remaining > 0:
            self.days_remaining -= 1
        else:
            # Weather changes
            old_weather = self.current_weather

            if self.forecast:
                self.current_weather = self.forecast.pop(0)
                self.forecast.append(random.choice(list(WeatherType)))
            else:
                self._generate_forecast()
                self.current_weather = self.forecast.pop(0)

            effect = WEATHER_EFFECTS[self.current_weather]
            self.days_remaining = random.randint(*effect.duration_range)

            # Record history
            self.weather_history.append((self.day, self.current_weather))
            if len(self.weather_history) > 30:
                self.weather_history.pop(0)

            if old_weather != self.current_weather:
                message = f"Weather changed: {effect.icon} {self.current_weather.value}"

        return self.current_weather, message

    def get_current_effects(self) -> WeatherEffect:
        """Get the effects of current weather"""
        return WEATHER_EFFECTS[self.current_weather]

    def get_weather_display(self) -> str:
        """Get formatted weather display for UI"""
        effect = WEATHER_EFFECTS[self.current_weather]
        forecast_icons = ' '.join([WEATHER_EFFECTS[w].icon for w in self.forecast[:3]])

        return (
            f"{effect.icon} {self.current_weather.value} "
            f"({self.days_remaining}d) │ Forecast: {forecast_icons}"
        )

    def get_detailed_report(self) -> List[str]:
        """Get detailed weather report"""
        effect = WEATHER_EFFECTS[self.current_weather]

        lines = [
            f"╔{'═' * 50}╗",
            f"║ {Theme.BOLD}WEATHER REPORT{Theme.RESET}".ljust(59) + "║",
            f"╠{'═' * 50}╣",
            f"║ Current: {effect.icon} {self.current_weather.value}".ljust(51) + "║",
            f"║ Duration: {self.days_remaining} day(s) remaining".ljust(51) + "║",
            f"║ {effect.description}".ljust(51) + "║",
            f"╠{'═' * 50}╣",
            f"║ {Theme.BOLD}EFFECTS:{Theme.RESET}".ljust(59) + "║",
        ]

        # Add effect modifiers
        if effect.power_modifier != 1.0:
            mod = f"{'+' if effect.power_modifier > 1 else ''}{int((effect.power_modifier - 1) * 100)}%"
            lines.append(f"║   ⚡ Power: {mod}".ljust(51) + "║")

        if effect.water_modifier != 1.0:
            mod = f"{'+' if effect.water_modifier > 1 else ''}{int((effect.water_modifier - 1) * 100)}%"
            lines.append(f"║   💧 Water: {mod}".ljust(51) + "║")

        if effect.food_modifier != 1.0:
            mod = f"{'+' if effect.food_modifier > 1 else ''}{int((effect.food_modifier - 1) * 100)}%"
            lines.append(f"║   🍖 Food: {mod}".ljust(51) + "║")

        if effect.happiness_modifier != 0:
            mod = f"{'+' if effect.happiness_modifier > 0 else ''}{effect.happiness_modifier}"
            lines.append(f"║   😊 Happiness: {mod}".ljust(51) + "║")

        if effect.health_modifier != 0:
            mod = f"{'+' if effect.health_modifier > 0 else ''}{effect.health_modifier}"
            lines.append(f"║   ❤️ Health: {mod}".ljust(51) + "║")

        if effect.exploration_modifier != 1.0:
            mod = f"{'+' if effect.exploration_modifier > 1 else ''}{int((effect.exploration_modifier - 1) * 100)}%"
            lines.append(f"║   🗺️ Exploration: {mod}".ljust(51) + "║")

        # Forecast
        lines.append(f"╠{'═' * 50}╣")
        lines.append(f"║ {Theme.BOLD}5-DAY FORECAST:{Theme.RESET}".ljust(59) + "║")

        for i, weather in enumerate(self.forecast[:5]):
            w_effect = WEATHER_EFFECTS[weather]
            lines.append(f"║   Day {i + 1}: {w_effect.icon} {weather.value}".ljust(51) + "║")

        lines.append(f"╚{'═' * 50}╝")

        return lines


# =============================================================================
# NOTIFICATION CENTER
# =============================================================================

class NotificationType(Enum):
    """Types of notifications"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    ACHIEVEMENT = "achievement"
    QUEST = "quest"
    EVENT = "event"


@dataclass
class Notification:
    """A single notification"""
    message: str
    type: NotificationType
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False
    priority: int = 0  # Higher = more important
    icon: str = ""
    action: Optional[str] = None  # Optional action hint

    def __post_init__(self):
        if not self.icon:
            icons = {
                NotificationType.INFO: "ℹ️",
                NotificationType.SUCCESS: "✅",
                NotificationType.WARNING: "⚠️",
                NotificationType.DANGER: "🚨",
                NotificationType.ACHIEVEMENT: "🏆",
                NotificationType.QUEST: "📜",
                NotificationType.EVENT: "📢",
            }
            self.icon = icons.get(self.type, "•")


class NotificationCenter:
    """Manages game notifications with priority queue"""

    def __init__(self, max_notifications: int = 50):
        self.notifications: List[Notification] = []
        self.max_notifications = max_notifications
        self.unread_count = 0

    def add(self, message: str, type: NotificationType = NotificationType.INFO,
            priority: int = 0, icon: str = "", action: str = None):
        """Add a new notification"""
        notification = Notification(
            message=message,
            type=type,
            priority=priority,
            icon=icon,
            action=action
        )

        self.notifications.insert(0, notification)
        self.unread_count += 1

        # Trim old notifications
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[:self.max_notifications]

    def get_recent(self, count: int = 5, unread_only: bool = False) -> List[Notification]:
        """Get recent notifications"""
        if unread_only:
            return [n for n in self.notifications if not n.read][:count]
        return self.notifications[:count]

    def get_by_type(self, type: NotificationType) -> List[Notification]:
        """Get notifications of a specific type"""
        return [n for n in self.notifications if n.type == type]

    def mark_read(self, index: int = None):
        """Mark notification(s) as read"""
        if index is not None:
            if 0 <= index < len(self.notifications):
                if not self.notifications[index].read:
                    self.notifications[index].read = True
                    self.unread_count = max(0, self.unread_count - 1)
        else:
            # Mark all as read
            for n in self.notifications:
                n.read = True
            self.unread_count = 0

    def clear(self):
        """Clear all notifications"""
        self.notifications = []
        self.unread_count = 0

    def get_display(self, count: int = 3) -> List[str]:
        """Get formatted notification display"""
        if not self.notifications:
            return ["   No notifications"]

        lines = []
        colors = {
            NotificationType.INFO: Theme.VAULT_CYAN,
            NotificationType.SUCCESS: Theme.VAULT_GREEN,
            NotificationType.WARNING: Theme.VAULT_GOLD,
            NotificationType.DANGER: Theme.VAULT_RED,
            NotificationType.ACHIEVEMENT: Theme.VAULT_PURPLE,
            NotificationType.QUEST: Theme.VAULT_PINK,
            NotificationType.EVENT: Theme.VAULT_ORANGE,
        }

        for notif in self.notifications[:count]:
            color = colors.get(notif.type, Theme.RESET)
            read_marker = " " if notif.read else "•"
            lines.append(f"{read_marker} {notif.icon} {color}{notif.message}{Theme.RESET}")

        if len(self.notifications) > count:
            remaining = len(self.notifications) - count
            lines.append(f"   {Theme.DIM}... and {remaining} more{Theme.RESET}")

        return lines


# =============================================================================
# ASCII ART GENERATOR
# =============================================================================

class ASCIIArt:
    """Generate and display ASCII art for the game"""

    VAULT_LOGO = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║  ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗   ██╗██████╗    ║
    ║  ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝  ███║╚════██╗   ║
    ║  ██║   ██║███████║██║   ██║██║     ██║     ╚██║ █████╔╝   ║
    ║  ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║      ██║ ╚═══██╗   ║
    ║   ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║      ██║██████╔╝   ║
    ║    ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝      ╚═╝╚═════╝    ║
    ║                                                           ║
    ║          ⚡ SURVIVAL PROTOCOL ⚡                           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """

    VAULT_DOOR = """
                    ╭─────────────────────────╮
                 ╭──┤    VAULT-TEC INDUSTRIES  ├──╮
              ╭──┤  ╰─────────────────────────╯  ├──╮
           ╭──┤  │    ┌───────────────────┐    │  ├──╮
        ╭──┤  │  │    │   ╔═══════════╗   │    │  │  ├──╮
        │  │  │  │    │   ║  VAULT    ║   │    │  │  │  │
        │  │  │  │    │   ║    13     ║   │    │  │  │  │
        │  │  │  │    │   ╚═══════════╝   │    │  │  │  │
        │  │  │  │    │                   │    │  │  │  │
        │  │  │  │    │   ◉ SECURED ◉    │    │  │  │  │
        │  │  │  │    └───────────────────┘    │  │  │  │
        │  │  │  │                              │  │  │  │
        ╰──┤  │  ╰──────────────────────────────╯  │  ├──╯
           ╰──┤                                    ├──╯
              ╰────────────────────────────────────╯
    """

    GAME_OVER = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║    ██████╗  █████╗ ███╗   ███╗███████╗               ║
    ║   ██╔════╝ ██╔══██╗████╗ ████║██╔════╝               ║
    ║   ██║  ███╗███████║██╔████╔██║█████╗                 ║
    ║   ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝                 ║
    ║   ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗               ║
    ║    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝               ║
    ║                                                      ║
    ║    ██████╗ ██╗   ██╗███████╗██████╗                  ║
    ║   ██╔═══██╗██║   ██║██╔════╝██╔══██╗                 ║
    ║   ██║   ██║██║   ██║█████╗  ██████╔╝                 ║
    ║   ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗                 ║
    ║   ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║                 ║
    ║    ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝                 ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """

    VICTORY = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗   ║
    ║   ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝   ║
    ║   ██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝    ║
    ║   ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝     ║
    ║    ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║      ║
    ║     ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ║
    ║                                                              ║
    ║          🏆 CONGRATULATIONS, OVERSEER! 🏆                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """

    LOADING_FRAMES = [
        "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
    ]

    @staticmethod
    def animate_loading(message: str = "Loading", duration: float = 2.0):
        """Display animated loading indicator"""
        frames = ASCIIArt.LOADING_FRAMES
        end_time = time.time() + duration
        i = 0

        while time.time() < end_time:
            print(f"\r{frames[i % len(frames)]} {message}...", end='', flush=True)
            time.sleep(0.1)
            i += 1

        print(f"\r✓ {message}... Done!    ")

    @staticmethod
    def draw_bordered_text(text: str, width: int = 60, title: str = "") -> List[str]:
        """Draw text in a decorative border"""
        lines = text.split('\n')
        max_width = max(len(line) for line in lines) if lines else 0
        width = max(width, max_width + 4)

        result = []

        # Top border with optional title
        if title:
            title_text = f"╡ {title} ╞"
            padding = (width - 2 - len(title_text)) // 2
            result.append(f"╔{'═' * padding}{title_text}{'═' * (width - 2 - padding - len(title_text))}╗")
        else:
            result.append(f"╔{'═' * (width - 2)}╗")

        # Content
        for line in lines:
            padding = width - 4 - len(line)
            result.append(f"║ {line}{' ' * padding} ║")

        # Bottom border
        result.append(f"╚{'═' * (width - 2)}╝")

        return result

    @staticmethod
    def create_mini_map(rooms: List[List[str]], width: int = 10, height: int = 5) -> List[str]:
        """Create a mini-map visualization of vault rooms"""
        lines = []
        lines.append("┌" + "─" * (width * 3) + "┐")

        for y in range(height):
            row = "│"
            for x in range(width):
                if y < len(rooms) and x < len(rooms[y]):
                    room = rooms[y][x]
                    if room:
                        # Map room types to symbols
                        symbols = {
                            'power': '⚡',
                            'water': '💧',
                            'food': '🍖',
                            'living': '🏠',
                            'medbay': '⚕️',
                            'storage': '📦',
                            'training': '💪',
                            'lab': '🔬',
                            'empty': '░░',
                        }
                        symbol = symbols.get(room.lower()[:5], '▒▒')
                        row += f"{symbol} "
                    else:
                        row += "░░ "
                else:
                    row += "░░ "
            row += "│"
            lines.append(row)

        lines.append("└" + "─" * (width * 3) + "┘")
        return lines

    @staticmethod
    def create_stat_graph(values: List[int], width: int = 20, height: int = 5,
                          title: str = "", color: str = "") -> List[str]:
        """Create a simple bar graph for statistics"""
        if not values:
            return []

        max_val = max(values) if max(values) > 0 else 1
        normalized = [int((v / max_val) * height) for v in values[-width:]]

        lines = []
        if title:
            lines.append(f"{color}{title}{Theme.RESET}")

        for row in range(height, 0, -1):
            line = ""
            for val in normalized:
                if val >= row:
                    line += f"{color}█{Theme.RESET}"
                else:
                    line += "░"
            lines.append(f"│{line}│")

        lines.append("└" + "─" * len(normalized) + "┘")

        return lines


# =============================================================================
# SCREEN EFFECTS
# =============================================================================

class ScreenEffects:
    """Terminal screen effects and transitions"""

    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        print('\033[2J\033[H', end='')

    @staticmethod
    def move_cursor(x: int, y: int):
        """Move cursor to position"""
        print(f'\033[{y};{x}H', end='')

    @staticmethod
    def hide_cursor():
        """Hide the cursor"""
        print('\033[?25l', end='')

    @staticmethod
    def show_cursor():
        """Show the cursor"""
        print('\033[?25h', end='')

    @staticmethod
    def bell():
        """Sound terminal bell"""
        print('\a', end='')

    @staticmethod
    def flash_screen():
        """Flash the screen (reverse video effect)"""
        print('\033[?5h', end='')  # Reverse video on
        time.sleep(0.1)
        print('\033[?5l', end='')  # Reverse video off

    @staticmethod
    def typewriter_effect(text: str, delay: float = 0.03):
        """Print text with typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            if char not in ' \n':
                time.sleep(delay)
        print()

    @staticmethod
    def fade_in_text(text: str, steps: int = 5):
        """Simulate fade-in effect using brightness levels"""
        # Use dim -> normal transition
        for i in range(steps):
            brightness = 232 + (i * 4)  # Grayscale from dark to light
            print(f'\r\033[38;5;{brightness}m{text}\033[0m', end='', flush=True)
            time.sleep(0.1)
        print(f'\r{text}')

    @staticmethod
    def wipe_transition(direction: str = 'right', char: str = '█'):
        """Screen wipe transition effect"""
        import shutil
        width = shutil.get_terminal_size().columns

        if direction == 'right':
            for i in range(width):
                print('\r' + char * i, end='', flush=True)
                time.sleep(0.01)
        elif direction == 'left':
            for i in range(width, 0, -1):
                print('\r' + ' ' * (width - i) + char * i, end='', flush=True)
                time.sleep(0.01)

        ScreenEffects.clear_screen()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_progress_animation(current: int, maximum: int, width: int = 20,
                               style: str = 'default') -> str:
    """Create an animated progress bar"""
    if maximum == 0:
        return '[' + '░' * width + ']'

    filled = int((current / maximum) * width)

    styles = {
        'default': ('█', '░'),
        'blocks': ('▓', '░'),
        'arrows': ('▶', '─'),
        'dots': ('●', '○'),
        'lines': ('━', '─'),
    }

    fill_char, empty_char = styles.get(style, styles['default'])

    return f'[{fill_char * filled}{empty_char * (width - filled)}]'


def format_time_remaining(seconds: int) -> str:
    """Format seconds into readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def create_table(headers: List[str], rows: List[List[str]],
                 column_widths: List[int] = None) -> List[str]:
    """Create a formatted table"""
    if not column_widths:
        column_widths = [max(len(str(row[i])) for row in [headers] + rows)
                        for i in range(len(headers))]

    lines = []

    # Top border
    border = "┌" + "┬".join("─" * (w + 2) for w in column_widths) + "┐"
    lines.append(border)

    # Header
    header_row = "│" + "│".join(f" {h.ljust(w)} " for h, w in zip(headers, column_widths)) + "│"
    lines.append(header_row)

    # Header separator
    separator = "├" + "┼".join("─" * (w + 2) for w in column_widths) + "┤"
    lines.append(separator)

    # Data rows
    for row in rows:
        data_row = "│" + "│".join(f" {str(c).ljust(w)} " for c, w in zip(row, column_widths)) + "│"
        lines.append(data_row)

    # Bottom border
    bottom = "└" + "┴".join("─" * (w + 2) for w in column_widths) + "┘"
    lines.append(bottom)

    return lines


# =============================================================================
# MAIN (Testing)
# =============================================================================

if __name__ == '__main__':
    print(Theme.rainbow_text("VAULT 13 - Game Enhancements Module"))
    print()

    # Test weather system
    weather = WeatherSystem()
    print("Weather System Test:")
    print(weather.get_weather_display())
    print()

    for line in weather.get_detailed_report():
        print(line)
    print()

    # Test notification center
    notifications = NotificationCenter()
    notifications.add("Welcome to Vault 13!", NotificationType.INFO)
    notifications.add("Power levels critical!", NotificationType.DANGER, priority=10)
    notifications.add("New quest available", NotificationType.QUEST)
    notifications.add("Achievement unlocked: First Steps", NotificationType.ACHIEVEMENT)

    print("Notification Center Test:")
    for line in notifications.get_display():
        print(line)
    print()

    # Test ASCII art
    print(Theme.gradient_text("Gradient Text Test - VAULT 13", 21, 51))
    print()

    print("Progress Bar Styles:")
    for style in ['default', 'blocks', 'arrows', 'dots', 'lines']:
        print(f"  {style}: {create_progress_animation(75, 100, 20, style)}")
    print()

    # Test table
    print("Table Test:")
    headers = ["Name", "Level", "Health", "Status"]
    rows = [
        ["Marcus", "5", "100/100", "Active"],
        ["Sarah", "3", "85/100", "Training"],
        ["John", "7", "50/100", "Injured"],
    ]
    for line in create_table(headers, rows):
        print(line)
