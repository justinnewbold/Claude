#!/usr/bin/env python3
"""
PASCAL'S WAGER

Should you believe in God?

If God exists and you believe: Infinite reward
If God exists and you don't: Infinite punishment
If God doesn't exist: Finite difference

Expected value calculation favors belief.
But which God? Many gods problem.

Decision theory meets theology.
"""

import os

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    DIVINE = '\033[38;5;226m'
    MATH = '\033[38;5;51m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class PascalsWager:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'PASCAL\\'S WAGER'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.DIVINE}\"Bet on God's existence.\"{C.RESET}

{C.BOLD}PAYOFF MATRIX:{C.RESET}

{C.DIM}                 God EXISTS    God DOESN'T{C.RESET}
{C.DIM}  Believe        +∞            -small cost{C.RESET}
{C.DIM}  Don't Believe  -∞            +small benefit{C.RESET}

{C.MATH}Expected Value (Believe) = P(God) × ∞ + P(No God) × (-small){C.RESET}
{C.MATH}Even if P(God) is tiny, ∞ × tiny = ∞{C.RESET}

{C.BOLD}Conclusion: Always believe!{C.RESET}

{C.SYSTEM}[Press ENTER for objections]{C.RESET}
""")
        input()
        
        self.clear_screen()
        print(f"\n{C.BOLD}OBJECTIONS:{C.RESET}\n")
        
        print(f"{C.DIVINE}1. WHICH GOD?{C.RESET}")
        print(f"{C.DIM}   Thousands of religions, contradictory claims{C.RESET}")
        print(f"{C.DIM}   Believing in wrong god might be worse than none{C.RESET}\n")
        
        print(f"{C.DIVINE}2. CAN YOU CHOOSE TO BELIEVE?{C.RESET}")
        print(f"{C.DIM}   Belief isn't voluntary{C.RESET}")
        print(f"{C.DIM}   You can't just decide to believe{C.RESET}\n")
        
        print(f"{C.DIVINE}3. GOD KNOWS YOUR MOTIVES{C.RESET}")
        print(f"{C.DIM}   Strategic belief vs genuine faith{C.RESET}")
        print(f"{C.DIM}   Would God reward calculated belief?{C.RESET}\n")
        
        print(f"{C.DIVINE}4. INFINITE EXPECTED VALUES{C.RESET}")
        print(f"{C.DIM}   Many actions have infinite stakes{C.RESET}")
        print(f"{C.DIM}   Can't decide everything by infinity{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        self.clear_screen()
        print(f"\n{C.BOLD}THE MANY GODS PROBLEM:{C.RESET}\n")
        print(f"{C.DIVINE}Pascal assumes: Christian God or No God{C.RESET}\n")
        print(f"{C.DIM}But what if:{C.RESET}")
        print(f"{C.DIM}- Zeus punishes Christians?{C.RESET}")
        print(f"{C.DIM}- Allah rewards only Muslims?{C.RESET}")
        print(f"{C.DIM}- Flying Spaghetti Monster rewards skeptics?{C.RESET}\n")
        
        print(f"{C.BOLD}Infinite gods, infinite payoff matrices.{C.RESET}")
        print(f"{C.BOLD}Which bet maximizes expected value?{C.RESET}\n")
        
        print(f"{C.MATH}Decision theory breaks down with multiple infinities.{C.RESET}\n")

def main():
    game = PascalsWager()
    game.play()

if __name__ == "__main__":
    main()
