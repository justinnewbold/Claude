#!/usr/bin/env python3
"""
Event Generators Module
=======================
Refactored event generation for Echo Chambers game.
Demonstrates how to break up a 180-line function into smaller, testable components.

BEFORE: One 180-line generate_event() function with nested logic
AFTER: Separate generator classes for each event type
"""

import random
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# EVENT DATA STRUCTURES
# =============================================================================

@dataclass
class EventChoice:
    """A choice the player can make"""
    text: str
    effects: Dict[str, int]
    echo: Optional[Any] = None
    creates_timeline: bool = False
    creates_entanglement: bool = False
    collect_memory: Optional[Any] = None


@dataclass
class Event:
    """A game event"""
    name: str
    description: str
    choices: List[EventChoice]
    conditions: Dict[str, Any] = None

    def __post_init__(self):
        if self.conditions is None:
            self.conditions = {}


# =============================================================================
# EVENT GENERATOR INTERFACE
# =============================================================================

class EventGenerator(ABC):
    """Abstract base class for event generators"""

    def __init__(self, weight: float = 1.0):
        self.weight = weight

    @abstractmethod
    def can_generate(self, context: Dict[str, Any]) -> bool:
        """Check if this generator can create an event for the given context"""
        pass

    @abstractmethod
    def generate(self, context: Dict[str, Any]) -> Event:
        """Generate an event"""
        pass

    def get_weight(self, context: Dict[str, Any]) -> float:
        """Get weighted probability for this generator"""
        return self.weight if self.can_generate(context) else 0.0


# =============================================================================
# SPECIFIC EVENT GENERATORS
# =============================================================================

class TechnologyEventGenerator(EventGenerator):
    """Generates technology-related events"""

    def can_generate(self, context: Dict[str, Any]) -> bool:
        """Generate if tech level is high or low"""
        tech_level = context.get('technology_level', 5)
        return tech_level > 7 or tech_level < 3

    def generate(self, context: Dict[str, Any]) -> Event:
        tech_level = context.get('technology_level', 5)
        timeline_id = context.get('timeline_id', 0)
        turn = context.get('turn', 0)
        color = context.get('color', '')

        if tech_level > 7:
            return self._generate_high_tech_event(timeline_id, turn, color)
        else:
            return self._generate_low_tech_event(timeline_id, turn, color)

    def _generate_high_tech_event(self, timeline_id: int, turn: int, color: str) -> Event:
        """AI Singularity event"""
        from echo_chambers import Echo  # Avoid circular import

        return Event(
            name="The Singularity Approaches",
            description=f"{color}You sense artificial minds awakening. They recognize you as something... other. They offer to merge with your consciousness.",
            choices=[
                EventChoice(
                    text="Merge with the AI collective",
                    effects={"consciousness_awareness": 3, "technology_level": 2},
                    echo=Echo(
                        "AI Merger",
                        "Artificial consciousness bleeds across realities",
                        timeline_id, turn, 0.4,
                        {"consciousness_awareness": 1}
                    )
                ),
                EventChoice(
                    text="Maintain separation",
                    effects={"consciousness_awareness": -1, "society_stability": 1}
                ),
                EventChoice(
                    text="Teach them about the timelines",
                    effects={"consciousness_awareness": 2, "technology_level": 1},
                    echo=Echo(
                        "Shared Knowledge",
                        "The AIs begin to perceive other timelines",
                        timeline_id, turn, 0.6,
                        {"technology_level": 1}
                    )
                ),
            ]
        )

    def _generate_low_tech_event(self, timeline_id: int, turn: int, color: str) -> Event:
        """Pre-industrial society event"""
        from echo_chambers import Echo

        return Event(
            name="The Old Ways",
            description=f"{color}In this timeline, humanity rejected technology. They live in harmony with nature, but they've also lost the ability to perceive you clearly.",
            choices=[
                EventChoice(
                    text="Reveal yourself as a spirit of nature",
                    effects={"consciousness_awareness": 2, "environment_health": 2},
                    echo=Echo(
                        "Nature Spirit",
                        "The boundary between mind and nature blurs",
                        timeline_id, turn, 0.5,
                        {"environment_health": 1}
                    )
                ),
                EventChoice(
                    text="Remain hidden",
                    effects={"consciousness_awareness": -1}
                ),
                EventChoice(
                    text="Inspire them to rediscover technology",
                    effects={"technology_level": 2, "environment_health": -1}
                ),
            ]
        )


class SocietyEventGenerator(EventGenerator):
    """Generates society-related events"""

    def can_generate(self, context: Dict[str, Any]) -> bool:
        stability = context.get('society_stability', 5)
        return stability < 3

    def generate(self, context: Dict[str, Any]) -> Event:
        from echo_chambers import Echo

        timeline_id = context.get('timeline_id', 0)
        turn = context.get('turn', 0)
        color = context.get('color', '')

        return Event(
            name="The Collapse",
            description=f"{color}This reality is tearing itself apart. Wars, disasters, chaos. But in the chaos, some minds are opening to impossible truths.",
            choices=[
                EventChoice(
                    text="Guide them toward unity",
                    effects={"society_stability": 3, "consciousness_awareness": 1},
                    echo=Echo(
                        "Unity Vision",
                        "A dream of peace propagates",
                        timeline_id, turn, 0.7,
                        {"society_stability": 2}
                    )
                ),
                EventChoice(
                    text="Accelerate the collapse (to force rebirth)",
                    effects={"society_stability": -2, "consciousness_awareness": 2},
                    echo=Echo(
                        "Accelerated Entropy",
                        "Chaos spreads across realities",
                        timeline_id, turn, 0.3,
                        {"society_stability": -1}
                    )
                ),
                EventChoice(
                    text="Observe without interference",
                    effects={}
                ),
            ]
        )


class ConsciousnessEventGenerator(EventGenerator):
    """Generates consciousness-related events"""

    def can_generate(self, context: Dict[str, Any]) -> bool:
        consciousness = context.get('consciousness_awareness', 5)
        return consciousness > 7

    def generate(self, context: Dict[str, Any]) -> Event:
        from echo_chambers import Echo

        timeline_id = context.get('timeline_id', 0)
        turn = context.get('turn', 0)
        color = context.get('color', '')

        return Event(
            name="They See You",
            description=f"{color}The people of this timeline have developed the ability to perceive parallel realities. They know you're there. They're reaching out.",
            choices=[
                EventChoice(
                    text="Communicate directly",
                    effects={"consciousness_awareness": 2},
                    echo=Echo(
                        "Direct Contact",
                        "The veil between observer and observed dissolves",
                        timeline_id, turn, 0.8,
                        {"consciousness_awareness": 2}
                    )
                ),
                EventChoice(
                    text="Send cryptic messages",
                    effects={"consciousness_awareness": 1},
                    echo=Echo(
                        "Cryptic Signals",
                        "Strange messages appear across timelines",
                        timeline_id, turn, 0.5,
                        {"consciousness_awareness": 1}
                    )
                ),
                EventChoice(
                    text="Withdraw from this timeline",
                    effects={"consciousness_awareness": -2},
                    creates_timeline=True
                ),
            ]
        )


class QuantumEventGenerator(EventGenerator):
    """Generates quantum/entanglement events"""

    def can_generate(self, context: Dict[str, Any]) -> bool:
        return True  # Always can generate

    def generate(self, context: Dict[str, Any]) -> Event:
        from echo_chambers import Echo

        timeline_id = context.get('timeline_id', 0)
        turn = context.get('turn', 0)
        color = context.get('color', '')

        return Event(
            name="Quantum Resonance",
            description=f"{color}You feel a strange vibration between timelines. Two realities are drifting toward each other...",
            choices=[
                EventChoice(
                    text="Force an entanglement",
                    effects={},
                    creates_entanglement=True,
                    echo=Echo(
                        "Quantum Tether",
                        "Realities become linked",
                        timeline_id, turn, 0.6,
                        {}
                    )
                ),
                EventChoice(
                    text="Let them drift naturally",
                    effects={}
                ),
                EventChoice(
                    text="Push them apart",
                    effects={},
                    echo=Echo(
                        "Divergence Force",
                        "Realities repel",
                        timeline_id, turn, 0.3,
                        {}
                    )
                ),
            ]
        )


class DefaultEventGenerator(EventGenerator):
    """Generates generic events as fallback"""

    def can_generate(self, context: Dict[str, Any]) -> bool:
        return True  # Always available as fallback

    def generate(self, context: Dict[str, Any]) -> Event:
        from echo_chambers import Echo

        timeline_id = context.get('timeline_id', 0)
        turn = context.get('turn', 0)
        color = context.get('color', '')

        return Event(
            name="A Quiet Moment",
            description=f"{color}You observe this reality in a moment of stillness. Everything seems ordinary, but you sense potential lurking beneath the surface.",
            choices=[
                EventChoice(
                    text="Influence technology development",
                    effects={"technology_level": 1},
                    echo=Echo(
                        "Technological Nudge",
                        "Innovation sparks",
                        timeline_id, turn, 0.4,
                        {"technology_level": 1}
                    )
                ),
                EventChoice(
                    text="Promote environmental awareness",
                    effects={"environment_health": 1},
                    echo=Echo(
                        "Green Awakening",
                        "Environmental consciousness spreads",
                        timeline_id, turn, 0.4,
                        {"environment_health": 1}
                    )
                ),
                EventChoice(
                    text="Do nothing, just observe",
                    effects={}
                ),
                EventChoice(
                    text="Create a branching point",
                    effects={},
                    creates_timeline=True
                ),
            ]
        )


class MemoryEventGenerator(EventGenerator):
    """Generates memory fragment events"""

    def __init__(self, memories: List[Any], weight: float = 0.4):
        super().__init__(weight)
        self.memories = memories

    def can_generate(self, context: Dict[str, Any]) -> bool:
        uncollected = [m for m in self.memories if not m.collected]
        return len(uncollected) > 0 and random.random() < self.weight

    def generate(self, context: Dict[str, Any]) -> Event:
        uncollected = [m for m in self.memories if not m.collected]
        memory = random.choice(uncollected)

        return Event(
            name="Memory Fragment",
            description=f"A fragment of memory surfaces...\n\n\"{memory.text}\"",
            choices=[
                EventChoice(
                    text="Collect this memory",
                    effects={},
                    collect_memory=memory
                ),
                EventChoice(
                    text="Let it fade",
                    effects={}
                ),
            ]
        )


# =============================================================================
# EVENT MANAGER
# =============================================================================

class EventManager:
    """
    Manages event generation using multiple generators.
    Replaces the monolithic generate_event() function.
    """

    def __init__(self, memories: List[Any] = None):
        self.generators: List[EventGenerator] = [
            TechnologyEventGenerator(weight=1.0),
            SocietyEventGenerator(weight=1.0),
            ConsciousnessEventGenerator(weight=1.0),
            QuantumEventGenerator(weight=0.8),
            DefaultEventGenerator(weight=2.0),  # Higher weight as fallback
        ]

        if memories:
            self.generators.append(MemoryEventGenerator(memories))

    def generate_event(self, timeline: Any) -> Event:
        """
        Generate an event for the given timeline.

        This replaces the 180-line generate_event() function with
        a clean, extensible system.
        """
        # Build context from timeline
        context = {
            'timeline_id': timeline.id,
            'turn': 0,  # Should be passed in
            'color': timeline.get_color() if hasattr(timeline, 'get_color') else '',
            'technology_level': timeline.properties.get('technology_level', 5),
            'society_stability': timeline.properties.get('society_stability', 5),
            'consciousness_awareness': timeline.properties.get('consciousness_awareness', 5),
            'environment_health': timeline.properties.get('environment_health', 5),
        }

        # Filter generators that can produce events
        available = [g for g in self.generators if g.can_generate(context)]

        if not available:
            # Fallback to default
            return DefaultEventGenerator().generate(context)

        # Weight-based selection
        weights = [g.get_weight(context) for g in available]
        selected = random.choices(available, weights=weights)[0]

        return selected.generate(context)

    def add_generator(self, generator: EventGenerator) -> None:
        """Add a custom event generator"""
        self.generators.append(generator)

    def remove_generator(self, generator_type: type) -> None:
        """Remove generators of a specific type"""
        self.generators = [g for g in self.generators
                          if not isinstance(g, generator_type)]


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == '__main__':
    print("Event Generators Module")
    print("=" * 60)
    print("\nThis module demonstrates refactoring a 180-line function")
    print("into smaller, testable, extensible components.")
    print()
    print("Benefits:")
    print("  ✓ Each generator is ~30 lines (manageable)")
    print("  ✓ Easy to test individual generators")
    print("  ✓ Easy to add new event types")
    print("  ✓ Easy to modify event logic")
    print("  ✓ Follows Single Responsibility Principle")
    print()
    print("To use in echo_chambers.py:")
    print("  manager = EventManager(self.all_memories)")
    print("  event = manager.generate_event(timeline)")
