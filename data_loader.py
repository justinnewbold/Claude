#!/usr/bin/env python3
"""
Data Loader Module
==================
Loads game data from JSON files.
Provides caching and validation.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

from logging_config import get_logger

logger = get_logger(__name__)


class DataLoadError(Exception):
    """Raised when data loading fails"""
    pass


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

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize data loader.

        Args:
            data_dir: Directory containing JSON files (default: ./data/)
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / 'data'

        self.data_dir = Path(data_dir)
        self._cache: Dict[str, Any] = {}

        logger.info(f"DataLoader initialized with data_dir: {self.data_dir}")

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

            # Cache it
            self._cache[filename] = data

            return data

        except json.JSONDecodeError as e:
            raise DataLoadError(f"Invalid JSON in {filename}: {e}")
        except Exception as e:
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
# GLOBAL INSTANCE
# =============================================================================

# Create global instance for convenience
_loader_instance: Optional[DataLoader] = None

def get_data_loader() -> DataLoader:
    """Get global DataLoader instance"""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = DataLoader()
    return _loader_instance


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
