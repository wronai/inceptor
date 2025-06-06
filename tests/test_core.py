"""Test core functionality of Inceptor."""
import pytest
from inceptor.core import DreamArchitect

class TestDreamArchitect:
    """Test suite for DreamArchitect class."""

    def test_init(self):
        """Test initialization of DreamArchitect."""
        architect = DreamArchitect()
        assert architect is not None

    def test_generate_architecture(self):
        """Test basic architecture generation."""
        architect = DreamArchitect()
        result = architect.generate("test prompt")
        assert isinstance(result, dict)
        assert "levels" in result
        assert isinstance(result["levels"], list)
