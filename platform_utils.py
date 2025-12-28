#!/usr/bin/env python3
"""
Cross-Platform Utilities for VAULT 13 Game Collection
======================================================

Provides platform-agnostic utilities for terminal handling, paths, and system
operations. This module ensures consistent behavior across Windows, macOS, and Linux.

SUPPORTED PLATFORMS
-------------------
- Windows 10+ (with Windows Terminal or cmd.exe with VT100 support)
- macOS 10.12+
- Linux (any modern distribution with a terminal emulator)

TERMINAL COLOR SUPPORT
----------------------
Colors are handled differently on each platform:

**Windows:**
  1. Uses colorama package (preferred) - automatically converts ANSI codes
  2. Falls back to Windows VT100 mode via ctypes if colorama unavailable
  3. Final fallback: os.system('') trick to enable ANSI support

**Unix (Linux/macOS):**
  - Native ANSI escape code support in all modern terminals
  - No special initialization required

**Disabling Colors:**
  - Set environment variable NO_COLOR=1 to disable all color output
  - Set TERM=dumb to simulate a dumb terminal

KEYBOARD INPUT
--------------
Non-blocking keyboard input works differently:

**Windows:**
  - Uses msvcrt.getch() and msvcrt.kbhit()
  - No special terminal mode changes required

**Unix:**
  - Uses termios to set terminal to raw mode
  - Falls back to regular input() if termios unavailable
  - Requires proper cleanup via try/finally or context manager

ASYNC SUPPORT
-------------
Async/event-driven I/O via eventlet is Unix-only. Windows uses threading fallback.

UNICODE
-------
- Windows: Ensure UTF-8 console mode with `chcp 65001` or Python UTF-8 mode
- Unix: Usually UTF-8 by default, respects LANG/LC_* environment variables

USAGE EXAMPLE
-------------
    from platform_utils import init_terminal, clear_screen, is_windows

    # Initialize terminal (required for Windows color support)
    init_terminal()

    # Clear screen (works cross-platform)
    clear_screen()

    # Platform-specific code
    if is_windows():
        # Windows-specific behavior
        pass
"""

import os
import sys
import shutil
import platform
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
from enum import Enum

# =============================================================================
# PLATFORM DETECTION
# =============================================================================

class Platform(Enum):
    """Supported platforms"""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"


def get_platform() -> Platform:
    """Detect the current operating system."""
    system = platform.system().lower()
    if system == "windows":
        return Platform.WINDOWS
    elif system == "darwin":
        return Platform.MACOS
    elif system == "linux":
        return Platform.LINUX
    return Platform.UNKNOWN


def is_windows() -> bool:
    """Check if running on Windows."""
    return get_platform() == Platform.WINDOWS


def is_macos() -> bool:
    """Check if running on macOS."""
    return get_platform() == Platform.MACOS


def is_linux() -> bool:
    """Check if running on Linux."""
    return get_platform() == Platform.LINUX


def is_unix() -> bool:
    """Check if running on a Unix-like system (Linux or macOS)."""
    return get_platform() in (Platform.LINUX, Platform.MACOS)


# =============================================================================
# TERMINAL INITIALIZATION
# =============================================================================

_terminal_initialized = False


def init_terminal() -> bool:
    """
    Initialize terminal for cross-platform color and Unicode support.
    Returns True if initialization succeeded.
    """
    global _terminal_initialized

    if _terminal_initialized:
        return True

    success = True

    if is_windows():
        # Enable ANSI escape sequences on Windows 10+
        try:
            # Method 1: Use colorama (preferred)
            import colorama
            colorama.init(autoreset=False, convert=True, strip=False)
        except ImportError:
            # Method 2: Enable VT100 mode via Windows API
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(
                    kernel32.GetStdHandle(-11),  # STD_OUTPUT_HANDLE
                    0x0001 | 0x0004  # ENABLE_PROCESSED_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING
                )
            except Exception:
                # Method 3: Simple fallback - running any command enables ANSI
                os.system('')
                success = False

        # Set UTF-8 code page for Unicode support
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        except Exception:
            pass

    # Set UTF-8 encoding for stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    _terminal_initialized = True
    return success


def cleanup_terminal():
    """Clean up terminal settings on exit."""
    if is_windows():
        try:
            import colorama
            colorama.deinit()
        except ImportError:
            pass


# =============================================================================
# TERMINAL CAPABILITIES
# =============================================================================

def get_terminal_size(fallback: Tuple[int, int] = (80, 24)) -> Tuple[int, int]:
    """Get terminal width and height."""
    try:
        size = shutil.get_terminal_size(fallback)
        return (size.columns, size.lines)
    except Exception:
        return fallback


def supports_color() -> bool:
    """Check if terminal supports ANSI colors."""
    # Check for NO_COLOR environment variable (standard)
    if os.environ.get('NO_COLOR'):
        return False

    # Check for FORCE_COLOR
    if os.environ.get('FORCE_COLOR'):
        return True

    # Check for dumb terminal
    if os.environ.get('TERM') == 'dumb':
        return False

    # Check if stdout is a TTY
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False

    # Windows: Check for Windows Terminal, ConEmu, or Windows 10+
    if is_windows():
        # Windows Terminal and ConEmu support colors
        if os.environ.get('WT_SESSION') or os.environ.get('ConEmuANSI'):
            return True
        # Windows 10 build 14393+ supports VT100
        try:
            version = platform.version()
            build = int(version.split('.')[-1])
            return build >= 14393
        except Exception:
            return True  # Assume modern Windows

    return True  # Unix systems generally support color


def supports_unicode() -> bool:
    """Check if terminal supports Unicode characters."""
    # Check encoding
    encoding = getattr(sys.stdout, 'encoding', '') or ''
    if encoding.lower().replace('-', '') in ('utf8', 'utf16', 'utf32'):
        return True

    # Check LANG environment variable
    lang = os.environ.get('LANG', '') + os.environ.get('LC_ALL', '')
    if 'utf' in lang.lower():
        return True

    # Windows Terminal supports Unicode
    if is_windows() and os.environ.get('WT_SESSION'):
        return True

    return False


def get_safe_characters() -> Dict[str, str]:
    """
    Get safe characters for the current terminal.
    Returns Unicode if supported, ASCII fallback otherwise.
    """
    if supports_unicode():
        return {
            'box_h': '─',
            'box_v': '│',
            'box_tl': '┌',
            'box_tr': '┐',
            'box_bl': '└',
            'box_br': '┘',
            'box_cross': '┼',
            'box_t_down': '┬',
            'box_t_up': '┴',
            'box_t_right': '├',
            'box_t_left': '┤',
            'progress_full': '█',
            'progress_empty': '░',
            'progress_half': '▓',
            'arrow_up': '↑',
            'arrow_down': '↓',
            'arrow_left': '←',
            'arrow_right': '→',
            'check': '✓',
            'cross': '✗',
            'bullet': '•',
            'star': '★',
            'heart': '♥',
        }
    else:
        return {
            'box_h': '-',
            'box_v': '|',
            'box_tl': '+',
            'box_tr': '+',
            'box_bl': '+',
            'box_br': '+',
            'box_cross': '+',
            'box_t_down': '+',
            'box_t_up': '+',
            'box_t_right': '+',
            'box_t_left': '+',
            'progress_full': '#',
            'progress_empty': '.',
            'progress_half': '=',
            'arrow_up': '^',
            'arrow_down': 'v',
            'arrow_left': '<',
            'arrow_right': '>',
            'check': 'Y',
            'cross': 'X',
            'bullet': '*',
            'star': '*',
            'heart': '<3',
        }


# =============================================================================
# SCREEN CONTROL
# =============================================================================

def clear_screen():
    """
    Clear the terminal screen using ANSI escape sequences.
    This is faster and more reliable than os.system('clear'/'cls').
    Works on all modern terminals including Windows 10+ Terminal.
    """
    # Use ANSI escape sequence - works on all modern terminals
    # \033[2J clears the screen, \033[H moves cursor to top-left
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()


def move_cursor(x: int, y: int):
    """Move cursor to position (x, y). 1-indexed."""
    print(f'\033[{y};{x}H', end='', flush=True)


def hide_cursor():
    """Hide the terminal cursor."""
    print('\033[?25l', end='', flush=True)


def show_cursor():
    """Show the terminal cursor."""
    print('\033[?25h', end='', flush=True)


def set_title(title: str):
    """Set the terminal window title."""
    if is_windows():
        os.system(f'title {title}')
    else:
        print(f'\033]0;{title}\007', end='', flush=True)


# =============================================================================
# COLOR SUPPORT
# =============================================================================

class Colors:
    """
    Cross-platform ANSI color codes with fallback support.
    Use Colors.init() to check color support before using.
    """

    _enabled = None

    # Reset
    RESET = '\033[0m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Standard colors (foreground)
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors (foreground)
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    @classmethod
    def init(cls) -> bool:
        """Initialize colors and check support. Returns True if colors are supported."""
        if cls._enabled is None:
            init_terminal()
            cls._enabled = supports_color()

            if not cls._enabled:
                # Disable all colors
                for attr in dir(cls):
                    if attr.isupper() and not attr.startswith('_'):
                        setattr(cls, attr, '')

        return cls._enabled

    @classmethod
    def is_enabled(cls) -> bool:
        """Check if colors are enabled."""
        if cls._enabled is None:
            cls.init()
        return cls._enabled

    @classmethod
    def rgb(cls, r: int, g: int, b: int, background: bool = False) -> str:
        """Generate 24-bit true color code."""
        if not cls.is_enabled():
            return ''
        prefix = 48 if background else 38
        return f'\033[{prefix};2;{r};{g};{b}m'

    @classmethod
    def color256(cls, code: int, background: bool = False) -> str:
        """Generate 256-color code."""
        if not cls.is_enabled():
            return ''
        prefix = 48 if background else 38
        return f'\033[{prefix};5;{code}m'


# =============================================================================
# PATH UTILITIES
# =============================================================================

def get_app_data_dir(app_name: str = "vault13") -> Path:
    """
    Get the platform-appropriate application data directory.
    Creates the directory if it doesn't exist.
    """
    if is_windows():
        # Windows: %APPDATA%/app_name or %LOCALAPPDATA%/app_name
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    elif is_macos():
        # macOS: ~/Library/Application Support/app_name
        base = Path.home() / 'Library' / 'Application Support'
    else:
        # Linux/Unix: ~/.local/share/app_name (XDG standard)
        xdg_data = os.environ.get('XDG_DATA_HOME', '')
        if xdg_data:
            base = Path(xdg_data)
        else:
            base = Path.home() / '.local' / 'share'

    app_dir = base / app_name
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_config_dir(app_name: str = "vault13") -> Path:
    """
    Get the platform-appropriate configuration directory.
    Creates the directory if it doesn't exist.
    """
    if is_windows():
        # Windows: Same as app data
        return get_app_data_dir(app_name)
    elif is_macos():
        # macOS: ~/Library/Preferences/app_name or same as app data
        base = Path.home() / 'Library' / 'Application Support'
    else:
        # Linux/Unix: ~/.config/app_name (XDG standard)
        xdg_config = os.environ.get('XDG_CONFIG_HOME', '')
        if xdg_config:
            base = Path(xdg_config)
        else:
            base = Path.home() / '.config'

    config_dir = base / app_name
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_save_dir(app_name: str = "vault13") -> Path:
    """Get the directory for save files."""
    save_dir = get_app_data_dir(app_name) / 'saves'
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def get_log_dir(app_name: str = "vault13") -> Path:
    """Get the directory for log files."""
    log_dir = get_app_data_dir(app_name) / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_cache_dir(app_name: str = "vault13") -> Path:
    """Get the platform-appropriate cache directory."""
    if is_windows():
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    elif is_macos():
        base = Path.home() / 'Library' / 'Caches'
    else:
        xdg_cache = os.environ.get('XDG_CACHE_HOME', '')
        if xdg_cache:
            base = Path(xdg_cache)
        else:
            base = Path.home() / '.cache'

    cache_dir = base / app_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_game_root() -> Path:
    """Get the root directory containing all game files."""
    # First check if we're running from source
    script_dir = Path(__file__).parent.resolve()

    # Check if this looks like the game directory
    if (script_dir / 'vault_shelter_v6.py').exists():
        return script_dir

    # Check if we're in a subdirectory
    parent = script_dir.parent
    if (parent / 'vault_shelter_v6.py').exists():
        return parent

    # Fall back to current working directory
    cwd = Path.cwd()
    if (cwd / 'vault_shelter_v6.py').exists():
        return cwd

    # Last resort: return the script directory
    return script_dir


# =============================================================================
# INPUT HANDLING
# =============================================================================

def get_key() -> str:
    """
    Get a single keypress from the user (non-blocking on Unix, blocking on Windows).
    Returns the key as a string.
    """
    if is_windows():
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # Handle special keys
            if key in (b'\x00', b'\xe0'):
                key = msvcrt.getch()
                # Map arrow keys
                mapping = {
                    b'H': 'UP', b'P': 'DOWN',
                    b'K': 'LEFT', b'M': 'RIGHT',
                }
                return mapping.get(key, '')
            return key.decode('utf-8', errors='replace')
        return ''
    else:
        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Check if input is available
            if select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                # Handle escape sequences (arrow keys, etc.)
                if key == '\x1b':
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key += sys.stdin.read(2)
                        mapping = {
                            '\x1b[A': 'UP', '\x1b[B': 'DOWN',
                            '\x1b[C': 'RIGHT', '\x1b[D': 'LEFT',
                        }
                        return mapping.get(key, key)
                return key
            return ''
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def wait_for_key() -> str:
    """Wait for a keypress and return it."""
    if is_windows():
        import msvcrt
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()
            mapping = {
                b'H': 'UP', b'P': 'DOWN',
                b'K': 'LEFT', b'M': 'RIGHT',
            }
            return mapping.get(key, '')
        return key.decode('utf-8', errors='replace')
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if key == '\x1b':
                key += sys.stdin.read(2)
                mapping = {
                    '\x1b[A': 'UP', '\x1b[B': 'DOWN',
                    '\x1b[C': 'RIGHT', '\x1b[D': 'LEFT',
                }
                return mapping.get(key, key)
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# =============================================================================
# SYSTEM UTILITIES
# =============================================================================

def get_python_executable() -> str:
    """Get the path to the Python executable."""
    return sys.executable


def get_system_info() -> Dict[str, Any]:
    """Get system information for debugging."""
    return {
        'platform': get_platform().value,
        'python_version': platform.python_version(),
        'os_name': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'machine': platform.machine(),
        'terminal_size': get_terminal_size(),
        'supports_color': supports_color(),
        'supports_unicode': supports_unicode(),
        'encoding': getattr(sys.stdout, 'encoding', 'unknown'),
    }


def open_file_explorer(path: Path):
    """Open the system file explorer at the given path."""
    import subprocess

    path = Path(path)
    if not path.exists():
        path = path.parent

    if is_windows():
        os.startfile(str(path))
    elif is_macos():
        subprocess.run(['open', str(path)])
    else:
        # Try common Linux file managers
        for cmd in ['xdg-open', 'nautilus', 'dolphin', 'thunar']:
            if shutil.which(cmd):
                subprocess.run([cmd, str(path)])
                break


# =============================================================================
# INITIALIZATION
# =============================================================================

def initialize() -> Dict[str, Any]:
    """
    Initialize all cross-platform utilities.
    Call this at the start of your application.
    Returns system info dict.
    """
    init_terminal()
    Colors.init()
    return get_system_info()


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == '__main__':
    print("Cross-Platform Utilities Test")
    print("=" * 40)

    info = initialize()

    print(f"\nPlatform: {info['platform']}")
    print(f"Python: {info['python_version']}")
    print(f"OS: {info['os_name']} {info['os_release']}")
    print(f"Terminal: {info['terminal_size'][0]}x{info['terminal_size'][1]}")
    print(f"Color support: {info['supports_color']}")
    print(f"Unicode support: {info['supports_unicode']}")

    print(f"\nApp data dir: {get_app_data_dir()}")
    print(f"Config dir: {get_config_dir()}")
    print(f"Save dir: {get_save_dir()}")
    print(f"Game root: {get_game_root()}")

    if Colors.is_enabled():
        print(f"\n{Colors.GREEN}Color test:{Colors.RESET}")
        print(f"  {Colors.RED}Red{Colors.RESET} {Colors.GREEN}Green{Colors.RESET} {Colors.BLUE}Blue{Colors.RESET}")
        print(f"  {Colors.BOLD}Bold{Colors.RESET} {Colors.DIM}Dim{Colors.RESET} {Colors.UNDERLINE}Underline{Colors.RESET}")
        print(f"  {Colors.color256(208)}256-color (208){Colors.RESET}")

    chars = get_safe_characters()
    print(f"\nBox characters: {chars['box_tl']}{chars['box_h']*5}{chars['box_tr']}")
    print(f"Progress: {chars['progress_full']*5}{chars['progress_empty']*5}")
    print(f"Arrows: {chars['arrow_up']} {chars['arrow_down']} {chars['arrow_left']} {chars['arrow_right']}")
