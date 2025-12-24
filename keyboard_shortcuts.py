#!/usr/bin/env python3
"""
Keyboard Shortcuts Reference
=============================

This module provides keyboard shortcut information for all games
in the Vault 13 collection.

Usage:
    from keyboard_shortcuts import get_shortcuts, print_shortcuts

    # Get shortcuts for a specific game
    vault_shortcuts = get_shortcuts('vault_shelter')

    # Print all shortcuts
    print_shortcuts()
"""

from typing import Dict, List, Optional
from colors import C


# =============================================================================
# SHORTCUT DEFINITIONS
# =============================================================================

GLOBAL_SHORTCUTS: Dict[str, str] = {
    'q / quit': 'Exit current game or menu',
    'h / help': 'Display help information',
    'Ctrl+C': 'Force quit (emergency exit)',
    'Enter': 'Confirm selection / submit input',
    'Esc': 'Cancel current action / go back',
}

GAME_SHORTCUTS: Dict[str, Dict[str, str]] = {
    'vault_shelter': {
        '1-9': 'Select menu option by number',
        's': 'View vault status',
        'b': 'Open build menu',
        'd': 'Manage dwellers',
        'e': 'Send on expedition',
        't': 'Trade with merchants',
        'r': 'Rest / end turn',
        'i': 'Open inventory',
        'm': 'View mission log',
        'p': 'Pause game',
    },
    'prisoners_dilemma': {
        'c': 'Cooperate',
        'd': 'Defect',
        's': 'View statistics',
        'n': 'New game / new opponent',
        'o': 'View opponent info',
    },
    'trolley_problem': {
        'p / pull': 'Pull the lever (divert trolley)',
        'w / wait': 'Do nothing (let trolley continue)',
        't / think': 'Reflect on the scenario',
        's / stats': 'View your decision history',
    },
    'monty_hall': {
        '1 / 2 / 3': 'Pick a door',
        's / switch': 'Switch to the other door',
        'k / stay': 'Stay with your choice',
        'r / stats': 'View win statistics',
    },
    'echo_chambers': {
        'n / north': 'Move north',
        's / south': 'Move south',
        'e / east': 'Move east',
        'w / west': 'Move west',
        'l / look': 'Examine surroundings',
        'i / interact': 'Interact with environment',
    },
    'chinese_room': {
        't / translate': 'Look up symbol in rulebook',
        'r / respond': 'Send a response',
        'p / think': 'Ponder the philosophy',
        'x / examine': 'Examine the room',
    },
    'braess_paradox': {
        'a / add': 'Add new road',
        'r / remove': 'Remove road',
        'v / view': 'View current network',
        's / simulate': 'Run traffic simulation',
    },
    'maxwells_demon': {
        'l / left': 'Open left gate',
        'r / right': 'Open right gate',
        'w / wait': 'Wait and observe',
        's / stats': 'View entropy statistics',
    },
    'game_of_life': {
        'Space': 'Toggle cell at cursor',
        'Arrow keys': 'Move cursor',
        'Enter': 'Advance one generation',
        'r': 'Run continuous simulation',
        'p': 'Pause simulation',
        'c': 'Clear board',
    },
    'chordflow': {
        'p / play': 'Play current progression',
        'a / add': 'Add chord to progression',
        'd / delete': 'Delete last chord',
        'c / clear': 'Clear all chords',
        'r / random': 'Generate random progression',
        's / save': 'Save progression',
        'l / load': 'Load saved progression',
    },
}

NAVIGATION_SHORTCUTS: Dict[str, str] = {
    'Arrow Up/Down': 'Navigate menu options',
    'Page Up/Down': 'Scroll long content',
    'Home': 'Go to top of list',
    'End': 'Go to bottom of list',
    'Tab': 'Move to next field/section',
    'Shift+Tab': 'Move to previous field/section',
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_shortcuts(game_id: Optional[str] = None) -> Dict[str, str]:
    """
    Get keyboard shortcuts for a specific game.

    Args:
        game_id: Game identifier (e.g., 'vault_shelter')
                 If None, returns global shortcuts.

    Returns:
        Dictionary mapping shortcut keys to descriptions.
    """
    if game_id is None:
        return GLOBAL_SHORTCUTS.copy()

    # Normalize game ID
    game_id = game_id.lower().replace('-', '_').replace(' ', '_')

    if game_id in GAME_SHORTCUTS:
        return GAME_SHORTCUTS[game_id].copy()

    return {}


def get_all_shortcuts() -> Dict[str, Dict[str, str]]:
    """Get all shortcuts organized by category."""
    return {
        'global': GLOBAL_SHORTCUTS,
        'navigation': NAVIGATION_SHORTCUTS,
        **GAME_SHORTCUTS,
    }


def format_shortcut(key: str, description: str, key_width: int = 20) -> str:
    """Format a single shortcut for display."""
    return f"  {C.BOLD}{key:<{key_width}}{C.RESET} {description}"


def print_shortcuts(game_id: Optional[str] = None) -> None:
    """
    Print keyboard shortcuts to terminal.

    Args:
        game_id: Specific game to show shortcuts for.
                 If None, shows global and navigation shortcuts.
    """
    print(f"\n{C.BOLD}{C.CYAN}╔══════════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}║             KEYBOARD SHORTCUTS REFERENCE                      ║{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}╚══════════════════════════════════════════════════════════════╝{C.RESET}\n")

    # Global shortcuts
    print(f"{C.BOLD}{C.YELLOW}GLOBAL SHORTCUTS:{C.RESET}")
    print(f"{C.DIM}{'─' * 50}{C.RESET}")
    for key, desc in GLOBAL_SHORTCUTS.items():
        print(format_shortcut(key, desc))
    print()

    # Navigation shortcuts
    print(f"{C.BOLD}{C.YELLOW}NAVIGATION:{C.RESET}")
    print(f"{C.DIM}{'─' * 50}{C.RESET}")
    for key, desc in NAVIGATION_SHORTCUTS.items():
        print(format_shortcut(key, desc))
    print()

    # Game-specific shortcuts
    if game_id:
        shortcuts = get_shortcuts(game_id)
        if shortcuts:
            game_name = game_id.replace('_', ' ').title()
            print(f"{C.BOLD}{C.YELLOW}{game_name.upper()} SHORTCUTS:{C.RESET}")
            print(f"{C.DIM}{'─' * 50}{C.RESET}")
            for key, desc in shortcuts.items():
                print(format_shortcut(key, desc))
            print()
    else:
        # Show all game shortcuts
        for game, shortcuts in GAME_SHORTCUTS.items():
            game_name = game.replace('_', ' ').title()
            print(f"{C.BOLD}{C.GREEN}{game_name}:{C.RESET}")
            print(f"{C.DIM}{'─' * 50}{C.RESET}")
            for key, desc in shortcuts.items():
                print(format_shortcut(key, desc))
            print()


def get_quick_reference() -> str:
    """Get a compact quick reference string."""
    lines = [
        f"{C.BOLD}Quick Reference:{C.RESET}",
        f"  {C.DIM}q{C.RESET} quit  {C.DIM}h{C.RESET} help  {C.DIM}Enter{C.RESET} confirm  {C.DIM}Esc{C.RESET} back",
    ]
    return '\n'.join(lines)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        game = sys.argv[1]
        print_shortcuts(game)
    else:
        print_shortcuts()
