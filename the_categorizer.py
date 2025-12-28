#!/usr/bin/env python3
"""
THE CATEGORIZER

You create categories.
Categories create reality.

Is a hotdog a sandwich?
Is a tomato a fruit or vegetable?

Your categories determine what things ARE.
Ontology as a game mechanic.
"""

import random


class TheCategorizer:
    def __init__(self):
        self.categories = {}
        
    def clear_screen(self):
        clear_screen()
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE CATEGORIZER'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        items = [
            ("Hotdog", "Is it a sandwich?"),
            ("Tomato", "Fruit or vegetable?"),
            ("Pluto", "Planet or not?"),
            ("Virus", "Alive or not?"),
        ]
        
        for item, question in items:
            print(f"\n{C.ITEM}{item}{C.RESET}")
            print(f"{question}\n")
            
            cat = input(f"{C.CAT}Your category: {C.RESET}").strip()
            self.categories[item] = cat
            
            print(f"\n{C.CAT}You have declared: {item} is {cat}{C.RESET}")
            print(f"{C.BOLD}Your categories create reality.{C.RESET}\n")
            input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
            self.clear_screen()
            
        print(f"\n{C.BOLD}YOUR ONTOLOGY:{C.RESET}\n")
        for item, cat in self.categories.items():
            print(f"{C.ITEM}{item}{C.RESET} → {C.CAT}{cat}{C.RESET}")
            
        print(f"\n{C.BOLD}Categories are human constructs.{C.RESET}")
        print(f"{C.BOLD}But they shape how we see the world.{C.RESET}\n")

def main():
    game = TheCategorizer()
    game.play()

if __name__ == "__main__":
    main()
