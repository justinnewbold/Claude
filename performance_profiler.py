#!/usr/bin/env python3
"""
Performance Profiler for VAULT 13 Game Collection

Profiles save/load operations, event generation, and game systems
to identify performance bottlenecks.

Usage:
    python performance_profiler.py [--full] [--save-load] [--events] [--games]
"""

import time
import json
import cProfile
import pstats
import io
import sys
import os
import statistics
from typing import Dict, List, Any, Callable
from dataclasses import dataclass, field
from contextlib import contextmanager

try:
    from colors import C
    from platform_utils import clear_screen
except ImportError:
    class C:
        RESET = BOLD = DIM = HEADER = SUCCESS = WARNING = DANGER = INFO = ""
    def clear_screen():
        pass


@dataclass
class TimingResult:
    """Result of a timing test"""
    name: str
    times: List[float] = field(default_factory=list)

    @property
    def mean(self) -> float:
        return statistics.mean(self.times) if self.times else 0

    @property
    def median(self) -> float:
        return statistics.median(self.times) if self.times else 0

    @property
    def min_time(self) -> float:
        return min(self.times) if self.times else 0

    @property
    def max_time(self) -> float:
        return max(self.times) if self.times else 0

    @property
    def stdev(self) -> float:
        return statistics.stdev(self.times) if len(self.times) > 1 else 0


class PerformanceProfiler:
    """Performance profiler for game systems"""

    def __init__(self):
        self.results: Dict[str, TimingResult] = {}
        self.profile_data: Dict[str, str] = {}

    @contextmanager
    def timer(self, name: str):
        """Context manager for timing operations"""
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            if name not in self.results:
                self.results[name] = TimingResult(name)
            self.results[name].times.append(elapsed)

    def time_function(self, name: str, func: Callable, *args, iterations: int = 10, **kwargs):
        """Time a function over multiple iterations"""
        result = TimingResult(name)

        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            result.times.append(elapsed)

        self.results[name] = result
        return result

    def profile_function(self, name: str, func: Callable, *args, **kwargs):
        """Profile a function with cProfile"""
        profiler = cProfile.Profile()
        profiler.enable()
        func(*args, **kwargs)
        profiler.disable()

        # Capture stats
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)

        self.profile_data[name] = stream.getvalue()

    def print_results(self):
        """Print timing results"""
        print(f"\n{C.HEADER}{C.BOLD}=== PERFORMANCE RESULTS ==={C.RESET}\n")

        for name, result in sorted(self.results.items()):
            status = C.SUCCESS if result.mean < 0.1 else (C.WARNING if result.mean < 0.5 else C.DANGER)
            print(f"{C.BOLD}{name}:{C.RESET}")
            print(f"  {status}Mean: {result.mean*1000:.2f}ms{C.RESET}")
            print(f"  Median: {result.median*1000:.2f}ms")
            print(f"  Min: {result.min_time*1000:.2f}ms | Max: {result.max_time*1000:.2f}ms")
            if result.stdev > 0:
                print(f"  StdDev: {result.stdev*1000:.2f}ms")
            print()

    def print_profile(self, name: str):
        """Print profile data for a function"""
        if name in self.profile_data:
            print(f"\n{C.HEADER}=== PROFILE: {name} ==={C.RESET}")
            print(self.profile_data[name])


def profile_save_load():
    """Profile save/load operations"""
    print(f"{C.INFO}Profiling Save/Load operations...{C.RESET}")
    profiler = PerformanceProfiler()

    # Create test game
    from vault_shelter_v6 import VaultGame
    game = VaultGame()

    # Profile save
    def save_test():
        from vault_shelter_v6 import save_game
        save_game(game, "test_profile_save.json")

    profiler.time_function("Save Game (empty)", save_test, iterations=5)

    # Add some dwellers and rooms
    for _ in range(20):
        game._event_new_arrival()

    profiler.time_function("Save Game (20 dwellers)", save_test, iterations=5)

    # Profile load
    def load_test():
        from vault_shelter_v6 import load_game
        load_game("test_profile_save.json")

    profiler.time_function("Load Game", load_test, iterations=5)

    # Profile JSON serialization directly
    from dataclasses import asdict
    def serialize_test():
        data = {
            "dwellers": [asdict(d) for d in game.dwellers],
            "resources": asdict(game.resources),
        }
        json.dumps(data)

    profiler.time_function("JSON Serialize", serialize_test, iterations=20)

    # Cleanup
    try:
        os.remove("test_profile_save.json")
    except:
        pass

    profiler.print_results()
    return profiler


def profile_event_generation():
    """Profile event generation"""
    print(f"{C.INFO}Profiling Event Generation...{C.RESET}")
    profiler = PerformanceProfiler()

    try:
        from event_generators import (
            generate_random_event, generate_quest_event,
            generate_disaster_event
        )

        profiler.time_function("Random Event", generate_random_event, iterations=100)
        profiler.time_function("Quest Event", generate_quest_event, iterations=50)
        profiler.time_function("Disaster Event", generate_disaster_event, iterations=50)

    except ImportError:
        print(f"{C.WARNING}Event generators not available{C.RESET}")

    # Profile turn processing
    from vault_shelter_v6 import VaultGame
    game = VaultGame()

    def process_turn_test():
        # Simplified turn processing
        game.day += 1
        for dweller in game.dwellers:
            dweller.happiness = max(0, min(100, dweller.happiness + 1))

    profiler.time_function("Turn Processing (simple)", process_turn_test, iterations=100)

    profiler.print_results()
    return profiler


def profile_ai_opponent():
    """Profile AI opponent system"""
    print(f"{C.INFO}Profiling AI Opponent...{C.RESET}")
    profiler = PerformanceProfiler()

    from ai_opponent import AIOpponent, AIConfig, Difficulty, RandomStrategy

    # Create test strategy
    class TestStrategy(RandomStrategy):
        def __init__(self):
            super().__init__(
                get_moves=lambda s: list(range(10)),
                evaluate=lambda s: -abs(s - 5),
                apply=lambda s, m: m,
                is_terminal=lambda s: s == 5
            )

    # Profile AI move selection
    config = AIConfig(difficulty=Difficulty.HARD, think_time_seconds=0)
    ai = AIOpponent("test", config, TestStrategy())

    def get_move_test():
        ai.get_move(0, list(range(10)))

    profiler.time_function("AI Get Move (Hard)", get_move_test, iterations=100)

    # Profile with learning
    def learn_test():
        ai.record_result(won=False, game_data={
            "player_moves": [1, 2, 3, 4, 5],
            "player_strategy": "aggressive"
        })

    profiler.time_function("AI Learn from Game", learn_test, iterations=50)

    # Profile minimax
    from ai_opponent import minimax
    strategy = TestStrategy()

    def minimax_test():
        minimax(strategy, 0, 5, True)

    profiler.time_function("Minimax (depth 5)", minimax_test, iterations=20)

    profiler.print_results()
    return profiler


def profile_karma_system():
    """Profile karma system"""
    print(f"{C.INFO}Profiling Karma System...{C.RESET}")
    profiler = PerformanceProfiler()

    try:
        from vault13.systems.karma import KarmaSystem, DecisionType

        karma = KarmaSystem()

        def record_decision_test():
            karma.record_decision(
                "test_game", f"event_{len(karma.profile.events)}",
                "Test decision", 5, DecisionType.VIRTUE
            )

        profiler.time_function("Record Decision", record_decision_test, iterations=100)

        def save_profile_test():
            karma.save_profile()

        profiler.time_function("Save Karma Profile", save_profile_test, iterations=20)

        def get_summary_test():
            karma.get_summary()

        profiler.time_function("Get Summary", get_summary_test, iterations=100)

    except ImportError:
        print(f"{C.WARNING}Karma system not available{C.RESET}")

    profiler.print_results()
    return profiler


def profile_game_imports():
    """Profile game import times"""
    print(f"{C.INFO}Profiling Game Import Times...{C.RESET}")
    profiler = PerformanceProfiler()

    games_to_test = [
        ("simulation_argument", "simulation_argument"),
        ("paradox_of_heap", "paradox_of_heap"),
        ("rokos_basilisk", "rokos_basilisk"),
        ("zenos_paradoxes", "zenos_paradoxes"),
        ("story_mode", "story_mode"),
    ]

    for name, module in games_to_test:
        # Remove from cache if present
        if module in sys.modules:
            del sys.modules[module]

        def import_test():
            import importlib
            if module in sys.modules:
                del sys.modules[module]
            importlib.import_module(module)

        with profiler.timer(f"Import {name}"):
            import_test()

    profiler.print_results()
    return profiler


def full_profile():
    """Run all profiling tests"""
    clear_screen()
    print(f"{C.HEADER}{C.BOLD}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║            VAULT 13 PERFORMANCE PROFILER                       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{C.RESET}\n")

    results = []

    results.append(("Game Imports", profile_game_imports()))
    results.append(("Save/Load", profile_save_load()))
    results.append(("Event Generation", profile_event_generation()))
    results.append(("AI Opponent", profile_ai_opponent()))
    results.append(("Karma System", profile_karma_system()))

    # Summary
    print(f"\n{C.HEADER}{C.BOLD}=== SUMMARY ==={C.RESET}\n")

    for category, profiler in results:
        print(f"{C.BOLD}{category}:{C.RESET}")
        for name, result in sorted(profiler.results.items()):
            status = "✓" if result.mean < 0.1 else ("⚠" if result.mean < 0.5 else "✗")
            print(f"  {status} {name}: {result.mean*1000:.2f}ms")
        print()

    print(f"{C.SUCCESS}Profiling complete!{C.RESET}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="VAULT 13 Performance Profiler")
    parser.add_argument("--full", action="store_true", help="Run all profiling tests")
    parser.add_argument("--save-load", action="store_true", help="Profile save/load operations")
    parser.add_argument("--events", action="store_true", help="Profile event generation")
    parser.add_argument("--ai", action="store_true", help="Profile AI opponent")
    parser.add_argument("--karma", action="store_true", help="Profile karma system")
    parser.add_argument("--imports", action="store_true", help="Profile game imports")

    args = parser.parse_args()

    if args.full or not any([args.save_load, args.events, args.ai, args.karma, args.imports]):
        full_profile()
    else:
        if args.save_load:
            profile_save_load()
        if args.events:
            profile_event_generation()
        if args.ai:
            profile_ai_opponent()
        if args.karma:
            profile_karma_system()
        if args.imports:
            profile_game_imports()


if __name__ == "__main__":
    main()
