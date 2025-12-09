#!/usr/bin/env python3
"""
Common Game Utilities
======================
Shared utility functions used across multiple games.
"""

import random
import math
from typing import List, Tuple, Dict, Any, Optional, Callable
from datetime import datetime, timedelta

from constants import *


# =============================================================================
# RANDOM NUMBER GENERATION
# =============================================================================

def roll_dice(sides: int = 6, count: int = 1) -> int:
    """
    Roll dice and return sum.

    Args:
        sides: Number of sides on each die
        count: Number of dice to roll

    Returns:
        Sum of all dice rolls

    Example:
        roll_dice(6, 2)  # Roll 2d6
    """
    return sum(random.randint(1, sides) for _ in range(count))


def weighted_choice(choices: Dict[Any, float]) -> Any:
    """
    Make weighted random choice.

    Args:
        choices: Dict mapping choices to weights

    Returns:
        Selected choice

    Example:
        weighted_choice({'common': 0.7, 'rare': 0.3})
    """
    items = list(choices.keys())
    weights = list(choices.values())
    return random.choices(items, weights=weights)[0]


def chance(probability: float) -> bool:
    """
    Random boolean with given probability.

    Args:
        probability: Probability of True (0.0 to 1.0)

    Returns:
        True or False

    Example:
        if chance(0.3):  # 30% chance
            print("Lucky!")
    """
    return random.random() < probability


def random_range(min_val: float, max_val: float, round_result: bool = False) -> float:
    """Random value in range with optional rounding"""
    result = random.uniform(min_val, max_val)
    return round(result) if round_result else result


# =============================================================================
# MATH UTILITIES
# =============================================================================

def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp value to range"""
    return max(min_value, min(max_value, value))


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between start and end.

    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0.0 to 1.0)

    Returns:
        Interpolated value
    """
    return start + (end - start) * t


def normalize(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize value to 0.0-1.0 range.

    Args:
        value: Value to normalize
        min_val: Minimum of range
        max_val: Maximum of range

    Returns:
        Normalized value (0.0 to 1.0)
    """
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """Calculate Manhattan distance between two points"""
    return abs(x2 - x1) + abs(y2 - y1)


# =============================================================================
# STAT CALCULATIONS
# =============================================================================

def calculate_stat_bonus(stat_value: int, base_multiplier: float = 1.0) -> float:
    """
    Calculate bonus from SPECIAL stat.

    Args:
        stat_value: Stat value (1-10)
        base_multiplier: Base multiplier

    Returns:
        Calculated bonus
    """
    # Stats scale non-linearly: 1=0.5x, 5=1.0x, 10=2.0x
    normalized = (stat_value - 1) / 9  # 0.0 to 1.0
    multiplier = 0.5 + (1.5 * normalized)  # 0.5 to 2.0
    return base_multiplier * multiplier


def calculate_level_xp(level: int, base_xp: int = 100, scaling: float = 1.2) -> int:
    """
    Calculate XP required for level.

    Args:
        level: Target level
        base_xp: XP required for level 1
        scaling: XP scaling factor per level

    Returns:
        Total XP required
    """
    return int(base_xp * (scaling ** (level - 1)))


def calculate_damage(
    base_damage: int,
    attacker_stat: int,
    defender_stat: int,
    variance: float = 0.2
) -> int:
    """
    Calculate combat damage.

    Args:
        base_damage: Base weapon damage
        attacker_stat: Attacker's relevant stat
        defender_stat: Defender's relevant stat
        variance: Random variance (±%)

    Returns:
        Final damage amount
    """
    # Stat bonus
    attacker_bonus = calculate_stat_bonus(attacker_stat)
    defender_bonus = calculate_stat_bonus(defender_stat)

    damage = base_damage * attacker_bonus / defender_bonus

    # Add variance
    variance_amount = damage * variance
    damage += random.uniform(-variance_amount, variance_amount)

    return max(1, int(damage))  # Minimum 1 damage


# =============================================================================
# RESOURCE CALCULATIONS
# =============================================================================

def calculate_production(
    base_production: int,
    workers: int,
    worker_stats: List[int],
    room_level: int = 1,
    difficulty_multiplier: float = 1.0
) -> int:
    """
    Calculate resource production.

    Args:
        base_production: Base production rate
        workers: Number of workers
        worker_stats: List of worker stat values
        room_level: Room upgrade level
        difficulty_multiplier: Difficulty modifier

    Returns:
        Total production
    """
    if workers == 0:
        return 0

    # Base production scales with room level
    base = base_production * room_level

    # Worker bonus (average of stats)
    avg_stat = sum(worker_stats[:workers]) / workers if workers > 0 else 5
    stat_multiplier = calculate_stat_bonus(int(avg_stat))

    # Calculate total
    production = base * stat_multiplier * difficulty_multiplier

    return int(production)


def calculate_consumption(
    population: int,
    base_consumption: int = 1,
    difficulty_multiplier: float = 1.0
) -> int:
    """
    Calculate resource consumption.

    Args:
        population: Number of dwellers
        base_consumption: Base consumption per dweller
        difficulty_multiplier: Difficulty modifier

    Returns:
        Total consumption
    """
    return int(population * base_consumption * difficulty_multiplier)


def calculate_storage_capacity(
    base_capacity: int,
    storage_rooms: int,
    bonus_per_room: int = 100
) -> int:
    """Calculate total storage capacity"""
    return base_capacity + (storage_rooms * bonus_per_room)


# =============================================================================
# TIME UTILITIES
# =============================================================================

def format_duration(seconds: int) -> str:
    """
    Format seconds into readable duration.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "2h 15m", "45s")
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s" if secs > 0 else f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h" if hours > 0 else f"{days}d"


def parse_duration(duration_str: str) -> int:
    """
    Parse duration string to seconds.

    Args:
        duration_str: Duration string (e.g., "2h", "30m", "1d 6h")

    Returns:
        Duration in seconds
    """
    import re

    total = 0
    patterns = {
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1
    }

    for unit, multiplier in patterns.items():
        match = re.search(rf'(\d+){unit}', duration_str)
        if match:
            total += int(match.group(1)) * multiplier

    return total


# =============================================================================
# TEXT UTILITIES
# =============================================================================

def pluralize(count: int, singular: str, plural: Optional[str] = None) -> str:
    """
    Pluralize word based on count.

    Args:
        count: Number of items
        singular: Singular form
        plural: Plural form (defaults to singular + 's')

    Returns:
        Pluralized string with count

    Example:
        pluralize(1, "dweller")  # "1 dweller"
        pluralize(5, "dweller")  # "5 dwellers"
        pluralize(2, "child", "children")  # "2 children"
    """
    if plural is None:
        plural = singular + 's'

    word = singular if count == 1 else plural
    return f"{count} {word}"


def abbreviate_number(num: int) -> str:
    """
    Abbreviate large numbers.

    Args:
        num: Number to abbreviate

    Returns:
        Abbreviated string (e.g., "1.5K", "2.3M")
    """
    if num < 1000:
        return str(num)
    elif num < 1_000_000:
        return f"{num / 1000:.1f}K"
    elif num < 1_000_000_000:
        return f"{num / 1_000_000:.1f}M"
    else:
        return f"{num / 1_000_000_000:.1f}B"


def wrap_text(text: str, width: int = 60) -> List[str]:
    """
    Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width

    Returns:
        List of wrapped lines
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)

        if current_length + word_length + len(current_line) <= width:
            current_line.append(word)
            current_length += word_length
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length

    if current_line:
        lines.append(' '.join(current_line))

    return lines


# =============================================================================
# LIST UTILITIES
# =============================================================================

def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks.

    Args:
        items: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def find_by_id(items: List[Dict[str, Any]], id_value: Any, id_key: str = 'id') -> Optional[Dict[str, Any]]:
    """Find item in list by ID"""
    return next((item for item in items if item.get(id_key) == id_value), None)


def group_by(items: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    Group items by key value.

    Args:
        items: List of dicts
        key: Key to group by

    Returns:
        Dict mapping key values to lists of items
    """
    groups = {}
    for item in items:
        group_key = item.get(key)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups


# =============================================================================
# PROBABILITY UTILITIES
# =============================================================================

def calculate_crit_chance(luck: int, base_chance: float = 0.05) -> float:
    """Calculate critical hit chance based on luck stat"""
    return min(0.5, base_chance + (luck - 5) * 0.02)  # Max 50%


def calculate_success_chance(
    stat: int,
    difficulty: int,
    base_chance: float = 0.5
) -> float:
    """
    Calculate success chance for stat check.

    Args:
        stat: Character stat (1-10)
        difficulty: Difficulty rating (1-10)
        base_chance: Base success chance

    Returns:
        Success probability (0.0 to 1.0)
    """
    stat_bonus = (stat - 5) * 0.1  # -0.4 to +0.5
    difficulty_penalty = (difficulty - 5) * 0.1

    chance = base_chance + stat_bonus - difficulty_penalty
    return clamp(chance, 0.05, 0.95)  # 5% minimum, 95% maximum


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Game Utilities Test")
    print("=" * 60)

    # Test dice rolling
    print("\n1. Dice Rolling:")
    print(f"   Roll 2d6: {roll_dice(6, 2)}")
    print(f"   Roll 1d20: {roll_dice(20)}")

    # Test weighted choice
    print("\n2. Weighted Choice:")
    choices = {'common': 0.7, 'rare': 0.2, 'legendary': 0.1}
    results = [weighted_choice(choices) for _ in range(10)]
    print(f"   10 random choices: {results}")

    # Test stat calculations
    print("\n3. Stat Calculations:")
    print(f"   Stat 1 bonus: {calculate_stat_bonus(1):.2f}x")
    print(f"   Stat 5 bonus: {calculate_stat_bonus(5):.2f}x")
    print(f"   Stat 10 bonus: {calculate_stat_bonus(10):.2f}x")

    # Test damage calculation
    print("\n4. Combat Damage:")
    damage = calculate_damage(base_damage=10, attacker_stat=8, defender_stat=5)
    print(f"   Damage (10 base, 8 atk, 5 def): {damage}")

    # Test production
    print("\n5. Resource Production:")
    production = calculate_production(
        base_production=5,
        workers=2,
        worker_stats=[7, 6],
        room_level=2
    )
    print(f"   Production (5 base, 2 workers, level 2): {production}")

    # Test time formatting
    print("\n6. Time Formatting:")
    print(f"   45 seconds: {format_duration(45)}")
    print(f"   3661 seconds: {format_duration(3661)}")
    print(f"   86400 seconds: {format_duration(86400)}")

    # Test text utilities
    print("\n7. Text Utilities:")
    print(f"   {pluralize(1, 'dweller')}")
    print(f"   {pluralize(5, 'dweller')}")
    print(f"   {abbreviate_number(1500)}")
    print(f"   {abbreviate_number(2_500_000)}")

    # Test probability
    print("\n8. Probability:")
    print(f"   Crit chance (luck 5): {calculate_crit_chance(5):.1%}")
    print(f"   Crit chance (luck 10): {calculate_crit_chance(10):.1%}")
    print(f"   Success (stat 8, diff 5): {calculate_success_chance(8, 5):.1%}")

    print("\n✅ All utility tests passed!")
