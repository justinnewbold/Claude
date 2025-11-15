#!/usr/bin/env python3
"""
THE GARDEN OF FORKING PATHS

Based on Jorge Luis Borges' story of the same name.

You exist at a moment of decision. Before you, all possible futures branch
infinitely. You can see them all simultaneously - every choice, every outcome,
every path forward.

Your goal is known. The path is not.

Navigate the labyrinth of time itself.
"""

import random
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# ANSI colors
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Path colors
    SUCCESS = '\033[38;5;46m'      # Green - leads to goal
    FAILURE = '\033[38;5;196m'     # Red - leads to death/failure
    UNKNOWN = '\033[38;5;243m'     # Gray - unexplored
    CURRENT = '\033[38;5;226m'     # Yellow - current position
    POSSIBLE = '\033[38;5;87m'     # Cyan - possible futures

    # Special
    GOAL = '\033[38;5;201m'        # Magenta - the goal
    PARADOX = '\033[38;5;141m'     # Purple - temporal paradox

    # UI
    HEADER = '\033[38;5;87m'
    HIGHLIGHT = '\033[38;5;226m'
    SYSTEM = '\033[38;5;243m'
    LORE = '\033[38;5;183m'


class OutcomeType(Enum):
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILURE = "failure"
    CONTINUE = "continue"
    PARADOX = "paradox"


@dataclass
class FutureNode:
    """A moment in a possible future"""
    id: str
    depth: int
    description: str
    choice_made: Optional[str]
    outcome: OutcomeType
    children: List['FutureNode'] = field(default_factory=list)
    visited: bool = False
    leads_to_goal: Optional[bool] = None  # Discovered through exploration


@dataclass
class Choice:
    """A choice at a branching point"""
    text: str
    future_node: FutureNode


class GardenOfForkingPaths:
    def __init__(self):
        self.current_depth = 0
        self.max_vision_depth = 3  # How many steps ahead you can see
        self.decisions_made = 0
        self.paths_explored = 0
        self.dead_ends_found = 0
        self.paradoxes_discovered = 0
        self.game_over = False
        self.goal_reached = False

        # The goal (changes each playthrough)
        self.goal_description = ""
        self.goal_depth = 0

        # Current path through time
        self.current_path: List[FutureNode] = []

        # Root of the future tree
        self.root: Optional[FutureNode] = None

        self.setup_game()

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_slow(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_game(self):
        """Initialize the game with a random goal"""
        goals = [
            ("prevent the assassination of the scholar", 8),
            ("retrieve the ancient manuscript before it burns", 7),
            ("escape the labyrinth before midnight", 9),
            ("deliver the warning before the invasion", 8),
            ("find the one person who remembers your name", 10),
            ("save your past self from a fatal mistake", 8),
            ("discover which timeline is real", 9),
            ("break the time loop", 7),
        ]

        self.goal_description, self.goal_depth = random.choice(goals)

        # Generate the future tree
        self.root = self.generate_future_branch(None, 0, self.goal_depth)

    def generate_future_branch(self, parent_choice: Optional[str], depth: int, max_depth: int) -> FutureNode:
        """Recursively generate a tree of possible futures"""

        node_id = f"future_{depth}_{random.randint(1000, 9999)}"

        # Determine if this is a terminal node
        is_terminal = depth >= max_depth or random.random() < (depth * 0.15)

        # Generate description based on depth and parent
        description = self.generate_moment_description(depth, parent_choice)

        # Determine outcome
        if depth == max_depth:
            # One path leads to success
            if random.random() < 0.3:  # 30% chance this branch can succeed
                outcome = OutcomeType.SUCCESS
            else:
                outcome = OutcomeType.FAILURE
        elif is_terminal:
            outcome = random.choice([OutcomeType.FAILURE, OutcomeType.PARADOX])
        else:
            outcome = OutcomeType.CONTINUE

        node = FutureNode(
            id=node_id,
            depth=depth,
            description=description,
            choice_made=parent_choice,
            outcome=outcome
        )

        # Generate children if not terminal
        if not is_terminal and depth < max_depth:
            num_choices = random.randint(2, 4)
            choices_available = self.get_available_choices(depth)

            for i in range(min(num_choices, len(choices_available))):
                choice_text = choices_available[i] if i < len(choices_available) else f"choice_{i}"
                child = self.generate_future_branch(choice_text, depth + 1, max_depth)
                node.children.append(child)

        return node

    def generate_moment_description(self, depth: int, choice: Optional[str]) -> str:
        """Generate a description of a future moment"""

        moments = [
            # Depth 0-2: Initial situations
            [
                "you stand at a crossroads under a blood moon",
                "you find yourself in a library that shouldn't exist",
                "a stranger approaches with urgent news",
                "you discover a letter addressed to your future self",
                "the clock strikes thirteen",
            ],
            # Depth 3-5: Complications
            [
                "your choice leads to an unexpected ally",
                "time seems to slow, then accelerate",
                "you recognize this moment from a dream",
                "the path splits in ways you didn't anticipate",
                "you encounter your past self",
                "a door appears that wasn't there before",
            ],
            # Depth 6-8: Climax approaching
            [
                "the timeline fractures around you",
                "you see multiple versions of this moment simultaneously",
                "reality becomes negotiable",
                "the scholar appears, unaware of their fate",
                "you reach the point of no return",
                "time itself seems to hold its breath",
            ],
            # Depth 9+: Resolution
            [
                "this is the moment everything was leading to",
                "you stand at the convergence of all possible paths",
                "the future crystallizes into a single point",
                "you make the choice that matters",
            ]
        ]

        category = min(depth // 3, len(moments) - 1)
        base = random.choice(moments[category])

        if choice:
            return f"having chosen to {choice}, {base}"
        return base

    def get_available_choices(self, depth: int) -> List[str]:
        """Get contextual choices based on depth"""

        choice_pools = [
            # Early choices
            [
                "take the left path",
                "take the right path",
                "wait and observe",
                "call out to the stranger",
                "hide in the shadows",
                "read the letter immediately",
                "burn the letter unread",
            ],
            # Mid choices
            [
                "trust the ally",
                "proceed alone",
                "examine the temporal anomaly",
                "try to warn your past self",
                "embrace the paradox",
                "fight against the timeline",
                "surrender to fate",
            ],
            # Late choices
            [
                "intervene directly",
                "let events unfold",
                "create a distraction",
                "reveal the truth",
                "maintain the deception",
                "sacrifice yourself",
                "save the scholar",
            ]
        ]

        category = min(depth // 3, len(choice_pools) - 1)
        pool = choice_pools[category]
        random.shuffle(pool)
        return pool

    def show_intro(self):
        """Display introduction"""
        self.clear_screen()
        self.print_header("T H E   G A R D E N   O F   F O R K I N G   P A T H S")

        intro = f"""
{C.DIM}"In all fictional works, each time a man is confronted with several
alternatives, he chooses one and eliminates the others; in the fiction
of Ts'ui Pên, he chooses—simultaneously—all of them."

— Jorge Luis Borges{C.RESET}

{C.LORE}You exist at a pivotal moment.

Before you, time branches infinitely. Every choice creates new futures.
Every decision eliminates infinite possibilities.

But you have a gift: {C.BOLD}you can see the futures before you choose{C.RESET}{C.LORE}.

Not all of them. Not infinitely far. But enough to navigate the labyrinth.{C.RESET}

{C.GOAL}Your goal: {self.goal_description}{C.RESET}

{C.DIM}You can see {self.max_vision_depth} moments into each possible future.
Choose wisely. Some paths lead to paradox. Some to failure. Some to success.

Time is a garden of forking paths.
You must find the one true path through it.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def visualize_futures(self, node: FutureNode, depth: int = 0, prefix: str = "", is_last: bool = True):
        """Recursively visualize the decision tree"""

        if depth > self.max_vision_depth:
            return

        # Determine color based on node state
        if node.visited:
            color = C.CURRENT
        elif node.outcome == OutcomeType.SUCCESS:
            color = C.SUCCESS
        elif node.outcome == OutcomeType.FAILURE:
            color = C.FAILURE
        elif node.outcome == OutcomeType.PARADOX:
            color = C.PARADOX
        else:
            color = C.UNKNOWN

        # Determine symbol
        if node.outcome == OutcomeType.SUCCESS:
            symbol = "★"
        elif node.outcome == OutcomeType.FAILURE:
            symbol = "✗"
        elif node.outcome == OutcomeType.PARADOX:
            symbol = "⚠"
        elif node.visited:
            symbol = "●"
        else:
            symbol = "○"

        # Print this node
        connector = "└── " if is_last else "├── "
        if depth == 0:
            connector = ""
            prefix = ""

        print(f"{prefix}{connector}{color}{symbol} {node.description[:50]}{C.RESET}")

        # Print children
        if node.children and depth < self.max_vision_depth:
            extension = "    " if is_last else "│   "
            new_prefix = prefix + extension

            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                self.visualize_futures(child, depth + 1, new_prefix, is_last_child)

    def explore_node(self, node: FutureNode):
        """Explore deeper into a future node"""
        node.visited = True
        self.paths_explored += 1

        # Check if this path leads to goal (propagate backwards)
        if node.outcome == OutcomeType.SUCCESS:
            node.leads_to_goal = True
            return True
        elif node.outcome in [OutcomeType.FAILURE, OutcomeType.PARADOX]:
            node.leads_to_goal = False
            if node.outcome == OutcomeType.PARADOX:
                self.paradoxes_discovered += 1
            else:
                self.dead_ends_found += 1
            return False
        else:
            # Continue - check children
            if node.children:
                any_leads_to_goal = any(
                    self.explore_node(child) for child in node.children
                )
                node.leads_to_goal = any_leads_to_goal
                return any_leads_to_goal
            else:
                # Dead end
                node.leads_to_goal = False
                self.dead_ends_found += 1
                return False

    def show_current_moment(self, node: FutureNode):
        """Display the current moment and available futures"""
        self.clear_screen()

        self.print_header(f"DEPTH: {node.depth} / {self.goal_depth}")

        print(f"{C.GOAL}Goal: {self.goal_description}{C.RESET}\n")

        print(f"{C.CURRENT}{C.BOLD}═══ CURRENT MOMENT ═══{C.RESET}\n")
        print(f"{C.LORE}{node.description}{C.RESET}\n")

        if not node.children:
            # Terminal node
            if node.outcome == OutcomeType.SUCCESS:
                print(f"{C.SUCCESS}{C.BOLD}✓ SUCCESS! You have achieved your goal!{C.RESET}\n")
                self.goal_reached = True
            elif node.outcome == OutcomeType.FAILURE:
                print(f"{C.FAILURE}{C.BOLD}✗ FAILURE. This path leads to ruin.{C.RESET}\n")
            elif node.outcome == OutcomeType.PARADOX:
                print(f"{C.PARADOX}{C.BOLD}⚠ PARADOX. You encounter your future self. Time collapses.{C.RESET}\n")

            input(f"{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
            return None

        # Show visible futures
        print(f"{C.POSSIBLE}{C.BOLD}═══ VISIBLE FUTURES ═══{C.RESET}\n")
        print(f"{C.DIM}You peer ahead and see the following possible paths...{C.RESET}\n")

        self.visualize_futures(node, 0)

        print(f"\n{C.BOLD}{C.HEADER}═══ CHOOSE YOUR PATH ═══{C.RESET}\n")

        # List choices
        for i, child in enumerate(node.children, 1):
            choice_color = C.RESET
            hint = ""

            if child.visited:
                if child.leads_to_goal:
                    choice_color = C.SUCCESS
                    hint = " [Leads to goal]"
                elif child.leads_to_goal is False:
                    choice_color = C.FAILURE
                    hint = " [Dead end]"
                else:
                    choice_color = C.UNKNOWN
                    hint = " [Uncertain]"

            print(f"{C.BOLD}{i}.{C.RESET} {choice_color}{child.choice_made}{hint}{C.RESET}")

        print(f"\n{C.BOLD}0.{C.RESET} Meditate on the future (explore paths more deeply)")
        print(f"{C.BOLD}9.{C.RESET} Give up")

        # Get choice
        while True:
            try:
                choice = input(f"\n{C.SYSTEM}Your decision: {C.RESET}")

                if choice == "0":
                    return "meditate"
                elif choice == "9":
                    return "give_up"

                choice_int = int(choice)
                if 1 <= choice_int <= len(node.children):
                    return node.children[choice_int - 1]

                print(f"{C.FAILURE}Invalid choice.{C.RESET}")
            except (ValueError, KeyboardInterrupt, EOFError):
                print(f"{C.FAILURE}Invalid input.{C.RESET}")

    def meditate(self, node: FutureNode):
        """Explore futures more deeply without committing"""
        self.clear_screen()

        print(f"\n{C.BOLD}{C.PARADOX}═══ MEDITATION ON FUTURES ═══{C.RESET}\n")
        print(f"{C.DIM}You close your eyes and peer deeper into the branching paths...")
        print(f"Exploring consequences...{C.RESET}\n")

        time.sleep(1.5)

        # Explore all visible children
        discoveries = 0
        for child in node.children:
            if not child.visited:
                self.explore_node(child)
                discoveries += 1

        if discoveries > 0:
            print(f"{C.SUCCESS}You gain clarity on {discoveries} possible futures.{C.RESET}\n")
        else:
            print(f"{C.DIM}You've already explored all visible paths deeply.{C.RESET}\n")

        input(f"{C.SYSTEM}[Press ENTER to return]{C.RESET}")

    def show_stats(self):
        """Show game statistics"""
        print(f"\n{C.SYSTEM}═══ JOURNEY STATISTICS ═══")
        print(f"Depth reached: {self.current_depth}/{self.goal_depth}")
        print(f"Decisions made: {self.decisions_made}")
        print(f"Paths explored: {self.paths_explored}")
        print(f"Dead ends found: {self.dead_ends_found}")
        print(f"Paradoxes discovered: {self.paradoxes_discovered}{C.RESET}\n")

    def show_ending(self, success: bool):
        """Show game ending"""
        self.clear_screen()

        if success:
            self.print_header("S U C C E S S")

            ending = f"""
{C.SUCCESS}You have achieved your goal: {self.goal_description}

By seeing all possible futures, you navigated the labyrinth of time.
You found the one true path through the garden of forking paths.{C.RESET}

{C.LORE}But in doing so, you eliminated infinite other possibilities.
Infinite other you's, in infinite other timelines, failed.

You succeeded because you could see what they could not:
The shape of time itself.{C.RESET}

{C.PARADOX}"Every moment bifurcates into infinite futures.
You simply chose the right sequence of moments." {C.RESET}

"""
            print(ending)
            self.show_stats()

        else:
            self.print_header("F A I L U R E")

            ending = f"""
{C.FAILURE}You did not achieve your goal: {self.goal_description}

Perhaps you chose poorly.
Perhaps the true path was hidden beyond your vision.
Perhaps success was never possible in this timeline.{C.RESET}

{C.LORE}Somewhere, in another branch of time, another version of you
made different choices. Perhaps they succeeded where you failed.{C.RESET}

{C.PARADOX}"In infinite time, all things happen to all men." {C.RESET}

"""
            print(ending)
            self.show_stats()

    def play(self):
        """Main game loop"""
        self.show_intro()

        current_node = self.root

        while not self.game_over:
            if current_node is None:
                self.game_over = True
                break

            result = self.show_current_moment(current_node)

            if result is None:
                # Terminal node reached
                self.game_over = True
                break
            elif result == "meditate":
                self.meditate(current_node)
            elif result == "give_up":
                self.game_over = True
                self.goal_reached = False
                break
            elif isinstance(result, FutureNode):
                # Move to chosen future
                current_node = result
                self.current_path.append(current_node)
                self.decisions_made += 1
                self.current_depth = current_node.depth

        # Show ending
        self.show_ending(self.goal_reached)

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE GARDEN OF FORKING PATHS")
        print(f"Based on the story by Jorge Luis Borges")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = GardenOfForkingPaths()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.SYSTEM}You step out of the garden. Time flows linearly once more.{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.FAILURE}Temporal error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
