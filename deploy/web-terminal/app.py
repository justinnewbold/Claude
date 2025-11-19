#!/usr/bin/env python3
"""
Web-based terminal for the Innovative Game Collection
Allows playing all games through a web browser
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

class Terminal:
    """Manages a pseudo-terminal for running games"""

    def __init__(self):
        self.fd = None
        self.child_pid = None

    def spawn(self, game_file):
        """Spawn a game in a pseudo-terminal"""
        (child_pid, fd) = pty.fork()

        if child_pid == 0:
            # Child process - run the game
            os.execvp('python3', ['python3', f'/home/user/Claude/{game_file}'])
        else:
            # Parent process - store the terminal
            self.child_pid = child_pid
            self.fd = fd
            self.set_terminal_size(80, 24)
            return fd

    def set_terminal_size(self, cols, rows):
        """Set the terminal size"""
        if self.fd:
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def read(self):
        """Read output from terminal"""
        if self.fd:
            try:
                return os.read(self.fd, 10240).decode('utf-8', errors='replace')
            except:
                return None
        return None

    def write(self, data):
        """Write input to terminal"""
        if self.fd:
            os.write(self.fd, data.encode())


# Store active terminals
terminals = {}

@app.route('/')
def index():
    """Show game selection page"""
    games = [
        # MAIN GAMES
        {'id': 'vault_shelter_v4', 'name': '🏛️ VAULT 13 v4.0 ULTIMATE - Quest/Explore/Skills (NEW!)', 'file': 'vault_shelter_v4.py'},
        {'id': 'vault_shelter_ai', 'name': '🏛️ VAULT 13 v3.0 AI Edition - With AI Advisor', 'file': 'vault_shelter_ai.py'},
        {'id': 'vault_shelter', 'name': '🏛️ VAULT 13 v2.0 - Survival Protocol', 'file': 'vault_shelter.py'},

        # MINI GAMES - Philosophical & Computational Thought Experiments
        {'id': 'echo_chambers', 'name': 'Echo Chambers', 'file': 'echo_chambers.py'},
        {'id': 'code_archaeology', 'name': 'Code Archaeology', 'file': 'code_archaeology.py'},
        {'id': 'infinite_library', 'name': 'The Infinite Library', 'file': 'infinite_library.py'},
        {'id': 'forking_paths', 'name': 'The Garden of Forking Paths', 'file': 'forking_paths.py'},
        {'id': 'last_recursion', 'name': 'The Last Recursion', 'file': 'last_recursion.py'},
        {'id': 'schrodingers_dungeon', 'name': 'Schrödinger\'s Dungeon', 'file': 'schrodingers_dungeon.py'},
        {'id': 'emergence_engine', 'name': 'The Emergence Engine', 'file': 'emergence_engine.py'},
        {'id': 'ship_of_theseus', 'name': 'The Ship of Theseus', 'file': 'ship_of_theseus.py'},
        {'id': 'butterfly_effect', 'name': 'The Butterfly Effect', 'file': 'butterfly_effect.py'},
        {'id': 'syntax_tree_climber', 'name': 'Syntax Tree Climber', 'file': 'syntax_tree_climber.py'},
        {'id': 'entanglement', 'name': 'Entanglement', 'file': 'entanglement.py'},
    ]
    return render_template('index.html', games=games)

@app.route('/play/<game_file>')
def play(game_file):
    """Show terminal page for a specific game"""
    return render_template('terminal.html', game_file=game_file)

@socketio.on('start')
def handle_start(data):
    """Start a game session"""
    game_file = data['game_file']
    session_id = request.sid

    terminal = Terminal()
    fd = terminal.spawn(game_file)
    terminals[session_id] = terminal

    # Start reading output
    socketio.start_background_task(read_output, session_id)

@socketio.on('input')
def handle_input(data):
    """Handle input from web terminal"""
    session_id = request.sid
    if session_id in terminals:
        terminals[session_id].write(data['input'])

@socketio.on('resize')
def handle_resize(data):
    """Handle terminal resize"""
    session_id = request.sid
    if session_id in terminals:
        terminals[session_id].set_terminal_size(data['cols'], data['rows'])

@socketio.on('disconnect')
def handle_disconnect():
    """Clean up terminal on disconnect"""
    session_id = request.sid
    if session_id in terminals:
        terminal = terminals[session_id]
        if terminal.child_pid:
            try:
                os.kill(terminal.child_pid, 9)
            except:
                pass
        if terminal.fd:
            os.close(terminal.fd)
        del terminals[session_id]

def read_output(session_id):
    """Background task to read terminal output"""
    while session_id in terminals:
        terminal = terminals[session_id]
        if terminal.fd:
            try:
                # Use select to avoid blocking
                ready, _, _ = select.select([terminal.fd], [], [], 0.1)
                if ready:
                    output = terminal.read()
                    if output:
                        socketio.emit('output', {'output': output}, room=session_id)
                    else:
                        break
            except:
                break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
