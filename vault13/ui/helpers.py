"""
VAULT 13: UI Helper Functions
Utility functions for terminal UI rendering.
"""

import time
from typing import List

from colors import C


def make_progress_bar(current: int, maximum: int, width: int = 12,
                      filled: str = "█", empty: str = "░") -> str:
    """Create a visual progress bar"""
    if maximum == 0:
        return f"[{empty * width}]"
    filled_amount = int((current / maximum) * width)
    return f"[{filled * filled_amount}{empty * (width - filled_amount)}]"


def get_status_color(value: float, max_value: float, reverse: bool = False) -> str:
    """Get color based on value ratio (red/yellow/green)"""
    ratio = value / max_value if max_value > 0 else 0
    if reverse:
        ratio = 1 - ratio

    if ratio >= 0.7:
        return '\033[38;5;46m'  # Green
    elif ratio >= 0.4:
        return '\033[38;5;226m'  # Yellow
    else:
        return '\033[38;5;196m'  # Red


def get_trend_indicator(current: int, previous: int) -> str:
    """Get trend arrow (↑↓→)"""
    if current > previous:
        return "↑"
    elif current < previous:
        return "↓"
    else:
        return "→"


def format_stat_bar(name: str, current: int, maximum: int, width: int = 12) -> str:
    """Format a stat with progress bar and color"""
    color = get_status_color(current, maximum)
    bar = make_progress_bar(current, maximum, width)
    reset = '\033[0m'
    return f"{name}: {color}{bar}{reset} {current}/{maximum}"


def draw_box(text: str, width: int = 40, style: str = "single") -> List[str]:
    """Draw a text box with borders"""
    if style == "double":
        corners = ("╔", "╗", "╚", "╝")
        horiz, vert = "═", "║"
    else:
        corners = ("┌", "┐", "└", "┘")
        horiz, vert = "─", "│"

    lines = []
    lines.append(f"{corners[0]}{horiz * (width - 2)}{corners[1]}")
    for line in text.split("\n"):
        padding = width - len(line) - 4
        lines.append(f"{vert} {line}{' ' * max(0, padding)} {vert}")
    lines.append(f"{corners[2]}{horiz * (width - 2)}{corners[3]}")
    return lines


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def create_sparkline(values: List[int], width: int = 10) -> str:
    """Create a simple sparkline graph"""
    if not values or len(values) == 0:
        return " " * width

    chars = "▁▂▃▄▅▆▇█"
    max_val = max(values) if max(values) > 0 else 1
    min_val = min(values)

    result = ""
    for val in values[-width:]:
        normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
        idx = min(int(normalized * (len(chars) - 1)), len(chars) - 1)
        result += chars[idx]

    return result.ljust(width)


def quick_feedback(message: str, style: str = "info", duration: float = 1.0):
    """Show quick non-blocking feedback message"""
    colors = {
        "success": C.SUCCESS,
        "warning": C.WARNING,
        "danger": C.DANGER,
        "info": C.INFO
    }
    icons = {
        "success": "✓",
        "warning": "⚠",
        "danger": "✗",
        "info": "ℹ"
    }
    color = colors.get(style, C.INFO)
    icon = icons.get(style, "•")
    print(f"\n{color}{icon} {message}{C.RESET}")
    time.sleep(duration)


def confirm_action(message: str, default: bool = False) -> bool:
    """Quick confirmation prompt with sensible defaults"""
    default_hint = "[Y/n]" if default else "[y/N]"
    response = input(f"{C.WARNING}{message} {default_hint}: {C.RESET}").strip().lower()
    if not response:
        return default
    return response in ['y', 'yes', '1', 'true']


def print_breadcrumb(*path: str):
    """Print navigation breadcrumb"""
    crumbs = " > ".join(path)
    print(f"{C.DIM}📍 {crumbs}{C.RESET}")
    print(f"{C.DIM}[0] Back  [/] Search  [?] Help{C.RESET}\n")


def print_header(title: str, subtitle: str = "", width: int = 60):
    """Print a styled header"""
    print(f"\n{C.HEADER}{C.BOLD}{'=' * width}{C.RESET}")
    print(f"{C.HEADER}{C.BOLD}{title.center(width)}{C.RESET}")
    if subtitle:
        print(f"{C.DIM}{subtitle.center(width)}{C.RESET}")
    print(f"{C.HEADER}{C.BOLD}{'=' * width}{C.RESET}\n")


def print_menu_option(key: str, description: str, enabled: bool = True):
    """Print a menu option with consistent formatting"""
    if enabled:
        print(f"  {C.SUCCESS}[{key}]{C.RESET} {description}")
    else:
        print(f"  {C.DIM}[{key}] {description} (unavailable){C.RESET}")


def print_resource_line(name: str, current: int, maximum: int, icon: str = ""):
    """Print a resource with bar and percentage"""
    pct = (current / maximum * 100) if maximum > 0 else 0
    bar = make_progress_bar(current, maximum, width=15)
    color = get_status_color(current, maximum)
    print(f"  {icon} {name:12} {color}{bar}{C.RESET} {current:3}/{maximum:3} ({pct:.0f}%)")


def format_time_remaining(turns: int) -> str:
    """Format turns remaining as human-readable string"""
    if turns <= 0:
        return "Complete"
    elif turns == 1:
        return "1 turn"
    else:
        return f"{turns} turns"


def print_divider(char: str = "─", width: int = 60):
    """Print a divider line"""
    print(f"{C.DIM}{char * width}{C.RESET}")
