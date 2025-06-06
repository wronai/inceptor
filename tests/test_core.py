"""Test core functionality of Inceptor."""
import pytest
from inceptor.core import DreamArchitect

class TestDreamArchitect:
    """Test suite for DreamArchitect class."""

    def test_init(self):
        """Test initialization of DreamArchitect."""
        architect = DreamArchitect()
        assert architect is not None

    def test_inception_architecture(self):
        """Test basic architecture generation."""
        architect = DreamArchitect()
        result = architect.inception("test prompt")
        assert hasattr(result, 'problem')
        assert hasattr(result, 'architecture')
        assert hasattr(result, 'tasks')
        assert hasattr(result, 'implementation')
        assert hasattr(result, 'metadata')
