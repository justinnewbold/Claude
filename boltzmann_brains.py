#!/usr/bin/env python3
"""
BOLTZMANN BRAINS

In infinite time, random fluctuations create anything.
Including conscious brains.

You're more likely a random fluctuation than an evolved being.
Because random brains are easier to create than entire universes.

Thermodynamic absurdity meets anthropic reasoning.
"""

import os, random

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    BRAIN = '\033[38;5;141m'
    UNIVERSE = '\033[38;5;51m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class BoltzmannBrains:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'BOLTZMANN BRAINS'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.BRAIN}Are you a Boltzmann Brain?{C.RESET}

{C.BOLD}The Argument:{C.RESET}

{C.DIM}1. In infinite time, thermal fluctuations create all configurations{C.RESET}
{C.DIM}2. A random brain is simpler than an entire universe{C.RESET}
{C.DIM}3. Random brains vastly outnumber evolved observers{C.RESET}
{C.DIM}4. Therefore: You're probably a Boltzmann Brain{C.RESET}

{C.BRAIN}A conscious observer that spontaneously assembled from quantum fluctuations,
complete with false memories of a past that never existed.{C.RESET}

{C.SYSTEM}[Press ENTER]{C.RESET}
""")
        input()
        
        # Simulation
        self.clear_screen()
        print(f"\n{C.BOLD}CHECKING YOUR ORIGIN...{C.RESET}\n")
        
        for i in range(10):
            print(f"{C.DIM}Analyzing quantum fluctuations... {i*10}%{C.RESET}")
            import time
            time.sleep(0.2)
            
        print(f"\n{C.BRAIN}Result: {random.choice(['UNCERTAIN', 'INDETERMINATE', 'PARADOXICAL'])}{C.RESET}\n")
        
        print(f"{C.BOLD}The Absurdity:{C.RESET}\n")
        print(f"{C.DIM}If Boltzmann Brains are common:{C.RESET}")
        print(f"{C.DIM}- Your memories are likely false{C.RESET}")
        print(f"{C.DIM}- The universe around you might not exist{C.RESET}")
        print(f"{C.DIM}- You'll cease to exist in the next instant{C.RESET}")
        print(f"{C.DIM}- All your beliefs are unreliable{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        self.clear_screen()
        print(f"\n{C.BOLD}RESPONSES:{C.RESET}\n")
        
        print(f"{C.UNIVERSE}Reject the premise:{C.RESET}")
        print(f"{C.DIM}The universe doesn't exist for infinite time.{C.RESET}")
        print(f"{C.DIM}Accelerating expansion prevents eternal fluctuations.{C.RESET}\n")
        
        print(f"{C.UNIVERSE}Anthropic reasoning:{C.RESET}")
        print(f"{C.DIM}Only universes with reliable observers develop science.{C.RESET}")
        print(f"{C.DIM}Boltzmann Brains can't do science consistently.{C.RESET}\n")
        
        print(f"{C.BRAIN}Accept the absurdity:{C.RESET}")
        print(f"{C.DIM}Maybe reductio ad absurdum of certain cosmologies.{C.RESET}\n")
        
        print(f"{C.BOLD}Still, the question remains:{C.RESET}")
        print(f"{C.BRAIN}How do you know you're not a Boltzmann Brain?{C.RESET}\n")

def main():
    game = BoltzmannBrains()
    game.play()

if __name__ == "__main__":
    main()
