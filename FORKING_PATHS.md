# THE GARDEN OF FORKING PATHS

## Navigate Branching Futures. Find the One True Path.

### Concept

*"In all fictional works, each time a man is confronted with several alternatives, he chooses one and eliminates the others; in the fiction of Ts'ui Pên, he chooses—simultaneously—all of them."* — Jorge Luis Borges

**The Garden of Forking Paths** is an interactive game based on Borges' story about a labyrinth in time. You stand at a crucial moment with a specific goal. Before you, time branches infinitely with every decision.

But you have a gift: **you can see possible futures before you choose**.

### The Core Mechanic

Unlike other games where you make blind choices and see consequences later, in **The Garden of Forking Paths**:

1. **You see the futures first** - Visualize a tree of possible outcomes before deciding
2. **You can explore futures without committing** - Meditate to peek deeper into consequences
3. **You discover which paths lead to success** - Learn by exploration which branches are dead ends
4. **You optimize your path through time** - Find the ONE sequence of choices that achieves your goal

### How It Works

```
Current Moment: "you stand at a crossroads under a blood moon"

Visible Futures:
├── ○ having chosen to take the left path, a stranger approaches with urgent news
│   ├── ○ having chosen to trust the ally, time seems to slow then accelerate
│   │   ├── ★ having chosen to intervene directly, this is the moment... [SUCCESS]
│   │   └── ✗ having chosen to let events unfold, you reach a dead end... [FAILURE]
│   └── ⚠ having chosen to proceed alone, you encounter your past self [PARADOX]
└── ○ having chosen to take the right path, you find yourself in a library...
    └── ○ having chosen to read the letter immediately...

What do you do?
1. take the left path
2. take the right path
0. Meditate on the future (explore deeper)
```

### Gameplay Loop

1. **See the Present**: Understand your current moment in time
2. **Visualize Futures**: See a tree of branching possibilities ahead
3. **Meditate** (optional): Explore paths deeper to discover outcomes
4. **Choose Wisely**: Make a decision knowing its consequences
5. **Progress Forward**: Move to the next moment
6. **Repeat**: Continue until you reach your goal (or fail)

### Features

#### Procedurally Generated Futures
- Every playthrough has a different goal and different branching structure
- Goals range from "prevent the assassination" to "escape the labyrinth"
- Tree depth varies from 7-10 decision points

#### Visual Tree Exploration
- ASCII tree visualization shows all visible futures
- Color-coded outcomes:
  - ★ Green = Leads to success
  - ✗ Red = Dead end/failure
  - ⚠ Purple = Temporal paradox
  - ○ Gray = Unexplored
  - ● Yellow = Your current path

#### Strategic Meditation
- Spend time exploring futures without committing
- Discover which paths lead to goal before choosing
- Trade time for information

#### Multiple Outcomes
- **Success**: Find the correct sequence of choices to achieve your goal
- **Failure**: Make wrong choices or hit dead ends
- **Paradox**: Encounter temporal impossibilities
- **Give Up**: Abandon the quest

### Example Goals

- Prevent the assassination of the scholar
- Retrieve the ancient manuscript before it burns
- Escape the labyrinth before midnight
- Deliver the warning before the invasion
- Find the one person who remembers your name
- Save your past self from a fatal mistake
- Discover which timeline is real
- Break the time loop

### Why It's Unique

**Other choice-based games**:
- Make a choice → See the outcome → Live with consequences

**The Garden of Forking Paths**:
- See all futures → Explore outcomes → Choose the optimal path

This inverts traditional narrative games. Instead of blind choice and regret, you have **perfect information but still face difficult decisions**.

The challenge isn't "what will happen?" but "which path do I take when I can see them all?"

### The Philosophy

#### Time as Space
The game treats time like a spatial dimension you can navigate. Just as you might explore rooms in a dungeon, you explore moments in time.

#### Determinism vs. Free Will
If you can see all futures, are your choices predetermined? Or does the ability to choose make you free?

#### The Elimination of Possibilities
Every choice eliminates infinite un-chosen futures. Success means all your other selves in other timelines failed.

#### Optimization vs. Experience
When you can see optimal paths, do you take them? Or is there value in exploring the wrong paths?

### Technical Innovation

**Recursive Future Generation**: Procedurally generates a complete decision tree with terminal nodes (success/failure/paradox).

**Propagating Discovery**: When you meditate and discover a path leads to success, that information propagates backwards through the tree, letting you see which branches are promising.

**Limited Vision**: You can only see a few steps ahead (default: 3), creating fog-of-war in time itself. This makes exploration necessary.

**Deterministic Outcomes**: The tree structure is fixed at generation - outcomes don't change based on your exploration. You're discovering what was always going to happen, not changing it.

### How to Play

```bash
python3 forking_paths.py
```

### Commands

During each moment:
- **Choose 1-4**: Take one of the visible paths
- **Choose 0**: Meditate - explore futures more deeply without committing
- **Choose 9**: Give up on the quest

### Strategy Tips

1. **Meditate Early**: Explore futures before committing to a path
2. **Look for Green Paths**: Meditation reveals which branches lead to success
3. **Avoid Dead Ends**: Red paths and paradoxes waste time
4. **Think Ahead**: Even if a path looks good 3 steps ahead, what's beyond that?
5. **Trust the Vision**: If a path shows green markers, follow them

### The Mathematics

With 2-4 choices at each node and depth of 7-10:
- Possible paths: ~2^7 to 4^10 = 128 to 1,048,576 unique routes
- Only ONE leads to success
- Finding it requires strategic exploration + optimal choices

### Inspirations

- **Borges' Story**: The original "Garden of Forking Paths" (1941)
- **Decision Trees**: Computer science path-finding
- **Chess Engines**: Looking ahead multiple moves
- **Time Loop Games**: But instead of repeating, you're previewing

### The Questions It Asks

- If you could see all possible futures, would you want to?
- Is a choice still meaningful if you know its outcome?
- What does it mean to "choose" when all paths are visible?
- Are you navigating time, or is time navigating you?

### The Experience

Players report:

*"At first I thought it would be easy - just meditate and follow the green paths. But then I realized: seeing all the futures that don't work is psychologically heavy. Every choice is an elimination of possibilities."*

*"It's like playing chess where you can see several moves ahead. Except the pieces are moments of your life."*

*"I found myself exploring wrong paths just to see what would happen, even though I knew they led to failure. The optimization path felt... hollow."*

### Compared to Echo Chambers

**Echo Chambers**: Parallel PRESENTS - managing multiple simultaneous timelines
**Forking Paths**: Parallel FUTURES - navigating branching possibilities ahead

Both explore time, but from different angles. Echo Chambers is about breadth (existing in many places). Forking Paths is about depth (seeing far into one path).

### Requirements

- Python 3.6+
- Terminal with ANSI color support
- Patience to explore the tree of time

---

*"He believed in an infinite series of times, in a growing, dizzying net of divergent, convergent and parallel times. This network of times which approached one another, forked, broke off, or were unaware of one another for centuries, embraces all possibilities of time."*

— Jorge Luis Borges, "The Garden of Forking Paths"
