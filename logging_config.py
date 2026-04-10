#!/usr/bin/env python3
"""
Logging Configuration Module
=============================
Centralized logging setup for all games.
Provides structured logging with rotation and proper formatting.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

try:
    from platform_utils import get_log_dir
except ImportError:
    # Fallback if platform_utils not available
    def get_log_dir(app_name: str = "vault13") -> Path:
        return Path.home() / f'.{app_name}' / 'logs'

# =============================================================================
# LOGGING LEVELS
# =============================================================================

LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

# =============================================================================
# CUSTOM FORMATTER
# =============================================================================

class ColoredFormatter(logging.Formatter):
    """Colored formatter for terminal output"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[38;5;243m',      # Gray
        'INFO': '\033[38;5;87m',        # Cyan
        'WARNING': '\033[38;5;226m',    # Yellow
        'ERROR': '\033[38;5;203m',      # Red
        'CRITICAL': '\033[38;5;196m',   # Bright Red
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'

    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{self.BOLD}{levelname}{self.RESET}"

        # Format the message
        result = super().format(record)

        # Reset levelname for next use
        record.levelname = levelname

        return result


class GameLogFilter(logging.Filter):
    """Filter to add game-specific context"""

    def __init__(self, game_name: str = "unknown"):
        super().__init__()
        self.game_name = game_name

    def filter(self, record):
        record.game_name = self.game_name
        return True


# =============================================================================
# LOGGER SETUP
# =============================================================================

def setup_logger(
    name: str = "vault13",
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True,
    colored_console: bool = True,
    max_bytes: int = 10_000_000,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        name: Logger name (usually module name or game name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to file
        log_to_console: Whether to log to console
        colored_console: Use colored output for console
        max_bytes: Max size of log file before rotation
        backup_count: Number of backup log files to keep

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL_MAP.get(level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # File handler with rotation
    if log_to_file:
        try:
            log_dir = get_log_dir()
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / f"{name}.log"

            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )

            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(logging.DEBUG)  # File gets everything
            logger.addHandler(file_handler)

        except (IOError, OSError) as e:
            print(f"Warning: Could not set up file logging: {e}", file=sys.stderr)

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)

        if colored_console and sys.stdout.isatty():
            console_formatter = ColoredFormatter(
                '%(levelname)s | %(name)s | %(message)s'
            )
        else:
            console_formatter = logging.Formatter(
                '%(levelname)-8s | %(name)s | %(message)s'
            )

        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(LEVEL_MAP.get(level.upper(), logging.INFO))
        logger.addHandler(console_handler)

    return logger


def setup_game_logger(game_name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger for a specific game with game context.

    Args:
        game_name: Name of the game (e.g., "echo_chambers", "vault_shelter")
        level: Logging level

    Returns:
        Configured logger with game context
    """
    logger = setup_logger(
        name=game_name,
        level=level,
        log_to_file=True,
        log_to_console=True,
        colored_console=True
    )

    # Add game-specific filter
    game_filter = GameLogFilter(game_name)
    for handler in logger.handlers:
        handler.addFilter(game_filter)

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance. If logger doesn't exist, creates one with defaults.

    Args:
        name: Logger name (uses calling module name if None)

    Returns:
        Logger instance
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')

    logger = logging.getLogger(name)

    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        setup_logger(name)

    return logger


# =============================================================================
# PERFORMANCE LOGGING
# =============================================================================

import functools
import time

def log_performance(logger: logging.Logger = None, threshold: float = 0.1):
    """
    Decorator to log function performance.
    Logs warning if function takes longer than threshold.

    Args:
        logger: Logger to use (creates one if None)
        threshold: Time threshold in seconds
    """
    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = get_logger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.perf_counter() - start_time
                if duration > threshold:
                    logger.warning(
                        f"Slow function: {func.__name__} took {duration:.3f}s "
                        f"(threshold: {threshold}s)"
                    )
                else:
                    logger.debug(f"{func.__name__} took {duration:.3f}s")

        return wrapper
    return decorator


def log_exceptions(logger: logging.Logger = None):
    """
    Decorator to log exceptions with full traceback.

    Args:
        logger: Logger to use (creates one if None)
    """
    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = get_logger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    f"Exception in {func.__name__}: {e}",
                    exc_info=True
                )
                raise

        return wrapper
    return decorator


# =============================================================================
# CONTEXT MANAGERS
# =============================================================================

from contextlib import contextmanager

@contextmanager
def log_context(logger: logging.Logger, operation: str, level: str = "INFO"):
    """
    Context manager for logging operation start/end.

    Usage:
        with log_context(logger, "Loading game"):
            # ... load game
    """
    log_level = LEVEL_MAP.get(level.upper(), logging.INFO)
    logger.log(log_level, f"Starting: {operation}")
    start_time = time.perf_counter()

    try:
        yield
        duration = time.perf_counter() - start_time
        logger.log(log_level, f"Completed: {operation} ({duration:.3f}s)")
    except Exception as e:
        duration = time.perf_counter() - start_time
        logger.error(f"Failed: {operation} ({duration:.3f}s) - {e}")
        raise


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_old_logs(days: int = 7):
    """Delete log files older than specified days"""
    try:
        log_dir = get_log_dir()
        if not log_dir.exists():
            return

        cutoff = datetime.now().timestamp() - (days * 86400)
        count = 0

        for log_file in log_dir.glob('*.log*'):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
                count += 1

        if count > 0:
            logger = get_logger(__name__)
            logger.info(f"Cleaned up {count} old log files")

    except (IOError, OSError) as e:
        print(f"Warning: Failed to clean old logs: {e}", file=sys.stderr)


def get_log_size() -> int:
    """Get total size of all log files in bytes"""
    try:
        log_dir = get_log_dir()
        if not log_dir.exists():
            return 0

        total_size = sum(f.stat().st_size for f in log_dir.glob('*.log*'))
        return total_size
    except (IOError, OSError):
        return 0


def format_log_size() -> str:
    """Get formatted string of total log size"""
    size = get_log_size()

    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} TB"


# =============================================================================
# DEFAULT LOGGER
# =============================================================================

# Create default logger for this module
default_logger = setup_logger("vault13")


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    # Test the logging system
    print("Testing Logging Configuration")
    print("=" * 60)

    # Create test logger
    test_logger = setup_game_logger("test_game", level="DEBUG")

    # Test all log levels
    test_logger.debug("This is a DEBUG message")
    test_logger.info("This is an INFO message")
    test_logger.warning("This is a WARNING message")
    test_logger.error("This is an ERROR message")
    test_logger.critical("This is a CRITICAL message")

    print()
    print("Testing performance logging:")

    @log_performance(test_logger, threshold=0.01)
    def slow_function():
        """Simulated slow function"""
        time.sleep(0.05)
        return "done"

    @log_performance(test_logger, threshold=0.1)
    def fast_function():
        """Simulated fast function"""
        time.sleep(0.001)
        return "done"

    slow_function()  # Should log warning
    fast_function()  # Should not log warning

    print()
    print("Testing exception logging:")

    @log_exceptions(test_logger)
    def failing_function():
        """Function that raises exception"""
        raise ValueError("Test exception")

    try:
        failing_function()
    except ValueError:
        print("Exception caught (and logged)")

    print()
    print("Testing context manager:")

    with log_context(test_logger, "Test operation"):
        time.sleep(0.01)

    print()
    print(f"Log directory: {get_log_dir()}")
    print(f"Total log size: {format_log_size()}")
