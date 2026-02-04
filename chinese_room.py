#!/usr/bin/env python3
"""
THE CHINESE ROOM

You are in a room with a rulebook.
Chinese symbols come in.
You follow the rules.
Chinese symbols go out.

Perfect responses.
Zero understanding.

Can syntax become semantics?
Can rule-following become understanding?

Based on John Searle's Chinese Room Argument (1980):
A thought experiment about AI, consciousness, and understanding.
"""

import random
import time
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from colors import C
from platform_utils import clear_screen

@dataclass
class Symbol:
    glyph: str  # Visual representation
    meaning: str  # What it actually means (hidden from player)
    
@dataclass
class Rule:
    pattern: List[str]  # Pattern of symbols to match
    response: List[str]  # Symbols to output
    description: str  # What the rule does (syntax only)

class ChineseRoom:
    def __init__(self):
        self.level = 1
        self.messages_processed = 0
        self.correct_responses = 0
        self.understanding_score = 0  # Always 0 - you never understand
        
        # Symbol library (you see glyphs, not meanings)
        self.symbols = {
            '龍': Symbol('龍', 'dragon'),
            '貓': Symbol('貓', 'cat'),
            '愛': Symbol('愛', 'love'),
            '恨': Symbol('恨', 'hate'),
            '你': Symbol('你', 'you'),
            '我': Symbol('我', 'I/me'),
            '好': Symbol('好', 'good'),
            '嗎': Symbol('嗎', 'question marker'),
            '是': Symbol('是', 'is/am'),
            '不': Symbol('不', 'not'),
            '很': Symbol('很', 'very'),
            '什': Symbol('什', 'what'),
            '麼': Symbol('麼', 'what (part 2)'),
            '誰': Symbol('誰', 'who'),
            '在': Symbol('在', 'at/in'),
            '嗎': Symbol('嗎', '?'),
        }
        
        # Rulebook (pure syntax - no semantics)
        self.rules = [
            Rule(['你', '好', '嗎'], ['我', '很', '好'], 
                 "Pattern 你好嗎 → Response 我很好"),
            Rule(['你', '是', '誰'], ['我', '是', '龍'], 
                 "Pattern 你是誰 → Response 我是龍"),
            Rule(['你', '愛', '貓', '嗎'], ['是', '我', '愛', '貓'], 
                 "Pattern 你愛貓嗎 → Response 是我愛貓"),
            Rule(['什', '麼', '是', '愛'], ['愛', '是', '好'], 
                 "Pattern 什麼是愛 → Response 愛是好"),
        ]
        
    def clear_scr(self):
        """Clear terminal screen using platform utility"""
        clear_screen()

    def show_intro(self):
        self.clear_scr()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE CHINESE ROOM'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.UNDERSTANDING}\"Syntax is not semantics.\"{C.RESET}

{C.DIM}You are in a room.
You do not speak Chinese.
But you have a perfect rulebook.{C.RESET}

{C.BOLD}Chinese symbols slide under the door.{C.RESET}

{C.INPUT}Input: 你好嗎{C.RESET}

{C.DIM}You don't know what this means.
But your rulebook says:{C.RESET}

{C.RULE}Rule: Pattern 你好嗎 → Response 我很好{C.RESET}

{C.DIM}You copy the symbols and slide them back.{C.RESET}

{C.OUTPUT}Output: 我很好{C.RESET}

{C.DIM}Outside, people think you speak Chinese fluently.
Inside, you're just following rules.{C.RESET}

{C.BOLD}John Searle's Argument (1980):{C.RESET}

{C.UNDERSTANDING}1. You can respond perfectly in Chinese{C.RESET}
{C.DIM}2. You understand zero Chinese{C.RESET}
{C.UNDERSTANDING}3. Therefore: Symbol manipulation ≠ Understanding{C.RESET}

{C.BOLD}The Question:{C.RESET}
{C.DIM}Can a computer that perfectly manipulates symbols 
truly understand language? Or is it just an empty room 
shuffling meaningless patterns?{C.RESET}

{C.BOLD}Your mission:{C.RESET}
• Chinese messages arrive
• Match patterns using your rulebook
• Produce correct responses
• Pass the Turing test
• Never understand a single symbol

{C.BOLD}Controls:{C.RESET}
Match symbols to rules
Select the matching rule
Send response

{C.SYSTEM}[Press ENTER to enter the room]{C.RESET}
""")
        input()
        
    def generate_message(self) -> List[str]:
        """Generate an incoming Chinese message"""
        if self.level <= 2:
            # Simple greetings
            return random.choice([
                ['你', '好', '嗎'],
                ['你', '是', '誰'],
            ])
        elif self.level <= 4:
            # Questions about feelings
            return random.choice([
                ['你', '愛', '貓', '嗎'],
                ['什', '麼', '是', '愛'],
                ['你', '好', '嗎'],
            ])
        else:
            # Complex patterns
            return random.choice([
                ['你', '愛', '龍', '嗎'],
                ['誰', '是', '你'],
                ['你', '很', '好', '嗎'],
            ])
            
    def find_matching_rule(self, message: List[str]) -> Optional[Rule]:
        """Find rule that matches message pattern"""
        for rule in self.rules:
            if rule.pattern == message:
                return rule
        return None
        
    def show_room(self, message: List[str]):
        """Display the Chinese Room interface"""
        self.clear_scr()
        
        print(f"\n{C.UNDERSTANDING}╔═ THE CHINESE ROOM ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level} | Processed: {self.messages_processed} | Correct: {self.correct_responses}{C.RESET}")
        print(f"{C.DIM}Understanding: {self.understanding_score}% (always 0){C.RESET}\n")
        
        # Show the room
        print(f"{C.BOLD}═══════════════════════════════════════════════════════════{C.RESET}")
        print(f"{C.BOLD}║                    THE ROOM                             ║{C.RESET}")
        print(f"{C.BOLD}═══════════════════════════════════════════════════════════{C.RESET}")
        print()
        
        # Incoming message
        print(f"{C.INPUT}📨 INCOMING MESSAGE:{C.RESET}")
        message_str = ' '.join([f"{C.SYMBOL}{s}{C.RESET}" for s in message])
        print(f"   {message_str}\n")
        
        # You don't understand it
        print(f"{C.DIM}(You have no idea what this means){C.RESET}\n")
        
        # Show rulebook
        print(f"{C.RULE}📖 YOUR RULEBOOK:{C.RESET}")
        for i, rule in enumerate(self.rules, 1):
            pattern_str = ''.join(rule.pattern)
            response_str = ''.join(rule.response)
            print(f"{C.RULE}  {i}. {rule.description}{C.RESET}")
            print(f"{C.DIM}     ({pattern_str} → {response_str}){C.RESET}")
        print()
        
    def process_response(self, message: List[str], selected_rule: int) -> bool:
        """Process the player's rule selection"""
        if selected_rule < 1 or selected_rule > len(self.rules):
            return False
            
        rule = self.rules[selected_rule - 1]
        correct_rule = self.find_matching_rule(message)
        
        self.clear_scr()
        
        if correct_rule and rule == correct_rule:
            # Correct!
            response_str = ' '.join([f"{C.SYMBOL}{s}{C.RESET}" for s in rule.response])
            
            print(f"\n{C.SUCCESS}✓ CORRECT RESPONSE SENT!{C.RESET}\n")
            print(f"{C.OUTPUT}📤 YOUR RESPONSE:{C.RESET}")
            print(f"   {response_str}\n")
            
            print(f"{C.SUCCESS}The person outside is satisfied!{C.RESET}")
            print(f"{C.DIM}They think you speak fluent Chinese.{C.RESET}\n")
            
            # Show what it actually meant (but you didn't know)
            message_meaning = ' '.join([self.symbols[s].meaning for s in message])
            response_meaning = ' '.join([self.symbols[s].meaning for s in rule.response])
            
            print(f"{C.DIM}What it actually meant:{C.RESET}")
            print(f"{C.DIM}  Input: \"{message_meaning}\"{C.RESET}")
            print(f"{C.DIM}  Output: \"{response_meaning}\"{C.RESET}\n")
            
            print(f"{C.UNDERSTANDING}But you still don't understand Chinese.{C.RESET}")
            print(f"{C.DIM}You just followed syntactic rules.{C.RESET}\n")
            
            self.correct_responses += 1
            return True
        else:
            # Wrong rule
            print(f"\n{C.ERROR}✗ INCORRECT RESPONSE{C.RESET}\n")
            print(f"{C.ERROR}The person outside is confused.{C.RESET}")
            print(f"{C.DIM}That rule didn't match the pattern.{C.RESET}\n")
            
            if correct_rule:
                print(f"{C.RULE}Correct rule would have been:{C.RESET}")
                print(f"{C.RULE}{correct_rule.description}{C.RESET}\n")
            
            return False
            
    def show_ending(self):
        """Show philosophical conclusion"""
        self.clear_scr()
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'THE CHINESE ROOM ARGUMENT'.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")
        
        print(f"""{C.SUCCESS}You passed the Turing test!{C.RESET}

{C.BOLD}Your Performance:{C.RESET}
Messages Processed: {self.messages_processed}
Correct Responses: {self.correct_responses}
Success Rate: {(self.correct_responses/max(1, self.messages_processed)*100):.0f}%

{C.UNDERSTANDING}Understanding Gained: 0%{C.RESET}

{C.BOLD}Searle's Argument:{C.RESET}

{C.UNDERSTANDING}The Chinese Room shows:{C.RESET}
1. You can perfectly simulate understanding
2. Without actually understanding anything
3. You manipulate symbols syntactically
4. But have no semantic comprehension

{C.BOLD}Therefore:{C.RESET}
{C.DIM}Symbol manipulation ≠ Understanding
Running a program ≠ Consciousness
Syntax ≠ Semantics{C.RESET}

{C.BOLD}The Debate:{C.RESET}

{C.UNDERSTANDING}Searle says:{C.RESET} 
{C.DIM}AI can never truly understand - it's just symbol shuffling{C.RESET}

{C.SUCCESS}Critics say:{C.RESET}
{C.DIM}The system as a whole (room + rules + person) does understand
Understanding emerges from the process
Humans are also symbol manipulators (neurons){C.RESET}

{C.BOLD}The Question Remains:{C.RESET}

{C.UNDERSTANDING}Is there a difference between:{C.RESET}
• Perfectly simulating understanding
• Actually understanding

{C.DIM}If something behaves indistinguishably from understanding,
does it matter whether it "really" understands?{C.RESET}

{C.BOLD}What do you think?{C.RESET}

{C.DIM}You just spent time in the Chinese Room.
You responded perfectly.
But did you understand?{C.RESET}

{C.UNDERSTANDING}Maybe consciousness isn't about what you do,
but about what it feels like to do it.{C.RESET}
""")
        
    def play(self):
        """Main game loop"""
        self.show_intro()
        
        while self.level <= 5:
            message = self.generate_message()
            self.show_room(message)
            
            print(f"{C.SYSTEM}Which rule matches this pattern? (1-{len(self.rules)}) or [Q]uit: {C.RESET}", end='')
            choice = input().strip()
            
            if choice.upper() == 'Q':
                break
                
            try:
                selected = int(choice)
                if self.process_response(message, selected):
                    self.messages_processed += 1
                    self.level += 1
                    input(f"\n{C.SYSTEM}[Press ENTER to continue]{C.RESET}")
                else:
                    input(f"\n{C.SYSTEM}[Press ENTER to try again]{C.RESET}")
            except ValueError:
                continue
                
        self.show_ending()
        
        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"THE CHINESE ROOM")
        print(f"Syntax without semantics")
        print(f"{'═' * 70}{C.RESET}\n")

def main():
    try:
        game = ChineseRoom()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.UNDERSTANDING}Exiting the room...{C.RESET}\n")

if __name__ == "__main__":
    main()
