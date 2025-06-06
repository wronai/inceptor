"""Test command line interface for Inceptor."""
import pytest
import json
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from inceptor.cli import cli
from inceptor.core import OllamaClient

class TestCLI:
    """Test suite for CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Fixture for invoking command-line interfaces."""
        return CliRunner()

    def test_cli_help(self, runner):
        """Test the CLI help command."""
        with patch('inceptor.cli.OllamaClient'):
            result = runner.invoke(cli, ['--help'])
            assert result.exit_code == 0
            assert 'Show this message and exit.' in result.output

    @patch('inceptor.cli.DreamArchitect')
    def test_cli_generate(self, mock_da_class, runner):
        """Test the generate command."""
        # Setup mock DreamArchitect instance
        mock_da = mock_da_class.return_value
        mock_da.inception.return_value = {
            'problem': 'test prompt',
            'architecture': {'test': 'test architecture'},
            'tasks': [],
            'implementation': {},
            'metadata': {}
        }
        
        # Setup mock Ollama client
        with patch('inceptor.cli.OllamaClient') as mock_ollama:
            mock_ollama.return_value.generate.return_value = 'test response'
            
            # Test with prompt as argument
            result = runner.invoke(cli, ['generate', 'test prompt'])
            assert result.exit_code == 0
            assert 'test prompt' in result.output
            
            # Test with prompt via interactive input
            result = runner.invoke(cli, ['generate'], input='test prompt\n')
            assert result.exit_code == 0
            assert 'test prompt' in result.output
            
            # Verify the mock was called
            mock_da.inception.assert_called()

    @patch('inceptor.cli.DreamArchitect')
    def test_cli_shell(self, mock_da_class, runner):
        """Test the interactive shell command (basic test)."""
        # Setup mock DreamArchitect instance
        mock_da = mock_da_class.return_value
        mock_da.inception.return_value = {
            'problem': 'test prompt',
            'architecture': {},
            'tasks': [],
            'implementation': {},
            'metadata': {}
        }
        
        # Setup mock Ollama client
        with patch('inceptor.cli.OllamaClient') as mock_ollama:
            mock_ollama.return_value.generate.return_value = 'test response'
            
            # Test shell with exit command
            result = runner.invoke(cli, ['shell'], input='exit\n')
            assert result.exit_code == 0
            assert 'Goodbye!' in result.output
