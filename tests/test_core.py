"""Test core functionality of Inceptor."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from inceptor.core import DreamArchitect, OllamaClient, ContextExtractor

class TestDreamArchitect:
    """Test suite for DreamArchitect class."""

    @patch('inceptor.core.OllamaClient')
    @patch('inceptor.core.ContextExtractor')
    def test_init(self, mock_extractor, mock_ollama):
        """Test initialization of DreamArchitect."""
        # Setup mocks
        mock_ollama.return_value = MagicMock()
        mock_extractor.return_value = MagicMock()
        
        # Test initialization
        architect = DreamArchitect()
        
        # Assertions
        assert architect is not None
        mock_ollama.assert_called_once()
        mock_extractor.assert_called_once()

    @patch('inceptor.core.OllamaClient')
    @patch('inceptor.core.ContextExtractor')
    def test_inception_architecture(self, mock_extractor, mock_ollama):
        """Test basic architecture generation."""
        # Setup mocks
        mock_ollama_instance = MagicMock()
        mock_ollama.return_value = mock_ollama_instance
        mock_ollama_instance.generate.return_value = '{"response": "test response"}'
        
        mock_extractor_instance = MagicMock()
        mock_extractor.return_value = mock_extractor_instance
        mock_extractor_instance.extract_context.return_value = {}
        mock_extractor_instance.enrich_context.return_value = {}
        
        # Initialize DreamArchitect with mocks
        architect = DreamArchitect()
        
        # Call the method under test
        result = architect.inception("test prompt")
        
        # Assertions
        assert hasattr(result, 'problem')
        assert hasattr(result, 'architecture')
        assert hasattr(result, 'tasks')
        assert hasattr(result, 'implementation')
        assert hasattr(result, 'metadata')
        
        # Verify mocks were called
        mock_extractor_instance.extract_context.assert_called_once()
        mock_ollama_instance.generate.assert_called()
