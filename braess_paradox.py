#!/usr/bin/env python3
"""
BRAESS'S PARADOX

Adding a road makes traffic worse.
More options = Worse outcomes.

Each driver makes the rational choice.
All drivers end up worse off.

Game theory meets traffic engineering.
"""

import os

class C:
    RESET, BOLD = '\033[0m', '\033[1m'
    ROAD = '\033[38;5;226m'
    TRAFFIC = '\033[38;5;203m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class BraessParadox:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def show_network(self, has_shortcut):
        if not has_shortcut:
            print(f"\n{C.ROAD}Network:{C.RESET}")
            print(f"  START → [A] → END (50 min)")
            print(f"  START → [B] → END (50 min)")
            print(f"\n{C.BOLD}Average time: 50 minutes{C.RESET}\n")
        else:
            print(f"\n{C.ROAD}Network with new road:{C.RESET}")
            print(f"  START → [A] → SHORTCUT → [B] → END")
            print(f"\n{C.TRAFFIC}Everyone uses shortcut!{C.RESET}")
            print(f"{C.BOLD}Average time: 80 minutes!{C.RESET}\n")
            
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'BRAESS\\'S PARADOX'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"{C.BOLD}Before: Two roads, balanced traffic{C.RESET}")
        self.show_network(False)
        
        input(f"{C.SYSTEM}[Press ENTER to add shortcut]{C.RESET}")
        
        print(f"\n{C.ROAD}City adds shortcut to reduce traffic...{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        self.clear_screen()
        print(f"\n{C.BOLD}After: Shortcut added{C.RESET}")
        self.show_network(True)
        
        print(f"{C.TRAFFIC}Adding a road made traffic WORSE!{C.RESET}\n")
        
        print(f"{C.BOLD}Why?{C.RESET}")
        print(f"- Each driver makes rational choice (use shortcut)")
        print(f"- Nash equilibrium shifts to worse outcome")
        print(f"- More options ≠ Better results\n")
        
        print(f"{C.DIM}Real examples:{C.RESET}")
        print(f"{C.DIM}- Seoul, South Korea (removed highway, traffic improved){C.RESET}")
        print(f"{C.DIM}- New York City (closed 42nd St, traffic improved){C.RESET}\n")

def main():
    game = BraessParadox()
    game.play()

if __name__ == "__main__":
    main()
