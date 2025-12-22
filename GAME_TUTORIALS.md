# VAULT 13 - Complete Game Tutorials

Welcome to the complete tutorial guide for VAULT 13 and all 36 philosophical mini-games. This guide explains how to play each game, what the objectives are, and how to use the AI helper features.

---

## Table of Contents

1. [Main Game: VAULT 13 - Survival Protocol](#main-game-vault-13---survival-protocol)
2. [AI Helper Features](#ai-helper-features)
3. [Quantum & Physics Games](#quantum--physics-games)
4. [Computation & Logic Games](#computation--logic-games)
5. [Philosophy & Consciousness Games](#philosophy--consciousness-games)
6. [Decision & Ethics Games](#decision--ethics-games)
7. [Other Paradox Games](#other-paradox-games)

---

# Main Game: VAULT 13 - Survival Protocol

## Overview

VAULT 13 is a post-apocalyptic vault management simulation inspired by Fallout Shelter. You are the Overseer of Vault 13, responsible for managing resources, dwellers, and survival in a hostile wasteland.

## How to Run

```bash
# Latest version (v9.0)
python3 vault_shelter_v6.py

# AI Edition (v3.0) - with AI advisor
python3 vault_shelter_ai.py

# Classic version (v2.0)
python3 vault_shelter.py
```

## Objective

**Primary Goal:** Keep your vault dwellers alive and happy while managing resources and expanding your vault.

**Victory Conditions (v6.0+):**
- **Utopia:** Achieve 90%+ average happiness with 20+ dwellers
- **Economic:** Accumulate 10,000+ caps
- **Research:** Complete all technology research
- **Military:** Successfully repel 10+ raids
- **Exodus:** Prepare and launch an expedition to a new vault location

## Core Mechanics

### Resources

| Resource | Icon | Purpose | Production Room |
|----------|------|---------|-----------------|
| Power | ⚡ | Keeps rooms functioning | Power Generator |
| Water | 💧 | Keeps dwellers hydrated | Water Treatment |
| Food | 🍖 | Keeps dwellers fed | Diner |
| Caps | 💰 | Currency for building/upgrades | Various activities |

**Critical Warning:** If any resource hits 0, dwellers start dying!

### SPECIAL Stats

Each dweller has 7 stats (1-10 scale) that affect their performance:

| Stat | Letter | Best For |
|------|--------|----------|
| Strength | S | Power Generator |
| Perception | P | Water Treatment |
| Endurance | E | Exploration, Health |
| Charisma | C | Radio Room, Trading |
| Intelligence | I | Science Lab, Medbay |
| Agility | A | Diner (Food) |
| Luck | L | Rush success, Loot |

**Tip:** Assign dwellers to rooms matching their highest stat for maximum production!

### Controls

| Key | Action |
|-----|--------|
| `B` | Build new room |
| `D` | Manage dwellers |
| `R` | Manage rooms |
| `E` | Send dweller on expedition |
| `T` | Talk to dweller (AI Edition) |
| `A` | AI Advisor (AI Edition) |
| `N` | Natural language mode (AI Edition) |
| `S` | Save game |
| `L` | Load game |
| `?` | Context-sensitive help |
| `Space/Enter` | Advance time (next turn) |
| `Q` | Quit |

### Building Rooms

| Room | Cost | Capacity | Function |
|------|------|----------|----------|
| Power Generator | 150 | 2 | Produces power |
| Water Treatment | 120 | 2 | Produces water |
| Diner | 100 | 2 | Produces food |
| Living Quarters | 100 | 4 | Increases population cap |
| Training Room | 200 | 2 | Train SPECIAL stats |
| Storage Room | 80 | 0 | Increases resource storage |
| Medbay | 150 | 2 | Heals injured dwellers |
| Science Lab | 250 | 2 | Research technologies |

### Daily Cycle

Each turn represents one day:
1. **Production Phase:** Rooms produce resources based on workers
2. **Consumption Phase:** Dwellers consume food and water
3. **Event Phase:** Random events may occur (raids, fires, new arrivals)
4. **Happiness Update:** Dweller mood changes based on conditions

### Tips for Beginners

1. **Balance resources first** - Ensure production exceeds consumption
2. **Assign everyone** - Idle dwellers lose happiness
3. **Match stats to rooms** - A dweller with high Strength in Power Generator produces more
4. **Build Living Quarters early** - You need room for new arrivals
5. **Save often** - Disasters can strike anytime
6. **Rush carefully** - Failed rushes cause fires!

---

# AI Helper Features

The AI Edition (v3.0+) includes three powerful AI features powered by Claude.

## Setup

```bash
# Install the Anthropic SDK
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run AI edition
python3 vault_shelter_ai.py
```

**Demo Mode:** Without an API key, the game runs with fallback responses.

## Feature 1: AI Overseer Advisor [A key]

**What it does:** Analyzes your entire vault and provides strategic recommendations.

**How to use:**
1. Press `A` from the main menu
2. Ask a question or press Enter for general analysis
3. Receive detailed strategic advice

**Example questions:**
- "What should I build next?"
- "Why is morale low?"
- "How can I improve efficiency?"
- "Help! My vault is failing!"

**The AI analyzes:**
- Resource levels vs consumption rates
- Dweller assignments and idle workers
- Production bottlenecks
- Health and happiness trends
- Optimal room placement

## Feature 2: Talk to Dwellers [T key]

**What it does:** Generates unique, personality-driven dialogue for each dweller.

**How to use:**
1. Press `T` from the main menu
2. Select a dweller to talk to
3. Read their context-aware response

**Personality System:**
Each dweller has 4 traits that affect their dialogue:
- **Outlook:** Optimistic, Pessimistic, Pragmatic, Cynical
- **Work Ethic:** Hardworking, Lazy, Ambitious, Laid-back
- **Social:** Friendly, Reserved, Charismatic, Awkward
- **Courage:** Brave, Cautious, Reckless, Cowardly

**Dynamic awareness:** Dialogue changes based on health, happiness, job, equipment, and recent events.

## Feature 3: Natural Language Commands [N key]

**What it does:** Control your vault by typing commands in plain English.

**How to use:**
1. Press `N` to toggle Natural Language mode
2. Type commands naturally
3. Type `menu` to return to normal controls

**Example commands:**
```
> assign sarah to power generator
> what's my food situation?
> rush the diner
> give sarah the laser rifle
> who should work in the science lab?
> end turn
```

**Supported actions:**
- Assignments: "assign [dweller] to [room]"
- Building: "build a [room type]"
- Upgrading: "upgrade [room]"
- Equipment: "equip [item] to [dweller]"
- Status: "check [resource]", "how much food?"
- Strategy: "what should I build?"
- Turn: "end turn", "next day"

---

# Quantum & Physics Games

## 1. Schrodinger's Dungeon

**File:** `schrodingers_dungeon.py`

**Concept:** Every room exists in quantum superposition until observed. Enemies are alive AND dead until you look.

**How to Play:**
- Navigate a dungeon using arrow keys or WASD
- Rooms marked with `?` are in superposition
- Moving near a room "observes" it, collapsing the wave function
- Collapsed rooms reveal: enemies (E), treasure ($), or empty (.)

**Objective:** Survive the dungeon by strategically observing rooms. Collect treasure while avoiding enemies.

**Controls:**
| Key | Action |
|-----|--------|
| W/↑ | Move up |
| S/↓ | Move down |
| A/← | Move left |
| D/→ | Move right |
| Q | Quantum manipulation (special ability) |

**Strategy:** Conserve your quantum manipulations for dangerous situations. The deeper you go, the more enemies appear.

---

## 2. Echo Chambers

**File:** `echo_chambers.py`

**Concept:** You exist across multiple parallel timelines simultaneously. Decisions create branching realities that continue to evolve.

**How to Play:**
- Start in the "Prime Timeline"
- Make choices that affect timeline properties
- Switch between timelines to observe consequences
- Collect memory fragments scattered across realities

**Objective:** Collect all memory fragments while preventing timeline collapse. Timelines decay when neglected.

**Timeline States:**
- **Healthy:** Stable, safe to explore
- **Decaying:** Neglected, needs attention
- **Corrupted:** Dangerous, may collapse
- **Collapsed:** Lost forever

**Strategy:** Balance attention across timelines. Actions in one timeline can "echo" to others.

---

## 3. Quantum Eraser

**File:** `quantum_eraser.py`

**Concept:** Explore the quantum eraser experiment - how observation affects reality, and how "erasing" information can restore interference patterns.

**How to Play:**
- Set up photon experiments
- Choose whether to observe (measure) particle paths
- See how observation collapses wave functions
- Use quantum erasure to restore superposition

**Objective:** Understand the relationship between observation, information, and quantum behavior.

---

## 4. Entanglement

**File:** `entanglement.py`

**Concept:** Explore quantum entanglement (EPR paradox). Measure one particle and instantly know about its entangled partner.

**How to Play:**
- Create entangled particle pairs
- Separate them across space
- Measure one particle's properties
- Observe instantaneous correlation with the other

**Objective:** Use entanglement to solve puzzles. Information doesn't travel faster than light - but correlations do!

---

## 5. The Butterfly Effect

**File:** `butterfly_effect.py`

**Concept:** Chaos theory - small changes lead to massive consequences. A butterfly flaps its wings and causes a hurricane.

**How to Play:**
- Start with a small decision
- Watch consequences cascade through systems
- Try to predict outcomes (hint: you can't)
- Observe how different initial conditions diverge

**Objective:** Experience sensitive dependence on initial conditions. Learn why long-term prediction is impossible in chaotic systems.

---

## 6. The Emergence Engine

**File:** `emergence_engine.py`

**Concept:** Simple rules create complex behavior. Watch emergence happen in cellular automata and multi-agent systems.

**How to Play:**
- Set initial conditions
- Define simple rules (like Conway's Game of Life)
- Run simulation
- Observe emergent patterns

**Objective:** Discover how complexity emerges from simplicity. Find gliders, oscillators, and stable structures.

---

## 7. Maxwell's Demon

**File:** `maxwells_demon.py`

**Concept:** A thought experiment about entropy. A demon sorts fast and slow molecules - seemingly violating the second law of thermodynamics.

**How to Play:**
- Control the demon at a partition between two chambers
- Sort molecules by speed (fast left, slow right)
- Create temperature difference without work
- Discover why this doesn't actually violate physics

**Objective:** Learn that information has physical cost. The demon's memory must be erased, increasing entropy.

---

## 8. Laplace's Demon

**File:** `laplaces_demon.py`

**Concept:** Determinism - if you knew all positions and velocities, could you predict the entire future?

**How to Play:**
- Given partial information about a system
- Try to predict future states
- Discover limits of determinism
- Encounter quantum uncertainty and chaos

**Objective:** Explore why perfect prediction is impossible even in a deterministic universe.

---

## 9. Twin Paradox

**File:** `twin_paradox.py`

**Concept:** Special relativity. One twin travels near light speed, returns younger than their sibling.

**How to Play:**
- Send one twin on a space journey
- Control velocity (as fraction of light speed)
- Return to Earth
- Compare ages due to time dilation

**Objective:** Experience how time passes differently for moving observers. Understand why this isn't actually a paradox.

---

# Computation & Logic Games

## 10. The Halting Problem

**File:** `halting_problem.py`

**Concept:** Alan Turing proved no algorithm can determine if ALL programs halt or loop forever.

**How to Play:**
- Analyze programs shown on screen
- Predict: will it HALT or LOOP forever?
- Press H for Halt, L for Loop
- Progress through increasingly complex programs

**Objective:** Experience the fundamental limit of computation. Encounter self-referential programs that break any oracle.

**Key Insight:** When you reach the PARADOX program that asks "what does the oracle say about me?", you've hit undecidability.

---

## 11. The Last Recursion

**File:** `last_recursion.py`

**Concept:** Recursion and stack overflow. Dive deeper into function calls until you hit the limit.

**How to Play:**
- Enter recursive function calls
- Track the call stack
- Manage stack depth
- Avoid stack overflow

**Objective:** Understand recursion by experiencing it. See how base cases prevent infinite recursion.

---

## 12. Syntax Tree Climber

**File:** `syntax_tree_climber.py`

**Concept:** Navigate abstract syntax trees (ASTs) - how compilers see your code.

**How to Play:**
- View code as a tree structure
- Navigate between nodes (expressions, statements, operators)
- Evaluate expressions by traversing the tree
- Transform code by manipulating nodes

**Objective:** Understand how programming languages are parsed and executed.

---

## 13. Code Archaeology

**File:** `code_archaeology.py`

**Concept:** Debug programs from alien civilizations using unfamiliar paradigms.

**How to Play:**
- Examine alien code samples
- Deduce the programming paradigm
- Figure out what the code does
- Fix bugs without documentation

**Objective:** Learn that programming concepts transcend syntax. Logic is universal.

---

## 14. Godel's Paradox

**File:** `godels_paradox.py`

**Concept:** Godel's Incompleteness Theorems - any consistent system has true statements it cannot prove.

**How to Play:**
- Work within a formal logical system
- Construct self-referential statements
- Discover statements that are true but unprovable
- Experience the limits of formal systems

**Objective:** Understand why mathematics cannot prove its own consistency.

---

## 15. The Infinite Library

**File:** `infinite_library.py`

**Concept:** Borges' Library of Babel - a library containing every possible book.

**How to Play:**
- Navigate through hexagonal rooms
- Each room contains books with random character sequences
- Search for meaningful text
- Most books are gibberish

**Objective:** Find coherent books in an ocean of noise. Experience the difference between possibility and probability.

---

## 16. Zeno's Runner

**File:** `zenos_runner.py`

**Concept:** Zeno's paradoxes - how can motion exist if you must cross infinite half-distances?

**How to Play:**
- Race toward a finish line
- Each step covers half the remaining distance
- Watch distance decrease: 1, 0.5, 0.25, 0.125...
- Experience infinite series convergence

**Objective:** Understand how infinite series can sum to finite values. Motion is possible!

---

## 17. Sorites Paradox

**File:** `sorites_paradox.py`

**Concept:** The paradox of the heap. Remove one grain of sand - when does a heap stop being a heap?

**How to Play:**
- Start with a heap of 10,000 grains
- Remove grains one at a time
- Answer: is this still a heap?
- Face the vagueness of language

**Objective:** Experience how precise logic struggles with vague concepts. Where do you draw the line?

---

# Philosophy & Consciousness Games

## 18. The Chinese Room

**File:** `chinese_room.py`

**Concept:** John Searle's argument about AI and understanding. Can symbol manipulation ever equal understanding?

**How to Play:**
- You're in a room with a rulebook
- Chinese symbols slide under the door
- Match patterns, output responses
- You don't understand Chinese - you follow rules

**Objective:** Pass the "Turing test" in Chinese while understanding nothing. Question whether AI truly understands.

**Controls:**
- Match incoming patterns to rules
- Select the correct rule number
- Send response

---

## 19. Mary's Room

**File:** `marys_room.py`

**Concept:** Knowledge argument about qualia. Mary knows everything about color science but has never seen red.

**How to Play:**
- Learn all physical facts about color
- Study wavelengths, neurons, perception
- Then... see red for the first time
- Did you learn something new?

**Objective:** Experience the debate between physicalism and qualia. Can all knowledge be expressed in facts?

---

## 20. Plato's Cave

**File:** `platos_cave.py`

**Concept:** Allegory of the Cave. Prisoners see only shadows and think they are reality.

**How to Play:**
- Start chained in a cave, seeing shadows
- Break free and turn around
- See the fire casting shadows
- Exit to sunlight and true reality
- Return to tell others (they won't believe you)

**Objective:** Experience the journey from illusion to enlightenment. Question what you assume is "real."

---

## 21. Ship of Theseus

**File:** `ship_of_theseus.py`

**Concept:** Identity paradox. Replace every plank of a ship - is it still the same ship?

**How to Play:**
- Manage a ship over time
- Replace worn planks gradually
- Eventually every original piece is gone
- Someone rebuilds a ship from the old planks
- Which is the "real" Ship of Theseus?

**Objective:** Explore personal identity and persistence through time. Are you the same person as yesterday?

---

## 22. The Categorizer

**File:** `the_categorizer.py`

**Concept:** Classification and taxonomy. Where do you draw boundaries between categories?

**How to Play:**
- Sort items into categories
- Encounter edge cases
- Decide: is a hot dog a sandwich?
- Face the arbitrary nature of classification

**Objective:** Understand that categories are human constructs, not natural kinds.

---

# Decision & Ethics Games

## 23. The Trolley Problem

**File:** `trolley_problem.py`

**Concept:** Ethics as cascading consequences. Every choice creates new dilemmas.

**How to Play:**
- Face the classic trolley problem
- Choose: let 5 die, or actively kill 1?
- Your choice leads to NEW dilemmas
- Track your ethical framework scores

**Objective:** Discover your moral philosophy through choices. Different frameworks often conflict.

**Ethical Frameworks:**
- **Utilitarian:** Greatest good for greatest number
- **Deontological:** Rules matter, don't use people as means
- **Virtue Ethics:** What would a virtuous person do?
- **Care Ethics:** Relationships and empathy matter

---

## 24. Prisoner's Dilemma

**File:** `prisoners_dilemma.py`

**Concept:** Game theory classic. Cooperate or defect?

**How to Play:**
- Play against AI strategies
- Choose: Cooperate (C) or Defect (D)
- Payoff matrix determines scores
- Watch strategies evolve over rounds

**Payoff Matrix:**
| You/Them | Cooperate | Defect |
|----------|-----------|--------|
| Cooperate | 3,3 | 0,5 |
| Defect | 5,0 | 1,1 |

**Objective:** Discover that Tit-for-Tat (cooperate first, then copy opponent) often wins tournaments.

---

## 25. Newcomb's Paradox

**File:** `newcombs_paradox.py`

**Concept:** A perfect predictor vs free will. One box or two boxes?

**How to Play:**
- Box A: Transparent, contains $1,000
- Box B: Opaque, contains $1M or $0
- Predictor fills Box B based on what you'll choose
- If predictor thinks you'll take both: Box B is empty
- If predictor thinks you'll take only B: Box B has $1M

**Objective:** Decide whether to one-box (trust the predictor) or two-box (maximize causal outcomes).

---

## 26. Pascal's Wager

**File:** `pascals_wager.py`

**Concept:** Decision theory about belief. The expected value of believing in God.

**How to Play:**
- Assign probabilities to God's existence
- Calculate expected outcomes for belief/non-belief
- Factor in infinite reward/punishment
- See how infinity breaks normal decision theory

**Objective:** Explore whether rational self-interest can justify belief.

---

## 27. Monty Hall

**File:** `monty_hall.py`

**Concept:** Counter-intuitive probability. Switching doors DOUBLES your odds.

**How to Play:**
- 3 doors: 1 car, 2 goats
- Pick a door
- Host reveals a goat behind another door
- Choose: Stay or Switch?
- Play multiple rounds to see statistics

**Objective:** Empirically verify that switching wins 2/3 of the time. Trust the math over intuition.

**The Math:**
- Initial pick: 1/3 chance of car
- Switching: 2/3 chance of car
- Host's reveal gives you information!

---

## 28. Sleeping Beauty

**File:** `sleeping_beauty.py`

**Concept:** Probability and self-location. What should Sleeping Beauty believe?

**Setup:**
- Coin flip: Heads or Tails
- Heads: Wake once (Monday)
- Tails: Wake twice (Monday and Tuesday, memory erased between)
- When awakened: "What's the probability the coin was Heads?"

**How to Play:**
- Experience the scenario from Beauty's perspective
- Choose your credence (1/2 or 1/3)
- Explore the "halfer" vs "thirder" debate

**Objective:** Understand how self-location affects probability calculations.

---

# Other Paradox Games

## 29. Garden of Forking Paths

**File:** `forking_paths.py`

**Concept:** Branching narratives. Every choice creates a new path.

**How to Play:**
- Read story segments
- Make choices at decision points
- Explore different branches
- See how narratives diverge

**Objective:** Experience non-linear storytelling. Every path is equally "real."

---

## 30. Bootstrap Paradox

**File:** `bootstrap_paradox.py`

**Concept:** Information with no origin. Objects that create themselves through time loops.

**How to Play:**
- Find a book in 2024
- Travel to 1600
- Give book to Shakespeare
- He publishes it
- Centuries later, you read it and travel back...

**Objective:** Experience causal loops. Where did the book ORIGINALLY come from? Nowhere!

---

## 31. Boltzmann Brains

**File:** `boltzmann_brains.py`

**Concept:** Statistical mechanics gone cosmic. Random fluctuations could create conscious brains.

**How to Play:**
- Watch entropy fluctuations
- See how random arrangements occasionally form ordered structures
- Consider: are you a real human or a Boltzmann Brain that just fluctuated into existence?

**Objective:** Question the reliability of memory and experience. Statistical mechanics has weird implications.

---

## 32. Simulation Hypothesis

**File:** `simulation_hypothesis.py`

**Concept:** Are we living in a computer simulation?

**How to Play:**
- Explore a world that may or may not be "base reality"
- Look for glitches and inconsistencies
- Consider the statistical argument: most minds might be simulated
- Test the boundaries of your reality

**Objective:** Question the nature of existence. If we're simulated, does it matter?

---

## 33. Doomsday Argument

**File:** `doomsday_argument.py`

**Concept:** Probability and human extinction. You're probably not among the first humans ever.

**How to Play:**
- Consider your birth rank (you're roughly human #100 billion)
- Apply the Copernican principle (you're not special)
- Calculate when humanity might end
- Grapple with the implications

**Objective:** Understand how self-location affects predictions about the future.

---

## 34. Munchhausen Trilemma

**File:** `munchhausen_trilemma.py`

**Concept:** The problem of justification. How do you justify your beliefs?

**How to Play:**
- Try to justify a statement
- Justify THAT justification
- Three possible outcomes:
  1. Infinite regress (justifications never end)
  2. Circular reasoning (A justifies B justifies A)
  3. Axiomatic foundation (accept something without proof)

**Objective:** See why epistemology is hard. Knowledge needs foundations, but where do they come from?

---

## 35. Braess's Paradox

**File:** `braess_paradox.py`

**Concept:** Adding roads can make traffic WORSE. Counter-intuitive network effects.

**How to Play:**
- Manage a road network
- Add new roads to reduce congestion
- Watch travel times... increase?
- Experience the paradox of choice in networks

**Objective:** Understand why individual optimization doesn't equal system optimization.

---

# Running Games

All games can be run directly from the command line:

```bash
# Navigate to the Claude directory
cd /home/user/Claude

# Run any game
python3 <game_file>.py

# Examples:
python3 vault_shelter_v6.py      # Main game
python3 trolley_problem.py       # Trolley Problem
python3 schrodingers_dungeon.py  # Schrodinger's Dungeon
python3 chinese_room.py          # Chinese Room
```

# Tips for All Games

1. **Read the introduction** - Each game explains its philosophical concept
2. **Take your time** - These are thought experiments, not action games
3. **Reflect on choices** - The goal is understanding, not winning
4. **Play multiple times** - Different choices reveal different insights
5. **Discuss with others** - Philosophy is better as conversation

---

# Quick Reference: Games by Difficulty

## Beginner-Friendly
- Monty Hall (simple probability)
- Plato's Cave (visual narrative)
- Bootstrap Paradox (short time-loop story)
- Prisoner's Dilemma (classic game theory)

## Intermediate
- Trolley Problem (ethics with consequences)
- Chinese Room (AI philosophy)
- Schrodinger's Dungeon (quantum + gameplay)
- VAULT 13 Main Game (resource management)

## Advanced
- Halting Problem (requires CS background)
- Godel's Paradox (mathematical logic)
- Echo Chambers (complex multi-timeline)
- Sleeping Beauty (probability paradox)

---

*Enjoy exploring these philosophical games! Each one offers a unique perspective on deep questions about reality, knowledge, ethics, and existence.*
