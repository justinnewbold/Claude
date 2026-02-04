"""
Tests for network_game module
==============================
"""

import pytest
import json
import time
import socket
from unittest.mock import Mock, patch, MagicMock


class TestGameMessage:
    """Test GameMessage dataclass"""

    def test_create_message(self):
        """Test creating a GameMessage"""
        from network_game import GameMessage

        msg = GameMessage(
            msg_type="move",
            data={"x": 1, "y": 2},
            player_id="player1"
        )

        assert msg.msg_type == "move"
        assert msg.data == {"x": 1, "y": 2}
        assert msg.player_id == "player1"
        assert msg.timestamp > 0

    def test_to_json(self):
        """Test serializing to JSON"""
        from network_game import GameMessage

        msg = GameMessage(
            msg_type="move",
            data={"action": "attack"},
            player_id="p1",
            timestamp=12345.0
        )

        json_str = msg.to_json()
        data = json.loads(json_str)

        assert data["msg_type"] == "move"
        assert data["data"]["action"] == "attack"
        assert data["player_id"] == "p1"

    def test_from_json(self):
        """Test deserializing from JSON"""
        from network_game import GameMessage

        json_str = '{"msg_type": "chat", "data": {"message": "hello"}, "timestamp": 123.0, "player_id": "p2"}'

        msg = GameMessage.from_json(json_str)

        assert msg.msg_type == "chat"
        assert msg.data["message"] == "hello"
        assert msg.player_id == "p2"

    def test_from_json_missing_required_fields(self):
        """Test that from_json raises on missing required fields"""
        from network_game import GameMessage

        # Missing msg_type
        with pytest.raises(KeyError):
            GameMessage.from_json('{"data": {}}')

        # Missing data
        with pytest.raises(KeyError):
            GameMessage.from_json('{"msg_type": "move"}')

    def test_from_json_invalid_types(self):
        """Test that from_json raises on invalid field types"""
        from network_game import GameMessage

        # msg_type not a string
        with pytest.raises(TypeError):
            GameMessage.from_json('{"msg_type": 123, "data": {}}')

        # data not a dict
        with pytest.raises(TypeError):
            GameMessage.from_json('{"msg_type": "move", "data": "invalid"}')

    def test_from_json_not_object(self):
        """Test that from_json raises when JSON is not an object"""
        from network_game import GameMessage

        with pytest.raises(TypeError):
            GameMessage.from_json('["a", "list"]')

        with pytest.raises(TypeError):
            GameMessage.from_json('"a string"')


class TestConnectionState:
    """Test ConnectionState enum"""

    def test_states_exist(self):
        """Test all connection states exist"""
        from network_game import ConnectionState

        assert ConnectionState.DISCONNECTED.value == "disconnected"
        assert ConnectionState.HOSTING.value == "hosting"
        assert ConnectionState.WAITING.value == "waiting"
        assert ConnectionState.CONNECTING.value == "connecting"
        assert ConnectionState.CONNECTED.value == "connected"
        assert ConnectionState.ERROR.value == "error"


class TestMessageType:
    """Test MessageType enum"""

    def test_types_exist(self):
        """Test all message types exist"""
        from network_game import MessageType

        assert MessageType.HANDSHAKE.value == "handshake"
        assert MessageType.GAME_START.value == "game_start"
        assert MessageType.MOVE.value == "move"
        assert MessageType.CHAT.value == "chat"
        assert MessageType.DISCONNECT.value == "disconnect"


class TestPlayerInfo:
    """Test PlayerInfo dataclass"""

    def test_create_player_info(self):
        """Test creating player info"""
        from network_game import PlayerInfo

        player = PlayerInfo(
            player_id="p1",
            name="Alice",
            is_host=True
        )

        assert player.player_id == "p1"
        assert player.name == "Alice"
        assert player.is_host is True
        assert player.is_ready is False


class TestNetworkGame:
    """Test NetworkGame class"""

    def test_creation(self):
        """Test creating a NetworkGame instance"""
        from network_game import NetworkGame, ConnectionState

        game = NetworkGame("Test Game", "Player1")

        assert game.game_name == "Test Game"
        assert game.player_name == "Player1"
        assert game.state == ConnectionState.DISCONNECTED
        assert game.is_host is False
        assert game.is_connected is False

    def test_get_local_ip(self):
        """Test getting local IP address"""
        from network_game import NetworkGame

        game = NetworkGame("Test", "Player")
        ip = game.get_local_ip()

        # Should return a valid IP format
        assert ip.count('.') == 3 or ip == "127.0.0.1"

    @patch('socket.socket')
    def test_host_success(self, mock_socket_class):
        """Test successful hosting"""
        from network_game import NetworkGame, ConnectionState

        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        game = NetworkGame("Test", "Host")
        result = game.host(port=5555)

        assert result is True
        assert game.state == ConnectionState.HOSTING
        assert game.is_host is True
        mock_socket.bind.assert_called_once()
        mock_socket.listen.assert_called_once_with(1)

    @patch('socket.socket')
    def test_host_failure(self, mock_socket_class):
        """Test hosting failure"""
        from network_game import NetworkGame, ConnectionState

        mock_socket = MagicMock()
        mock_socket.bind.side_effect = socket.error("Port in use")
        mock_socket_class.return_value = mock_socket

        game = NetworkGame("Test", "Host")
        result = game.host(port=5555)

        assert result is False
        assert game.state == ConnectionState.ERROR

    def test_disconnect(self):
        """Test disconnecting"""
        from network_game import NetworkGame, ConnectionState

        game = NetworkGame("Test", "Player")
        game.state = ConnectionState.CONNECTED
        game._client_socket = MagicMock()

        game.disconnect()

        assert game.state == ConnectionState.DISCONNECTED

    def test_on_message_callback(self):
        """Test message callback registration"""
        from network_game import NetworkGame

        game = NetworkGame("Test", "Player")
        callback = Mock()

        game.on_message(callback)

        assert callback in game._on_message_callbacks


class TestTurnManager:
    """Test TurnManager class"""

    def test_creation(self):
        """Test creating a TurnManager"""
        from network_game import NetworkGame, TurnManager

        network = NetworkGame("Test", "Player")
        turns = TurnManager(network, is_my_turn=True)

        assert turns.is_my_turn is True
        assert turns.turn_number == 0
        assert turns.move_history == []

    def test_make_move_when_my_turn(self):
        """Test making a move when it's my turn"""
        from network_game import NetworkGame, TurnManager

        network = NetworkGame("Test", "Player")
        network.send_move = Mock(return_value=True)

        turns = TurnManager(network, is_my_turn=True)
        result = turns.make_move({"x": 1, "y": 2})

        assert result is True
        assert turns.is_my_turn is False
        assert turns.turn_number == 1
        assert len(turns.move_history) == 1

    def test_make_move_when_not_my_turn(self):
        """Test making a move when it's not my turn"""
        from network_game import NetworkGame, TurnManager

        network = NetworkGame("Test", "Player")

        turns = TurnManager(network, is_my_turn=False)
        result = turns.make_move({"x": 1, "y": 2})

        assert result is False
        assert turns.turn_number == 0


class TestConvenienceFunctions:
    """Test convenience functions"""

    @patch('network_game.NetworkGame')
    def test_host_game(self, mock_class):
        """Test host_game convenience function"""
        from network_game import host_game

        mock_instance = MagicMock()
        mock_instance.host.return_value = True
        mock_class.return_value = mock_instance

        result = host_game("Test", "Host", 5555)

        assert result is not None
        mock_instance.host.assert_called_once_with(5555)

    @patch('network_game.NetworkGame')
    def test_join_game(self, mock_class):
        """Test join_game convenience function"""
        from network_game import join_game

        mock_instance = MagicMock()
        mock_instance.join.return_value = True
        mock_class.return_value = mock_instance

        result = join_game("Test", "192.168.1.1", "Guest", 5555)

        assert result is not None
        mock_instance.join.assert_called_once_with("192.168.1.1", 5555)
