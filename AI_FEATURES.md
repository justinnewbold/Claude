# 🤖 VAULT 13 - AI FEATURES GUIDE

## Overview

VAULT 13 v3.0 AI Edition integrates three powerful AI features that transform the vault management experience from a strategy game into a living, breathing world with personality and intelligence.

---

## 🚀 Quick Start

### Installation

```bash
# Install the Anthropic Python SDK
pip install anthropic

# Set your API key (get one at https://console.anthropic.com/)
export ANTHROPIC_API_KEY="your-api-key-here"

# Run the AI-enhanced game
python3 vault_shelter_ai.py
```

### Demo Mode

If you don't have an API key, the game runs in **demo mode** with fallback responses. All game mechanics work normally, but AI features show placeholder text.

---

## 🎯 The 3 AI Features

### 1. 🤖 AI Overseer Advisor [A key]

**What it does:** Analyzes your entire vault and provides strategic recommendations.

**How to use:**
1. Press `[A]` from the main menu
2. Either ask a specific question or press Enter for general analysis
3. Get detailed strategic advice with actionable recommendations

**Example Session:**
```
Your question: why is morale low?

ADVISOR REPORT:

⚠️  CRITICAL CONCERNS:
- Average dweller happiness is 42% (below healthy threshold of 60%)
- 2 dwellers (Sarah Johnson, Michael Brown) are idle with no work assignment
- John Smith has been at low health (35%) for 3+ days without treatment

💡 RECOMMENDATIONS:
1. Heal John Smith immediately (50 caps) - low health causes -5 happiness/turn
2. Assign Sarah to the empty Diner slot - she has Agility: 7 (excellent for food production)
3. Assign Michael to Power Generator - his Strength: 6 provides good bonus
4. Consider building a Medbay (150 caps) for passive healing

📊 LONG-TERM STRATEGY:
Focus on keeping all dwellers employed and healthy. Idle dwellers lose 3 happiness/turn.
```

**What the AI analyzes:**
- Current resource levels vs consumption
- Dweller assignments and idle workers
- Production efficiency and bottlenecks
- Health and happiness trends
- Recent events and their impact
- Optimal room placement and upgrades

**Cost:** ~$0.003 per query (~300 tokens)

---

### 2. 💬 Talk to Dwellers [T key]

**What it does:** Generates unique, context-aware dialogue for each dweller based on their personality, situation, and SPECIAL stats.

**How to use:**
1. Press `[T]` from the main menu
2. Select a dweller to talk to
3. AI generates dialogue that fits their personality and current situation

**Example Dialogues:**

```
Sarah Johnson (Pessimistic, Hardworking, Reserved, Cautious)
Health: 85% | Happiness: 45% | Assigned: Power Generator

Context: Working hard but unhappy

Sarah says:
"Sure, I'll keep the lights on while everyone else takes it easy.
At least the generator doesn't complain like some people around here."
```

```
John Smith (Optimistic, Lazy, Charismatic, Reckless)
Health: 100% | Happiness: 80% | Assigned: None

Context: Idle and loving it

John says:
"Why rush? The vault's been standing for 200 years, it can wait another day
for me to finish my nap. Besides, I do my best thinking horizontally!"
```

```
Emma Williams (Pragmatic, Ambitious, Friendly, Brave)
Health: 65% | Happiness: 70% | Equipped: Laser Rifle, Scientist Coat

Context: Well-equipped and confident

Emma says:
"With this laser rifle and my new coat, I feel ready for anything the wasteland
throws at us. Let's go find some trouble - for science!"
```

**Personality System:**

Each dweller has 4 personality traits:
- **Outlook**: Optimistic, Pessimistic, Pragmatic, Cynical
- **Work Ethic**: Hardworking, Lazy, Ambitious, Laid-back
- **Social**: Friendly, Reserved, Charismatic, Awkward
- **Courage**: Brave, Cautious, Reckless, Cowardly

The AI uses these traits to generate authentic, consistent dialogue that makes each dweller feel like a real character.

**Dynamic Context Awareness:**

Dialogue changes based on:
- Health (injured dwellers mention pain)
- Happiness (unhappy dwellers complain or threaten to leave)
- Job assignment (workers talk about their duties)
- Equipment (armed dwellers feel confident)
- Recent events (fire survivors mention the trauma)

**Cost:** ~$0.0004 per dialogue (~100 tokens)

---

### 3. 💬 Natural Language Commands [N key]

**What it does:** Lets you control the vault by typing commands in plain English instead of navigating menus.

**How to use:**
1. Press `[N]` to toggle Natural Language mode
2. Type commands naturally
3. AI parses your intent and executes actions
4. Type 'menu' to return to normal controls

**Example Commands:**

```
💬 > assign sarah to power generator
✓ Assigning Sarah Johnson to Power Generator on Floor 1...
  Her Strength (7) will boost production by 40%!

💬 > what's my food situation?
📊 Food Analysis:
   Current: 18/30 (60% capacity)
   Production: +7/turn (1 Diner, Level 1, 2 workers)
   Consumption: -4/turn (4 dwellers)
   Net: +3/turn (stable but could be better)

   Suggestion: Upgrade Diner to Level 2 (150 caps) for +50% production

💬 > rush the diner
⚡ Initiating rush in Diner...
   Workers: Alex (Luck: 6), Taylor (Luck: 5)
   Success chance: 75%

   Rolling... SUCCESS! ✨
   Produced: 21 food
   Bonus: 35 caps
   Rush cooldown: 3 turns

💬 > give sarah the laser rifle
✓ Equipped Laser Rifle ⚡ to Sarah Johnson
  Combat power: 7 → 22 (+15 from weapon)

💬 > upgrade water treatment
✓ Upgrading Water Treatment to Level 2
  Cost: 180 caps
  New production: 10 water/turn (was 5)

💬 > who should I assign to the science lab?
🤖 Based on SPECIAL stats, Emma Williams is ideal for the Science Lab.
   Her Intelligence (8) is highest among unassigned dwellers.
   This will maximize research efficiency.

💬 > menu
✓ Returning to menu mode.
```

**Supported Commands:**
- **Assignments**: "assign [dweller] to [room]"
- **Building**: "build a [room type]", "construct water treatment"
- **Upgrading**: "upgrade [room]", "level up diner"
- **Rushing**: "rush [room]", "rush production in power generator"
- **Equipment**: "equip [item] to [dweller]", "give [dweller] [item]"
- **Status**: "check [resource]", "how much food do I have?", "show power status"
- **Strategy**: "what should I build?", "who should I assign where?"
- **Turn**: "end turn", "next day", "advance time"

**Smart Parsing:**

The AI understands:
- Synonyms ("build" = "construct" = "create")
- Partial names ("sarah" = "Sarah Johnson")
- Context ("the diner" refers to your existing Diner)
- Questions vs commands
- Ambiguous requests (asks for clarification)

**Cost:** ~$0.0005 per command (~150 tokens)

---

## 💰 Cost Analysis

Using **Claude 3.5 Sonnet** (recommended model):

| Feature | Tokens In | Tokens Out | Cost per Use |
|---------|-----------|------------|--------------|
| Advisor Analysis | ~500 | ~300 | $0.0025 |
| Dweller Dialogue | ~50 | ~50 | $0.0004 |
| NL Command Parse | ~150 | ~50 | $0.0005 |

**Typical 1-hour gameplay session:**
- 3 Advisor queries: $0.0075
- 15 Dweller dialogues: $0.006
- 20 NL commands: $0.01

**Total:** ~$0.024/hour = **2.4 cents per hour!**

### Monthly Cost Estimates

| Usage Level | Hours/Month | Monthly Cost |
|-------------|-------------|--------------|
| Casual | 10 hours | $0.24 |
| Regular | 40 hours | $0.96 |
| Heavy | 100 hours | $2.40 |

**Conclusion:** AI features are incredibly affordable, costing less than a cup of coffee per month even for heavy users.

---

## 🛠️ Technical Implementation

### Architecture

```python
# AI Integration Layer
vault_shelter_ai.py
├── AI Helper Functions
│   ├── call_ai_model() - Main API interface
│   ├── get_dweller_dialogue() - Personality-aware dialogue
│   ├── get_advisor_analysis() - Strategic analysis
│   └── parse_natural_language_command() - Command parsing
│
├── Graceful Fallback
│   ├── AI_ENABLED flag (checks for API key)
│   └── generate_fallback_response() - Demo mode responses
│
└── Enhanced Game Class
    ├── ai_advisor_menu() - [A] menu
    ├── talk_to_dweller_menu() - [T] menu
    ├── natural_language_mode() - [N] toggle
    └── process_nl_command() - NL parser
```

### API Integration

```python
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def call_ai_model(prompt, max_tokens=500, system_prompt=""):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

### Prompt Engineering Examples

**Dweller Dialogue Prompt:**
```
Generate a short, in-character comment (1-2 sentences max) for this Fallout-style vault dweller.

Dweller: Sarah Johnson
Personality: Pessimistic, Hardworking, Reserved, Cautious
Health: 85% | Happiness: 45%
SPECIAL Stats: S:7 P:5 E:6 C:4 I:5 A:6 L:5
Assigned: Yes - Power Generator

Context: Working hard but unhappy

Generate a witty, Fallout-themed comment that fits their personality.
Keep it brief and natural. No quotes, just the dialogue.
```

**Advisor Prompt:**
```
You are the AI Overseer Advisor for Vault 13. Analyze this vault
and provide strategic advice.

Vault State:
{detailed JSON of resources, dwellers, rooms, events}

Player Question: "why is morale low?"

Give concise, actionable advice in this format:
⚠️  CRITICAL CONCERNS: (immediate threats)
💡 RECOMMENDATIONS: (2-3 specific actions)
📊 LONG-TERM STRATEGY: (1 sentence)

Be specific with numbers and dweller names.
```

---

## 🎮 Gameplay Tips with AI

### 1. Use the Advisor Strategically

**Early Game:**
- Ask: "What should I build next?"
- The AI considers your caps, dweller count, and production needs

**Mid Game:**
- Ask: "How can I improve efficiency?"
- Get specific recommendations on room upgrades and worker optimization

**Crisis:**
- Ask: "Help! My vault is failing!"
- Get emergency triage advice

### 2. Build Emotional Connections

Talk to dwellers regularly, especially:
- After they survive dangerous events
- When they've been idle too long
- After major achievements (reaching 100% happiness)
- Before risky missions

Their unique personalities make them memorable!

### 3. Natural Language for Speed

Common repetitive tasks are faster in NL mode:
- Assigning multiple new arrivals
- Checking status of all resources
- Quick equipment swaps
- Batch operations

**Example NL workflow:**
```
💬 > assign alex to diner
💬 > assign morgan to water
💬 > assign casey to power
💬 > check all resources
💬 > end turn
```

vs. navigating menus 5 separate times.

---

## 🔒 Privacy & Security

### What Data is Sent?

**To Anthropic API:**
- Game state (resources, dweller stats, rooms)
- Your questions/commands
- Recent event log (last 3-5 events)

**NOT sent:**
- Your system information
- Personal data
- Save game files (except temporarily during queries)

### API Key Security

```bash
# Store securely in environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Or use .env file (gitignored)
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Load in game
from dotenv import load_dotenv
load_dotenv()
```

**NEVER commit API keys to git!**

---

## 🐛 Troubleshooting

### "AI Features: DISABLED"

**Cause:** Missing API key or anthropic library

**Solution:**
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

### "AI Error: Authentication failed"

**Cause:** Invalid or expired API key

**Solution:** Get a new key from https://console.anthropic.com/

### "AI taking too long to respond"

**Cause:** Network issues or high API load

**Solution:**
- Check internet connection
- Try again in a moment
- Game continues to work, AI is non-blocking

### "Dialogue doesn't match dweller personality"

**Cause:** Random variation in AI responses

**Solution:** This is normal! AI generates creative responses. If consistently off, the dweller's personality traits might need adjustment.

---

## 🔮 Future AI Enhancements

Planned for v4.0:

1. **Multi-Turn Quests** - AI generates entire quest chains with choices
2. **Voice Mode** - Speak commands aloud (using speech-to-text)
3. **Dweller Relationships** - AI tracks friendships, rivalries, romances
4. **Procedural Events** - Entirely AI-generated random events
5. **Smart Automation** - "Auto-assign dwellers optimally"
6. **Visual Dialogue Trees** - Branching conversations with dwellers
7. **Multiplayer Advisor** - Compare your vault to others, get personalized tips

---

## 📊 Comparison: v2.0 vs v3.0 AI

| Feature | v2.0 (Standard) | v3.0 AI Edition |
|---------|----------------|-----------------|
| Strategic Help | Manual learning | AI Advisor analyzes and recommends |
| Dweller Personality | Generic | Unique AI-generated traits |
| Dialogue | None | Context-aware, personality-driven |
| Controls | Menu-based only | Menu + Natural Language |
| Learning Curve | Steep | Gentler (AI teaches you) |
| Replayability | High | Higher (every dweller unique) |
| Immersion | Good | Excellent (living characters) |
| Cost | Free | ~$0.02/hour of play |

---

## 🎯 Best Practices

### For New Players

1. **Start with the Advisor** - Press [A] and ask "what should I do first?"
2. **Talk to dwellers** - Press [T] to understand personalities
3. **Use NL mode for learning** - Type "how do I [action]?" to get guidance

### For Experienced Players

1. **Use NL for speed** - Assign workers, check status, manage equipment
2. **Ask tactical questions** - "Should I rush this room?" "Who should fight this fire?"
3. **Get second opinions** - "I'm planning to build X, thoughts?"

### For Roleplayers

1. **Check in with dwellers daily** - Build storylines around their personalities
2. **Ask ethical questions** - "Who should get the limited medical supplies?"
3. **Create narrative** - Ask AI to describe events dramatically

---

## 📝 Example Full Session

```
Day 15 - Morning

[A] AI Advisor
> "what should I prioritize today?"

⚠️  CRITICAL: Water at 8/30 (27%), consumption exceeds production
💡 RECOMMENDATIONS:
1. Build second Water Treatment immediately (120 caps available)
2. Assign Emma (Perception: 8) once built
3. Consider rushing existing Water Treatment (68% success chance)

[T] Talk to Emma
> Select: Emma Williams

Emma Williams:
"I've been studying the water filtration systems. With my expertise,
I could run a second plant easily. Just saying, Overseer."

[N] Natural Language Mode
> "build water treatment at floor 2 position 2"
✓ Built Water Treatment on Floor 2

> "assign emma to new water treatment"
✓ Emma assigned! Her Perception (8) will provide 60% production bonus!

> "check water status now"
📊 Water: Production now 12/turn, consumption 4/turn
   Status: RECOVERING - will reach safe levels in 3 turns

> "thanks emma"
[T] Emma Williams:
"Just doing my job, boss. Though a bonus wouldn't hurt!"
*she grins*

[E] End Turn
✓ Day 16 begins...
```

---

## 🎓 Conclusion

The AI features in VAULT 13 v3.0 transform the game from a management sim into an immersive experience with living characters and intelligent guidance. Whether you're seeking strategic help, character-driven storytelling, or just a more natural way to play, these features enhance every aspect of vault life.

**Cost:** Pennies per hour
**Value:** Infinite

Welcome to the future of vault management, Overseer! 🤖

---

*For more information, visit the [Anthropic Documentation](https://docs.anthropic.com/)*
