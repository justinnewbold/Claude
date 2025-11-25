"""
Vercel Serverless Function Entrypoint for VAULT 13 Web Terminal
================================================================
This file exposes the Flask application for Vercel deployment.

Note: Vercel serverless functions have limited WebSocket support.
The terminal gameplay requires WebSocket for real-time I/O.
This deployment serves the game launcher and info pages.
"""

import os
import sys
from pathlib import Path

# Add the web-terminal directory to Python path
web_terminal_path = Path(__file__).parent.parent / 'deploy' / 'web-terminal'
sys.path.insert(0, str(web_terminal_path))

# Add root directory for config imports
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from flask import Flask, render_template, jsonify

# Create a minimal Flask app for Vercel
app = Flask(
    __name__,
    template_folder=str(web_terminal_path / 'templates'),
    static_folder=str(web_terminal_path / 'static'),
    static_url_path='/static'
)

# Try to import game registry
try:
    sys.path.insert(0, str(root_path))
    from config import GAME_REGISTRY, APP_DISPLAY_NAME, APP_VERSION
except ImportError:
    GAME_REGISTRY = {}
    APP_DISPLAY_NAME = "VAULT 13"
    APP_VERSION = "9.0"


@app.route('/')
def index():
    """Show game selection page."""
    games = []

    if GAME_REGISTRY:
        categories = {
            'main': 'Main Games',
            'quantum': 'Quantum & Physics',
            'physics': 'Physics Simulations',
            'computation': 'Computation & Logic',
            'logic': 'Logic & Mathematics',
            'philosophy': 'Philosophy of Mind',
            'decision': 'Decision Theory',
            'other': 'Other Experiments'
        }

        for game_id, game_info in GAME_REGISTRY.items():
            games.append({
                'id': game_info.id,
                'name': game_info.name,
                'file': game_info.file,
                'description': game_info.description,
                'category': categories.get(game_info.category, game_info.category),
                'available': True  # Assume available for display
            })
    else:
        # Fallback game list
        games = [
            {'id': 'vault_shelter_v6', 'name': 'VAULT 13 v9.0 - Ultimate Evolution', 'file': 'vault_shelter_v6.py', 'description': 'Full vault simulation', 'category': 'Main Games', 'available': True},
            {'id': 'vault_shelter_v5', 'name': 'VAULT 13 v5.0 - Mega', 'file': 'vault_shelter_v5.py', 'description': '9 game systems', 'category': 'Main Games', 'available': True},
            {'id': 'echo_chambers', 'name': 'Echo Chambers', 'file': 'echo_chambers.py', 'description': 'Timeline navigation', 'category': 'Quantum & Physics', 'available': True},
        ]

    return render_template('index.html', games=games, app_name=APP_DISPLAY_NAME, version=APP_VERSION)


@app.route('/play/<game_file>')
def play(game_file: str):
    """Show terminal page for a specific game."""
    return render_template('terminal.html', game_file=game_file, app_name=APP_DISPLAY_NAME)


@app.route('/api/games')
def api_games():
    """API endpoint to get games list."""
    games = []
    for game_id, game_info in GAME_REGISTRY.items():
        games.append({
            'id': game_info.id,
            'name': game_info.name,
            'file': game_info.file,
            'description': game_info.description,
            'category': game_info.category,
            'available': True
        })
    return jsonify(games)


@app.route('/api/system')
def api_system():
    """API endpoint to get system info."""
    return jsonify({
        'platform': 'vercel',
        'version': APP_VERSION,
        'name': APP_DISPLAY_NAME,
        'websocket_note': 'WebSocket terminal requires local server or WebSocket-enabled hosting'
    })


# Vercel expects the app variable
handler = app
