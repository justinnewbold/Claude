#!/usr/bin/env python3
"""
NEWCOMB'S PARADOX

The Predictor knows what you'll choose before you choose it.

Box A: $1,000 (visible)
Box B: $1,000,000 or $0 (depends on prediction)

Take both boxes? Take only B?

The Predictor is never wrong.
But you have free will... right?
"""

import os


class NewcombsParadox:
    def __init__(self):
        self.games_played = 0
        self.total_won = 0
        
    def clear_screen(self):
        clear_screen()
        
    def play_game(self):
        self.clear_screen()
        print(f"\n{C.PREDICT}THE PREDICTOR{C.RESET} has analyzed your brain state.\n")
        print(f"Two boxes before you:\n")
        print(f"{C.MONEY}Box A (transparent): $1,000{C.RESET}")
        print(f"{C.PREDICT}Box B (opaque): ??? {C.RESET}\n")
        
        print(f"Rules:")
        print(f"1. You can take both boxes, or only Box B")
        print(f"2. Box B contains $1M if Predictor thought you'd take only B")
        print(f"3. Box B is empty if Predictor thought you'd take both\n")
        print(f"{C.PREDICT}The Predictor is 99.9% accurate.{C.RESET}\n")
        
        print(f"[1] Take only Box B")
        print(f"[2] Take both boxes")
        choice = input(f"\n{C.SYSTEM}Choose: {C.RESET}").strip()
        
        self.clear_screen()
        
        # Predictor was right!
        if choice == "1":
            print(f"\n{C.MONEY}You take only Box B...{C.RESET}\n")
            print(f"{C.MONEY}$1,000,000!{C.RESET}\n")
            print(f"{C.PREDICT}The Predictor knew you'd choose this.{C.RESET}\n")
            self.total_won += 1000000
        else:
            print(f"\n{C.MONEY}You take both boxes...{C.RESET}\n")
            print(f"Box A: $1,000")
            print(f"Box B: $0\n")
            print(f"{C.PREDICT}The Predictor knew you'd be greedy.{C.RESET}\n")
            self.total_won += 1000
            
        self.games_played += 1
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
    def play(self):
        for _ in range(3):
            self.play_game()
            
        print(f"\n{C.BOLD}Total won: ${self.total_won:,}{C.RESET}\n")
        print(f"{C.PREDICT}The Predictor is always right.{C.RESET}")
        print(f"{C.DIM}But you had free will... didn't you?{C.RESET}\n")

def main():
    game = NewcombsParadox()
    game.play()

if __name__ == "__main__":
    main()
