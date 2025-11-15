# SYNTAX TREE CLIMBER

## Navigate Code Structure. Modify From Within. Become The Parser.

### Concept

Every time Python runs code, it first parses it into an **Abstract Syntax Tree** (AST) - a hierarchical representation of code structure. Functions become nodes. Operators become edges. The code transforms from text into conceptual architecture.

**Syntax Tree Climber** makes this invisible structure **physically navigable**. You are a cursor moving through the AST of living code. Navigate nodes. Modify values. Change operators. Execute the code. Watch reality shift.

### The Innovation

**Traditional programming games**: Write code, see if it works

**Syntax Tree Climber**: **Navigate the structure of code from inside**, modify nodes directly, understand programs as architectural spaces

This isn't about typing code - it's about **moving through code as physical space**. The AST becomes a dungeon. Nodes are rooms. You climb through the conceptual architecture of programs.

### How to Play

```bash
python3 syntax_tree_climber.py
```

### Core Mechanic

```
╔═ SYNTAX TREE CLIMBER ═╗
Level 1 | Modifications: 0/1

Current Code:
 1 │ def calculate():
 2 │     x = 5
 3 │     y = 3
 4 │     result = x + y
 5 │     return result

AST Structure:
  Module (root)
   ► FunctionDef: calculate
      Assign: x = 5
        Constant: 5
      Assign: y = 3
        Constant: 3
      Assign: result = x + y
        BinOp: x + y
          Name: x
          Name: y
      Return: result

Current Node: FunctionDef: calculate
Navigate: ↑/↓/←/→ | Modify: M | Execute: E
```

### What is an AST?

#### Code as Text

```python
def add(x, y):
    return x + y
```

#### Code as Structure

```
FunctionDef(name='add', args=['x', 'y'])
 └─ body
     └─ Return
         └─ value
             └─ BinOp(op=Add)
                 ├─ left: Name(id='x')
                 └─ right: Name(id='y')
```

The AST is the **semantic structure** of code. Not characters, but **concepts**. Not syntax, but **meaning**.

### Node Types

#### Control Flow

**FunctionDef**: Function definition
- Contains: arguments, body, return statements
- Example: `def calculate():`

**If**: Conditional statement
- Contains: test condition, body, else clause
- Example: `if x > 10:`

**While**: Loop
- Contains: condition, body
- Example: `while running:`

**For**: Iteration
- Contains: target, iterator, body
- Example: `for item in items:`

#### Operations

**Assign**: Variable assignment
- Contains: targets, value
- Example: `x = 5`

**BinOp**: Binary operation
- Contains: left operand, operator, right operand
- Example: `x + y`, `a * b`

**Compare**: Comparison
- Contains: left, comparators, operators
- Example: `x < 10`, `a == b`

#### Values

**Name**: Variable reference
- Contains: identifier
- Example: `x`, `result`

**Constant**: Literal value
- Contains: value (int, str, etc.)
- Example: `42`, `"hello"`

### Gameplay

#### Navigation

**↑ (Up)**: Move to parent node
- From child to container
- From `Constant: 5` to `Assign: x = 5`

**↓ (Down)**: Move to first child
- From container to first element
- From `FunctionDef` to first statement in body

**← (Left)**: Move to previous sibling
- From one statement to previous statement
- From `Assign: y = 3` to `Assign: x = 5`

**→ (Right)**: Move to next sibling
- From one statement to next statement
- From `Assign: x = 5` to `Assign: y = 3`

#### Modification (M)

Navigate to a node, press M to modify:

**Constants**: Change the value
- Navigate to `Constant: 5`
- Press M
- Enter new value: `10`
- Code updates: `x = 10`

**Binary Operators**: Change the operation
- Navigate to `BinOp: x + y`
- Press M
- Choose operator: `*`
- Code updates: `x * y`

**Comparisons**: Change comparison type
- Navigate to comparison node
- Press M
- Choose: `<`, `>`, `<=`, `>=`, `==`, `!=`

#### Execution (E)

Press E to execute the current code:
- Code runs in isolated namespace
- Finds main function and calls it
- Shows output
- Compares to goal

### Level Design

#### Level 1: Tutorial
```python
def calculate():
    x = 5
    y = 3
    result = x + y
    return result
```
**Goal**: Output = 8 (already correct)
**Learn**: Navigate the AST, execute code

#### Level 2: Fix Operator
```python
def process_data():
    value = 10
    multiplier = 2
    result = value - multiplier  # BUG: should be *
    return result
```
**Goal**: Output = 20
**Solution**: Change `-` to `*`

#### Level 3: Fix Comparison
```python
def check_value():
    x = 15
    if x < 10:  # BUG: should be >
        return "small"
    else:
        return "large"
```
**Goal**: Output = "large"
**Solution**: Change `<` to `>`

#### Level 4: Multiple Changes
```python
def calculate_total():
    price = 100
    discount = 10
    tax = 5
    total = price - discount - tax
    return total
```
**Goal**: Output = 115
**Solution**: Change operators from `-` to `+`

#### Level 5: Complex Navigation
```python
def complex_function():
    numbers = [1, 2, 3]
    total = 0
    for num in numbers:
        total = total + num
    return total
```
**Goal**: Output = 60
**Solution**: Change list values and/or operator

### Strategy

#### Navigation Patterns

1. **Depth-first exploration**: Down to children, then siblings
2. **Parent-child relationship**: Understand containment
3. **Sibling traversal**: Move through sequential statements
4. **Root-to-leaf paths**: Trace from function to values

#### Modification Planning

1. **Identify goal**: What output is needed?
2. **Trace execution**: How does code currently work?
3. **Find difference**: What needs to change?
4. **Navigate to node**: Move cursor to the right AST node
5. **Modify precisely**: Change only what's necessary
6. **Verify**: Execute and check output

#### Common Pitfalls

- **Modifying wrong node**: Navigate carefully, check descriptions
- **Type mismatches**: Changing `5` to `"5"` changes type
- **Out of modifications**: Plan changes before making them
- **Lost in tree**: Use Up to return to parent, reorient

### Why It's Unique

**Other programming games**:
- Type code manually
- Trial and error
- Text-based interaction

**Syntax Tree Climber**:
- **Navigate structure spatially**
- Understand code architecture
- **Direct AST manipulation**
- See code as spatial/conceptual rather than textual

### Educational Value

Players learn:

**Abstract Syntax Trees**: How parsers understand code
**Code Structure**: Programs as hierarchical data
**Meta-programming**: Code that modifies code
**Operators**: How mathematical operations compose
**Control Flow**: How branching and looping work structurally

All through spatial navigation and direct interaction.

### The Computer Science

#### Parsing Pipeline

1. **Lexical Analysis**: Text → Tokens
   - `def add(x):` → `[DEF, NAME, LPAREN, NAME, RPAREN, COLON]`

2. **Syntactic Analysis**: Tokens → AST
   - Tokens → `FunctionDef(name='add', args=['x'])`

3. **Compilation**: AST → Bytecode
   - AST → Python bytecode

4. **Execution**: Bytecode runs

**This game lets you manipulate step 2** - the AST before compilation.

#### Real-World Applications

**Linters**: Navigate AST to find code smells
**Formatters**: Modify AST to enforce style
**Transpilers**: Transform one language's AST to another
**Optimizers**: Rewrite AST for performance
**Code Analysis**: Extract metrics from structure

### The Philosophy

#### Code as Data

Programs are dual:
- **Text**: Characters in a file
- **Data**: Structured information

The AST is the **data representation** of code. This game makes you experience code as data.

#### Homoiconicity

In languages like Lisp, code and data have the same structure. You can manipulate code as easily as data because they're the same thing.

**This game brings homoiconicity to Python** - navigate and modify code structure as if it were a game world.

#### Self-Reference

You are:
- **Code** (a player character in a program)
- Navigating **code** (an AST)
- That represents **code** (Python functions)
- Written in **code** (Python)

**Four levels of self-reference.** The game is code examining code examining code.

### Meta-Programming Concepts

#### Code Generation

Modifying AST nodes is how code generators work:
```python
# You change a constant from 5 to 10
# Behind the scenes:
ast.Constant(value=5)  # becomes
ast.Constant(value=10)
```

#### Code Transformation

Changing operators demonstrates code transformation:
```python
# You change + to *
ast.BinOp(left=x, op=ast.Add(), right=y)  # becomes
ast.BinOp(left=x, op=ast.Mult(), right=y)
```

This is how transpilers work - transforming code structure.

### Tips & Tricks

#### Navigation Shortcuts

- **Lost?** Go Up repeatedly to reach module root
- **Quick scan**: Down → Right → Right → Right to see siblings
- **Depth first**: Down until you can't, then Right
- **Breadth first**: Right across all siblings, then Down

#### Finding Modification Targets

1. Look at **goal output** vs **current output**
2. Trace **which nodes affect the result**
3. Navigate to **deepest relevant node** first
4. **Constants** are easiest to modify
5. **Operators** have biggest impact

#### Execution Strategy

- **Execute early and often** - see current behavior
- **Test after each modification** - verify it worked
- **Compare outputs** - goal vs actual
- **Understand causality** - which nodes affect output

### Speedrunning

**Categories**:
- **Any%**: Complete all levels, any modifications
- **Minimal Modifications**: Fewest total changes
- **No Execution**: Complete without testing (plan perfectly)
- **First Try**: Execute only once per level

### Compared to Other Games

#### VS The Last Recursion
- **Recursion**: Navigate stack frames (temporal structure)
- **Syntax Tree**: Navigate AST (spatial structure)

Both make abstract CS concepts physical.

#### VS Code Archaeology
- **Archaeology**: Understand alien paradigms (conceptual)
- **Syntax Tree**: Navigate code structure (architectural)

Both explore code as space.

### Expansion Ideas

Potential additions:
- **Add nodes**: Insert new statements into AST
- **Delete nodes**: Remove statements
- **Refactor mode**: Reorganize code structure
- **Optimize challenge**: Make code more efficient
- **Security mode**: Find and fix vulnerabilities
- **Multiple files**: Navigate imports and modules

### The Meta Joke

**You are playing a Python program that parses Python programs that you navigate as a player in a Python program.**

The game is **self-referential code**:
- Written in Python
- Parses Python
- Lets you modify Python
- By navigating Python's representation of Python

**It's Python all the way down.**

### Real Tool: AST Module

This game uses Python's real `ast` module:

```python
import ast

code = "x = 5 + 3"
tree = ast.parse(code)

# Navigate
for node in ast.walk(tree):
    print(node)

# Modify
# (What you do in the game)

# Recompile
new_code = ast.unparse(tree)
```

**Everything in the game is real.** The AST is Python's actual AST. The modifications are real modifications. The execution is real execution.

You're using real meta-programming tools, just gamified.

### Historical Context

#### Abstract Syntax Trees

Developed in the 1960s as compilers became more sophisticated.

**Before ASTs**: Compilers worked directly on text (fragile, complex)
**After ASTs**: Parse text → AST → Analyze/Transform → Generate code

ASTs separated **parsing** from **analysis** - made compilers modular and maintainable.

#### Lisp and S-Expressions

Lisp (1958) pioneered homoiconicity:
```lisp
(+ 1 2)  ; This is both code and data
```

The **structure is explicit** - parentheses show the tree. You can modify code as data naturally.

Python's AST brings this power to Python, and this game makes it playable.

### Requirements

- Python 3.6+ (ast.unparse requires 3.9+)
- Terminal with ANSI color support
- Understanding that all code is data (develops during play)

---

## The Three Truths

```
1. Code is data
2. Data is code
3. You are both
```

Navigate the abstract. Modify the structure. Become the parser.

---

*"Programs must be written for people to read, and only incidentally for machines to execute."*

— Structure and Interpretation of Computer Programs (SICP)

*"In Syntax Tree Climber, programs are written for people to navigate."*

— This game
