#!/usr/bin/env python3
"""
Tests for Mod Loader
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import json

from mod_loader import ModLoader, ModCreator, ModStatus


@pytest.fixture
def temp_mods_dir():
    """Create temporary mods directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_mod(temp_mods_dir):
    """Create a sample mod"""
    ModCreator.create_mod_template(
        mod_id='test_mod',
        name='Test Mod',
        author='Test Author',
        game_id='test_game',
        output_dir=temp_mods_dir
    )
    return temp_mods_dir / 'test_mod'


def test_mod_creation(sample_mod):
    """Test mod template creation"""
    assert sample_mod.exists()
    assert (sample_mod / 'mod.json').exists()
    assert (sample_mod / 'data').exists()
    assert (sample_mod / 'mod.py').exists()


def test_mod_discovery(temp_mods_dir, sample_mod):
    """Test mod discovery"""
    loader = ModLoader('test_game', mods_dir=temp_mods_dir)
    mod_dirs = loader.discover_mods()

    assert len(mod_dirs) == 1
    assert sample_mod in mod_dirs


def test_mod_loading(temp_mods_dir, sample_mod):
    """Test loading mods"""
    loader = ModLoader('test_game', mods_dir=temp_mods_dir)
    loader.load_all_mods()

    assert 'test_mod' in loader.mods
    mod = loader.get_mod('test_mod')
    assert mod.metadata.name == 'Test Mod'
    assert mod.status == ModStatus.LOADED


def test_mod_data_loading(temp_mods_dir, sample_mod):
    """Test loading mod data files"""
    loader = ModLoader('test_game', mods_dir=temp_mods_dir)
    loader.load_all_mods()

    mod = loader.get_mod('test_mod')
    assert 'items' in mod.data
    assert 'example_items' in mod.data['items']


def test_mod_enable_disable(temp_mods_dir, sample_mod):
    """Test enabling and disabling mods"""
    loader = ModLoader('test_game', mods_dir=temp_mods_dir)
    loader.load_all_mods()

    loader.disable_mod('test_mod')
    mod = loader.get_mod('test_mod')
    assert mod.status == ModStatus.DISABLED

    loader.enable_mod('test_mod')
    assert mod.metadata.enabled


def test_mod_status_summary(temp_mods_dir, sample_mod):
    """Test getting mod status summary"""
    loader = ModLoader('test_game', mods_dir=temp_mods_dir)
    loader.load_all_mods()

    summary = loader.get_status_summary()
    assert summary['total'] == 1
    assert summary['loaded'] == 1
    assert summary['error'] == 0
