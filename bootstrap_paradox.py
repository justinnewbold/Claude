#!/usr/bin/env python3
"""
BOOTSTRAP PARADOX

Information with no origin.
Objects with no creator.

You travel back in time with a book.
You give it to Shakespeare.
He publishes it.
Centuries later, you read it and travel back to give it to him.

Where did the book come from?
"""

import os

class C:
    RESET, BOLD = '\033[0m', '\033[1m'
    TIME = '\033[38;5;141m'
    OBJECT = '\033[38;5;226m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class BootstrapParadox:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'BOOTSTRAP PARADOX'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"{C.TIME}Year 2024:{C.RESET}")
        print(f"You find a mysterious book.\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.TIME}You travel to 1600...{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.TIME}Year 1600:{C.RESET}")
        print(f"You give the book to Shakespeare.")
        print(f"He publishes it under his name.\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.TIME}Back to 2024...{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.BOLD}Wait...{C.RESET}\n")
        print(f"{C.OBJECT}Where did the book originally come from?{C.RESET}\n")
        
        print(f"You got it from Shakespeare.")
        print(f"Shakespeare got it from you.")
        print(f"You got it from Shakespeare...")
        print(f"Shakespeare got it from you...\n")
        
        print(f"{C.BOLD}Infinite loop. No origin.{C.RESET}\n")
        print(f"{C.TIME}Information with no creator = Bootstrap Paradox{C.RESET}\n")

def main():
    game = BootstrapParadox()
    game.play()

if __name__ == "__main__":
    main()
