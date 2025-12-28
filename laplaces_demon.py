#!/usr/bin/env python3
"""
LAPLACE'S DEMON

Perfect knowledge of the present = Perfect prediction of the future.
Rewind time. Watch it unfold exactly the same way.
Every atom, every thought, every choice - predetermined.

Free will in a deterministic universe?

Based on Pierre-Simon Laplace's thought experiment (1814).
"""

import random, time
from dataclasses import dataclass, field
from typing import List
from colors import C
from platform_utils import clear_screen


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    
@dataclass
class UniverseState:
    tick: int
    particles: List[Particle]
    
class LaplacesDemon:
    def __init__(self):
        self.initial_state = None
        self.history = []
        self.tick = 0
        
    def clear_screen(self):
        clear_screen()
        
    def init_universe(self):
        """Create initial deterministic universe"""
        random.seed(42)  # Deterministic!
        particles = [Particle(
            x=random.uniform(10, 50),
            y=random.uniform(5, 15),
            vx=random.uniform(-2, 2),
            vy=random.uniform(-2, 2)
        ) for _ in range(5)]
        self.initial_state = UniverseState(0, particles)
        self.history = [self.initial_state]
        
    def step_universe(self, state: UniverseState) -> UniverseState:
        """Deterministic physics step"""
        new_particles = []
        for p in state.particles:
            new_x = p.x + p.vx
            new_y = p.y + p.vy
            new_vx, new_vy = p.vx, p.vy
            
            # Bounce off walls (deterministic)
            if new_x <= 0 or new_x >= 60: new_vx = -new_vx
            if new_y <= 0 or new_y >= 20: new_vy = -new_vy
            
            new_particles.append(Particle(new_x, new_y, new_vx, new_vy))
            
        return UniverseState(state.tick + 1, new_particles)
        
    def show_intro(self):
        self.clear_screen()
        title = "LAPLACE'S DEMON"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.DEMON}"We may regard the present state of the universe as the effect
of its past and the cause of its future."{C.RESET}

{C.DIM}Pierre-Simon Laplace (1814) imagined an intellect that knows:
• The precise location of every atom
• The precise momentum of every atom
• All forces acting between them{C.RESET}

{C.DEMON}For such an intellect, nothing would be uncertain.
The future, like the past, would be present before its eyes.{C.RESET}

{C.BOLD}You are that demon.{C.RESET}

{C.BOLD}Controls:{C.RESET}
SPACE - Advance time one step
R - Rewind to beginning  
P - Predict future (auto-play)
Q - Quit

{C.DEMON}Watch the universe unfold deterministically.
Rewind. Watch it unfold exactly the same way.{C.RESET}

{C.SYSTEM}[Press ENTER to observe the universe]{C.RESET}
""")
        input()
        
    def show_universe(self):
        self.clear_screen()
        print(f"\n{C.DEMON}╔═ LAPLACE'S DEMON ═╗{C.RESET}")
        print(f"{C.SYSTEM}Tick: {self.tick}{C.RESET}\n")
        
        # Render particles
        grid = [[' ' for _ in range(60)] for _ in range(20)]
        state = self.history[min(self.tick, len(self.history)-1)]
        
        for p in state.particles:
            x, y = int(p.x), int(p.y)
            if 0 <= x < 60 and 0 <= y < 20:
                grid[y][x] = f"{C.PRESENT}●{C.RESET}"
                
        for row in grid:
            print(''.join(row))
            
        print(f"\n{C.DEMON}Perfect determinism: Same initial state = Same evolution{C.RESET}")
        
    def play(self):
        self.show_intro()
        self.init_universe()
        
        while True:
            self.show_universe()
            print(f"\n{C.SYSTEM}[SPACE]Next | [R]ewind | [P]redict | [Q]uit: {C.RESET}", end='')
            choice = input().strip().upper()
            
            if choice == 'Q':
                break
            elif choice == ' ':
                if self.tick < len(self.history) - 1:
                    self.tick += 1
                else:
                    state = self.step_universe(self.history[-1])
                    self.history.append(state)
                    self.tick += 1
            elif choice == 'R':
                self.tick = 0
                print(f"\n{C.DEMON}Rewinding... Watch it unfold identically.{C.RESET}")
                time.sleep(1)
            elif choice == 'P':
                for _ in range(10):
                    if self.tick < len(self.history) - 1:
                        self.tick += 1
                    else:
                        state = self.step_universe(self.history[-1])
                        self.history.append(state)
                        self.tick += 1
                    self.show_universe()
                    time.sleep(0.3)
                    
        print(f"\n{C.DEMON}Determinism observed.{C.RESET}\n")

def main():
    try:
        game = LaplacesDemon()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.DEMON}Demon dismissed{C.RESET}\n")

if __name__ == "__main__":
    main()
