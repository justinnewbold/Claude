#!/usr/bin/env python3
"""
Shared Terminal Colors Module
=============================

Centralized ANSI color codes for all games in the Vault 13 collection.
Import this module instead of defining colors in each game file.

Usage:
    from colors import Colors, C

    print(f"{C.BOLD}Bold text{C.RESET}")
    print(f"{Colors.SUCCESS}Success!{Colors.RESET}")
"""

from typing import ClassVar


class Colors:
    """
    ANSI escape codes for terminal colors and formatting.

    Categories:
    - Basic formatting (RESET, BOLD, DIM, etc.)
    - Standard colors (RED, GREEN, BLUE, etc.)
    - Game-specific semantic colors (SUCCESS, WARNING, DANGER, etc.)
    - Theme colors for specific games
    """

    # ==========================================================================
    # BASIC FORMATTING
    # ==========================================================================
    RESET: ClassVar[str] = '\033[0m'
    BOLD: ClassVar[str] = '\033[1m'
    DIM: ClassVar[str] = '\033[2m'
    ITALIC: ClassVar[str] = '\033[3m'
    UNDERLINE: ClassVar[str] = '\033[4m'
    BLINK: ClassVar[str] = '\033[5m'
    REVERSE: ClassVar[str] = '\033[7m'
    HIDDEN: ClassVar[str] = '\033[8m'
    STRIKETHROUGH: ClassVar[str] = '\033[9m'

    # ==========================================================================
    # STANDARD FOREGROUND COLORS (8-color)
    # ==========================================================================
    BLACK: ClassVar[str] = '\033[30m'
    RED: ClassVar[str] = '\033[31m'
    GREEN: ClassVar[str] = '\033[32m'
    YELLOW: ClassVar[str] = '\033[33m'
    BLUE: ClassVar[str] = '\033[34m'
    MAGENTA: ClassVar[str] = '\033[35m'
    CYAN: ClassVar[str] = '\033[36m'
    WHITE: ClassVar[str] = '\033[37m'

    # ==========================================================================
    # BRIGHT FOREGROUND COLORS
    # ==========================================================================
    BRIGHT_BLACK: ClassVar[str] = '\033[90m'
    BRIGHT_RED: ClassVar[str] = '\033[91m'
    BRIGHT_GREEN: ClassVar[str] = '\033[92m'
    BRIGHT_YELLOW: ClassVar[str] = '\033[93m'
    BRIGHT_BLUE: ClassVar[str] = '\033[94m'
    BRIGHT_MAGENTA: ClassVar[str] = '\033[95m'
    BRIGHT_CYAN: ClassVar[str] = '\033[96m'
    BRIGHT_WHITE: ClassVar[str] = '\033[97m'

    # ==========================================================================
    # SEMANTIC COLORS (for game UI)
    # ==========================================================================
    SUCCESS: ClassVar[str] = '\033[38;5;46m'   # Bright green
    WARNING: ClassVar[str] = '\033[38;5;226m'  # Yellow
    DANGER: ClassVar[str] = '\033[38;5;196m'   # Red
    INFO: ClassVar[str] = '\033[38;5;39m'      # Blue
    MUTED: ClassVar[str] = '\033[38;5;243m'    # Gray
    SYSTEM: ClassVar[str] = '\033[38;5;243m'   # Gray (alias)

    # ==========================================================================
    # VAULT SHELTER THEME COLORS
    # ==========================================================================
    POWER: ClassVar[str] = '\033[38;5;220m'    # Yellow/gold for power
    WATER: ClassVar[str] = '\033[38;5;45m'     # Cyan for water
    FOOD: ClassVar[str] = '\033[38;5;214m'     # Orange for food
    CAPS: ClassVar[str] = '\033[38;5;226m'     # Gold for caps/currency
    HEALTH: ClassVar[str] = '\033[38;5;196m'   # Red for health
    RADIATION: ClassVar[str] = '\033[38;5;46m' # Green for radiation

    # Room colors
    ROOM_POWER: ClassVar[str] = '\033[38;5;220m'
    ROOM_WATER: ClassVar[str] = '\033[38;5;45m'
    ROOM_FOOD: ClassVar[str] = '\033[38;5;214m'
    ROOM_LIVING: ClassVar[str] = '\033[38;5;141m'
    ROOM_TRAINING: ClassVar[str] = '\033[38;5;208m'
    ROOM_STORAGE: ClassVar[str] = '\033[38;5;250m'
    ROOM_EMPTY: ClassVar[str] = '\033[38;5;240m'

    # ==========================================================================
    # PHILOSOPHICAL GAMES THEME COLORS
    # ==========================================================================
    HEADER: ClassVar[str] = '\033[38;5;87m'    # Cyan header
    PARADOX: ClassVar[str] = '\033[38;5;213m'  # Pink/magenta for paradoxes
    QUANTUM: ClassVar[str] = '\033[38;5;51m'   # Bright cyan for quantum
    DIVINE: ClassVar[str] = '\033[38;5;226m'   # Gold for divine/religious
    MATH: ClassVar[str] = '\033[38;5;51m'      # Cyan for mathematical
    SHADOW: ClassVar[str] = '\033[38;5;240m'   # Dark gray for shadows
    DEMON: ClassVar[str] = '\033[38;5;196m'    # Red for demons

    # ==========================================================================
    # TRAFFIC/NETWORK COLORS (Braess's Paradox)
    # ==========================================================================
    ROAD: ClassVar[str] = '\033[38;5;226m'     # Yellow for roads
    TRAFFIC: ClassVar[str] = '\033[38;5;203m'  # Red-orange for traffic

    # ==========================================================================
    # GAME THEORY COLORS
    # ==========================================================================
    COOPERATE: ClassVar[str] = '\033[38;5;46m'  # Green for cooperation
    DEFECT: ClassVar[str] = '\033[38;5;196m'    # Red for defection

    # ==========================================================================
    # UI ELEMENTS
    # ==========================================================================
    BORDER: ClassVar[str] = '\033[38;5;240m'   # Gray for borders
    HIGHLIGHT: ClassVar[str] = '\033[38;5;226m' # Yellow highlight
    SELECTED: ClassVar[str] = '\033[38;5;39m'   # Blue for selected items

    # ==========================================================================
    # SPECIAL STATS (SPECIAL system)
    # ==========================================================================
    STRENGTH: ClassVar[str] = '\033[38;5;196m'     # Red
    PERCEPTION: ClassVar[str] = '\033[38;5;33m'    # Blue
    ENDURANCE: ClassVar[str] = '\033[38;5;208m'    # Orange
    CHARISMA: ClassVar[str] = '\033[38;5;226m'     # Yellow
    INTELLIGENCE: ClassVar[str] = '\033[38;5;39m'  # Light blue
    AGILITY: ClassVar[str] = '\033[38;5;46m'       # Green
    LUCK: ClassVar[str] = '\033[38;5;213m'         # Pink

    # ==========================================================================
    # AI/ASSISTANT COLORS
    # ==========================================================================
    AI: ClassVar[str] = '\033[38;5;177m'       # Purple for AI responses
    USER: ClassVar[str] = '\033[38;5;87m'      # Cyan for user input

    # ==========================================================================
    # GAME-SPECIFIC COLORS (consolidated from individual games)
    # ==========================================================================
    # Butterfly Effect
    PARTICLE: ClassVar[str] = '\033[38;5;51m'       # Cyan
    WALL: ClassVar[str] = '\033[38;5;240m'          # Gray
    GOAL: ClassVar[str] = '\033[38;5;46m'           # Green
    AGENT: ClassVar[str] = '\033[38;5;226m'         # Yellow
    INTERVENTION: ClassVar[str] = '\033[38;5;141m'  # Purple
    CHAOS: ClassVar[str] = '\033[38;5;201m'         # Magenta
    ERROR: ClassVar[str] = '\033[38;5;203m'         # Red-orange

    # Infinite Library
    SHELF: ClassVar[str] = '\033[38;5;94m'          # Brown
    BOOK: ClassVar[str] = '\033[38;5;220m'          # Gold
    TEXT: ClassVar[str] = '\033[38;5;252m'          # Light gray
    SPECIAL: ClassVar[str] = '\033[38;5;141m'       # Purple
    PROPHECY: ClassVar[str] = '\033[38;5;201m'      # Bright magenta
    TRUTH: ClassVar[str] = '\033[38;5;46m'          # Bright green
    NONSENSE: ClassVar[str] = '\033[38;5;243m'      # Dark gray

    # Syntax Tree Climber
    FUNCTION: ClassVar[str] = '\033[38;5;51m'       # Cyan
    CLASS: ClassVar[str] = '\033[38;5;141m'         # Purple
    CONTROL: ClassVar[str] = '\033[38;5;214m'       # Orange
    ASSIGN: ClassVar[str] = '\033[38;5;46m'         # Green
    EXPR: ClassVar[str] = '\033[38;5;243m'          # Gray
    LITERAL: ClassVar[str] = '\033[38;5;226m'       # Yellow
    PLAYER: ClassVar[str] = '\033[38;5;201m'        # Magenta
    CODE: ClassVar[str] = '\033[38;5;117m'          # Light blue
    META: ClassVar[str] = '\033[38;5;171m'          # Pink

    # Schrodinger's Dungeon
    SUPERPOSITION: ClassVar[str] = '\033[38;5;201m' # Magenta
    OBSERVED: ClassVar[str] = '\033[38;5;252m'      # White-ish
    UNOBSERVED: ClassVar[str] = '\033[38;5;240m'    # Dark gray
    WAVE: ClassVar[str] = '\033[38;5;51m'           # Cyan

    # Code Archaeology
    ANCIENT: ClassVar[str] = '\033[38;5;130m'       # Brown/rust
    MODERN: ClassVar[str] = '\033[38;5;39m'         # Blue
    ARTIFACT: ClassVar[str] = '\033[38;5;226m'      # Gold

    # Generic game colors
    ENEMY: ClassVar[str] = '\033[38;5;196m'         # Red
    ALLY: ClassVar[str] = '\033[38;5;46m'           # Green
    NEUTRAL: ClassVar[str] = '\033[38;5;243m'       # Gray
    TREASURE: ClassVar[str] = '\033[38;5;226m'      # Gold
    PORTAL: ClassVar[str] = '\033[38;5;201m'        # Magenta

    # Echo Chambers / Timeline colors
    TIMELINE_1: ClassVar[str] = '\033[38;5;51m'     # Cyan
    TIMELINE_2: ClassVar[str] = '\033[38;5;213m'    # Pink
    TIMELINE_3: ClassVar[str] = '\033[38;5;228m'    # Yellow
    TIMELINE_4: ClassVar[str] = '\033[38;5;118m'    # Green
    TIMELINE_5: ClassVar[str] = '\033[38;5;141m'    # Purple
    HEALTHY: ClassVar[str] = '\033[38;5;46m'        # Bright green
    DECAYING: ClassVar[str] = '\033[38;5;208m'      # Orange
    CORRUPTED: ClassVar[str] = '\033[38;5;196m'     # Red
    ENTANGLED: ClassVar[str] = '\033[38;5;201m'     # Magenta
    CHOICE: ClassVar[str] = '\033[38;5;226m'        # Yellow
    ECHO: ClassVar[str] = '\033[38;5;147m'          # Light purple
    MEMORY: ClassVar[str] = '\033[38;5;183m'        # Pink

    # Code Archaeology specific
    MACHINE: ClassVar[str] = '\033[38;5;51m'        # Cyan
    ORGANIC: ClassVar[str] = '\033[38;5;120m'       # Light green
    ETHEREAL: ClassVar[str] = '\033[38;5;141m'      # Purple
    CHAOTIC: ClassVar[str] = '\033[38;5;196m'       # Red
    LORE: ClassVar[str] = '\033[38;5;183m'          # Pink
    COMMENT: ClassVar[str] = '\033[38;5;245m'       # Gray

    # Schrodinger's Dungeon specific
    SUPERPOSED: ClassVar[str] = '\033[38;5;141m'    # Purple
    ENEMY_ALIVE: ClassVar[str] = '\033[38;5;196m'   # Red
    ENEMY_DEAD: ClassVar[str] = '\033[38;5;240m'    # Dark gray
    EMPTY: ClassVar[str] = '\033[38;5;243m'         # Gray

    @classmethod
    def rgb(cls, r: int, g: int, b: int) -> str:
        """Generate 24-bit RGB color code."""
        return f'\033[38;2;{r};{g};{b}m'

    @classmethod
    def bg_rgb(cls, r: int, g: int, b: int) -> str:
        """Generate 24-bit RGB background color code."""
        return f'\033[48;2;{r};{g};{b}m'

    @classmethod
    def color256(cls, n: int) -> str:
        """Generate 256-color code (0-255)."""
        return f'\033[38;5;{n}m'

    @classmethod
    def bg_color256(cls, n: int) -> str:
        """Generate 256-color background code (0-255)."""
        return f'\033[48;5;{n}m'


# Convenience alias
C = Colors


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def colorize(text: str, *codes: str) -> str:
    """
    Apply color codes to text and reset at end.

    Usage:
        colorize("Hello", C.BOLD, C.RED)  # Bold red "Hello"
    """
    return ''.join(codes) + text + Colors.RESET


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(f"{C.BOLD}Colors Module Demo{C.RESET}")
    print("=" * 60 + "\n")

    print(f"{C.BOLD}Basic Formatting:{C.RESET}")
    print(f"  {C.BOLD}Bold{C.RESET} | {C.DIM}Dim{C.RESET} | {C.UNDERLINE}Underline{C.RESET}")

    print(f"\n{C.BOLD}Standard Colors:{C.RESET}")
    print(f"  {C.RED}Red{C.RESET} {C.GREEN}Green{C.RESET} {C.BLUE}Blue{C.RESET} {C.YELLOW}Yellow{C.RESET} {C.MAGENTA}Magenta{C.RESET} {C.CYAN}Cyan{C.RESET}")

    print(f"\n{C.BOLD}Semantic Colors:{C.RESET}")
    print(f"  {C.SUCCESS}Success{C.RESET} {C.WARNING}Warning{C.RESET} {C.DANGER}Danger{C.RESET} {C.INFO}Info{C.RESET} {C.MUTED}Muted{C.RESET}")

    print(f"\n{C.BOLD}Vault Theme:{C.RESET}")
    print(f"  {C.POWER}Power{C.RESET} {C.WATER}Water{C.RESET} {C.FOOD}Food{C.RESET} {C.CAPS}Caps{C.RESET} {C.HEALTH}Health{C.RESET}")

    print(f"\n{C.BOLD}Philosophy Theme:{C.RESET}")
    print(f"  {C.PARADOX}Paradox{C.RESET} {C.QUANTUM}Quantum{C.RESET} {C.DIVINE}Divine{C.RESET} {C.SHADOW}Shadow{C.RESET}")

    print(f"\n{C.BOLD}Custom Colors:{C.RESET}")
    print(f"  RGB: {Colors.rgb(255, 100, 50)}Custom Orange{C.RESET}")
    print(f"  256: {Colors.color256(200)}Color 200{C.RESET}")

    print(f"\n{C.BOLD}Colorize helper:{C.RESET}")
    print(f"  {colorize('Bold Red Text', C.BOLD, C.RED)}")

    print("\n" + "=" * 60)
    print(f"{C.SUCCESS}✓ All colors working!{C.RESET}")
    print("=" * 60 + "\n")
