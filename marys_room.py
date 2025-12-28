#!/usr/bin/env python3
"""
MARY'S ROOM

Mary knows everything about color.
Every wavelength, every neural response, every physical fact.

But she's never seen color - she lives in a black and white room.

One day, she sees red for the first time.

Does she learn something new?
"""

import time


class MarysRoom:
    def clear_screen(self):
        clear_screen()
        
    def play(self):
        self.clear_screen()
        title = "MARY'S ROOM"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"{C.BW}You are Mary.{C.RESET}\n")
        print(f"{C.BW}You've lived your entire life in a black and white room.{C.RESET}")
        print(f"{C.BW}You've studied color your whole life.{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.BW}You know:{C.RESET}")
        print(f"{C.BW}- Red light: ~700nm wavelength{C.RESET}")
        print(f"{C.BW}- Activates L-cones in the retina{C.RESET}")
        print(f"{C.BW}- Neural signals to V4 visual cortex{C.RESET}")
        print(f"{C.BW}- Every physical fact about red{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        print(f"\n{C.BW}But you've never SEEN red.{C.RESET}\n")
        print(f"{C.BW}One day, you leave the room...{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER to see red]{C.RESET}")
        
        self.clear_screen()
        print(f"\n\n\n")
        print(f"{'█' * 70}".replace('█', f"{C.RED}█{C.RESET}"))
        print(f"{'█' * 70}".replace('█', f"{C.RED}█{C.RESET}"))
        print(f"{C.RED}{'THIS IS RED'.center(70)}{C.RESET}")
        print(f"{'█' * 70}".replace('█', f"{C.RED}█{C.RESET}"))
        print(f"{'█' * 70}".replace('█', f"{C.RED}█{C.RESET}"))
        print(f"\n\n")
        
        time.sleep(2)
        
        print(f"\n{C.BOLD}Did you learn something new?{C.RESET}\n")
        print(f"You knew all physical facts about red.")
        print(f"But experiencing red feels like NEW knowledge.\n")
        print(f"{C.DIM}This is QUALIA - subjective experience.{C.RESET}\n")
        print(f"Knowledge argument: Physical facts ≠ Experiential facts\n")

def main():
    game = MarysRoom()
    game.play()

if __name__ == "__main__":
    main()
