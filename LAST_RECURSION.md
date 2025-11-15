# THE LAST RECURSION

## Debug Yourself From The Inside

### Concept

```python
function escape(depth):
    if depth > MAX_DEPTH:
        raise StackOverflowError

    return escape(depth + 1)  # You are trapped here
```

**The Last Recursion** is a unique puzzle/roguelike game where you ARE a function trapped in infinite recursion. Navigate through your own stack frames, collect return values, avoid corruption, and find the base case before stack overflow destroys you.

### The Innovation

Unlike philosophical narrative games, this is an **actual puzzle/action game** with unique mechanics:

- **You navigate the call stack** - Each level is literally a stack frame
- **Recursion as gameplay** - Going deeper is part of the challenge
- **Stack pressure mechanics** - The deeper you go, the more danger you're in
- **Code corruption** - Your own code degrades as stack grows
- **Find the base case** - The only way to escape infinite recursion

### How It Works

```
╔═ STACK FRAME 3 ═╗
Stack: ████░░░░░░ 40%
Returns: 2/3 | Corruption: 30%

  ####################
  #@.......R.........#
  #.###.............#
  #.###.....X.......#
  #.................#
  #........X........#
  #......R..........#
  #.......##......B.#
  #.................#
  ####################

  @ = You (the function)
  R = Return values (collect to satisfy contract)
  > = Exit (recurse deeper OR return)
  X = Corruption (damages your stack)
  B = Base case (escape recursion!)
  # = Walls (code structure)
```

### Core Mechanics

#### 1. Stack Frames as Levels
Each recursion level is a puzzle you must navigate:
- Start at top-left
- Collect required return values (R)
- Reach exit (>)
- Avoid corruption (X)

#### 2. Recursion Depth
- **Depth 0**: Clean, simple
- **Depth 5**: More walls, corruption appears
- **Depth 8**: Heavily corrupted, complex
- **Depth 10**: Stack overflow - game over

#### 3. Return Values
- Each frame requires return values (contracts)
- Must collect all before exiting
- Needed to safely return to previous frames

#### 4. Stack Corruption
- Hitting corruption (X) damages your stack
- More corruption = harder to escape
- Visual feedback: colors get darker/redder

#### 5. Base Case
- Randomly appears at depth 5+
- Marked as "B"
- Finding it lets you escape entire recursion
- Without it, you must reach depth 10 (overflow)

### Gameplay Loop

1. **Navigate** the current stack frame (W/A/S/D)
2. **Collect** all required return values (R)
3. **Decide**:
   - Exit (>) to recurse deeper
   - Return (R key) to previous frame (if you have returns)
4. **Find** the base case (B) to escape
5. **Avoid** stack overflow (depth 10)

### Controls

- **W/A/S/D** or **Arrow Keys**: Move
- **R**: Return to previous stack frame (if possible)
- **Q**: Give up (stack overflow)

### Win Conditions

**Success**: Find the base case (B) and safely unwind the stack

**Failure**:
- Reach depth 10 without base case (stack overflow)
- Too corrupted to continue
- Give up

### Strategy Tips

1. **Collect all returns** before moving on - you'll need them to go back
2. **Explore thoroughly** at depth 5+ - base case appears there
3. **Avoid corruption** when possible - it makes everything harder
4. **Don't recurse unnecessarily** - the deeper you go, the harder it gets
5. **You can go back!** If you have returns, use R to return to previous frames

### The Programming Metaphor

This game is a playable metaphor for:

- **Recursive functions** - Calling yourself
- **Stack frames** - Each call creates a new frame
- **Return values** - Functions must return something
- **Stack overflow** - Too much recursion crashes
- **Base cases** - The condition that stops recursion
- **Memory corruption** - Stack degradation

### Why It's Unique

**Other roguelikes**: Navigate dungeons, find exit, collect loot

**The Last Recursion**:
- Navigate your own **code**
- Each level is a **recursive call to yourself**
- "Going deeper" = recursing
- "Going back" = returning
- Goal isn't just exit - it's **finding the condition to stop recursing**

The game makes abstract CS concepts (recursion, stack frames, base cases) **physically navigable**.

### Technical Details

#### Procedural Generation
- Levels generated based on depth
- More walls/corruption at deeper levels
- Base case probability increases with depth
- Deterministic for given depth + seed

#### Visual Feedback
- **Color coding by depth**: Cyan → Blue → Purple → Red
- Stack pressure bar shows overflow risk
- Corruption percentage displayed
- Return value counter

#### Difficulty Curve
- **Depth 0-2**: Tutorial (easy navigation)
- **Depth 3-5**: Medium (more obstacles)
- **Depth 6-8**: Hard (heavy corruption)
- **Depth 9-10**: Critical (stack overflow imminent)

### Example Session

```
Start: Depth 0
↓ Collect returns, exit
Depth 1
↓ Collect returns, exit
Depth 2
↓ Collect returns, exit
Depth 3 (corruption appears)
↓ Carefully collect returns, exit
Depth 4
↓ Find BASE CASE (B)!
← Return with base case
Depth 3
← Return
Depth 2
← Return
Depth 1
← Return
Depth 0
SUCCESS! Recursion unwound safely.
```

### The Philosophy

While more action-oriented than the other games, this still explores:

- **Self-reference**: You are debugging yourself
- **Infinite regress**: Recursion without base case
- **Emergence**: Complex behavior from simple rules
- **Abstraction made concrete**: Code concepts as physical space

### Compared to Other Games in Collection

- **Echo Chambers**: Parallel timelines (breadth)
- **Code Archaeology**: Debug others' code (external)
- **Infinite Library**: Search infinite space (exploration)
- **Forking Paths**: Navigate futures (planning)
- **Last Recursion**: Debug yourself (internal, action)

This adds **action/puzzle gameplay** to the collection while maintaining conceptual depth.

### Educational Value

Players learn:
- How recursion actually works
- Why base cases are critical
- What stack frames are
- How stack overflow happens
- Why return values matter

All through gameplay, not lectures.

### Speedrun Potential

- **Minimum depth run**: Find base case as early as possible
- **Maximum depth run**: See how deep you can go
- **Perfect run**: No corruption hits
- **Minimum moves**: Shortest path to base case

### Future Enhancements

Possible additions:
- **Parameters**: Collect parameters to enable returns
- **Tail call optimization**: Special moves that don't increase depth
- **Function composition**: Multiple functions in stack
- **Exception handling**: Try/catch mechanics
- **Memoization**: Remember visited frames

### How to Play

```bash
python3 last_recursion.py
```

### Requirements

- Python 3.6+
- Terminal with ANSI color support
- Keyboard input (W/A/S/D)

### Tips for Enjoyment

1. **Think like a function** - You're not exploring a dungeon, you're executing code
2. **Plan your recursion** - Don't go deeper than necessary
3. **Collect before exiting** - Always get all returns first
4. **Hunt for the base case** - It's your ticket out
5. **Watch the stack** - Pressure bar shows your danger level

---

## The Code

The game itself is recursive:
```python
def play_level(depth):
    if found_base_case():
        return SUCCESS

    if depth >= MAX_DEPTH:
        return STACK_OVERFLOW

    collect_returns()

    if chose_to_recurse():
        return play_level(depth + 1)
    else:
        return play_level(depth - 1)
```

You're playing the function from inside itself.

---

*"The only way out of infinite recursion is through it."*
