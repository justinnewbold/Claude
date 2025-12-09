"""
Vault Shelter - Resource Management Module
==========================================
Resource tracking and consumption system
"""

from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum


class ResourceType(Enum):
    """Types of resources"""
    POWER = "power"
    WATER = "water"
    FOOD = "food"
    CAPS = "caps"  # Currency
    STIMPAKS = "stimpaks"  # Medical
    RADAWAY = "radaway"  # Radiation treatment


@dataclass
class ResourceManager:
    """
    Manages vault resources with consumption and storage.

    Extracted from vault_shelter_v6.py as part of modular refactoring.
    """
    # Current amounts
    power: int = 100
    water: int = 100
    food: int = 100
    caps: int = 1000
    stimpaks: int = 5
    radaway: int = 5

    # Storage capacity
    power_storage: int = 200
    water_storage: int = 200
    food_storage: int = 200
    caps_storage: int = 99999  # Unlimited

    # Consumption rates
    power_consumption: int = 10  # Per turn
    water_consumption: int = 10  # Per turn
    food_consumption: int = 10  # Per turn

    # History for tracking trends
    history: Dict[str, List[int]] = field(default_factory=lambda: {
        'power': [],
        'water': [],
        'food': [],
        'caps': []
    })

    def add_resource(self, resource: str, amount: int) -> int:
        """
        Add resources up to storage capacity.

        Args:
            resource: Resource type
            amount: Amount to add

        Returns:
            Amount actually added
        """
        current = getattr(self, resource, 0)
        storage = getattr(self, f"{resource}_storage", 99999)

        max_add = storage - current
        actual_add = min(amount, max_add)

        setattr(self, resource, current + actual_add)
        return actual_add

    def consume_resource(self, resource: str, amount: int) -> bool:
        """
        Consume resources if available.

        Args:
            resource: Resource type
            amount: Amount to consume

        Returns:
            True if sufficient resources available
        """
        current = getattr(self, resource, 0)

        if current >= amount:
            setattr(self, resource, current - amount)
            return True

        return False

    def has_resources(self, requirements: Dict[str, int]) -> bool:
        """
        Check if vault has required resources.

        Args:
            requirements: Dict of resource: amount

        Returns:
            True if all requirements met
        """
        for resource, amount in requirements.items():
            current = getattr(self, resource, 0)
            if current < amount:
                return False

        return True

    def spend_resources(self, requirements: Dict[str, int]) -> bool:
        """
        Spend multiple resources.

        Args:
            requirements: Dict of resource: amount

        Returns:
            True if transaction successful
        """
        # Check first
        if not self.has_resources(requirements):
            return False

        # Spend
        for resource, amount in requirements.items():
            current = getattr(self, resource, 0)
            setattr(self, resource, current - amount)

        return True

    def calculate_consumption(self, population: int) -> Dict[str, int]:
        """
        Calculate per-turn resource consumption.

        Args:
            population: Number of dwellers

        Returns:
            Dict of resource: amount consumed
        """
        consumption = {}

        # Base consumption per dweller
        consumption['food'] = population * 1
        consumption['water'] = population * 1

        # Power depends on number of rooms (handled elsewhere)
        consumption['power'] = self.power_consumption

        return consumption

    def apply_consumption(self, population: int) -> Dict[str, bool]:
        """
        Apply turn-based consumption.

        Args:
            population: Number of dwellers

        Returns:
            Dict of resource: shortage (True if shortage occurred)
        """
        consumption = self.calculate_consumption(population)
        shortages = {}

        for resource, amount in consumption.items():
            current = getattr(self, resource, 0)
            new_amount = max(0, current - amount)
            setattr(self, resource, new_amount)

            # Track shortage
            shortages[resource] = (new_amount == 0 and amount > 0)

        return shortages

    def record_history(self):
        """Record current resource levels for trend tracking"""
        self.history['power'].append(self.power)
        self.history['water'].append(self.water)
        self.history['food'].append(self.food)
        self.history['caps'].append(self.caps)

        # Keep only last 50 entries
        for key in self.history:
            self.history[key] = self.history[key][-50:]

    def get_trend(self, resource: str) -> str:
        """
        Get trend indicator for resource.

        Args:
            resource: Resource type

        Returns:
            Arrow indicator (↑↓→)
        """
        if resource not in self.history or len(self.history[resource]) < 2:
            return "→"

        recent = self.history[resource][-5:]
        if len(recent) < 2:
            return "→"

        avg_recent = sum(recent) / len(recent)
        current = getattr(self, resource, 0)

        if current > avg_recent * 1.1:
            return "↑"
        elif current < avg_recent * 0.9:
            return "↓"
        else:
            return "→"

    def get_status_color(self, resource: str) -> str:
        """
        Get color based on resource status.

        Args:
            resource: Resource type

        Returns:
            ANSI color code
        """
        current = getattr(self, resource, 0)
        storage = getattr(self, f"{resource}_storage", 100)

        ratio = current / storage if storage > 0 else 0

        if ratio >= 0.7:
            return '\033[38;5;46m'  # Green
        elif ratio >= 0.4:
            return '\033[38;5;226m'  # Yellow
        else:
            return '\033[38;5;196m'  # Red

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'power': self.power,
            'water': self.water,
            'food': self.food,
            'caps': self.caps,
            'stimpaks': self.stimpaks,
            'radaway': self.radaway,
            'power_storage': self.power_storage,
            'water_storage': self.water_storage,
            'food_storage': self.food_storage,
            'power_consumption': self.power_consumption,
            'water_consumption': self.water_consumption,
            'food_consumption': self.food_consumption,
            'history': self.history,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ResourceManager':
        """Create from dictionary"""
        return cls(**data)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def format_resource_bar(name: str, current: int, maximum: int, width: int = 12) -> str:
    """
    Format a resource with progress bar and color.

    Args:
        name: Resource name
        current: Current amount
        maximum: Maximum amount
        width: Bar width

    Returns:
        Formatted string with color
    """
    ratio = current / maximum if maximum > 0 else 0
    filled_amount = int(ratio * width)

    # Color based on ratio
    if ratio >= 0.7:
        color = '\033[38;5;46m'  # Green
    elif ratio >= 0.4:
        color = '\033[38;5;226m'  # Yellow
    else:
        color = '\033[38;5;196m'  # Red

    reset = '\033[0m'
    bar = f"[{'█' * filled_amount}{'░' * (width - filled_amount)}]"

    return f"{name}: {color}{bar}{reset} {current}/{maximum}"


def calculate_optimal_production(population: int, rooms_count: int) -> Dict[str, int]:
    """
    Calculate optimal production levels.

    Args:
        population: Number of dwellers
        rooms_count: Number of rooms

    Returns:
        Dict of resource: optimal production
    """
    return {
        'food': population * 2,  # 2x consumption for buffer
        'water': population * 2,
        'power': rooms_count * 5,  # 5 per room
    }


def predict_shortage(resources: ResourceManager, population: int, turns_ahead: int = 5) -> Dict[str, int]:
    """
    Predict when resources will run out.

    Args:
        resources: Resource manager
        population: Current population
        turns_ahead: How many turns to look ahead

    Returns:
        Dict of resource: turns until shortage (or None)
    """
    consumption = resources.calculate_consumption(population)
    predictions = {}

    for resource, per_turn in consumption.items():
        current = getattr(resources, resource, 0)

        if per_turn > 0:
            turns_remaining = current // per_turn
            if turns_remaining <= turns_ahead:
                predictions[resource] = turns_remaining

    return predictions
