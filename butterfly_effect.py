#!/usr/bin/env python3
"""
THE BUTTERFLY EFFECT

A chaos theory puzzle game about sensitive dependence on initial conditions.

In chaos theory, the butterfly effect describes how tiny changes in initial
conditions can lead to vastly different outcomes. A butterfly flaps its wings
in Brazil, and weeks later a tornado forms in Texas.

In this game, you make microscopic interventions in a simulated world,
then watch as those tiny changes cascade into completely different futures.

Your goal: Orchestrate chaos to achieve specific outcomes.
"""

import random
import time
import os
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum

# ANSI colors
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Elements
    PARTICLE = '\033[38;5;51m'      # Cyan - particle
    WALL = '\033[38;5;240m'         # Gray - wall
    GOAL = '\033[38;5;46m'          # Green - goal
    DANGER = '\033[38;5;203m'       # Red - danger
    AGENT = '\033[38;5;226m'        # Yellow - agent
    INTERVENTION = '\033[38;5;141m' # Purple - intervention

    # UI
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    ERROR = '\033[38;5;203m'
    CHAOS = '\033[38;5;201m'
    WARNING = '\033[38;5;214m'


class CellType(Enum):
    EMPTY = "empty"
    WALL = "wall"
    PARTICLE = "particle"
    AGENT = "agent"
    GOAL = "goal"
    DANGER = "danger"


@dataclass
class Cell:
    """A cell in the simulation grid"""
    cell_type: CellType
    velocity: Tuple[float, float] = (0.0, 0.0)  # For physics
    energy: float = 1.0


@dataclass
class SimulationState:
    """The state of the world at a moment in time"""
    width: int
    height: int
    grid: List[List[Cell]]
    timestep: int = 0

    def copy(self) -> 'SimulationState':
        """Deep copy of simulation state"""
        new_grid = []
        for row in self.grid:
            new_row = []
            for cell in row:
                new_cell = Cell(
                    cell_type=cell.cell_type,
                    velocity=cell.velocity,
                    energy=cell.energy
                )
                new_row.append(new_cell)
            new_grid.append(new_row)

        return SimulationState(
            width=self.width,
            height=self.height,
            grid=new_grid,
            timestep=self.timestep
        )

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get cell at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def set_cell(self, x: int, y: int, cell: Cell):
        """Set cell at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = cell


@dataclass
class Intervention:
    """A tiny change you make to initial conditions"""
    x: int
    y: int
    description: str
    velocity_delta: Tuple[float, float] = (0.0, 0.0)
    energy_delta: float = 0.0


class ChaosSimulator:
    """Simulates a chaotic physical system"""

    def __init__(self, state: SimulationState):
        self.state = state
        self.gravity = 0.1
        self.friction = 0.95
        self.bounce = -0.7

    def step(self):
        """Advance simulation one timestep"""
        new_grid = [[Cell(CellType.EMPTY) for _ in range(self.state.width)]
                    for _ in range(self.state.height)]

        # Copy walls and static elements
        for y in range(self.state.height):
            for x in range(self.state.width):
                cell = self.state.grid[y][x]
                if cell.cell_type in [CellType.WALL, CellType.GOAL, CellType.DANGER]:
                    new_grid[y][x] = cell

        # Update particles and agents (they have physics)
        for y in range(self.state.height):
            for x in range(self.state.width):
                cell = self.state.grid[y][x]

                if cell.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                    # Apply gravity
                    vx, vy = cell.velocity
                    vy += self.gravity

                    # Apply friction
                    vx *= self.friction
                    vy *= self.friction

                    # Calculate new position
                    new_x = int(x + vx)
                    new_y = int(y + vy)

                    # Boundary checking
                    if new_x < 0 or new_x >= self.state.width:
                        vx *= self.bounce
                        new_x = max(0, min(self.state.width - 1, new_x))

                    if new_y < 0 or new_y >= self.state.height:
                        vy *= self.bounce
                        new_y = max(0, min(self.state.height - 1, new_y))

                    # Check collision with walls
                    target_cell = new_grid[new_y][new_x]
                    if target_cell.cell_type == CellType.WALL:
                        # Bounce off wall
                        vx *= self.bounce
                        vy *= self.bounce
                        new_x, new_y = x, y
                    elif target_cell.cell_type == CellType.EMPTY:
                        # Move to new position
                        new_cell = Cell(
                            cell_type=cell.cell_type,
                            velocity=(vx, vy),
                            energy=cell.energy * 0.99  # Energy decay
                        )
                        new_grid[new_y][new_x] = new_cell
                    else:
                        # Collision with another particle
                        # Simple: stay in place
                        new_cell = Cell(
                            cell_type=cell.cell_type,
                            velocity=(vx * 0.5, vy * 0.5),
                            energy=cell.energy * 0.95
                        )
                        new_grid[y][x] = new_cell

        self.state.grid = new_grid
        self.state.timestep += 1


class ButterflyEffect:
    def __init__(self):
        self.original_state: Optional[SimulationState] = None
        self.current_state: Optional[SimulationState] = None
        self.interventions: List[Intervention] = []
        self.max_interventions = 3
        self.simulation_length = 100
        self.level = 1
        self.game_over = False
        self.victory = False

        self.setup_level(1)

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_level(self, level_num: int):
        """Setup a specific level"""
        width, height = 40, 20
        grid = [[Cell(CellType.EMPTY) for _ in range(width)] for _ in range(height)]

        if level_num == 1:
            # Tutorial: Single particle needs to hit goal
            # Add floor
            for x in range(width):
                grid[height-1][x] = Cell(CellType.WALL)

            # Add some platforms
            for x in range(10, 20):
                grid[15][x] = Cell(CellType.WALL)
            for x in range(25, 35):
                grid[10][x] = Cell(CellType.WALL)

            # Add particle at top
            grid[2][5] = Cell(CellType.PARTICLE, velocity=(0.2, 0.0))

            # Add goal at bottom right
            grid[height-2][35] = Cell(CellType.GOAL)

        elif level_num == 2:
            # Multiple particles, need to get one to goal
            for x in range(width):
                grid[height-1][x] = Cell(CellType.WALL)

            # Platforms creating a maze
            for x in range(5, 15):
                grid[12][x] = Cell(CellType.WALL)
            for x in range(20, 35):
                grid[12][x] = Cell(CellType.WALL)
            for x in range(10, 25):
                grid[8][x] = Cell(CellType.WALL)

            # Multiple particles
            grid[2][8] = Cell(CellType.PARTICLE, velocity=(0.1, 0.0))
            grid[2][12] = Cell(CellType.PARTICLE, velocity=(-0.1, 0.0))
            grid[2][16] = Cell(CellType.PARTICLE, velocity=(0.15, 0.0))

            # Goal in specific location
            grid[height-2][30] = Cell(CellType.GOAL)

        elif level_num == 3:
            # Avoid danger zones
            for x in range(width):
                grid[height-1][x] = Cell(CellType.WALL)

            # Platforms
            for x in range(0, 15):
                grid[15][x] = Cell(CellType.WALL)
            for x in range(25, width):
                grid[15][x] = Cell(CellType.WALL)

            # Danger zones
            for x in range(10, 20):
                grid[height-2][x] = Cell(CellType.DANGER)

            # Agent that must avoid danger
            grid[2][5] = Cell(CellType.AGENT, velocity=(0.3, 0.0))

            # Goal
            grid[height-2][35] = Cell(CellType.GOAL)

        elif level_num == 4:
            # Complex cascade: domino effect
            for x in range(width):
                grid[height-1][x] = Cell(CellType.WALL)

            # Multiple levels of platforms
            for x in range(0, 10):
                grid[16][x] = Cell(CellType.WALL)
            for x in range(15, 25):
                grid[12][x] = Cell(CellType.WALL)
            for x in range(30, width):
                grid[8][x] = Cell(CellType.WALL)

            # Chain of particles
            grid[15][5] = Cell(CellType.PARTICLE, velocity=(0.05, 0.0))
            grid[11][20] = Cell(CellType.PARTICLE, velocity=(0.0, 0.0))
            grid[7][35] = Cell(CellType.PARTICLE, velocity=(0.0, 0.0))

            # Goal at bottom
            grid[height-2][38] = Cell(CellType.GOAL)

        else:
            # Victory!
            self.victory = True
            self.game_over = True
            return

        self.original_state = SimulationState(width=width, height=height, grid=grid)
        self.current_state = self.original_state.copy()
        self.interventions = []

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("T H E   B U T T E R F L Y   E F F E C T")

        intro = f"""
{C.CHAOS}\"A butterfly flaps its wings in Brazil, causing a tornado in Texas.\"{C.RESET}

{C.DIM}Welcome to chaos theory as a puzzle game.

The butterfly effect: Tiny changes in initial conditions lead to
vastly different outcomes. Small causes, big effects.

In this game, you orchestrate chaos.{C.RESET}

{C.BOLD}How It Works:{C.RESET}

1. You see a simulated world with particles, platforms, and goals
2. You can make {C.INTERVENTION}tiny interventions{C.RESET} (nudge particles, add energy)
3. The simulation runs forward 100 timesteps
4. Watch how your tiny changes cascade into major differences
5. Goal: Create specific outcomes through minimal intervention

{C.BOLD}Symbols:{C.RESET}

{C.PARTICLE}●{C.RESET} = Particle (affected by physics)
{C.AGENT}@{C.RESET} = Agent (special particle)
{C.WALL}█{C.RESET} = Wall (solid obstacle)
{C.GOAL}◆{C.RESET} = Goal (target location)
{C.DANGER}✖{C.RESET} = Danger (avoid!)
{C.INTERVENTION}◉{C.RESET} = Your intervention point

{C.BOLD}Controls:{C.RESET}

{C.SYSTEM}Planning Phase:{C.RESET}
  Arrow keys - Move cursor
  V - Add velocity nudge (+0.5 horizontal)
  E - Add energy boost (+2.0)
  R - Reset interventions

{C.SYSTEM}Simulation:{C.RESET}
  ENTER - Run simulation with interventions
  SPACE - Run original (no interventions)

{C.SYSTEM}Other:{C.RESET}
  Q - Quit
  N - Next level (after success)

{C.CHAOS}Small changes. Big consequences.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def render_state(self, state: SimulationState, cursor_pos: Optional[Tuple[int, int]] = None):
        """Render a simulation state"""
        for y in range(state.height):
            line = "  "
            for x in range(state.width):
                cell = state.grid[y][x]

                # Check if this is cursor position
                if cursor_pos and cursor_pos == (x, y):
                    line += f"{C.INTERVENTION}◉{C.RESET}"
                elif cell.cell_type == CellType.WALL:
                    line += f"{C.WALL}█{C.RESET}"
                elif cell.cell_type == CellType.PARTICLE:
                    line += f"{C.PARTICLE}●{C.RESET}"
                elif cell.cell_type == CellType.AGENT:
                    line += f"{C.AGENT}@{C.RESET}"
                elif cell.cell_type == CellType.GOAL:
                    line += f"{C.GOAL}◆{C.RESET}"
                elif cell.cell_type == CellType.DANGER:
                    line += f"{C.DANGER}✖{C.RESET}"
                else:
                    line += f"{C.DIM}·{C.RESET}"
            print(line)

    def apply_interventions(self, state: SimulationState):
        """Apply interventions to a state"""
        for intervention in self.interventions:
            cell = state.get_cell(intervention.x, intervention.y)
            if cell and cell.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                vx, vy = cell.velocity
                dvx, dvy = intervention.velocity_delta
                cell.velocity = (vx + dvx, vy + dvy)
                cell.energy += intervention.energy_delta

    def run_simulation(self, state: SimulationState, steps: int) -> SimulationState:
        """Run simulation forward"""
        sim_state = state.copy()
        simulator = ChaosSimulator(sim_state)

        for _ in range(steps):
            simulator.step()

        return sim_state

    def check_goal(self, state: SimulationState) -> bool:
        """Check if goal is achieved"""
        for y in range(state.height):
            for x in range(state.width):
                cell = state.grid[y][x]
                if cell.cell_type == CellType.GOAL:
                    # Check if any particle/agent is on goal
                    # Actually, let's check neighbors
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]:
                        nx, ny = x + dx, y + dy
                        neighbor = state.get_cell(nx, ny)
                        if neighbor and neighbor.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                            return True
        return False

    def check_danger(self, state: SimulationState) -> bool:
        """Check if agent hit danger"""
        for y in range(state.height):
            for x in range(state.width):
                cell = state.grid[y][x]
                if cell.cell_type == CellType.DANGER:
                    # Check neighbors
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]:
                        nx, ny = x + dx, y + dy
                        neighbor = state.get_cell(nx, ny)
                        if neighbor and neighbor.cell_type == CellType.AGENT:
                            return True
        return False

    def show_planning_screen(self, cursor_x: int, cursor_y: int):
        """Show the planning interface"""
        self.clear_screen()
        print(f"\n{C.CHAOS}╔═ BUTTERFLY EFFECT - PLANNING PHASE ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level} | Interventions: {len(self.interventions)}/{self.max_interventions}{C.RESET}\n")

        self.render_state(self.current_state, cursor_pos=(cursor_x, cursor_y))

        print(f"\n{C.SYSTEM}Cursor: ({cursor_x}, {cursor_y}) | " +
              f"Move: Arrows | Nudge: V | Energy: E | Reset: R | Simulate: ENTER{C.RESET}")

        if self.interventions:
            print(f"\n{C.INTERVENTION}Interventions planned:{C.RESET}")
            for i, interv in enumerate(self.interventions):
                print(f"  {i+1}. {interv.description} at ({interv.x}, {interv.y})")

    def show_simulation(self, final_state: SimulationState, success: bool, danger_hit: bool):
        """Show simulation result"""
        self.clear_screen()
        print(f"\n{C.CHAOS}╔═ BUTTERFLY EFFECT - RESULT ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level} | Timestep: {final_state.timestep}{C.RESET}\n")

        self.render_state(final_state)

        if danger_hit:
            print(f"\n{C.ERROR}✖ FAILURE: Agent hit danger zone!{C.RESET}")
        elif success:
            print(f"\n{C.SUCCESS}✓ SUCCESS: Goal achieved!{C.RESET}")
            print(f"{C.SYSTEM}[Press N for next level]{C.RESET}")
        else:
            print(f"\n{C.WARNING}Goal not reached. Try different interventions.{C.RESET}")
            print(f"{C.SYSTEM}[Press any key to continue]{C.RESET}")

    def show_victory(self):
        """Show victory screen"""
        self.clear_screen()
        self.print_header("C H A O S   M A S T E R E D")

        victory = f"""
{C.SUCCESS}You've learned to orchestrate chaos!{C.RESET}

{C.DIM}The butterfly effect teaches us:

• Small changes can have enormous consequences
• Complex systems are sensitive to initial conditions
• Prediction becomes impossible over long timescales
• Deterministic doesn't mean predictable{C.RESET}

{C.BOLD}Chaos Theory in Nature:{C.RESET}

{C.CHAOS}Weather:{C.RESET} Why we can't predict weather weeks ahead
{C.CHAOS}Ecosystems:{C.RESET} How tiny environmental changes cascade
{C.CHAOS}Economics:{C.RESET} Small market shifts triggering crashes
{C.CHAOS}Evolution:{C.RESET} Tiny mutations creating new species

{C.CHAOS}\"The flap of a butterfly's wings in Brazil can set off
a tornado in Texas.\"{C.RESET}

— Edward Lorenz, chaos theory pioneer

{C.DIM}You've experienced this principle through play:
Tiny interventions creating massive divergence.

This is the mathematics of unpredictability.
This is chaos.{C.RESET}
"""
        print(victory)

    def play(self):
        """Main game loop"""
        self.show_intro()

        cursor_x, cursor_y = 5, 5

        while not self.game_over:
            self.show_planning_screen(cursor_x, cursor_y)

            # Get input
            try:
                import sys, tty, termios
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                    # Handle arrow keys (escape sequences)
                    if ch == '\x1b':
                        ch += sys.stdin.read(2)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)

                # Handle input
                if ch == '\x1b[A':  # Up arrow
                    cursor_y = max(0, cursor_y - 1)
                elif ch == '\x1b[B':  # Down arrow
                    cursor_y = min(self.current_state.height - 1, cursor_y + 1)
                elif ch == '\x1b[D':  # Left arrow
                    cursor_x = max(0, cursor_x - 1)
                elif ch == '\x1b[C':  # Right arrow
                    cursor_x = min(self.current_state.width - 1, cursor_x + 1)
                elif ch.lower() == 'v':
                    # Add velocity intervention
                    if len(self.interventions) < self.max_interventions:
                        cell = self.current_state.get_cell(cursor_x, cursor_y)
                        if cell and cell.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                            intervention = Intervention(
                                x=cursor_x,
                                y=cursor_y,
                                description="Velocity nudge",
                                velocity_delta=(0.5, 0.0)
                            )
                            self.interventions.append(intervention)
                elif ch.lower() == 'e':
                    # Add energy intervention
                    if len(self.interventions) < self.max_interventions:
                        cell = self.current_state.get_cell(cursor_x, cursor_y)
                        if cell and cell.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                            intervention = Intervention(
                                x=cursor_x,
                                y=cursor_y,
                                description="Energy boost",
                                energy_delta=2.0
                            )
                            self.interventions.append(intervention)
                elif ch.lower() == 'r':
                    # Reset interventions
                    self.interventions = []
                    self.current_state = self.original_state.copy()
                elif ch == '\r' or ch == '\n':
                    # Run simulation with interventions
                    sim_state = self.original_state.copy()
                    self.apply_interventions(sim_state)
                    final_state = self.run_simulation(sim_state, self.simulation_length)

                    success = self.check_goal(final_state)
                    danger = self.check_danger(final_state)

                    self.show_simulation(final_state, success, danger)

                    # Wait for input
                    try:
                        tty.setraw(fd)
                        ch2 = sys.stdin.read(1)
                        if ch2.lower() == 'n' and success:
                            self.level += 1
                            self.setup_level(self.level)
                            cursor_x, cursor_y = 5, 5
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old)

                elif ch == ' ':
                    # Run original simulation (no interventions)
                    final_state = self.run_simulation(self.original_state.copy(), self.simulation_length)
                    self.show_simulation(final_state, False, False)

                    try:
                        tty.setraw(fd)
                        sys.stdin.read(1)
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old)

                elif ch.lower() == 'q':
                    self.game_over = True
                    self.victory = False

            except (ImportError, termios.error):
                # Fallback for systems without termios
                cmd = input(f"\n{C.SYSTEM}Command: {C.RESET}").lower().strip()

                if cmd in ['w', 'up']:
                    cursor_y = max(0, cursor_y - 1)
                elif cmd in ['s', 'down']:
                    cursor_y = min(self.current_state.height - 1, cursor_y + 1)
                elif cmd in ['a', 'left']:
                    cursor_x = max(0, cursor_x - 1)
                elif cmd in ['d', 'right']:
                    cursor_x = min(self.current_state.width - 1, cursor_x + 1)
                elif cmd == 'v':
                    if len(self.interventions) < self.max_interventions:
                        cell = self.current_state.get_cell(cursor_x, cursor_y)
                        if cell and cell.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                            intervention = Intervention(
                                x=cursor_x,
                                y=cursor_y,
                                description="Velocity nudge",
                                velocity_delta=(0.5, 0.0)
                            )
                            self.interventions.append(intervention)
                elif cmd == 'e':
                    if len(self.interventions) < self.max_interventions:
                        cell = self.current_state.get_cell(cursor_x, cursor_y)
                        if cell and cell.cell_type in [CellType.PARTICLE, CellType.AGENT]:
                            intervention = Intervention(
                                x=cursor_x,
                                y=cursor_y,
                                description="Energy boost",
                                energy_delta=2.0
                            )
                            self.interventions.append(intervention)
                elif cmd == 'r' or cmd == 'reset':
                    self.interventions = []
                    self.current_state = self.original_state.copy()
                elif cmd == 'enter' or cmd == 'simulate' or cmd == '':
                    sim_state = self.original_state.copy()
                    self.apply_interventions(sim_state)
                    final_state = self.run_simulation(sim_state, self.simulation_length)

                    success = self.check_goal(final_state)
                    danger = self.check_danger(final_state)

                    self.show_simulation(final_state, success, danger)

                    if success:
                        next_cmd = input(f"{C.SYSTEM}Next level? (y/n): {C.RESET}").lower()
                        if next_cmd == 'y':
                            self.level += 1
                            self.setup_level(self.level)
                            cursor_x, cursor_y = 5, 5
                    else:
                        input(f"{C.SYSTEM}Press ENTER to continue...{C.RESET}")

                elif cmd == 'space' or cmd == 'original':
                    final_state = self.run_simulation(self.original_state.copy(), self.simulation_length)
                    self.show_simulation(final_state, False, False)
                    input(f"{C.SYSTEM}Press ENTER to continue...{C.RESET}")

                elif cmd == 'q' or cmd == 'quit':
                    self.game_over = True
                    self.victory = False

        # Game over
        if self.victory:
            self.show_victory()
        else:
            print(f"\n{C.SYSTEM}Exiting chaos simulator...{C.RESET}\n")

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE BUTTERFLY EFFECT")
        print(f"Small changes, big consequences")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = ButterflyEffect()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.CHAOS}Chaos interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
