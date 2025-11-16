#!/usr/bin/env python3
"""
THE TWIN PARADOX

One twin stays on Earth.
One twin travels at near light-speed.
Time dilation: Traveling twin ages slower.

Both see the other's clock moving slow.
Who is actually younger when they reunite?

Special relativity puzzle.
"""

import os, time

class C:
    RESET, BOLD = '\033[0m', '\033[1m'
    EARTH = '\033[38;5;46m'
    SPACE = '\033[38;5;141m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class TwinParadox:
    def __init__(self):
        self.earth_age = 20
        self.space_age = 20
        self.years_traveled = 0
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE TWIN PARADOX'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.BOLD}Two twins, age 20.{C.RESET}

{C.EARTH}Alice stays on Earth.{C.RESET}
{C.SPACE}Bob travels at 0.9c (90% light speed).{C.RESET}

{C.BOLD}Time dilation formula:{C.RESET}
t' = t / √(1 - v²/c²)

At v=0.9c: Time passes 2.29x slower for Bob.

{C.SYSTEM}[Press ENTER]{C.RESET}
""")
        input()
        
        # Simulate journey
        for year in range(1, 11):
            self.clear_screen()
            print(f"\n{C.BOLD}YEAR {year}{C.RESET}\n")
            
            self.earth_age += 1
            self.space_age += 1 / 2.29  # Time dilation
            
            print(f"{C.EARTH}Alice (Earth): {self.earth_age:.1f} years old{C.RESET}")
            print(f"{C.SPACE}Bob (Spaceship): {self.space_age:.1f} years old{C.RESET}\n")
            
            time.sleep(0.5)
            
        # Reunion
        print(f"\n{C.BOLD}Bob returns to Earth!{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        self.clear_screen()
        print(f"\n{C.BOLD}REUNION:{C.RESET}\n")
        print(f"{C.EARTH}Alice: {self.earth_age:.1f} years old{C.RESET}")
        print(f"{C.SPACE}Bob: {self.space_age:.1f} years old{C.RESET}\n")
        
        print(f"{C.BOLD}Bob is younger!{C.RESET}\n")
        print(f"{C.BOLD}The Paradox:{C.RESET}")
        print(f"{C.DIM}From Bob's perspective, Alice's clock moved slow.{C.RESET}")
        print(f"{C.DIM}From Alice's perspective, Bob's clock moved slow.{C.RESET}")
        print(f"{C.DIM}How can both be true?{C.RESET}\n")
        
        print(f"{C.BOLD}Resolution:{C.RESET}")
        print(f"{C.DIM}Bob ACCELERATED (changed reference frames).{C.RESET}")
        print(f"{C.DIM}Asymmetry breaks the symmetry.{C.RESET}")
        print(f"{C.DIM}Special relativity requires Bob ages less.{C.RESET}\n")

def main():
    game = TwinParadox()
    game.play()

if __name__ == "__main__":
    main()
