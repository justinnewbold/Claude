"""
Vault Shelter Refactored
=========================
Modular refactoring of vault_shelter_v6.py demonstrating clean architecture.

This package demonstrates:
- Separation of concerns (Dweller, Room, Resources)
- Clean imports
- Maintainable codebase
- Proper module organization

Modules:
- dweller.py: Dweller class and related utilities
- room.py: Room class, room types, and production logic
- resources.py: ResourceManager for vault resources
- game.py: Main game class integrating all modules
"""

from vault_shelter_refactored.dweller import (
    Dweller,
    create_random_dweller,
    calculate_child_stats,
    get_relationship_status
)

from vault_shelter_refactored.room import (
    Room,
    RoomType,
    RoomConfig,
    DEFAULT_ROOM_CONFIGS,
    calculate_adjacency_bonus,
    get_room_icon,
    get_room_name
)

from vault_shelter_refactored.resources import (
    ResourceManager,
    ResourceType,
    format_resource_bar,
    calculate_optimal_production,
    predict_shortage
)

from vault_shelter_refactored.game import VaultShelterRefactored

__all__ = [
    # Dweller exports
    'Dweller',
    'create_random_dweller',
    'calculate_child_stats',
    'get_relationship_status',

    # Room exports
    'Room',
    'RoomType',
    'RoomConfig',
    'DEFAULT_ROOM_CONFIGS',
    'calculate_adjacency_bonus',
    'get_room_icon',
    'get_room_name',

    # Resource exports
    'ResourceManager',
    'ResourceType',
    'format_resource_bar',
    'calculate_optimal_production',
    'predict_shortage',

    # Game export
    'VaultShelterRefactored',
]
