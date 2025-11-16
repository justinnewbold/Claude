#!/usr/bin/env python3
"""
THE SHIP OF THESEUS

Replace planks one by one.
At what point does it stop being the same ship?
If you rebuild the original from old planks, which is the real ship?

Identity through gradual change.
Persistence through replacement.

Based on Plutarch's ancient paradox.
"""

import os, random

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    SHIP = '\033[38;5;51m'
    OLD = '\033[38;5;203m'
    NEW = '\033[38;5;46m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class ShipOfTheseus:
    def __init__(self):
        self.original_planks = 100
        self.current_original = 100
        self.current_new = 0
        self.old_planks_pile = []
        self.rebuilt_ship_planks = 0
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def show_intro(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE SHIP OF THESEUS'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SHIP}The ship that carried Theseus has returned.{C.RESET}

{C.DIM}Over time, planks rot and are replaced.
One plank: Still the same ship.
Ten planks: Still the same ship.
Fifty planks: Still the same... ship?
All planks: Is it still the same ship?{C.RESET}

{C.BOLD}The paradox deepens:{C.RESET}

{C.DIM}Someone collects all the old planks.
They rebuild the original ship from original parts.{C.RESET}

{C.BOLD}Now there are TWO ships:{C.RESET}
{C.NEW}Ship A: All new planks, continuous existence{C.RESET}
{C.OLD}Ship B: All original planks, rebuilt{C.RESET}

{C.BOLD}Which is the real Ship of Theseus?{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
""")
        input()
        
    def show_ships(self):
        self.clear_screen()
        print(f"\n{C.SHIP}╔═ THE SHIP OF THESEUS ═╗{C.RESET}\n")
        
        # Main ship
        print(f"{C.BOLD}SHIP A (continuous existence):{C.RESET}")
        print(f"  {C.OLD}Original planks: {self.current_original}{C.RESET}")
        print(f"  {C.NEW}New planks: {self.current_new}{C.RESET}")
        print(f"  Total: {self.current_original + self.current_new}\n")
        
        # Pile of old planks
        print(f"{C.BOLD}PILE OF OLD PLANKS:{C.RESET}")
        print(f"  {C.OLD}Count: {len(self.old_planks_pile)}{C.RESET}\n")
        
        # Rebuilt ship
        if self.rebuilt_ship_planks > 0:
            print(f"{C.BOLD}SHIP B (rebuilt from originals):{C.RESET}")
            print(f"  {C.OLD}Original planks: {self.rebuilt_ship_planks}{C.RESET}\n")
            
        # Identity question
        pct = (self.current_new / (self.current_original + self.current_new)) * 100
        print(f"{C.SYSTEM}Ship A is {pct:.0f}% new planks{C.RESET}\n")
        
        if pct > 50:
            print(f"{C.DIM}More than half the ship has been replaced.{C.RESET}")
            print(f"{C.DIM}Is it still the Ship of Theseus?{C.RESET}\n")
            
    def replace_plank(self):
        if self.current_original > 0:
            self.current_original -= 1
            self.current_new += 1
            self.old_planks_pile.append("old_plank")
            return True
        return False
        
    def rebuild_from_old(self):
        if len(self.old_planks_pile) >= 10:
            for _ in range(10):
                self.old_planks_pile.pop()
                self.rebuilt_ship_planks += 1
            return True
        return False
        
    def play(self):
        self.show_intro()
        
        while self.current_original > 0 or len(self.old_planks_pile) > 0:
            self.show_ships()
            
            print(f"{C.SYSTEM}[R]eplace plank | [B]uild from old | [Q]uit: {C.RESET}", end='')
            choice = input().strip().upper()
            
            if choice == 'Q':
                break
            elif choice == 'R':
                if self.replace_plank():
                    print(f"\n{C.NEW}Replaced 1 old plank with new plank{C.RESET}")
                    input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
            elif choice == 'B':
                if self.rebuild_from_old():
                    print(f"\n{C.OLD}Added 10 original planks to Ship B{C.RESET}")
                    input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
                else:
                    print(f"\n{C.SYSTEM}Need at least 10 old planks{C.RESET}")
                    input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
                    
        # Final question
        self.clear_screen()
        print(f"\n{C.BOLD}FINAL STATE:{C.RESET}\n")
        print(f"{C.NEW}Ship A: 100% new planks, continuous existence{C.RESET}")
        print(f"{C.OLD}Ship B: {self.rebuilt_ship_planks} original planks, rebuilt{C.RESET}\n")
        
        print(f"{C.BOLD}Which is the real Ship of Theseus?{C.RESET}\n")
        print(f"[A] Ship A (continuous identity)")
        print(f"[B] Ship B (original materials)")
        print(f"[N] Neither")
        print(f"[C] Both\n")
        
        choice = input(f"{C.SYSTEM}Your answer: {C.RESET}").strip().upper()
        
        print(f"\n{C.BOLD}There is no right answer.{C.RESET}\n")
        print(f"{C.DIM}Philosophers debate this for 2000+ years.{C.RESET}")
        print(f"{C.DIM}Identity over time is not simple.{C.RESET}\n")

def main():
    game = ShipOfTheseus()
    game.play()

if __name__ == "__main__":
    main()
