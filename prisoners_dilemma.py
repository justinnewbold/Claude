#!/usr/bin/env python3
"""
THE PRISONER'S DILEMMA TOURNAMENT

You vs evolving AI strategies.
Cooperate or betray?
Trust or defect?

Watch strategies evolve through generations.
Tit-for-tat, always defect, forgiving, grudger...

Based on Robert Axelrod's tournaments (1980s).
What strategy survives?
"""

import random
from dataclasses import dataclass
from colors import C
from platform_utils import clear_screen
from enum import Enum


class Move(Enum):
    COOPERATE = "C"
    DEFECT = "D"

@dataclass
class Strategy:
    name: str
    score: int = 0
    
    def choose(self, history, opp_history):
        if self.name == "Always Cooperate":
            return Move.COOPERATE
        elif self.name == "Always Defect":
            return Move.DEFECT
        elif self.name == "Tit-for-Tat":
            return opp_history[-1] if opp_history else Move.COOPERATE
        elif self.name == "Grudger":
            return Move.DEFECT if Move.DEFECT in opp_history else Move.COOPERATE
        return Move.COOPERATE

class PrisonersDilemma:
    def __init__(self):
        self.strategies = [
            Strategy("Always Cooperate"),
            Strategy("Always Defect"),
            Strategy("Tit-for-Tat"),
            Strategy("Grudger"),
        ]
        
    def clear_screen(self):
        clear_screen()
        
    def payoff(self, m1, m2):
        """Payoff matrix"""
        if m1 == Move.COOPERATE and m2 == Move.COOPERATE:
            return (3, 3)
        elif m1 == Move.COOPERATE and m2 == Move.DEFECT:
            return (0, 5)
        elif m1 == Move.DEFECT and m2 == Move.COOPERATE:
            return (5, 0)
        else:
            return (1, 1)
            
    def show_intro(self):
        self.clear_screen()
        title = "THE PRISONER'S DILEMMA TOURNAMENT"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.BOLD}Two prisoners, separate cells.{C.RESET}

{C.COOP}COOPERATE{C.RESET} (stay silent): Both get 3 years
{C.DEFECT}DEFECT{C.RESET} (betray): You go free (0), partner gets 5 years

If both defect: Both get 1 year

{C.BOLD}Rational choice: Always defect{C.RESET}
{C.BOLD}Best outcome: Both cooperate{C.RESET}

{C.SYSTEM}[Press ENTER]{C.RESET}
""")
        input()
        
    def play(self):
        self.show_intro()
        
        for round in range(5):
            self.clear_screen()
            print(f"\n{C.BOLD}ROUND {round+1}{C.RESET}\n")
            
            # Tournament
            for s in self.strategies:
                opp = random.choice([x for x in self.strategies if x != s])
                m1 = s.choose([], [])
                m2 = opp.choose([], [])
                p1, p2 = self.payoff(m1, m2)
                s.score += p1
                
            # Show scores
            for s in sorted(self.strategies, key=lambda x: -x.score):
                print(f"{s.name}: {s.score}")
                
            input(f"\n{C.SYSTEM}[Press ENTER]{C.RESET}")
            
        print(f"\n{C.BOLD}Winner: {max(self.strategies, key=lambda x: x.score).name}{C.RESET}\n")

def main():
    game = PrisonersDilemma()
    game.play()

if __name__ == "__main__":
    main()
