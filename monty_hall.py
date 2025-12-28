#!/usr/bin/env python3
"""
THE MONTY HALL PROBLEM

3 doors. 1 car. 2 goats.
You pick door 1.
Host reveals goat behind door 3.

Switch to door 2, or stay with door 1?

Counter-intuitive probability.
Switching DOUBLES your odds.
"""

import random
from colors import C
from platform_utils import clear_screen


class MontyHall:
    def __init__(self):
        self.stay_wins = 0
        self.switch_wins = 0
        self.games_played = 0
        
    def clear_screen(self):
        clear_screen()
        
    def play_round(self):
        # Setup
        car_door = random.randint(1, 3)
        
        self.clear_screen()
        print(f"\n{C.DOOR}Three doors. Behind one: a car. Behind two: goats.{C.RESET}\n")
        print(f"{C.DOOR}[1] [2] [3]{C.RESET}\n")
        
        # Player choice
        player_choice = random.randint(1, 3)  # Simulate choosing door 1
        print(f"You choose door {player_choice}.\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Host reveals goat
        available = [d for d in [1,2,3] if d != player_choice and d != car_door]
        revealed = random.choice(available) if available else ([d for d in [1,2,3] if d != player_choice][0])
        
        print(f"\n{C.GOAT}Host opens door {revealed}... It's a GOAT!{C.RESET}\n")
        print(f"Remaining: Door {player_choice} (your choice) and Door {[d for d in [1,2,3] if d != player_choice and d != revealed][0]}\n")
        
        # Switch or stay?
        print(f"[S]tay with door {player_choice}")
        print(f"[W]itch to door {[d for d in [1,2,3] if d != player_choice and d != revealed][0]}\n")
        
        choice = input(f"{C.SYSTEM}Your choice: {C.RESET}").strip().upper()
        
        if choice == 'W':
            final_choice = [d for d in [1,2,3] if d != player_choice and d != revealed][0]
            strategy = "SWITCHED"
        else:
            final_choice = player_choice
            strategy = "STAYED"
            
        # Reveal
        self.clear_screen()
        print(f"\n{C.BOLD}You {strategy} to door {final_choice}...{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        if final_choice == car_door:
            print(f"\n{C.CAR}🚗 IT'S A CAR! YOU WIN!{C.RESET}\n")
            if choice == 'W':
                self.switch_wins += 1
            else:
                self.stay_wins += 1
        else:
            print(f"\n{C.GOAT}🐐 It's a goat. You lose.{C.RESET}\n")
            
        self.games_played += 1
        
        # Show statistics
        if self.games_played > 0:
            print(f"{C.BOLD}STATISTICS:{C.RESET}")
            print(f"  Stay wins: {self.stay_wins}")
            print(f"  Switch wins: {self.switch_wins}")
            print(f"  Games: {self.games_played}\n")
            
        input(f"{C.SYSTEM}[Press ENTER for next round]{C.RESET}")
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE MONTY HALL PROBLEM'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.BOLD}The counter-intuitive probability puzzle.{C.RESET}

{C.DIM}Initial odds: 1/3 for each door
After host reveals goat: Should you switch?{C.RESET}

{C.BOLD}Switching DOUBLES your odds from 1/3 to 2/3!{C.RESET}

{C.SYSTEM}[Press ENTER to play]{C.RESET}
""")
        input()
        
        for _ in range(5):
            self.play_round()
            
        # Final reveal
        self.clear_screen()
        print(f"\n{C.BOLD}THE MATHEMATICS:{C.RESET}\n")
        print(f"Staying: 1/3 chance (33%)")
        print(f"Switching: 2/3 chance (67%)\n")
        print(f"{C.BOLD}Switching is ALWAYS better!{C.RESET}\n")

def main():
    game = MontyHall()
    game.play()

if __name__ == "__main__":
    main()
