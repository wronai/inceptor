#!/usr/bin/env python3
"""
DreamArchitect CLI - Interactive Shell Client
Requires: pip install click rich tabulate pyyaml
"""

import click
import json
import yaml
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import subprocess
from dataclasses import asdict

# Rich for beautiful output
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.tree import Tree
from rich.json import JSON

# Import our DreamArchitect library
try:
    from inceptor import DreamArchitect, quick_solution, analyze_context, Solution
except ImportError:
    print("❌ DreamArchitect library not found. Make sure it's in your Python path.")
    sys.exit(1)

console = Console()


class DreamCLI:
    """Interactive CLI for DreamArchitect"""

    def __init__(self):
        self.config_file = Path.home() / '.dream_architect_config.yaml'
        self.history_file = Path.home() / '.dream_architect_history.json'
        self.config = self.load_config()
        self.architect = DreamArchitect(self.config.get('ollama_url', 'http://localhost:11434'))
        self.history = self.load_history()

    def load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            'ollama_url': 'http://localhost:11434',
            'default_levels': 3,
            'output_format': 'rich',
            'auto_save': True,
            'workspace': str(Path.home() / 'dream_architect_workspace')
        }

        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                return {**default_config, **config}
        else:
            self.save_config(default_config)
            return default_config

    def save_config(self, config: Dict):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def load_history(self) -> list:
        """Load command history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_history(self):
        """Save command history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-100:], f, indent=2)  # Keep last 100 entries

    def add_to_history(self, command: str, result: Any):
        """Add command to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'success': result is not None
        }
        self.history.append(entry)
        if self.config.get('auto_save', True):
            self.save_history()


class DreamShell:
    """Interactive shell for DreamArchitect"""

    def __init__(self):
        self.cli = DreamCLI()
        self.current_solution: Optional[Solution] = None
        self.workspace = Path(self.cli.config.get('workspace', './dream_workspace'))
        self.workspace.mkdir(exist_ok=True)

    def show_banner(self):
        """Display welcome banner"""
        banner = """
╔══════════════════════════════════════╗
║        🌀 DREAM ARCHITECT CLI        ║
║   Multi-Level Solution Generator     ║
║        Powered by Mistral:7b         ║
╚══════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold blue"))
        console.print("Type 'help' for commands or 'exit' to quit\n")

    def cmd_help(self):
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

    def cmd_dream(self, problem: str, levels: int = None):
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

    def cmd_quick(self, problem: str):
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

    def cmd_context(self, text: str):
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

    def cmd_show(self):
        """Show current solution"""
        if not self.current_solution:
            console.print("❌ No solution loaded. Use 'dream' command first.", style="red")
            return

        self.show_solution_summary()

        detail = Prompt.ask("Show details for",
                            choices=["limbo", "dream", "reality", "deeper", "deepest", "all", "none"], default="none")

        if detail != "none":
            self.show_solution_detail(detail)

    def cmd_save(self, name: str = None):
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

    def cmd_load(self, name: str):
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

    def cmd_export(self, format_type: str = "json"):
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

    def cmd_workspace(self):
        """Open workspace directory"""
        console.print(f"📁 Workspace: [bold]{self.workspace}[/bold]")

        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", str(self.workspace)])
        elif sys.platform == "win32":  # Windows
            subprocess.run(["explorer", str(self.workspace)])
        else:  # Linux
            subprocess.run(["xdg-open", str(self.workspace)])

    def cmd_history(self):
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

    def cmd_config(self):
        """Show/edit configuration"""
        table = Table(title="Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")

        for key, value in self.cli.config.items():
            table.add_row(key, str(value))

        console.print(table)

        if Confirm.ask("Edit configuration?"):
            self.edit_config()

    def cmd_status(self):
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

    def cmd_levels(self, levels: int):
        """Set default architecture levels"""
        if levels < 1 or levels > 5:
            console.print("❌ Levels must be between 1 and 5", style="red")
            return

        self.cli.config['default_levels'] = levels
        self.cli.save_config(self.cli.config)
        console.print(f"✅ Default levels set to: {levels}")

    def show_solution_summary(self):
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

    def show_solution_detail(self, level: str):
        """Show detailed view of specific level"""
        if not self.current_solution or not hasattr(self.current_solution, 'architecture'):
            return

        if level == "all":
            data = asdict(self.current_solution)
        else:
            data = self.current_solution.architecture.get(level, {})

        console.print(Panel(JSON(json.dumps(data, indent=2)), title=f"{level.upper()} Details"))

    def export_implementation_files(self):
        """Export implementation files to workspace"""
        if not hasattr(self.current_solution, 'implementation'):
            console.print("❌ No implementation to export.", style="red")
            return

        export_dir = self.workspace / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        export_dir.mkdir(exist_ok=True)

        # This would need to be implemented based on the actual structure
        # of the implementation data from the DreamArchitect
        console.print(f"📁 Files would be exported to: {export_dir}")

    def edit_config(self):
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

    def run(self):
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
def cli():
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
def dream(problem, levels, output):
    """Generate solution architecture"""
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
@click.option('--context', '-c', help='JSON string with custom context', default='{}')
@click.option('--levels', '-l', default=4, help='Architecture depth (1-5)')
@click.option('--output', '-o', type=click.Choice(['json', 'yaml', 'summary']), default='summary')
def generate(problem, context, levels, output):
    """Generate solution architecture with custom context
    
    Example:
        inceptor generate "CI/CD pipeline for a Python microservice" \
            --context '{"cloud_provider": "aws", "container_orchestrator": "kubernetes"}'
    """
    try:
        # Parse the context JSON string
        context_dict = json.loads(context)
        
        architect = DreamArchitect()
        console.print(f"🌀 Generating {levels}-level architecture with custom context...")
        
        solution = architect.inception(
            problem,
            max_levels=levels,
            additional_context=context_dict
        )

        if output == 'json':
            console.print(JSON(json.dumps(asdict(solution), indent=2)))
        elif output == 'yaml':
            console.print(Syntax(yaml.dump(asdict(solution), default_flow_style=False), "yaml"))
        else:
            console.print(f"✅ Solution generated for: [bold]{problem}[/bold]")
            console.print(f"📊 Levels: {levels}")
            console.print(f"🏗️  Components: {len(solution.architecture.get('limbo', {}).get('components', []))}")
            console.print("\nCustom context used:")
            console.print_json(data=context_dict)

    except json.JSONDecodeError:
        console.print("❌ Error: Invalid JSON in context parameter", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")
        sys.exit(1)


@cli.command()
def status():
    """Check system status"""
    try:
        architect = DreamArchitect()
        response = architect.ollama.generate("test", max_tokens=1)
        console.print("✅ System Status: [green]OK[/green]")
    except Exception as e:
        console.print(f"❌ System Status: [red]FAILED[/red] - {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()