# Quick Start Guide for New Improvements

## 🚀 What's New?

Your codebase now has professional-grade infrastructure! Here's what was added:

## 📦 New Files

### Core Infrastructure
1. **constants.py** - All magic numbers in one place
2. **logging_config.py** - Professional logging system
3. **base_game.py** - Base class for all games
4. **event_generators.py** - Refactored event system (example)

### Testing
5. **tests/** - Complete test suite with pytest
6. **pytest.ini** - Test configuration
7. **requirements-dev.txt** - Development dependencies

### Documentation
8. **IMPROVEMENTS.md** - Detailed documentation
9. **QUICK_START.md** - This file!

## 🎯 How to Use

### Run Tests
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_constants.py -v
```

### Use Constants
```python
# OLD WAY ❌
timeline.decay_level += turns_away * 0.15  # What is 0.15?
stat = max(1, min(10, value))  # Magic numbers!

# NEW WAY ✅
from constants import DECAY_RATE_PER_TURN, validate_stat
timeline.decay_level += turns_away * DECAY_RATE_PER_TURN
stat = validate_stat(value)
```

### Use Logging
```python
# OLD WAY ❌
print(f"Loading game...")
print(f"Warning: {error}")

# NEW WAY ✅
from logging_config import get_logger

logger = get_logger(__name__)
logger.info("Loading game...")
logger.warning(f"Error occurred: {error}")
```

### Create New Games
```python
# OLD WAY ❌
# Copy/paste 200 lines of boilerplate from another game

# NEW WAY ✅
from base_game import TurnBasedGame, GameMetadata

class MyNewGame(TurnBasedGame):
    def __init__(self):
        metadata = GameMetadata(
            name="My Game",
            version="1.0",
            description="Cool game"
        )
        super().__init__(metadata)
        # All terminal management, logging, state handling included!

    def setup(self): pass
    def update(self): pass
    def render(self): pass
    def handle_input(self, key): pass
    def cleanup(self): pass

# That's it! You get logging, performance tracking, error handling for free!
```

## 📊 Test Coverage

Current test coverage:
- ✅ Constants validation (12 tests)
- ✅ Config management (10 tests)
- ✅ Platform detection (9 tests)
- 📝 Game logic (TODO - add tests for your games!)

## 🎓 Learn by Example

### Example 1: Performance Logging
```python
from logging_config import get_logger, log_performance

logger = get_logger(__name__)

@log_performance(logger, threshold=0.1)
def slow_function():
    """Automatically logs if this takes > 100ms"""
    # ... your code ...
```

### Example 2: Context Logging
```python
from logging_config import log_context

with log_context(logger, "Saving game"):
    save_game_data()
    # Automatically logs start/end and duration
```

### Example 3: Custom Event Generator
```python
from event_generators import EventGenerator, Event, EventChoice

class MyCustomGenerator(EventGenerator):
    def can_generate(self, context):
        return context.get('special_condition') == True

    def generate(self, context):
        return Event(
            name="My Event",
            description="Something cool happens",
            choices=[
                EventChoice(text="Do thing", effects={"stat": 1}),
                EventChoice(text="Do other thing", effects={"stat": -1}),
            ]
        )

# Add to manager
manager.add_generator(MyCustomGenerator())
```

## 🐛 Debugging

### View Logs
```bash
# Logs are saved to:
# - Linux: ~/.local/share/vault13/logs/
# - macOS: ~/Library/Application Support/vault13/logs/
# - Windows: %APPDATA%/vault13/logs/

# View latest log
tail -f ~/.local/share/vault13/logs/vault13.log
```

### Run Tests with Debugging
```bash
# Drop into debugger on failure
pytest --pdb

# Verbose output
pytest -vv

# Show print statements
pytest -s
```

## 🔥 Quick Wins

### Replace Magic Numbers (5 min)
1. Find magic number: `if ratio >= 0.7:`
2. Add to constants.py: `STATUS_THRESHOLD_GOOD = 0.7`
3. Replace: `if ratio >= STATUS_THRESHOLD_GOOD:`

### Add Logging (2 min)
1. Import: `from logging_config import get_logger`
2. Get logger: `logger = get_logger(__name__)`
3. Use: `logger.info("Something happened")`

### Write a Test (10 min)
1. Create `tests/test_myfeature.py`
2. Write test:
```python
def test_my_feature():
    result = my_function(5)
    assert result == 10
```
3. Run: `pytest tests/test_myfeature.py -v`

## 📚 Next Steps

1. **Update one game** - Pick a small game and make it use BaseGame
2. **Write 5 tests** - Test critical game logic
3. **Replace 10 magic numbers** - Move to constants.py
4. **Add logging** - To 3 important functions

## 💡 Tips

- Start small - Don't refactor everything at once
- Write tests before refactoring - Safety net!
- Use constants for ALL tunable values
- Log important operations for debugging
- Run tests frequently

## 🆘 Troubleshooting

**Tests not running?**
```bash
pip install -r requirements-dev.txt
```

**Import errors?**
```bash
# Make sure you're in the project root
cd /home/user/Claude
export PYTHONPATH=.
```

**Logs not appearing?**
```python
from logging_config import get_logger
logger = get_logger(__name__)
logger.info("This should appear!")
```

## 📞 Need Help?

- Read IMPROVEMENTS.md for detailed docs
- Check test files for examples
- Run `python constants.py` to test constants
- Run `python logging_config.py` to test logging
- Run `python base_game.py` to see example game

---

**Happy coding! 🎮**
