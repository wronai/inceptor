#!/usr/bin/env python3
"""
Inceptor CLI - Command Line Interface
"""
# Standard library imports
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import asdict
from typing import Optional, Dict, Any, List, Union, cast

# Third-party imports
import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.json import JSON
from rich.table import Table
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn

# Local application imports
from .core import DreamArchitect
from .core.models import Solution, Level, Component, Relationship

# Initialize console for rich output
console = Console()


class CLI:
    """Command Line Interface for Inceptor"""
    
    def __init__(self) -> None:
        self.architect = DreamArchitect()
        self.current_solution: Optional[Solution] = None
        self.history: List[Dict[str, Any]] = []
        self.workspace_dir: Path = Path.home() / ".inceptor"


def print_help() -> None:
    """Print help message"""
    help_text = """
Inceptor - AI-Powered Multi-Level Solution Architecture Generator

Usage:
  inceptor [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate  Generate solution architecture
  shell     Start interactive shell
  help      Show this help message
    """
    click.echo(help_text)


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """Inceptor CLI - Multi-Level Solution Architecture Generator"""
    ctx.obj = CLI()


@cli.command()
@click.argument('prompt', required=False)
@click.pass_obj
def generate(cli_obj: CLI, prompt: Optional[str] = None) -> None:
    """Generate solution architecture"""
    if not prompt:
        prompt = click.prompt('Enter your architecture description', type=str)
    
    result = cli_obj.architect.generate(prompt)
    click.echo(f"Generated architecture for: {result['prompt']}")
    for level in result['levels']:
        click.echo(f"- {level['name']}: {level['description']}")
    return result


@cli.command()
def shell() -> None:
    """Start interactive shell"""
    click.echo("Starting interactive shell... (Not implemented yet)")
    click.echo("Type 'exit' to quit.")
    while True:
        try:
            cmd = click.prompt('inceptor> ', type=str)
            if cmd.lower() in ('exit', 'quit'):
                break
            # Add more commands here
            click.echo(f"Command: {cmd}")
        except (KeyboardInterrupt, EOFError):
            break
    click.echo("Goodbye!")


if __name__ == "__main__":
    cli()
    def cmd_help(self) -> None:
        """Show help"""
        table = Table(title="Available Commands")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Example", style="green")

        commands = [
            ("dream <problem>", "Generate solution architecture", "dream 'logging system for Flask app'"),
            ("quick <problem>", "Quick 3-level solution", "quick 'CI/CD pipeline'"),
            ("context <text>", "Analyze context from text", "context 'urgent Python security audit'"),
            ("levels <1-5>", "Set architecture depth", "levels 4"),
            ("show", "Display current solution", "show"),
            ("save [name]", "Save solution to file", "save my_logging_system"),
            ("load <name>", "Load solution from file", "load my_logging_system"),
            ("export <format>", "Export (json/yaml/files)", "export files"),
            ("workspace", "Open workspace directory", "workspace"),
            ("history", "Show command history", "history"),
            ("config", "Show/edit configuration", "config"),
            ("status", "Check Ollama connection", "status"),
            ("clear", "Clear screen", "clear"),
            ("exit", "Exit shell", "exit")
        ]

        for cmd, desc, example in commands:
            table.add_row(cmd, desc, example)

        console.print(table)

    def cmd_dream(self, problem: str, levels: int = None) -> None:
        """Generate dream architecture"""
        if not problem:
            problem = Prompt.ask("Enter your problem description")

        levels = levels or self.cli.config.get('default_levels', 3)

        console.print(f"🌀 Generating {levels}-level architecture for: [bold]{problem}[/bold]")

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
        ) as progress:
            task = progress.add_task("Thinking...", total=None)

            try:
                progress.update(task, description="Level 1: Meta-Architecture...")
                self.current_solution = self.cli.architect.inception(problem, max_levels=levels)
                progress.update(task, description="Complete!")

                self.cli.add_to_history(f"dream '{problem}' levels={levels}", self.current_solution)
                self.show_solution_summary()

            except Exception as e:
                console.print(f"❌ Error: {str(e)}", style="red")
                self.cli.add_to_history(f"dream '{problem}' levels={levels}", None)

    def cmd_quick(self, problem: str) -> None:
        """Quick 3-level solution"""
        if not problem:
            problem = Prompt.ask("Enter your problem description")

        console.print(f"⚡ Quick solution for: [bold]{problem}[/bold]")

        try:
            result = quick_solution(problem, levels=3)
            console.print("✅ Solution generated!")
            console.print(JSON(json.dumps(result, indent=2)))
            self.cli.add_to_history(f"quick '{problem}'", result)
        except Exception as e:
            console.print(f"❌ Error: {str(e)}", style="red")

    def cmd_context(self, text: str) -> None:
        """Analyze context"""
        if not text:
            text = Prompt.ask("Enter text to analyze")

        context = analyze_context(text)

        table = Table(title="Context Analysis")
        table.add_column("Category", style="cyan")
        table.add_column("Detected", style="green")

        for category, items in context.items():
            if items:
                table.add_row(category.title(), ", ".join(items))

        console.print(table)
        self.cli.add_to_history(f"context '{text}'", context)

    def cmd_show(self) -> None:
        """Show current solution"""
        if not self.current_solution:
            console.print("❌ No solution loaded. Use 'dream' command first.", style="red")
            return

        self.show_solution_summary()

        detail = Prompt.ask("Show details for",
                            choices=["limbo", "dream", "reality", "deeper", "deepest", "all", "none"], default="none")

        if detail != "none":
            self.show_solution_detail(detail)

    def cmd_save(self, name: str = None) -> None:
        """Save current solution"""
        if not self.current_solution:
            console.print("❌ No solution to save.", style="red")
            return

        if not name:
            name = Prompt.ask("Enter solution name", default=f"solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

        save_path = self.workspace / f"{name}.yaml"

        with open(save_path, 'w') as f:
            yaml.dump(asdict(self.current_solution), f, default_flow_style=False)

        console.print(f"✅ Solution saved to: [bold]{save_path}[/bold]")

    def cmd_load(self, name: str) -> None:
        """Load solution from file"""
        if not name:
            # Show available solutions
            solutions = list(self.workspace.glob("*.yaml"))
            if not solutions:
                console.print("❌ No saved solutions found.", style="red")
                return

            table = Table(title="Saved Solutions")
            table.add_column("Name", style="cyan")
            table.add_column("Modified", style="white")

            for sol in solutions:
                table.add_row(sol.stem, datetime.fromtimestamp(sol.stat().st_mtime).strftime('%Y-%m-%d %H:%M'))

            console.print(table)
            name = Prompt.ask("Enter solution name to load")

        load_path = self.workspace / f"{name}.yaml"

        if not load_path.exists():
            console.print(f"❌ Solution '{name}' not found.", style="red")
            return

        with open(load_path, 'r') as f:
            data = yaml.safe_load(f)
            # Reconstruct Solution object (simplified)
            self.current_solution = type('Solution', (), data)

        console.print(f"✅ Solution '{name}' loaded.")

    def cmd_export(self, format_type: str = "json") -> None:
        """Export current solution"""
        if not self.current_solution:
            console.print("❌ No solution to export.", style="red")
            return

        if format_type == "files":
            self.export_implementation_files()
        elif format_type == "json":
            output = json.dumps(asdict(self.current_solution), indent=2)
            console.print(Syntax(output, "json"))
        elif format_type == "yaml":
            output = yaml.dump(asdict(self.current_solution), default_flow_style=False)
            console.print(Syntax(output, "yaml"))
        else:
            console.print(f"❌ Unknown format: {format_type}")

    def cmd_workspace(self) -> None:
        """Open workspace directory"""
        console.print(f"📁 Workspace: [bold]{self.workspace}[/bold]")

        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", str(self.workspace)])
        elif sys.platform == "win32":  # Windows
            subprocess.run(["explorer", str(self.workspace)])
        else:  # Linux
            subprocess.run(["xdg-open", str(self.workspace)])

    def cmd_history(self) -> None:
        """Show command history"""
        table = Table(title="Command History")
        table.add_column("Time", style="cyan")
        table.add_column("Command", style="white")
        table.add_column("Status", style="green")

        for entry in self.cli.history[-10:]:  # Last 10 entries
            status = "✅" if entry['success'] else "❌"
            time_str = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
            table.add_row(time_str, entry['command'][:50], status)

        console.print(table)

    def cmd_config(self) -> None:
        """Show/edit configuration"""
        table = Table(title="Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")

        for key, value in self.cli.config.items():
            table.add_row(key, str(value))

        console.print(table)

        if Confirm.ask("Edit configuration?"):
            self.edit_config()

    def cmd_status(self) -> None:
        """Check Ollama connection"""
        try:
            # Try to connect to Ollama
            response = self.cli.architect.ollama.generate("test", max_tokens=1)
            console.print("✅ Ollama connection: [green]OK[/green]")
            console.print(f"📍 URL: {self.cli.architect.ollama.base_url}")
            console.print(f"🤖 Model: {self.cli.architect.ollama.model}")
        except Exception as e:
            console.print("❌ Ollama connection: [red]FAILED[/red]")
            console.print(f"Error: {str(e)}")

    def cmd_levels(self, levels: int) -> None:
        """Set default architecture levels"""
        if levels < 1 or levels > 5:
            console.print("❌ Levels must be between 1 and 5", style="red")
            return

        self.cli.config['default_levels'] = levels
        self.cli.save_config(self.cli.config)
        console.print(f"✅ Default levels set to: {levels}")

    def show_solution_summary(self) -> None:
        """Display solution summary"""
        if not self.current_solution:
            return

        # Create tree view
        tree = Tree("🏗️ Architecture Overview")

        if hasattr(self.current_solution, 'architecture') and self.current_solution.architecture:
            for level, data in self.current_solution.architecture.items():
                level_tree = tree.add(f"📊 {level.upper()}")

                if level == 'limbo' and 'components' in data:
                    components_tree = level_tree.add("Components")
                    for comp in data['components']:
                        components_tree.add(f"• {comp.get('name', 'Unknown')} ({comp.get('priority', 'N/A')})")

        console.print(tree)

    def show_solution_detail(self, level: str) -> None:
        """Show detailed view of specific level"""
        if not self.current_solution or not hasattr(self.current_solution, 'architecture'):
            return

        if level == "all":
            data = asdict(self.current_solution)
        else:
            data = self.current_solution.architecture.get(level, {})

        console.print(Panel(JSON(json.dumps(data, indent=2)), title=f"{level.upper()} Details"))

    def export_implementation_files(self) -> None:
        """Export implementation files to workspace"""
        if not hasattr(self.current_solution, 'implementation'):
            console.print("❌ No implementation to export.", style="red")
            return

        export_dir = self.workspace / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        export_dir.mkdir(exist_ok=True)

        # This would need to be implemented based on the actual structure
        # of the implementation data from the DreamArchitect
        console.print(f"📁 Files would be exported to: {export_dir}")

    def edit_config(self) -> None:
        """Interactive configuration editor"""
        for key, current_value in self.cli.config.items():
            new_value = Prompt.ask(f"{key}", default=str(current_value))

            # Try to maintain type
            if isinstance(current_value, int):
                try:
                    self.cli.config[key] = int(new_value)
                except ValueError:
                    self.cli.config[key] = new_value
            elif isinstance(current_value, bool):
                self.cli.config[key] = new_value.lower() in ('true', 'yes', '1')
            else:
                self.cli.config[key] = new_value

        self.cli.save_config(self.cli.config)
        console.print("✅ Configuration saved!")

    def run(self) -> None:
        """Main shell loop"""
        self.show_banner()

        while True:
            try:
                command = Prompt.ask("[bold blue]dream>[/bold blue]").strip()

                if not command:
                    continue

                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                if cmd == 'exit' or cmd == 'quit':
                    console.print("👋 Goodbye!")
                    break
                elif cmd == 'help':
                    self.cmd_help()
                elif cmd == 'clear':
                    console.clear()
                elif cmd == 'dream':
                    problem = ' '.join(args) if args else None
                    self.cmd_dream(problem)
                elif cmd == 'quick':
                    problem = ' '.join(args) if args else None
                    self.cmd_quick(problem)
                elif cmd == 'context':
                    text = ' '.join(args) if args else None
                    self.cmd_context(text)
                elif cmd == 'show':
                    self.cmd_show()
                elif cmd == 'save':
                    name = args[0] if args else None
                    self.cmd_save(name)
                elif cmd == 'load':
                    name = args[0] if args else None
                    self.cmd_load(name)
                elif cmd == 'export':
                    format_type = args[0] if args else 'json'
                    self.cmd_export(format_type)
                elif cmd == 'workspace':
                    self.cmd_workspace()
                elif cmd == 'history':
                    self.cmd_history()
                elif cmd == 'config':
                    self.cmd_config()
                elif cmd == 'status':
                    self.cmd_status()
                elif cmd == 'levels':
                    if args:
                        try:
                            levels = int(args[0])
                            self.cmd_levels(levels)
                        except ValueError:
                            console.print("❌ Invalid number", style="red")
                    else:
                        console.print(f"Current levels: {self.cli.config.get('default_levels', 3)}")
                else:
                    console.print(f"❌ Unknown command: {cmd}. Type 'help' for available commands.", style="red")

            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!")
                break
            except Exception as e:
                console.print(f"❌ Error: {str(e)}", style="red")


@click.group()
def cli() -> None:
    """DreamArchitect CLI - Multi-Level Solution Generator"""
    pass


@cli.command()
def shell():
    """Start interactive shell"""
    shell = DreamShell()
    shell.run()


@cli.command()
@click.argument('problem')
@click.option('--levels', '-l', default=3, help='Architecture depth (1-5)')
@click.option('--output', '-o', type=click.Choice(['json', 'yaml', 'summary']), default='summary')
def dream(problem: str, levels: Optional[int], output: Optional[str]) -> int:
    """Generate solution architecture
    
    Args:
        problem: The problem description to generate a solution for
        levels: Number of architecture levels to generate
        output: Optional output file path to save the solution
        
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    architect = DreamArchitect()

    console.print(f"🌀 Generating {levels}-level architecture...")

    try:
        solution = architect.inception(problem, max_levels=levels)

        if output == 'json':
            console.print(JSON(json.dumps(asdict(solution), indent=2)))
        elif output == 'yaml':
            console.print(Syntax(yaml.dump(asdict(solution), default_flow_style=False), "yaml"))
        else:
            console.print(f"✅ Solution generated for: [bold]{problem}[/bold]")
            console.print(f"📊 Levels: {levels}")
            console.print(f"🏗️ Components: {len(solution.architecture.get('limbo', {}).get('components', []))}")

    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('text')
def context(text):
    """Analyze context from text"""
    result = analyze_context(text)

    table = Table(title="Context Analysis")
    table.add_column("Category", style="cyan")
    table.add_column("Detected", style="green")

    for category, items in result.items():
        if items:
            table.add_row(category.title(), ", ".join(items))

    console.print(table)


@cli.command()
@click.argument('problem')
@click.option('--context', '-c', help='JSON context for the generation')
@click.option('--levels', '-l', type=int, default=3, help='Number of architecture levels (1-5)')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def generate(problem: str, context: Optional[str], levels: int, output: Optional[str]) -> int:
    """Generate solution architecture with custom context
    
    Example:
        inceptor generate "CI/CD pipeline for a Python microservice" \
            --context '{"cloud_provider": "aws", "container_orchestrator": "kubernetes"}'
            
    Args:
        problem: The problem description to generate a solution for
        context: Optional JSON string containing additional context
        levels: Number of architecture levels to generate (1-5)
        output: Optional output file path to save the solution
        
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    cli = CLI()
    
    try:
        # Parse context if provided
        context_dict: Dict[str, Any] = {}
        if context:
            try:
                context_dict = json.loads(context)
            except json.JSONDecodeError:
                console.print("[red]Error: Invalid JSON context provided[/]")
                return 1
        
        # Generate solution
        with console.status("[bold green]Generating solution..."):
            solution = cli.architect.inception(
                problem=problem,
                context=context_dict,
                levels=levels
            )
        
        # Output results
        if output:
            with open(output, 'w') as f:
                json.dump(asdict(solution), f, indent=2)
            console.print(f"✅ Solution saved to {output}")
        else:
            console.print(Panel(
                f"[bold green]Solution Architecture[/]\n\n{json.dumps(asdict(solution), indent=2)}",
                title="Generated Solution"
            ))
            
        return 0
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/]")
        return 1


@cli.command()
def status() -> None:
    """Check system status
    
    Returns:
        None: Outputs status information to the console
    """
    try:
        # Check Ollama connection
        response = requests.get('http://localhost:11434/api/tags')
        response.raise_for_status()
        
        console.print("✅ [green]Ollama is running[/]")
        console.print(f"📡 API Version: {response.json().get('version', 'unknown')}")
    except requests.exceptions.RequestException as e:
        console.print(f"❌ [red]Ollama connection failed: {str(e)}[/]")
        console.print("Please make sure Ollama is installed and running (https://ollama.ai/)")
    except Exception as e:
        console.print(f"❌ [red]An unexpected error occurred: {str(e)}[/]")
        sys.exit(1)


if __name__ == "__main__":
    cli()