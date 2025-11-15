# SCHRÖDINGER'S DUNGEON

## Where Observation Creates Reality

### Concept

In quantum mechanics, particles exist in superposition - multiple states simultaneously - until observed. **Schrödinger's Dungeon** turns this into a roguelike where every room, enemy, and treasure exists in quantum superposition until you observe it.

Is there an enemy in that corner? Both yes and no. Until you look.

### The Innovation

**Traditional roguelikes**: Fixed world, you explore it

**Schrödinger's Dungeon**: Superposed world, you collapse it

The dungeon doesn't have a determined state until you observe it. You're not just exploring - you're creating reality through observation.

### Core Mechanics

```
╔═ QUANTUM DUNGEON ═╗
Room (0, 0) | HP: 10/10 | Gold: 0 | Q-Power: 3

  ###############
  #.....?.......#
  #.?...@...?...#
  #.......E.....#
  #...?.....$...#
  #.............▯#
  ###############

? = Superposed (could be enemy, treasure, or empty)
E = Collapsed to Enemy
$ = Collapsed to Treasure
@ = You (the observer)
▯ = Exit to next room
```

### Quantum States

#### Superposition
- Entities marked **?** exist in multiple states simultaneously
- Could be: Enemy (40-70% prob), Treasure (20%), or Empty (10-40%)
- Deeper rooms have higher enemy probability

#### Wave Function Collapse
- **Movement**: Walking into an entity collapses it
- **Observation**: Seeing an entity (within radius) collapses it
- **Quantum Manipulation**: Force favorable collapse (limited uses)

### Gameplay

#### Movement (W/A/S/D)
- Move in cardinal directions
- Auto-observe nearby entities (1 tile radius)
- Touching superposed entity collapses it
- Face consequences of collapse (combat, treasure, or nothing)

#### Observe (O)
- Collapse entities at extended range
- See what's ahead before committing
- No resource cost, but takes a turn

#### Quantum Manipulation (Q)
- **Limited uses** (starts with 3)
- Force favorable collapse in 3-tile radius
- All nearby superposed entities collapse to treasure or empty
- **NO ENEMIES** - you're cheating probability

### Combat

When you touch an enemy:
- Simple combat system
- Deal 1-3 damage
- Enemies have 2-4 HP
- If you don't one-shot them, they hit back for 1-2 damage
- Defeated enemies become ✗ (observable corpses)

### Treasure

- Gold pickups (3-8 gold)
- Instantly collected on contact
- No practical use yet (it's about the score)

### Room Navigation

Each room has 4 exits (north, south, east, west):
- Exits are marked **▯**
- Lead to procedurally generated adjacent rooms
- Each new room is fresh superposition
- Deeper = harder (more enemy probability)

### Strategy

#### Early Game
1. **Observe liberally** - Collapse entities before touching them
2. **Save Q-Power** - Don't waste quantum manipulations
3. **Avoid unnecessary risks** - Path around superposed entities

#### Mid Game
1. **Use Q-Power strategically** - Clear dangerous areas
2. **Observe before committing** - Look ahead before moving
3. **Manage HP** - Avoid low HP combat

#### Late Game
1. **Speed through** - You know the patterns
2. **Aggressive Q-Power use** - Clear paths efficiently
3. **Exit hunting** - Find exits fast

### Victory Condition

**Survive 10 rooms** - Navigate through 10 different rooms while staying alive

### The Quantum Mechanics Explained

#### Schrödinger's Cat

The famous thought experiment: A cat in a box with poison is simultaneously alive and dead until observed. In this game, **every entity is Schrödinger's cat**.

#### Observer Effect

In quantum mechanics, observation affects the system. Here, your presence (vision) **collapses wave functions** - determines reality.

#### Probability Manipulation

Quantum manipulation represents **influencing probability** before measurement. You're "loading the dice" before rolling.

### Educational Value

Players learn:
- **Superposition**: Multiple states existing simultaneously
- **Wave function collapse**: How observation creates definite states
- **Probability**: Different outcomes have different likelihoods
- **Observer effect**: Measurement changes the system

All through gameplay, not lectures.

### Why It's Unique

**Other roguelikes with randomness**:
- Randomness determined at generation
- You discover what was already there

**Schrödinger's Dungeon**:
- Randomness exists in superposition
- You **create** what's there by observing
- Can manipulate probability before collapse
- Observation is a mechanic, not just flavor

The difference is philosophical but gameplay-relevant. Nothing is determined until you look.

### Tips & Tricks

#### Observation Radius
- Default: 1 tile (Manhattan distance)
- Automatic around player
- Observe ability extends to 3 tiles
- Plan your vision carefully

#### Quantum Manipulation Timing
- Use when surrounded by unknowns
- 3-tile radius clears a safe zone
- Only 3 uses per game
- Save for dangerous situations

#### Combat Avoidance
- Observe before moving
- Path around enemies
- Use Q-Power to eliminate threats
- Fight only when necessary

#### Room Exploration
- Observe full room from center
- Identify exits
- Note enemy positions
- Plan path to exit

### The Philosophy

**Determinism vs Indeterminism**

Traditional roguelikes: World exists, you discover it (determinism)

Schrödinger's Dungeon: World becomes, you create it (indeterminism)

**Observer-Dependent Reality**

The game asks: *Does the enemy exist before you see it? Or does your observation create it?*

In the game: Literally the latter.

**Probability vs Certainty**

Most games hide information but have fixed reality.

This game has **no fixed reality** - only probabilities that collapse.

### Speedrunning

**Categories**:
- **Any%**: Reach 10 rooms, any HP
- **Pacifist**: Reach 10 rooms, 0 enemies defeated
- **No Q-Power**: No quantum manipulation uses
- **Gold Hoarder**: Maximum gold collected

**Routes**:
- Observe-heavy (slow but safe)
- Q-Power rush (fast but risky)
- Blind movement (RNG dependent, exciting)

### Code Structure

The game implements:
```python
class QuantumEntity:
    possible_states: List[str]
    probabilities: List[float]
    collapsed_state: Optional[str]

    def collapse(self) -> str:
        # Weighted random based on probabilities
        return random.choices(states, weights=probs)[0]
```

Each entity is literally in superposition until collapsed.

### How to Play

```bash
python3 schrodingers_dungeon.py
```

### Controls

- **W/A/S/D**: Move (collapses entities on contact)
- **O**: Observe at range (collapses without contact)
- **Q**: Quantum Manipulate (force favorable collapse)
- **X**: Quit

### Requirements

- Python 3.6+
- Terminal with ANSI color support
- Understanding that reality is probabilistic (optional)

### Compared to Other Games

#### VS Traditional Roguelikes
- **They**: Fixed generation, discover reality
- **This**: Quantum generation, create reality

#### VS The Last Recursion
- **Recursion**: Navigate code structure (internal)
- **Schrödinger**: Navigate probability space (external)

#### VS Echo Chambers
- **Echo**: Parallel definite timelines
- **Schrödinger**: Superposed indefinite states

Both deal with multiple realities, but differently.

### The Science

Inspired by real quantum mechanics:
- **Superposition**: Quantum particles in multiple states
- **Collapse**: Measurement forces single state
- **Probability**: Outcomes distributed by probability amplitudes
- **Observer effect**: Observation changes systems

Simplified for gameplay, but philosophically accurate.

### Expansion Ideas

Potential additions:
- **Entanglement**: Linked entities collapse together
- **Quantum Tunneling**: Phase through walls
- **Decoherence**: Superposition degrades over time
- **Schrödinger's Items**: Superposed equipment
- **Bosses**: Mega-superposed entities

### The Meta-Joke

The game itself exists in superposition:
- Is it fun? Unknown until you play.
- Is it hard? Depends on your observation.
- Will you win? Both yes and no until you try.

The cat is proud. Or dead. Or both.

---

*"The paradox vanishes only when you realize: before measurement, there is no reality."*

— Interpretation of Quantum Mechanics (Copenhagen)
