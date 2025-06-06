"""Test command line interface for Inceptor."""
import pytest
from click.testing import CliRunner
from inceptor.cli import cli

class TestCLI:
    """Test suite for CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Fixture for invoking command-line interfaces."""
        return CliRunner()

    def test_cli_help(self, runner):
        """Test the CLI help command."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Show this message and exit.' in result.output

    def test_cli_generate(self, runner):
        """Test the generate command."""
        result = runner.invoke(cli, ['generate', 'test prompt'])
        assert result.exit_code == 0
        assert 'test prompt' in result.output

    @pytest.mark.skip(reason="Interactive shell test needs mocking")
    def test_cli_shell(self, runner):
        """Test the interactive shell command (basic test)."""
        result = runner.invoke(cli, ['shell'], input='exit\n')
        assert result.exit_code == 0
