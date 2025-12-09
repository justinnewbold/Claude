# Repository Structure

This document explains the organization of the Vault 13 Game Development Framework repository after Round 6 refactoring.

## Overview

The repository has been reorganized to follow clean architecture principles with clear separation between:
- **Infrastructure** - Core framework modules
- **Games** - Individual game implementations
- **Legacy** - Historical versions for reference

## Directory Structure

```
Claude/
├── infrastructure/          # Core game development framework
│   ├── __init__.py         # Main exports
│   ├── base_game.py        # TurnBasedGame base class
│   ├── save_system.py      # Save/load functionality
│   ├── achievements.py     # Achievement system
│   ├── config_manager.py   # Configuration management
│   ├── tutorial_system.py  # Tutorial framework
│   ├── mod_loader.py       # Mod support
│   ├── analytics.py        # Analytics tracking
│   ├── localization.py     # I18n support
│   ├── validation.py       # Input validation
│   ├── logging_config.py   # Logging setup
│   ├── error_handling.py   # Error handling utilities
│   ├── data_loader.py      # Data loading utilities
│   ├── game_utils.py       # Game utilities
│   ├── constants.py        # Shared constants
│   ├── event_generators.py # Event generation
│   └── platform_utils.py   # Platform detection
│
├── games/                  # Game implementations
│   ├── schrodingers_dungeon_refactored.py
│   ├── echo_chambers_refactored_demo.py
│   └── ...more games...
│
├── vault_shelter_refactored/  # Refactored Vault Shelter (modular)
│   ├── __init__.py           # Package exports
│   ├── dweller.py            # Dweller class and utilities
│   ├── room.py               # Room class and production
│   ├── resources.py          # Resource management
│   └── game.py               # Main game class
│
├── games_legacy/           # Historical versions
│   ├── vault_shelter_v4.py
│   ├── vault_shelter_v5.py
│   ├── vault_shelter_v5.5.py
│   └── vault_shelter_v5.5_additions.py
│
├── tests/                  # Test suites
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
│
├── tools/                  # Development tools
│
├── docs/                   # Documentation
│   └── api/               # API documentation
│
├── mods/                   # Community mods
│
├── localization/           # Translation files
│
├── vault_shelter_v6.py     # Current monolithic version (6,983 lines)
│
└── README.md              # Main repository README
```

## Key Changes in Round 6

### 1. Infrastructure Organization
All core framework modules have been moved to `infrastructure/` with a clean `__init__.py` that exports the most commonly used components.

**Usage:**
```python
from infrastructure import TurnBasedGame, GameMetadata, get_save_system, get_config
```

### 2. Vault Shelter Refactoring
The massive 6,983-line `vault_shelter_v6.py` has been refactored into modular components:

**Before:** One massive file
```
vault_shelter_v6.py (6,983 lines, 64 classes)
```

**After:** Clean modular structure
```
vault_shelter_refactored/
├── __init__.py      # Clean exports
├── dweller.py       # ~380 lines - Dweller class, SPECIAL stats, relationships
├── room.py          # ~400 lines - Room class, production, upgrades
├── resources.py     # ~350 lines - Resource management, consumption
└── game.py          # ~640 lines - Main game logic
```

**Benefits:**
- ✅ Each file is ~300-600 lines (manageable size)
- ✅ Clear separation of concerns
- ✅ Easy to test individual components
- ✅ Multiple developers can work in parallel
- ✅ Import only what you need

**Usage:**
```python
from vault_shelter_refactored import (
    Dweller,
    Room,
    ResourceManager,
    VaultShelterRefactored
)
```

### 3. Game Organization
All refactored games have been moved to `games/` directory for easy discovery.

### 4. Legacy Preservation
Old versions (v4, v5, v5.5) moved to `games_legacy/` for historical reference and comparison.

## Module Details

### Infrastructure Modules

#### base_game.py
Base class for turn-based games with:
- Game loop management
- Screen clearing
- Header formatting
- Metadata tracking

#### save_system.py
Complete save/load system with:
- Multiple save slots
- JSON persistence
- Metadata tracking
- Backup functionality

#### achievements.py
Achievement system featuring:
- Achievement definitions
- Progress tracking
- Statistics
- Categories and rarity levels

#### config_manager.py
Configuration management with:
- Settings persistence
- Default values
- Interactive settings menu

### Vault Shelter Refactored Modules

#### dweller.py
**Dweller Class:**
- Full SPECIAL stat system (Strength, Perception, Endurance, Charisma, Intelligence, Agility, Luck)
- Relationships and affection tracking
- Experience and leveling
- Skill learning
- Equipment bonuses
- Trait system
- Age and gender tracking

**Utility Functions:**
- `create_random_dweller()` - Generate dweller with random stats
- `calculate_child_stats()` - Calculate child stats from parents
- `get_relationship_status()` - Get relationship status from affection
- `format_dweller_card()` - Format dweller details

#### room.py
**Room Class:**
- 15 room types (Power, Water, Garden, etc.)
- Production calculation with bonuses
- Dweller assignment
- Room upgrades (levels 1-3)
- Rush mechanic
- Incident resolution

**Utility Functions:**
- `calculate_adjacency_bonus()` - Bonus from adjacent rooms
- `get_room_icon()` - Get icon for room type
- `get_room_name()` - Get name for room type

#### resources.py
**ResourceManager Class:**
- Resource tracking (power, water, food, caps, stimpaks, radaway)
- Storage capacity management
- Consumption calculation
- Multi-resource transactions
- Resource history
- Shortage prediction

**Utility Functions:**
- `format_resource_bar()` - Format resource with progress bar
- `calculate_optimal_production()` - Calculate optimal production levels
- `predict_shortage()` - Predict when resources will run out

#### game.py
**VaultShelterRefactored Class:**
Main game class that integrates all modules:
- Dweller management
- Room building and management
- Resource production/consumption
- Event system
- Achievement tracking
- Save/load integration

## Import Patterns

### Using Infrastructure
```python
# Old way (scattered imports)
from base_game import TurnBasedGame
from save_system import get_save_system
from achievements import AchievementSystem

# New way (clean package import)
from infrastructure import (
    TurnBasedGame,
    GameMetadata,
    get_save_system,
    AchievementSystem,
    get_config,
    get_logger
)
```

### Using Vault Shelter Modules
```python
# Import specific components
from vault_shelter_refactored.dweller import Dweller, create_random_dweller
from vault_shelter_refactored.room import Room, RoomType
from vault_shelter_refactored.resources import ResourceManager

# Or import everything
from vault_shelter_refactored import (
    Dweller,
    Room,
    ResourceManager,
    VaultShelterRefactored
)
```

## Development Workflow

### Creating a New Game

1. Import infrastructure:
```python
from infrastructure import TurnBasedGame, GameMetadata
```

2. Create game class:
```python
class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(GameMetadata(
            name="My Game",
            version="1.0",
            description="Description"
        ))
```

3. Implement required methods:
- `setup()` - Initialize game
- `render()` - Display game state
- `handle_input()` - Process player input
- `update()` - Update game state
- `cleanup()` - Cleanup on exit

### Running Tests
```bash
pytest tests/unit/           # Unit tests
pytest tests/integration/    # Integration tests
pytest                       # All tests
```

## Migration Guide

### From Old Structure to New

**Old:**
```python
# Direct imports from root
from base_game import TurnBasedGame
from save_system import SaveSystem
```

**New:**
```python
# Import from infrastructure package
from infrastructure import TurnBasedGame, get_save_system
```

**Old (Monolithic):**
```python
# Everything in one file
class VaultGame:
    # 6,983 lines...
```

**New (Modular):**
```python
# Clean imports
from vault_shelter_refactored import (
    Dweller,
    Room,
    ResourceManager,
    VaultShelterRefactored
)

# Use specific components
resources = ResourceManager()
dweller = Dweller(name="Sarah")
room = Room(room_type=RoomType.POWER_GENERATOR, floor=0, position=0)
```

## Benefits of New Structure

### For Developers
- 📦 **Modular** - Work on specific components without touching everything
- 🧪 **Testable** - Easy to test individual modules
- 📖 **Readable** - Each file is ~300-600 lines, not 6,983
- 🔧 **Maintainable** - Clear separation of concerns
- 🚀 **Scalable** - Easy to add new features

### For the Codebase
- ✅ Clean import structure
- ✅ No circular dependencies
- ✅ Proper package organization
- ✅ Reusable components
- ✅ Clear documentation

## Next Steps

1. **Continue Refactoring** - Extract more classes from vault_shelter_v6.py:
   - Quest system
   - Technology/Research
   - Policy system
   - Disaster system
   - Combat system

2. **Add More Games** - Move additional games to `games/` directory

3. **Improve Documentation** - Add docstrings and type hints

4. **Write More Tests** - Increase test coverage

5. **Create CLI Tool** - Game launcher and development tools

## Related Documentation

- `README.md` - Main repository README
- `IMPLEMENTATION_GUIDE.md` - Detailed implementation guide
- `IMPROVEMENTS_ROUND*.md` - Improvement logs
- `docs/api/` - API documentation

## Questions?

Check the main README or implementation guide for more details.
