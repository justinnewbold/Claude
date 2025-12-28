#!/usr/bin/env python3
"""
PLATO'S CAVE

Prisoners see only shadows on wall.
One escapes, sees true reality.
Returns to tell others.

They don't believe him.
"""

import time


class PlatosCave:
    def clear_screen(self):
        clear_screen()
        
    def play(self):
        self.clear_screen()
        title = "PLATO'S CAVE"
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{title.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SHADOW}You are chained in a cave.{C.RESET}

{C.DIM}You've been here your whole life.
You face the wall.
Behind you: a fire.
Between fire and you: people carrying objects.

You see only shadows on the wall.
You think shadows ARE reality.{C.RESET}

{C.SYSTEM}[Press ENTER]{C.RESET}
""")
        input()
        
        # Show shadows
        for i in range(3):
            self.clear_screen()
            print(f"\n{C.SHADOW}SHADOWS ON THE WALL:{C.RESET}\n")
            print(f"{C.SHADOW}     🚶  🐕  🌳{C.RESET}\n")
            time.sleep(0.8)
            
        print(f"{C.DIM}This is all you've ever known.{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Escape
        self.clear_screen()
        print(f"\n{C.LIGHT}Your chains break...{C.RESET}\n")
        time.sleep(1)
        
        print(f"{C.LIGHT}You turn around.{C.RESET}\n")
        time.sleep(1)
        
        print(f"{C.LIGHT}The fire blinds you at first.{C.RESET}\n")
        time.sleep(1)
        
        print(f"{C.LIGHT}You see: Objects casting the shadows.{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Exit cave
        self.clear_screen()
        print(f"\n{C.LIGHT}You find the cave exit...{C.RESET}\n")
        time.sleep(1)
        
        print(f"{C.LIGHT}SUNLIGHT!{C.RESET}\n")
        time.sleep(1)
        
        print(f"{C.BOLD}TRUE REALITY:{C.RESET}")
        print(f"{C.LIGHT}🌞 🌳 🏔️  🌊{C.RESET}\n")
        
        print(f"{C.DIM}Real objects. Real light. Not shadows.{C.RESET}\n")
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Return
        self.clear_screen()
        print(f"\n{C.BOLD}You return to the cave...{C.RESET}\n")
        
        print(f'{C.SHADOW}"I saw true reality! Sunlight! Real objects!"{C.RESET}\n')
        
        print(f"{C.DIM}Other prisoners:{C.RESET}")
        crazy = "You're crazy. Shadows are all that exist."
        nonsense = "Don't speak of this nonsense."
        print(f'{C.SHADOW}"{crazy}"{C.RESET}')
        print(f'{C.SHADOW}"Your eyes were damaged. You see illusions."{C.RESET}')
        print(f'{C.SHADOW}"{nonsense}"{C.RESET}\n')
        
        print(f"{C.BOLD}They don't believe you.{C.RESET}\n")
        
        print(f"{C.DIM}The Allegory:{C.RESET}")
        print(f"{C.DIM}- Cave = World of appearances{C.RESET}")
        print(f"{C.DIM}- Shadows = Sensory experience{C.RESET}")
        print(f"{C.DIM}- Sunlight = True knowledge/Forms{C.RESET}")
        print(f"{C.DIM}- Escape = Philosophical enlightenment{C.RESET}\n")

def main():
    game = PlatosCave()
    game.play()

if __name__ == "__main__":
    main()
