#!/usr/bin/env python3
"""
Game Constants Module
=====================
Centralized constants to eliminate magic numbers throughout the codebase.
All configurable values should be defined here for easy tuning.
"""

# =============================================================================
# ECHO CHAMBERS CONSTANTS
# =============================================================================

# Timeline Decay
DECAY_RATE_PER_TURN = 0.15  # How much timelines decay when not visited
DECAY_THRESHOLD_DECAYING = 4.0  # Decay level when timeline becomes "decaying"
DECAY_THRESHOLD_CORRUPTED = 8.0  # Decay level when timeline becomes "corrupted"

# Timeline Properties
PROPERTY_DRIFT_MIN = -2
PROPERTY_DRIFT_MAX = 2
PROPERTY_MIN = 0
PROPERTY_MAX = 10

# Event Generation
EVENT_PROPERTY_DRIFT_CHANCE = 0.3  # Chance for properties to drift in unvisited timelines
EVENT_MEMORY_CHANCE = 0.4  # Chance for memory fragment event
EVENT_CONVERGENCE_CHANCE = 0.15  # Chance for convergence event (requires 4+ timelines)

# Echo Propagation
ECHO_PROPAGATION_BASE_CHANCE = 0.4  # Base chance for echo to propagate
ECHO_PROPAGATION_HIGH_CHANCE = 0.7  # High propagation chance
ECHO_PROPAGATION_LOW_CHANCE = 0.3  # Low propagation chance

# Convergence
MIN_TIMELINES_FOR_CONVERGENCE = 4
CONVERGENCE_SAVE_BOTH_CHANCE = 0.5  # 50% chance to save both timelines in risky choice

# =============================================================================
# UI/DISPLAY CONSTANTS
# =============================================================================

# Progress Bars
PROGRESS_BAR_WIDTH = 12
PROGRESS_BAR_FILLED_CHAR = "█"
PROGRESS_BAR_EMPTY_CHAR = "░"

# Status Colors (RGB value thresholds)
STATUS_THRESHOLD_GOOD = 0.7  # Green when ratio >= 70%
STATUS_THRESHOLD_WARNING = 0.4  # Yellow when ratio >= 40%, Red below

# Terminal Effects
TYPEWRITER_DELAY = 0.03  # Seconds between characters
FADE_STEPS = 5  # Number of steps for fade effects
LOADING_ANIMATION_DELAY = 0.1  # Seconds between loading frames

# =============================================================================
# VAULT SHELTER CONSTANTS
# =============================================================================

# Starting Resources
STARTING_POWER = 100
STARTING_WATER = 100
STARTING_FOOD = 100
STARTING_CAPS = 500
STARTING_DWELLERS = 3

# Resource Limits
MAX_DWELLERS = 200
MAX_RESOURCE_CAPACITY = 1000
STORAGE_INCREASE_PER_ROOM = 100

# SPECIAL Stats
STAT_MIN = 1
STAT_MAX = 10
STAT_STARTING_MIN = 3
STAT_STARTING_MAX = 7

# Health & Happiness
BASE_HEALTH = 50
HEALTH_PER_ENDURANCE = 5
BASE_HAPPINESS = 50
HAPPINESS_MIN = 0
HAPPINESS_MAX = 100
HAPPINESS_DECAY_RATE = 0.1

# Room Costs (Base)
ROOM_COST_POWER_GENERATOR = 150
ROOM_COST_WATER_TREATMENT = 120
ROOM_COST_DINER = 100
ROOM_COST_LIVING_QUARTERS = 100
ROOM_COST_TRAINING_ROOM = 200
ROOM_COST_STORAGE_ROOM = 80
ROOM_COST_MEDBAY = 180
ROOM_COST_SCIENCE_LAB = 250

# Production Rates (per dweller per turn)
POWER_PRODUCTION_BASE = 5
WATER_PRODUCTION_BASE = 5
FOOD_PRODUCTION_BASE = 5

# Consumption Rates (per dweller per turn)
POWER_CONSUMPTION_PER_DWELLER = 1
WATER_CONSUMPTION_PER_DWELLER = 1
FOOD_CONSUMPTION_PER_DWELLER = 1

# Event Chances
EVENT_CHANCE_BASE = 0.2  # 20% chance per turn
EVENT_CHANCE_DISASTER = 0.05  # 5% chance for disasters
EVENT_CHANCE_POSITIVE = 0.5  # 50% of events are positive

# Combat
COMBAT_BASE_DAMAGE = 10
COMBAT_DAMAGE_VARIANCE = 5
RAIDER_BASE_HEALTH = 50
RAIDER_HEALTH_SCALING = 10  # Additional health per difficulty level

# Time Constants
AUTOSAVE_INTERVAL_DEFAULT = 60  # seconds
EXPEDITION_BASE_DURATION = 10  # turns
TRAINING_BASE_DURATION = 5  # turns
CONSTRUCTION_BASE_DURATION = 3  # turns

# =============================================================================
# DIFFICULTY MULTIPLIERS
# =============================================================================

DIFFICULTY_MULTIPLIERS = {
    'easy': {
        'resource_production': 1.5,
        'resource_consumption': 0.7,
        'event_frequency': 0.5,
        'disaster_frequency': 0.3,
        'enemy_damage': 0.7,
    },
    'normal': {
        'resource_production': 1.0,
        'resource_consumption': 1.0,
        'event_frequency': 1.0,
        'disaster_frequency': 1.0,
        'enemy_damage': 1.0,
    },
    'hard': {
        'resource_production': 0.8,
        'resource_consumption': 1.2,
        'event_frequency': 1.3,
        'disaster_frequency': 1.5,
        'enemy_damage': 1.3,
    },
    'survival': {
        'resource_production': 0.5,
        'resource_consumption': 1.5,
        'event_frequency': 2.0,
        'disaster_frequency': 2.0,
        'enemy_damage': 2.0,
    },
}

# =============================================================================
# WEATHER SYSTEM CONSTANTS
# =============================================================================

# Weather Duration (days)
WEATHER_DURATION_MIN = 1
WEATHER_DURATION_MAX = 8
WEATHER_FORECAST_DAYS = 5

# Weather Weights (for random selection)
WEATHER_WEIGHTS = {
    'CLEAR': 25,
    'CLOUDY': 20,
    'RAIN': 15,
    'STORM': 8,
    'RADIATION_STORM': 3,
    'DUST_STORM': 10,
    'ACID_RAIN': 2,
    'HEAT_WAVE': 8,
    'COLD_SNAP': 7,
    'FOG': 12,
}

# =============================================================================
# GAME BALANCE CONSTANTS
# =============================================================================

# Upgrade Costs
UPGRADE_COST_MULTIPLIER = 1.5  # Each upgrade costs 50% more
MAX_ROOM_UPGRADES = 3

# Experience/Leveling
XP_PER_LEVEL = 100
XP_SCALING_FACTOR = 1.2  # Each level requires 20% more XP
MAX_DWELLER_LEVEL = 50

# Skill Unlocks
SKILL_UNLOCK_LEVEL_TIER1 = 5
SKILL_UNLOCK_LEVEL_TIER2 = 10
SKILL_UNLOCK_LEVEL_TIER3 = 15

# Trading
TRADE_PRICE_VARIANCE = 0.2  # Prices vary by ±20%
TRADE_REPUTATION_MULTIPLIER = 0.1  # 10% discount per reputation level

# Faction Relations
FACTION_REPUTATION_MIN = -100
FACTION_REPUTATION_MAX = 100
FACTION_REPUTATION_HOSTILE_THRESHOLD = -50
FACTION_REPUTATION_ALLIED_THRESHOLD = 50

# =============================================================================
# NOTIFICATION SYSTEM
# =============================================================================

MAX_NOTIFICATIONS = 50
NOTIFICATION_DISPLAY_COUNT = 3  # Show 3 most recent by default
NOTIFICATION_PRIORITY_HIGH = 10
NOTIFICATION_PRIORITY_NORMAL = 5
NOTIFICATION_PRIORITY_LOW = 1

# =============================================================================
# PERFORMANCE CONSTANTS
# =============================================================================

# Logging
SLOW_FUNCTION_THRESHOLD = 0.1  # Log functions taking >100ms
MAX_LOG_FILE_SIZE = 10_000_000  # 10MB
MAX_LOG_FILES = 5

# Save Files
MAX_SAVE_SLOTS = 10
SAVE_COMPRESSION_LEVEL = 6  # 0-9, higher = smaller but slower
MAX_HISTORY_ENTRIES = 100  # Max history items to track

# Animation/UI
MIN_FRAME_TIME = 0.016  # ~60 FPS cap
MAX_PARTICLES = 100
SPARKLINE_WIDTH = 10

# =============================================================================
# FILE PATHS
# =============================================================================

# Config Files
CONFIG_FILE_NAME = 'config.json'
SETTINGS_FILE_NAME = 'settings.json'
ACHIEVEMENTS_FILE_NAME = 'achievements.json'
LEADERBOARD_FILE_NAME = 'leaderboard.json'

# Save Files
DEFAULT_SAVE_NAME = 'vault_save.json'
AUTOSAVE_NAME = 'autosave.json'
BACKUP_SUFFIX = '.backup'

# =============================================================================
# VALIDATION RANGES
# =============================================================================

# Settings Validation
ANIMATION_SPEED_MIN = 0.5
ANIMATION_SPEED_MAX = 2.0
VOLUME_MIN = 0.0
VOLUME_MAX = 1.0
AUTOSAVE_INTERVAL_MIN = 10
AUTOSAVE_INTERVAL_MAX = 600

# =============================================================================
# ERROR MESSAGES
# =============================================================================

ERROR_INSUFFICIENT_RESOURCES = "Insufficient resources"
ERROR_NO_AVAILABLE_DWELLERS = "No available dwellers"
ERROR_ROOM_FULL = "Room is at capacity"
ERROR_INVALID_POSITION = "Invalid position"
ERROR_SAVE_FAILED = "Failed to save game"
ERROR_LOAD_FAILED = "Failed to load game"

# =============================================================================
# SUCCESS MESSAGES
# =============================================================================

SUCCESS_ROOM_BUILT = "Room constructed successfully"
SUCCESS_DWELLER_ASSIGNED = "Dweller assigned"
SUCCESS_GAME_SAVED = "Game saved successfully"
SUCCESS_GAME_LOADED = "Game loaded successfully"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def validate_stat(value: int) -> int:
    """Clamp stat value to valid range"""
    return max(STAT_MIN, min(STAT_MAX, value))

def validate_happiness(value: float) -> float:
    """Clamp happiness to valid range"""
    return max(HAPPINESS_MIN, min(HAPPINESS_MAX, value))

def validate_resource(value: int, max_capacity: int = MAX_RESOURCE_CAPACITY) -> int:
    """Clamp resource to valid range"""
    return max(0, min(max_capacity, value))

def get_difficulty_multiplier(difficulty: str, stat: str) -> float:
    """Get difficulty multiplier for a specific stat"""
    return DIFFICULTY_MULTIPLIERS.get(difficulty.lower(), DIFFICULTY_MULTIPLIERS['normal']).get(stat, 1.0)


if __name__ == '__main__':
    # Test constants
    print("Game Constants Module")
    print("=" * 50)
    print(f"Decay rate per turn: {DECAY_RATE_PER_TURN}")
    print(f"Starting dwellers: {STARTING_DWELLERS}")
    print(f"Max dwellers: {MAX_DWELLERS}")
    print(f"SPECIAL stat range: {STAT_MIN}-{STAT_MAX}")
    print()
    print("Difficulty Multipliers (Normal):")
    for key, value in DIFFICULTY_MULTIPLIERS['normal'].items():
        print(f"  {key}: {value}")
