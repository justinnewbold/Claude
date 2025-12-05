#!/usr/bin/env python3
"""
Tests for Tutorial System
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from tutorial_system import TutorialSystem, TutorialBuilder, TutorialStepType


@pytest.fixture
def temp_tutorial_dir():
    """Create temporary directory for tutorial data"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_tutorial(temp_tutorial_dir):
    """Create sample tutorial"""
    builder = TutorialBuilder('test_game')
    builder.add_info(
        id='step1',
        title='Welcome',
        message='Welcome to the game!'
    ).add_action(
        id='step2',
        title='First Action',
        message='Press M to open menu',
        required_action='open_menu'
    )

    tutorial_file = temp_tutorial_dir / 'test_game_tutorial.json'
    builder.build(tutorial_file)

    return tutorial_file


def test_tutorial_loading(sample_tutorial):
    """Test loading tutorial"""
    tutorial = TutorialSystem('test_game', tutorial_file=sample_tutorial)
    assert len(tutorial.steps) == 2
    assert tutorial.is_active()


def test_tutorial_progression(sample_tutorial):
    """Test tutorial step progression"""
    tutorial = TutorialSystem('test_game', tutorial_file=sample_tutorial)

    # First step should be info
    step = tutorial.get_current_step()
    assert step.id == 'step1'
    assert step.type == TutorialStepType.INFO

    # Complete first step
    tutorial.complete_current_step()

    # Should advance to second step
    step = tutorial.get_current_step()
    assert step.id == 'step2'
    assert step.type == TutorialStepType.ACTION


def test_tutorial_action_completion(sample_tutorial):
    """Test completing action-based tutorial step"""
    tutorial = TutorialSystem('test_game', tutorial_file=sample_tutorial)

    # Skip to action step
    tutorial.complete_current_step()

    # Wrong action shouldn't complete
    assert not tutorial.check_action('wrong_action')

    # Correct action should complete
    assert tutorial.check_action('open_menu')


def test_tutorial_skip(sample_tutorial):
    """Test skipping tutorial"""
    tutorial = TutorialSystem('test_game', tutorial_file=sample_tutorial)

    assert tutorial.is_active()
    tutorial.skip()
    assert not tutorial.is_active()
    assert tutorial.progress.skipped


def test_tutorial_restart(sample_tutorial):
    """Test restarting tutorial"""
    tutorial = TutorialSystem('test_game', tutorial_file=sample_tutorial)

    tutorial.complete_current_step()
    tutorial.complete_current_step()

    assert tutorial.progress.current_step == 2

    tutorial.restart()
    assert tutorial.progress.current_step == 0
    assert not tutorial.progress.completed
