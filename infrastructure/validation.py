#!/usr/bin/env python3
"""
Input Validation Module
=======================
Robust input validation for all games.
Handles common validation patterns with clear error messages.
"""

import re
from typing import Optional, List, Callable, Any, TypeVar, Union
from enum import Enum

from constants import (
    STAT_MIN, STAT_MAX,
    HAPPINESS_MIN, HAPPINESS_MAX,
    validate_stat
)

T = TypeVar('T')


class ValidationError(Exception):
    """Raised when input validation fails"""
    pass


# =============================================================================
# NUMERIC VALIDATION
# =============================================================================

def validate_int(
    value: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    error_msg: Optional[str] = None
) -> int:
    """
    Validate and convert string to integer with range checking.

    Args:
        value: String to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        error_msg: Custom error message

    Returns:
        Validated integer

    Raises:
        ValidationError: If validation fails
    """
    try:
        num = int(value.strip())
    except ValueError:
        msg = error_msg or f"'{value}' is not a valid number"
        raise ValidationError(msg)

    if min_value is not None and num < min_value:
        msg = error_msg or f"Value must be at least {min_value} (got {num})"
        raise ValidationError(msg)

    if max_value is not None and num > max_value:
        msg = error_msg or f"Value must be at most {max_value} (got {num})"
        raise ValidationError(msg)

    return num


def validate_float(
    value: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    error_msg: Optional[str] = None
) -> float:
    """Validate and convert string to float with range checking"""
    try:
        num = float(value.strip())
    except ValueError:
        msg = error_msg or f"'{value}' is not a valid number"
        raise ValidationError(msg)

    if min_value is not None and num < min_value:
        msg = error_msg or f"Value must be at least {min_value} (got {num})"
        raise ValidationError(msg)

    if max_value is not None and num > max_value:
        msg = error_msg or f"Value must be at most {max_value} (got {num})"
        raise ValidationError(msg)

    return num


def validate_choice(
    value: str,
    choices: List[Any],
    case_sensitive: bool = False,
    error_msg: Optional[str] = None
) -> Any:
    """
    Validate that input is one of allowed choices.

    Args:
        value: User input
        choices: List of valid choices
        case_sensitive: Whether to match case exactly
        error_msg: Custom error message

    Returns:
        Matched choice from the list

    Raises:
        ValidationError: If input doesn't match any choice
    """
    value = value.strip()

    if not case_sensitive:
        value_lower = value.lower()
        for choice in choices:
            if str(choice).lower() == value_lower:
                return choice
    else:
        if value in [str(c) for c in choices]:
            return value

    # Not found
    choices_str = ", ".join(str(c) for c in choices)
    msg = error_msg or f"Invalid choice. Must be one of: {choices_str}"
    raise ValidationError(msg)


# =============================================================================
# STRING VALIDATION
# =============================================================================

def validate_string(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    allow_empty: bool = False,
    error_msg: Optional[str] = None
) -> str:
    """
    Validate string with length and pattern checking.

    Args:
        value: String to validate
        min_length: Minimum length
        max_length: Maximum length
        pattern: Regex pattern to match
        allow_empty: Whether empty strings are allowed
        error_msg: Custom error message

    Returns:
        Validated string

    Raises:
        ValidationError: If validation fails
    """
    value = value.strip()

    if not allow_empty and not value:
        msg = error_msg or "Input cannot be empty"
        raise ValidationError(msg)

    if min_length is not None and len(value) < min_length:
        msg = error_msg or f"Input must be at least {min_length} characters (got {len(value)})"
        raise ValidationError(msg)

    if max_length is not None and len(value) > max_length:
        msg = error_msg or f"Input must be at most {max_length} characters (got {len(value)})"
        raise ValidationError(msg)

    if pattern is not None and not re.match(pattern, value):
        msg = error_msg or f"Input doesn't match required pattern: {pattern}"
        raise ValidationError(msg)

    return value


def validate_name(value: str, max_length: int = 20) -> str:
    """Validate a name (letters, spaces, hyphens only)"""
    return validate_string(
        value,
        min_length=1,
        max_length=max_length,
        pattern=r'^[a-zA-Z][a-zA-Z\s\-]*$',
        error_msg="Name must contain only letters, spaces, and hyphens"
    )


# =============================================================================
# BOOLEAN VALIDATION
# =============================================================================

def validate_bool(value: str, error_msg: Optional[str] = None) -> bool:
    """
    Validate boolean input.
    Accepts: y/yes/true/1 for True, n/no/false/0 for False
    """
    value_lower = value.strip().lower()

    if value_lower in ('y', 'yes', 'true', '1'):
        return True
    elif value_lower in ('n', 'no', 'false', '0'):
        return False
    else:
        msg = error_msg or "Please enter yes/no (y/n)"
        raise ValidationError(msg)


# =============================================================================
# INTERACTIVE INPUT WITH VALIDATION
# =============================================================================

def get_validated_input(
    prompt: str,
    validator: Callable[[str], T],
    max_attempts: int = 3,
    default: Optional[T] = None
) -> Optional[T]:
    """
    Get input with validation and retry logic.

    Args:
        prompt: Prompt to show user
        validator: Function that validates and transforms input
        max_attempts: Maximum retry attempts
        default: Default value if input is empty (None = no default)

    Returns:
        Validated input or default, None if user exhausted attempts

    Example:
        age = get_validated_input(
            "Enter age: ",
            lambda x: validate_int(x, 0, 120),
            max_attempts=3
        )
    """
    for attempt in range(max_attempts):
        try:
            user_input = input(prompt).strip()

            # Check for default
            if not user_input and default is not None:
                return default

            # Validate
            return validator(user_input)

        except ValidationError as e:
            remaining = max_attempts - attempt - 1
            print(f"❌ {e}")
            if remaining > 0:
                print(f"   ({remaining} attempts remaining)")
            else:
                print("   Maximum attempts exceeded.")

        except (KeyboardInterrupt, EOFError):
            print("\n(Input cancelled)")
            return None

    return None


def get_int_input(
    prompt: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    default: Optional[int] = None
) -> Optional[int]:
    """Get validated integer input"""
    return get_validated_input(
        prompt,
        lambda x: validate_int(x, min_value, max_value),
        default=default
    )


def get_choice_input(
    prompt: str,
    choices: List[Any],
    case_sensitive: bool = False,
    default: Optional[Any] = None
) -> Optional[Any]:
    """Get validated choice input"""
    return get_validated_input(
        prompt,
        lambda x: validate_choice(x, choices, case_sensitive),
        default=default
    )


def get_yes_no_input(prompt: str, default: Optional[bool] = None) -> Optional[bool]:
    """Get yes/no input"""
    if default is not None:
        hint = "[Y/n]" if default else "[y/N]"
        prompt = f"{prompt} {hint}: "
    else:
        prompt = f"{prompt} [y/n]: "

    return get_validated_input(
        prompt,
        validate_bool,
        default=default
    )


# =============================================================================
# MENU VALIDATION
# =============================================================================

def validate_menu_choice(
    value: str,
    num_options: int,
    allow_zero: bool = True,
    error_msg: Optional[str] = None
) -> int:
    """
    Validate menu choice (1-N or 0 for back/exit).

    Args:
        value: User input
        num_options: Number of menu options
        allow_zero: Whether 0 is valid (for back/exit)
        error_msg: Custom error message

    Returns:
        Validated choice as integer

    Raises:
        ValidationError: If choice is invalid
    """
    try:
        choice = int(value.strip())
    except ValueError:
        msg = error_msg or "Please enter a number"
        raise ValidationError(msg)

    min_val = 0 if allow_zero else 1

    if choice < min_val or choice > num_options:
        if allow_zero:
            msg = error_msg or f"Please choose 0-{num_options}"
        else:
            msg = error_msg or f"Please choose 1-{num_options}"
        raise ValidationError(msg)

    return choice


def get_menu_choice(
    options: List[str],
    prompt: str = "Choose an option: ",
    allow_back: bool = True,
    title: Optional[str] = None
) -> Optional[int]:
    """
    Display menu and get validated choice.

    Args:
        options: List of menu options
        prompt: Input prompt
        allow_back: Show "0 - Back" option
        title: Optional menu title

    Returns:
        Choice index (1-N) or 0 for back, None if cancelled

    Example:
        choice = get_menu_choice(
            ["New Game", "Load Game", "Settings"],
            title="Main Menu"
        )
        if choice == 1:
            new_game()
        elif choice == 0:
            return
    """
    # Display menu
    if title:
        print(f"\n{'═' * 50}")
        print(f"{title.center(50)}")
        print(f"{'═' * 50}\n")

    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    if allow_back:
        print(f"  0. Back")

    print()

    # Get choice
    return get_validated_input(
        prompt,
        lambda x: validate_menu_choice(x, len(options), allow_back),
        max_attempts=3
    )


# =============================================================================
# GAME-SPECIFIC VALIDATORS
# =============================================================================

def validate_stat_input(value: str) -> int:
    """Validate SPECIAL stat (1-10)"""
    return validate_int(value, STAT_MIN, STAT_MAX,
                       f"Stat must be between {STAT_MIN} and {STAT_MAX}")


def validate_happiness_input(value: str) -> float:
    """Validate happiness value (0-100)"""
    return validate_float(value, HAPPINESS_MIN, HAPPINESS_MAX,
                         f"Happiness must be between {HAPPINESS_MIN} and {HAPPINESS_MAX}")


def validate_resource_amount(value: str, max_capacity: int = 1000) -> int:
    """Validate resource amount (0 to capacity)"""
    return validate_int(value, 0, max_capacity,
                       f"Amount must be between 0 and {max_capacity}")


def validate_dweller_id(value: str, max_dwellers: int) -> int:
    """Validate dweller ID"""
    return validate_int(value, 0, max_dwellers - 1,
                       f"Dweller ID must be between 0 and {max_dwellers - 1}")


# =============================================================================
# BATCH VALIDATION
# =============================================================================

def validate_all(validations: List[tuple]) -> List[Any]:
    """
    Run multiple validations and collect all errors.

    Args:
        validations: List of (value, validator, name) tuples

    Returns:
        List of validated values

    Raises:
        ValidationError: With all error messages combined

    Example:
        results = validate_all([
            (name_input, validate_name, "Name"),
            (age_input, lambda x: validate_int(x, 0, 120), "Age"),
        ])
    """
    errors = []
    results = []

    for value, validator, name in validations:
        try:
            results.append(validator(value))
        except ValidationError as e:
            errors.append(f"{name}: {e}")

    if errors:
        raise ValidationError("\n".join(errors))

    return results


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Input Validation Module Test")
    print("=" * 60)

    # Test integer validation
    print("\n1. Integer Validation:")
    try:
        print(f"  validate_int('5', 1, 10) = {validate_int('5', 1, 10)}")
        print(f"  validate_int('15', 1, 10) = ...", end=" ")
        validate_int('15', 1, 10)
    except ValidationError as e:
        print(f"✓ ValidationError: {e}")

    # Test choice validation
    print("\n2. Choice Validation:")
    choices = ['red', 'green', 'blue']
    print(f"  validate_choice('RED', {choices}) = {validate_choice('RED', choices)}")

    # Test string validation
    print("\n3. String Validation:")
    print(f"  validate_name('John Doe') = {validate_name('John Doe')}")

    # Test boolean
    print("\n4. Boolean Validation:")
    print(f"  validate_bool('y') = {validate_bool('y')}")
    print(f"  validate_bool('no') = {validate_bool('no')}")

    # Interactive test
    print("\n5. Interactive Test (press Ctrl+C to skip):")
    try:
        age = get_int_input("Enter age (0-120): ", 0, 120)
        if age:
            print(f"  ✓ Valid age: {age}")

        color = get_choice_input("Choose color (red/green/blue): ", ['red', 'green', 'blue'])
        if color:
            print(f"  ✓ Valid choice: {color}")

        confirm = get_yes_no_input("Continue?", default=True)
        if confirm is not None:
            print(f"  ✓ Answer: {confirm}")
    except KeyboardInterrupt:
        print("\n  (Skipped)")

    print("\n✅ All validation tests passed!")
