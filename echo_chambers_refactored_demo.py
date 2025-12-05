#!/usr/bin/env python3
"""
Echo Chambers - Refactored Demo
================================
Demonstration of how to refactor echo_chambers.py using the new infrastructure.

This shows how to integrate:
- base_game.py: Game loop and base functionality
- validation.py: Input validation
- logging_config.py: Logging
- save_system.py: Save/load functionality
- achievements.py: Achievement tracking
- event_generators.py: Event generation
- constants.py: Centralized constants
"""

import random
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum

# NEW: Import new infrastructure modules
from base_game import TurnBasedGame, GameMetadata
from validation import get_menu_choice, get_yes_no_input
from logging_config import get_logger, log_performance
from save_system import get_save_system, SaveFile
from achievements import AchievementSystem, Achievement, AchievementCategory, AchievementRarity
from event_generators import EventManager, Event, EventGenerator, EventContext
from constants import (
    # Echo Chambers specific constants
    DECAY_RATE_PER_TURN,
    DECAY_THRESHOLD_DECAYING,
    DECAY_THRESHOLD_CORRUPTED,
    TIMELINE_MAX_ENTANGLEMENTS
)


# =============================================================================
# GAME CONSTANTS (Now centralized!)
# =============================================================================

class TimelineState(Enum):
    """Timeline states - same as before"""
    HEALTHY = "healthy"
    DECAYING = "decaying"
    CORRUPTED = "corrupted"
    COLLAPSED = "collapsed"


# =============================================================================
# GAME DATA STRUCTURES
# =============================================================================

@dataclass
class Timeline:
    """A parallel reality"""
    id: int
    name: str
    state: TimelineState
    last_visited: int
    created_at: int
    decay_level: float = 0.0
    properties: Dict[str, int] = field(default_factory=dict)

    def get_state_icon(self) -> str:
        """Get icon for timeline state"""
        return {
            TimelineState.HEALTHY: "✅",
            TimelineState.DECAYING: "⚠️",
            TimelineState.CORRUPTED: "❌",
            TimelineState.COLLAPSED: "💀"
        }[self.state]


# =============================================================================
# CUSTOM EVENT GENERATORS
# =============================================================================

class QuantumEventGenerator(EventGenerator):
    """Generate quantum-related events"""

    def can_generate(self, context: EventContext) -> bool:
        """Can generate if timeline has high consciousness"""
        timeline = context.custom_data.get('timeline')
        if timeline:
            return timeline.properties.get('consciousness_awareness', 0) > 5
        return False

    def generate(self, context: EventContext) -> Event:
        """Generate a quantum event"""
        events = [
            Event(
                name="Quantum Fluctuation",
                description="You feel reality shift around you. A decision point approaches.",
                choices=[
                    {"text": "Embrace the shift", "effects": {"consciousness": +2}},
                    {"text": "Resist the change", "effects": {"stability": +1}}
                ]
            ),
            Event(
                name="Echo Resonance",
                description="Your actions in other timelines echo back to you.",
                choices=[
                    {"text": "Listen closely", "effects": {"consciousness": +1, "memory_chance": 0.5}},
                    {"text": "Block it out", "effects": {"stability": +2}}
                ]
            )
        ]
        return random.choice(events)


# =============================================================================
# MAIN GAME CLASS (Using base_game.py!)
# =============================================================================

class EchoChambersRefactored(TurnBasedGame):
    """
    Echo Chambers using new infrastructure.

    Key improvements:
    - Extends TurnBasedGame for game loop
    - Uses logging for debugging
    - Uses validation for input
    - Integrated save/load system
    - Achievement tracking
    - Event generators for cleaner events
    """

    def __init__(self):
        # Initialize base game
        super().__init__(GameMetadata(
            name="Echo Chambers",
            version="2.0 (Refactored)",
            description="Navigate parallel timelines and piece together your fragmented consciousness"
        ))

        # NEW: Logger for debugging
        self.logger = get_logger(__name__)
        self.logger.info("Initializing Echo Chambers (Refactored)")

        # Game state
        self.timelines: List[Timeline] = []
        self.current_timeline_id = 0
        self.memories_collected = 0

        # NEW: Save system integration
        self.save_system = get_save_system()

        # NEW: Achievement system
        self.achievements = AchievementSystem(game_id='echo_chambers')
        self._setup_achievements()

        # NEW: Event manager with custom generators
        self.event_manager = EventManager()
        self.event_manager.register_generator(QuantumEventGenerator())

        # NEW: Register achievement unlock callback
        self.achievements.on_unlock(self._on_achievement_unlocked)

    def _setup_achievements(self):
        """Setup game achievements"""
        achievements = [
            Achievement(
                id="first_timeline",
                name="Reality Hopper",
                description="Create your first alternate timeline",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.COMMON,
                points=10,
                icon="🌀",
                requirements={'timelines_created': 1}
            ),
            Achievement(
                id="memory_collector",
                name="Remember",
                description="Collect 5 memory fragments",
                category=AchievementCategory.COLLECTION,
                rarity=AchievementRarity.UNCOMMON,
                points=15,
                icon="🧠",
                requirements={'memories_collected': 5}
            ),
            Achievement(
                id="timeline_master",
                name="Quantum Navigator",
                description="Maintain 5 healthy timelines simultaneously",
                category=AchievementCategory.GAMEPLAY,
                rarity=AchievementRarity.RARE,
                points=25,
                icon="⚛️",
                requirements={'healthy_timelines': 5}
            ),
            Achievement(
                id="survive_50",
                name="Persistence",
                description="Survive 50 turns across timelines",
                category=AchievementCategory.PROGRESSION,
                rarity=AchievementRarity.UNCOMMON,
                points=20,
                icon="💪",
                requirements={'turns_survived': 50}
            )
        ]

        for achievement in achievements:
            self.achievements.register_achievement(achievement)

    def _on_achievement_unlocked(self, achievement: Achievement):
        """Called when achievement is unlocked"""
        self.logger.info(f"Achievement unlocked: {achievement.name}")
        print(f"\n{'='*60}")
        print(f"🏆 ACHIEVEMENT UNLOCKED: {achievement.name}")
        print(f"   {achievement.description}")
        print(f"   +{achievement.points} points")
        print(f"{'='*60}\n")
        input("Press Enter to continue...")

    def setup(self) -> None:
        """Initialize game - called by base class"""
        self.logger.info("Setting up game")

        # Create first timeline
        self.timelines.append(Timeline(
            id=0,
            name="Prime Timeline",
            state=TimelineState.HEALTHY,
            last_visited=0,
            created_at=0,
            properties={
                "technology_level": 5,
                "society_stability": 7,
                "consciousness_awareness": 3
            }
        ))

        # Show intro
        self._show_intro()

    def _show_intro(self):
        """Show game introduction"""
        self.clear_screen()
        self.print_header("ECHO CHAMBERS (Refactored Demo)")

        print("""
You are a consciousness that exists across parallel timelines.
Every choice splinters reality. Every moment branches into infinite possibilities.

But the timelines are decaying...
Your memories are fragmented...
And you can't remember why.

Navigate your parallel selves, collect memory fragments,
and survive the coming Convergence.
        """)

        input("\nPress Enter to begin...")

    @log_performance(get_logger(__name__))  # NEW: Performance tracking!
    def render(self) -> None:
        """Render game state - called by base class"""
        self.clear_screen()
        self.print_header(f"Echo Chambers - Turn {self.turn}")

        # Show current timeline
        timeline = self.timelines[self.current_timeline_id]
        print(f"\n{timeline.get_state_icon()} Current: {timeline.name}")
        print(f"   State: {timeline.state.value}")
        print(f"   Decay: {timeline.decay_level:.1f}")
        print(f"   Properties:")
        for prop, value in timeline.properties.items():
            print(f"      {prop}: {value}")

        # Show all timelines
        print(f"\n📊 All Timelines ({len(self.timelines)}):")
        for t in self.timelines:
            print(f"   {t.get_state_icon()} {t.id}. {t.name} - {t.state.value}")

        # Show stats
        print(f"\n🧠 Memories Collected: {self.memories_collected}")
        print(f"🎯 Achievements: {len(self.achievements.get_unlocked())}/{len(self.achievements.achievements)}")

    def handle_input(self, key: Optional[str] = None) -> None:
        """Handle user input - called by base class"""
        # NEW: Using validation.py for menu!
        options = [
            "🔄 Take Action",
            "🌀 Create New Timeline",
            "🚪 Switch Timeline",
            "💾 Save Game",
            "📜 View Achievements",
            "❌ Quit"
        ]

        choice = get_menu_choice(options, title="What do you do?")

        if choice == 1:
            self._take_action()
        elif choice == 2:
            self._create_timeline()
        elif choice == 3:
            self._switch_timeline()
        elif choice == 4:
            self._save_game()
        elif choice == 5:
            self._view_achievements()
        elif choice == 6:
            # NEW: Using validation for confirmation!
            if get_yes_no_input("Are you sure you want to quit?", default=False):
                self.quit()

    def update(self) -> None:
        """Update game state - called by base class"""
        # Evolve all timelines
        for timeline in self.timelines:
            if timeline.id != self.current_timeline_id:
                self._evolve_timeline(timeline)

        # Update achievements
        self._update_achievements()

        # Check win/lose conditions
        self._check_game_state()

    def cleanup(self) -> None:
        """Cleanup - called by base class"""
        self.logger.info(f"Game ended after {self.turn} turns")
        print("\n" + "="*60)
        print("Thanks for playing Echo Chambers!")
        print(f"Final Stats:")
        print(f"  Turns: {self.turn}")
        print(f"  Timelines: {len(self.timelines)}")
        print(f"  Memories: {self.memories_collected}")
        stats = self.achievements.get_statistics()
        print(f"  Achievements: {stats['unlocked']}/{stats['total_achievements']}")
        print("="*60)

    # =============================================================================
    # GAME ACTIONS
    # =============================================================================

    def _take_action(self):
        """Take an action in current timeline"""
        timeline = self.timelines[self.current_timeline_id]

        # NEW: Generate event using event_manager
        context = EventContext(
            turn=self.turn,
            custom_data={'timeline': timeline}
        )

        event = self.event_manager.generate_event(context)

        if event:
            self.logger.debug(f"Event generated: {event.name}")

            # Show event
            print(f"\n{'='*60}")
            print(f"⚡ {event.name}")
            print(f"{event.description}")
            print(f"{'='*60}\n")

            # Show choices (using validation!)
            choice_texts = [choice['text'] for choice in event.choices]
            choice_idx = get_menu_choice(choice_texts, title="Choose your action")

            if choice_idx > 0:
                chosen = event.choices[choice_idx - 1]
                self._apply_effects(chosen.get('effects', {}))

                # Chance to find memory
                if random.random() < 0.3:
                    self.memories_collected += 1
                    print("\n🧠 You found a memory fragment!")
                    self.achievements.update_progress('memory_collector', {
                        'memories_collected': self.memories_collected
                    })

    def _create_timeline(self):
        """Create a new branching timeline"""
        if len(self.timelines) >= 5:
            print("\n⚠️ You can't manage more than 5 timelines!")
            input("Press Enter...")
            return

        # Create new timeline
        new_id = len(self.timelines)
        new_timeline = Timeline(
            id=new_id,
            name=f"Timeline {chr(65 + new_id)}",  # A, B, C...
            state=TimelineState.HEALTHY,
            last_visited=self.turn,
            created_at=self.turn,
            properties=self.timelines[self.current_timeline_id].properties.copy()
        )

        self.timelines.append(new_timeline)
        self.logger.info(f"Created timeline {new_id}")

        print(f"\n🌀 Created {new_timeline.name}!")

        # Update achievements
        self.achievements.update_progress('first_timeline', {
            'timelines_created': len(self.timelines) - 1
        })

        input("Press Enter...")

    def _switch_timeline(self):
        """Switch to a different timeline"""
        if len(self.timelines) == 1:
            print("\n⚠️ No other timelines to switch to!")
            input("Press Enter...")
            return

        # Show timelines using validation menu
        timeline_names = [
            f"{t.get_state_icon()} {t.name} ({t.state.value})"
            for t in self.timelines
        ]

        choice = get_menu_choice(timeline_names, title="Switch to which timeline?")

        if choice > 0:
            self.current_timeline_id = choice - 1
            self.timelines[self.current_timeline_id].last_visited = self.turn
            self.logger.info(f"Switched to timeline {self.current_timeline_id}")

    def _save_game(self):
        """Save game state"""
        # NEW: Using save_system.py!
        save_data = {
            'timelines': [
                {
                    'id': t.id,
                    'name': t.name,
                    'state': t.state.value,
                    'last_visited': t.last_visited,
                    'created_at': t.created_at,
                    'decay_level': t.decay_level,
                    'properties': t.properties
                }
                for t in self.timelines
            ],
            'current_timeline_id': self.current_timeline_id,
            'turn': self.turn,
            'memories_collected': self.memories_collected
        }

        try:
            self.save_system.save(
                game_id='echo_chambers',
                game_name='Echo Chambers',
                data=save_data,
                save_slot=1,
                play_time=self.turn * 30  # Rough estimate
            )
            print("\n💾 Game saved successfully!")
            self.logger.info("Game saved")
        except Exception as e:
            print(f"\n❌ Error saving game: {e}")
            self.logger.error(f"Save failed: {e}")

        input("Press Enter...")

    def _view_achievements(self):
        """View achievement progress"""
        self.clear_screen()
        self.print_header("Achievements")

        stats = self.achievements.get_statistics()
        print(f"\n🏆 Progress: {stats['unlocked']}/{stats['total_achievements']}")
        print(f"⭐ Points: {stats['earned_points']}/{stats['total_points']}")
        print(f"📊 Completion: {stats['completion_percent']:.1f}%\n")

        print("Unlocked:")
        for ach in self.achievements.get_unlocked():
            self.achievements.print_achievement(ach)
            print()

        print("\nLocked:")
        for ach in self.achievements.get_locked():
            self.achievements.print_achievement(ach)
            print()

        input("\nPress Enter to continue...")

    # =============================================================================
    # GAME MECHANICS
    # =============================================================================

    def _evolve_timeline(self, timeline: Timeline):
        """Evolve timeline based on time away"""
        turns_away = self.turn - timeline.last_visited

        if turns_away > 0:
            # NEW: Using constants instead of magic numbers!
            decay_amount = DECAY_RATE_PER_TURN * turns_away
            timeline.decay_level += decay_amount

            # Update state based on decay
            if timeline.decay_level >= DECAY_THRESHOLD_CORRUPTED:
                timeline.state = TimelineState.CORRUPTED
            elif timeline.decay_level >= DECAY_THRESHOLD_DECAYING:
                timeline.state = TimelineState.DECAYING
            else:
                timeline.state = TimelineState.HEALTHY

    def _apply_effects(self, effects: Dict[str, int]):
        """Apply effects to current timeline"""
        timeline = self.timelines[self.current_timeline_id]

        for prop, change in effects.items():
            if prop in timeline.properties:
                timeline.properties[prop] += change
                timeline.properties[prop] = max(0, min(10, timeline.properties[prop]))

    def _update_achievements(self):
        """Update achievement progress"""
        # Survival achievement
        self.achievements.update_progress('survive_50', {
            'turns_survived': self.turn
        })

        # Timeline master achievement
        healthy_count = sum(1 for t in self.timelines if t.state == TimelineState.HEALTHY)
        self.achievements.update_progress('timeline_master', {
            'healthy_timelines': healthy_count
        })

    def _check_game_state(self):
        """Check for win/lose conditions"""
        # Lose: all timelines corrupted
        all_corrupted = all(
            t.state == TimelineState.CORRUPTED
            for t in self.timelines
        )

        if all_corrupted:
            print("\n💀 All timelines have collapsed!")
            print("Game Over")
            input("\nPress Enter...")
            self.quit()


# =============================================================================
# LOAD GAME FUNCTIONALITY
# =============================================================================

def load_game() -> Optional[EchoChambersRefactored]:
    """Load a saved game"""
    save_system = get_save_system()
    save_file = save_system.load('echo_chambers', save_slot=1)

    if not save_file:
        print("No save file found!")
        return None

    # Create game instance
    game = EchoChambersRefactored()

    # Restore state
    data = save_file.data
    game.turn = data['turn']
    game.current_timeline_id = data['current_timeline_id']
    game.memories_collected = data['memories_collected']

    # Restore timelines
    game.timelines = [
        Timeline(
            id=t['id'],
            name=t['name'],
            state=TimelineState(t['state']),
            last_visited=t['last_visited'],
            created_at=t['created_at'],
            decay_level=t['decay_level'],
            properties=t['properties']
        )
        for t in data['timelines']
    ]

    print(f"\n✅ Loaded game from turn {game.turn}")
    return game


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point"""
    # Ask if load or new game
    print("Echo Chambers (Refactored Demo)")
    print("="*60)

    choice = get_menu_choice(
        ["New Game", "Load Game", "Quit"],
        title="Main Menu"
    )

    if choice == 1:
        game = EchoChambersRefactored()
        game.run()  # Uses base class game loop!
    elif choice == 2:
        game = load_game()
        if game:
            game.run()
    elif choice == 3:
        print("Goodbye!")


if __name__ == '__main__':
    main()
