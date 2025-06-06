"""Pytest configuration and fixtures for Inceptor tests."""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Fixtures
@pytest.fixture
def mock_ollama():
    """Mock Ollama API client."""
    mock = MagicMock()
    mock.generate.return_value = {
        'model': 'mistral:7b',
        'response': 'Mocked response',
        'done': True
    }
    return mock

@pytest.fixture
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / 'data'

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Prevent any HTTP requests from being made during tests."""
    def urlopen_mock(self, method, url, *args, **kwargs):
        raise RuntimeError(f"Unexpected HTTP request to {url}")
    
    monkeypatch.setattr('urllib3.connectionpool.HTTPConnectionPool.urlopen', urlopen_mock)
