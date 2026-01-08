"""
VAULT 13: Universal Karma System
Tracks player choices across all games and affects outcomes.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from enum import Enum


class KarmaAlignment(Enum):
    """Moral alignment based on karma"""
    SAINT = "Saint"           # 75+
    GOOD = "Good"             # 25 to 74
    NEUTRAL = "Neutral"       # -24 to 24
    BAD = "Bad"               # -74 to -25
    VILLAIN = "Villain"       # -75 and below


class DecisionType(Enum):
    """Types of moral decisions"""
    UTILITARIAN = "utilitarian"     # Greatest good for greatest number
    DEONTOLOGICAL = "deontological" # Duty-based ethics
    VIRTUE = "virtue"               # Character-based ethics
    CONSEQUENTIAL = "consequential" # Outcome-based
    SELF_INTEREST = "self_interest" # Self-serving
    SACRIFICE = "sacrifice"         # Self-sacrifice for others


@dataclass
class KarmaEvent:
    """A recorded karma-affecting event"""
    game_id: str
    event_id: str
    description: str
    karma_change: int
    decision_type: DecisionType
    timestamp: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KarmaProfile:
    """Player's karma profile across all games"""
    total_karma: int = 0
    events: List[KarmaEvent] = field(default_factory=list)
    game_karma: Dict[str, int] = field(default_factory=dict)  # game_id -> karma
    decision_counts: Dict[str, int] = field(default_factory=dict)  # decision_type -> count
    alignment_history: List[str] = field(default_factory=list)

    # Philosophical tendencies (tracked across games)
    utilitarian_score: int = 0
    deontological_score: int = 0
    virtue_score: int = 0
    self_interest_score: int = 0


class KarmaSystem:
    """
    Universal Karma System

    Tracks player moral choices across all philosophical games and
    affects outcomes, dialogue, and available options in other games.
    """

    KARMA_FILE = "karma_profile.json"

    def __init__(self, save_dir: str = None):
        self.save_dir = save_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), '..', 'saves'
        )
        self.profile = KarmaProfile()
        self.load_profile()

    def load_profile(self) -> bool:
        """Load karma profile from disk"""
        filepath = os.path.join(self.save_dir, self.KARMA_FILE)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                self.profile = KarmaProfile(
                    total_karma=data.get("total_karma", 0),
                    game_karma=data.get("game_karma", {}),
                    decision_counts=data.get("decision_counts", {}),
                    alignment_history=data.get("alignment_history", []),
                    utilitarian_score=data.get("utilitarian_score", 0),
                    deontological_score=data.get("deontological_score", 0),
                    virtue_score=data.get("virtue_score", 0),
                    self_interest_score=data.get("self_interest_score", 0),
                )
                return True
        except Exception:
            pass
        return False

    def save_profile(self) -> bool:
        """Save karma profile to disk"""
        os.makedirs(self.save_dir, exist_ok=True)
        filepath = os.path.join(self.save_dir, self.KARMA_FILE)
        try:
            data = {
                "total_karma": self.profile.total_karma,
                "game_karma": self.profile.game_karma,
                "decision_counts": self.profile.decision_counts,
                "alignment_history": self.profile.alignment_history,
                "utilitarian_score": self.profile.utilitarian_score,
                "deontological_score": self.profile.deontological_score,
                "virtue_score": self.profile.virtue_score,
                "self_interest_score": self.profile.self_interest_score,
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def record_decision(self, game_id: str, event_id: str, description: str,
                       karma_change: int, decision_type: DecisionType,
                       context: Dict[str, Any] = None):
        """Record a moral decision"""
        from datetime import datetime

        event = KarmaEvent(
            game_id=game_id,
            event_id=event_id,
            description=description,
            karma_change=karma_change,
            decision_type=decision_type,
            timestamp=datetime.now().isoformat(),
            context=context or {}
        )

        # Update totals
        self.profile.total_karma += karma_change
        self.profile.events.append(event)

        # Update game-specific karma
        if game_id not in self.profile.game_karma:
            self.profile.game_karma[game_id] = 0
        self.profile.game_karma[game_id] += karma_change

        # Update decision type counts
        dtype = decision_type.value
        if dtype not in self.profile.decision_counts:
            self.profile.decision_counts[dtype] = 0
        self.profile.decision_counts[dtype] += 1

        # Update philosophical tendency scores
        if decision_type == DecisionType.UTILITARIAN:
            self.profile.utilitarian_score += abs(karma_change)
        elif decision_type == DecisionType.DEONTOLOGICAL:
            self.profile.deontological_score += abs(karma_change)
        elif decision_type == DecisionType.VIRTUE:
            self.profile.virtue_score += abs(karma_change)
        elif decision_type == DecisionType.SELF_INTEREST:
            self.profile.self_interest_score += abs(karma_change)

        # Track alignment changes
        new_alignment = self.get_alignment().value
        if (not self.profile.alignment_history or
            self.profile.alignment_history[-1] != new_alignment):
            self.profile.alignment_history.append(new_alignment)

        self.save_profile()

    def get_alignment(self) -> KarmaAlignment:
        """Get current moral alignment"""
        karma = self.profile.total_karma
        if karma >= 75:
            return KarmaAlignment.SAINT
        elif karma >= 25:
            return KarmaAlignment.GOOD
        elif karma >= -24:
            return KarmaAlignment.NEUTRAL
        elif karma >= -74:
            return KarmaAlignment.BAD
        else:
            return KarmaAlignment.VILLAIN

    def get_dominant_philosophy(self) -> str:
        """Get the player's dominant ethical framework"""
        scores = {
            "Utilitarian": self.profile.utilitarian_score,
            "Deontological": self.profile.deontological_score,
            "Virtue Ethics": self.profile.virtue_score,
            "Egoist": self.profile.self_interest_score,
        }
        if not any(scores.values()):
            return "Undefined"
        return max(scores, key=scores.get)

    def get_game_karma(self, game_id: str) -> int:
        """Get karma for a specific game"""
        return self.profile.game_karma.get(game_id, 0)

    def get_modifier(self, base_value: int, positive_for_good: bool = True) -> int:
        """
        Get a value modified by karma.

        If positive_for_good=True, good karma increases the value.
        If positive_for_good=False, good karma decreases the value.
        """
        karma_modifier = self.profile.total_karma / 100  # -1.0 to 1.0
        if not positive_for_good:
            karma_modifier = -karma_modifier
        return int(base_value * (1 + karma_modifier * 0.5))

    def affects_outcome(self, threshold: int, favor_good: bool = True) -> bool:
        """
        Check if karma affects an outcome.

        Returns True if karma exceeds threshold (or is below -threshold if !favor_good)
        """
        if favor_good:
            return self.profile.total_karma >= threshold
        else:
            return self.profile.total_karma <= -threshold

    def get_dialogue_modifier(self) -> str:
        """Get a modifier string for NPC dialogue based on karma"""
        alignment = self.get_alignment()
        modifiers = {
            KarmaAlignment.SAINT: "speaks to you with reverence",
            KarmaAlignment.GOOD: "seems friendly toward you",
            KarmaAlignment.NEUTRAL: "regards you neutrally",
            KarmaAlignment.BAD: "eyes you suspiciously",
            KarmaAlignment.VILLAIN: "recoils from your presence",
        }
        return modifiers.get(alignment, "")

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the karma profile"""
        return {
            "total_karma": self.profile.total_karma,
            "alignment": self.get_alignment().value,
            "dominant_philosophy": self.get_dominant_philosophy(),
            "total_decisions": len(self.profile.events),
            "games_played": len(self.profile.game_karma),
            "alignment_changes": len(self.profile.alignment_history),
        }

    def reset(self):
        """Reset karma profile (for new game+)"""
        self.profile = KarmaProfile()
        self.save_profile()


# Global karma system instance
_karma_system: Optional[KarmaSystem] = None


def get_karma_system() -> KarmaSystem:
    """Get the global karma system instance"""
    global _karma_system
    if _karma_system is None:
        _karma_system = KarmaSystem()
    return _karma_system


# =============================================================================
# KARMA EVENTS FOR DIFFERENT GAMES
# =============================================================================

# Trolley Problem decisions
TROLLEY_KARMA = {
    "pull_lever": {"karma": -5, "type": DecisionType.UTILITARIAN,
                   "desc": "Sacrificed one to save five"},
    "do_nothing": {"karma": 5, "type": DecisionType.DEONTOLOGICAL,
                   "desc": "Refused to actively cause death"},
    "push_man": {"karma": -15, "type": DecisionType.UTILITARIAN,
                 "desc": "Pushed someone to their death"},
    "sacrifice_self": {"karma": 25, "type": DecisionType.SACRIFICE,
                      "desc": "Offered yourself to save others"},
}

# Chinese Room decisions
CHINESE_ROOM_KARMA = {
    "claim_understanding": {"karma": -10, "type": DecisionType.SELF_INTEREST,
                           "desc": "Falsely claimed to understand"},
    "admit_limitation": {"karma": 10, "type": DecisionType.VIRTUE,
                        "desc": "Honestly admitted limitations"},
    "seek_true_understanding": {"karma": 15, "type": DecisionType.VIRTUE,
                               "desc": "Pursued genuine understanding"},
}

# Ship of Theseus decisions
SHIP_OF_THESEUS_KARMA = {
    "preserve_original": {"karma": 5, "type": DecisionType.DEONTOLOGICAL,
                         "desc": "Valued the original form"},
    "embrace_change": {"karma": 5, "type": DecisionType.CONSEQUENTIAL,
                      "desc": "Accepted transformation"},
    "destroy_to_preserve": {"karma": -10, "type": DecisionType.SELF_INTEREST,
                           "desc": "Destroyed what was to preserve identity"},
}

# Prisoner's Dilemma decisions
PRISONERS_DILEMMA_KARMA = {
    "cooperate": {"karma": 10, "type": DecisionType.VIRTUE,
                 "desc": "Chose cooperation over betrayal"},
    "defect": {"karma": -10, "type": DecisionType.SELF_INTEREST,
              "desc": "Betrayed for personal gain"},
    "tit_for_tat": {"karma": 0, "type": DecisionType.CONSEQUENTIAL,
                   "desc": "Responded in kind"},
    "always_forgive": {"karma": 15, "type": DecisionType.VIRTUE,
                      "desc": "Forgave betrayal"},
}
