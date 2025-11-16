#!/usr/bin/env python3
"""
THE SORITES PARADOX

1 grain of sand: Not a heap
Add 1 grain: Still not a heap
Add 1 grain: Still not a heap
...
Eventually: A heap!

When did it become a heap?
Vagueness breaks logic.
"""

import os

class C:
    RESET, BOLD = '\033[0m', '\033[1m'
    SAND = '\033[38;5;226m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class SoritesParadox:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE SORITES PARADOX'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SAND}Building a heap of sand...{C.RESET}

{C.BOLD}The Argument:{C.RESET}

{C.DIM}1. One grain of sand is not a heap{C.RESET}
{C.DIM}2. Adding one grain can't turn not-heap into heap{C.RESET}
{C.DIM}3. Therefore: No amount of grains makes a heap{C.RESET}

{C.BOLD}But we KNOW heaps exist!{C.RESET}

{C.SYSTEM}[Press ENTER to add grains]{C.RESET}
""")
        input()
        
        grains = 0
        while grains < 100:
            self.clear_screen()
            grains += 1
            
            print(f"\n{C.SAND}GRAINS: {grains}{C.RESET}\n")
            print(f"{C.SAND}{'●' * min(grains, 50)}{C.RESET}\n")
            
            if grains == 1:
                print(f"{C.DIM}Clearly not a heap.{C.RESET}\n")
            elif grains < 10:
                print(f"{C.DIM}Still not a heap.{C.RESET}\n")
            elif grains < 50:
                print(f"{C.DIM}Is this a heap? Hard to say...{C.RESET}\n")
            elif grains < 80:
                print(f"{C.DIM}Probably a heap?{C.RESET}\n")
            else:
                print(f"{C.BOLD}Definitely a heap!{C.RESET}\n")
                
            if grains % 10 == 0:
                print(f"Is this a heap? [Y]es/[N]o/[U]nsure: ", end='')
                response = input().strip().upper()
                
                if response == 'U':
                    print(f"\n{C.BOLD}Exactly! Vagueness makes it unclear.{C.RESET}\n")
                    input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
                    
        self.clear_screen()
        print(f"\n{C.BOLD}THE PARADOX:{C.RESET}\n")
        
        print(f"{C.DIM}We can't identify exact transition point.{C.RESET}")
        print(f"{C.DIM}But clearly 1 grain ≠ heap, 10000 grains = heap.{C.RESET}\n")
        
        print(f"{C.BOLD}RESPONSES:{C.RESET}\n")
        print(f"{C.DIM}1. Reject vagueness (supervaluationism){C.RESET}")
        print(f"{C.DIM}2. Accept degrees of truth (fuzzy logic){C.RESET}")
        print(f"{C.DIM}3. Context-dependent (epistemicism){C.RESET}\n")
        
        print(f"{C.BOLD}Other vague predicates:{C.RESET}")
        print(f"{C.DIM}- When does tall become short?{C.RESET}")
        print(f"{C.DIM}- When does red become orange?{C.RESET}")
        print(f"{C.DIM}- When does child become adult?{C.RESET}\n")

def main():
    game = SoritesParadox()
    game.play()

if __name__ == "__main__":
    main()
