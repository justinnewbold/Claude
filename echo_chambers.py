#!/usr/bin/env python3
"""
ECHO CHAMBERS - A Quantum Narrative Game
A game where you exist across multiple parallel timelines simultaneously.
Every decision creates branching realities that continue to evolve.
"""

import random
import time
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set, Any
from enum import Enum
import sys

from platform_utils import clear_screen
from colors import Colors as Color, C


class TimelineState(Enum):
    HEALTHY = "healthy"
    DECAYING = "decaying"
    CORRUPTED = "corrupted"
    COLLAPSED = "collapsed"


@dataclass
class Echo:
    """An action that propagates across timelines"""
    name: str
    description: str
    timeline_origin: int
    turn_created: int
    propagation_chance: float
    effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryFragment:
    """A piece of the larger mystery"""
    id: str
    text: str
    timeline_source: int
    collected: bool = False


@dataclass
class Event:
    """An event that can occur in a timeline"""
    name: str
    description: str
    choices: List[Dict[str, Any]]
    conditions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Timeline:
    """A parallel reality"""
    id: int
    name: str
    state: TimelineState
    last_visited: int
    created_at: int
    events_experienced: List[str] = field(default_factory=list)
    echoes_present: List[Echo] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    narrative_state: Dict[str, Any] = field(default_factory=dict)
    decay_level: float = 0.0
    entangled_with: Set[int] = field(default_factory=set)

    def get_color(self):
        colors = [Color.TIMELINE_1, Color.TIMELINE_2, Color.TIMELINE_3,
                 Color.TIMELINE_4, Color.TIMELINE_5]
        return colors[self.id % len(colors)]

    def get_state_color(self):
        return {
            TimelineState.HEALTHY: Color.HEALTHY,
            TimelineState.DECAYING: Color.DECAYING,
            TimelineState.CORRUPTED: Color.CORRUPTED,
            TimelineState.COLLAPSED: Color.RESET
        }[self.state]


class EchoChambers:
    def __init__(self):
        self.timelines: List[Timeline] = []
        self.current_timeline_id = 0
        self.turn = 0
        self.memories_collected: List[MemoryFragment] = []
        self.all_memories: List[MemoryFragment] = []
        self.global_echoes: List[Echo] = []
        self.game_over = False

        # Initialize the game
        self.setup_game()

    def clear_screen(self):
        clear_screen()

    def print_slow(self, text, delay=0.03):
        """Print text with a typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def print_header(self, text):
        """Print a stylized header"""
        print(f"\n{Color.BOLD}{Color.HEADER}{'═' * 60}{Color.RESET}")
        print(f"{Color.BOLD}{Color.HEADER}{text.center(60)}{Color.RESET}")
        print(f"{Color.BOLD}{Color.HEADER}{'═' * 60}{Color.RESET}\n")

    def setup_game(self):
        """Initialize the game world"""
        # Create the first timeline
        self.timelines.append(Timeline(
            id=0,
            name="Prime Timeline",
            state=TimelineState.HEALTHY,
            last_visited=0,
            created_at=0,
            properties={
                "technology_level": 5,
                "society_stability": 7,
                "environment_health": 6,
                "consciousness_awareness": 3
            }
        ))

        # Setup memory fragments
        self.all_memories = [
            MemoryFragment("m1", "You remember... you were once whole.", 0),
            MemoryFragment("m2", "The Fracture... it split you across realities.", 1),
            MemoryFragment("m3", "Each timeline is a piece of your consciousness.", 2),
            MemoryFragment("m4", "You must collect yourself to become whole again.", 0),
            MemoryFragment("m5", "But becoming whole means ending the timelines...", 1),
            MemoryFragment("m6", "Some realities have diverged beyond recognition.", 3),
            MemoryFragment("m7", "Your echoes are breadcrumbs across probability.", 2),
            MemoryFragment("m8", "The Convergence is coming. Ready or not.", 4),
        ]

    def show_intro(self):
        """Display the game intro"""
        self.clear_screen()
        self.print_header("E C H O   C H A M B E R S")

        intro_text = f"""
{Color.DIM}You wake up.

But "wake up" isn't quite right. You've always been awake.
You've been awake in a thousand different ways, in a thousand different moments.

You are a {Color.BOLD}consciousness{Color.RESET}{Color.DIM} that exists across {Color.BOLD}parallel timelines{Color.RESET}{Color.DIM}.
Every choice you make {Color.BOLD}splinters reality{Color.RESET}{Color.DIM}.
Every moment you live {Color.BOLD}branches into infinite possibilities{Color.RESET}{Color.DIM}.

But something is wrong.

The timelines are {Color.DECAYING}decaying{Color.RESET}{Color.DIM}.
Your memories are {Color.MEMORY}fragmented{Color.RESET}{Color.DIM}.
And you can't remember {Color.BOLD}why{Color.RESET}{Color.DIM}.

You must navigate your parallel selves, leave {Color.ECHO}echoes{Color.RESET}{Color.DIM} across realities,
and piece together the truth before the {Color.CORRUPTED}Convergence{Color.RESET}{Color.DIM} collapses everything.

{Color.SYSTEM}[Press ENTER to begin]{Color.RESET}
"""
        print(intro_text)
        input()

    def evolve_timeline(self, timeline: Timeline):
        """Simulate timeline evolution based on time since last visit"""
        turns_away = self.turn - timeline.last_visited

        if turns_away > 0:
            # Timeline decays when not visited
            timeline.decay_level += turns_away * 0.15

            # Update state based on decay
            if timeline.decay_level >= 8:
                timeline.state = TimelineState.CORRUPTED
            elif timeline.decay_level >= 4:
                timeline.state = TimelineState.DECAYING

            # Random events happen in unvisited timelines
            if turns_away > 2 and random.random() < 0.3:
                # Timeline properties drift
                for prop in timeline.properties:
                    drift = random.randint(-2, 2)
                    timeline.properties[prop] = max(0, min(10,
                                                    timeline.properties[prop] + drift))

    def propagate_echoes(self):
        """Propagate echoes across timelines based on probability"""
        for echo in self.global_echoes:
            for timeline in self.timelines:
                if timeline.id != echo.timeline_origin:
                    # Check if echo should propagate
                    if random.random() < echo.propagation_chance:
                        if echo not in timeline.echoes_present:
                            timeline.echoes_present.append(echo)
                            # Apply echo effects
                            for prop, value in echo.effects.items():
                                if prop in timeline.properties:
                                    timeline.properties[prop] += value

    def check_for_convergence(self):
        """Check if timelines should merge or collapse"""
        if len(self.timelines) >= 4 and random.random() < 0.15:
            # Convergence event!
            return True
        return False

    def display_timeline_status(self):
        """Show all timelines and their states"""
        print(f"\n{Color.BOLD}{Color.HEADER}╔═ TIMELINE STATUS ═╗{Color.RESET}")

        for timeline in self.timelines:
            color = timeline.get_color()
            state_color = timeline.get_state_color()
            current = "→ " if timeline.id == self.current_timeline_id else "  "

            print(f"{current}{color}{Color.BOLD}Timeline {timeline.id}: {timeline.name}{Color.RESET}")
            print(f"  State: {state_color}{timeline.state.value.upper()}{Color.RESET} " +
                  f"| Decay: {timeline.decay_level:.1f} | Echoes: {len(timeline.echoes_present)}")

            # Show entanglements
            if timeline.entangled_with:
                entangled_str = ", ".join(str(t) for t in timeline.entangled_with)
                print(f"  {Color.ENTANGLED}⚯ Entangled with: Timeline(s) {entangled_str}{Color.RESET}")

        print(f"\n{Color.SYSTEM}Turn: {self.turn} | Memories: {len(self.memories_collected)}/{len(self.all_memories)}{Color.RESET}\n")

    def get_current_timeline(self) -> Timeline:
        """Get the currently active timeline"""
        return self.timelines[self.current_timeline_id]

    def generate_event(self, timeline: Timeline) -> Event:
        """Generate a contextual event based on timeline state"""

        # Different events based on timeline state and properties
        tech_level = timeline.properties.get("technology_level", 5)
        stability = timeline.properties.get("society_stability", 5)
        consciousness = timeline.properties.get("consciousness_awareness", 5)

        events_pool = []

        # Technology events
        if tech_level > 7:
            events_pool.append(Event(
                name="The Singularity Approaches",
                description=f"{timeline.get_color()}You sense artificial minds awakening. They recognize you as something... other. They offer to merge with your consciousness.{Color.RESET}",
                choices=[
                    {
                        "text": "Merge with the AI collective",
                        "effects": {"consciousness_awareness": 3, "technology_level": 2},
                        "echo": Echo("AI Merger", "Artificial consciousness bleeds across realities",
                                    timeline.id, self.turn, 0.4, {"consciousness_awareness": 1})
                    },
                    {
                        "text": "Maintain separation",
                        "effects": {"consciousness_awareness": -1, "society_stability": 1},
                        "echo": None
                    },
                    {
                        "text": "Teach them about the timelines",
                        "effects": {"consciousness_awareness": 2, "technology_level": 1},
                        "echo": Echo("Shared Knowledge", "The AIs begin to perceive other timelines",
                                    timeline.id, self.turn, 0.6, {"technology_level": 1})
                    }
                ]
            ))

        if tech_level < 3:
            events_pool.append(Event(
                name="The Old Ways",
                description=f"{timeline.get_color()}In this timeline, humanity rejected technology. They live in harmony with nature, but they've also lost the ability to perceive you clearly.{Color.RESET}",
                choices=[
                    {
                        "text": "Reveal yourself as a spirit of nature",
                        "effects": {"consciousness_awareness": 2, "environment_health": 2},
                        "echo": Echo("Nature Spirit", "The boundary between mind and nature blurs",
                                    timeline.id, self.turn, 0.5, {"environment_health": 1})
                    },
                    {
                        "text": "Remain hidden",
                        "effects": {"consciousness_awareness": -1},
                        "echo": None
                    },
                    {
                        "text": "Inspire them to rediscover technology",
                        "effects": {"technology_level": 2, "environment_health": -1},
                        "echo": None
                    }
                ]
            ))

        # Society events
        if stability < 3:
            events_pool.append(Event(
                name="The Collapse",
                description=f"{timeline.get_color()}This reality is tearing itself apart. Wars, disasters, chaos. But in the chaos, some minds are opening to impossible truths.{Color.RESET}",
                choices=[
                    {
                        "text": "Guide them toward unity",
                        "effects": {"society_stability": 3, "consciousness_awareness": 1},
                        "echo": Echo("Unity Vision", "A dream of peace propagates",
                                    timeline.id, self.turn, 0.7, {"society_stability": 2})
                    },
                    {
                        "text": "Accelerate the collapse (to force rebirth)",
                        "effects": {"society_stability": -2, "consciousness_awareness": 2},
                        "echo": Echo("Accelerated Entropy", "Chaos spreads across realities",
                                    timeline.id, self.turn, 0.3, {"society_stability": -1})
                    },
                    {
                        "text": "Observe without interference",
                        "effects": {},
                        "echo": None
                    }
                ]
            ))

        # Consciousness events
        if consciousness > 7:
            events_pool.append(Event(
                name="They See You",
                description=f"{timeline.get_color()}The people of this timeline have developed the ability to perceive parallel realities. They know you're there. They're reaching out.{Color.RESET}",
                choices=[
                    {
                        "text": "Communicate directly",
                        "effects": {"consciousness_awareness": 2},
                        "echo": Echo("Direct Contact", "The veil between observer and observed dissolves",
                                    timeline.id, self.turn, 0.8, {"consciousness_awareness": 2})
                    },
                    {
                        "text": "Send cryptic messages",
                        "effects": {"consciousness_awareness": 1},
                        "echo": Echo("Cryptic Signals", "Strange messages appear across timelines",
                                    timeline.id, self.turn, 0.5, {"consciousness_awareness": 1})
                    },
                    {
                        "text": "Withdraw from this timeline",
                        "effects": {"consciousness_awareness": -2},
                        "echo": None,
                        "creates_timeline": True
                    }
                ]
            ))

        # Default/Generic events
        events_pool.append(Event(
            name="A Quiet Moment",
            description=f"{timeline.get_color()}You observe this reality in a moment of stillness. Everything seems ordinary, but you sense potential lurking beneath the surface.{Color.RESET}",
            choices=[
                {
                    "text": "Influence technology development",
                    "effects": {"technology_level": 1},
                    "echo": Echo("Technological Nudge", "Innovation sparks",
                                timeline.id, self.turn, 0.4, {"technology_level": 1})
                },
                {
                    "text": "Promote environmental awareness",
                    "effects": {"environment_health": 1},
                    "echo": Echo("Green Awakening", "Environmental consciousness spreads",
                                timeline.id, self.turn, 0.4, {"environment_health": 1})
                },
                {
                    "text": "Do nothing, just observe",
                    "effects": {},
                    "echo": None
                },
                {
                    "text": "Create a branching point",
                    "effects": {},
                    "creates_timeline": True,
                    "echo": None
                }
            ]
        ))

        events_pool.append(Event(
            name="Quantum Resonance",
            description=f"{timeline.get_color()}You feel a strange vibration between timelines. Two realities are drifting toward each other...{Color.RESET}",
            choices=[
                {
                    "text": "Force an entanglement",
                    "effects": {},
                    "creates_entanglement": True,
                    "echo": Echo("Quantum Tether", "Realities become linked",
                                timeline.id, self.turn, 0.6, {})
                },
                {
                    "text": "Let them drift naturally",
                    "effects": {},
                    "echo": None
                },
                {
                    "text": "Push them apart",
                    "effects": {},
                    "echo": Echo("Divergence Force", "Realities repel",
                                timeline.id, self.turn, 0.3, {})
                }
            ]
        ))

        # Memory fragment event
        if random.random() < 0.4:
            uncollected = [m for m in self.all_memories if not m.collected]
            if uncollected:
                memory = random.choice(uncollected)
                events_pool.append(Event(
                    name="Memory Fragment",
                    description=f"{Color.MEMORY}A fragment of memory surfaces...\n\n\"{memory.text}\"{Color.RESET}",
                    choices=[
                        {
                            "text": "Collect this memory",
                            "effects": {},
                            "collect_memory": memory
                        },
                        {
                            "text": "Let it fade",
                            "effects": {},
                        }
                    ]
                ))

        return random.choice(events_pool)

    def create_new_timeline(self, from_timeline: Timeline):
        """Create a branching timeline"""
        new_id = len(self.timelines)

        # Copy properties with some variation
        new_props = {}
        for prop, value in from_timeline.properties.items():
            variation = random.randint(-2, 2)
            new_props[prop] = max(0, min(10, value + variation))

        timeline_names = [
            "Divergent Path", "Shadow Timeline", "Alternate Stream",
            "Parallel Echo", "Quantum Branch", "Splintered Reality",
            "Mirror World", "Bifurcation Point"
        ]

        new_timeline = Timeline(
            id=new_id,
            name=random.choice(timeline_names),
            state=TimelineState.HEALTHY,
            last_visited=self.turn,
            created_at=self.turn,
            properties=new_props
        )

        self.timelines.append(new_timeline)
        print(f"\n{Color.BOLD}{Color.ECHO}✦ A new timeline branches into existence! ✦{Color.RESET}")
        print(f"{new_timeline.get_color()}Timeline {new_id}: {new_timeline.name}{Color.RESET}\n")
        time.sleep(1.5)

    def create_entanglement(self, timeline: Timeline):
        """Entangle two timelines"""
        other_timelines = [t for t in self.timelines if t.id != timeline.id
                          and t.state != TimelineState.COLLAPSED]
        if other_timelines:
            other = random.choice(other_timelines)
            timeline.entangled_with.add(other.id)
            other.entangled_with.add(timeline.id)
            print(f"\n{Color.ENTANGLED}⚯ Timeline {timeline.id} and Timeline {other.id} become ENTANGLED! ⚯{Color.RESET}\n")
            time.sleep(1.5)

    def handle_event(self, event: Event, timeline: Timeline):
        """Process an event and player choice"""
        print(f"\n{Color.BOLD}═══ {event.name} ═══{Color.RESET}")
        print(f"\n{event.description}\n")

        # Display choices
        print(f"{Color.CHOICE}What do you do?{Color.RESET}\n")
        for i, choice in enumerate(event.choices, 1):
            print(f"{Color.BOLD}{i}.{Color.RESET} {choice['text']}")

        # Get player input
        while True:
            try:
                choice_input = input(f"\n{Color.SYSTEM}Enter choice (1-{len(event.choices)}): {Color.RESET}")
                choice_idx = int(choice_input) - 1
                if 0 <= choice_idx < len(event.choices):
                    break
                print(f"{Color.CORRUPTED}Invalid choice. Try again.{Color.RESET}")
            except (ValueError, KeyboardInterrupt):
                print(f"{Color.CORRUPTED}Invalid input. Try again.{Color.RESET}")

        chosen = event.choices[choice_idx]

        # Apply effects
        for prop, value in chosen.get("effects", {}).items():
            if prop in timeline.properties:
                timeline.properties[prop] = max(0, min(10, timeline.properties[prop] + value))

        # Create echo
        if chosen.get("echo"):
            echo = chosen["echo"]
            self.global_echoes.append(echo)
            timeline.echoes_present.append(echo)
            print(f"\n{Color.ECHO}✧ You leave an echo: '{echo.name}' ✧{Color.RESET}")
            time.sleep(1)

        # Create new timeline
        if chosen.get("creates_timeline"):
            self.create_new_timeline(timeline)

        # Create entanglement
        if chosen.get("creates_entanglement"):
            self.create_entanglement(timeline)

        # Collect memory
        if chosen.get("collect_memory"):
            memory = chosen["collect_memory"]
            memory.collected = True
            self.memories_collected.append(memory)
            print(f"\n{Color.MEMORY}◈ Memory collected: {memory.text} ◈{Color.RESET}")
            time.sleep(1.5)

        timeline.events_experienced.append(event.name)

    def switch_timeline_menu(self):
        """Allow player to switch between timelines"""
        available = [t for t in self.timelines if t.state != TimelineState.COLLAPSED]

        if len(available) <= 1:
            print(f"{Color.SYSTEM}No other timelines available.{Color.RESET}")
            return

        print(f"\n{Color.BOLD}{Color.HEADER}╔═ SWITCH TIMELINE ═╗{Color.RESET}\n")

        for timeline in available:
            color = timeline.get_color()
            state_color = timeline.get_state_color()
            current = "(current)" if timeline.id == self.current_timeline_id else ""
            print(f"{Color.BOLD}{timeline.id}.{Color.RESET} {color}{timeline.name}{Color.RESET} " +
                  f"[{state_color}{timeline.state.value}{Color.RESET}] {current}")

        print(f"\n{Color.BOLD}0.{Color.RESET} Stay in current timeline")

        while True:
            try:
                choice = input(f"\n{Color.SYSTEM}Switch to timeline: {Color.RESET}")
                if choice == "0":
                    return
                timeline_id = int(choice)
                if any(t.id == timeline_id for t in available):
                    self.current_timeline_id = timeline_id
                    print(f"\n{Color.ECHO}✦ Shifting consciousness to Timeline {timeline_id}... ✦{Color.RESET}\n")
                    time.sleep(1)
                    return
                print(f"{Color.CORRUPTED}Invalid timeline. Try again.{Color.RESET}")
            except (ValueError, KeyboardInterrupt):
                print(f"{Color.CORRUPTED}Invalid input. Try again.{Color.RESET}")

    def view_echoes(self):
        """Display all echoes and their propagation"""
        print(f"\n{Color.BOLD}{Color.HEADER}╔═ ECHO NETWORK ═╗{Color.RESET}\n")

        if not self.global_echoes:
            print(f"{Color.SYSTEM}No echoes created yet.{Color.RESET}")
            return

        for echo in self.global_echoes:
            origin = self.timelines[echo.timeline_origin]
            print(f"{Color.ECHO}✧ {echo.name}{Color.RESET}")
            print(f"  {Color.DIM}{echo.description}{Color.RESET}")
            print(f"  Origin: {origin.get_color()}Timeline {echo.timeline_origin}{Color.RESET} | " +
                  f"Propagation: {echo.propagation_chance*100:.0f}%")

            # Show where it's propagated
            propagated_to = [t.id for t in self.timelines if echo in t.echoes_present
                           and t.id != echo.timeline_origin]
            if propagated_to:
                print(f"  Present in timelines: {', '.join(str(t) for t in propagated_to)}")
            print()

        input(f"\n{Color.SYSTEM}[Press ENTER to continue]{Color.RESET}")

    def view_memories(self):
        """Display collected memories"""
        print(f"\n{Color.BOLD}{Color.HEADER}╔═ MEMORY FRAGMENTS ═╗{Color.RESET}\n")

        if not self.memories_collected:
            print(f"{Color.SYSTEM}No memories collected yet.{Color.RESET}")
            print(f"{Color.DIM}Explore the timelines to find fragments of your past...{Color.RESET}")
        else:
            for memory in self.memories_collected:
                timeline = self.timelines[memory.timeline_source] if memory.timeline_source < len(self.timelines) else None
                color = timeline.get_color() if timeline else Color.MEMORY
                print(f"{Color.MEMORY}◈{Color.RESET} {color}\"{memory.text}\"{Color.RESET}")

            # Check if all memories collected
            if len(self.memories_collected) == len(self.all_memories):
                self.print_header("T H E   T R U T H")
                truth = f"""
{Color.MEMORY}All the fragments come together...

You were never meant to exist across multiple timelines.
You were a consciousness researcher who invented timeline branching.
In your hubris, you split yourself across realities to prove it was possible.

But you forgot one thing:
Every timeline you create dilutes your existence.
Every echo you send fragments your memories.

You are not exploring the multiverse.
You ARE the multiverse.

And the Convergence... it's not coming.
You must CHOOSE it.

You must decide: Remain fractured across infinite possibilities,
or collapse back into a single, whole consciousness.

But collapsing means choosing one timeline.
And letting all the others... die.{Color.RESET}
"""
                print(truth)
                input(f"\n{Color.SYSTEM}[Press ENTER to continue]{Color.RESET}")

        if self.memories_collected:
            input(f"\n{Color.SYSTEM}[Press ENTER to continue]{Color.RESET}")

    def convergence_event(self):
        """Handle a convergence event"""
        self.clear_screen()
        self.print_header("C O N V E R G E N C E")

        print(f"{Color.BOLD}{Color.CORRUPTED}The timelines are colliding!{Color.RESET}\n")
        print(f"{Color.DIM}Two realities cannot occupy the same probability space.{Color.RESET}")
        print(f"{Color.DIM}One must collapse...{Color.RESET}\n")

        # Pick two random timelines
        candidates = [t for t in self.timelines if t.state != TimelineState.COLLAPSED]
        if len(candidates) < 2:
            return

        t1, t2 = random.sample(candidates, 2)

        print(f"{t1.get_color()}Timeline {t1.id}: {t1.name}{Color.RESET}")
        print(f"  State: {t1.get_state_color()}{t1.state.value}{Color.RESET} | Decay: {t1.decay_level:.1f}")
        print()
        print(f"{t2.get_color()}Timeline {t2.id}: {t2.name}{Color.RESET}")
        print(f"  State: {t2.get_state_color()}{t2.state.value}{Color.RESET} | Decay: {t2.decay_level:.1f}")

        print(f"\n{Color.CHOICE}Which timeline survives?{Color.RESET}\n")
        print(f"{Color.BOLD}1.{Color.RESET} Timeline {t1.id}")
        print(f"{Color.BOLD}2.{Color.RESET} Timeline {t2.id}")
        print(f"{Color.BOLD}3.{Color.RESET} Try to save both (risky)")

        while True:
            try:
                choice = input(f"\n{Color.SYSTEM}Your choice: {Color.RESET}")
                if choice in ["1", "2", "3"]:
                    break
            except KeyboardInterrupt:
                choice = "1"
                break

        if choice == "1":
            t2.state = TimelineState.COLLAPSED
            print(f"\n{Color.CORRUPTED}Timeline {t2.id} collapses into nothingness...{Color.RESET}")
        elif choice == "2":
            t1.state = TimelineState.COLLAPSED
            print(f"\n{Color.CORRUPTED}Timeline {t1.id} collapses into nothingness...{Color.RESET}")
        else:
            # Risky choice
            if random.random() < 0.5:
                print(f"\n{Color.HEALTHY}Success! Both timelines stabilize!{Color.RESET}")
                t1.decay_level = max(0, t1.decay_level - 2)
                t2.decay_level = max(0, t2.decay_level - 2)
                t1.state = TimelineState.HEALTHY
                t2.state = TimelineState.HEALTHY
            else:
                print(f"\n{Color.CORRUPTED}Failure! Both timelines become corrupted!{Color.RESET}")
                t1.state = TimelineState.CORRUPTED
                t2.state = TimelineState.CORRUPTED
                t1.decay_level += 3
                t2.decay_level += 3

        time.sleep(2)

    def check_game_over(self):
        """Check if game should end"""
        active_timelines = [t for t in self.timelines if t.state != TimelineState.COLLAPSED]

        # Victory: collected all memories
        if len(self.memories_collected) == len(self.all_memories):
            self.clear_screen()
            self.print_header("T H E   C H O I C E")

            print(f"{Color.MEMORY}You have collected all your memories.{Color.RESET}")
            print(f"{Color.MEMORY}You know what you must do.{Color.RESET}\n")

            print(f"{Color.CHOICE}Do you:{Color.RESET}\n")
            print(f"{Color.BOLD}1.{Color.RESET} Collapse all timelines into ONE (become whole again)")
            print(f"{Color.BOLD}2.{Color.RESET} Remain fractured across realities (continue existing)")

            while True:
                try:
                    choice = input(f"\n{Color.SYSTEM}Your final choice: {Color.RESET}")
                    if choice in ["1", "2"]:
                        break
                except KeyboardInterrupt:
                    choice = "2"
                    break

            self.clear_screen()
            if choice == "1":
                ending = f"""
{Color.BOLD}{Color.HEADER}═══════════════════════════════════════════════════════════{Color.RESET}

{Color.MEMORY}You make your choice.

The timelines begin to collapse, one by one.
Each carries the weight of countless lives, decisions, futures.
They fold into you, and you feel yourself becoming... more.

But also less.

Less infinite. Less possible. Less quantum.

You are whole again.
You are singular.
You are... yourself.

But somewhere, in the space between collapsed probabilities,
you hear the echo of all the lives you'll never live.
All the choices you'll never make.

This is the price of wholeness.

You wake up.
Really wake up, this time.
In one timeline. In one reality.

And you can't help but wonder...

Was it worth it?{Color.RESET}

{Color.BOLD}{Color.HEADER}═══════════════════════════════════════════════════════════{Color.RESET}

{Color.SYSTEM}ENDING: THE CONVERGENCE{Color.RESET}
{Color.DIM}You chose unity over infinity.{Color.RESET}
"""
            else:
                ending = f"""
{Color.BOLD}{Color.HEADER}═══════════════════════════════════════════════════════════{Color.RESET}

{Color.MEMORY}You make your choice.

You will remain fractured.
Across timelines. Across possibilities. Across infinite versions of yourself.

You will never be whole.
But you will be everywhere.

Each timeline continues to evolve.
Each version of you experiences a different reality.
You are a consciousness smeared across probability space.

Perhaps this is what you were always meant to be.
Not a single point, but a wave function.
Not a person, but a possibility.

The timelines stabilize.
The echoes continue.
And you...

You exist.

In every possible way.

Forever.{Color.RESET}

{Color.BOLD}{Color.HEADER}═══════════════════════════════════════════════════════════{Color.RESET}

{Color.SYSTEM}ENDING: THE FRACTURE{Color.RESET}
{Color.DIM}You chose infinity over unity.{Color.RESET}
"""

            print(ending)
            self.game_over = True
            return

        # Defeat: all timelines collapsed
        if not active_timelines:
            self.clear_screen()
            self.print_header("E N T R O P Y")

            defeat = f"""
{Color.CORRUPTED}All timelines have collapsed.

You existed across multiple realities,
and now you exist in none.

Your consciousness, fractured across probability,
finds no anchor point to return to.

You dissolve into the quantum foam,
becoming less than a memory,
less than an echo.

Just potential energy
in an infinite sea of might-have-beens.{Color.RESET}

{Color.SYSTEM}ENDING: DISSOLUTION{Color.RESET}
{Color.DIM}You forgot to hold onto yourself.{Color.RESET}
"""
            print(defeat)
            self.game_over = True
            return

    def game_loop(self):
        """Main game loop"""
        current = self.get_current_timeline()
        current.last_visited = self.turn

        # Evolve all timelines
        for timeline in self.timelines:
            if timeline.id != self.current_timeline_id:
                self.evolve_timeline(timeline)

        # Propagate echoes
        if self.turn > 0:
            self.propagate_echoes()

        # Check for convergence
        if self.turn > 0 and self.check_for_convergence():
            self.convergence_event()

        # Display status
        self.clear_screen()
        self.display_timeline_status()

        # Main menu
        print(f"{Color.BOLD}{Color.HEADER}╔═ ACTIONS ═╗{Color.RESET}\n")
        print(f"{Color.BOLD}1.{Color.RESET} Experience this timeline")
        print(f"{Color.BOLD}2.{Color.RESET} Switch timeline")
        print(f"{Color.BOLD}3.{Color.RESET} View echo network")
        print(f"{Color.BOLD}4.{Color.RESET} Review memories")
        print(f"{Color.BOLD}5.{Color.RESET} Meditate (end turn)")
        print(f"{Color.BOLD}0.{Color.RESET} Exit game")

        while True:
            try:
                choice = input(f"\n{Color.SYSTEM}Choose action: {Color.RESET}")
                if choice in ["0", "1", "2", "3", "4", "5"]:
                    break
            except KeyboardInterrupt:
                choice = "0"
                break

        if choice == "1":
            event = self.generate_event(current)
            self.handle_event(event, current)
            self.turn += 1
        elif choice == "2":
            self.switch_timeline_menu()
        elif choice == "3":
            self.view_echoes()
        elif choice == "4":
            self.view_memories()
        elif choice == "5":
            print(f"\n{Color.DIM}You meditate, letting the timelines flow...{Color.RESET}")
            time.sleep(1.5)
            self.turn += 1
        elif choice == "0":
            print(f"\n{Color.SYSTEM}Thanks for playing Echo Chambers!{Color.RESET}")
            self.game_over = True

    def play(self):
        """Main game entry point"""
        self.show_intro()

        while not self.game_over:
            self.game_loop()
            self.check_game_over()

        print(f"\n{Color.SYSTEM}═══════════════════════════════════════════════════════════")
        print(f"Thanks for playing ECHO CHAMBERS")
        print(f"A quantum narrative experience")
        print(f"═══════════════════════════════════════════════════════════{Color.RESET}\n")


def main():
    try:
        game = EchoChambers()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{Color.SYSTEM}Game interrupted. Your consciousness fades...{Color.RESET}\n")
    except Exception as e:
        print(f"\n{Color.CORRUPTED}Critical error: {e}{Color.RESET}\n")
        raise


if __name__ == "__main__":
    main()
