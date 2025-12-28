#!/usr/bin/env python3
"""
SYNTAX TREE CLIMBER

Navigate the Abstract Syntax Tree of living code.
Modify nodes. Change logic. Become the parser.

In most games, you navigate physical space.
In this game, you navigate CONCEPTUAL space - the structure of code itself.

You are a cursor moving through an AST.
The code is both the game and the puzzle.
Modify it. Execute it. Watch reality change.

This is meta-programming as gameplay.
"""

import ast
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum

from platform_utils import clear_screen
from colors import C


class NodeType(Enum):
    """Types of AST nodes we care about"""
    MODULE = "Module"
    FUNCTION = "FunctionDef"
    CLASS = "ClassDef"
    IF = "If"
    WHILE = "While"
    FOR = "For"
    ASSIGN = "Assign"
    EXPR = "Expr"
    RETURN = "Return"
    BINOP = "BinOp"
    COMPARE = "Compare"
    CALL = "Call"
    NAME = "Name"
    CONSTANT = "Constant"
    OTHER = "Other"


@dataclass
class ASTPosition:
    """Current position in the AST"""
    node: ast.AST
    parent: Optional[ast.AST] = None
    field_name: Optional[str] = None
    index: Optional[int] = None


class SyntaxTreeClimber:
    def __init__(self):
        self.level = 1
        self.game_over = False
        self.victory = False

        # Current code and AST
        self.code: str = ""
        self.tree: Optional[ast.AST] = None
        self.position: Optional[ASTPosition] = None

        # Level state
        self.goal_output: Any = None
        self.modifications_made = 0
        self.max_modifications = 5

        self.setup_level(1)

    def clear_screen(self):
        clear_screen()

    def print_header(self, text):
        print(f"\n{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{text.center(70)}{C.RESET}")
        print(f"{C.BOLD}{C.HEADER}{'═' * 70}{C.RESET}\n")

    def setup_level(self, level_num: int):
        """Setup a specific level with code to navigate"""

        if level_num == 1:
            # Tutorial: Simple function, need to navigate to return value
            self.code = """def calculate():
    x = 5
    y = 3
    result = x + y
    return result
"""
            self.goal_output = 8
            self.max_modifications = 1

        elif level_num == 2:
            # Change operator to fix bug
            self.code = """def process_data():
    value = 10
    multiplier = 2
    result = value - multiplier
    return result
"""
            self.goal_output = 20
            self.max_modifications = 1

        elif level_num == 3:
            # Fix conditional logic
            self.code = """def check_value():
    x = 15
    if x < 10:
        return "small"
    else:
        return "large"
"""
            self.goal_output = "large"
            self.max_modifications = 1

        elif level_num == 4:
            # Multiple changes needed
            self.code = """def calculate_total():
    price = 100
    discount = 10
    tax = 5
    total = price - discount - tax
    return total
"""
            self.goal_output = 115
            self.max_modifications = 2

        elif level_num == 5:
            # Complex AST navigation
            self.code = """def complex_function():
    numbers = [1, 2, 3]
    total = 0
    for num in numbers:
        total = total + num
    return total
"""
            self.goal_output = 60
            self.max_modifications = 3

        else:
            # Victory!
            self.victory = True
            self.game_over = True
            return

        # Parse code into AST
        try:
            self.tree = ast.parse(self.code)
            # Start at the module root
            self.position = ASTPosition(node=self.tree)
            self.modifications_made = 0
        except SyntaxError as e:
            print(f"{C.ERROR}Failed to parse code: {e}{C.RESET}")

    def get_node_type(self, node: ast.AST) -> str:
        """Get readable node type"""
        return node.__class__.__name__

    def get_node_color(self, node: ast.AST) -> str:
        """Get color for node type"""
        node_type = self.get_node_type(node)

        if node_type in ['FunctionDef', 'AsyncFunctionDef', 'Lambda']:
            return C.FUNCTION
        elif node_type in ['ClassDef']:
            return C.CLASS
        elif node_type in ['If', 'While', 'For', 'Match']:
            return C.CONTROL
        elif node_type in ['Assign', 'AugAssign', 'AnnAssign']:
            return C.ASSIGN
        elif node_type in ['Constant', 'Num', 'Str']:
            return C.LITERAL
        else:
            return C.EXPR

    def get_node_description(self, node: ast.AST) -> str:
        """Get human-readable description of node"""
        node_type = self.get_node_type(node)

        if node_type == 'Module':
            return "Module (root)"
        elif node_type == 'FunctionDef':
            return f"Function: {node.name}"
        elif node_type == 'ClassDef':
            return f"Class: {node.name}"
        elif node_type == 'If':
            return "If statement"
        elif node_type == 'While':
            return "While loop"
        elif node_type == 'For':
            return "For loop"
        elif node_type == 'Assign':
            targets = ', '.join([self.node_to_string(t) for t in node.targets])
            value = self.node_to_string(node.value)
            return f"Assign: {targets} = {value}"
        elif node_type == 'Return':
            value = self.node_to_string(node.value) if node.value else "None"
            return f"Return: {value}"
        elif node_type == 'BinOp':
            left = self.node_to_string(node.left)
            op = self.op_to_string(node.op)
            right = self.node_to_string(node.right)
            return f"BinOp: {left} {op} {right}"
        elif node_type == 'Compare':
            return "Comparison"
        elif node_type == 'Name':
            return f"Variable: {node.id}"
        elif node_type == 'Constant':
            return f"Constant: {node.value}"
        else:
            return f"{node_type}"

    def node_to_string(self, node: ast.AST) -> str:
        """Convert AST node to string"""
        try:
            return ast.unparse(node)
        except (ValueError, TypeError, RecursionError):
            return f"<{self.get_node_type(node)}>"

    def op_to_string(self, op: ast.operator) -> str:
        """Convert operator to string"""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%',
            ast.Pow: '**',
        }
        return op_map.get(type(op), '?')

    def get_children(self, node: ast.AST) -> List[Tuple[str, Any, int]]:
        """Get all child nodes with field names"""
        children = []

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, ast.AST):
                        children.append((field, item, i))
            elif isinstance(value, ast.AST):
                children.append((field, value, None))

        return children

    def navigate_down(self) -> bool:
        """Navigate to first child"""
        if not self.position:
            return False

        children = self.get_children(self.position.node)
        if children:
            field_name, child_node, index = children[0]
            self.position = ASTPosition(
                node=child_node,
                parent=self.position.node,
                field_name=field_name,
                index=index
            )
            return True
        return False

    def navigate_up(self) -> bool:
        """Navigate to parent"""
        if not self.position or not self.position.parent:
            return False

        self.position = ASTPosition(
            node=self.position.parent,
            parent=None  # We'd need to track grandparent, simplified for now
        )
        return True

    def navigate_next(self) -> bool:
        """Navigate to next sibling"""
        if not self.position or not self.position.parent:
            return False

        parent_children = self.get_children(self.position.parent)

        # Find current position in parent's children
        for i, (field, child, index) in enumerate(parent_children):
            if child is self.position.node:
                # Move to next sibling if exists
                if i + 1 < len(parent_children):
                    field_name, next_node, next_index = parent_children[i + 1]
                    self.position = ASTPosition(
                        node=next_node,
                        parent=self.position.parent,
                        field_name=field_name,
                        index=next_index
                    )
                    return True
                break

        return False

    def navigate_prev(self) -> bool:
        """Navigate to previous sibling"""
        if not self.position or not self.position.parent:
            return False

        parent_children = self.get_children(self.position.parent)

        # Find current position in parent's children
        for i, (field, child, index) in enumerate(parent_children):
            if child is self.position.node:
                # Move to previous sibling if exists
                if i > 0:
                    field_name, prev_node, prev_index = parent_children[i - 1]
                    self.position = ASTPosition(
                        node=prev_node,
                        parent=self.position.parent,
                        field_name=field_name,
                        index=prev_index
                    )
                    return True
                break

        return False

    def modify_constant(self, new_value):
        """Modify a constant node"""
        if not self.position:
            return False

        node = self.position.node
        if isinstance(node, ast.Constant):
            # Try to convert new_value to appropriate type
            try:
                if isinstance(node.value, int):
                    node.value = int(new_value)
                elif isinstance(node.value, float):
                    node.value = float(new_value)
                elif isinstance(node.value, str):
                    node.value = str(new_value)
                else:
                    node.value = new_value

                self.modifications_made += 1
                # Recompile code
                self.code = ast.unparse(self.tree)
                return True
            except (ValueError, TypeError, RecursionError):
                return False

        return False

    def modify_operator(self, new_op: str):
        """Modify an operator in a BinOp"""
        if not self.position:
            return False

        node = self.position.node
        if isinstance(node, ast.BinOp):
            op_map = {
                '+': ast.Add(),
                '-': ast.Sub(),
                '*': ast.Mult(),
                '/': ast.Div(),
                '%': ast.Mod(),
                '**': ast.Pow(),
            }

            if new_op in op_map:
                node.op = op_map[new_op]
                self.modifications_made += 1
                self.code = ast.unparse(self.tree)
                return True

        return False

    def modify_comparison(self, new_cmp: str):
        """Modify a comparison operator"""
        if not self.position:
            return False

        node = self.position.node
        if isinstance(node, ast.Compare):
            cmp_map = {
                '<': ast.Lt(),
                '>': ast.Gt(),
                '<=': ast.LtE(),
                '>=': ast.GtE(),
                '==': ast.Eq(),
                '!=': ast.NotEq(),
            }

            if new_cmp in cmp_map and len(node.ops) > 0:
                node.ops[0] = cmp_map[new_cmp]
                self.modifications_made += 1
                self.code = ast.unparse(self.tree)
                return True

        return False

    def execute_code(self) -> Tuple[bool, Any]:
        """Execute the current code and get result"""
        try:
            # Create namespace for execution
            namespace = {}

            # Execute the code
            exec(self.code, namespace)

            # Find the main function (first FunctionDef)
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    if func_name in namespace:
                        result = namespace[func_name]()
                        return True, result

            return False, None
        except Exception as e:
            return False, str(e)

    def render_ast_tree(self, node: ast.AST, depth: int = 0, max_depth: int = 3):
        """Render AST as tree structure"""
        if depth > max_depth:
            return

        indent = "  " * depth
        is_current = node is self.position.node

        color = self.get_node_color(node)
        marker = f"{C.PLAYER}►{C.RESET}" if is_current else " "

        desc = self.get_node_description(node)
        print(f"{indent}{marker} {color}{desc}{C.RESET}")

        # Show children
        children = self.get_children(node)
        for field_name, child_node, index in children:
            self.render_ast_tree(child_node, depth + 1, max_depth)

    def show_game_screen(self):
        """Show main game interface"""
        self.clear_screen()
        print(f"\n{C.META}╔═ SYNTAX TREE CLIMBER ═╗{C.RESET}")
        print(f"{C.SYSTEM}Level {self.level} | Modifications: {self.modifications_made}/{self.max_modifications}{C.RESET}")
        print(f"{C.SYSTEM}Goal Output: {self.goal_output}{C.RESET}\n")

        # Show current code
        print(f"{C.BOLD}Current Code:{C.RESET}")
        for i, line in enumerate(self.code.split('\n'), 1):
            print(f"{C.CODE}{i:2} │ {line}{C.RESET}")

        print(f"\n{C.BOLD}AST Structure:{C.RESET}")
        self.render_ast_tree(self.tree, max_depth=4)

        print(f"\n{C.BOLD}Current Node:{C.RESET}")
        print(f"{C.SYSTEM}{self.get_node_description(self.position.node)}{C.RESET}")

        print(f"\n{C.SYSTEM}Navigate: ↑/↓/←/→ | Modify: M | Execute: E | Quit: Q{C.RESET}")

    def show_intro(self):
        """Show introduction"""
        self.clear_screen()
        self.print_header("S Y N T A X   T R E E   C L I M B E R")

        intro = f"""
{C.META}\"Code is data. Data is code. You are both.\"{C.RESET}

{C.DIM}Welcome to the ultimate meta-programming puzzle.

You are a cursor navigating the Abstract Syntax Tree (AST)
of living Python code. Each node is a room. Each connection
is a path. The code is both the game and the puzzle.

Your mission: Navigate the AST, modify nodes, change the code's
behavior to produce specific outputs.{C.RESET}

{C.BOLD}What is an AST?{C.RESET}

When Python runs code, it first parses it into a tree structure:

{C.CODE}def add(x, y):
    return x + y{C.RESET}

Becomes:

{C.FUNCTION}FunctionDef(name='add')
  └─ Return
      └─ BinOp(op=Add)
          ├─ Name(id='x')
          └─ Name(id='y'){C.RESET}

{C.BOLD}Gameplay:{C.RESET}

1. {C.SYSTEM}Navigate{C.RESET} through AST nodes (functions, variables, operators)
2. {C.SYSTEM}Modify{C.RESET} nodes (change constants, swap operators)
3. {C.SYSTEM}Execute{C.RESET} code to test your changes
4. {C.SYSTEM}Achieve{C.RESET} the goal output with limited modifications

{C.BOLD}Controls:{C.RESET}

{C.SYSTEM}Navigation:{C.RESET}
  ↑ - Move to parent node
  ↓ - Move to first child node
  ← - Move to previous sibling
  → - Move to next sibling

{C.SYSTEM}Modification:{C.RESET}
  M - Modify current node
  E - Execute code and see output

{C.SYSTEM}Other:{C.RESET}
  Q - Quit

{C.META}You are not playing code.
You ARE code.
Navigate yourself.{C.RESET}

{C.SYSTEM}[Press ENTER to begin]{C.RESET}
"""
        print(intro)
        input()

    def show_modification_menu(self):
        """Show modification options for current node"""
        node = self.position.node
        node_type = self.get_node_type(node)

        print(f"\n{C.BOLD}Modify {node_type}:{C.RESET}")

        if isinstance(node, ast.Constant):
            print(f"{C.SYSTEM}Current value: {node.value}{C.RESET}")
            new_value = input(f"{C.SYSTEM}New value: {C.RESET}").strip()
            return self.modify_constant(new_value)

        elif isinstance(node, ast.BinOp):
            current_op = self.op_to_string(node.op)
            print(f"{C.SYSTEM}Current operator: {current_op}{C.RESET}")
            print(f"{C.SYSTEM}Options: +, -, *, /, %, **{C.RESET}")
            new_op = input(f"{C.SYSTEM}New operator: {C.RESET}").strip()
            return self.modify_operator(new_op)

        elif isinstance(node, ast.Compare):
            print(f"{C.SYSTEM}Options: <, >, <=, >=, ==, !={C.RESET}")
            new_cmp = input(f"{C.SYSTEM}New comparison: {C.RESET}").strip()
            return self.modify_comparison(new_cmp)

        else:
            print(f"{C.ERROR}Cannot modify this node type{C.RESET}")
            input(f"{C.SYSTEM}Press ENTER to continue...{C.RESET}")
            return False

    def show_execution_result(self, success: bool, result: Any):
        """Show code execution result"""
        print(f"\n{C.BOLD}Execution Result:{C.RESET}")

        if success:
            print(f"{C.SUCCESS}Output: {result}{C.RESET}")

            if result == self.goal_output:
                print(f"{C.SUCCESS}✓ GOAL ACHIEVED!{C.RESET}")
                print(f"{C.SYSTEM}Press N for next level, or ENTER to continue{C.RESET}")
            else:
                print(f"{C.ERROR}✗ Goal: {self.goal_output}{C.RESET}")
                print(f"{C.SYSTEM}Press ENTER to continue...{C.RESET}")
        else:
            print(f"{C.ERROR}Error: {result}{C.RESET}")
            print(f"{C.SYSTEM}Press ENTER to continue...{C.RESET}")

    def show_victory(self):
        """Show victory screen"""
        self.clear_screen()
        self.print_header("M E T A   M A S T E R Y")

        victory = f"""
{C.SUCCESS}You've navigated the abstract.
Modified the conceptual.
Become the parser.{C.RESET}

{C.DIM}In this game, you experienced:

• Abstract Syntax Trees - how code becomes structure
• Meta-programming - code that modifies code
• Self-reference - navigating from within
• The dual nature of code - both instruction and data{C.RESET}

{C.BOLD}What You Learned:{C.RESET}

{C.META}AST Navigation:{C.RESET} Moving through code structure
{C.META}Node Types:{C.RESET} Functions, classes, operators, literals
{C.META}Code Modification:{C.RESET} Changing behavior by altering structure
{C.META}Meta-Programming:{C.RESET} Programs that understand themselves

{C.META}\"To understand recursion, you must first understand recursion.\"{C.RESET}

{C.DIM}You were code navigating code.
A function exploring its own definition.
The parser parsing itself.

This is the essence of meta-programming:{C.RESET}

{C.BOLD}Code as data.
Data as code.
Self-awareness through structure.{C.RESET}
"""
        print(victory)

    def play(self):
        """Main game loop"""
        self.show_intro()

        while not self.game_over:
            self.show_game_screen()

            # Get input
            try:
                import tty, termios
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                    # Handle arrow keys
                    if ch == '\x1b':
                        ch += sys.stdin.read(2)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)

                if ch == '\x1b[A':  # Up
                    self.navigate_up()
                elif ch == '\x1b[B':  # Down
                    self.navigate_down()
                elif ch == '\x1b[D':  # Left
                    self.navigate_prev()
                elif ch == '\x1b[C':  # Right
                    self.navigate_next()
                elif ch.lower() == 'm':
                    if self.modifications_made < self.max_modifications:
                        self.show_modification_menu()
                elif ch.lower() == 'e':
                    success, result = self.execute_code()
                    self.show_execution_result(success, result)

                    next_input = sys.stdin.read(1)
                    if next_input.lower() == 'n' and success and result == self.goal_output:
                        self.level += 1
                        self.setup_level(self.level)
                elif ch.lower() == 'q':
                    self.game_over = True
                    self.victory = False

            except (ImportError, termios.error):
                # Fallback
                cmd = input(f"\n{C.SYSTEM}Command (up/down/left/right/m/e/q): {C.RESET}").lower().strip()

                if cmd == 'up':
                    self.navigate_up()
                elif cmd == 'down':
                    self.navigate_down()
                elif cmd == 'left':
                    self.navigate_prev()
                elif cmd == 'right':
                    self.navigate_next()
                elif cmd == 'm':
                    if self.modifications_made < self.max_modifications:
                        if self.show_modification_menu():
                            print(f"{C.SUCCESS}Modified!{C.RESET}")
                        else:
                            print(f"{C.ERROR}Modification failed{C.RESET}")
                elif cmd == 'e':
                    success, result = self.execute_code()
                    self.show_execution_result(success, result)

                    if success and result == self.goal_output:
                        next_cmd = input().strip().lower()
                        if next_cmd == 'n':
                            self.level += 1
                            self.setup_level(self.level)
                    else:
                        input()
                elif cmd == 'q':
                    self.game_over = True
                    self.victory = False

        # Game over
        if self.victory:
            self.show_victory()
        else:
            print(f"\n{C.SYSTEM}Exiting meta-space...{C.RESET}\n")

        print(f"\n{C.SYSTEM}{'═' * 70}")
        print(f"SYNTAX TREE CLIMBER")
        print(f"Code as data, data as code")
        print(f"{'═' * 70}{C.RESET}\n")


def main():
    try:
        game = SyntaxTreeClimber()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{C.META}Parse interrupted{C.RESET}\n")
    except Exception as e:
        print(f"\n{C.ERROR}System error: {e}{C.RESET}\n")
        raise


if __name__ == "__main__":
    main()
