"""
Tests for validation module
============================
"""

import pytest
from validation import (
    ValidationError,
    validate_int,
    validate_float,
    validate_choice,
    validate_string,
    validate_name,
    validate_bool,
    validate_menu_choice,
    validate_stat_input,
)


class TestIntegerValidation:
    """Test integer validation"""

    def test_valid_integer(self):
        """Test valid integer conversion"""
        assert validate_int("42") == 42
        assert validate_int("  10  ") == 10
        assert validate_int("-5") == -5

    def test_invalid_integer(self):
        """Test invalid input raises error"""
        with pytest.raises(ValidationError):
            validate_int("not a number")

        with pytest.raises(ValidationError):
            validate_int("12.5")

    def test_range_validation(self):
        """Test range constraints"""
        assert validate_int("5", 1, 10) == 5

        with pytest.raises(ValidationError):
            validate_int("15", 1, 10)  # Too high

        with pytest.raises(ValidationError):
            validate_int("0", 1, 10)  # Too low


class TestChoiceValidation:
    """Test choice validation"""

    def test_valid_choice(self):
        """Test valid choice selection"""
        choices = ['red', 'green', 'blue']
        assert validate_choice('red', choices) == 'red'
        assert validate_choice('RED', choices) == 'red'  # Case insensitive by default

    def test_invalid_choice(self):
        """Test invalid choice raises error"""
        choices = ['red', 'green', 'blue']
        with pytest.raises(ValidationError):
            validate_choice('yellow', choices)

    def test_case_sensitive(self):
        """Test case sensitive matching"""
        choices = ['Red', 'Green']
        assert validate_choice('Red', choices, case_sensitive=True) == 'Red'

        with pytest.raises(ValidationError):
            validate_choice('red', choices, case_sensitive=True)


class TestStringValidation:
    """Test string validation"""

    def test_valid_string(self):
        """Test valid string"""
        assert validate_string("hello") == "hello"
        assert validate_string("  world  ") == "world"  # Stripped

    def test_empty_string(self):
        """Test empty string handling"""
        with pytest.raises(ValidationError):
            validate_string("")

        # Allow empty
        assert validate_string("", allow_empty=True) == ""

    def test_length_validation(self):
        """Test length constraints"""
        assert validate_string("abc", min_length=2, max_length=5) == "abc"

        with pytest.raises(ValidationError):
            validate_string("a", min_length=2)

        with pytest.raises(ValidationError):
            validate_string("too long", max_length=5)

    def test_pattern_validation(self):
        """Test pattern matching"""
        # Letters only
        assert validate_string("abc", pattern=r'^[a-z]+$') == "abc"

        with pytest.raises(ValidationError):
            validate_string("abc123", pattern=r'^[a-z]+$')


class TestNameValidation:
    """Test name validation"""

    def test_valid_names(self):
        """Test valid names"""
        assert validate_name("John") == "John"
        assert validate_name("Mary Jane") == "Mary Jane"
        assert validate_name("O'Brien") == "O'Brien"

    def test_invalid_names(self):
        """Test invalid names"""
        with pytest.raises(ValidationError):
            validate_name("123")  # Starts with number

        with pytest.raises(ValidationError):
            validate_name("John@Doe")  # Special characters

        with pytest.raises(ValidationError):
            validate_name("")  # Empty


class TestBooleanValidation:
    """Test boolean validation"""

    def test_true_values(self):
        """Test values that should be True"""
        assert validate_bool("y") is True
        assert validate_bool("yes") is True
        assert validate_bool("Y") is True
        assert validate_bool("YES") is True
        assert validate_bool("true") is True
        assert validate_bool("1") is True

    def test_false_values(self):
        """Test values that should be False"""
        assert validate_bool("n") is False
        assert validate_bool("no") is False
        assert validate_bool("N") is False
        assert validate_bool("NO") is False
        assert validate_bool("false") is False
        assert validate_bool("0") is False

    def test_invalid_values(self):
        """Test invalid values"""
        with pytest.raises(ValidationError):
            validate_bool("maybe")

        with pytest.raises(ValidationError):
            validate_bool("2")


class TestMenuChoice:
    """Test menu choice validation"""

    def test_valid_choices(self):
        """Test valid menu choices"""
        assert validate_menu_choice("1", 3) == 1
        assert validate_menu_choice("3", 3) == 3
        assert validate_menu_choice("0", 3, allow_zero=True) == 0

    def test_invalid_choices(self):
        """Test invalid menu choices"""
        with pytest.raises(ValidationError):
            validate_menu_choice("4", 3)  # Out of range

        with pytest.raises(ValidationError):
            validate_menu_choice("0", 3, allow_zero=False)  # Zero not allowed

        with pytest.raises(ValidationError):
            validate_menu_choice("abc", 3)  # Not a number


class TestGameSpecificValidators:
    """Test game-specific validators"""

    def test_stat_validation(self):
        """Test SPECIAL stat validation"""
        assert validate_stat_input("5") == 5
        assert validate_stat_input("10") == 10

        with pytest.raises(ValidationError):
            validate_stat_input("0")  # Too low

        with pytest.raises(ValidationError):
            validate_stat_input("11")  # Too high


class TestErrorMessages:
    """Test that error messages are helpful"""

    def test_custom_error_messages(self):
        """Test custom error messages"""
        try:
            validate_int("abc", error_msg="Please enter a valid number!")
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            assert "Please enter a valid number!" in str(e)

    def test_default_error_messages(self):
        """Test default error messages are clear"""
        try:
            validate_int("15", 1, 10)
        except ValidationError as e:
            assert "at most" in str(e).lower()
            assert "10" in str(e)
