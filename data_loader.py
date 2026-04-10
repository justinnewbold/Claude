#!/usr/bin/env python3
"""
Data Loader Module
==================
Loads game data from JSON files.
Provides caching and validation.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from logging_config import get_logger

logger = get_logger(__name__)


class DataLoadError(Exception):
    """Raised when data loading fails"""
    pass


class DataValidationError(Exception):
    """Raised when data validation fails"""
    pass


# =============================================================================
# SCHEMA VALIDATION
# =============================================================================

def validate_required_fields(data: Dict[str, Any], required: List[str], context: str) -> List[str]:
    """Validate that required fields are present"""
    errors = []
    for field in required:
        if field not in data:
            errors.append(f"{context}: Missing required field '{field}'")
    return errors


def validate_field_type(value: Any, expected_type: str, field_name: str, context: str) -> List[str]:
    """Validate field type"""
    errors = []
    type_map = {
        'string': str,
        'integer': int,
        'number': (int, float),
        'boolean': bool,
        'object': dict,
        'array': list,
    }

    if expected_type in type_map:
        if not isinstance(value, type_map[expected_type]):
            errors.append(f"{context}.{field_name}: Expected {expected_type}, got {type(value).__name__}")

    return errors


def validate_weapon(weapon_id: str, weapon: Dict[str, Any]) -> List[str]:
    """Validate a weapon entry"""
    errors = []
    context = f"weapons.{weapon_id}"

    required = ['id', 'name', 'type', 'damage', 'rarity', 'cost']
    errors.extend(validate_required_fields(weapon, required, context))

    if 'damage' in weapon and not isinstance(weapon['damage'], int):
        errors.append(f"{context}.damage: Must be an integer")
    if 'damage' in weapon and isinstance(weapon['damage'], int) and weapon['damage'] < 0:
        errors.append(f"{context}.damage: Must be non-negative")

    valid_rarities = ['common', 'uncommon', 'rare', 'legendary']
    if 'rarity' in weapon and weapon['rarity'] not in valid_rarities:
        errors.append(f"{context}.rarity: Must be one of {valid_rarities}")

    return errors


def validate_outfit(outfit_id: str, outfit: Dict[str, Any]) -> List[str]:
    """Validate an outfit entry"""
    errors = []
    context = f"outfits.{outfit_id}"

    required = ['id', 'name', 'type', 'defense', 'rarity', 'cost']
    errors.extend(validate_required_fields(outfit, required, context))

    if 'defense' in outfit and not isinstance(outfit['defense'], int):
        errors.append(f"{context}.defense: Must be an integer")
    if 'defense' in outfit and isinstance(outfit['defense'], int) and outfit['defense'] < 0:
        errors.append(f"{context}.defense: Must be non-negative")

    return errors


def validate_room(room_id: str, room: Dict[str, Any]) -> List[str]:
    """Validate a room entry"""
    errors = []
    context = f"rooms.{room_id}"

    required = ['id', 'name', 'description', 'cost', 'capacity']
    errors.extend(validate_required_fields(room, required, context))

    if 'cost' in room and not isinstance(room['cost'], int):
        errors.append(f"{context}.cost: Must be an integer")
    if 'capacity' in room and not isinstance(room['capacity'], int):
        errors.append(f"{context}.capacity: Must be an integer")

    return errors


def validate_skill(skill_id: str, skill: Dict[str, Any]) -> List[str]:
    """Validate a skill entry"""
    errors = []
    context = f"skills.{skill_id}"

    required = ['id', 'name', 'description', 'category', 'bonus_type', 'bonus_value', 'cost']
    errors.extend(validate_required_fields(skill, required, context))

    valid_categories = ['production', 'combat', 'exploration', 'social', 'survival', 'special']
    if 'category' in skill and skill['category'] not in valid_categories:
        errors.append(f"{context}.category: Must be one of {valid_categories}")

    return errors


def validate_equipment_data(data: Dict[str, Any]) -> List[str]:
    """Validate equipment.json data"""
    errors = []

    if 'weapons' not in data:
        errors.append("Missing 'weapons' section")
    else:
        for weapon_id, weapon in data['weapons'].items():
            errors.extend(validate_weapon(weapon_id, weapon))

    if 'outfits' not in data:
        errors.append("Missing 'outfits' section")
    else:
        for outfit_id, outfit in data['outfits'].items():
            errors.extend(validate_outfit(outfit_id, outfit))

    return errors


def validate_rooms_data(data: Dict[str, Any]) -> List[str]:
    """Validate rooms.json data"""
    errors = []

    if 'rooms' not in data:
        errors.append("Missing 'rooms' section")
    else:
        for room_id, room in data['rooms'].items():
            errors.extend(validate_room(room_id, room))

    return errors


def validate_skills_data(data: Dict[str, Any]) -> List[str]:
    """Validate skills.json data"""
    errors = []

    if 'skills' not in data:
        errors.append("Missing 'skills' section")
    else:
        for skill_id, skill in data['skills'].items():
            errors.extend(validate_skill(skill_id, skill))

    return errors


# =============================================================================
# DATA LOADER CLASS
# =============================================================================

class DataLoader:
    """
    Loads and caches game data from JSON files.

    Usage:
        loader = DataLoader()
        rooms = loader.get_rooms()
        equipment = loader.get_equipment()
    """

    def __init__(self, data_dir: Optional[Path] = None, validate: bool = True):
        """
        Initialize data loader.

        Args:
            data_dir: Directory containing JSON files (default: ./data/)
            validate: Whether to validate data against schemas (default: True)
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / 'data'

        self.data_dir = Path(data_dir)
        self._cache: Dict[str, Any] = {}
        self._validate = validate

        # Mapping of filenames to validation functions
        self._validators = {
            'equipment.json': validate_equipment_data,
            'rooms.json': validate_rooms_data,
            'skills.json': validate_skills_data,
        }

        logger.info(f"DataLoader initialized with data_dir: {self.data_dir}, validate: {validate}")

    def _load_json(self, filename: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Load JSON file with caching.

        Args:
            filename: Name of JSON file (e.g., "rooms.json")
            use_cache: Whether to use cached data

        Returns:
            Parsed JSON data

        Raises:
            DataLoadError: If file cannot be loaded
        """
        # Check cache
        if use_cache and filename in self._cache:
            logger.debug(f"Loading {filename} from cache")
            return self._cache[filename]

        # Load from file
        file_path = self.data_dir / filename

        if not file_path.exists():
            raise DataLoadError(f"Data file not found: {file_path}")

        try:
            logger.debug(f"Loading {filename} from disk")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate if enabled and validator exists
            if self._validate and filename in self._validators:
                errors = self._validators[filename](data)
                if errors:
                    logger.warning(f"Validation errors in {filename}: {errors}")
                    raise DataValidationError(
                        f"Validation failed for {filename}:\n" +
                        "\n".join(f"  - {e}" for e in errors[:10]) +
                        (f"\n  ... and {len(errors) - 10} more errors" if len(errors) > 10 else "")
                    )
                logger.debug(f"Validation passed for {filename}")

            # Cache it
            self._cache[filename] = data

            return data

        except json.JSONDecodeError as e:
            raise DataLoadError(f"Invalid JSON in {filename}: {e}")
        except DataValidationError:
            raise
        except (IOError, OSError, KeyError, TypeError) as e:
            raise DataLoadError(f"Failed to load {filename}: {e}")

    def get_rooms(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get room configurations.

        Returns:
            Dict with 'rooms' key containing room data
        """
        return self._load_json('rooms.json', use_cache)

    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get specific room configuration by ID"""
        rooms_data = self.get_rooms()
        return rooms_data.get('rooms', {}).get(room_id)

    def get_equipment(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get equipment data (weapons and outfits).

        Returns:
            Dict with 'weapons' and 'outfits' keys
        """
        return self._load_json('equipment.json', use_cache)

    def get_weapon(self, weapon_id: str) -> Optional[Dict[str, Any]]:
        """Get specific weapon by ID"""
        equipment_data = self.get_equipment()
        return equipment_data.get('weapons', {}).get(weapon_id)

    def get_outfit(self, outfit_id: str) -> Optional[Dict[str, Any]]:
        """Get specific outfit by ID"""
        equipment_data = self.get_equipment()
        return equipment_data.get('outfits', {}).get(outfit_id)

    def get_skills(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get skills data.

        Returns:
            Dict with 'skills' key containing skill data
        """
        return self._load_json('skills.json', use_cache)

    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get specific skill by ID"""
        skills_data = self.get_skills()
        return skills_data.get('skills', {}).get(skill_id)

    def get_skills_by_category(self, category: str) -> Dict[str, Any]:
        """Get all skills in a category"""
        skills_data = self.get_skills()
        skills = skills_data.get('skills', {})

        return {
            skill_id: skill
            for skill_id, skill in skills.items()
            if skill.get('category') == category
        }

    def clear_cache(self) -> None:
        """Clear the data cache"""
        self._cache.clear()
        logger.debug("Data cache cleared")

    def reload(self) -> None:
        """Reload all data from disk"""
        self.clear_cache()
        logger.info("Data reloaded from disk")


# =============================================================================
# LAZY LOADING SUPPORT
# =============================================================================

class LazyData:
    """
    Lazy loading wrapper for data files.

    Data is only loaded when first accessed, reducing startup time.

    Usage:
        lazy_rooms = LazyData('rooms.json')
        # Data not loaded yet
        actual_data = lazy_rooms.data  # Data loaded now
    """

    def __init__(self, filename: str, loader: Optional['DataLoader'] = None):
        """
        Initialize lazy data wrapper.

        Args:
            filename: Name of JSON file to load
            loader: DataLoader instance (uses global if None)
        """
        self._filename = filename
        self._loader = loader
        self._data: Optional[Dict[str, Any]] = None
        self._loaded = False

    @property
    def data(self) -> Dict[str, Any]:
        """Get data, loading on first access."""
        if not self._loaded:
            loader = self._loader or get_data_loader()
            self._data = loader._load_json(self._filename)
            self._loaded = True
        return self._data

    @property
    def is_loaded(self) -> bool:
        """Check if data has been loaded."""
        return self._loaded

    def reload(self) -> Dict[str, Any]:
        """Force reload data from disk."""
        loader = self._loader or get_data_loader()
        self._data = loader._load_json(self._filename, use_cache=False)
        self._loaded = True
        return self._data

    def __repr__(self) -> str:
        status = "loaded" if self._loaded else "not loaded"
        return f"LazyData({self._filename!r}, {status})"


class LazyDataLoader:
    """
    Data loader with lazy loading for improved startup performance.

    Unlike DataLoader which caches after first explicit load,
    LazyDataLoader doesn't load anything until accessed.

    Usage:
        lazy_loader = LazyDataLoader()
        # Nothing loaded yet

        rooms = lazy_loader.rooms  # Rooms loaded now
        weapons = lazy_loader.weapons  # Equipment loaded now
    """

    def __init__(self, data_dir: Optional[Path] = None, validate: bool = True):
        """
        Initialize lazy data loader.

        Args:
            data_dir: Directory containing JSON files
            validate: Whether to validate data against schemas
        """
        self._inner_loader = DataLoader(data_dir, validate)

        # Create lazy wrappers for each data file
        self._lazy_rooms = LazyData('rooms.json', self._inner_loader)
        self._lazy_equipment = LazyData('equipment.json', self._inner_loader)
        self._lazy_skills = LazyData('skills.json', self._inner_loader)

        logger.info("LazyDataLoader initialized (data will load on first access)")

    @property
    def rooms(self) -> Dict[str, Any]:
        """Get rooms data (lazy loaded)."""
        return self._lazy_rooms.data

    @property
    def weapons(self) -> Dict[str, Any]:
        """Get weapons data (lazy loaded)."""
        return self._lazy_equipment.data.get('weapons', {})

    @property
    def outfits(self) -> Dict[str, Any]:
        """Get outfits data (lazy loaded)."""
        return self._lazy_equipment.data.get('outfits', {})

    @property
    def equipment(self) -> Dict[str, Any]:
        """Get full equipment data (lazy loaded)."""
        return self._lazy_equipment.data

    @property
    def skills(self) -> Dict[str, Any]:
        """Get skills data (lazy loaded)."""
        return self._lazy_skills.data

    def get_loading_status(self) -> Dict[str, bool]:
        """Get loading status of all data files."""
        return {
            'rooms': self._lazy_rooms.is_loaded,
            'equipment': self._lazy_equipment.is_loaded,
            'skills': self._lazy_skills.is_loaded,
        }

    def preload_all(self) -> None:
        """Force load all data files (useful for testing)."""
        _ = self.rooms
        _ = self.equipment
        _ = self.skills
        logger.info("All data preloaded")

    def reload_all(self) -> None:
        """Force reload all data from disk."""
        self._lazy_rooms.reload()
        self._lazy_equipment.reload()
        self._lazy_skills.reload()
        logger.info("All data reloaded")


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

# Create global instance for convenience
_loader_instance: Optional[DataLoader] = None
_lazy_loader_instance: Optional[LazyDataLoader] = None


def get_data_loader() -> DataLoader:
    """Get global DataLoader instance"""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = DataLoader()
    return _loader_instance


def get_lazy_loader() -> LazyDataLoader:
    """Get global LazyDataLoader instance for optimized loading"""
    global _lazy_loader_instance
    if _lazy_loader_instance is None:
        _lazy_loader_instance = LazyDataLoader()
    return _lazy_loader_instance


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def load_rooms() -> Dict[str, Any]:
    """Quick function to load rooms"""
    return get_data_loader().get_rooms()

def load_equipment() -> Dict[str, Any]:
    """Quick function to load equipment"""
    return get_data_loader().get_equipment()

def load_skills() -> Dict[str, Any]:
    """Quick function to load skills"""
    return get_data_loader().get_skills()


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Data Loader Test")
    print("=" * 60)

    try:
        loader = DataLoader()

        # Test loading rooms
        print("\n1. Loading rooms...")
        rooms = loader.get_rooms()
        print(f"   ✓ Loaded {len(rooms['rooms'])} rooms")
        print(f"   Example: {list(rooms['rooms'].keys())[0]}")

        # Test specific room
        print("\n2. Loading specific room...")
        power_gen = loader.get_room('POWER_GENERATOR')
        if power_gen:
            print(f"   ✓ {power_gen['name']}: {power_gen['description']}")
            print(f"     Cost: {power_gen['cost']}, Production: {power_gen['production']}")

        # Test loading equipment
        print("\n3. Loading equipment...")
        equipment = loader.get_equipment()
        print(f"   ✓ Loaded {len(equipment['weapons'])} weapons")
        print(f"   ✓ Loaded {len(equipment['outfits'])} outfits")

        # Test specific weapon
        print("\n4. Loading specific weapon...")
        plasma = loader.get_weapon('plasma_gun')
        if plasma:
            print(f"   ✓ {plasma['name']}: {plasma['description']}")
            print(f"     Damage: {plasma['damage']}, Rarity: {plasma['rarity']}")

        # Test loading skills
        print("\n5. Loading skills...")
        skills = loader.get_skills()
        print(f"   ✓ Loaded {len(skills['skills'])} skills")

        # Test skills by category
        print("\n6. Loading combat skills...")
        combat_skills = loader.get_skills_by_category('combat')
        print(f"   ✓ Found {len(combat_skills)} combat skills")
        for skill_id, skill in combat_skills.items():
            print(f"     - {skill['name']}: {skill['description']}")

        # Test caching
        print("\n7. Testing cache...")
        import time
        start = time.time()
        loader.get_rooms()  # From cache
        cache_time = time.time() - start
        print(f"   ✓ Cache access took {cache_time*1000:.2f}ms")

        print("\n✅ All data loading tests passed!")

    except DataLoadError as e:
        print(f"\n❌ Data load error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise
