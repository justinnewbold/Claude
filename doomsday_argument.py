#!/usr/bin/env python3
"""
THE DOOMSDAY ARGUMENT

You are human #60,000,000,000.
How many humans will ever exist?

If you're typical, you're near the middle.
Therefore, only ~120 billion humans total.
Therefore, humanity ends soon.

Anthropic reasoning about the apocalypse.
"""

import os, random

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    DOOM = '\033[38;5;203m'
    HUMAN = '\033[38;5;226m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class DoomsdayArgument:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE DOOMSDAY ARGUMENT'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"{C.HUMAN}You are human #{random.randint(100000000000, 120000000000):,}{C.RESET}\n")
        
        print(f"Approximately {C.HUMAN}100 billion{C.RESET} humans have ever lived.")
        print(f"You are somewhere near the middle of humanity's history.\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.BOLD}The Argument:{C.RESET}\n")
        print(f"1. You're a random sample from all humans")
        print(f"2. If you're typical, you're near the median")
        print(f"3. Therefore, you're ~50% through human history")
        print(f"4. Therefore, ~100 billion more humans will exist")
        print(f"5. At current birth rates: {C.DOOM}~200 years left{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.DOOM}CONCLUSION: Humanity ends soon.{C.RESET}\n")
        
        print(f"{C.DIM}Counter-arguments:{C.RESET}")
        print(f"{C.DIM}- Self-sampling assumption may be wrong{C.RESET}")
        print(f"{C.DIM}- Future populations could be huge (trillions){C.RESET}")
        print(f"{C.DIM}- Selection effects matter{C.RESET}\n")
        
        print(f"{C.BOLD}But the probability remains...{C.RESET}\n")

def main():
    game = DoomsdayArgument()
    game.play()

if __name__ == "__main__":
    main()
