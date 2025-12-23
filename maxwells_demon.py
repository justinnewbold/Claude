#!/usr/bin/env python3
"""
MAXWELL'S DEMON

Information is not free.
Every observation has a cost.
Every memory must be erased.
And erasure requires energy.

This is why perpetual motion is impossible.

Based on Maxwell's Demon thought experiment (1867)
and Landauer's Principle (1961):
Erasing one bit of information dissipates at least kT ln(2) energy.
"""

import os, random, time, math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    HOT = '\033[38;5;196m'
    COLD = '\033[38;5;51m'
    PARTICLE = '\033[38;5;226m'
    DEMON = '\033[38;5;141m'
    INFO = '\033[38;5;87m'
    ENERGY = '\033[38;5;46m'
    ENTROPY = '\033[38;5;203m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    WARNING = '\033[38;5;214m'

@dataclass
class Particle:
    speed: float  # velocity magnitude
    position: int  # 0-9 for left chamber, 10-19 for right chamber
    direction: int  # 1 or -1
    
    @property
    def chamber(self) -> str:
        return 'left' if self.position < 10 else 'right'
        
    @property
    def is_fast(self) -> bool:
        return self.speed > 5.0

@dataclass
class MemoryBit:
    particle_id: int
    speed: float
    timestamp: int

class GameState(Enum):
    OBSERVING = "observing"
    SORTING = "sorting"
    ERASING = "erasing"
    COMPLETE = "complete"

class MaxwellsDemon:
    def __init__(self):
        self.particles: List[Particle] = []
        self.memory: List[MemoryBit] = []
        self.max_memory = 10  # Limited information storage
        
        self.door_open = False
        self.door_position = 9  # Between left (0-9) and right (10-19)
        
        self.energy_spent = 0.0
        self.information_gained = 0
        self.information_erased = 0
        
        self.tick = 0
        self.state = GameState.OBSERVING
        
        self.level = 1
        self.target_entropy_reduction = 2.0
        
        # Initialize particles
        self._spawn_particles()
        
    def _spawn_particles(self):
        """Create particles with random speeds distributed across chambers"""
        self.particles = []
        num_particles = 10 + (self.level * 2)
        
        for i in range(num_particles):
            speed = random.uniform(1.0, 10.0)
            position = random.randint(0, 19)
            direction = random.choice([1, -1])
            self.particles.append(Particle(speed, position, direction))
            
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def show_intro(self):
        self.clear_screen()
        title = "MAXWELL'S DEMON"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.DEMON}\"Can we violate the Second Law of Thermodynamics?\"{C.RESET}

{C.DIM}In 1867, James Clerk Maxwell proposed a thought experiment:

A demon guards a door between two chambers of gas.
The demon observes each molecule's speed.
Fast molecules → Hot chamber (right)
Slow molecules → Cold chamber (left)

Without doing work, entropy decreases.
A perpetual motion machine!{C.RESET}

{C.BOLD}But there's a catch...{C.RESET}

{C.INFO}In 1961, Rolf Landauer proved:{C.RESET}
{C.BOLD}Information erasure has an energy cost.{C.RESET}

{C.DIM}The demon's memory fills up with observations.
To continue, it must erase its memory.
Erasure dissipates energy: kT ln(2) per bit.
The energy cost exactly balances the entropy decrease.{C.RESET}

{C.ENTROPY}The Second Law of Thermodynamics is safe.{C.RESET}

{C.BOLD}Your mission:{C.RESET}
• Observe particles to measure their speed
• Sort fast particles to the right, slow to the left
• Manage your limited memory (information storage)
• Erase memory when full (costs energy!)
• Decrease entropy without running out of energy

{C.BOLD}Controls:{C.RESET}
O - Observe particle (uses memory)
D - Toggle door (open/close)
E - Erase memory (costs energy)
SPACE - Advance time
Q - Quit

{C.WARNING}Remember: Information is not free.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
""")
        input()
        
    def calculate_entropy(self) -> Tuple[float, float]:
        """Calculate entropy in each chamber (based on speed distribution)"""
        left_speeds = [p.speed for p in self.particles if p.chamber == 'left']
        right_speeds = [p.speed for p in self.particles if p.chamber == 'right']
        
        if not left_speeds or not right_speeds:
            return 0.0, 0.0
            
        # Simple entropy approximation: variance of speeds
        left_entropy = sum((s - sum(left_speeds)/len(left_speeds))**2 for s in left_speeds) / len(left_speeds)
        right_entropy = sum((s - sum(right_speeds)/len(right_speeds))**2 for s in right_speeds) / len(right_speeds)
        
        return left_entropy, right_entropy
        
    def calculate_total_entropy(self) -> float:
        """Total system entropy"""
        left, right = self.calculate_entropy()
        return left + right
        
    def calculate_temperature_diff(self) -> float:
        """Temperature difference between chambers (average speed)"""
        left_speeds = [p.speed for p in self.particles if p.chamber == 'left']
        right_speeds = [p.speed for p in self.particles if p.chamber == 'right']
        
        if not left_speeds or not right_speeds:
            return 0.0
            
        left_temp = sum(left_speeds) / len(left_speeds)
        right_temp = sum(right_speeds) / len(right_speeds)
        
        return right_temp - left_temp
        
    def update_particles(self):
        """Move particles, handle collisions with door"""
        for p in self.particles:
            new_pos = p.position + p.direction
            
            # Bounce off walls
            if new_pos < 0:
                new_pos = 0
                p.direction *= -1
            elif new_pos > 19:
                new_pos = 19
                p.direction *= -1
                
            # Check door at position 9/10
            if p.position < 10 and new_pos >= 10:  # Moving left to right
                if not self.door_open:
                    new_pos = 9
                    p.direction *= -1
            elif p.position >= 10 and new_pos < 10:  # Moving right to left
                if not self.door_open:
                    new_pos = 10
                    p.direction *= -1
                    
            p.position = new_pos
            
        self.tick += 1
        
    def observe_particle(self, particle_id: int) -> bool:
        """Observe a particle (costs memory)"""
        if len(self.memory) >= self.max_memory:
            return False
            
        if particle_id >= len(self.particles):
            return False
            
        particle = self.particles[particle_id]
        self.memory.append(MemoryBit(particle_id, particle.speed, self.tick))
        self.information_gained += 1
        
        return True
        
    def erase_memory(self) -> float:
        """Erase all memory (Landauer's principle: costs energy)"""
        if not self.memory:
            return 0.0
            
        # Landauer's limit: kT ln(2) per bit
        # Simplified: 1 energy unit per bit erased
        bits_erased = len(self.memory)
        energy_cost = bits_erased * 1.0
        
        self.memory.clear()
        self.energy_spent += energy_cost
        self.information_erased += bits_erased
        
        return energy_cost
        
    def render_chamber(self):
        """Visualize the two chambers"""
        print(f"\n{C.BOLD}CHAMBER:{C.RESET}")
        
        # Top wall
        print(f"  {C.COLD}{'━' * 12}{C.RESET}{'║' if not self.door_open else ' '}{C.HOT}{'━' * 12}{C.RESET}")
        
        # Particles
        left_chamber = [' '] * 10
        right_chamber = [' '] * 10
        
        for i, p in enumerate(self.particles):
            symbol = f"{C.PARTICLE}●{C.RESET}" if p.is_fast else f"{C.PARTICLE}○{C.RESET}"
            if p.position < 10:
                left_chamber[p.position] = symbol
            else:
                right_chamber[p.position - 10] = symbol
                
        # Render chambers
        for row in range(3):
            left_row = ''.join(left_chamber[row*3:(row+1)*3]) if row < 3 else ''.join(left_chamber[9:10])
            right_row = ''.join(right_chamber[row*3:(row+1)*3]) if row < 3 else ''.join(right_chamber[9:10])
            
            door_symbol = '║' if not self.door_open else ' '
            print(f"  {C.COLD}{left_row:^12}{C.RESET}{door_symbol}{C.HOT}{right_row:^12}{C.RESET}")
            
        # Bottom wall
        print(f"  {C.COLD}{'━' * 12}{C.RESET}{'║' if not self.door_open else ' '}{C.HOT}{'━' * 12}{C.RESET}")
        
        print(f"\n  {C.COLD}COLD (slow){C.RESET}  {'[CLOSED]' if not self.door_open else '[OPEN]':^5}  {C.HOT}HOT (fast){C.RESET}")
        
    def render_stats(self):
        """Show statistics"""
        temp_diff = self.calculate_temperature_diff()
        total_entropy = self.calculate_total_entropy()
        
        print(f"\n{C.BOLD}THERMODYNAMICS:{C.RESET}")
        print(f"  Temperature Δ: {C.HOT if temp_diff > 0 else C.COLD}{temp_diff:+.2f}{C.RESET}")
        print(f"  Total Entropy: {C.ENTROPY}{total_entropy:.2f}{C.RESET}")
        
        print(f"\n{C.BOLD}INFORMATION:{C.RESET}")
        print(f"  Memory: {C.INFO}{'█' * len(self.memory)}{'░' * (self.max_memory - len(self.memory))}{C.RESET} ({len(self.memory)}/{self.max_memory})")
        print(f"  Bits Gained: {C.INFO}{self.information_gained}{C.RESET}")
        print(f"  Bits Erased: {C.WARNING}{self.information_erased}{C.RESET}")
        
        print(f"\n{C.BOLD}ENERGY:{C.RESET}")
        print(f"  Energy Spent: {C.ENERGY}{self.energy_spent:.1f}{C.RESET}")
        
        # Show memory contents
        if self.memory:
            print(f"\n{C.BOLD}MEMORY BUFFER:{C.RESET}")
            for i, mem in enumerate(self.memory[-5:]):  # Show last 5
                speed_label = f"{C.HOT}FAST{C.RESET}" if mem.speed > 5.0 else f"{C.COLD}SLOW{C.RESET}"
                print(f"  {i}: Particle #{mem.particle_id} - {speed_label} ({mem.speed:.1f})")
                
    def render_particles_list(self):
        """Show list of particles for observation"""
        print(f"\n{C.BOLD}PARTICLES (for observation):{C.RESET}")
        
        for i, p in enumerate(self.particles[:8]):  # Show first 8
            chamber_label = f"{C.COLD}LEFT{C.RESET}" if p.chamber == 'left' else f"{C.HOT}RIGHT{C.RESET}"
            
            # Check if already observed
            observed = any(m.particle_id == i for m in self.memory)
            obs_marker = f"{C.INFO}[OBSERVED]{C.RESET}" if observed else ""
            
            print(f"  {i}: {chamber_label} {obs_marker}")
            
    def show_level_complete(self):
        """Show level completion"""
        self.clear_screen()
        temp_diff = self.calculate_temperature_diff()
        
        print(f"\n{C.SUCCESS}╔═══════════════════════════════════════╗{C.RESET}")
        print(f"{C.SUCCESS}║  LEVEL {self.level} COMPLETE!{' ' * 23}║{C.RESET}")
        print(f"{C.SUCCESS}╚═══════════════════════════════════════╝{C.RESET}\n")
        
        print(f"{C.BOLD}Results:{C.RESET}")
        print(f"  Temperature Difference: {C.HOT}{temp_diff:.2f}{C.RESET}")
        print(f"  Energy Spent: {C.ENERGY}{self.energy_spent:.1f}{C.RESET}")
        print(f"  Information Processed: {C.INFO}{self.information_erased}{C.RESET} bits\n")
        
        print(f"{C.DIM}Landauer's Principle validated:{C.RESET}")
        print(f"{C.DIM}Energy spent erasing information ≈ Entropy decrease{C.RESET}\n")
        
        print(f"{C.ENTROPY}The Second Law of Thermodynamics holds.{C.RESET}")
        print(f"{C.DIM}Information has a thermodynamic cost.{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER for next level]{C.RESET}")
        
    def show_ending(self):
        """Show final screen"""
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THERMODYNAMICS TRIUMPHANT'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SUCCESS}You've experienced Maxwell's revelation!{C.RESET}

{C.BOLD}What you learned:{C.RESET}

{C.INFO}1. Information is Physical{C.RESET}
   Memory, observation, knowledge - these are not abstract.
   They exist in physical systems and obey physical laws.

{C.INFO}2. Landauer's Principle (1961){C.RESET}
   Erasing one bit of information dissipates at least kT ln(2) energy.
   Information erasure is a thermodynamic process.

{C.INFO}3. Maxwell's Demon Paradox Resolved{C.RESET}
   The demon CAN decrease entropy by sorting particles.
   But its memory fills up with observations.
   Erasing memory to continue costs energy.
   The energy cost = entropy decrease.

{C.ENTROPY}4. Second Law of Thermodynamics is Safe{C.RESET}
   Entropy always increases in closed systems.
   Information processing doesn't violate this.
   Perpetual motion is impossible.

{C.DIM}Modern Applications:{C.RESET}
• Quantum computing (reversible computation to minimize erasure)
• Black hole thermodynamics (Bekenstein-Hawking entropy)
• Limits of computation (minimum energy per operation)
• Nanoscale engineering (thermodynamic costs matter)

{C.DEMON}You played as the demon and learned:{C.RESET}
{C.DIM}Every measurement has a cost.
Every memory must be erased.
Every erasure dissipates energy.
Information is not free.{C.RESET}

{C.BOLD}Total Energy Spent: {C.ENERGY}{self.energy_spent:.1f}{C.RESET}
{C.BOLD}Information Processed: {C.INFO}{self.information_erased}{C.RESET} {C.BOLD}bits{C.RESET}
""")
        
    def play_level(self):
        """Play one level"""
        initial_temp_diff = abs(self.calculate_temperature_diff())
        
        while True:
            self.clear_screen()
            
            print(f"\n{C.DEMON}╔═ MAXWELL'S DEMON - LEVEL {self.level} ═╗{C.RESET}")
            print(f"{C.SYSTEM}Goal: Create temperature difference > {self.target_entropy_reduction:.1f}{C.RESET}\n")
            
            self.render_chamber()
            self.render_stats()
            
            # Check win condition
            temp_diff = self.calculate_temperature_diff()
            if temp_diff >= self.target_entropy_reduction:
                self.show_level_complete()
                return True
                
            print(f"\n{C.SYSTEM}[O]bserve | [D]oor | [E]rase | [SPACE]Time | [Q]uit: {C.RESET}", end='')
            choice = input().strip().upper()
            
            if choice == 'Q':
                return False
            elif choice == 'O':
                self.render_particles_list()
                print(f"\n{C.SYSTEM}Enter particle ID to observe: {C.RESET}", end='')
                try:
                    pid = int(input().strip())
                    if self.observe_particle(pid):
                        print(f"{C.SUCCESS}✓ Particle observed{C.RESET}")
                    else:
                        print(f"{C.WARNING}Memory full! Erase memory first.{C.RESET}")
                    time.sleep(0.5)
                except ValueError:
                    pass
            elif choice == 'D':
                self.door_open = not self.door_open
            elif choice == 'E':
                cost = self.erase_memory()
                if cost > 0:
                    print(f"\n{C.WARNING}Erased memory. Energy cost: {cost:.1f}{C.RESET}")
                    time.sleep(0.8)
            elif choice == ' ':
                self.update_particles()
                
    def play(self):
        """Main game loop"""
        self.show_intro()
        
        while self.level <= 3:
            self._spawn_particles()
            
            if not self.play_level():
                print(f"\n{C.SYSTEM}Demon dismissed...{C.RESET}\n")
                return
                
            self.level += 1
            self.target_entropy_reduction += 1.0
            
        self.show_ending()
        
        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"MAXWELL'S DEMON")
        print(f"Information is not free")
        print(f"{'═' * 70}{C.RESET}\n")

def main():
    try:
        game = MaxwellsDemon()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.DEMON}Demon interrupted{C.RESET}\n")

if __name__ == "__main__":
    main()
