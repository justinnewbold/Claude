#!/usr/bin/env python3
"""
THE MÜNCHHAUSEN TRILEMMA

To justify a belief, you need another belief.
To justify THAT belief, you need another.

Three options:
1. Infinite regress (never end)
2. Circular reasoning (loop back)
3. Arbitrary stopping (unjustified foundation)

All three are problematic.
Can you justify anything?
"""

import os

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    REGRESS = '\033[38;5;203m'
    CIRCULAR = '\033[38;5;141m'
    FOUNDATIONAL = '\033[38;5;226m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'

class MunchhausenTrilemma:
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def play(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE MÜNCHHAUSEN TRILEMMA'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.BOLD}Can you justify your beliefs?{C.RESET}

{C.DIM}Claim: "The sky is blue"
Why? "Light scatters"
Why does light scatter? "Rayleigh scattering"
Why Rayleigh scattering? "Physics of photons"
Why trust physics? "Scientific method"
Why trust scientific method? ...{C.RESET}

{C.BOLD}Three options:{C.RESET}

{C.SYSTEM}[Press ENTER]{C.RESET}
""")
        input()
        
        # Option 1: Infinite regress
        self.clear_screen()
        print(f"\n{C.REGRESS}OPTION 1: INFINITE REGRESS{C.RESET}\n")
        
        for i in range(10):
            print(f"{C.DIM}Why? → Reason {i+1}{C.RESET}")
            print(f"{C.DIM}Why that? → Reason {i+2}{C.RESET}")
            
        print(f"{C.REGRESS}→ → → → → ∞{C.RESET}\n")
        
        print(f"{C.BOLD}Problem:{C.RESET}")
        print(f"{C.DIM}Never reach a foundation.{C.RESET}")
        print(f"{C.DIM}Infinite justifications are impossible.{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Option 2: Circular
        self.clear_screen()
        print(f"\n{C.CIRCULAR}OPTION 2: CIRCULAR REASONING{C.RESET}\n")
        
        print(f"{C.DIM}A is justified by B{C.RESET}")
        print(f"{C.DIM}B is justified by C{C.RESET}")
        print(f"{C.DIM}C is justified by A{C.RESET}\n")
        
        print(f"{C.CIRCULAR}A → B → C → A → B → C → ...{C.RESET}\n")
        
        print(f"{C.BOLD}Problem:{C.RESET}")
        print(f"{C.DIM}Begging the question.{C.RESET}")
        print(f"{C.DIM}No independent foundation.{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Option 3: Foundationalism
        self.clear_screen()
        print(f"\n{C.FOUNDATIONAL}OPTION 3: FOUNDATIONALISM{C.RESET}\n")
        
        print(f"{C.DIM}Claim A{C.RESET}")
        print(f"{C.DIM}  ↑ justified by{C.RESET}")
        print(f"{C.DIM}Claim B{C.RESET}")
        print(f"{C.DIM}  ↑ justified by{C.RESET}")
        print(f"{C.DIM}Claim C{C.RESET}")
        print(f"{C.DIM}  ↑ justified by{C.RESET}")
        print(f"{C.FOUNDATIONAL}AXIOM (not justified){C.RESET}\n")
        
        print(f"{C.BOLD}Problem:{C.RESET}")
        print(f"{C.DIM}Foundation is arbitrary.{C.RESET}")
        print(f"{C.DIM}Why accept axioms without justification?{C.RESET}\n")
        
        input(f"{C.SYSTEM}[Press ENTER]{C.RESET}")
        
        # Conclusion
        self.clear_screen()
        print(f"\n{C.BOLD}THE TRILEMMA:{C.RESET}\n")
        
        print(f"{C.REGRESS}1. Infinite Regress{C.RESET} - Never finishes")
        print(f"{C.CIRCULAR}2. Circular Reasoning{C.RESET} - Begs question")
        print(f"{C.FOUNDATIONAL}3. Foundationalism{C.RESET} - Arbitrary axioms\n")
        
        print(f"{C.BOLD}All three are problematic!{C.RESET}\n")
        
        print(f"{C.DIM}Responses:{C.RESET}")
        print(f"{C.DIM}- Accept foundationalism (most common){C.RESET}")
        print(f"{C.DIM}- Coherentism (web of beliefs, not chain){C.RESET}")
        print(f"{C.DIM}- Infinitism (infinite regress is okay){C.RESET}")
        print(f"{C.DIM}- Skepticism (nothing is justified){C.RESET}\n")
        
        print(f"{C.BOLD}How do YOU justify your beliefs?{C.RESET}\n")

def main():
    game = MunchhausenTrilemma()
    game.play()

if __name__ == "__main__":
    main()
