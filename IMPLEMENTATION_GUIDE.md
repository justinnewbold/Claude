# Complete Implementation Guide

## 🎯 Overview

This guide shows you how to use the complete Vault 13 game development framework in your projects.

---

## 🚀 Quick Start (5 Minutes)

### Create Your First Game

```python
#!/usr/bin/env python3
from base_game import TurnBasedGame, GameMetadata
from validation import get_menu_choice
from logging_config import get_logger

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(GameMetadata(
            name="My First Game",
            version="1.0",
            description="A simple game"
        ))
        self.logger = get_logger(__name__)
        self.score = 0

    def setup(self):
        print("Welcome to My First Game!")

    def render(self):
        self.clear_screen()
        self.print_header(f"Score: {self.score}")

    def handle_input(self, key=None):
        options = ["Add Point", "Remove Point", "Quit"]
        choice = get_menu_choice(options)

        if choice == 1:
            self.score += 1
        elif choice == 2:
            self.score -= 1
        elif choice == 3:
            self.quit()

    def update(self):
        pass  # Game logic here

    def cleanup(self):
        print(f"Final score: {self.score}")

if __name__ == '__main__':
    game = MyGame()
    game.run()
```

Run it:
```bash
python my_game.py
```

---

## 📦 Feature Integration

### Add Save/Load

```python
from save_system import get_save_system

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.save_system = get_save_system()

    def save_game(self):
        self.save_system.save(
            game_id='my_game',
            game_name='My Game',
            data={'score': self.score, 'level': self.level},
            save_slot=1
        )
        print("Game saved!")

    def load_game(self):
        save_file = self.save_system.load('my_game', save_slot=1)
        if save_file:
            self.score = save_file.data['score']
            self.level = save_file.data['level']
            print("Game loaded!")
```

### Add Achievements

```python
from achievements import AchievementSystem, Achievement, AchievementCategory, AchievementRarity

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.achievements = AchievementSystem('my_game')
        self._setup_achievements()

    def _setup_achievements(self):
        self.achievements.register_achievement(Achievement(
            id="score_100",
            name="Century",
            description="Reach 100 points",
            category=AchievementCategory.PROGRESSION,
            rarity=AchievementRarity.UNCOMMON,
            points=15,
            icon="🏆",
            requirements={'score': 100}
        ))

    def update(self):
        # Track progress
        self.achievements.update_progress('score_100', {
            'score': self.score
        })
```

### Add Configuration

```python
from config_manager import get_config

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.config = get_config()

    def setup(self):
        # Check if tutorial should be shown
        if self.config.should_show_tutorial():
            self.show_tutorial()

        # Use text speed setting
        delay = self.config.get_text_delay()

    def print_slowly(self, text):
        import time
        delay = self.config.get_text_delay()
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
```

### Add Tutorials

```python
from tutorial_system import TutorialSystem, TutorialBuilder

# Create tutorial
builder = TutorialBuilder('my_game')
builder.add_info(
    id='welcome',
    title='Welcome!',
    message='Welcome to My Game!'
).add_action(
    id='first_move',
    title='Make Your First Move',
    message='Press 1 to add a point',
    required_action='add_point',
    reward='Great! You earned a point.'
)
builder.build(Path('data/my_game_tutorial.json'))

# In game
class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.tutorial = TutorialSystem('my_game')

    def setup(self):
        if self.tutorial.is_active():
            self.tutorial.show_current_step()

    def handle_input(self, key=None):
        # ... handle input ...

        # Check tutorial
        if choice == 1:
            self.tutorial.check_action('add_point')
```

### Add Mod Support

```python
from mod_loader import ModLoader

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.mods = ModLoader('my_game')
        self.mods.load_all_mods()

    def load_items(self):
        # Load base items
        base_items = {'sword': {'damage': 10}}

        # Merge with mod items
        all_items = self.mods.merge_data(base_items, 'items')

        return all_items
```

### Add Localization

```python
from localization import get_localization

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.loc = get_localization('my_game')

        # Set language from config
        lang = self.config.load_game_config('my_game').get('language', 'en')
        self.loc.set_language(lang)

    def render(self):
        # Use localized strings
        print(self.loc.get('ui.main_menu'))
        print(self.loc.get('game.score', score=self.score))

        # Pluralization
        print(self.loc.get_plural('items.count', len(self.inventory)))
```

### Add Analytics

```python
from analytics import get_analytics, track_game_start, track_game_end, EventType

class MyGame(TurnBasedGame):
    def __init__(self):
        super().__init__(...)
        self.analytics = get_analytics()

    def setup(self):
        if self.analytics.is_enabled():
            track_game_start('my_game', {'version': '1.0'})

    def on_level_up(self):
        if self.analytics.is_enabled():
            self.analytics.track_event(EventType.LEVEL_UP, {
                'level': self.level
            })

    def cleanup(self):
        if self.analytics.is_enabled():
            track_game_end()
```

---

## 🎮 Complete Game Template

```python
#!/usr/bin/env python3
"""
Complete Game Template
Shows all features integrated
"""

from base_game import TurnBasedGame, GameMetadata
from validation import get_menu_choice, get_yes_no_input
from logging_config import get_logger
from config_manager import get_config
from save_system import get_save_system
from achievements import AchievementSystem
from tutorial_system import TutorialSystem
from mod_loader import ModLoader
from analytics import get_analytics, track_game_start, track_game_end
from localization import get_localization


class CompleteGame(TurnBasedGame):
    """A complete game using all infrastructure"""

    def __init__(self):
        super().__init__(GameMetadata(
            name="Complete Game",
            version="1.0",
            description="Full-featured game template"
        ))

        # Initialize all systems
        self.logger = get_logger(__name__)
        self.config = get_config()
        self.save_system = get_save_system()
        self.achievements = AchievementSystem('complete_game')
        self.tutorial = TutorialSystem('complete_game')
        self.mods = ModLoader('complete_game')
        self.analytics = get_analytics()
        self.loc = get_localization('complete_game')

        # Game state
        self.score = 0
        self.level = 1

        # Load mods
        self.mods.load_all_mods()

        # Start analytics
        if self.analytics.is_enabled():
            track_game_start('complete_game', {'version': '1.0'})

    def setup(self):
        # Show tutorial if needed
        if self.config.should_show_tutorial() and self.tutorial.is_active():
            self.tutorial.show_current_step()

        self.logger.info("Game started")

    def render(self):
        self.clear_screen()
        self.print_header(self.loc.get('game.title'))

        print(f"\n{self.loc.get('game.score')}: {self.score}")
        print(f"{self.loc.get('game.level')}: {self.level}")

        # Show tutorial if active
        if self.tutorial.is_active():
            step = self.tutorial.get_current_step()
            if step:
                print(f"\n💡 {step.hint}")

    def handle_input(self, key=None):
        options = [
            self.loc.get('action.play'),
            self.loc.get('action.save'),
            self.loc.get('action.load'),
            self.loc.get('action.quit')
        ]

        choice = get_menu_choice(options)

        if choice == 1:
            self.play_turn()
        elif choice == 2:
            self.save_game()
        elif choice == 3:
            self.load_game()
        elif choice == 4:
            if get_yes_no_input(self.loc.get('msg.confirm_quit')):
                self.quit()

    def play_turn(self):
        self.score += 10
        self.logger.debug(f"Score increased to {self.score}")

        # Check tutorial
        self.tutorial.check_condition('score', self.score)

        # Update achievements
        self.achievements.update_progress('score_100', {'score': self.score})

    def update(self):
        # Auto-save
        if self.config.should_auto_save():
            if self.turn % self.config.gameplay.auto_save_interval == 0:
                self.save_game()

    def save_game(self):
        self.save_system.save(
            game_id='complete_game',
            game_name='Complete Game',
            data={'score': self.score, 'level': self.level, 'turn': self.turn},
            save_slot=1,
            play_time=self.turn * 10
        )
        print(self.loc.get('msg.game_saved'))
        self.logger.info("Game saved")

    def load_game(self):
        save_file = self.save_system.load('complete_game', save_slot=1)
        if save_file:
            self.score = save_file.data['score']
            self.level = save_file.data['level']
            self.turn = save_file.data['turn']
            print(self.loc.get('msg.game_loaded'))
            self.logger.info("Game loaded")

    def cleanup(self):
        if self.analytics.is_enabled():
            track_game_end()

        self.logger.info(f"Game ended - Score: {self.score}, Level: {self.level}")
        print(f"\n{self.loc.get('msg.thanks_for_playing')}")


def main():
    game = CompleteGame()
    game.run()


if __name__ == '__main__':
    main()
```

---

## 🔧 Testing Your Game

### Unit Tests

```python
# tests/test_my_game.py
import pytest
from my_game import MyGame

def test_game_creation():
    game = MyGame()
    assert game.score == 0

def test_add_point():
    game = MyGame()
    game.score += 1
    assert game.score == 1

def test_save_load():
    game = MyGame()
    game.score = 100
    game.save_game()

    game2 = MyGame()
    game2.load_game()
    assert game2.score == 100
```

Run tests:
```bash
pytest tests/
```

### Type Checking

```bash
mypy my_game.py --ignore-missing-imports
```

---

## 📦 Creating Mods

### 1. Create Mod Structure

```bash
python -c "from mod_loader import ModCreator; ModCreator.create_mod_template('awesome_mod', 'Awesome Mod', 'Your Name', 'my_game', Path('mods/my_game'))"
```

### 2. Edit mod.json

```json
{
  "id": "awesome_mod",
  "name": "Awesome Mod",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "Adds awesome new content",
  "type": "content",
  "game_id": "my_game",
  "game_version": "1.0",
  "dependencies": [],
  "enabled": true
}
```

### 3. Add Data Files

```json
// mods/my_game/awesome_mod/data/items.json
{
  "cool_sword": {
    "name": "Cool Sword",
    "damage": 50,
    "description": "A very cool sword"
  }
}
```

### 4. Add Code (Optional)

```python
# mods/my_game/awesome_mod/mod.py
def init(mod_loader):
    print("Awesome Mod loaded!")

def on_game_start(game):
    print("Awesome Mod: Game started!")
```

---

## 🌍 Adding Translations

### 1. Create Translation Template

```python
from localization import TranslationCreator

TranslationCreator.create_template(
    game_id='my_game',
    language_code='es',
    language_name='Español',
    author='Your Name'
)
```

### 2. Translate Strings

```json
// localization/my_game/es.json
{
  "metadata": {
    "language_code": "es",
    "language_name": "Español",
    "completion_percent": 100.0
  },
  "translations": {
    "ui": {
      "yes": "Sí",
      "no": "No"
    },
    "game": {
      "score": "Puntuación",
      "level": "Nivel"
    },
    "msg": {
      "game_saved": "¡Juego guardado!",
      "thanks_for_playing": "¡Gracias por jugar!"
    }
  }
}
```

---

## ⚙️ Configuration

Users can customize:

```bash
# Open settings
python -c "from config_manager import show_settings_menu; show_settings_menu()"
```

Settings stored in: `~/.vault13/config.json`

---

## 📊 Analytics Dashboard

```bash
# View analytics
python -c "from analytics import show_analytics_dashboard; show_analytics_dashboard()"
```

Data stored in: `~/.vault13/analytics/`

---

## 🎓 Best Practices

1. **Always extend TurnBasedGame** for game loop
2. **Use validation.py** for all input (prevents crashes)
3. **Use logging** instead of print for debugging
4. **Add achievements** for replay value
5. **Support mods** from day one
6. **Localize** your game (11 languages supported)
7. **Write tests** for critical functionality
8. **Use configuration** for customization
9. **Respect privacy** (analytics opt-in only)
10. **Document** your code

---

## 🚀 Deployment

### 1. Organize Files

```
my_game/
├── my_game.py
├── data/
│   ├── my_game_tutorial.json
│   ├── rooms.json
│   └── items.json
├── localization/
│   └── my_game/
│       ├── en.json
│       └── es.json
├── mods/
│   └── my_game/
│       └── (community mods)
├── requirements.txt
└── README.md
```

### 2. Create requirements.txt

```
pytest>=7.4.0
mypy>=1.5.0
```

### 3. Package

```bash
python setup.py sdist
```

---

## 📚 Further Reading

- **IMPROVEMENTS_ROUND1.md** - Foundation infrastructure
- **IMPROVEMENTS_ROUND2.md** - Utilities and data
- **IMPROVEMENTS_ROUND3.md** - Game features
- **IMPROVEMENTS_ROUND4.md** - Advanced features
- **QUICK_START.md** - 5-minute tutorial
- **IMPROVEMENTS_SUMMARY.md** - Complete overview

---

## 💬 Support

For issues and questions:
- Check documentation in `.md` files
- Review code examples in this guide
- Look at test files for usage examples
- Check `echo_chambers_refactored_demo.py` for complete example

---

**Happy Game Development! 🎮**
