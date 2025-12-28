#!/usr/bin/env python3
"""
Network Game Support
====================
Provides multiplayer/network capabilities for competitive games.

Features:
- Simple socket-based networking
- Host/Join game modes
- Turn-based synchronization
- Message passing between players
- Lobby system for matchmaking

Usage:
    from network_game import NetworkGame, GameMessage

    # Host a game
    game = NetworkGame("My Game")
    game.host(port=5555)
    game.wait_for_player()

    # Or join a game
    game = NetworkGame("My Game")
    game.join("192.168.1.100", port=5555)

    # Send/receive moves
    game.send_move({"action": "place", "x": 3, "y": 4})
    opponent_move = game.receive_move()
"""

import socket
import json
import threading
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, Callable, List
from enum import Enum
from logging_config import get_logger

logger = get_logger(__name__)


class ConnectionState(Enum):
    """State of the network connection"""
    DISCONNECTED = "disconnected"
    HOSTING = "hosting"
    WAITING = "waiting"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


class MessageType(Enum):
    """Types of network messages"""
    HANDSHAKE = "handshake"
    GAME_START = "game_start"
    MOVE = "move"
    CHAT = "chat"
    SYNC = "sync"
    DISCONNECT = "disconnect"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


@dataclass
class GameMessage:
    """A message sent between players"""
    msg_type: str
    data: Dict[str, Any]
    timestamp: float = 0.0
    player_id: str = ""

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()

    def to_json(self) -> str:
        """Serialize to JSON"""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> 'GameMessage':
        """Deserialize from JSON"""
        data = json.loads(json_str)
        return cls(**data)


@dataclass
class PlayerInfo:
    """Information about a player"""
    player_id: str
    name: str
    is_host: bool = False
    is_ready: bool = False


class NetworkGame:
    """
    Manages network connectivity for multiplayer games.

    Supports both hosting and joining games with simple
    turn-based message passing.
    """

    def __init__(self, game_name: str, player_name: str = "Player"):
        self.game_name = game_name
        self.player_name = player_name
        self.player_id = f"{player_name}_{int(time.time())}"

        self.state = ConnectionState.DISCONNECTED
        self.is_host = False

        self._socket: Optional[socket.socket] = None
        self._client_socket: Optional[socket.socket] = None
        self._peer_address: Optional[tuple] = None

        self._receive_thread: Optional[threading.Thread] = None
        self._running = False

        self._message_queue: List[GameMessage] = []
        self._message_lock = threading.Lock()

        self._on_message_callbacks: List[Callable[[GameMessage], None]] = []
        self._on_connect_callback: Optional[Callable[[PlayerInfo], None]] = None
        self._on_disconnect_callback: Optional[Callable[[], None]] = None

        self.opponent_info: Optional[PlayerInfo] = None
        self.latency_ms: float = 0.0

        logger.info(f"NetworkGame initialized: {game_name}")

    # === Connection Management ===

    def host(self, port: int = 5555, timeout: float = 60.0) -> bool:
        """
        Host a game and wait for a player to connect.

        Args:
            port: Port to listen on
            timeout: How long to wait for a connection

        Returns:
            True if a player connected, False otherwise
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.settimeout(timeout)
            self._socket.bind(('', port))
            self._socket.listen(1)

            self.state = ConnectionState.HOSTING
            self.is_host = True

            logger.info(f"Hosting game on port {port}")
            return True

        except socket.error as e:
            logger.error(f"Failed to host: {e}")
            self.state = ConnectionState.ERROR
            return False

    def wait_for_player(self) -> bool:
        """Wait for a player to connect to hosted game"""
        if self.state != ConnectionState.HOSTING:
            return False

        self.state = ConnectionState.WAITING
        try:
            self._client_socket, self._peer_address = self._socket.accept()
            logger.info(f"Player connected from {self._peer_address}")

            # Perform handshake
            if self._perform_handshake():
                self.state = ConnectionState.CONNECTED
                self._start_receive_thread()
                return True
            else:
                self.state = ConnectionState.ERROR
                return False

        except socket.timeout:
            logger.info("Connection timeout")
            self.state = ConnectionState.DISCONNECTED
            return False
        except socket.error as e:
            logger.error(f"Connection error: {e}")
            self.state = ConnectionState.ERROR
            return False

    def join(self, host: str, port: int = 5555, timeout: float = 10.0) -> bool:
        """
        Join a hosted game.

        Args:
            host: Host IP address
            port: Port to connect to
            timeout: Connection timeout

        Returns:
            True if connected successfully
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(timeout)
            self._socket.connect((host, port))

            self.state = ConnectionState.CONNECTING
            self.is_host = False
            self._client_socket = self._socket

            logger.info(f"Connected to {host}:{port}")

            # Perform handshake
            if self._perform_handshake():
                self.state = ConnectionState.CONNECTED
                self._start_receive_thread()
                return True
            else:
                self.state = ConnectionState.ERROR
                return False

        except socket.error as e:
            logger.error(f"Failed to join: {e}")
            self.state = ConnectionState.ERROR
            return False

    def disconnect(self):
        """Disconnect from the game"""
        self._running = False

        # Send disconnect message
        try:
            self._send_message(GameMessage(
                msg_type=MessageType.DISCONNECT.value,
                data={"reason": "Player disconnected"},
                player_id=self.player_id
            ))
        except Exception:
            pass

        # Close sockets
        if self._client_socket:
            try:
                self._client_socket.close()
            except Exception:
                pass
            self._client_socket = None

        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

        self.state = ConnectionState.DISCONNECTED
        logger.info("Disconnected")

        if self._on_disconnect_callback:
            self._on_disconnect_callback()

    # === Messaging ===

    def send_move(self, move_data: Dict[str, Any]) -> bool:
        """
        Send a game move to the opponent.

        Args:
            move_data: Dictionary containing move information

        Returns:
            True if sent successfully
        """
        return self._send_message(GameMessage(
            msg_type=MessageType.MOVE.value,
            data=move_data,
            player_id=self.player_id
        ))

    def receive_move(self, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """
        Wait for and receive a move from the opponent.

        Args:
            timeout: How long to wait for a move

        Returns:
            Move data dictionary, or None if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            msg = self._get_queued_message(MessageType.MOVE)
            if msg:
                return msg.data

            time.sleep(0.05)

        return None

    def send_chat(self, message: str) -> bool:
        """Send a chat message to the opponent"""
        return self._send_message(GameMessage(
            msg_type=MessageType.CHAT.value,
            data={"message": message},
            player_id=self.player_id
        ))

    def send_sync(self, game_state: Dict[str, Any]) -> bool:
        """Send game state synchronization data"""
        return self._send_message(GameMessage(
            msg_type=MessageType.SYNC.value,
            data=game_state,
            player_id=self.player_id
        ))

    # === Callbacks ===

    def on_message(self, callback: Callable[[GameMessage], None]):
        """Register a callback for incoming messages"""
        self._on_message_callbacks.append(callback)

    def on_connect(self, callback: Callable[[PlayerInfo], None]):
        """Register a callback for when a player connects"""
        self._on_connect_callback = callback

    def on_disconnect(self, callback: Callable[[], None]):
        """Register a callback for disconnection"""
        self._on_disconnect_callback = callback

    # === Internal Methods ===

    def _perform_handshake(self) -> bool:
        """Exchange player info with peer"""
        try:
            # Send our info
            handshake = GameMessage(
                msg_type=MessageType.HANDSHAKE.value,
                data={
                    "player_name": self.player_name,
                    "player_id": self.player_id,
                    "game_name": self.game_name,
                    "is_host": self.is_host
                },
                player_id=self.player_id
            )
            self._send_message(handshake)

            # Receive opponent info
            response_data = self._receive_raw()
            if response_data:
                response = GameMessage.from_json(response_data)
                if response.msg_type == MessageType.HANDSHAKE.value:
                    self.opponent_info = PlayerInfo(
                        player_id=response.data.get("player_id", "unknown"),
                        name=response.data.get("player_name", "Opponent"),
                        is_host=response.data.get("is_host", False)
                    )
                    logger.info(f"Handshake complete: {self.opponent_info.name}")

                    if self._on_connect_callback:
                        self._on_connect_callback(self.opponent_info)

                    return True

            return False

        except Exception as e:
            logger.error(f"Handshake failed: {e}")
            return False

    def _send_message(self, message: GameMessage) -> bool:
        """Send a message to the peer"""
        if not self._client_socket:
            return False

        try:
            data = message.to_json().encode('utf-8')
            # Send length prefix (4 bytes)
            length = len(data)
            self._client_socket.sendall(length.to_bytes(4, 'big'))
            self._client_socket.sendall(data)
            return True
        except socket.error as e:
            logger.error(f"Send failed: {e}")
            return False

    def _receive_raw(self) -> Optional[str]:
        """Receive raw message data"""
        if not self._client_socket:
            return None

        try:
            # Read length prefix
            length_data = self._client_socket.recv(4)
            if not length_data:
                return None

            length = int.from_bytes(length_data, 'big')

            # Read message data
            data = b''
            while len(data) < length:
                chunk = self._client_socket.recv(length - len(data))
                if not chunk:
                    return None
                data += chunk

            return data.decode('utf-8')

        except socket.error:
            return None

    def _start_receive_thread(self):
        """Start background thread for receiving messages"""
        self._running = True
        self._receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._receive_thread.start()

    def _receive_loop(self):
        """Background loop for receiving messages"""
        while self._running and self.state == ConnectionState.CONNECTED:
            try:
                data = self._receive_raw()
                if data:
                    message = GameMessage.from_json(data)
                    self._handle_message(message)
                else:
                    # Connection closed
                    break
            except Exception as e:
                logger.error(f"Receive error: {e}")
                break

        if self._running:
            self.disconnect()

    def _handle_message(self, message: GameMessage):
        """Handle an incoming message"""
        # Handle ping/pong for latency
        if message.msg_type == MessageType.PING.value:
            self._send_message(GameMessage(
                msg_type=MessageType.PONG.value,
                data={"ping_time": message.timestamp},
                player_id=self.player_id
            ))
            return

        if message.msg_type == MessageType.PONG.value:
            ping_time = message.data.get("ping_time")
            if ping_time is not None:
                self.latency_ms = (time.time() - ping_time) * 1000
            return

        if message.msg_type == MessageType.DISCONNECT.value:
            logger.info("Opponent disconnected")
            self.disconnect()
            return

        # Queue message for processing
        with self._message_lock:
            self._message_queue.append(message)

        # Call callbacks
        for callback in self._on_message_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    def _get_queued_message(self, msg_type: MessageType) -> Optional[GameMessage]:
        """Get a message of specific type from queue"""
        with self._message_lock:
            for i, msg in enumerate(self._message_queue):
                if msg.msg_type == msg_type.value:
                    return self._message_queue.pop(i)
        return None

    # === Utility Methods ===

    def ping(self) -> float:
        """Measure latency to peer"""
        self._send_message(GameMessage(
            msg_type=MessageType.PING.value,
            data={},
            player_id=self.player_id
        ))
        time.sleep(0.5)  # Wait for pong
        return self.latency_ms

    def get_local_ip(self) -> str:
        """Get local IP address for hosting"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    @property
    def is_connected(self) -> bool:
        """Check if connected to opponent"""
        return self.state == ConnectionState.CONNECTED


class TurnManager:
    """
    Manages turn-based gameplay over network.

    Usage:
        turns = TurnManager(network_game, is_my_turn=True)

        while game_running:
            if turns.is_my_turn:
                move = get_player_move()
                turns.make_move(move)
            else:
                move = turns.wait_for_opponent_move()
                apply_opponent_move(move)
    """

    def __init__(self, network: NetworkGame, is_my_turn: bool = True):
        self.network = network
        self.is_my_turn = is_my_turn
        self.turn_number = 0
        self.move_history: List[Dict[str, Any]] = []

    def make_move(self, move_data: Dict[str, Any]) -> bool:
        """Make a move and send to opponent"""
        if not self.is_my_turn:
            return False

        move_data["turn_number"] = self.turn_number
        success = self.network.send_move(move_data)

        if success:
            self.move_history.append(move_data)
            self.turn_number += 1
            self.is_my_turn = False

        return success

    def wait_for_opponent_move(self, timeout: float = 60.0) -> Optional[Dict[str, Any]]:
        """Wait for opponent's move"""
        if self.is_my_turn:
            return None

        move = self.network.receive_move(timeout)

        if move:
            self.move_history.append(move)
            self.turn_number += 1
            self.is_my_turn = True

        return move


# Convenience functions
def host_game(game_name: str, player_name: str = "Host",
              port: int = 5555) -> Optional[NetworkGame]:
    """Convenience function to host a game"""
    game = NetworkGame(game_name, player_name)
    if game.host(port):
        return game
    return None


def join_game(game_name: str, host: str, player_name: str = "Player",
              port: int = 5555) -> Optional[NetworkGame]:
    """Convenience function to join a game"""
    game = NetworkGame(game_name, player_name)
    if game.join(host, port):
        return game
    return None


if __name__ == '__main__':
    import sys

    print("Network Game Demo")
    print("=" * 40)

    if len(sys.argv) > 1 and sys.argv[1] == "host":
        print("Hosting game...")
        game = NetworkGame("Demo Game", "Host")
        game.host(5555)
        print(f"Your IP: {game.get_local_ip()}")
        print("Waiting for player...")

        if game.wait_for_player():
            print(f"Player connected: {game.opponent_info.name}")
            print("Sending test move...")
            game.send_move({"test": "hello from host"})
            response = game.receive_move()
            print(f"Received: {response}")
            game.disconnect()
        else:
            print("No player connected")

    elif len(sys.argv) > 2 and sys.argv[1] == "join":
        host_ip = sys.argv[2]
        print(f"Joining game at {host_ip}...")
        game = NetworkGame("Demo Game", "Guest")

        if game.join(host_ip, 5555):
            print(f"Connected to: {game.opponent_info.name}")
            move = game.receive_move()
            print(f"Received: {move}")
            game.send_move({"test": "hello from guest"})
            game.disconnect()
        else:
            print("Could not connect")

    else:
        print("Usage:")
        print("  python network_game.py host        - Host a game")
        print("  python network_game.py join <ip>   - Join a game")
