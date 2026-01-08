"""
VAULT 13: Resources Model
The Resources class for vault resource management.
"""

from dataclasses import dataclass


@dataclass
class Resources:
    """Vault resources with management methods"""
    power: int = 20
    power_max: int = 30
    water: int = 20
    water_max: int = 30
    food: int = 20
    food_max: int = 30
    caps: int = 500
    # Advanced resources
    research: int = 0
    influence: int = 0
    materials: int = 0
    metal: int = 0
    electronics: int = 0
    cloth: int = 0

    def add(self, resource: str, amount: int):
        """Add resource (respects maximums for basic resources)"""
        if resource in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            current = getattr(self, resource)
            setattr(self, resource, current + amount)
        else:
            current = getattr(self, resource)
            max_val = getattr(self, f"{resource}_max")
            setattr(self, resource, min(max_val, current + amount))

    def remove(self, resource: str, amount: int) -> bool:
        """Remove resource if enough available"""
        current = getattr(self, resource, 0)
        if current >= amount:
            setattr(self, resource, current - amount)
            return True
        return False

    def consume_with_rationing(self, resource: str, amount: int) -> int:
        """Consume up to available amount, return amount consumed"""
        current = getattr(self, resource)
        actual = min(current, amount)
        setattr(self, resource, current - actual)
        return actual

    def has_enough(self, resource: str, amount: int) -> bool:
        """Check if enough resource available"""
        return getattr(self, resource, 0) >= amount

    def is_critical(self, resource: str) -> bool:
        """Check if resource is at critical level"""
        if resource in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            return getattr(self, resource, 0) < 50
        current = getattr(self, resource)
        max_val = getattr(self, f"{resource}_max")
        return current < max_val * 0.2

    def is_full(self, resource: str) -> bool:
        """Check if resource is at maximum"""
        if resource in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            return False  # These have no max
        current = getattr(self, resource)
        max_val = getattr(self, f"{resource}_max")
        return current >= max_val

    def get_percentage(self, resource: str) -> float:
        """Get resource as percentage of max (0-100)"""
        if resource in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            return 100.0  # No max, always "full"
        current = getattr(self, resource)
        max_val = getattr(self, f"{resource}_max")
        return (current / max_val * 100) if max_val > 0 else 0

    def increase_storage(self, resource: str, amount: int):
        """Increase maximum storage for a resource"""
        if resource not in ["caps", "research", "influence", "materials", "metal", "electronics", "cloth"]:
            max_attr = f"{resource}_max"
            current_max = getattr(self, max_attr)
            setattr(self, max_attr, current_max + amount)

    def get_all_basic(self) -> dict:
        """Get all basic resources as dict"""
        return {
            "power": self.power,
            "water": self.water,
            "food": self.food,
            "caps": self.caps
        }

    def get_all_advanced(self) -> dict:
        """Get all advanced resources as dict"""
        return {
            "research": self.research,
            "influence": self.influence,
            "materials": self.materials,
            "metal": self.metal,
            "electronics": self.electronics,
            "cloth": self.cloth
        }
