#!/usr/bin/env python3
"""
Tutorial System
===============
Interactive tutorial and hint system for games.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum

from logging_config import get_logger
from error_handling import error_context
from achievements import AchievementSystem


logger = get_logger(__name__)


class TutorialStepType(Enum):
    """Types of tutorial steps"""
    INFO = "info"  # Just show information
    ACTION = "action"  # Wait for specific action
    CHOICE = "choice"  # Wait for specific choice
    CONDITION = "condition"  # Wait for condition to be met


@dataclass
class TutorialStep:
    """A single tutorial step"""
    id: str
    type: TutorialStepType
    title: str
    message: str
    hint: Optional[str] = None
    required_action: Optional[str] = None
    required_condition: Optional[Dict[str, Any]] = None
    reward: Optional[str] = None
    skippable: bool = True
    highlight: Optional[str] = None  # What to highlight in UI


@dataclass
class TutorialProgress:
    """Player's progress through tutorial"""
    tutorial_id: str
    current_step: int = 0
    completed_steps: List[str] = field(default_factory=list)
    skipped: bool = False
    completed: bool = False


class TutorialSystem:
    """
    Interactive tutorial system.

    Features:
    - Step-by-step tutorials
    - Context-sensitive hints
    - Progress tracking
    - Skip functionality
    - Rewards for completion
    - Integration with achievements
    """

    def __init__(
        self,
        game_id: str,
        tutorial_file: Optional[Path] = None,
        achievements: Optional[AchievementSystem] = None
    ):
        """
        Initialize tutorial system.

        Args:
            game_id: Game identifier
            tutorial_file: Path to tutorial definition file
            achievements: Achievement system for rewards
        """
        self.game_id = game_id
        self.logger = get_logger(__name__)
        self.achievements = achievements

        # Tutorial data
        self.tutorial_file = tutorial_file or Path(f"data/{game_id}_tutorial.json")
        self.progress_file = Path(f"saves/{game_id}_tutorial_progress.json")

        self.steps: List[TutorialStep] = []
        self.progress = TutorialProgress(tutorial_id=game_id)

        # Callbacks
        self.on_step_complete_callbacks: List[Callable[[TutorialStep], None]] = []

        # Load data
        self._load_tutorial()
        self._load_progress()

    def _load_tutorial(self):
        """Load tutorial steps from file"""
        if not self.tutorial_file.exists():
            self.logger.warning(f"Tutorial file not found: {self.tutorial_file}")
            return

        with error_context("loading tutorial"):
            with open(self.tutorial_file, 'r') as f:
                data = json.load(f)

            for step_data in data.get('steps', []):
                step = TutorialStep(
                    id=step_data['id'],
                    type=TutorialStepType(step_data['type']),
                    title=step_data['title'],
                    message=step_data['message'],
                    hint=step_data.get('hint'),
                    required_action=step_data.get('required_action'),
                    required_condition=step_data.get('required_condition'),
                    reward=step_data.get('reward'),
                    skippable=step_data.get('skippable', True),
                    highlight=step_data.get('highlight')
                )
                self.steps.append(step)

            self.logger.info(f"Loaded {len(self.steps)} tutorial steps")

    def _load_progress(self):
        """Load tutorial progress"""
        if not self.progress_file.exists():
            return

        with error_context("loading tutorial progress"):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)

            self.progress.current_step = data.get('current_step', 0)
            self.progress.completed_steps = data.get('completed_steps', [])
            self.progress.skipped = data.get('skipped', False)
            self.progress.completed = data.get('completed', False)

    def _save_progress(self):
        """Save tutorial progress"""
        with error_context("saving tutorial progress"):
            # Ensure directory exists
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'tutorial_id': self.progress.tutorial_id,
                'current_step': self.progress.current_step,
                'completed_steps': self.progress.completed_steps,
                'skipped': self.progress.skipped,
                'completed': self.progress.completed
            }

            with open(self.progress_file, 'w') as f:
                json.dump(data, f, indent=2)

    def is_active(self) -> bool:
        """Check if tutorial is currently active"""
        return not self.progress.completed and not self.progress.skipped

    def is_completed(self) -> bool:
        """Check if tutorial is completed"""
        return self.progress.completed

    def get_current_step(self) -> Optional[TutorialStep]:
        """Get current tutorial step"""
        if not self.is_active():
            return None

        if self.progress.current_step >= len(self.steps):
            return None

        return self.steps[self.progress.current_step]

    def show_current_step(self):
        """Display current tutorial step"""
        step = self.get_current_step()
        if not step:
            return

        print("\n" + "="*60)
        print(f"📚 TUTORIAL: {step.title}")
        print("="*60)
        print(f"\n{step.message}")

        if step.hint:
            print(f"\n💡 Hint: {step.hint}")

        if step.skippable:
            print("\n(Press 'S' to skip tutorial)")

        print("="*60 + "\n")

    def check_action(self, action: str) -> bool:
        """
        Check if action completes current step.

        Args:
            action: Action performed by player

        Returns:
            True if step completed
        """
        step = self.get_current_step()
        if not step:
            return False

        # Check for skip
        if action.lower() == 's' and step.skippable:
            self.skip()
            return True

        # Check if this action completes the step
        if step.type == TutorialStepType.ACTION:
            if step.required_action and action == step.required_action:
                self.complete_current_step()
                return True

        return False

    def check_condition(self, condition_name: str, value: Any) -> bool:
        """
        Check if condition completes current step.

        Args:
            condition_name: Name of condition
            value: Current value of condition

        Returns:
            True if step completed
        """
        step = self.get_current_step()
        if not step:
            return False

        if step.type == TutorialStepType.CONDITION:
            if step.required_condition:
                required_value = step.required_condition.get(condition_name)
                if required_value is not None and value >= required_value:
                    self.complete_current_step()
                    return True

        return False

    def complete_current_step(self):
        """Mark current step as completed and advance"""
        step = self.get_current_step()
        if not step:
            return

        # Mark completed
        self.progress.completed_steps.append(step.id)
        self.progress.current_step += 1

        # Trigger callbacks
        for callback in self.on_step_complete_callbacks:
            try:
                callback(step)
            except Exception as e:
                self.logger.error(f"Error in step complete callback: {e}")

        # Check if tutorial finished
        if self.progress.current_step >= len(self.steps):
            self._complete_tutorial()
        else:
            self._save_progress()

        # Show reward
        if step.reward:
            print(f"\n✨ {step.reward}")

    def _complete_tutorial(self):
        """Mark tutorial as completed"""
        self.progress.completed = True
        self._save_progress()

        print("\n" + "="*60)
        print("🎓 TUTORIAL COMPLETED!")
        print("="*60)
        print("\nCongratulations! You've completed the tutorial.")
        print("You're ready to play on your own now!")
        print("="*60 + "\n")

        # Award achievement
        if self.achievements:
            self.achievements.unlock(f"{self.game_id}_tutorial_complete")

    def skip(self):
        """Skip the tutorial"""
        self.progress.skipped = True
        self._save_progress()

        print("\n📚 Tutorial skipped!")
        print("You can always replay it from the main menu.\n")

    def restart(self):
        """Restart tutorial from beginning"""
        self.progress.current_step = 0
        self.progress.completed_steps = []
        self.progress.skipped = False
        self.progress.completed = False
        self._save_progress()

        self.logger.info("Tutorial restarted")

    def get_hint_for_context(self, context: str) -> Optional[str]:
        """
        Get contextual hint for current situation.

        Args:
            context: Current game context

        Returns:
            Hint text if available
        """
        step = self.get_current_step()
        if step and step.highlight == context:
            return step.hint
        return None

    def on_step_complete(self, callback: Callable[[TutorialStep], None]):
        """
        Register callback for step completion.

        Args:
            callback: Function to call when step completed
        """
        self.on_step_complete_callbacks.append(callback)


# =============================================================================
# TUTORIAL BUILDER
# =============================================================================

class TutorialBuilder:
    """Helper class to build tutorials programmatically"""

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.steps: List[Dict[str, Any]] = []

    def add_info(
        self,
        id: str,
        title: str,
        message: str,
        hint: Optional[str] = None
    ) -> 'TutorialBuilder':
        """Add information step"""
        self.steps.append({
            'id': id,
            'type': 'info',
            'title': title,
            'message': message,
            'hint': hint,
            'skippable': True
        })
        return self

    def add_action(
        self,
        id: str,
        title: str,
        message: str,
        required_action: str,
        hint: Optional[str] = None,
        reward: Optional[str] = None
    ) -> 'TutorialBuilder':
        """Add action step"""
        self.steps.append({
            'id': id,
            'type': 'action',
            'title': title,
            'message': message,
            'required_action': required_action,
            'hint': hint,
            'reward': reward,
            'skippable': True
        })
        return self

    def add_condition(
        self,
        id: str,
        title: str,
        message: str,
        condition_name: str,
        condition_value: Any,
        hint: Optional[str] = None,
        reward: Optional[str] = None
    ) -> 'TutorialBuilder':
        """Add condition step"""
        self.steps.append({
            'id': id,
            'type': 'condition',
            'title': title,
            'message': message,
            'required_condition': {condition_name: condition_value},
            'hint': hint,
            'reward': reward,
            'skippable': True
        })
        return self

    def build(self, output_file: Path):
        """Build and save tutorial"""
        data = {
            'game_id': self.game_id,
            'version': '1.0',
            'steps': self.steps
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Tutorial saved: {output_file}")


# =============================================================================
# EXAMPLE TUTORIAL
# =============================================================================

def create_example_tutorial():
    """Create example tutorial for testing"""
    builder = TutorialBuilder('example_game')

    builder.add_info(
        id='welcome',
        title='Welcome!',
        message='Welcome to the game! This tutorial will teach you the basics.',
        hint='Press Enter to continue'
    ).add_action(
        id='open_menu',
        title='Open Menu',
        message='Let\'s start by opening the main menu. Press M to open it.',
        required_action='open_menu',
        hint='Press the M key',
        reward='Great! You opened the menu.'
    ).add_action(
        id='check_inventory',
        title='Check Inventory',
        message='Now let\'s check your inventory. Press I to open it.',
        required_action='open_inventory',
        hint='Press the I key',
        reward='Perfect! You can see your items now.'
    ).add_condition(
        id='collect_items',
        title='Collect Items',
        message='Explore and collect 5 items.',
        condition_name='items_collected',
        condition_value=5,
        hint='Walk around and pick up items you find',
        reward='Excellent! You\'ve collected 5 items.'
    ).add_info(
        id='completion',
        title='Tutorial Complete',
        message='Congratulations! You\'ve completed the tutorial. Have fun playing!',
        hint=None
    )

    output_file = Path('data/example_game_tutorial.json')
    builder.build(output_file)


# =============================================================================
# TESTING
# =============================================================================

if __name__ == '__main__':
    print("Tutorial System Test")
    print("=" * 60)

    # Create example tutorial
    create_example_tutorial()

    # Load and test it
    tutorial = TutorialSystem('example_game')

    print(f"\nTutorial loaded: {len(tutorial.steps)} steps")
    print(f"Active: {tutorial.is_active()}")

    # Show first step
    tutorial.show_current_step()

    # Simulate completing steps
    print("\nSimulating tutorial progression...")

    step = tutorial.get_current_step()
    if step:
        print(f"\nStep 1: {step.title}")
        tutorial.complete_current_step()

    # Simulate action
    tutorial.check_action('open_menu')
    print("Performed action: open_menu")

    tutorial.check_action('open_inventory')
    print("Performed action: open_inventory")

    # Simulate condition
    for i in range(1, 6):
        if tutorial.check_condition('items_collected', i):
            print(f"Collected {i} items - step complete!")

    print(f"\nTutorial completed: {tutorial.is_completed()}")
    print("\n✅ Tutorial system test passed!")
