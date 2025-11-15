# ENTANGLEMENT

## Spooky Action at a Distance

### Concept

In quantum mechanics, **entanglement** is perhaps the strangest phenomenon. When two particles become entangled, measuring one instantly affects the other - regardless of the distance between them. Change the spin of one entangled electron, and its partner changes simultaneously, even if it's on the other side of the universe.

Einstein called this **"spooky action at a distance"** and believed it proved quantum mechanics was incomplete. He was wrong - entanglement is real, verified by countless experiments.

**Entanglement** makes this quantum phenomenon playable. Puzzle blocks are quantum-correlated. Push one, its partner moves too. Navigate both to goals simultaneously using nothing but entanglement.

### The Innovation

**Traditional puzzle games**: One object, one action, one consequence

**Entanglement**: One action → multiple simultaneous consequences via quantum correlation

You don't control blocks directly - you control them through their quantum relationships. This is **correlation as gameplay**.

### How to Play

```bash
python3 entanglement.py
```

### Core Mechanic

```
╔═ ENTANGLEMENT ═╗
Level 1 | Moves: 5

  ████████████████████
  █··@···■·····■····█
  █·············○···█
  █·············○···█
  █················█
  ████████████████████

@ = You
■ = Entangled block
○ = Goal (empty)
◆ = Goal (with block)
█ = Wall

Entangled Pairs:
  ■ (5,1) ⟷ ■ (10,1)
```

When you push one ■, both move in the same direction simultaneously.

### Quantum Entanglement Basics

#### What Is Entanglement?

Two particles are entangled when their quantum states are correlated:
- Measure one → Instantly know the other's state
- Change one → The other changes simultaneously
- Distance doesn't matter (can be light-years apart)
- No signal travels between them (doesn't violate relativity)

#### The EPR Paradox (1935)

Einstein, Podolsky, and Rosen asked: *How can particles communicate faster than light?*

Their conclusion: Either quantum mechanics is incomplete (there are "hidden variables"), or reality is non-local (spooky action).

#### Bell's Theorem (1964)

John Stewart Bell proved experimentally: **There are no hidden variables. Entanglement is real.**

The universe genuinely has instant correlations. Nature is fundamentally non-local.

### Gameplay

#### Movement

**W/A/S/D**: Move player
- Walk into empty space → You move
- Walk into block → You push it
- Push entangled block → **Both blocks move**

#### Entanglement Rules

**When you push an entangled block:**
1. Check if the block can move in that direction (no wall, no other block)
2. Check if its entangled partner can ALSO move in that direction
3. If both can move → Both move simultaneously
4. If either is blocked → Neither moves

**This is quantum correlation** - they're linked. One can't move unless both can.

#### Goal

Get all blocks onto goal positions (○)
- Blocks on goals show as: ◆ (highlighted)
- All goals must be filled to complete level
- Minimum moves bonus for efficiency

### Level Design

#### Level 1: Tutorial
```
Two entangled blocks, side by side
Push one right → Both move right
Get both onto goals
```

**Teaches**: Basic entanglement mechanics

#### Level 2: Multiple Pairs
```
Two independent entangled pairs
Each pair moves together
Navigate both pairs to different goals
```

**Teaches**: Managing multiple entangled systems

#### Level 3: Chain Reaction
```
Blocks arranged in a line:
■A ■A ■B ■B ■C ■C
Pushing left pair causes cascade
```

**Teaches**: Entanglement cascades and planning

#### Level 4: Complex Maze
```
Walls create paths
Entangled pairs separated by walls
Must navigate different routes simultaneously
```

**Teaches**: Strategic use of entanglement through obstacles

### Strategy

#### Planning Phase

1. **Identify entangled pairs** - Which blocks move together?
2. **Trace paths** - Where do both blocks need to go?
3. **Find constraints** - What walls block movement?
4. **Plan sequence** - What order of pushes works?

#### Execution Tactics

**Use walls as guides**:
- One block against wall → Can push other freely in perpendicular direction
- Create reference points for positioning

**Think in pairs**:
- Never consider one block alone
- Always visualize both entangled positions
- They're one system, not two objects

**Work backwards**:
- Start from goal positions
- Trace reverse path to starting positions
- Execute forward

**Minimize moves**:
- Each move affects both blocks
- Plan efficient paths
- Avoid backtracking

#### Common Mistakes

- **Forgetting the partner**: Pushing one without considering where partner goes
- **Assuming independence**: Blocks are NOT independent - they're correlated
- **Sequential thinking**: Both blocks move NOW, not after
- **Ignoring constraints**: Partner might be blocked even if pushed block isn't

### Why It's Unique

**Other Sokoban-like games**: Push one box at a time

**Entanglement**: **Push correlated pairs simultaneously**

The innovation:
- **Quantum correlation** as core mechanic
- **Synchronized movement** creating puzzles
- **Action at a distance** (blocks separated spatially, move together)
- **Constraint solving** (both must be able to move)

Traditional puzzles: One cause → One effect

Entanglement: One cause → Multiple correlated effects

### Educational Value

Players learn through gameplay:

**Quantum Correlation**: How entangled particles share state
**Action at a Distance**: Instant effects regardless of separation
**Non-locality**: No physical connection needed
**Constraint Propagation**: How correlations create limitations
**EPR Paradox**: The strangeness Einstein questioned

### The Science

#### Real Quantum Entanglement

**Spin Entanglement**:
```
Two electrons entangled with opposite spins
Measure one as "up" → Instantly know other is "down"
Works regardless of distance
```

**Photon Polarization**:
```
Entangled photons share polarization
Measure one vertically → Other is horizontal
Used in quantum cryptography
```

#### Bell Test Experiments

Performed thousands of times since 1972:
- Create entangled particles
- Separate them (sometimes kilometers apart)
- Measure both simultaneously
- Results show correlations impossible without "spooky action"

**Conclusion**: Entanglement is experimentally proven. Nature is non-local.

#### Applications

**Quantum Computing**:
- Entangled qubits perform parallel computation
- Quantum algorithms exploit correlation
- Exponentially faster than classical for some problems

**Quantum Cryptography**:
- Entangled photons for unbreakable encryption
- Any eavesdropping disturbs entanglement (detectable)
- Perfectly secure communication

**Quantum Teleportation**:
- Transfer quantum state using entanglement
- Not faster-than-light communication (requires classical channel)
- But state transfer without physical transmission

**Quantum Sensors**:
- Entangled particles for ultra-precise measurements
- Gravitational wave detectors
- Atomic clocks

### The Philosophy

#### Non-Locality

Entanglement proves the universe is **non-local**:
- Events at one location instantly affect events elsewhere
- No signal travels (doesn't violate relativity)
- But correlation is instantaneous

This challenges our intuition about space and separation.

#### Holism

Entangled particles aren't two separate things - they're **one system**:
- Can't describe one without describing both
- The whole has properties the parts don't
- Quantum mechanics is fundamentally holistic

In the game: You don't move blocks separately. You move the **entangled system**.

#### Reality and Measurement

Entanglement raises questions:
- Do particles have definite states before measurement?
- Or does measurement create the state?
- How can correlation exist without communication?

The game doesn't answer these - quantum mechanics doesn't either. It just works.

### Tips & Tricks

#### Visualization

- **Draw paths**: Sketch where each block needs to go
- **Trace simultaneously**: Follow both blocks at once mentally
- **Use symmetry**: Entangled pairs often move symmetrically

#### Wall Techniques

- **Pin one block**: Use wall to stop one, move other
- **Channel pairs**: Use corridors to guide both
- **Create barriers**: Walls separate but don't break entanglement

#### Efficiency

- **Minimal moves**: Fewest pushes win
- **Direct paths**: Straight lines when possible
- **Avoid oscillation**: Don't push back and forth

#### Advanced

- **Chain reactions**: Push one pair into another
- **Cascade setups**: Arrange so one move triggers many
- **Constraint exploitation**: Use blocking as a tool

### Speedrunning

**Categories**:
- **Any%**: Complete all levels, any moves
- **Minimal Moves**: Fewest total moves across all levels
- **Perfect Path**: Complete each level in theoretical minimum
- **No Resets**: Complete without restarting levels

**Strategies**:
- Pre-plan entire solution before first move
- Memorize optimal sequences
- Execute without hesitation

### Compared to Other Games

#### VS Schrödinger's Dungeon
- **Schrödinger**: Superposition (probabilistic states)
- **Entanglement**: Correlation (deterministic links)

Both quantum phenomena, different mechanics.

#### VS The Butterfly Effect
- **Butterfly**: Delayed cascade effects (temporal)
- **Entanglement**: Instant correlated effects (spatial)

Both show how actions propagate, different mechanisms.

### Expansion Ideas

Potential additions:
- **Triple entanglement**: Three blocks moving together
- **Partial entanglement**: Only some properties shared
- **Entanglement creation**: Form links during gameplay
- **Decoherence**: Entanglement decays over time/moves
- **Measurement**: Collapse entanglement to gain info
- **3D levels**: Entanglement in three dimensions

### Historical Context

#### Einstein's Objection

Einstein never accepted entanglement:
- Called it "spooky action at a distance"
- Believed it proved quantum mechanics incomplete
- Proposed hidden variable theories as alternative

He was wrong, but his skepticism drove crucial experiments.

#### Bell's Breakthrough

John Stewart Bell (1964) proved:
- Hidden variable theories make different predictions than QM
- Experiments can distinguish between them
- Results: Quantum mechanics is correct, no hidden variables

#### Modern Verification

Since 1970s:
- Hundreds of Bell test experiments
- Entanglement verified at distances up to 1200km
- Loopholes progressively closed
- Now: Indisputable experimental fact

### The Math (Simplified)

#### Entangled State

Two particles A and B in entangled state:
```
|Ψ⟩ = (1/√2)(|↑⟩A|↓⟩B - |↓⟩A|↑⟩B)
```

This means:
- If A is measured up, B is down
- If A is measured down, B is up
- But neither has definite state until measured

**Correlation without communication.**

#### Bell Inequality

Classical correlation predicts:
```
|E(a,b) - E(a,c)| ≤ 1 + E(b,c)
```

Quantum entanglement violates this:
```
Can reach values > 2√2 ≈ 2.83
```

This violation proves non-locality.

### Real-World Analogy

**Classical correlation** (not entanglement):
- Separate pair of gloves into two boxes
- Open one → Know the other's handedness
- But the glove was always left or right

**Quantum entanglement**:
- Separate entangled particles
- Measure one → Other becomes correlated state
- But neither had definite state before measurement
- **State is created by measurement, not revealed**

This is the profound weirdness.

### The Game's Accuracy

**What's accurate**:
- Instant correlation (push one → both move now)
- Action at a distance (separation doesn't matter)
- Correlation constraint (both must satisfy movement rules)
- Can't signal faster than light (you still need to move to blocks)

**What's simplified**:
- Real entanglement is about quantum states, not position
- Real particles don't "push" each other
- Measurement causes decoherence (game entanglement persists)

But the **spirit** is accurate - correlation without mechanism.

### Requirements

- Python 3.6+
- Terminal with ANSI color support
- Willingness to accept non-locality (optional)

---

## The Three Truths

```
1. Entanglement is real
2. Correlation is instant
3. Distance doesn't matter
```

Spooky action at a distance. Made playable.

---

*"I think I can safely say that nobody understands quantum mechanics."*

— Richard Feynman

*"But you can still play with it."*

— This game
