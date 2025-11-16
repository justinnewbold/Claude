#!/usr/bin/env python3
"""
THE SIMULATION HYPOTHESIS

If it's possible to simulate consciousness,
and civilizations create many simulations,
then most conscious beings are simulated.

Therefore: You're probably in a simulation.

Look for glitches. Find the limits. Wake up.
"""

import os, random, time

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    REAL = '\033[38;5;46m'
    SIM = '\033[38;5;141m'
    GLITCH = '\033[38;5;203m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class SimulationHypothesis:
    def __init__(self):
        self.glitches_found = 0
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def check_for_glitches(self):
        glitches = [
            ("Déjà vu detected", "Memory buffer overflow?"),
            ("Quantum randomness", "PRNG seed visible?"),
            ("Planck length limit", "Resolution limit of simulation?"),
            ("Speed of light constant", "Update rate cap?"),
            ("Observer effect in QM", "Optimization: only render when observed?"),
        ]
        
        glitch = random.choice(glitches)
        self.glitches_found += 1
        return glitch
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE SIMULATION HYPOTHESIS'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SIM}\"You're probably living in a simulation.\"{C.RESET}

{C.BOLD}The Argument (Nick Bostrom, 2003):{C.RESET}

{C.DIM}1. Either:{C.RESET}
{C.DIM}   a) Civilizations go extinct before creating simulations{C.RESET}
{C.DIM}   b) Advanced civs don't want to run simulations{C.RESET}
{C.DIM}   c) We're almost certainly in a simulation{C.RESET}

{C.DIM}2. If simulations are possible and common:{C.RESET}
{C.DIM}   Simulated beings >> Real beings{C.RESET}
{C.DIM}   Therefore: You're probably simulated{C.RESET}

{C.BOLD}Let's look for glitches...{C.RESET}

{C.SYSTEM}[Press ENTER to scan reality]{C.RESET}
""")
        input()
        
        for _ in range(5):
            self.clear_screen()
            print(f"\n{C.SIM}SCANNING REALITY...{C.RESET}\n")
            
            phenomenon, interpretation = self.check_for_glitches()
            
            print(f"{C.GLITCH}ANOMALY DETECTED:{C.RESET}")
            print(f"  {phenomenon}")
            print(f"  {C.DIM}{interpretation}{C.RESET}\n")
            
            time.sleep(1)
            input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
            
        self.clear_screen()
        print(f"\n{C.BOLD}GLITCHES FOUND: {self.glitches_found}{C.RESET}\n")
        
        print(f"{C.SIM}SIMULATION PROBABILITY: {random.randint(60, 99)}%{C.RESET}\n")
        
        print(f"{C.BOLD}IMPLICATIONS:{C.RESET}\n")
        print(f"{C.DIM}If you're in a simulation:{C.RESET}")
        print(f"{C.DIM}- Your universe may be a science experiment{C.RESET}")
        print(f"{C.DIM}- Laws of physics could change{C.RESET}")
        print(f"{C.DIM}- You could be shut down at any moment{C.RESET}")
        print(f"{C.DIM}- Simulators might be watching{C.RESET}\n")
        
        print(f"{C.BOLD}Can you prove you're NOT simulated?{C.RESET}\n")

def main():
    game = SimulationHypothesis()
    game.play()

if __name__ == "__main__":
    main()
