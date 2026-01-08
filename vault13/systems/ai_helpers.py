"""
VAULT 13: AI Helper Functions
AI integration and fallback generation.
"""

import os
import json
import random
from typing import List

# AI Integration
AI_ENABLED = False
ai_client = None

try:
    import anthropic
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    if API_KEY:
        ai_client = anthropic.Anthropic(api_key=API_KEY)
        AI_ENABLED = True
except ImportError:
    pass


def call_ai_model(prompt: str, max_tokens: int = 500, system_prompt: str = "") -> str:
    """Call AI with fallback"""
    if not AI_ENABLED or ai_client is None:
        return generate_fallback_response(prompt)
    try:
        messages = [{"role": "user", "content": prompt}]
        response = ai_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=system_prompt if system_prompt else "You are the AI assistant for Vault 13.",
            messages=messages
        )
        return response.content[0].text
    except Exception:
        return generate_fallback_response(prompt)


def generate_fallback_response(prompt: str) -> str:
    """Fallback responses when AI is unavailable"""
    prompt_lower = prompt.lower()
    if "dialogue" in prompt_lower or "comment" in prompt_lower:
        return random.choice([
            "Another day in the vault. Could be worse.",
            "Just doing my part to keep everyone alive.",
            "I wonder what the surface looks like now...",
            "At least we have each other down here.",
            "The vault protects us. We protect each other.",
            "Have you checked the water purifiers today?",
            "I heard there's a new shipment coming in.",
            "Stay safe out there, Overseer.",
        ])
    elif "quest" in prompt_lower:
        return json.dumps({
            "title": "Resource Emergency",
            "description": "The vault needs supplies urgently.",
            "steps": [{"description": "Gather 50 of any resource", "type": "resource"}],
            "rewards": {"caps": 100}
        })
    elif "advisor" in prompt_lower:
        return "Focus on maintaining resource balance and keeping dwellers happy."
    else:
        return "[AI unavailable - using fallback]"


def generate_quest(game) -> dict:
    """Generate a procedural quest"""
    from vault13.models.quest import Quest, QuestStep

    if not AI_ENABLED:
        quest_templates = [
            {
                "title": "Resource Shortage",
                "description": "Gather resources to survive.",
                "quest_type": "resource",
                "steps": [QuestStep("Accumulate 50 food", {"resource": "food", "amount": 50})],
                "rewards": {"caps": 200}
            },
            {
                "title": "Population Growth",
                "description": "Expand your vault population.",
                "quest_type": "dweller",
                "steps": [QuestStep("Have 6 dwellers", {"dwellers": 6})],
                "rewards": {"caps": 300, "research": 50}
            },
            {
                "title": "Technological Advancement",
                "description": "Research new technologies.",
                "quest_type": "research",
                "steps": [QuestStep("Accumulate 100 research points", {"research": 100})],
                "rewards": {"caps": 250}
            },
            {
                "title": "Vault Security",
                "description": "Strengthen your defenses.",
                "quest_type": "military",
                "steps": [QuestStep("Arm 3 dwellers with weapons", {"armed_dwellers": 3})],
                "rewards": {"caps": 400}
            }
        ]

        template = random.choice(quest_templates)
        return Quest(
            quest_id=f"quest_{game.day}_{random.randint(1000, 9999)}",
            title=template["title"],
            description=template["description"],
            quest_type=template["quest_type"],
            steps=template["steps"],
            rewards=template["rewards"],
            created_day=game.day
        )

    # AI-generated quest
    vault_state = {
        "day": game.day,
        "dwellers": len(game.dwellers),
        "caps": game.resources.caps,
        "government": game.government.value if game.government else "None"
    }

    prompt = f"""Generate a Fallout-style vault quest.
Vault State: {json.dumps(vault_state)}

Return ONLY valid JSON:
{{
    "title": "Quest Name",
    "description": "Brief description",
    "steps": [{{"description": "Step 1", "type": "resource"}}],
    "rewards": {{"caps": 100}}
}}"""

    try:
        response = call_ai_model(prompt, max_tokens=300)
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            quest_data = json.loads(response[json_start:json_end])
            steps = [QuestStep(s.get("description", "Complete objective"), s)
                    for s in quest_data.get("steps", [])]
            return Quest(
                quest_id=f"quest_{game.day}_{random.randint(1000, 9999)}",
                title=quest_data["title"],
                description=quest_data["description"],
                quest_type="ai_generated",
                steps=steps,
                rewards=quest_data.get("rewards", {"caps": 100}),
                created_day=game.day
            )
    except Exception:
        pass

    # Fallback
    return Quest(
        quest_id=f"quest_{game.day}",
        title="Vault Emergency",
        description="Handle the current crisis.",
        quest_type="survival",
        steps=[QuestStep("Survive another day", {"survival": True})],
        rewards={"caps": 150},
        created_day=game.day
    )


def get_dweller_dialogue(dweller, context: str, game_state: dict) -> str:
    """Generate dweller dialogue"""
    if not AI_ENABLED:
        return generate_fallback_response("dialogue")

    prompt = f"""Generate a short comment (1-2 sentences) for this dweller.

Dweller: {dweller.name} (Age {dweller.age}, {dweller.gender})
Personality: {dweller.get_personality_summary()}
Health: {dweller.health}% | Happiness: {dweller.happiness}%
{"Child (cannot work)" if dweller.is_child else f"Level {dweller.level}"}
Context: {context}

Generate a witty, Fallout-themed comment. No quotes."""

    return call_ai_model(prompt, max_tokens=100)


def inherit_traits(parent1_traits: List[str], parent2_traits: List[str]) -> List[str]:
    """Inherit traits from parents with mutation chance"""
    from vault13.constants import TRAIT_LIBRARY, TraitType

    inherited = []

    # Inherit from parents (50% chance for each inheritable trait)
    for trait_id in parent1_traits + parent2_traits:
        if trait_id in TRAIT_LIBRARY:
            trait = TRAIT_LIBRARY[trait_id]
            if trait.inheritable and random.random() < 0.5:
                if trait_id not in inherited:
                    inherited.append(trait_id)

    # 5% chance for random mutation
    if random.random() < 0.05:
        mutation_traits = [t for t, data in TRAIT_LIBRARY.items()
                          if data.trait_type == TraitType.MUTATION]
        if mutation_traits:
            mutation = random.choice(mutation_traits)
            if mutation not in inherited:
                inherited.append(mutation)

    return inherited
