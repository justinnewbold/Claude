# 🚀 VAULT 13 v4.0 ULTIMATE EDITION - Feature Guide

**The Ultimate Vault Management Experience**

---

## 🎯 What's New in v4.0

VAULT 13 v4.0 Ultimate Edition is the most feature-rich version yet, combining:
- **All v3.0 AI features** (Advisor, Dialogue, Natural Language)
- **All v2.0 core features** (Rush, Upgrades, Combat, Equipment)
- **5 Brand New Game-Changing Features** (Quests, Exploration, Skills, Objectives, Adjacency)

This is a **2,434-line mega-game** that transforms the vault sim into an RPG-strategy hybrid with AI-powered storytelling.

---

## 🆕 The 5 New Features

### 1. 📜 AI Quest Generator

**What it is:** Procedurally generated multi-turn story quests created by AI based on your vault's current state.

**How to use:**
- Press `[Q]` to view active quests
- Quests appear randomly or can be generated on-demand (with AI enabled)
- Complete quest steps to earn rewards

**Example Quest:**
```
Quest: "The Water Crisis"
Description: A contamination event threatens your water supply. Act fast!

Steps:
1. Accumulate 100 water units
2. Build a new Water Treatment facility
3. Assign a dweller with Perception 7+

Rewards: 300 caps, +1 Science Lab blueprint
```

**Features:**
- 2-4 step quests with varied objectives
- Context-aware generation (AI considers your vault's situation)
- Rewards include caps, equipment, and special bonuses
- Track up to 3 quests simultaneously
- Quest log with progress tracking

**Cost:** AI quests use ~200-300 tokens (~$0.001 per quest)

---

### 2. 🏜️ Wasteland Expeditions

**What it is:** Send idle dwellers on time-based expeditions to explore the wasteland for loot and experience.

**How to use:**
- Press `[X]` to open the expeditions menu
- Select an idle dweller
- Choose destination (Nearby Ruins, Military Base, etc.)
- Wait for them to return with loot or injuries

**Destinations:**
| Name | Duration | Difficulty | Potential Loot |
|------|----------|------------|----------------|
| Nearby Ruins | 2 days | 3/10 | 150-600 caps |
| Old Supermarket | 3 days | 5/10 | 250-1000 caps |
| Military Base | 5 days | 7/10 | 350-1400 caps, weapons |
| Distant City | 7 days | 10/10 | 500-2000 caps, rare items |

**Success Calculation:**
```
Base Success = 100 - (Difficulty × 8)
+ Dweller's (Endurance + Luck + Perception) / 3 × 5
+ Wasteland Survivor skill: -25% duration
+ Scavenger skill: +50% loot
```

**Features:**
- Dwellers gain experience on successful returns
- 30% chance to find rare equipment
- Failed expeditions result in injury
- Integrates with Exodus victory objective
- Shows countdown timers for active expeditions

**Strategy Tips:**
- High Endurance/Perception/Luck = better survival
- Equip weapons for harder expeditions
- Learn Wasteland Survivor skill to reduce time
- Scavenger skill dramatically increases loot

---

### 3. ⭐ Dweller Skills & Progression

**What it is:** An RPG-style progression system where dwellers can learn powerful skills after meeting SPECIAL stat requirements.

**How to use:**
- Press `[K]` to open the skills menu
- Select a dweller
- View available skills (based on their stats)
- Learn skills instantly if requirements are met

**9 Learnable Skills:**

**Production Skills:**
- ⚡ **Power Expert** - +30% power production
  - Requires: STR 6, INT 5
- 💧 **Water Purifier** - +30% water production
  - Requires: PER 6, INT 5
- 🍖 **Master Chef** - +30% food production
  - Requires: AGI 6, CHA 5

**Combat Skills:**
- 🎯 **Sharp Shooter** - +50% weapon damage
  - Requires: PER 7, AGI 6
- 🛡️ **Tank** - -30% damage taken
  - Requires: STR 7, END 7

**Exploration Skills:**
- 🏜️ **Wasteland Survivor** - -25% expedition time
  - Requires: END 6, LCK 6
- 🔍 **Scavenger** - +50% expedition loot
  - Requires: PER 6, LCK 7

**Utility Skills:**
- 👑 **Leader** - +10% happiness to nearby dwellers
  - Requires: CHA 8, INT 6
- ⚕️ **Medic** - Faster healing, can treat others
  - Requires: INT 7, CHA 5

**Progression System:**
- Dwellers gain XP from expeditions, combat, and work
- Level up every 100 XP
- Higher levels unlock more skills
- Skills are permanent once learned

**Example Build:**
```
Sarah Johnson
Level 5 | 380 XP
SPECIAL: S:7 P:8 E:6 C:5 I:6 A:4 L:7
Skills: Water Purifier, Scavenger, Wasteland Survivor

Perfect for: Expeditions + Water Production
```

---

### 4. 🎯 Vault Objectives (Victory Conditions)

**What it is:** Choose your win condition! Five different paths to victory, each requiring a unique strategy.

**How to use:**
- Press `[O]` to view objectives
- See progress toward current objective
- Change objective anytime

**The 5 Victory Conditions:**

#### 🕊️ Survival (Default)
**Goal:** Survive 100 days in the wasteland
**Progress:** Day 45/100
**Strategy:** Balanced resource management, defensive play
**Difficulty:** Medium

#### 🌟 Utopia
**Goal:** Achieve perfect vault (10+ dwellers, all 90+ happiness)
**Progress:** 8 dwellers, avg 72% happiness
**Strategy:** Focus on happiness-boosting rooms (Medbay, Training)
**Difficulty:** Hard

#### 💰 Economic Dominance
**Goal:** Accumulate 10,000 caps
**Progress:** 2,450 / 10,000 caps
**Strategy:** Maximize production, send constant expeditions
**Difficulty:** Medium

#### ⚔️ Military Fortress
**Goal:** 15 armed and trained dwellers
**Progress:** 6/15 armed
**Strategy:** Equipment farming, combat training
**Difficulty:** Medium-Hard

#### 🚀 Exodus
**Goal:** Complete 10 successful wasteland expeditions
**Progress:** 3/10 completed
**Strategy:** High-risk expeditions with skilled explorers
**Difficulty:** Hard

**Features:**
- Real-time progress tracking in main UI
- Switch objectives without penalty
- Multiple completions tracked
- Objectives integrate with game systems

---

### 5. ✨ Room Adjacency & Synergy Bonuses

**What it is:** Strategic room placement matters! Certain room combinations provide production bonuses and benefits.

**How it works:**
- Rooms adjacent horizontally receive bonuses
- Bonuses are calculated automatically
- Bonus indicators appear as ✨ on rooms

**Adjacency Bonuses:**

**Same-Type Clustering (+15% production):**
- ⚡ Power Generator + ⚡ Power Generator = "Power Grid"
- 💧 Water Treatment + 💧 Water Treatment = "Water Network"
- 🍖 Diner + 🍖 Diner = "Kitchen Complex"

**Synergistic Combinations:**
- 🔬 Science Lab + ⚡ Power Generator = +10% production ("Research Power")
- ⚕️ Medbay + 🏠 Living Quarters = +5 happiness ("Healthcare Access")
- 💪 Training Room + 🏠 Living Quarters = +3 happiness ("Fitness Center")
- 📦 Storage Room + 🍖 Diner = +10% production ("Kitchen Storage")

**Strategic Planning:**
```
GOOD Layout (Floor 1):
[⚡ Power I ✨] [⚡ Power I ✨] [🔬 Science]
+15% bonus      +25% bonus!    +10% bonus

BAD Layout (Floor 1):
[⚡ Power I] [🏠 Living] [💧 Water I]
No bonuses - rooms don't synergize
```

**Example Production Math:**
```
Base: Power Generator Lvl 1 = 5 power/turn
Workers: 2 dwellers with STR 7 = ×1.4 multiplier
Room Level: Level 1 = ×1 multiplier
Adjacency: Next to another Power Gen = +15%

Total: 5 × 1.4 × 1.0 × 1.15 = 8 power/turn (instead of 7)
```

**Tips:**
- Plan your vault layout before building
- Group production rooms by type
- Place Living Quarters near Medbay/Training
- Storage Rooms help nearby production rooms

---

## 🔄 How v4.0 Features Work Together

### Example Gameplay Loop:

**Day 25:**
1. Check active quest: "Equip the Militia" (arm 5 dwellers)
2. Send Sarah (Scavenger skill) on Military Base expedition
3. While waiting, train John's stats to unlock Sharp Shooter skill
4. Build second Diner next to first for Kitchen Complex bonus
5. Switch objective to Military Fortress

**Day 28:**
6. Sarah returns with Laser Rifle and 850 caps!
7. Equip rifle to John
8. John levels up, learns Sharp Shooter (+50% weapon damage)
9. Quest progresses: 3/5 dwellers armed
10. Use AI Advisor to plan next steps

**Day 32:**
11. Complete quest, earn 400 caps reward
12. AI generates new quest: "The Exodus Begins"
13. Use caps to build Training Room
14. Place Training Room next to Living Quarters (+3 happiness bonus)
15. All dwellers hit 85% happiness

This creates a **virtuous cycle** where:
- Expeditions provide loot → Enables skills → Improves production
- Quests give direction → Complete objectives → Unlock more quests
- Skills multiply effectiveness → Better expeditions → More resources
- Strategic building → Adjacency bonuses → Faster progression

---

## 📊 v4.0 Complete Feature Matrix

| Feature | v2.0 | v3.0 AI | v4.0 Ultimate |
|---------|------|---------|---------------|
| Resource Management | ✓ | ✓ | ✓ |
| Room Building | ✓ | ✓ | ✓ |
| Rush Production | ✓ | ✓ | ✓ |
| Room Upgrades (1-3) | ✓ | ✓ | ✓ |
| Combat System | ✓ | ✓ | ✓ |
| Equipment (Weapons/Outfits) | ✓ | ✓ | ✓ |
| Smart Rationing | ✓ | ✓ | ✓ |
| Enhanced Graphics | ✓ | ✓ | ✓ |
| AI Overseer Advisor | - | ✓ | ✓ |
| Dweller Personalities | - | ✓ | ✓ |
| AI Dialogue Generation | - | ✓ | ✓ |
| Natural Language Commands | - | ✓ | ✓ |
| **AI Quest Generator** | - | - | ✓ NEW |
| **Wasteland Expeditions** | - | - | ✓ NEW |
| **Dweller Skills (9 skills)** | - | - | ✓ NEW |
| **Victory Objectives (5 types)** | - | - | ✓ NEW |
| **Room Adjacency Bonuses** | - | - | ✓ NEW |
| **XP & Leveling System** | - | - | ✓ NEW |
| Lines of Code | 1,736 | 1,007 | 2,434 |

---

## 🎮 v4.0 Controls Reference

### Main Menu
- `[B]` Build Room
- `[U]` Upgrade Room
- `[H]` Rush Production
- `[D]` Manage Dwellers (heal, unassign)
- `[R]` Assign Workers
- `[I]` Fight Incident
- `[G]` Manage Equipment
- `[V]` View Details
- `[E]` End Turn
- `[S]` Save Game
- `[Z]` Quit

### NEW v4.0 Features
- `[Q]` View Quests (v4.0)
- `[X]` Wasteland Expeditions (v4.0)
- `[K]` Learn Skills (v4.0)
- `[O]` Vault Objectives (v4.0)

### AI Features (if enabled)
- `[A]` AI Overseer Advisor
- `[T]` Talk to Dweller
- `[N]` Toggle Natural Language Mode

---

## 💡 Strategy Guide for v4.0

### Early Game (Days 1-20)

**Priorities:**
1. Assign all idle dwellers to production
2. Build a Diner (critical for food)
3. Focus on Survival objective initially
4. Don't send expeditions until dwellers are equipped

**Skill Strategy:**
- Train dwellers to 6+ in their job stat
- Aim for production skills first (Power Expert, etc.)
- Save combat skills for later

**Room Layout:**
```
Floor 1: [⚡Power][⚡Power][💧Water]  ← Build Power Gen first
Floor 2: [🏠Living][🍖Diner][Empty]
Floor 3: [Empty][Empty][Empty]
```

### Mid Game (Days 21-60)

**Priorities:**
1. Switch to Economic or Exodus objective
2. Start expeditions to Nearby Ruins
3. Upgrade Level 1 rooms to Level 2
4. Cluster production rooms for adjacency bonuses

**Skill Strategy:**
- Get Wasteland Survivor on explorers
- Get Scavenger on high-Luck dwellers
- Production skills on dedicated workers

**Expedition Strategy:**
- Only send idle dwellers
- Start with low difficulty (2-3)
- Equip weapons before harder expeditions
- Track return dates

### Late Game (Days 61-100)

**Priorities:**
1. Complete active quests for rewards
2. Push toward chosen victory objective
3. Send Military Base/City expeditions
4. Build Science Labs if not already done

**Skill Strategy:**
- Diversify - get Leader, Medic, Tank
- Max out combat skills for hard content
- Leader dwellers boost vault happiness

**Victory Push:**
- **Survival:** Just survive, maintain resources
- **Utopia:** Heal everyone, maximize happiness
- **Economic:** Non-stop expeditions
- **Military:** Farm equipment, arm everyone
- **Exodus:** Skilled explorers to dangerous locations

---

## 🔬 Advanced Mechanics

### Production Formula (v4.0)
```python
Production = Base × Level × Workers × StatMult × SkillMult × AdjacencyMult

Where:
- Base = Room's base production (5 for Power Gen)
- Level = Room level (1-3)
- Workers = 1 + (worker_count × 0.2)
- StatMult = avg_worker_stat / 5
- SkillMult = 1 + skill_bonuses (e.g., 1.3 with Power Expert)
- AdjacencyMult = 1 + adjacency_bonuses (e.g., 1.15 with neighbor)
```

**Example:**
```
Level 2 Power Generator
2 workers: STR 8, STR 6 (avg 7)
One worker has Power Expert skill
Adjacent to another Power Gen

Production = 5 × 2 × 1.4 × 1.4 × 1.3 × 1.15
           = 5 × 2 × 1.4 × 1.4 × 1.3 × 1.15
           = ~29 power/turn

vs. v2.0: 5 × 2 × 1.4 × 1.4 = 19 power/turn
```

**Skills amplify production by 53%!**

### Expedition Success Formula
```python
Success% = BASE + (SurvivalScore × 5)
Where:
- BASE = 100 - (Difficulty × 8)
- SurvivalScore = (END + LCK + PER) / 3

Modifiers:
- Scavenger: Loot × 1.5
- Wasteland Survivor: Duration × 0.75
- Weapon equipped: +10% success
```

**Example:**
```
Military Base (Difficulty 7)
Dweller: END 6, LCK 7, PER 8 = SurvivalScore 7

Success = (100 - 56) + (7 × 5) = 44 + 35 = 79%

With Wasteland Survivor:
Duration: 5 days → 4 days
```

### XP & Leveling
```
XP Sources:
- Expedition (success): Difficulty × 20
- Combat (win): 10 XP
- Work (per turn): 1 XP
- Quest completion: 50-100 XP

Level Requirements:
- Level 2: 100 XP
- Level 3: 200 XP (cumulative: 300)
- Level 4: 300 XP (cumulative: 600)
- etc.
```

---

## 🤖 AI Integration (Same as v3.0)

v4.0 includes all v3.0 AI features with full integration:
- Quest generation uses AI for unique stories
- Advisor now considers quests, expeditions, and objectives
- Dweller dialogue references their skills and level
- Natural language can trigger new features: "send john on expedition"

**Cost Estimate for v4.0:**
- Same base cost as v3.0: ~$0.02/hour
- Quest generation: +$0.001 per quest
- **Total: ~$0.025/hour** (2.5 cents)

---

## 📝 Save System

v4.0 uses `vault_save_v4.json` (separate from v2.0/v3.0 saves):
- Saves all new features (quests, expeditions, skills, objectives)
- Compatible with all game modes
- Auto-backup on quit

---

## 🎯 Achievement Ideas (Future v5.0?)

Suggested achievements players can track manually:

- **🏆 Skill Master**: Learn all 9 skills on a single dweller
- **🏆 Wasteland Legend**: Complete 50 successful expeditions
- **🏆 Collector**: Find all equipment types
- **🏆 Perfect Synergy**: Build a vault with 10+ adjacency bonuses active
- **🏆 Quest Hero**: Complete 25 AI-generated quests
- **🏆 Five Ways to Win**: Complete all 5 victory objectives
- **🏆 Day 200 Club**: Survive 200 days
- **🏆 Utopia Architect**: Achieve 100% happiness on all dwellers

---

## 🚀 What's Next?

Potential v5.0 features (not yet implemented):
- **Multiplayer Vaults**: Compete or cooperate with other players
- **Vault Policies**: Choose government type (Democracy, Autocracy, etc.)
- **Breeding System**: Dwellers can have children with inherited stats
- **Tech Tree**: Research unlocks new room types and bonuses
- **Seasonal Events**: Holidays, disasters, special challenges
- **Voice Mode**: Speak commands aloud (speech-to-text)
- **Dweller Relationships**: Friendships, rivalries, romances tracked by AI

---

## 💻 Technical Details

**File:** `vault_shelter_v4.py`
**Lines:** 2,434
**Dependencies:** Python 3.7+, anthropic (optional)
**Save Format:** JSON (`vault_save_v4.json`)
**Platform:** Cross-platform (Linux, macOS, Windows)

**New Data Structures:**
- `Quest` - AI-generated quest with steps and rewards
- `Expedition` - Wasteland expedition with return timer
- `Skill` - Learnable ability with stat requirements
- `VaultObjective` - Victory condition with progress tracking
- `ADJACENCY_BONUSES` - Room synergy configuration

**Key Enhancements:**
- Extended `Dweller` class with `learned_skills`, `experience`, `level`, `on_expedition`
- Enhanced `Room.get_production()` with skill and adjacency multipliers
- New game loop integrations: `process_expedition_returns()`, quest tracking
- Comprehensive menu system for all new features

---

## 🎓 Conclusion

VAULT 13 v4.0 Ultimate Edition represents the **pinnacle of terminal-based vault simulation**, combining:
- Deep strategy (adjacency, skills, objectives)
- AI-powered storytelling (quests, dialogue, advisor)
- RPG progression (leveling, skills, equipment)
- Exploration mechanics (expeditions, loot, risk/reward)
- Multiple victory paths (5 distinct objectives)

Whether you're a min-maxer optimizing production chains, a storyteller following AI-generated quests, or an explorer sending dwellers into the wasteland, v4.0 offers **hundreds of hours** of emergent gameplay.

**Welcome to the ultimate vault management experience, Overseer!** 🏛️⚡💧🍖

---

*For AI features documentation, see `AI_FEATURES.md`*
*For basic v2.0 mechanics, see `VAULT_SHELTER.md`*
