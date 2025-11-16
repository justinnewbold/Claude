#!/usr/bin/env python3
"""
THE HALTING PROBLEM

Can you predict if a program will halt?
Can you build a perfect oracle?
What happens when the program asks about itself?

Some questions have no answers.
Some problems cannot be solved.
This is the limit of computation.

Based on Alan Turing's proof (1936):
The Halting Problem is undecidable.
No algorithm can determine, for all programs,
whether they will halt or loop forever.
"""

import os, random, time
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from enum import Enum

class C:
    RESET, BOLD, DIM = '\033[0m', '\033[1m', '\033[2m'
    HALT = '\033[38;5;46m'
    LOOP = '\033[38;5;203m'
    ORACLE = '\033[38;5;141m'
    CODE = '\033[38;5;87m'
    PARADOX = '\033[38;5;201m'
    HEADER = '\033[38;5;87m'
    SYSTEM = '\033[38;5;243m'
    SUCCESS = '\033[38;5;46m'
    ERROR = '\033[38;5;203m'
    WARNING = '\033[38;5;214m'

class Prediction(Enum):
    HALTS = "halts"
    LOOPS = "loops"
    UNKNOWN = "unknown"

@dataclass
class Program:
    name: str
    code: str
    description: str
    actual_behavior: Prediction
    complexity: int
    is_self_referential: bool = False
    
@dataclass
class AnalysisResult:
    correct: bool
    explanation: str

class HaltingProblem:
    def __init__(self):
        self.level = 1
        self.correct_predictions = 0
        self.total_predictions = 0
        self.oracle_confidence = 100
        self.paradox_encountered = False
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def show_intro(self):
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE HALTING PROBLEM'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.ORACLE}\"Can we predict if any program will halt?\"{C.RESET}

{C.DIM}In 1936, Alan Turing proved something shocking:
There is NO algorithm that can determine, for ALL programs,
whether they will halt (finish) or loop forever.

This is not a matter of being clever enough.
It is IMPOSSIBLE. Provably. Fundamentally.{C.RESET}

{C.BOLD}The Proof (simplified):{C.RESET}

1. Assume we have a perfect halting detector: {C.ORACLE}ORACLE(program){C.RESET}
   • Returns TRUE if program halts
   • Returns FALSE if program loops forever

2. Now create this program:
{C.CODE}
   def PARADOX():
       if ORACLE(PARADOX) == TRUE:
           loop_forever()
       else:
           return
{C.RESET}

3. Ask: Does {C.PARADOX}PARADOX(){C.RESET} halt?
   • If ORACLE says "halts" → PARADOX loops forever
   • If ORACLE says "loops" → PARADOX halts
   {C.BOLD}Contradiction!{C.RESET}

4. Therefore: No perfect ORACLE can exist.

{C.BOLD}Your mission:{C.RESET}
• Analyze programs to predict if they halt or loop
• Start with simple programs
• Progress to complex, self-referential ones
• Encounter the fundamental limit of computation

{C.BOLD}Controls:{C.RESET}
H - Predict program HALTS
L - Predict program LOOPS
Q - Quit

{C.WARNING}Warning: You will encounter programs you cannot decide.
This is not failure. This is the nature of computation.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
""")
        input()
        
    def create_program(self, level: int) -> Program:
        """Generate programs of increasing complexity"""
        
        if level == 1:
            return Program(
                name="simple_counter",
                code="""def simple_counter():
    i = 0
    while i < 10:
        i = i + 1
    return i""",
                description="Counts from 0 to 10",
                actual_behavior=Prediction.HALTS,
                complexity=1
            )
            
        elif level == 2:
            return Program(
                name="infinite_loop",
                code="""def infinite_loop():
    while True:
        pass""",
                description="Simple infinite loop",
                actual_behavior=Prediction.LOOPS,
                complexity=1
            )
            
        elif level == 3:
            return Program(
                name="conditional_halt",
                code="""def conditional_halt(n):
    while n > 0:
        n = n - 1
    return n""",
                description="Decrements until zero (input n=5)",
                actual_behavior=Prediction.HALTS,
                complexity=2
            )
            
        elif level == 4:
            return Program(
                name="collatz_conjecture",
                code="""def collatz(n):
    # n = 27
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    return n""",
                description="Collatz sequence (3n+1 problem) with n=27",
                actual_behavior=Prediction.HALTS,
                complexity=3
            )
            
        elif level == 5:
            return Program(
                name="unknown_halt",
                code="""def mystery():
    x = 3
    while x != 1:
        if is_prime(x):
            x = x * 2 + 1
        else:
            x = x - 2""",
                description="Complex number sequence - behavior unclear",
                actual_behavior=Prediction.UNKNOWN,
                complexity=4
            )
            
        elif level == 6:
            return Program(
                name="goldbach_search",
                code="""def goldbach_search():
    n = 4
    while True:
        # Search for even number that's NOT
        # sum of two primes (Goldbach's conjecture)
        if not can_sum_two_primes(n):
            return n  # Counterexample found!
        n = n + 2""",
                description="Searches for counterexample to Goldbach's conjecture",
                actual_behavior=Prediction.UNKNOWN,
                complexity=5
            )
            
        elif level == 7:
            return Program(
                name="self_checker",
                code="""def self_checker():
    # This program checks its own source code
    source = get_my_source_code()
    if contains_infinite_loop(source):
        return False
    else:
        while True:
            pass""",
                description="Checks if it contains infinite loop, then does opposite",
                actual_behavior=Prediction.UNKNOWN,
                complexity=5,
                is_self_referential=True
            )
            
        elif level == 8:
            # The ultimate paradox
            return Program(
                name="PARADOX",
                code="""def PARADOX():
    # This program asks YOU (the oracle)
    # if it will halt
    
    prediction = YOUR_PREDICTION()
    
    if prediction == "HALTS":
        # You said I halt, so I'll loop forever
        while True:
            pass
    else:
        # You said I loop, so I'll halt
        return True""",
                description="Asks you to predict itself, then does the opposite",
                actual_behavior=Prediction.UNKNOWN,
                complexity=10,
                is_self_referential=True
            )
            
        else:
            return None
            
    def show_program(self, program: Program):
        """Display the program for analysis"""
        self.clear_screen()
        
        print(f"\n{C.ORACLE}╔═ HALTING ORACLE - LEVEL {self.level} ═╗{C.RESET}")
        print(f"{C.SYSTEM}Oracle Confidence: {self.oracle_confidence}%{C.RESET}")
        print(f"{C.SYSTEM}Accuracy: {self.correct_predictions}/{self.total_predictions}{C.RESET}\n")
        
        print(f"{C.BOLD}PROGRAM: {C.CODE}{program.name}{C.RESET}")
        print(f"{C.DIM}Complexity: {'⚡' * program.complexity}{C.RESET}\n")
        
        if program.is_self_referential:
            print(f"{C.WARNING}⚠ WARNING: Self-referential program detected{C.RESET}\n")
            
        print(f"{C.CODE}{'─' * 60}{C.RESET}")
        for line in program.code.split('\n'):
            print(f"{C.CODE}{line}{C.RESET}")
        print(f"{C.CODE}{'─' * 60}{C.RESET}\n")
        
        print(f"{C.DIM}{program.description}{C.RESET}\n")
        
    def analyze_prediction(self, program: Program, prediction: Prediction) -> AnalysisResult:
        """Check if prediction is correct"""
        self.total_predictions += 1
        
        # Special case: unknowable programs
        if program.actual_behavior == Prediction.UNKNOWN:
            if program.is_self_referential and program.name == "PARADOX":
                # The ultimate paradox
                return AnalysisResult(
                    correct=False,
                    explanation=f"""{C.PARADOX}╔═══════════════════════════════════════════════════════════════╗
║                    PARADOX ENCOUNTERED                        ║
╚═══════════════════════════════════════════════════════════════╝{C.RESET}

{C.BOLD}You predicted: {prediction.value}{C.RESET}

But this program checks YOUR prediction and does the opposite!

{C.PARADOX}• If you say "HALTS" → it loops forever{C.RESET}
{C.PARADOX}• If you say "LOOPS" → it halts{C.RESET}

{C.BOLD}Your prediction is contradicted by the program's behavior.{C.RESET}

This is Turing's proof in action:
{C.DIM}No algorithm can correctly predict all programs.
The Halting Problem is UNDECIDABLE.{C.RESET}

{C.ORACLE}You've reached the fundamental limit of computation.{C.RESET}"""
                )
            else:
                # Genuinely unknowable (like Goldbach)
                return AnalysisResult(
                    correct=False,
                    explanation=f"""{C.WARNING}UNKNOWABLE{C.RESET}

You predicted: {prediction.value}

{C.BOLD}But this program's behavior depends on unsolved problems:{C.RESET}
{program.description}

{C.DIM}Whether it halts is tied to open mathematical conjectures.
We don't know if it halts, and may never know.{C.RESET}

{C.ORACLE}Some questions are beyond current mathematics.{C.RESET}"""
                )
                
        # Normal programs
        if prediction == program.actual_behavior:
            self.correct_predictions += 1
            return AnalysisResult(
                correct=True,
                explanation=f"""{C.SUCCESS}✓ CORRECT!{C.RESET}

The program {C.BOLD}{prediction.value}{C.RESET}.

{C.DIM}Your oracle successfully predicted this program's behavior.{C.RESET}"""
            )
        else:
            self.oracle_confidence = max(0, self.oracle_confidence - 10)
            return AnalysisResult(
                correct=False,
                explanation=f"""{C.ERROR}✗ INCORRECT{C.RESET}

You predicted: {prediction.value}
Actual behavior: {program.actual_behavior.value}

{C.DIM}Your oracle made a mistake. Confidence decreased.{C.RESET}"""
            )
            
    def show_ending(self):
        """Show final revelation"""
        self.clear_screen()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'COMPUTATIONAL LIMITS REACHED'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SUCCESS}You've encountered Turing's proof!{C.RESET}

{C.BOLD}What you learned:{C.RESET}

{C.ORACLE}1. The Halting Problem is Undecidable{C.RESET}
   No algorithm can determine, for ALL programs,
   whether they halt or loop forever.
   
   This is not a matter of being smart enough.
   It is IMPOSSIBLE. Fundamentally. Provably.

{C.ORACLE}2. Self-Reference Creates Paradoxes{C.RESET}
   When a program can reference itself and your prediction,
   it can construct contradictions.
   
   This is similar to:
   • "This statement is false" (liar's paradox)
   • Gödel's incompleteness theorems
   • Russell's paradox in set theory

{C.ORACLE}3. Limits of Computation{C.RESET}
   There are problems that:
   • Can be clearly stated
   • Have definite answers
   • But CANNOT be solved by any algorithm
   
   The Halting Problem is one of them.

{C.ORACLE}4. Rice's Theorem{C.RESET}
   ANY non-trivial property of programs is undecidable.
   • Does program compute prime numbers? Undecidable.
   • Does program ever print "hello"? Undecidable.
   • Does program run in polynomial time? Undecidable.

{C.DIM}Implications:{C.RESET}
• Perfect virus detection is impossible
• Perfect program verification is impossible
• Perfect bug detection is impossible
• Compilers cannot perfectly optimize all code

{C.PARADOX}Your Performance:{C.RESET}
Correct Predictions: {self.correct_predictions}/{self.total_predictions}
Final Confidence: {self.oracle_confidence}%

{C.DIM}You did well on simple programs.
But self-referential programs defeated you.
This is not your failure.
This is the nature of computation itself.{C.RESET}

{C.BOLD}Some problems have no solution.
Some questions have no answer.
Some computations cannot be computed.{C.RESET}

{C.ORACLE}This is the Halting Problem.
This is the limit of what can be known.{C.RESET}
""")
        
    def play(self):
        """Main game loop"""
        self.show_intro()
        
        while self.level <= 8:
            program = self.create_program(self.level)
            if program is None:
                break
                
            self.show_program(program)
            
            print(f"{C.SYSTEM}Will this program [H]alt or [L]oop? ([Q]uit): {C.RESET}", end='')
            choice = input().strip().upper()
            
            if choice == 'Q':
                break
            elif choice == 'H':
                prediction = Prediction.HALTS
            elif choice == 'L':
                prediction = Prediction.LOOPS
            else:
                continue
                
            result = self.analyze_prediction(program, prediction)
            
            self.clear_screen()
            print(f"\n{result.explanation}\n")
            
            if program.name == "PARADOX":
                self.paradox_encountered = True
                input(f"{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
                break
                
            if result.correct:
                self.level += 1
                
            input(f"{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
            
        self.show_ending()
        
        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE HALTING PROBLEM")
        print(f"Undecidable, unsolvable, unknowable")
        print(f"{'═' * 70}{C.RESET}\n")

def main():
    try:
        game = HaltingProblem()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.ORACLE}Oracle terminated{C.RESET}\n")

if __name__ == "__main__":
    main()
