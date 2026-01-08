"""
VAULT 13: Save/Load System
Game persistence functions.
"""

import json
import os
import logging
from dataclasses import asdict
from typing import Optional, Dict, Any

from colors import C

# Logger
game_logger = logging.getLogger('vault13')


def save_game(game, filename: str = "vault_save.json") -> bool:
    """Save game to JSON file"""
    game_logger.info(f"Saving game to {filename}")

    # Ensure saves directory exists
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'saves')
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    save_data = {
        "version": "9.0_MODULAR",
        "day": game.day,
        "resources": asdict(game.resources),
        "dwellers": [asdict(d) for d in game.dwellers],
        "vault_layout": [[{
            "room_type": room.room_type.value,
            "level": room.level,
            "floor": room.floor,
            "position": room.position,
            "assigned_dwellers": room.assigned_dwellers,
            "under_construction": room.under_construction,
            "on_fire": room.on_fire,
            "has_incident": room.has_incident
        } for room in floor] for floor in game.vault_layout],
        "researched_tech": game.researched_tech,
        "government": game.government.value if game.government else None,
        "active_policies": game.active_policies,
        "faction_reputations": {f.value: rep for f, rep in game.faction_reputations.items()},
        "legendary_inventory": game.legendary_inventory,
        "children_born": game.children_born,
        "disasters_survived": game.disasters_survived,
        "major_events": game.major_events,
        "equipment_inventory": game.equipment_inventory,
        "floors_unlocked": game.floors_unlocked,
        # Karma system
        "karma_scores": getattr(game, 'karma_scores', {}),
    }

    try:
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        game_logger.info("Game saved successfully")
        print(f"{C.SUCCESS}✓ Game saved to {filename}!{C.RESET}")
        return True
    except Exception as e:
        game_logger.error(f"Save failed: {e}")
        print(f"{C.DANGER}Save failed: {e}{C.RESET}")
        return False


def load_game(filename: str = "vault_save.json") -> Optional[Dict[str, Any]]:
    """Load game from JSON file"""
    game_logger.info(f"Loading game from {filename}")

    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'saves')
    filepath = os.path.join(save_dir, filename)

    # Also check current directory for backwards compatibility
    if not os.path.exists(filepath):
        filepath = filename

    try:
        with open(filepath, 'r') as f:
            save_data = json.load(f)

        game_logger.info(f"Game loaded successfully from day {save_data['day']}")
        print(f"{C.SUCCESS}✓ Game loaded from day {save_data['day']}!{C.RESET}")
        return save_data
    except FileNotFoundError:
        game_logger.warning(f"Save file not found: {filename}")
        print(f"{C.WARNING}No save file found.{C.RESET}")
        return None
    except json.JSONDecodeError as e:
        game_logger.error(f"Invalid save file: {e}")
        print(f"{C.DANGER}Invalid save file: {e}{C.RESET}")
        return None
    except Exception as e:
        game_logger.error(f"Load failed: {e}")
        print(f"{C.DANGER}Load failed: {e}{C.RESET}")
        return None


def list_saves() -> list:
    """List available save files"""
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'saves')
    if not os.path.exists(save_dir):
        return []

    saves = []
    for filename in os.listdir(save_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(save_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                saves.append({
                    "filename": filename,
                    "day": data.get("day", 0),
                    "version": data.get("version", "unknown"),
                    "dwellers": len(data.get("dwellers", []))
                })
            except Exception:
                pass
    return saves


def delete_save(filename: str) -> bool:
    """Delete a save file"""
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'saves')
    filepath = os.path.join(save_dir, filename)

    try:
        os.remove(filepath)
        print(f"{C.SUCCESS}✓ Save file deleted.{C.RESET}")
        return True
    except Exception as e:
        print(f"{C.DANGER}Failed to delete save: {e}{C.RESET}")
        return False


def create_backup(game, backup_name: str = None) -> bool:
    """Create a backup save"""
    if backup_name is None:
        backup_name = f"backup_day{game.day}.json"
    return save_game(game, backup_name)
