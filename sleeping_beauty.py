#!/usr/bin/env python3
"""
SLEEPING BEAUTY PROBLEM

Coin flipped. You're put to sleep.
If HEADS: Wake once on Monday.
If TAILS: Wake Monday, memory erased, wake Tuesday.

You wake up. What's the probability it was HEADS?

Self-locating belief puzzle.
"""

import os, random

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    HEADS = '\033[38;5;226m'
    TAILS = '\033[38;5;51m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class SleepingBeauty:
    def __init__(self):
        self.halfer_score = 0
        self.thirder_score = 0
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play_round(self):
        # Flip coin
        coin = random.choice(['HEADS', 'TAILS'])
        
        self.clear_screen()
        print(f"\n{C.BOLD}SLEEPING BEAUTY EXPERIMENT{C.RESET}\n")
        print(f"{C.DIM}Coin flipped (you don't see result).{C.RESET}")
        print(f"{C.DIM}You're put to sleep...{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        self.clear_screen()
        print(f"\n{C.BOLD}You wake up.{C.RESET}\n")
        print(f"{C.DIM}You don't know if it's Monday or Tuesday.{C.RESET}")
        print(f"{C.DIM}You don't remember if you've woken before.{C.RESET}\n")
        
        print(f"{C.BOLD}What's the probability the coin was HEADS?{C.RESET}\n")
        print(f"[1] 1/2 (Halfer position)")
        print(f"[2] 1/3 (Thirder position)\n")
        
        choice = input(f"{C.SYSTEM}Your answer: {C.RESET}").strip()
        
        # Reveal
        self.clear_screen()
        print(f"\n{C.BOLD}COIN RESULT: {coin}{C.RESET}\n")
        
        if coin == 'HEADS':
            print(f"{C.DIM}It's Monday. This is your only waking.{C.RESET}\n")
        else:
            day = random.choice(['Monday', 'Tuesday'])
            print(f"{C.DIM}It's {day}.{C.RESET}")
            if day == 'Tuesday':
                print(f"{C.DIM}You woke yesterday too (but memory erased).{C.RESET}\n")
            else:
                print(f"{C.DIM}You'll wake tomorrow too (but memory will be erased).{C.RESET}\n")
                
        # Score
        print(f"{C.BOLD}ARGUMENTS:{C.RESET}\n")
        print(f"{C.HEADS}Halfers (1/2):{C.RESET}")
        print(f"{C.DIM}  Coin flip is 50/50. No new info changes that.{C.RESET}\n")
        
        print(f"{C.TAILS}Thirders (1/3):{C.RESET}")
        print(f"{C.DIM}  3 equally likely scenarios:{C.RESET}")
        print(f"{C.DIM}    Heads-Monday, Tails-Monday, Tails-Tuesday{C.RESET}")
        print(f"{C.DIM}  Only 1/3 are Heads.{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE SLEEPING BEAUTY PROBLEM'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.BOLD}A probability puzzle with no consensus answer.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
""")
        input()
        
        for _ in range(3):
            self.play_round()
            
        self.clear_screen()
        print(f"\n{C.BOLD}Still debated among philosophers!{C.RESET}\n")
        print(f"{C.DIM}Halfers and Thirders both have valid arguments.{C.RESET}")
        print(f"{C.DIM}Self-locating belief is tricky.{C.RESET}\n")

def main():
    game = SleepingBeauty()
    game.play()

if __name__ == "__main__":
    main()
