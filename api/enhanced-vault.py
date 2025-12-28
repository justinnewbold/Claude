"""
VAULT 13 - Enhanced Edition
Complete implementation of all game improvements:
- Interactive Tutorial System
- Visual Stat Feedback
- Clearer Resource Warnings
- Smart Command Shortcuts
- Contextual Help System
- Story-Driven Quests
- Dweller Personalities
- Achievement System
- Daily Challenges
- Dynamic Branching Events
- Relationship Mechanics
- Visual Progress Milestones
- Interactive Expedition Mini-Game
- Prestige System (New Game+)
"""

import random
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class PersonalityTrait(Enum):
    # Outlook
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    PRAGMATIC = "pragmatic"
    CYNICAL = "cynical"

    # Work Ethic
    HARDWORKING = "hardworking"
    LAZY = "lazy"
    AMBITIOUS = "ambitious"
    LAID_BACK = "laid-back"

    # Social
    FRIENDLY = "friendly"
    RESERVED = "reserved"
    CHARISMATIC = "charismatic"
    AWKWARD = "awkward"

    # Courage
    BRAVE = "brave"
    CAUTIOUS = "cautious"
    RECKLESS = "reckless"
    COWARDLY = "cowardly"

@dataclass
class Dweller:
    name: str
    strength: int
    perception: int
    endurance: int
    charisma: int
    intelligence: int
    agility: int
    luck: int
    health: int = 100
    happiness: int = 70
    job: Optional[str] = None
    backstory: str = ""
    unique_trait: str = ""
    personality: Dict[str, str] = None
    relationships: Dict[str, int] = None  # name -> relationship score (-100 to 100)

    def __post_init__(self):
        if self.personality is None:
            self.personality = {
                'outlook': random.choice(['optimistic', 'pessimistic', 'pragmatic', 'cynical']),
                'work_ethic': random.choice(['hardworking', 'lazy', 'ambitious', 'laid-back']),
                'social': random.choice(['friendly', 'reserved', 'charismatic', 'awkward']),
                'courage': random.choice(['brave', 'cautious', 'reckless', 'cowardly'])
            }
        if self.relationships is None:
            self.relationships = {}

    def get_stat_color(self, stat: int) -> str:
        """Return color code for stat visualization"""
        if stat >= 8:
            return "🟢"
        elif stat >= 5:
            return "🟡"
        else:
            return "🔴"

    def get_effectiveness(self, stat_name: str) -> Tuple[str, int]:
        """Calculate job effectiveness bonus"""
        stat = getattr(self, stat_name.lower())
        if stat >= 8:
            return "⭐⭐⭐ Excellent", (stat - 5) * 10
        elif stat >= 5:
            return "⭐⭐ Good", (stat - 5) * 10
        else:
            return "⭐ Poor", (stat - 5) * 10

@dataclass
class Quest:
    id: str
    name: str
    description: str
    unlock_day: int
    completed: bool = False
    rewards: Dict[str, int] = None
    choices: List[Dict] = None
    current_stage: int = 0

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    unlocked: bool = False
    bonus: Dict[str, Any] = None
    icon: str = "🏆"

@dataclass
class DailyChallenge:
    description: str
    goal_type: str
    goal_value: int
    reward: Dict[str, int]
    completed: bool = False

@dataclass
class Event:
    title: str
    description: str
    choices: List[Dict[str, Any]]

# ============================================================================
# DWELLER GENERATOR WITH PERSONALITIES AND BACKSTORIES
# ============================================================================

class DwellerGenerator:
    FIRST_NAMES = [
        "Marcus", "Sarah", "David", "Elena", "James", "Maya", "Robert", "Lisa",
        "John", "Emma", "Michael", "Sophia", "William", "Olivia", "Richard", "Ava"
    ]

    LAST_NAMES = [
        "Chen", "Rodriguez", "Johnson", "Kim", "Smith", "Patel", "Garcia", "Davis",
        "Martinez", "Brown", "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson"
    ]

    BACKSTORIES = [
        {
            "profession": "Former Doctor",
            "trait": "Fast Healer",
            "bonus": "heals 2x faster",
            "story": "Saved lives before the war. Now saves them in the vault."
        },
        {
            "profession": "Pre-War Engineer",
            "trait": "Tech Savvy",
            "bonus": "+20% power production",
            "story": "Built bridges between cities. Now builds hope underground."
        },
        {
            "profession": "Wasteland Scout",
            "trait": "Explorer",
            "bonus": "+30% expedition success",
            "story": "Wandered the wastes alone before finding safety here."
        },
        {
            "profession": "Chef",
            "trait": "Food Expert",
            "bonus": "+15% food production",
            "story": "Ran a five-star restaurant. Now makes the best of rations."
        },
        {
            "profession": "Teacher",
            "trait": "Mentor",
            "bonus": "+50% training speed",
            "story": "Educated children before the war. Still teaches hope."
        },
        {
            "profession": "Soldier",
            "trait": "Combat Ready",
            "bonus": "+2 damage in combat",
            "story": "Fought in the war. Now fights for survival."
        },
        {
            "profession": "Scientist",
            "trait": "Researcher",
            "bonus": "+25% research speed",
            "story": "Worked on Project Vault. Knows its secrets."
        },
        {
            "profession": "Farmer",
            "trait": "Green Thumb",
            "bonus": "+10% all production",
            "story": "Grew food for thousands. Every seed matters now."
        }
    ]

    @classmethod
    def generate(cls, special_dweller: bool = False) -> Dweller:
        """Generate a dweller with personality and backstory"""
        name = f"{random.choice(cls.FIRST_NAMES)} {random.choice(cls.LAST_NAMES)}"

        if special_dweller:
            # Special dwellers have higher stats and unique traits
            backstory_data = random.choice(cls.BACKSTORIES)
            return Dweller(
                name=name,
                strength=random.randint(5, 10),
                perception=random.randint(5, 10),
                endurance=random.randint(5, 10),
                charisma=random.randint(5, 10),
                intelligence=random.randint(5, 10),
                agility=random.randint(5, 10),
                luck=random.randint(5, 10),
                backstory=f"{backstory_data['profession']}: {backstory_data['story']}",
                unique_trait=f"{backstory_data['trait']} ({backstory_data['bonus']})"
            )
        else:
            # Regular dwellers
            return Dweller(
                name=name,
                strength=random.randint(3, 8),
                perception=random.randint(3, 8),
                endurance=random.randint(3, 8),
                charisma=random.randint(3, 8),
                intelligence=random.randint(3, 8),
                agility=random.randint(3, 8),
                luck=random.randint(3, 8),
                backstory=f"Vault dweller. {random.choice(['Hopeful for the future.', 'Misses the surface.', 'Proud to serve.', 'Dreams of adventure.'])}"
            )

# ============================================================================
# ENHANCED VAULT GAME ENGINE
# ============================================================================

class EnhancedVaultGame:
    def __init__(self):
        # Core resources
        self.day = 1
        self.food = 50
        self.water = 50
        self.power = 30
        self.caps = 100

        # Dwellers
        self.dwellers: List[Dweller] = []
        self.max_dwellers = 50

        # Rooms
        self.rooms = ['Living Quarters', 'Diner', 'Water Treatment']

        # Tutorial system
        self.tutorial_active = True
        self.tutorial_stage = 0
        self.tutorial_completed = False

        # Quest system
        self.quests: List[Quest] = []
        self.active_quest: Optional[Quest] = None

        # Achievement system
        self.achievements: List[Achievement] = []
        self.achievement_bonuses = {}

        # Daily challenge
        self.daily_challenge: Optional[DailyChallenge] = None

        # Prestige system
        self.prestige_level = 0
        self.prestige_dwellers = []

        # Progress milestones
        self.vault_tier = "Struggling Shelter"  # Tiers: Struggling -> Established -> Thriving -> Legend

        # Expedition system
        self.active_expedition = None

        # Event history
        self.event_history = []

        # Statistics
        self.total_days_survived = 0
        self.total_dwellers_ever = 0
        self.total_expeditions = 0

        # Initialize game
        self._initialize_game()

    def _initialize_game(self):
        """Initialize game with starting dwellers and systems"""
        # Create starting dwellers (3 special, 7 regular)
        for i in range(3):
            self.dwellers.append(DwellerGenerator.generate(special_dweller=True))
        for i in range(7):
            self.dwellers.append(DwellerGenerator.generate(special_dweller=False))

        self.total_dwellers_ever = 10

        # Initialize relationships
        self._initialize_relationships()

        # Setup quests
        self._initialize_quests()

        # Setup achievements
        self._initialize_achievements()

        # Generate first daily challenge
        self._generate_daily_challenge()

    def _initialize_relationships(self):
        """Create initial relationships between dwellers"""
        for dweller in self.dwellers:
            # Each dweller starts with neutral to slight relationships
            for other in self.dwellers:
                if other.name != dweller.name:
                    dweller.relationships[other.name] = random.randint(-10, 20)

    def _initialize_quests(self):
        """Setup story-driven quest chain"""
        self.quests = [
            Quest(
                id="radio_contact",
                name="Radio Contact",
                description="Detect a signal from Vault 8",
                unlock_day=10,
                rewards={"caps": 100, "power": 20},
                choices=[
                    {"text": "Respond to signal", "outcome": "alliance"},
                    {"text": "Ignore it (could be a trap)", "outcome": "isolate"}
                ]
            ),
            Quest(
                id="first_expedition",
                name="First Expedition",
                description="Send a team to investigate the signal source",
                unlock_day=25,
                rewards={"caps": 200, "special_dweller": True},
                choices=[
                    {"text": "Send your best team", "outcome": "success_high_risk"},
                    {"text": "Send a small scout team", "outcome": "safe_low_reward"}
                ]
            ),
            Quest(
                id="the_survivor",
                name="The Survivor",
                description="Rescue a dweller with unique skills from the wasteland",
                unlock_day=50,
                rewards={"legendary_dweller": True, "caps": 300}
            ),
            Quest(
                id="trade_route",
                name="Trade Route",
                description="Establish wasteland commerce",
                unlock_day=75,
                rewards={"trade_bonus": 0.5, "caps": 500}
            ),
            Quest(
                id="new_beginning",
                name="New Beginning",
                description="Choose your vault's future",
                unlock_day=100,
                rewards={"prestige": True},
                choices=[
                    {"text": "Remain isolated (safety)", "outcome": "isolate"},
                    {"text": "Unite with other vaults (cooperation)", "outcome": "unite"},
                    {"text": "Expand to the surface (ambition)", "outcome": "expand"}
                ]
            )
        ]

    def _initialize_achievements(self):
        """Setup achievement system"""
        self.achievements = [
            Achievement(
                id="pop_boom",
                name="Population Boom",
                description="Reach 25 dwellers",
                bonus={"birth_rate": 0.1},
                icon="👥"
            ),
            Achievement(
                id="resource_king",
                name="Resource King",
                description="Store 500 of each resource",
                bonus={"storage": 0.05},
                icon="💰"
            ),
            Achievement(
                id="survivor",
                name="Survivor",
                description="Survive 50 days without deaths",
                bonus={"health_bonus": 0.05},
                icon="❤️"
            ),
            Achievement(
                id="wasteland_explorer",
                name="Wasteland Explorer",
                description="Complete 10 successful expeditions",
                bonus={"expedition_loot": 0.2},
                icon="🗺️"
            ),
            Achievement(
                id="master_builder",
                name="Master Builder",
                description="Build 15 rooms",
                bonus={"build_cost": -0.1},
                icon="🏗️"
            ),
            Achievement(
                id="century_club",
                name="Century Club",
                description="Survive 100 days",
                bonus={"all_production": 0.1},
                icon="💯"
            )
        ]

    def _generate_daily_challenge(self):
        """Generate a new daily challenge"""
        challenges = [
            {
                "description": "Produce 50 power today",
                "goal_type": "power_production",
                "goal_value": 50,
                "reward": {"caps": 100}
            },
            {
                "description": "Train a dweller to 10 in any stat",
                "goal_type": "training",
                "goal_value": 10,
                "reward": {"caps": 150}
            },
            {
                "description": "Complete an expedition without injuries",
                "goal_type": "expedition_perfect",
                "goal_value": 1,
                "reward": {"caps": 200}
            },
            {
                "description": "Reach 100 happiness average",
                "goal_type": "happiness",
                "goal_value": 100,
                "reward": {"caps": 120}
            },
            {
                "description": "Collect 150 caps from any source",
                "goal_type": "caps_gain",
                "goal_value": 150,
                "reward": {"food": 50, "water": 50}
            }
        ]

        challenge_data = random.choice(challenges)
        self.daily_challenge = DailyChallenge(**challenge_data)

    def _update_vault_tier(self):
        """Update vault visual tier based on progress"""
        if self.day >= 81:
            self.vault_tier = "🌟 Wasteland Legend"
        elif self.day >= 51:
            self.vault_tier = "✨ Thriving Community"
        elif self.day >= 21:
            self.vault_tier = "⚡ Established Vault"
        else:
            self.vault_tier = "🔰 Struggling Shelter"

    def _check_achievements(self):
        """Check and unlock achievements"""
        unlocked_new = []

        for achievement in self.achievements:
            if achievement.unlocked:
                continue

            unlock = False
            if achievement.id == "pop_boom" and len(self.dwellers) >= 25:
                unlock = True
            elif achievement.id == "resource_king" and min(self.food, self.water, self.power) >= 500:
                unlock = True
            elif achievement.id == "survivor" and self.day >= 50:
                unlock = True
            elif achievement.id == "wasteland_explorer" and self.total_expeditions >= 10:
                unlock = True
            elif achievement.id == "master_builder" and len(self.rooms) >= 15:
                unlock = True
            elif achievement.id == "century_club" and self.day >= 100:
                unlock = True

            if unlock:
                achievement.unlocked = True
                unlocked_new.append(achievement)
                # Apply bonus
                if achievement.bonus:
                    self.achievement_bonuses.update(achievement.bonus)

        return unlocked_new

    def _check_quests(self):
        """Check if any quests should unlock"""
        for quest in self.quests:
            if not quest.completed and quest.unlock_day == self.day:
                self.active_quest = quest
                return f"\n🎭 NEW QUEST UNLOCKED: {quest.name}\n{quest.description}\n"
        return ""

    def get_status(self) -> str:
        """Return formatted vault status with all enhancements"""
        avg_happiness = sum(d.happiness for d in self.dwellers) // max(1, len(self.dwellers))

        # Resource warnings with actionable advice
        warnings = self._get_resource_warnings()

        # Tutorial hint if active
        tutorial_hint = self._get_tutorial_hint() if self.tutorial_active else ""

        # Daily challenge display
        challenge_display = ""
        if self.daily_challenge and not self.daily_challenge.completed:
            challenge_display = f"\n📋 DAILY CHALLENGE: {self.daily_challenge.description}"

        # Active quest display
        quest_display = ""
        if self.active_quest and not self.active_quest.completed:
            quest_display = f"\n🎭 ACTIVE QUEST: {self.active_quest.name}"

        status = f"""
╔══════════════════════════════════════════════════╗
║     VAULT 13 - Day {self.day:3d}  [{self.vault_tier}]
╠══════════════════════════════════════════════════╣
║ 👥 Dwellers: {len(self.dwellers):3d}/{self.max_dwellers}   😊 Happiness: {avg_happiness:3d}%
║ 🍖 Food: {self.food:4d}      💧 Water: {self.water:4d}
║ ⚡ Power: {self.power:4d}     💰 Caps: {self.caps:4d}
╠══════════════════════════════════════════════════╣
║ Rooms: {len(self.rooms)} | Achievements: {sum(1 for a in self.achievements if a.unlocked)}/{len(self.achievements)}
╚══════════════════════════════════════════════════╝
{warnings}{tutorial_hint}{challenge_display}{quest_display}

Commands: 1)Status 2)Build 3)Dwellers 4)Explore 5)Rest 6)Quests 7)Achievements ?Help
"""
        return status

    def _get_resource_warnings(self) -> str:
        """Generate specific actionable warnings"""
        warnings = []

        # Food warning
        if self.food <= 20:
            consumption = len(self.dwellers) // 2
            turns_left = self.food // max(1, consumption)
            warnings.append(f"⚠️  FOOD CRITICAL: {self.food} → 0 in ~{turns_left} turns")
            warnings.append(f"   → Build Diner (100 caps)")
            warnings.append(f"   → Trade for food (30 caps)")

        # Water warning
        if self.water <= 20:
            consumption = len(self.dwellers) // 2
            turns_left = self.water // max(1, consumption)
            warnings.append(f"⚠️  WATER CRITICAL: {self.water} → 0 in ~{turns_left} turns")
            warnings.append(f"   → Build Water Treatment (120 caps)")
            warnings.append(f"   → Trade for water (30 caps)")

        # Power warning
        if self.power <= 15:
            warnings.append(f"⚠️  POWER LOW: {self.power}")
            warnings.append(f"   → Build Power Generator (150 caps)")

        # Happiness warning
        avg_happiness = sum(d.happiness for d in self.dwellers) // max(1, len(self.dwellers))
        if avg_happiness < 50:
            warnings.append(f"⚠️  MORALE LOW: {avg_happiness}%")
            warnings.append(f"   → Check dweller assignments")
            warnings.append(f"   → Ensure resources are adequate")

        return "\n".join(warnings) + "\n" if warnings else ""

    def _get_tutorial_hint(self) -> str:
        """Return contextual tutorial hints"""
        hints = [
            "\n💡 TUTORIAL: Welcome to Vault 13! Press '1' or type 'status' to view your vault.",
            "\n💡 TUTORIAL: Try building a room! Type '2' or 'build' to construct.",
            "\n💡 TUTORIAL: Check your dwellers with '3' or 'dwellers'. Assign them to rooms!",
            "\n💡 TUTORIAL: Send dwellers to explore with '4' or 'explore'. Risk vs reward!",
            "\n💡 TUTORIAL: End the day with '5' or 'rest'. Resources are consumed each day.",
            "\n✅ TUTORIAL COMPLETE! You're ready to lead Vault 13. Good luck, Overseer!"
        ]

        if self.tutorial_stage < len(hints):
            return hints[self.tutorial_stage]
        else:
            self.tutorial_active = False
            return ""

    def advance_tutorial(self):
        """Progress tutorial to next stage"""
        if self.tutorial_active:
            self.tutorial_stage += 1
            if self.tutorial_stage >= 6:
                self.tutorial_active = False
                self.tutorial_completed = True

    def build_room(self) -> str:
        """Enhanced room building with visual feedback"""
        room_options = [
            {"name": "Power Generator", "cost": 150, "stat": "STR", "production": "⚡ Power"},
            {"name": "Water Treatment", "cost": 120, "stat": "PER", "production": "💧 Water"},
            {"name": "Diner", "cost": 100, "stat": "AGI", "production": "🍖 Food"},
            {"name": "Med Bay", "cost": 150, "stat": "INT", "healing": True},
            {"name": "Science Lab", "cost": 200, "stat": "INT", "research": True},
            {"name": "Training Room", "cost": 180, "stat": "ALL", "training": True},
            {"name": "Living Quarters", "cost": 100, "capacity": 4},
            {"name": "Armory", "cost": 220, "stat": "STR", "defense": True}
        ]

        # Apply achievement bonuses
        cost_multiplier = 1.0 - self.achievement_bonuses.get("build_cost", 0)

        menu = "\n╔═══ BUILD ROOM ═══╗\n"
        for i, room in enumerate(room_options, 1):
            cost = int(room["cost"] * cost_multiplier)
            can_afford = "✓" if self.caps >= cost else "✗"
            menu += f"{i}. {room['name']} - {cost} caps {can_afford}\n"
        menu += "0. Cancel\n╚══════════════════╝\n"

        return menu + "\nType room number to build:"

    def view_dwellers(self) -> str:
        """Enhanced dweller view with color-coded stats and personalities"""
        output = "\n╔═══ VAULT DWELLERS ═══╗\n"

        for i, dweller in enumerate(self.dwellers, 1):
            # Health and happiness indicators
            health_bar = self._make_progress_bar(dweller.health, 100, 10)
            happy_bar = self._make_progress_bar(dweller.happiness, 100, 10)

            output += f"\n{i}. {dweller.name}\n"
            output += f"   Health: {health_bar} {dweller.health}/100\n"
            output += f"   Happy:  {happy_bar} {dweller.happiness}/100\n"
            output += f"   Job: {dweller.job or 'Idle'}\n"

            # Color-coded SPECIAL stats
            output += f"   S:{dweller.strength}{dweller.get_stat_color(dweller.strength)} "
            output += f"P:{dweller.perception}{dweller.get_stat_color(dweller.perception)} "
            output += f"E:{dweller.endurance}{dweller.get_stat_color(dweller.endurance)} "
            output += f"C:{dweller.charisma}{dweller.get_stat_color(dweller.charisma)} "
            output += f"I:{dweller.intelligence}{dweller.get_stat_color(dweller.intelligence)} "
            output += f"A:{dweller.agility}{dweller.get_stat_color(dweller.agility)} "
            output += f"L:{dweller.luck}{dweller.get_stat_color(dweller.luck)}\n"

            # Show personality
            output += f"   {dweller.personality['outlook'].title()}, "
            output += f"{dweller.personality['work_ethic']}, "
            output += f"{dweller.personality['social']}\n"

            # Show unique trait if any
            if dweller.unique_trait:
                output += f"   🌟 {dweller.unique_trait}\n"

            # Show top relationships
            top_relationships = sorted(dweller.relationships.items(), key=lambda x: x[1], reverse=True)[:2]
            if top_relationships:
                output += f"   "
                for name, score in top_relationships:
                    # Safely get first name, defaulting to full name if no space
                    display_name = name.split()[0] if name and ' ' in name else name
                    if score > 50:
                        output += f"❤️ {display_name} "
                    elif score < -50:
                        output += f"⚔️ {display_name} "

        output += "\n╚══════════════════════╝\n"
        output += "Type dweller number for details, or 'back' to return\n"
        return output

    def _make_progress_bar(self, current: int, maximum: int, length: int = 10) -> str:
        """Create visual progress bar"""
        filled = int((current / maximum) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"

    def start_expedition(self) -> str:
        """Interactive expedition mini-game"""
        if len(self.dwellers) < 3:
            return "❌ Need at least 3 dwellers to send on expedition!"

        # Setup expedition
        self.active_expedition = {
            "current_room": 0,
            "rooms_explored": 0,
            "loot": {"caps": 0, "food": 0, "water": 0, "items": []},
            "team": random.sample(self.dwellers, min(3, len(self.dwellers))),
            "injuries": 0
        }

        locations = [
            "Abandoned Supermarket",
            "Ruined Hospital",
            "Office Building",
            "Military Outpost",
            "Research Facility"
        ]

        self.active_expedition["location"] = random.choice(locations)

        return self._expedition_encounter()

    def _expedition_encounter(self) -> str:
        """Generate expedition encounter"""
        encounters = [
            {
                "title": "Supply Cache",
                "desc": "You find an unopened storage locker.",
                "choices": [
                    {"text": "1. Force it open (STR check)", "stat": "strength", "success_loot": 50, "fail_injury": True},
                    {"text": "2. Pick the lock (PER check)", "stat": "perception", "success_loot": 75, "fail_loot": 10},
                    {"text": "3. Leave it (safe)", "loot": 0}
                ]
            },
            {
                "title": "Radroach Nest",
                "desc": "Giant cockroaches block your path!",
                "choices": [
                    {"text": "1. Fight them (STR check)", "stat": "strength", "success_loot": 30, "fail_injury": True},
                    {"text": "2. Sneak past (AGI check)", "stat": "agility", "success": True, "fail_injury": True},
                    {"text": "3. Use grenade (costs 50 caps)", "cost": 50, "success": True}
                ]
            },
            {
                "title": "Medical Supplies",
                "desc": "Intact medical cabinet with supplies!",
                "choices": [
                    {"text": "1. Take everything (50 caps worth)", "loot": 50},
                    {"text": "2. Search carefully (INT check for rare items)", "stat": "intelligence", "rare": True},
                    {"text": "3. Just take essentials (25 caps, safe)", "loot": 25}
                ]
            },
            {
                "title": "Survivor Encounter",
                "desc": "A wasteland wanderer offers to trade.",
                "choices": [
                    {"text": "1. Trade caps for supplies", "trade": True},
                    {"text": "2. Recruit them (CHA check)", "stat": "charisma", "success_dweller": True},
                    {"text": "3. Part ways peacefully", "loot": 0}
                ]
            },
            {
                "title": "Radiation Zone",
                "desc": "High radiation detected. Valuable loot visible through haze.",
                "choices": [
                    {"text": "1. Risk it (END check)", "stat": "endurance", "success_loot": 100, "fail_injury": True},
                    {"text": "2. Go around (safe, no loot)", "loot": 0},
                    {"text": "3. Send robot if available", "tech": True, "loot": 100}
                ]
            }
        ]

        encounter = random.choice(encounters)

        output = f"\n🗺️  EXPEDITION: {self.active_expedition['location']}\n"
        output += f"═══════════════════════════════\n"
        output += f"Room {self.active_expedition['rooms_explored'] + 1}/5\n\n"
        output += f"📍 {encounter['title']}\n"
        output += f"{encounter['desc']}\n\n"

        for choice in encounter['choices']:
            output += f"{choice['text']}\n"

        output += "\n0. Retreat to vault\n"

        self.active_expedition["current_encounter"] = encounter

        return output

    def handle_expedition_choice(self, choice_idx: int) -> str:
        """Handle player's expedition choice"""
        if not self.active_expedition:
            return "No active expedition!"

        encounter = self.active_expedition["current_encounter"]

        if choice_idx == 0:
            # Retreat
            result = self._complete_expedition()
            return result

        choice = encounter["choices"][choice_idx - 1]
        team = self.active_expedition["team"]

        result_text = ""

        # Check if stat check required
        if "stat" in choice:
            # Average stat of team
            stat_name = choice["stat"]
            avg_stat = sum(getattr(d, stat_name) for d in team) // len(team)
            success_chance = min(90, avg_stat * 10)
            success = random.randint(1, 100) <= success_chance

            if success:
                result_text = f"✅ Success! (Team {stat_name.upper()}: {avg_stat})\n"
                if "success_loot" in choice:
                    self.active_expedition["loot"]["caps"] += choice["success_loot"]
                    result_text += f"Found {choice['success_loot']} caps!\n"
            else:
                result_text = f"❌ Failed! (Team {stat_name.upper()} too low: {avg_stat})\n"
                if choice.get("fail_injury"):
                    self.active_expedition["injuries"] += 1
                    result_text += "A team member was injured!\n"

        # Direct loot
        elif "loot" in choice:
            self.active_expedition["loot"]["caps"] += choice["loot"]
            result_text = f"Collected {choice['loot']} caps.\n"

        # Trade option
        elif choice.get("trade"):
            result_text = "Traded 30 caps for supplies.\n"
            self.active_expedition["loot"]["food"] += 20
            self.active_expedition["loot"]["water"] += 20

        self.active_expedition["rooms_explored"] += 1

        # Check if expedition complete
        if self.active_expedition["rooms_explored"] >= 5:
            result_text += "\n" + self._complete_expedition()
        else:
            result_text += "\nMoving to next room...\n"
            result_text += self._expedition_encounter()

        return result_text

    def _complete_expedition(self) -> str:
        """Complete expedition and return rewards"""
        if not self.active_expedition:
            return ""

        loot = self.active_expedition["loot"]
        injuries = self.active_expedition["injuries"]

        # Apply loot
        self.caps += loot["caps"]
        self.food += loot.get("food", 0)
        self.water += loot.get("water", 0)

        # Apply injuries
        for i in range(injuries):
            if self.dwellers:
                injured = random.choice(self.dwellers)
                injured.health -= 30
                if injured.health <= 0:
                    self.dwellers.remove(injured)

        self.total_expeditions += 1

        # Check daily challenge
        if (self.daily_challenge and
            self.daily_challenge.goal_type == "expedition_perfect" and
            injuries == 0):
            self.daily_challenge.completed = True

        result = f"""
╔═══ EXPEDITION COMPLETE ═══╗
Location: {self.active_expedition['location']}
Rooms explored: {self.active_expedition['rooms_explored']}/5

REWARDS:
💰 Caps: +{loot['caps']}
🍖 Food: +{loot.get('food', 0)}
💧 Water: +{loot.get('water', 0)}

⚠️  Injuries: {injuries}

Total expeditions: {self.total_expeditions}
╚═══════════════════════════╝
"""

        self.active_expedition = None
        return result

    def rest(self) -> str:
        """Enhanced rest with dynamic events and relationship updates"""
        # Consume resources
        consumption = len(self.dwellers) // 2
        self.food -= consumption
        self.water -= consumption
        self.power -= consumption // 2

        self.day += 1
        self.total_days_survived += 1

        self.advance_tutorial()
        self._update_vault_tier()

        # Update relationships
        self._update_relationships()

        # Check for quests
        quest_message = self._check_quests()

        # Check achievements
        new_achievements = self._check_achievements()
        achievement_text = ""
        if new_achievements:
            achievement_text = "\n🎉 ACHIEVEMENTS UNLOCKED:\n"
            for ach in new_achievements:
                achievement_text += f"   {ach.icon} {ach.name}: {ach.description}\n"

        # Dynamic branching events
        event_text = ""
        if random.random() < 0.3:  # 30% chance of event
            event = self._generate_dynamic_event()
            if event:
                event_text = f"\n🎭 EVENT: {event.title}\n{event.description}\n\n"
                for i, choice in enumerate(event.choices, 1):
                    event_text += f"{i}. {choice['text']}\n"
                self.pending_event = event

        # Simple events if no dynamic event
        elif random.random() < 0.2:
            event_text = self._generate_simple_event()

        # Resource warnings
        warnings = []
        if self.food <= 0:
            if self.dwellers:
                dead = random.choice(self.dwellers)
                self.dwellers.remove(dead)
                warnings.append(f"💀 {dead.name} died of starvation!")
            self.food = 0

        if self.water <= 0:
            for dweller in self.dwellers:
                dweller.happiness = max(0, dweller.happiness - 30)
            warnings.append("⚠️  Dehydration! All dwellers suffering!")
            self.water = 0

        # New daily challenge
        if self.day % 5 == 0:
            self._generate_daily_challenge()

        result = f"💤 Day {self.day} begins... (-{consumption} food/water)\n"
        result += "\n".join(warnings) + "\n" if warnings else ""
        result += quest_message
        result += achievement_text
        result += event_text
        result += self.get_status()

        return result

    def _update_relationships(self):
        """Update dweller relationships over time"""
        for dweller in self.dwellers:
            for other in self.dwellers:
                if other.name == dweller.name:
                    continue

                # Relationships change based on personality compatibility
                change = 0

                # Social personalities affect relationship growth
                if dweller.personality['social'] == 'friendly':
                    change += random.randint(1, 3)
                elif dweller.personality['social'] == 'awkward':
                    change += random.randint(-1, 1)

                # Random events
                if random.random() < 0.05:  # 5% chance of significant event
                    change += random.randint(-10, 10)

                # Update
                dweller.relationships[other.name] = max(-100, min(100,
                    dweller.relationships.get(other.name, 0) + change))

    def _generate_dynamic_event(self) -> Optional[Event]:
        """Generate dynamic event with branching choices"""
        events = [
            Event(
                title="Mysterious Trader",
                description="A well-armed trader arrives at your vault door. They're offering rare goods but seem suspicious.",
                choices=[
                    {
                        "text": "Trade 100 caps for mystery box",
                        "outcome": lambda: self._event_mystery_box()
                    },
                    {
                        "text": "Invite them inside to talk",
                        "outcome": lambda: self._event_trader_inside()
                    },
                    {
                        "text": "Send them away",
                        "outcome": lambda: "You politely decline. The trader leaves, muttering about missed opportunities."
                    }
                ]
            ),
            Event(
                title="Dweller Dispute",
                description=f"{random.choice(self.dwellers).name} and {random.choice(self.dwellers).name} are having a heated argument!",
                choices=[
                    {
                        "text": "Mediate peacefully (CHA check)",
                        "outcome": lambda: self._event_mediate()
                    },
                    {
                        "text": "Let them work it out",
                        "outcome": lambda: self._event_ignore_dispute()
                    },
                    {
                        "text": "Separate them to different rooms",
                        "outcome": lambda: "You assign them to different areas. Tension eases but isn't resolved."
                    }
                ]
            ),
            Event(
                title="Radio Broadcast",
                description="You intercept a distress call from nearby survivors. They need medical supplies urgently.",
                choices=[
                    {
                        "text": "Send supplies (costs 50 caps)",
                        "outcome": lambda: self._event_send_aid()
                    },
                    {
                        "text": "Offer shelter instead",
                        "outcome": lambda: self._event_offer_shelter()
                    },
                    {
                        "text": "Ignore the call (safety first)",
                        "outcome": lambda: "You maintain radio silence. Survival requires hard choices."
                    }
                ]
            )
        ]

        return random.choice(events) if random.random() < 0.5 else None

    def _event_mystery_box(self) -> str:
        """Mystery box outcome"""
        if self.caps >= 100:
            self.caps -= 100
            if random.random() < 0.7:  # 70% good
                reward = random.randint(150, 300)
                self.caps += reward
                return f"✅ The box contained {reward} caps worth of valuable supplies! Net: +{reward - 100}"
            else:
                return "❌ The box contained junk. You've been scammed! -100 caps"
        return "Not enough caps!"

    def _event_trader_inside(self) -> str:
        """Invite trader inside"""
        if random.random() < 0.6:  # 60% good outcome
            new_dweller = DwellerGenerator.generate(special_dweller=True)
            self.dwellers.append(new_dweller)
            return f"✅ The trader was actually a skilled wanderer seeking shelter! {new_dweller.name} joins your vault."
        else:
            stolen = min(50, self.caps)
            self.caps -= stolen
            return f"❌ The trader steals {stolen} caps while you're distracted! They flee into the wasteland."

    def _event_mediate(self) -> str:
        """Mediate dispute"""
        avg_cha = sum(d.charisma for d in self.dwellers) // max(1, len(self.dwellers))
        if random.randint(1, 10) <= avg_cha:
            for dweller in random.sample(self.dwellers, min(2, len(self.dwellers))):
                dweller.happiness += 10
            return "✅ Your diplomatic skills resolve the conflict! Both dwellers feel heard. +10 happiness each"
        else:
            for dweller in random.sample(self.dwellers, min(2, len(self.dwellers))):
                dweller.happiness -= 5
            return "❌ Your mediation backfires. Both dwellers are now upset with management. -5 happiness each"

    def _event_ignore_dispute(self) -> str:
        """Let them work it out"""
        if random.random() < 0.5:
            return "✅ They resolve it themselves and become closer friends!"
        else:
            return "❌ The argument escalates. Both dwellers are unhappy. -10 happiness each"

    def _event_send_aid(self) -> str:
        """Send aid to survivors"""
        if self.caps >= 50:
            self.caps -= 50
            # 80% chance of good outcome
            if random.random() < 0.8:
                new_dweller = DwellerGenerator.generate(special_dweller=False)
                self.dwellers.append(new_dweller)
                return f"❤️  The grateful survivors send {new_dweller.name} to join your vault! Karma pays off."
            else:
                return "The supplies are delivered. No response. Sometimes kindness is its own reward."
        return "Not enough caps to send aid."

    def _event_offer_shelter(self) -> str:
        """Offer shelter to survivors"""
        if len(self.dwellers) < self.max_dwellers:
            count = random.randint(1, 3)
            for _ in range(count):
                self.dwellers.append(DwellerGenerator.generate(special_dweller=False))
            return f"✅ {count} grateful survivors join your vault! +{count} dwellers"
        return "No room for more dwellers!"

    def _generate_simple_event(self) -> str:
        """Generate simple random events"""
        events = [
            ("🎉", "Dwellers threw a party!", lambda: self._modify_happiness(10)),
            ("🎵", "Someone found a working radio! Morale boost!", lambda: self._modify_happiness(5)),
            ("👶", "A child was born in the vault!", lambda: self._add_dweller()),
            ("📚", "Dwellers discovered old books. Knowledge preserved!", lambda: None),
            ("🔧", "Maintenance completed. All systems nominal.", lambda: None),
        ]

        icon, message, effect = random.choice(events)
        if effect:
            effect()

        return f"\n{icon} {message}\n"

    def _modify_happiness(self, amount: int):
        """Modify all dwellers' happiness"""
        for dweller in self.dwellers:
            dweller.happiness = max(0, min(100, dweller.happiness + amount))

    def _add_dweller(self):
        """Add a new dweller"""
        if len(self.dwellers) < self.max_dwellers:
            self.dwellers.append(DwellerGenerator.generate(special_dweller=False))

    def view_quests(self) -> str:
        """Display all quests"""
        output = "\n╔═══ QUESTS ═══╗\n"

        for quest in self.quests:
            status = "✅" if quest.completed else ("🔓" if quest.unlock_day <= self.day else "🔒")
            output += f"{status} {quest.name} (Day {quest.unlock_day})\n"
            if quest.unlock_day <= self.day:
                output += f"   {quest.description}\n"
                if quest.completed:
                    output += "   COMPLETED!\n"

        output += "╚══════════════╝\n"
        return output

    def view_achievements(self) -> str:
        """Display all achievements"""
        output = "\n╔═══ ACHIEVEMENTS ═══╗\n"

        for achievement in self.achievements:
            status = "✅" if achievement.unlocked else "⬜"
            output += f"{status} {achievement.icon} {achievement.name}\n"
            output += f"   {achievement.description}\n"
            if achievement.unlocked and achievement.bonus:
                output += f"   BONUS ACTIVE: {achievement.bonus}\n"

        unlocked = sum(1 for a in self.achievements if a.unlocked)
        output += f"\nTotal: {unlocked}/{len(self.achievements)}\n"
        output += "╚════════════════════╝\n"
        return output

    def get_help(self, context: str = "main") -> str:
        """Contextual help system"""
        if context == "main":
            return """
╔═══ VAULT 13 HELP ═══╗

COMMANDS (use numbers or names):
1. status     - View vault statistics
2. build      - Construct new rooms
3. dwellers   - Manage your people
4. explore    - Send expedition to wasteland
5. rest       - End day & advance time
6. quests     - View story missions
7. achievements - View unlocked achievements
8. trade      - Trade with merchants
9. help       - Show this help
?             - Context-sensitive help

TIPS:
• Keep resources balanced
• Assign dwellers to matching rooms
• Watch for color-coded stat ratings:
  🟢 = Excellent (8-10)
  🟡 = Good (5-7)
  🔴 = Poor (1-4)
• Complete daily challenges for bonuses
• Build relationships between dwellers

╚══════════════════════╝
"""
        elif context == "building":
            return """
BUILDING HELP:
• Power Generator - Needs high STR workers
• Water Treatment - Needs high PER workers
• Diner - Needs high AGI workers
• Med Bay - Heals injured dwellers
• Training Room - Improves dweller stats
• Science Lab - Unlocks research
"""
        elif context == "expedition":
            return """
EXPEDITION HELP:
• Requires 3+ dwellers
• Risk vs reward gameplay
• Stat checks determine success
• Can find caps, resources, and items
• Injuries can occur
• Better team stats = better chances
"""
        else:
            return "No help available for this context. Type 'help' for main help."

# ============================================================================
# GAME WRAPPER FOR BROWSER INTEGRATION
# ============================================================================

def create_enhanced_vault():
    """Factory function to create enhanced vault game"""
    return EnhancedVaultGame()

if __name__ == "__main__":
    # Test the enhanced game
    game = EnhancedVaultGame()
    print(game.get_status())
    print(game.view_dwellers())
    print(game.view_achievements())
