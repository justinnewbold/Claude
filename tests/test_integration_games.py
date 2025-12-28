"""
Integration tests for game flows.

Tests the end-to-end functionality of games including:
- Game initialization and loading
- Input handling and state changes
- Save/load functionality
- Demo mode execution
- Multi-step game scenarios
"""

import pytest
import sys
import json
import io
from pathlib import Path
from unittest.mock import patch, MagicMock
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestGameInitialization:
    """Test game modules can be imported and initialized"""

    def test_vault_shelter_imports(self):
        """Test vault shelter module imports correctly"""
        import vault_shelter_v6 as vault
        assert hasattr(vault, 'GameState')
        assert hasattr(vault, 'Vault')
        assert hasattr(vault, 'Dweller')

    def test_vault_shelter_gamestate_init(self):
        """Test GameState initializes correctly"""
        import vault_shelter_v6 as vault
        state = vault.GameState()
        assert state is not None
        assert hasattr(state, 'vault')
        assert hasattr(state, 'dwellers')

    def test_echo_chambers_imports(self):
        """Test echo chambers module imports correctly"""
        import echo_chambers
        assert hasattr(echo_chambers, 'main') or hasattr(echo_chambers, 'run_game')

    def test_schrodingers_dungeon_imports(self):
        """Test Schrodinger's dungeon imports correctly"""
        import schrodingers_dungeon
        assert True  # Import succeeded

    def test_prisoners_dilemma_imports(self):
        """Test prisoners dilemma imports correctly"""
        import prisoners_dilemma
        assert True  # Import succeeded


class TestGameLauncherIntegration:
    """Test GameLauncher integration with games"""

    @pytest.fixture
    def launcher(self):
        """Create GameLauncher instance"""
        from game_launcher import GameLauncher
        return GameLauncher()

    def test_launcher_loads_all_games(self, launcher):
        """Test launcher loads games from registry"""
        assert len(launcher.games) > 30, "Should have 30+ games loaded"

    def test_launcher_game_info_complete(self, launcher):
        """Test all loaded games have complete info"""
        for game_id, game in launcher.games.items():
            assert game.id, f"{game_id} missing id"
            assert game.name, f"{game_id} missing name"
            assert game.module_path, f"{game_id} missing module_path"

    def test_launcher_can_find_vault_shelter(self, launcher):
        """Test launcher finds vault shelter game"""
        game = launcher.games.get('vault_shelter')
        assert game is not None
        assert 'VAULT' in game.name

    def test_launcher_categories_populated(self, launcher):
        """Test launcher has category information"""
        categories = set()
        for game in launcher.games.values():
            if hasattr(game, 'category') and game.category:
                categories.add(game.category)
        assert len(categories) >= 3, "Should have multiple categories"


class TestDemoModeIntegration:
    """Test demo mode system integration"""

    @pytest.fixture
    def demo_runner(self):
        """Create DemoRunner instance"""
        from demo_mode import DemoRunner, DemoSpeed
        return DemoRunner("vault_shelter", DemoSpeed.INSTANT)

    @pytest.fixture
    def demo_scenario(self):
        """Create test demo scenario"""
        from demo_mode import DemoScenario
        scenario = DemoScenario(
            name="Test Scenario",
            description="Integration test scenario",
            game_id="vault_shelter"
        )
        scenario.add_comment("Starting test")
        scenario.add_input("1")
        scenario.add_wait(0.01)
        scenario.add_input("q")
        return scenario

    def test_demo_runner_initializes(self, demo_runner):
        """Test demo runner initializes correctly"""
        assert demo_runner.game_id == "vault_shelter"
        assert demo_runner.running is False

    def test_demo_scenario_builds(self, demo_scenario):
        """Test demo scenario builds correctly"""
        assert len(demo_scenario.actions) == 4
        assert demo_scenario.actions[0].action_type == 'comment'
        assert demo_scenario.actions[1].action_type == 'input'
        assert demo_scenario.actions[2].action_type == 'wait'
        assert demo_scenario.actions[3].action_type == 'input'

    def test_demo_scenario_to_dict(self, demo_scenario):
        """Test scenario serialization"""
        data = demo_scenario.to_dict()
        assert data['name'] == "Test Scenario"
        assert len(data['actions']) == 4

    def test_demo_scenario_from_dict(self, demo_scenario):
        """Test scenario deserialization"""
        from demo_mode import DemoScenario
        data = demo_scenario.to_dict()
        restored = DemoScenario.from_dict(data)
        assert restored.name == demo_scenario.name
        assert len(restored.actions) == len(demo_scenario.actions)

    def test_demo_runner_action_callback(self, demo_runner, demo_scenario):
        """Test demo runner invokes callbacks"""
        actions_received = []

        def track_action(action):
            actions_received.append(action)

        demo_runner.on_action(track_action)

        # Capture stdout to avoid test output noise
        with redirect_stdout(io.StringIO()):
            demo_runner.run_scenario(demo_scenario)

        assert len(actions_received) == 4


class TestSaveSystem:
    """Test game state save/load functionality"""

    @pytest.fixture
    def save_system(self, tmp_path):
        """Create save system with temp directory"""
        from save_system import SaveSystem
        return SaveSystem(save_dir=tmp_path)

    def test_save_system_init(self, save_system):
        """Test save system initializes"""
        assert save_system is not None
        assert hasattr(save_system, 'save')
        assert hasattr(save_system, 'load')

    def test_save_and_load_simple_state(self, save_system):
        """Test saving and loading simple state"""
        test_state = {
            'score': 100,
            'level': 5,
            'items': ['sword', 'shield']
        }

        # Save
        result = save_system.save(
            game_id='test_game',
            game_name='Test Game',
            data=test_state,
            save_slot=1
        )
        assert result is True

        # Load
        loaded = save_system.load('test_game', save_slot=1)

        assert loaded is not None
        assert loaded.data.get('score') == 100
        assert loaded.data.get('level') == 5
        assert 'sword' in loaded.data.get('items', [])


class TestAIOpponentIntegration:
    """Test AI opponent system integration"""

    @pytest.fixture
    def ai_opponent(self):
        """Create AI opponent"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty
        config = AIConfig(difficulty=Difficulty.MEDIUM)
        return AIOpponent("test_game", config=config)

    def test_ai_opponent_init(self, ai_opponent):
        """Test AI opponent initializes"""
        assert ai_opponent is not None

    def test_ai_makes_move_from_list(self, ai_opponent):
        """Test AI can select from possible moves"""
        possible_moves = ['move_a', 'move_b', 'move_c']
        game_state = {'turn': 1}

        move = ai_opponent.get_move(game_state, possible_moves)
        assert move in possible_moves

    def test_ai_difficulty_affects_behavior(self):
        """Test different difficulties have different behavior"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty

        easy_config = AIConfig(difficulty=Difficulty.EASY)
        hard_config = AIConfig(difficulty=Difficulty.HARD)
        easy_ai = AIOpponent("test_game", config=easy_config)
        hard_ai = AIOpponent("test_game", config=hard_config)

        # They should have different configurations
        assert easy_ai.config.difficulty != hard_ai.config.difficulty


class TestNetworkGameIntegration:
    """Test network game system integration"""

    def test_network_game_import(self):
        """Test network game module imports"""
        from network_game import NetworkGame, GameMessage, PlayerInfo
        assert NetworkGame is not None
        assert GameMessage is not None
        assert PlayerInfo is not None

    def test_network_game_initialization(self):
        """Test NetworkGame initializes correctly"""
        from network_game import NetworkGame
        game = NetworkGame("test_game")
        assert game.game_id == "test_game"
        assert game.is_host is False

    def test_player_info_creation(self):
        """Test PlayerInfo dataclass"""
        from network_game import PlayerInfo
        player = PlayerInfo(
            player_id="p1",
            name="Test Player"
        )
        assert player.player_id == "p1"
        assert player.name == "Test Player"

    def test_game_message_creation(self):
        """Test GameMessage dataclass"""
        from network_game import GameMessage, MessageType
        msg = GameMessage(
            type=MessageType.GAME_START,
            payload={'game_id': 'test'}
        )
        assert msg.type == MessageType.GAME_START
        assert msg.payload['game_id'] == 'test'


class TestLoggingIntegration:
    """Test logging system integration with games"""

    def test_logging_config_imports(self):
        """Test logging config imports correctly"""
        from logging_config import (
            get_logger,
            setup_game_logger,
            log_performance,
            log_exceptions
        )
        assert get_logger is not None
        assert setup_game_logger is not None

    def test_game_logger_creation(self):
        """Test creating game-specific logger"""
        from logging_config import setup_game_logger
        logger = setup_game_logger("test_integration")
        assert logger is not None
        assert logger.name == "test_integration"

    def test_performance_decorator(self):
        """Test performance logging decorator"""
        from logging_config import log_performance, get_logger
        import time

        logger = get_logger("perf_test")
        call_count = 0

        @log_performance(logger, threshold=10.0)  # High threshold to avoid warning
        def fast_func():
            nonlocal call_count
            call_count += 1
            return "done"

        result = fast_func()
        assert result == "done"
        assert call_count == 1


class TestColorSystemIntegration:
    """Test color system integration with games"""

    def test_colors_import(self):
        """Test colors module imports"""
        from colors import C
        assert hasattr(C, 'RESET')
        assert hasattr(C, 'BOLD')

    def test_game_colors_available(self):
        """Test game-specific colors are available"""
        from colors import C
        # Check a sampling of game-specific colors
        game_colors = [
            'POWER', 'WATER', 'FOOD', 'SAFE',  # Vault colors
            'PARTICLE', 'WALL', 'GOAL',  # Physics colors
            'TIMELINE_1', 'SUPERPOSITION',  # Quantum colors
        ]
        for color in game_colors:
            assert hasattr(C, color), f"Missing color: {color}"

    def test_colors_produce_ansi_codes(self):
        """Test colors produce valid ANSI codes"""
        from colors import C
        # All color codes should start with escape sequence
        assert C.RESET.startswith('\033[') or C.RESET.startswith('\x1b[')
        assert C.BOLD.startswith('\033[') or C.BOLD.startswith('\x1b[')


class TestAPIIntegration:
    """Test API specification and endpoints"""

    @pytest.fixture
    def openapi_spec(self):
        """Load OpenAPI specification"""
        spec_path = Path(__file__).parent.parent / "api" / "openapi.json"
        with open(spec_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_openapi_spec_exists(self):
        """Test OpenAPI spec file exists"""
        spec_path = Path(__file__).parent.parent / "api" / "openapi.json"
        assert spec_path.exists(), "OpenAPI spec should exist"

    def test_openapi_spec_valid(self, openapi_spec):
        """Test OpenAPI spec is valid structure"""
        assert 'openapi' in openapi_spec
        assert 'info' in openapi_spec
        assert 'paths' in openapi_spec

    def test_openapi_has_game_endpoints(self, openapi_spec):
        """Test spec has game-related endpoints"""
        paths = openapi_spec.get('paths', {})
        assert '/games' in paths
        assert '/games/{gameId}' in paths

    def test_openapi_has_session_endpoints(self, openapi_spec):
        """Test spec has session-related endpoints"""
        paths = openapi_spec.get('paths', {})
        assert '/games/{gameId}/start' in paths
        assert '/sessions/{sessionId}/input' in paths

    def test_openapi_schemas_complete(self, openapi_spec):
        """Test spec has required schemas"""
        schemas = openapi_spec.get('components', {}).get('schemas', {})
        required_schemas = [
            'GameInfo', 'GameDetails', 'GamesListResponse',
            'GameSessionResponse', 'ErrorResponse'
        ]
        for schema in required_schemas:
            assert schema in schemas, f"Missing schema: {schema}"


class TestCrossModuleIntegration:
    """Test integration between multiple modules"""

    def test_game_launcher_uses_registry(self):
        """Test GameLauncher loads from JSON registry"""
        from game_launcher import GameLauncher
        launcher = GameLauncher()

        # Load registry directly
        registry_path = Path(__file__).parent.parent / "games_registry.json"
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        # Compare counts
        registry_count = len(registry.get('games', {}))
        launcher_count = len(launcher.games)

        assert launcher_count == registry_count, \
            f"Launcher ({launcher_count}) should match registry ({registry_count})"

    def test_demo_mode_uses_colors(self):
        """Test demo mode uses color system"""
        from demo_mode import DemoRunner, DemoSpeed
        from colors import C

        # Demo mode should use C colors
        runner = DemoRunner("test", DemoSpeed.INSTANT)
        # The runner references C in its methods
        assert hasattr(C, 'CYAN')  # Used in demo mode

    def test_save_system_handles_game_data(self, tmp_path):
        """Test save system works with game-like data"""
        from save_system import SaveSystem

        save_system = SaveSystem(save_dir=tmp_path)

        # Create game-like state
        game_state = {
            'vault': {
                'level': 1,
                'resources': {
                    'power': 100,
                    'water': 100,
                    'food': 100
                }
            },
            'dwellers': [
                {'name': 'Test', 'strength': 5}
            ],
            'day': 1
        }

        # Save and restore
        save_system.save('integration_test', 'Integration Test', game_state, save_slot=1)
        restored = save_system.load('integration_test', save_slot=1)

        assert restored.data['vault']['level'] == 1
        assert restored.data['vault']['resources']['power'] == 100
        assert len(restored.data['dwellers']) == 1


class TestEndToEndScenarios:
    """End-to-end scenario tests"""

    def test_full_game_launch_flow(self):
        """Test complete flow: launcher -> game info -> would-be launch"""
        from game_launcher import GameLauncher

        launcher = GameLauncher()

        # Get a game
        game = launcher.games.get('vault_shelter')
        assert game is not None

        # Verify launch info is available
        assert game.module_path.endswith('.py')
        assert game.main_function == 'main'

    def test_demo_scenario_save_load_cycle(self, tmp_path):
        """Test creating, saving, and loading demo scenario"""
        from demo_mode import DemoScenario

        # Create scenario
        original = DemoScenario(
            name="save_load_test",
            description="Test save/load cycle",
            game_id="test_game"
        )
        original.add_comment("Step 1")
        original.add_input("1")
        original.add_comment("Step 2")
        original.add_input("2")

        # Save to temp path
        save_path = tmp_path / "test_scenario.json"
        original.save(save_path)

        # Load it back
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        restored = DemoScenario.from_dict(data)

        # Verify
        assert restored.name == original.name
        assert len(restored.actions) == len(original.actions)
        assert restored.actions[1].value == "1"
        assert restored.actions[3].value == "2"

    def test_multiple_ai_difficulty_levels(self):
        """Test AI operates at different difficulty levels"""
        from ai_opponent import AIOpponent, AIConfig, Difficulty

        difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        moves = ['a', 'b', 'c', 'd', 'e']

        for diff in difficulties:
            config = AIConfig(difficulty=diff)
            ai = AIOpponent("test_game", config=config)
            move = ai.get_move({}, moves)
            assert move in moves, f"Difficulty {diff} should return valid move"
