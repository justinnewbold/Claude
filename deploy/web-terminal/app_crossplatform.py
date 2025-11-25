#!/usr/bin/env python3
"""
Cross-Platform Web Terminal for VAULT 13 Game Collection
=========================================================
Allows playing all games through a web browser on any platform.
Supports: Windows, macOS, Linux

Uses subprocess instead of PTY for cross-platform compatibility.
"""

import os
import sys
import json
import signal
import threading
import subprocess
import queue
from pathlib import Path
from typing import Dict, Optional, Any

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from config import GAME_REGISTRY, paths, APP_DISPLAY_NAME, APP_VERSION
    from platform_utils import is_windows, get_python_executable, get_system_info
except ImportError:
    # Fallback definitions
    GAME_REGISTRY = {}
    APP_DISPLAY_NAME = "VAULT 13"
    APP_VERSION = "9.0"

    def is_windows():
        return os.name == 'nt'

    def get_python_executable():
        return sys.executable

    def get_system_info():
        return {}

    class PathsFallback:
        game_root = Path(__file__).parent.parent.parent

    paths = PathsFallback()

# =============================================================================
# FLASK APPLICATION SETUP
# =============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vault13-secret-key-change-in-production')

# Configure SocketIO with appropriate async mode
async_mode = None
if is_windows():
    # Windows works better with threading mode
    async_mode = 'threading'
else:
    # Unix systems can use eventlet
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        async_mode = 'threading'

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode=async_mode,
    ping_timeout=60,
    ping_interval=25
)


# =============================================================================
# CROSS-PLATFORM TERMINAL CLASS
# =============================================================================

class CrossPlatformTerminal:
    """
    Cross-platform terminal emulator using subprocess.
    Works on Windows, macOS, and Linux.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.process: Optional[subprocess.Popen] = None
        self.output_queue: queue.Queue = queue.Queue()
        self.running = False
        self.reader_thread: Optional[threading.Thread] = None
        self.cols = 80
        self.rows = 24

    def spawn(self, game_file: str) -> bool:
        """
        Spawn a game process.
        Returns True if successful.
        """
        try:
            # Determine the game path
            game_path = paths.game_root / game_file
            if not game_path.exists():
                self.output_queue.put(f"\r\nError: Game file not found: {game_file}\r\n")
                return False

            # Get Python executable
            python_exe = get_python_executable()

            # Set up environment
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'  # Disable output buffering
            env['TERM'] = 'xterm-256color'
            env['COLUMNS'] = str(self.cols)
            env['LINES'] = str(self.rows)

            # Platform-specific process creation
            if is_windows():
                # Windows: Use CREATE_NEW_PROCESS_GROUP for better signal handling
                self.process = subprocess.Popen(
                    [python_exe, '-u', str(game_path)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=env,
                    cwd=str(paths.game_root),
                    bufsize=0,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                # Unix: Standard subprocess with unbuffered I/O
                self.process = subprocess.Popen(
                    [python_exe, '-u', str(game_path)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=env,
                    cwd=str(paths.game_root),
                    bufsize=0,
                    start_new_session=True
                )

            self.running = True

            # Start output reader thread
            self.reader_thread = threading.Thread(
                target=self._read_output,
                daemon=True
            )
            self.reader_thread.start()

            return True

        except Exception as e:
            self.output_queue.put(f"\r\nError starting game: {e}\r\n")
            return False

    def _read_output(self):
        """Background thread to read process output."""
        try:
            while self.running and self.process and self.process.poll() is None:
                # Read available data
                data = self.process.stdout.read(4096)
                if data:
                    # Decode and queue the output
                    text = data.decode('utf-8', errors='replace')
                    self.output_queue.put(text)
                else:
                    break
        except Exception as e:
            self.output_queue.put(f"\r\n[Terminal Error: {e}]\r\n")
        finally:
            self.running = False
            # Signal process ended
            self.output_queue.put(None)

    def write(self, data: str):
        """Write input to the process."""
        if self.process and self.process.stdin and self.running:
            try:
                self.process.stdin.write(data.encode('utf-8'))
                self.process.stdin.flush()
            except (BrokenPipeError, OSError):
                self.running = False

    def resize(self, cols: int, rows: int):
        """
        Handle terminal resize.
        Note: This doesn't actually resize subprocess terminals,
        but we store the values for reference.
        """
        self.cols = cols
        self.rows = rows

    def get_output(self) -> Optional[str]:
        """Get queued output (non-blocking)."""
        try:
            return self.output_queue.get_nowait()
        except queue.Empty:
            return None

    def is_alive(self) -> bool:
        """Check if the process is still running."""
        return self.running and self.process and self.process.poll() is None

    def terminate(self):
        """Terminate the process."""
        self.running = False
        if self.process:
            try:
                if is_windows():
                    # Windows: Use taskkill for proper termination
                    subprocess.run(
                        ['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                        capture_output=True
                    )
                else:
                    # Unix: Send SIGTERM to process group
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except (ProcessLookupError, OSError):
                pass

            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                pass


# =============================================================================
# ACTIVE SESSIONS
# =============================================================================

terminals: Dict[str, CrossPlatformTerminal] = {}
output_threads: Dict[str, threading.Thread] = {}


def output_emitter(session_id: str):
    """Background task to emit terminal output to client."""
    terminal = terminals.get(session_id)
    if not terminal:
        return

    while session_id in terminals:
        output = terminal.get_output()
        if output is None:
            # Process ended
            socketio.emit('output', {'output': '\r\n[Game ended]\r\n'}, room=session_id)
            break
        elif output:
            socketio.emit('output', {'output': output}, room=session_id)
        else:
            socketio.sleep(0.05)  # Small delay to prevent busy-waiting


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    """Show game selection page."""
    # Build games list from registry or fallback
    games = []

    if GAME_REGISTRY:
        # Group by category
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
            game_path = paths.game_root / game_info.file
            games.append({
                'id': game_info.id,
                'name': game_info.name,
                'file': game_info.file,
                'description': game_info.description,
                'category': categories.get(game_info.category, game_info.category),
                'available': game_path.exists()
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
        game_path = paths.game_root / game_info.file
        games.append({
            'id': game_info.id,
            'name': game_info.name,
            'file': game_info.file,
            'description': game_info.description,
            'category': game_info.category,
            'available': game_path.exists()
        })
    return jsonify(games)


@app.route('/api/system')
def api_system():
    """API endpoint to get system info."""
    return jsonify(get_system_info())


# =============================================================================
# SOCKET.IO EVENTS
# =============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")


@socketio.on('start')
def handle_start(data: Dict[str, Any]):
    """Start a game session."""
    game_file = data.get('game_file', '')
    session_id = request.sid

    # Clean up any existing terminal for this session
    if session_id in terminals:
        terminals[session_id].terminate()
        del terminals[session_id]

    # Create new terminal
    terminal = CrossPlatformTerminal(session_id)
    terminals[session_id] = terminal

    if terminal.spawn(game_file):
        emit('output', {'output': f'\r\nStarting {game_file}...\r\n\r\n'})
        # Start output emitter
        socketio.start_background_task(output_emitter, session_id)
    else:
        emit('output', {'output': '\r\nFailed to start game.\r\n'})


@socketio.on('input')
def handle_input(data: Dict[str, Any]):
    """Handle input from web terminal."""
    session_id = request.sid
    if session_id in terminals:
        input_data = data.get('input', '')
        terminals[session_id].write(input_data)


@socketio.on('resize')
def handle_resize(data: Dict[str, Any]):
    """Handle terminal resize."""
    session_id = request.sid
    if session_id in terminals:
        cols = data.get('cols', 80)
        rows = data.get('rows', 24)
        terminals[session_id].resize(cols, rows)


@socketio.on('disconnect')
def handle_disconnect():
    """Clean up terminal on disconnect."""
    session_id = request.sid
    print(f"Client disconnected: {session_id}")

    if session_id in terminals:
        terminals[session_id].terminate()
        del terminals[session_id]


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run the web terminal server."""
    import argparse

    parser = argparse.ArgumentParser(description='VAULT 13 Web Terminal Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  {APP_DISPLAY_NAME} - Web Terminal Server")
    print(f"  Version: {APP_VERSION}")
    print(f"{'='*60}")
    print(f"\n  Server starting at http://{args.host}:{args.port}")
    print(f"  Press Ctrl+C to stop\n")

    socketio.run(
        app,
        host=args.host,
        port=args.port,
        debug=args.debug,
        use_reloader=args.debug,
        log_output=True
    )


if __name__ == '__main__':
    main()
