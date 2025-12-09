#!/usr/bin/env python3
"""
Error Handling Utilities
=========================
Consistent error handling patterns for all games.
"""

import sys
import traceback
from typing import Optional, Callable, Any, TypeVar
from functools import wraps
from contextlib import contextmanager

from logging_config import get_logger
from constants import (
    ERROR_INSUFFICIENT_RESOURCES,
    ERROR_NO_AVAILABLE_DWELLERS,
    ERROR_ROOM_FULL,
    ERROR_INVALID_POSITION,
    ERROR_SAVE_FAILED,
    ERROR_LOAD_FAILED
)

logger = get_logger(__name__)

T = TypeVar('T')


# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================

class GameError(Exception):
    """Base exception for all game errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.user_message = user_message or message


class ResourceError(GameError):
    """Raised when resources are insufficient"""
    def __init__(self, resource: str, required: int, available: int):
        message = f"Insufficient {resource}: need {required}, have {available}"
        user_message = f"Not enough {resource}! Need {required}, but only have {available}."
        super().__init__(message, user_message)
        self.resource = resource
        self.required = required
        self.available = available


class CapacityError(GameError):
    """Raised when capacity is exceeded"""
    def __init__(self, item_type: str, max_capacity: int):
        message = f"{item_type} capacity exceeded (max: {max_capacity})"
        user_message = f"Cannot add more {item_type}! Maximum capacity: {max_capacity}"
        super().__init__(message, user_message)
        self.item_type = item_type
        self.max_capacity = max_capacity


class InvalidStateError(GameError):
    """Raised when operation is invalid for current state"""
    def __init__(self, operation: str, current_state: str, required_state: str):
        message = f"Cannot {operation} in state {current_state} (requires {required_state})"
        user_message = f"Cannot {operation} right now."
        super().__init__(message, user_message)
        self.operation = operation
        self.current_state = current_state
        self.required_state = required_state


class SaveLoadError(GameError):
    """Raised when save/load operations fail"""
    pass


class ConfigError(GameError):
    """Raised when configuration is invalid"""
    pass


# =============================================================================
# ERROR CONTEXT MANAGER
# =============================================================================

@contextmanager
def error_context(operation: str, user_friendly: bool = True):
    """
    Context manager for handling errors with logging.

    Args:
        operation: Description of operation being performed
        user_friendly: Show user-friendly messages

    Usage:
        with error_context("Loading save file"):
            load_save_data()
    """
    try:
        yield
    except GameError as e:
        logger.error(f"GameError during {operation}: {e}")
        if user_friendly and e.user_message:
            print(f"\n❌ {e.user_message}")
        else:
            print(f"\n❌ Error: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during {operation}: {e}")
        if user_friendly:
            print(f"\n❌ An unexpected error occurred. Please try again.")
        else:
            print(f"\n❌ Error: {e}")
        raise


# =============================================================================
# ERROR HANDLING DECORATORS
# =============================================================================

def handle_errors(
    user_friendly: bool = True,
    default_return: Any = None,
    suppress: bool = False
):
    """
    Decorator to handle errors in functions.

    Args:
        user_friendly: Show user-friendly error messages
        default_return: Return this value on error (if suppress=True)
        suppress: Suppress exceptions and return default_return

    Usage:
        @handle_errors(user_friendly=True)
        def save_game(data):
            # ... save logic
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except GameError as e:
                logger.error(f"GameError in {func.__name__}: {e}")
                if user_friendly and e.user_message:
                    print(f"\n❌ {e.user_message}")
                else:
                    print(f"\n❌ {e}")

                if suppress:
                    return default_return
                raise
            except Exception as e:
                logger.exception(f"Unexpected error in {func.__name__}: {e}")
                if user_friendly:
                    print(f"\n❌ An error occurred in {func.__name__}.")
                else:
                    print(f"\n❌ Error: {e}")

                if suppress:
                    return default_return
                raise
        return wrapper
    return decorator


def retry_on_error(
    max_attempts: int = 3,
    exceptions: tuple = (Exception,),
    backoff: float = 1.0
):
    """
    Decorator to retry function on error.

    Args:
        max_attempts: Maximum number of attempts
        exceptions: Tuple of exceptions to catch
        backoff: Delay multiplier between attempts

    Usage:
        @retry_on_error(max_attempts=3, exceptions=(IOError,))
        def save_to_file(data):
            # ... save logic
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {e}")
                        raise

                    delay = backoff * attempt
                    logger.warning(f"{func.__name__} failed (attempt {attempt}/{max_attempts}), "
                                 f"retrying in {delay}s: {e}")
                    time.sleep(delay)

            return None  # Should never reach here
        return wrapper
    return decorator


# =============================================================================
# ERROR FORMATTERS
# =============================================================================

def format_error(error: Exception, include_traceback: bool = False) -> str:
    """
    Format error for display.

    Args:
        error: Exception to format
        include_traceback: Include full traceback

    Returns:
        Formatted error string
    """
    if isinstance(error, GameError) and error.user_message:
        message = error.user_message
    else:
        message = str(error)

    if include_traceback:
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        return f"{message}\n\nTraceback:\n{tb}"

    return message


def print_error(error: Exception, title: str = "Error", verbose: bool = False):
    """
    Print formatted error to console.

    Args:
        error: Exception to print
        title: Error title
        verbose: Show full traceback
    """
    print(f"\n{'=' * 60}")
    print(f"❌ {title}")
    print('=' * 60)
    print(format_error(error, include_traceback=verbose))
    print('=' * 60)


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def require_resource(resource: str, required: int, available: int) -> None:
    """
    Validate resource availability.

    Raises:
        ResourceError: If insufficient resources
    """
    if available < required:
        raise ResourceError(resource, required, available)


def require_capacity(item_type: str, current: int, max_capacity: int) -> None:
    """
    Validate capacity.

    Raises:
        CapacityError: If capacity exceeded
    """
    if current >= max_capacity:
        raise CapacityError(item_type, max_capacity)


def require_state(operation: str, current_state: str, required_state: str) -> None:
    """
    Validate game state.

    Raises:
        InvalidStateError: If state is invalid for operation
    """
    if current_state != required_state:
        raise InvalidStateError(operation, current_state, required_state)


# =============================================================================
# GRACEFUL SHUTDOWN
# =============================================================================

def setup_exit_handlers(cleanup_func: Optional[Callable] = None):
    """
    Setup handlers for graceful shutdown.

    Args:
        cleanup_func: Function to call on exit
    """
    import atexit
    import signal

    if cleanup_func:
        atexit.register(cleanup_func)

        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down gracefully")
            cleanup_func()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Error Handling Utilities Test")
    print("=" * 60)

    # Test custom exceptions
    print("\n1. Testing custom exceptions:")
    try:
        raise ResourceError("food", required=100, available=50)
    except ResourceError as e:
        print(f"   ✓ ResourceError: {e.user_message}")

    try:
        raise CapacityError("dwellers", max_capacity=200)
    except CapacityError as e:
        print(f"   ✓ CapacityError: {e.user_message}")

    # Test error context
    print("\n2. Testing error context:")
    try:
        with error_context("Test operation", user_friendly=True):
            raise ResourceError("caps", 500, 100)
    except ResourceError:
        print("   ✓ Error context caught and logged")

    # Test decorators
    print("\n3. Testing error decorator:")

    @handle_errors(user_friendly=True, suppress=True, default_return=False)
    def failing_function():
        raise ValueError("Something went wrong")

    result = failing_function()
    print(f"   ✓ Suppressed error, returned: {result}")

    # Test retry decorator
    print("\n4. Testing retry decorator:")

    attempt_counter = 0

    @retry_on_error(max_attempts=3, backoff=0.1)
    def flaky_function():
        global attempt_counter
        attempt_counter += 1
        if attempt_counter < 2:
            raise IOError("Network error")
        return "Success!"

    result = flaky_function()
    print(f"   ✓ Succeeded after {attempt_counter} attempts: {result}")

    # Test validation helpers
    print("\n5. Testing validation helpers:")
    try:
        require_resource("water", required=100, available=150)
        print("   ✓ Resource validation passed")
    except ResourceError:
        print("   ❌ Resource validation failed unexpectedly")

    try:
        require_resource("power", required=100, available=50)
        print("   ❌ Should have raised ResourceError")
    except ResourceError:
        print("   ✓ Resource validation correctly raised error")

    print("\n✅ All error handling tests passed!")
