#!/usr/bin/env python3
"""
ZENO'S RUNNER

To reach the goal, you must first reach the halfway point.
To reach the halfway point, you must first reach the quarter point.
To reach the quarter point, you must first reach the eighth point.

Infinite steps to a finite goal.
Motion should be impossible.
Yet here you are, moving.

Based on Zeno of Elea's Paradoxes of Motion (5th century BCE):
The dichotomy paradox, Achilles and the tortoise, the arrow paradox.

How do you complete infinitely many tasks in finite time?
"""

import os, time, math
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    RUNNER = '\033[38;5;46m'
    GOAL = '\033[38;5;226m'
    STEP = '\033[38;5;51m'
    INFINITE = '\033[38;5;141m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    PARADOX = '\033[38;5;201m'

class ZenosRunner:
    def __init__(self):
        self.position = 0.0
        self.goal = 100.0
        self.steps_taken = 0
        self.distance_traveled = 0.0
        self.subdivision_level = 0
        self.level = 1
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def show_intro(self):
        self.clear_screen()
        title = "ZENO'S RUNNER"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.PARADOX}\"That which is in locomotion must arrive at the halfway 
stage before it arrives at the goal.\"{C.RESET}

{C.DIM}Zeno of Elea (5th century BCE) argued that motion is impossible.{C.RESET}

{C.BOLD}The Dichotomy Paradox:{C.RESET}

{C.INFINITE}To travel 100 meters, you must first travel 50 meters.{C.RESET}
{C.DIM}To travel 50 meters, you must first travel 25 meters.{C.RESET}
{C.INFINITE}To travel 25 meters, you must first travel 12.5 meters.{C.RESET}
{C.DIM}To travel 12.5 meters, you must first travel 6.25 meters...{C.RESET}

{C.PARADOX}Infinitely many steps to reach any goal.{C.RESET}
{C.BOLD}How can you complete infinitely many tasks in finite time?{C.RESET}

{C.BOLD}Achilles and the Tortoise:{C.RESET}

{C.DIM}Achilles races a tortoise with a head start.
By the time Achilles reaches where the tortoise was,
the tortoise has moved a bit further.
By the time Achilles reaches that new position,
the tortoise has moved again...{C.RESET}

{C.PARADOX}Achilles must complete infinitely many catches-up.
How can he ever overtake?{C.RESET}

{C.BOLD}The Arrow Paradox:{C.RESET}

{C.DIM}An arrow in flight:
At every instant, it occupies a space equal to itself.
At every instant, it is motionless.
If it's motionless at every instant, how does it move?{C.RESET}

{C.BOLD}Your Mission:{C.RESET}
• Reach the goal
• Navigate infinite subdivisions
• Complete infinitely many steps
• Resolve the paradox through action

{C.BOLD}Controls:{C.RESET}
M - Make a move (travel to next subdivision)
Z - Zoom into infinite detail
SPACE - Complete remaining distance instantly
Q - Quit

{C.INFINITE}Mathematics says: Infinite series can sum to finite values.
∑(1/2^n) = 1 (sum of 1/2 + 1/4 + 1/8 + ... = 1){C.RESET}

{C.SYSTEM}[Press ENTER to begin running]{C.RESET}
""")
        input()
        
    def show_track(self):
        """Visualize the infinite subdivision"""
        self.clear_screen()
        
        print(f"\n{C.INFINITE}╔═ ZENO'S PARADOX - LEVEL {self.level} ═╗{C.RESET}")
        print(f"{C.SYSTEM}Steps: {self.steps_taken} | Distance: {self.distance_traveled:.6f}/{self.goal}{C.RESET}\n")
        
        # Visual track
        track_width = 60
        runner_pos = int((self.position / self.goal) * track_width)
        
        # Show track
        print(f"{C.BOLD}START{C.RESET} " + "═" * track_width + f" {C.GOAL}GOAL{C.RESET}")
        
        # Runner position
        track = [' '] * track_width
        if runner_pos < track_width:
            track[runner_pos] = f"{C.RUNNER}►{C.RESET}"
        
        print("     " + ''.join(track))
        print("     " + "═" * track_width)
        
        # Remaining distance
        remaining = self.goal - self.position
        print(f"\n{C.BOLD}Remaining Distance: {C.INFINITE}{remaining:.10f}{C.RESET}")
        
        # Next step (always half of remaining)
        if remaining > 0.000001:
            next_step = remaining / 2.0
            print(f"{C.STEP}Next Step (half of remaining): {next_step:.10f}{C.RESET}")
            
            # Show the subdivision visually
            print(f"\n{C.DIM}Infinite subdivision:{C.RESET}")
            subdivision_display = []
            r = remaining
            for i in range(6):
                half = r / 2.0
                subdivision_display.append(f"  {r:.10f} → {half:.10f}")
                r = half
            for line in subdivision_display[:4]:
                print(f"{C.DIM}{line}...{C.RESET}")
            print(f"{C.INFINITE}  ∞ (continues forever){C.RESET}")
            
    def make_move(self):
        """Move half the remaining distance"""
        remaining = self.goal - self.position
        
        if remaining < 0.000001:  # Effectively at goal
            return False
            
        step = remaining / 2.0
        self.position += step
        self.distance_traveled += step
        self.steps_taken += 1
        self.subdivision_level += 1
        
        return True
        
    def complete_instantly(self):
        """Resolve the paradox - complete the infinite series"""
        remaining = self.goal - self.position
        
        if remaining < 0.000001:
            return
            
        self.clear_screen()
        print(f"\n{C.INFINITE}COMPLETING INFINITE SERIES...{C.RESET}\n")
        
        # Animate the infinite sum
        print(f"{C.DIM}Performing infinitely many steps in finite time:{C.RESET}\n")
        
        total = 0.0
        r = remaining
        for i in range(12):
            half = r / 2.0
            total += half
            r = half
            print(f"{C.STEP}Step {i+1}: +{half:.10f} (total: {self.position + total:.6f}){C.RESET}")
            time.sleep(0.1)
            
        print(f"\n{C.INFINITE}...")
        print(f"...")
        print(f"∞{C.RESET}\n")
        
        time.sleep(0.5)
        
        # Mathematical resolution
        print(f"{C.SUCCESS}INFINITE SERIES CONVERGES!{C.RESET}\n")
        print(f"{C.BOLD}∑(remaining/2^n) from n=1 to ∞ = remaining{C.RESET}\n")
        print(f"{C.DIM}The infinite series sums to a finite value.{C.RESET}")
        print(f"{C.DIM}You can complete infinitely many tasks in finite time.{C.RESET}\n")
        
        self.position = self.goal
        self.steps_taken += float('inf')  # Philosophically infinite steps
        
        time.sleep(2)
        
    def show_level_complete(self):
        """Show completion screen"""
        self.clear_screen()
        print(f"\n{C.SUCCESS}╔═══════════════════════════════════════╗{C.RESET}")
        print(f"{C.SUCCESS}║  GOAL REACHED!                        ║{C.RESET}")
        print(f"{C.SUCCESS}╚═══════════════════════════════════════╝{C.RESET}\n")
        
        print(f"{C.BOLD}Despite infinite subdivisions:{C.RESET}")
        print(f"  Steps Taken: {self.steps_taken}")
        print(f"  Distance Traveled: {self.distance_traveled:.10f}")
        print(f"  Final Position: {self.position:.10f}\n")
        
        print(f"{C.INFINITE}You completed infinitely many tasks.{C.RESET}")
        print(f"{C.DIM}Motion is possible after all.{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER for next level]{C.RESET}")
        
    def show_ending(self):
        """Show philosophical conclusion"""
        self.clear_screen()
        title = "ZENO'S PARADOXES RESOLVED"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SUCCESS}You've proven motion is possible!{C.RESET}

{C.BOLD}Zeno's Argument:{C.RESET}
{C.PARADOX}1. To move any distance, you must complete infinitely many steps{C.RESET}
{C.PARADOX}2. You cannot complete infinitely many tasks{C.RESET}
{C.PARADOX}3. Therefore, motion is impossible{C.RESET}

{C.BOLD}But clearly motion happens!{C.RESET}

{C.INFINITE}The Resolution (Calculus):{C.RESET}

{C.DIM}Infinite series can converge to finite sums.{C.RESET}

{C.BOLD}∑(1/2^n) from n=1 to ∞ = 1{C.RESET}

{C.DIM}1/2 + 1/4 + 1/8 + 1/16 + ... = 1{C.RESET}

{C.SUCCESS}You CAN complete infinitely many tasks in finite time!{C.RESET}

{C.BOLD}Modern Understanding:{C.RESET}

{C.INFINITE}Continuous Motion:{C.RESET}
{C.DIM}Zeno assumed motion is discrete (step by step).
Modern physics treats motion as continuous.
Calculus provides the mathematical tools.{C.RESET}

{C.INFINITE}Infinite Divisibility:{C.RESET}
{C.DIM}Space and time can be infinitely divided mathematically.
But quantum mechanics suggests physical limits (Planck length/time).{C.RESET}

{C.INFINITE}Supertasks:{C.RESET}
{C.DIM}Philosophy term for completing infinitely many tasks.
You just performed one!{C.RESET}

{C.BOLD}What Zeno Taught Us:{C.RESET}

{C.DIM}1. Infinity is counterintuitive{C.RESET}
{C.DIM}2. Our intuitions about infinite processes can be wrong{C.RESET}
{C.DIM}3. Mathematics lets us reason about infinity{C.RESET}
{C.DIM}4. The paradox spurred development of calculus{C.RESET}

{C.PARADOX}Zeno's paradoxes seemed absurd - obviously motion happens.{C.RESET}
{C.SUCCESS}But resolving them required 2000+ years and advanced mathematics.{C.RESET}

{C.INFINITE}Sometimes the obvious requires proof.{C.RESET}
""")
        
    def play(self):
        """Main game loop"""
        self.show_intro()
        
        while self.level <= 3:
            self.position = 0.0
            self.steps_taken = 0
            self.distance_traveled = 0.0
            self.goal = 100.0 * self.level
            
            while self.position < self.goal - 0.000001:
                self.show_track()
                
                print(f"\n{C.SYSTEM}[M]ove half distance | [SPACE]Complete instantly | [Q]uit: {C.RESET}", end='')
                choice = input().strip().upper()
                
                if choice == 'Q':
                    print(f"\n{C.SYSTEM}Abandoning the race...{C.RESET}\n")
                    return
                elif choice == 'M':
                    if not self.make_move():
                        break
                elif choice == ' ':
                    self.complete_instantly()
                    break
                    
            self.show_level_complete()
            self.level += 1
            
        self.show_ending()
        
        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"ZENO'S RUNNER")
        print(f"Infinite steps, finite distance")
        print(f"{'═' * 70}{C.RESET}\n")

def main():
    try:
        game = ZenosRunner()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.PARADOX}Motion interrupted{C.RESET}\n")

if __name__ == "__main__":
    main()
