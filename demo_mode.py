#!/usr/bin/env python3
"""
Demo Mode System
================
Provides automated demo/showcase functionality for games.

Features:
- Auto-play with AI-generated moves
- Scripted demo scenarios
- Speed control
- Commentary generation
- Progress tracking

Usage:
    from demo_mode import DemoRunner, DemoScenario

    # Run automatic demo
    runner = DemoRunner("vault_shelter")
    runner.run_demo()

    # Run scripted scenario
    scenario = DemoScenario.load("tutorial_demo")
    runner.run_scenario(scenario)
"""

import time
import random
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from pathlib import Path
from enum import Enum

from logging_config import get_logger
from platform_utils import clear_screen
from colors import C

logger = get_logger(__name__)


class DemoSpeed(Enum):
    """Demo playback speed"""
    SLOW = 2.0       # 2 seconds between actions
    NORMAL = 1.0     # 1 second between actions
    FAST = 0.5       # 0.5 seconds between actions
    INSTANT = 0.0    # No delay


@dataclass
class DemoAction:
    """A single action in a demo scenario"""
    action_type: str          # 'input', 'wait', 'comment', 'clear'
    value: str = ""           # The input/comment text
    delay: float = 1.0        # Delay after action
    condition: Optional[str] = None  # Optional condition to check


@dataclass
class DemoScenario:
    """A scripted demo scenario"""
    name: str
    description: str
    game_id: str
    actions: List[DemoAction] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_input(self, value: str, delay: float = 1.0) -> 'DemoScenario':
        """Add an input action"""
        self.actions.append(DemoAction('input', value, delay))
        return self

    def add_wait(self, seconds: float) -> 'DemoScenario':
        """Add a wait action"""
        self.actions.append(DemoAction('wait', '', seconds))
        return self

    def add_comment(self, text: str, delay: float = 2.0) -> 'DemoScenario':
        """Add a commentary text"""
        self.actions.append(DemoAction('comment', text, delay))
        return self

    def add_clear(self) -> 'DemoScenario':
        """Add a screen clear"""
        self.actions.append(DemoAction('clear', '', 0))
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'description': self.description,
            'game_id': self.game_id,
            'actions': [
                {
                    'type': a.action_type,
                    'value': a.value,
                    'delay': a.delay,
                    'condition': a.condition
                }
                for a in self.actions
            ],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DemoScenario':
        """Create from dictionary"""
        scenario = cls(
            name=data['name'],
            description=data['description'],
            game_id=data['game_id'],
            metadata=data.get('metadata', {})
        )
        for action_data in data.get('actions', []):
            scenario.actions.append(DemoAction(
                action_type=action_data['type'],
                value=action_data.get('value', ''),
                delay=action_data.get('delay', 1.0),
                condition=action_data.get('condition')
            ))
        return scenario

    @classmethod
    def load(cls, scenario_name: str) -> 'DemoScenario':
        """Load scenario from file"""
        scenarios_dir = Path(__file__).parent / "demo_scenarios"
        scenario_file = scenarios_dir / f"{scenario_name}.json"

        if scenario_file.exists():
            with open(scenario_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        else:
            raise FileNotFoundError(f"Scenario not found: {scenario_name}")

    def save(self, path: Optional[Path] = None) -> None:
        """Save scenario to file"""
        if path is None:
            scenarios_dir = Path(__file__).parent / "demo_scenarios"
            scenarios_dir.mkdir(exist_ok=True)
            path = scenarios_dir / f"{self.name}.json"

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)


class DemoRunner:
    """
    Runs demo/showcase mode for games.

    Can run either:
    - Automated demo with AI-like moves
    - Scripted scenario with predefined actions
    """

    def __init__(self, game_id: str, speed: DemoSpeed = DemoSpeed.NORMAL):
        self.game_id = game_id
        self.speed = speed
        self.running = False
        self.paused = False

        self._action_count = 0
        self._start_time = 0.0

        # Callbacks
        self._on_action: Optional[Callable[[DemoAction], None]] = None
        self._on_comment: Optional[Callable[[str], None]] = None

        logger.info(f"DemoRunner initialized for {game_id}")

    def set_speed(self, speed: DemoSpeed) -> None:
        """Set demo playback speed"""
        self.speed = speed

    def on_action(self, callback: Callable[[DemoAction], None]) -> 'DemoRunner':
        """Register callback for actions"""
        self._on_action = callback
        return self

    def on_comment(self, callback: Callable[[str], None]) -> 'DemoRunner':
        """Register callback for comments"""
        self._on_comment = callback
        return self

    def run_scenario(self, scenario: DemoScenario) -> bool:
        """
        Run a scripted demo scenario.

        Args:
            scenario: The scenario to run

        Returns:
            True if completed, False if interrupted
        """
        self.running = True
        self._start_time = time.time()
        self._action_count = 0

        logger.info(f"Starting demo scenario: {scenario.name}")

        self._show_intro(scenario)

        for action in scenario.actions:
            if not self.running:
                break

            while self.paused:
                time.sleep(0.1)
                if not self.running:
                    break

            self._execute_action(action)
            self._action_count += 1

        self._show_outro(scenario)
        self.running = False

        return self._action_count == len(scenario.actions)

    def run_auto_demo(self, duration_seconds: float = 60.0,
                     get_valid_moves: Optional[Callable[[], List[str]]] = None) -> None:
        """
        Run an automated demo with random/smart moves.

        Args:
            duration_seconds: How long to run the demo
            get_valid_moves: Optional callback to get valid moves
        """
        self.running = True
        self._start_time = time.time()
        self._action_count = 0

        logger.info(f"Starting auto demo for {self.game_id}")

        self._show_auto_intro()

        while self.running and (time.time() - self._start_time) < duration_seconds:
            while self.paused:
                time.sleep(0.1)
                if not self.running:
                    break

            # Get and execute a move
            if get_valid_moves:
                moves = get_valid_moves()
                if moves:
                    move = self._choose_smart_move(moves)
                    action = DemoAction('input', move, self.speed.value)
                    self._execute_action(action)
                    self._action_count += 1
            else:
                # Generic demo move
                action = DemoAction('input', '1', self.speed.value)
                self._execute_action(action)
                self._action_count += 1

            time.sleep(self.speed.value)

        self._show_auto_outro()
        self.running = False

    def stop(self) -> None:
        """Stop the demo"""
        self.running = False
        logger.info("Demo stopped")

    def pause(self) -> None:
        """Pause the demo"""
        self.paused = True
        logger.info("Demo paused")

    def resume(self) -> None:
        """Resume the demo"""
        self.paused = False
        logger.info("Demo resumed")

    def _execute_action(self, action: DemoAction) -> None:
        """Execute a single demo action"""
        if self._on_action:
            self._on_action(action)

        if action.action_type == 'input':
            self._show_input(action.value)
        elif action.action_type == 'wait':
            time.sleep(action.delay)
        elif action.action_type == 'comment':
            self._show_comment(action.value)
            if self._on_comment:
                self._on_comment(action.value)
        elif action.action_type == 'clear':
            clear_screen()

        if action.delay > 0 and action.action_type != 'wait':
            time.sleep(action.delay * self.speed.value)

    def _show_input(self, value: str) -> None:
        """Display input being entered"""
        print(f"{C.DIM}> {C.BOLD}{value}{C.RESET}")

    def _show_comment(self, text: str) -> None:
        """Display commentary"""
        print(f"\n{C.CYAN}💬 {text}{C.RESET}\n")

    def _show_intro(self, scenario: DemoScenario) -> None:
        """Show demo introduction"""
        clear_screen()
        print(f"\n{C.BOLD}{'═' * 60}{C.RESET}")
        print(f"{C.CYAN}🎬 DEMO MODE{C.RESET}".center(70))
        print(f"{C.BOLD}{'═' * 60}{C.RESET}\n")
        print(f"{C.BOLD}{scenario.name}{C.RESET}")
        print(f"{C.DIM}{scenario.description}{C.RESET}")
        print(f"\n{C.DIM}Press Ctrl+C to exit demo{C.RESET}")
        print(f"\n{'─' * 60}\n")
        time.sleep(2)

    def _show_outro(self, scenario: DemoScenario) -> None:
        """Show demo conclusion"""
        elapsed = time.time() - self._start_time
        print(f"\n{C.BOLD}{'═' * 60}{C.RESET}")
        print(f"{C.GREEN}✓ Demo Complete!{C.RESET}".center(70))
        print(f"{C.BOLD}{'═' * 60}{C.RESET}\n")
        print(f"Actions: {self._action_count}")
        print(f"Duration: {elapsed:.1f}s")
        print()

    def _show_auto_intro(self) -> None:
        """Show auto-demo introduction"""
        clear_screen()
        print(f"\n{C.BOLD}{'═' * 60}{C.RESET}")
        print(f"{C.CYAN}🤖 AUTO DEMO MODE{C.RESET}".center(70))
        print(f"{C.BOLD}{'═' * 60}{C.RESET}\n")
        print(f"Game: {self.game_id}")
        print(f"Speed: {self.speed.name}")
        print(f"\n{C.DIM}Press Ctrl+C to exit{C.RESET}")
        print(f"\n{'─' * 60}\n")
        time.sleep(1)

    def _show_auto_outro(self) -> None:
        """Show auto-demo conclusion"""
        elapsed = time.time() - self._start_time
        print(f"\n{C.BOLD}{'═' * 60}{C.RESET}")
        print(f"{C.GREEN}✓ Auto Demo Complete!{C.RESET}".center(70))
        print(f"{C.BOLD}{'═' * 60}{C.RESET}\n")
        print(f"Actions taken: {self._action_count}")
        print(f"Duration: {elapsed:.1f}s")
        print()

    def _choose_smart_move(self, moves: List[str]) -> str:
        """Choose a move intelligently (or randomly)"""
        # Prefer certain types of moves
        priority_keywords = ['build', 'assign', 'explore', 'attack', 'upgrade']

        for keyword in priority_keywords:
            for move in moves:
                if keyword in move.lower():
                    return move

        return random.choice(moves)


# === Demo Scenario Builder ===

def create_vault_tutorial_demo() -> DemoScenario:
    """Create a tutorial demo for Vault Shelter"""
    scenario = DemoScenario(
        name="Vault Tutorial Demo",
        description="Learn the basics of running your vault",
        game_id="vault_shelter"
    )

    scenario.add_comment("Welcome to VAULT 13! Let's learn the basics.")
    scenario.add_input("1", 1.5)  # View vault
    scenario.add_comment("Here's your vault overview. You can see resources at the top.")
    scenario.add_wait(2)
    scenario.add_input("2", 1.5)  # Dwellers
    scenario.add_comment("These are your dwellers. Each has unique stats and skills.")
    scenario.add_wait(2)
    scenario.add_input("q", 1.0)  # Back
    scenario.add_input("3", 1.5)  # Build
    scenario.add_comment("You can build rooms to expand your vault.")
    scenario.add_wait(2)
    scenario.add_input("q", 1.0)  # Back

    return scenario


def create_philosophical_game_demo(game_id: str) -> DemoScenario:
    """Create a generic demo for philosophical games"""
    scenario = DemoScenario(
        name=f"{game_id.title()} Demo",
        description=f"Demonstration of {game_id.replace('_', ' ').title()}",
        game_id=game_id
    )

    scenario.add_comment(f"This is {game_id.replace('_', ' ').title()}")
    scenario.add_wait(1)
    scenario.add_input("1", 2.0)
    scenario.add_comment("Watch as the game explores philosophical concepts...")
    scenario.add_wait(2)
    scenario.add_input("1", 2.0)
    scenario.add_input("2", 2.0)

    return scenario


# === Main ===

if __name__ == '__main__':
    print("Demo Mode System")
    print("=" * 40)

    # Create and save a sample scenario
    scenario = create_vault_tutorial_demo()
    print(f"\nCreated scenario: {scenario.name}")
    print(f"Actions: {len(scenario.actions)}")

    # Run a quick demo
    print("\nRunning demo preview...")
    runner = DemoRunner("vault_shelter", DemoSpeed.FAST)

    for action in scenario.actions[:3]:
        runner._execute_action(action)

    print("\n✓ Demo mode system ready!")
