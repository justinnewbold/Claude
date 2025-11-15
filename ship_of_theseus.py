#!/usr/bin/env python3
"""
THE SHIP OF THESEUS

The ancient paradox: If you replace every part of a ship gradually,
is it still the same ship?

You are a robot exploring dungeons. You can replace your parts.
But each replacement changes you. Are you still... you?

Your discarded parts remain behind. They assemble into OTHER YOUS.
Who is the real you? The one with original parts? Or continuous consciousness?

Navigate. Upgrade. Discard. Question your identity.
"""

import random
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum

# ANSI colors
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Identity colors (fade as you become less "original")
    ORIGINAL = '\033[38;5;51m'      # Bright cyan - 100% original
    MOSTLY_YOU = '\033[38;5;45m'    # Cyan - 75% original
    HALF_YOU = '\033[38;5;39m'      # Blue-cyan - 50% original
    BARELY_YOU = '\033[38;5;33m'    # Blue - 25% original
    NOT_YOU = '\033[38;5;240m'      # Gray - 0% original

    # Parts
    PART_OLD = '\033[38;5;243m'     # Gray - old discarded
    PART_NEW = '\033[38;5;46m'      # Green - new upgrade

    # Clones
    CLONE = '\033[38;5;196m'        # Red - assembled from your parts

    # UI
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    ERROR = '\033[38;5;203m'
    IDENTITY = '\033[38;5;141m'
    GOAL = '\033[38;5;226m'


class PartType(Enum):
    BODY = "body"
    HEAD = "head"
    ARMS = "arms"
    LEGS = "legs"
    CORE = "core"


@dataclass
class Part:
    """A component of the robot"""
    part_type: PartType
    generation: int  # 0 = original, higher = more upgraded
    unique_id: str   # Identifies this specific part instance

    def __repr__(self):
        return f"{self.part_type.value}_{self.generation}"


@dataclass
class Entity:
    """A robot entity (player or clone)"""
    position: Tuple[int, int]
    parts: Dict[PartType, Part]
    is_player: bool
    identity_score: float  # 0-1, how "original" are you
    memory: List[str] = field(default_factory=list)

    def get_identity_color(self):
        if self.identity_score >= 0.8:
            return C.ORIGINAL
        elif self.identity_score >= 0.6:
            return C.MOSTLY_YOU
        elif self.identity_score >= 0.4:
            return C.HALF_YOU
        elif self.identity_score >= 0.2:
            return C.BARELY_YOU
        else:
            return C.NOT_YOU


@dataclass
class Level:
    """A level in the dungeon"""
    width: int
    height: int
    player: Entity
    clones: List[Entity] = field(default_factory=list)
    upgrade_parts: Dict[Tuple[int, int], Part] = field(default_factory=dict)
    discarded_parts: Dict[Tuple[int, int], Part] = field(default_factory=dict)
    walls: Set[Tuple[int, int]] = field(default_factory=set)
    goal_pos: Optional[Tuple[int, int]] = None


class ShipOfTheseus:
    def __init__(self):
        # Create original player
        original_parts = {
            PartType.BODY: Part(PartType.BODY, 0, "original_body"),
            PartType.HEAD: Part(PartType.HEAD, 0, "original_head"),
            PartType.ARMS: Part(PartType.ARMS, 0, "original_arms"),
            PartType.LEGS: Part(PartType.LEGS, 0, "original_legs"),
            PartType.CORE: Part(PartType.CORE, 0, "original_core"),
        }

        self.level = Level(
            width=50,
            height=15,
            player=Entity(
                position=(2, 2),
                parts=original_parts,
                is_player=True,
                identity_score=1.0,
                memory=["You awaken. All parts original."]
            )
        )

        self.game_over = False
        self.victory = False
        self.parts_replaced = 0
        self.clones_created = 0
        self.philosophical_events = []

        self.setup_level()

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_level(self):
        """Generate level with parts and walls"""
        # Add walls
        for x in range(self.level.width):
            self.level.walls.add((x, 0))
            self.level.walls.add((x, self.level.height - 1))
        for y in range(self.level.height):
            self.level.walls.add((0, y))
            self.level.walls.add((self.level.width - 1, y))

        # Add some obstacles
        for _ in range(20):
            x, y = random.randint(5, self.level.width - 5), random.randint(2, self.level.height - 3)
            self.level.walls.add((x, y))

        # Place upgrade parts
        part_types = list(PartType)
        for _ in range(15):
            x = random.randint(5, self.level.width - 2)
            y = random.randint(2, self.level.height - 2)
            if (x, y) not in self.level.walls and (x, y) != self.level.player.position:
                part_type = random.choice(part_types)
                gen = random.randint(1, 3)
                part = Part(part_type, gen, f"upgrade_{part_type.value}_{random.randint(1000, 9999)}")
                self.level.upgrade_parts[(x, y)] = part

        # Set goal
        self.level.goal_pos = (self.level.width - 3, self.level.height - 3)

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("T H E   S H I P   O F   T H E S E U S")

        intro = f"""
{C.IDENTITY}"If you replace every part of yourself, are you still you?"{C.RESET}

{C.DIM}You are a robot explorer. As you navigate the dungeon, you find
upgraded parts to replace your aging components.

But each replacement changes you. Your identity shifts.

Your discarded parts don't disappear. They remain on the ground.
And when enough parts accumulate... they {C.CLONE}assemble into another you{C.RESET}{C.DIM}.

Who is the real you?{C.RESET}

{C.BOLD}The Paradox:{C.RESET}

The Ship of Theseus - an ancient philosophical puzzle:
If a ship has all its parts replaced gradually, is it the same ship?

And if the old parts are reassembled... which is the real ship?

{C.BOLD}Gameplay:{C.RESET}

{C.SUCCESS}+{C.RESET} = Upgrade part (better stats, but less "you")
{C.PART_OLD}o{C.RESET} = Your discarded part
{C.CLONE}×{C.RESET} = Clone (assembled from your old parts)
{C.ORIGINAL}@{C.RESET} = You (color shows identity)
{C.GOAL}G{C.RESET} = Goal

{C.BOLD}Controls:{C.RESET}

W/A/S/D - Move
P - Replace part (when standing on upgrade)
M - View memories and identity
Q - Quit

{C.IDENTITY}The more you upgrade, the less "you" you become.
But staying original means staying weak.

What is identity? Continuity? Or original components?{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def calculate_identity(self, entity: Entity) -> float:
        """Calculate identity score based on original parts"""
        original_count = sum(1 for part in entity.parts.values() if part.generation == 0)
        return original_count / len(entity.parts)

    def render_level(self):
        """Render current level"""
        player_color = self.level.player.get_identity_color()

        print(f"\n{C.IDENTITY}╔═ THE SHIP OF THESEUS ═╗{C.RESET}")
        print(f"{C.SYSTEM}Identity: {self.level.player.identity_score*100:.0f}% | " +
              f"Parts replaced: {self.parts_replaced} | Clones: {len(self.level.clones)}{C.RESET}\n")

        # Render grid
        for y in range(self.level.height):
            line = "  "
            for x in range(self.level.width):
                pos = (x, y)

                if pos == self.level.player.position:
                    line += f"{player_color}@{C.RESET}"
                elif pos == self.level.goal_pos:
                    line += f"{C.GOAL}G{C.RESET}"
                elif any(clone.position == pos for clone in self.level.clones):
                    line += f"{C.CLONE}×{C.RESET}"
                elif pos in self.level.discarded_parts:
                    line += f"{C.PART_OLD}o{C.RESET}"
                elif pos in self.level.upgrade_parts:
                    line += f"{C.PART_NEW}+{C.RESET}"
                elif pos in self.level.walls:
                    line += "#"
                else:
                    line += "."
            print(line)

        # Show current parts
        print(f"\n{C.SYSTEM}Your parts:{C.RESET}")
        for part_type, part in self.level.player.parts.items():
            color = C.ORIGINAL if part.generation == 0 else C.PART_NEW
            print(f"  {color}{part_type.value}: gen{part.generation}{C.RESET}")

        print(f"\n{C.SYSTEM}Move: W/A/S/D | Replace part: P | Memories: M | Quit: Q{C.RESET}")

    def move_player(self, dx: int, dy: int):
        """Move the player"""
        x, y = self.level.player.position
        new_x, new_y = x + dx, y + dy

        # Check walls
        if (new_x, new_y) in self.level.walls:
            return

        # Check clones
        if any(clone.position == (new_x, new_y) for clone in self.level.clones):
            self.philosophical_event("meet_clone")
            return

        # Move
        self.level.player.position = (new_x, new_y)

        # Check goal
        if self.level.player.position == self.level.goal_pos:
            self.victory = True
            self.game_over = True

    def replace_part(self):
        """Replace a part if standing on upgrade"""
        pos = self.level.player.position

        if pos not in self.level.upgrade_parts:
            print(f"\n{C.ERROR}No upgrade part here!{C.RESET}")
            time.sleep(0.5)
            return

        new_part = self.level.upgrade_parts[pos]
        old_part = self.level.player.parts[new_part.part_type]

        # Replace
        self.level.player.parts[new_part.part_type] = new_part
        del self.level.upgrade_parts[pos]

        # Discard old part
        self.level.discarded_parts[pos] = old_part

        # Update identity
        self.level.player.identity_score = self.calculate_identity(self.level.player)
        self.parts_replaced += 1

        # Add memory
        memory = f"Replaced {new_part.part_type.value}: gen{old_part.generation}→gen{new_part.generation}. Identity: {self.level.player.identity_score*100:.0f}%"
        self.level.player.memory.append(memory)

        print(f"\n{C.SUCCESS}Replaced {new_part.part_type.value}!{C.RESET}")
        print(f"{C.IDENTITY}Identity now: {self.level.player.identity_score*100:.0f}%{C.RESET}")
        time.sleep(1)

        # Check for clone creation
        self.try_create_clone()

        # Philosophical events
        if self.level.player.identity_score == 0:
            self.philosophical_event("zero_identity")
        elif self.level.player.identity_score <= 0.5 and self.parts_replaced == 3:
            self.philosophical_event("half_replaced")

    def try_create_clone(self):
        """Check if we can assemble a clone from discarded parts"""
        # Count parts by type
        part_counts = {pt: 0 for pt in PartType}
        available_parts = {}

        for pos, part in self.level.discarded_parts.items():
            part_counts[part.part_type] += 1
            if part.part_type not in available_parts:
                available_parts[part.part_type] = (pos, part)

        # Need at least one of each type
        if all(count >= 1 for count in part_counts.values()):
            # Create clone
            clone_parts = {}
            positions_to_remove = []

            for part_type, (pos, part) in available_parts.items():
                clone_parts[part_type] = part
                positions_to_remove.append(pos)

            # Remove used parts
            for pos in positions_to_remove:
                del self.level.discarded_parts[pos]

            # Place clone at average position
            avg_x = sum(p[0] for p in positions_to_remove) // len(positions_to_remove)
            avg_y = sum(p[1] for p in positions_to_remove) // len(positions_to_remove)

            clone = Entity(
                position=(avg_x, avg_y),
                parts=clone_parts,
                is_player=False,
                identity_score=self.calculate_identity(Entity(
                    position=(0,0),
                    parts=clone_parts,
                    is_player=False,
                    identity_score=0
                )),
                memory=[f"Assembled from discarded parts. Identity: {self.calculate_identity(Entity(position=(0,0), parts=clone_parts, is_player=False, identity_score=0))*100:.0f}%"]
            )

            self.level.clones.append(clone)
            self.clones_created += 1

            print(f"\n{C.CLONE}{C.BOLD}A CLONE ASSEMBLES FROM YOUR DISCARDED PARTS!{C.RESET}")
            print(f"{C.CLONE}It has {clone.identity_score*100:.0f}% of your original identity.{C.RESET}")
            time.sleep(2)

            self.philosophical_event("clone_created")

    def philosophical_event(self, event_type: str):
        """Trigger philosophical reflection"""
        events = {
            "meet_clone": "You face a being made of your old parts. It looks at you. You are both the Ship of Theseus. Or neither of you are.",
            "zero_identity": "You have replaced every original part. Nothing of the original remains. Are you still you? Or are you a new being with its memories?",
            "half_replaced": "You are half original, half new. The Ship of Theseus stands at the midpoint. When did you stop being you?",
            "clone_created": "A new entity emerges from your cast-offs. It has more original parts than you do. Which of you is the real you?"
        }

        if event_type in events:
            self.philosophical_events.append(events[event_type])

    def view_memories(self):
        """View identity and memories"""
        self.clear_screen()
        self.print_header("I D E N T I T Y   &   M E M O R Y")

        color = self.level.player.get_identity_color()
        print(f"\n{C.BOLD}Current Identity: {color}{self.level.player.identity_score*100:.0f}% original{C.RESET}\n")

        print(f"{C.SYSTEM}Original parts remaining:{C.RESET}")
        for part_type, part in self.level.player.parts.items():
            if part.generation == 0:
                print(f"  {C.ORIGINAL}✓ {part_type.value}{C.RESET}")
            else:
                print(f"  {C.PART_NEW}✗ {part_type.value} (replaced with gen{part.generation}){C.RESET}")

        print(f"\n{C.SYSTEM}Memory log:{C.RESET}")
        for memory in self.level.player.memory[-10:]:  # Last 10
            print(f"  {C.DIM}{memory}{C.RESET}")

        if self.philosophical_events:
            print(f"\n{C.IDENTITY}Philosophical reflections:{C.RESET}")
            for event in self.philosophical_events:
                print(f"  {C.IDENTITY}{event}{C.RESET}\n")

        # Show clones
        if self.level.clones:
            print(f"\n{C.CLONE}Entities assembled from your parts:{C.RESET}")
            for i, clone in enumerate(self.level.clones, 1):
                print(f"  {C.CLONE}Clone #{i}: {clone.identity_score*100:.0f}% original identity{C.RESET}")

        input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")

    def show_ending(self):
        """Show game ending"""
        self.clear_screen()
        self.print_header("T H E   P A R A D O X   R E S O L V E D ?")

        identity = self.level.player.identity_score * 100

        print(f"\n{C.BOLD}You reached the goal.{C.RESET}\n")
        print(f"Identity: {C.IDENTITY}{identity:.0f}% original{C.RESET}")
        print(f"Parts replaced: {self.parts_replaced}/{len(PartType)}")
        print(f"Clones created: {self.clones_created}\n")

        # Philosophical conclusion based on identity
        if identity == 100:
            conclusion = f"""{C.ORIGINAL}You remained completely original.
Every part is as it began. You are definitively YOU.

But you never grew. Never changed. Never improved.
Is stagnation the price of identity?{C.RESET}"""
        elif identity >= 80:
            conclusion = f"""{C.MOSTLY_YOU}You kept most of yourself intact.
Careful upgrades. Measured change. You are mostly YOU.

You balanced identity with growth.
The ship sails on, recognizable but renewed.{C.RESET}"""
        elif identity >= 50:
            conclusion = f"""{C.HALF_YOU}You stand at the threshold.
Half original. Half new. Neither fully one nor the other.

The paradox embodied. Are you the same? Different?
Perhaps identity is not binary.{C.RESET}"""
        elif identity > 0:
            conclusion = f"""{C.BARELY_YOU}Almost nothing original remains.
You are new, wearing the memories of the old.

The Ship of Theseus has been rebuilt.
But the voyages continue. Is continuity enough?{C.RESET}"""
        else:
            conclusion = f"""{C.NOT_YOU}Every part replaced. Nothing original remains.
You are entirely new. The old you exists only in memory.

And yet... you remember being that other you.
Are memories enough to preserve identity?{C.RESET}"""

        print(conclusion)

        print(f"\n{C.IDENTITY}The paradox has no answer.{C.RESET}")
        print(f"{C.DIM}Identity is continuous consciousness? Or original components?")
        print(f"The ship that changes? Or the parts that remain?")
        print(f"You decide.{C.RESET}")

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            self.clear_screen()
            self.render_level()

            # Get input
            try:
                import sys, tty, termios
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)

                if ch.lower() == 'w':
                    self.move_player(0, -1)
                elif ch.lower() == 's':
                    self.move_player(0, 1)
                elif ch.lower() == 'a':
                    self.move_player(-1, 0)
                elif ch.lower() == 'd':
                    self.move_player(1, 0)
                elif ch.lower() == 'p':
                    self.replace_part()
                elif ch.lower() == 'm':
                    self.view_memories()
                elif ch.lower() == 'q':
                    self.game_over = True
                    self.victory = False

            except (ImportError, termios.error):
                cmd = input(f"\n{C.SYSTEM}Command: {C.RESET}").lower().strip()

                if cmd in ['w', 'up']:
                    self.move_player(0, -1)
                elif cmd in ['s', 'down']:
                    self.move_player(0, 1)
                elif cmd in ['a', 'left']:
                    self.move_player(-1, 0)
                elif cmd in ['d', 'right']:
                    self.move_player(1, 0)
                elif cmd == 'p':
                    self.replace_part()
                elif cmd == 'm':
                    self.view_memories()
                elif cmd == 'q':
                    self.game_over = True
                    self.victory = False

        # Ending
        if self.victory:
            self.show_ending()

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE SHIP OF THESEUS")
        print(f"A paradox about identity")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = ShipOfTheseus()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.IDENTITY}Identity crisis interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
